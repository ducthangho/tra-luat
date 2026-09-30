# ĐẶC TẢ — `R378-SYMLINK-DOI-DAC-QUYEN` — **revision 22, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `R378-SYMLINK-DOI-DAC-QUYEN` |
| `revision` | **22** |
| `thay_the_cho` | revision 21, `e83059b737f6e9c5b3c53c059266adb28d72fe7806e34a1dd81f7684ad54a0a8` |
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

### 0.14 — Vì sao có revision 15: ĐÓNG MIỀN CLI bằng một bảng hợp đồng, ca sinh từ bảng

Cross-review lượt 10 (codex `gpt-6-astra` medium) trên head `76f199e` theo r14: `blocked`, **P1 0 · P2 1 · P3 0 · P4 1**. Nguồn
của r15 — chủ kho 25-09-2026, trong phiên điều phối, bản chiếu `issues/574#issuecomment-5835624981`: *"r15 + g15, đóng miền CLI
(đề xuất)"* ⟦nguon:chi-thi⟧, giữ hạn `2026-09-26T06:00:00Z`.

- **F2 (P2), tiếp diễn — bảy đột biến sống:** `l10_first_file` · `l10_last_file` (chỉ duyệt tệp đầu / cuối), `l10_sum_overwrite`
  (ghi đè thay vì cộng dồn qua tệp), `l10_fixed_mau` (bỏ `--mau`; trên r14 thật `KHONG_DO_DUOC 33`), `l10_ham_endpoints` (`--ham`
  chỉ giữ tên đầu và cuối), `l10_drop_cli_label` (bỏ `CO_NHAN` khi tổng hợp), `l10_label_no_underscore` (markup `_` trước nhãn).
  Sáu cái đầu nằm ở đường CLI: ma trận r14 vẫn là DANH SÁCH điểm chọn tay, nên mỗi lượt reviewer tìm được một điểm ngoài nó.
- **P4:** Phụ lục H của r14 khai *"14 ca chạy CLI"* ⟦nguon:verdict⟧; đếm máy là 12. Con số gõ tay đã sai. Từ r15, mọi số ca trong
  lời dẫn được SINH từ dòng in của `tu-kiem` lúc dựng đặc tả.

**Đổi ở r15 — công cụ con trỏ v6, Phụ lục I, nguyên văn** (Phụ lục E–H giữ làm lịch sử). Chỉ `tu_kiem` đổi; phần văn bản trước
và sau `tu_kiem` bằng byte với v5. Mười hai ca CLI kê tay của r14 được THAY bằng các ca SINH từ bảng dưới.

**HỢP ĐỒNG CLI CỦA LỆNH `kiem` — bảng CÓ THẨM QUYỀN (từ r15).** `tu_kiem` sinh ca từ đúng các chiều này; oracle chỉ cộng véc tơ
kỳ vọng viết tay của từng tệp mẫu và so sánh, không gọi `kiem`, `main` hay biểu thức chính quy nào của cổng.

| chiều | miền trong bảng | kỳ vọng |
|---|---|---|
| argv | `kiem` + cờ + tệp, qua `main` trong tiến trình con | — |
| cờ `--nguon` / `--mau` | luôn có; `--mau` là mẫu tên RIÊNG (`spec-r{n}.txt`), khác mặc định | con trỏ phân giải theo đúng mẫu ấy |
| vị trí cờ so với tệp | trước mọi tệp · sau mọi tệp · xen giữa tệp đầu và phần còn lại | kết quả không phụ thuộc vị trí |
| số tệp | 1 · 2 (MỌI hoán vị có thứ tự của bảy tệp mẫu) · 3 (ba bộ chọn) · 7 (cả bảy) | — |
| tệp mẫu và véc tơ `(DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN)` | sạch `(1,0,0,0,0)` · lệch băm ×2 tệp khác nhau `(0,1,0,0,0)` · thiếu nguồn `(0,0,1,0,0)` · trích không nhãn `(0,0,0,1,0)` · nhãn thường `(0,0,0,0,1)` · nhãn sau `_…_` `(0,0,0,0,1)` | — |
| cộng dồn | mọi bộ đếm, qua mọi tệp, cùng loại và khác loại | tổng theo TỪNG phần tử |
| mã thoát | — | `1` khi `LECH + KHONG_DO_DUOC + VI_PHAM > 0`, ngược lại `0` |
| dòng `TONG` | — | đúng MỘT dòng bắt đầu `TONG `, có ĐỦ năm khoá |
| `--ham` trên tệp năm hàm `a`…`e`, hàm xấu `{a, c, e}` | 13 danh sách: một tên (đầu/giữa/cuối), hai, ba, năm tên; lỗi ở đầu, GIỮA, cuối; thứ tự đảo; tên NGOÀI tập (`zz`); cờ `--ham` trước và sau tệp | `VI_PHAM` = số tên trong danh sách thuộc `{a, c, e}`; tên ngoài tập không tính |
| không `--ham` trên cùng tệp | — | `VI_PHAM 3` |

**CHƯA ĐO — ngoài bảng, khai thẳng:** cờ lặp lại hai lần (giá trị sau thắng hay trước); cờ thiếu giá trị; `--nguon` không tồn
tại; tệp đầu vào không tồn tại hoặc không đọc được; đường dẫn có khoảng trắng; lệnh `sinh` và `tim`; mã hoá khác UTF-8. Không
chiều nào reviewer đã nêu nằm trong danh sách này.

**Đo, không suy (`rc` đọc trực tiếp):** `tu-kiem` in `TU_KIEM DAT 143/143 (truc tiep 62, CLI 81)` — 143 ca, trong đó 81 ca CLI sinh từ bảng, rc=0. **46 đột biến công cụ** — 39 của các lượt trước và 7 của lượt 10 —
mỗi cái một bản sao, một tiến trình: **cả 46 ĐỎ**. Cùng bảy đột biến lượt 10 trên v5: cả bảy `73/73`, rc=0 — tái lập bảng của
reviewer.

| đột biến (lượt 10) | ca đỏ đầu tiên ở v6 (danh sách đầy đủ trong nhật ký đo) |
|---|---|
| `l10_first_file` · `l10_last_file` · `l10_sum_overwrite` | `cli_co_sau_lech.md+lech2.md` — mong `LECH 2`, nhận 1 |
| `l10_fixed_mau` | mọi ca CLI có con trỏ, ví dụ `cli_co_truoc_lech.md` — nhận `KHONG_DO_DUOC` |
| `l10_ham_endpoints` | `cli_ham_b,c,d`, `cli_ham_d,c,b` — lỗi ở GIỮA |
| `l10_drop_cli_label` | `cli_co_truoc_nhan.md` — mong `CO_NHAN 1` |
| `l10_label_no_underscore` | `nhan_sau_gach_duoi`, `cli_co_truoc_nhan_gach.md` |

**Tiêu chí số:** N1–N3 của §0.13 giữ nguyên định nghĩa. Đo tại r15 bằng v6: N1 `143/143`, rc=0 · N2 `TONG {'DUNG': 33, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 24}`, rc=0 · N3 `TONG {'DUNG': 2, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 0}`, rc=0.

**Mã:** không đổi — head vẫn `76f199e`. **Không đổi ở r15:** mọi số hạng, `A1`–`A12`, Phụ lục A–H, §7, §9, `write_set`, điều
kiện dừng, hạn.

### 0.15 — Vì sao có revision 16: vị trí TỪNG cờ là một trục riêng, và phép phủ bảng được ĐO trên argv đã sinh

Cross-review lượt 11 (codex `gpt-6-astra` medium) trên head `76f199e` theo r15: `blocked`, **P1 0 · P2 1 · P3 0 · P4 0**. Nguồn
của r16 — chủ kho 26-09-2026, trong phiên điều phối, bản chiếu `issues/574#issuecomment-5842443596`: *"Mở r16 + g16 (đề xuất)"*
⟦nguon:chi-thi⟧, giữ hạn `2026-09-26T06:00:00Z`.

- **F2 (P2), tiếp diễn:** bảng §0.14 khai ô cờ `--ham` trước và sau tệp, nhưng bộ sinh r15 luôn đặt `--ham` TRƯỚC `h.py`
  (13 trước, 0 sau) — nhánh chẵn/lẻ chỉ đổi vị trí của `--nguon`/`--mau`. Đột biến `l11_ham_after_file` (bỏ `--ham` khi nó đứng
  sau một tệp) vẫn `143/143`. Lời khai của bảng rộng hơn thứ bộ sinh sinh ra — và không gì trong `tu_kiem` đối chiếu hai thứ ấy.

**Đổi ở r16 — công cụ con trỏ v7, Phụ lục J, nguyên văn** (Phụ lục E–I giữ làm lịch sử). Chỉ `tu_kiem` đổi; phần văn bản trước
và sau `tu_kiem` bằng byte với v6.

1. **Vị trí từng cờ là trục riêng, tách khỏi nội dung danh sách hàm:** mỗi danh sách trong 13 danh sách `--ham` chạy HAI lần —
   `--ham` trước chính tệp và `--ham` sau chính tệp; `--nguon`/`--mau` vẫn luân phiên trước/sau.
2. **Kiểm phủ bảng BẰNG MÁY trên argv đã sinh:** sau khi sinh, `tu_kiem` đọc lại argv THẬT của mọi ca CLI, tính cho mỗi ca các ô
   `(số tệp)` và `(vị trí của từng cờ so với các tệp: trước · xen · sau)`, rồi đòi mỗi ô của §0.14 có ít nhất một ca: số tệp
   1 · 2 · 3 · 7; `--nguon` và `--mau` mỗi cờ trước · xen · sau; `--ham` trước · sau. Thiếu một ô ⇒ `tu-kiem` ĐỎ với tên ô. Phép
   phủ đếm từ argv, không từ ý định của bộ sinh.
3. Bảng §0.14 GIỮ nguyên chữ và vẫn có thẩm quyền; ô `--ham` trước/sau nay có ca thật (ở r15 ô ấy là lời khai không có ca).

**Đo, không suy (`rc` đọc trực tiếp):** `tu-kiem` in `TU_KIEM DAT 156/156 (truc tiep 62, CLI 94)` — 156 ca, trong đó 94 ca CLI sinh từ bảng, rc=0. **48 đột biến**, mỗi cái một bản sao, một tiến trình, **cả 48
ĐỎ**: 46 đột biến công cụ của các lượt trước, `l11_ham_after_file` (đỏ ở `cli_ham_sau_*`), và một đột biến của CHÍNH bộ sinh —
chỉ sinh `--ham` trước tệp — đỏ DUY NHẤT ở phép phủ bảng (`PHU_BANG: o chua co ca: [('vi_tri--ham', 'sau')]`), tức phép phủ có
răng riêng. Cùng `l11_ham_after_file` trên v6: `143/143`, rc=0 — tái lập phản chứng của reviewer.

**Tiêu chí số:** N1–N3 của §0.13 giữ nguyên định nghĩa. Đo tại r16 bằng v7: N1 `156/156`, rc=0 · N2 `TONG {'DUNG': 33, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 25}`, rc=0 · N3 `TONG {'DUNG': 2, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 0}`, rc=0.

**Mã:** không đổi — head vẫn `76f199e`. **Không đổi ở r16:** mọi số hạng, `A1`–`A12`, bảng §0.14, Phụ lục A–I, §7, §9,
`write_set`, điều kiện dừng, hạn.

### 0.16 — Vì sao có revision 17: nhãn phải đứng NGAY sau câu trích của nó — ca trộn nhãn đúng / sai / thiếu

Cross-review lượt 12 (codex `gpt-6-astra` medium) trên head `76f199e` theo r16: `blocked`, **P1 0 · P2 1 · P3 0 · P4 0**. Nguồn
của r17 — chủ kho 26-09-2026, trong phiên điều phối, bản chiếu `issues/574#issuecomment-5843256803`: *"r17 + g17, nới hạn (đề
xuất)"* ⟦nguon:chi-thi⟧. **Hạn của g17 là `2026-09-27T06:00:00Z` — quyết định NỚI HẠN của chủ kho ghi tại mốc ấy**, không phải
executor tự nới; g16 vẫn hết hạn `2026-09-26T06:00:00Z`.

- **F2 (P2), vòng 6:** đột biến `NHAN.match(k, m.end())` → `NHAN.search(k, m.end())` — nhãn không còn phải đứng NGAY sau câu
  trích, chỉ cần có ĐÂU ĐÓ phía sau trong khối — vẫn `156/156`. Mọi ca nhãn của r16 chỉ có một câu trích mỗi khối.

**Đổi ở r17 — công cụ con trỏ v8, Phụ lục K, nguyên văn** (Phụ lục E–J giữ làm lịch sử). Chỉ `tu_kiem` đổi; phần văn bản trước
và sau `tu_kiem` bằng byte với v7. Thêm bảy ca, mỗi ca một khối có hai hoặc ba câu trích, mỗi câu mang nhãn hợp lệ, nhãn ngoài
danh sách, hoặc không nhãn; kỳ vọng viết tay: `VI_PHAM` = số câu không mang nhãn hợp lệ NGAY sau, `CO_NHAN` = số câu mang nhãn
hợp lệ ngay sau.

| ca | thứ tự trong khối | kỳ vọng `(DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN)` |
|---|---|---|
| `nhan_xau_truoc_nhan_dung` | sai · đúng | `(0,0,0,1,1)` |
| `nhan_dung_truoc_nhan_xau` | đúng · sai | `(0,0,0,1,1)` |
| `nhan_thieu_truoc_nhan_dung` | thiếu · đúng | `(0,0,0,1,1)` |
| `nhan_dung_truoc_nhan_thieu` | đúng · thiếu | `(0,0,0,1,1)` |
| `nhan_xau_thieu_dung` | sai · thiếu · đúng | `(0,0,0,2,1)` |
| `nhan_thieu_xau_dung` | thiếu · sai · đúng | `(0,0,0,2,1)` |
| `nhan_dung_xau_thieu` | đúng · sai · thiếu | `(0,0,0,2,1)` |

**Đo, không suy (`rc` đọc trực tiếp):** `tu-kiem` in `TU_KIEM DAT 163/163 (truc tiep 69, CLI 94)` — 163 ca, trong đó 94 ca CLI sinh từ bảng, rc=0. **49 đột biến**, mỗi cái một bản sao, một tiến trình, **cả 49
ĐỎ**: 48 của r16 (kể cả đột biến bộ sinh mà chỉ phép phủ bảng bắt) và `l12_nhan_search` — đỏ ở mọi ca có câu trích sai/thiếu
nhãn ĐỨNG TRƯỚC một câu có nhãn hợp lệ (`nhan_xau_truoc_nhan_dung`, `nhan_thieu_truoc_nhan_dung`, …). Cùng `l12_nhan_search` trên
v7: `156/156`, rc=0 — tái lập phản chứng của reviewer. Hoán vị đúng-trước-sai/thiếu không phân biệt `match` với `search` — giữ
làm ca hồi quy, không tính là răng.

**Tiêu chí số:** N1–N3 của §0.13 giữ nguyên định nghĩa; bảng §0.14 và phép phủ bảng của §0.15 giữ nguyên. Đo tại r17 bằng v8:
N1 `163/163`, rc=0 · N2 `TONG {'DUNG': 33, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 26}`, rc=0 · N3 `TONG {'DUNG': 2, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 0}`, rc=0.

**Mã:** không đổi — head vẫn `76f199e`. **Không đổi ở r17:** mọi số hạng, `A1`–`A12`, bảng §0.14, Phụ lục A–J, §7, §9,
`write_set`, điều kiện dừng. **Đổi:** hạn của lease (g17), theo quyết định chủ kho nêu trên.

### 0.17 — Vì sao có revision 18: bảng LỚP KHOẢNG NỐI câu–nhãn có thẩm quyền, ca sinh từ bảng

Cross-review lượt 13 (codex `gpt-6-astra` medium) trên head `76f199e` theo r17: `blocked`, **P1 0 · P2 1 · P3 0 · P4 0** (verdict
`pull/588#issuecomment-5843590964`; tái lập độc lập `issues/588#issuecomment-5843592704`). Nguồn của r18 — chủ kho 26-09-2026, trong
phiên điều phối, bản chiếu `issues/574#issuecomment-5843748247`: *"r18 + g18: bảng khoảng nối (đề xuất)"* ⟦nguon:chi-thi⟧. **Hạn của
g18 là `2026-09-27T06:00:00Z` — bằng hạn g17, không nới thêm** (mốc trên).

- **F2 (P2), vòng 7:** đột biến tiền tố của `NHAN` từ `[*_]*\s*` thành `[*_.,;:]*\s*` — dấu câu giữa câu trích và nhãn được coi
  như markup — vẫn `163/163`, rc=0; kiểm r17 và docstring vẫn như cũ. Bộ tự kiểm có ca dương cho markup và khoảng trắng nhưng
  không có ca âm cho dấu câu ngay tại khoảng nối.

**Đổi ở r18 — công cụ con trỏ v9, Phụ lục L, nguyên văn** (Phụ lục E–K giữ làm lịch sử). Chỉ `tu_kiem` đổi: phần văn bản trước
`def tu_kiem` và từ `def main` trở đi bằng byte với v8. Parser (`NHAN`, `Q`, `kiem`) KHÔNG đổi — mã #588 không đổi.

**Bảng lớp khoảng nối — CÓ THẨM QUYỀN.** Khoảng nối là đoạn giữa dấu ngoặc ĐÓNG của câu trích và nhãn. Markup phải ĐÓNG ngay sau
dấu ngoặc (cặp với markup MỞ trước câu) rồi mới tới khoảng trắng; khoảng trắng nằm trong cùng đoạn. Cực chỉ do bảng quyết định:
`DUONG` ⇒ kỳ vọng `(0,0,0,0,1)`, `AM` ⇒ `(0,0,0,1,0)` — oracle KHÔNG gọi regex nào của cổng. Bảng dưới do bộ dựng đặc tả đọc từ
chính khối mã v9 (không gõ tay), nên không trôi được khỏi mã:

| lớp | markup mở trước câu | khoảng nối | cực |
|---|---|---|---|
| `rong` | (rỗng) | (rỗng) | **DUONG** |
| `cach` | (rỗng) | `' '` | **DUONG** |
| `cach_nhieu` | (rỗng) | `'   '` | **DUONG** |
| `tab` | (rỗng) | `'\t'` | **DUONG** |
| `xuong_dong` | (rỗng) | `'\n'` | **DUONG** |
| `cach_xuong_dong` | (rỗng) | `' \n  '` | **DUONG** |
| `sao` | `'*'` | `'*'` | **DUONG** |
| `sao_cach` | `'*'` | `'* '` | **DUONG** |
| `gach` | `'_'` | `'_'` | **DUONG** |
| `gach_cach` | `'_'` | `'_ '` | **DUONG** |
| `sao_doi` | `'**'` | `'**'` | **DUONG** |
| `sao_doi_cach` | `'**'` | `'** '` | **DUONG** |
| `gach_doi_xuong_dong` | `'__'` | `'__\n'` | **DUONG** |
| `dau0` | (rỗng) | `';'` | **AM** |
| `dau1` | (rỗng) | `','` | **AM** |
| `dau2` | (rỗng) | `'.'` | **AM** |
| `dau3` | (rỗng) | `':'` | **AM** |
| `dau4` | (rỗng) | `'!'` | **AM** |
| `dau5` | (rỗng) | `'?'` | **AM** |
| `dau0_cach` | (rỗng) | `'; '` | **AM** |
| `dau1_cach` | (rỗng) | `', '` | **AM** |
| `dau2_cach` | (rỗng) | `'. '` | **AM** |
| `dau3_cach` | (rỗng) | `': '` | **AM** |
| `dau4_cach` | (rỗng) | `'! '` | **AM** |
| `dau5_cach` | (rỗng) | `'? '` | **AM** |
| `sao_roi_dau` | `'*'` | `'*; '` | **AM** |
| `cach_roi_dau` | (rỗng) | `' , '` | **AM** |
| `cach_roi_sao` | (rỗng) | `' *'` | **AM** |
| `chu` | (rỗng) | `' va '` | **AM** |
| `chu_dinh` | (rỗng) | `'x '` | **AM** |
| `noi_dung_xen` | (rỗng) | `' (ghi chu) '` | **AM** |
| `ngoac_dong` | (rỗng) | `') '` | **AM** |
| `gach_ngang` | (rỗng) | `' — '` | **AM** |
| `doan_moi` | (rỗng) | `'\n\n'` | **AM** |

Mỗi lớp sinh HAI ca — câu trích ngoặc thẳng và ngoặc cong, token `r1`, câu 8 ký tự, nhãn hợp lệ `ma` — tổng 68 ca. Ba ca đối
chứng viết tay: nhãn đứng TRƯỚC câu ⇒ `(0,0,0,1,0)`; hai nhãn hợp lệ liên tiếp sau một câu ⇒ `(0,0,0,0,1)`; nhãn ngoài danh sách
rồi nhãn hợp lệ sau CÙNG một câu ⇒ `(0,0,0,1,0)` (nhãn thứ hai không cứu câu).

**Kiểm phủ bằng máy, trên tệp ĐÃ SINH** (khoảng nối tách lại từ nội dung tệp, không đọc lại bảng): mỗi kiểu ngoặc phải có ô
`DUONG` cho khoảng trắng rỗng, dấu cách, tab, xuống dòng; cho markup `*` và `_` (có và không có khoảng trắng sau), `**` và `__`
(có khoảng trắng sau); ô `AM` cho TỪNG dấu trong `; , . : ! ?` (liền nhãn và kèm khoảng trắng), cho chữ xen, cho khoảng trắng
rồi markup, và cho dòng trống (đoạn mới). Thiếu một ô ⇒ `tu-kiem` ĐỎ.

**Đo, không suy (`rc` đọc trực tiếp):** `tu-kiem` in `TU_KIEM DAT 234/234 (truc tiep 140, CLI 94)` — 234 ca, trong đó 94 ca CLI sinh từ bảng §0.14 và 68 ca sinh từ bảng khoảng nối, rc=0. **64 đột biến** công cụ, mỗi cái một bản sao, một tiến trình,
**cả 64 ĐỎ**: 49 của r17, 11 đột biến tiền tố `NHAN` (dấu câu `.,;:` của reviewer; `!?`; ba ký tự bất kỳ; bỏ xuống dòng; bỏ tab;
markup trộn khoảng trắng; markup tối đa một ký tự; khoảng trắng bắt buộc; tối đa một khoảng trắng; chữ xen; ngoặc đóng) và 4 đột
biến BỘ SINH mà chỉ phép phủ bảng bắt (bỏ lớp dấu câu liền nhãn; chỉ một kiểu ngoặc; bỏ lớp `**`; bỏ lớp đoạn mới). Cùng 11 đột
biến tiền tố trên v8: 10 SỐNG `163/163`, rc=0 (kể cả đột biến của reviewer — tái lập phản chứng), chỉ markup-tối-đa-một-ký-tự
chết nhờ ca cũ `nhan_sau_markup_dam`.

**Tiêu chí số:** N1–N3 của §0.13 giữ nguyên định nghĩa; bảng §0.14, phép phủ bảng của §0.15 và các ca của §0.16 giữ nguyên. Đo
tại r18 bằng v9: N1 `234/234`, rc=0 · N2 `TONG {'DUNG': 33, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 27}`, rc=0 · N3 `TONG {'DUNG': 2, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 0}`, rc=0.

**Mã:** không đổi — head #588 vẫn `76f199e`. **Không đổi ở r18:** mọi số hạng, `A1`–`A12`, bảng §0.14, Phụ lục A–K, §7, §9,
`write_set`, điều kiện dừng, hạn lease.

### 0.18 — Vì sao có revision 19: parser CƯỠNG CHẾ cặp markup mở–đóng; bảng ranh giới code–văn bản

Cross-review lượt 14 (codex `gpt-6-astra` medium) trên head `76f199e` theo r18: `blocked`, **P1 0 · P2 2 · P3 0 · P4 0** (verdict
`pull/588#issuecomment-5844250968`; tái lập độc lập `issues/588#issuecomment-5844252966`). Nguồn của r19 — chủ kho 26-09-2026, trong
phiên điều phối, bản chiếu `issues/574#issuecomment-5844317341`: *"r19 + g19: sửa parser + ca code (đề xuất)"* ⟦nguon:chi-thi⟧. **Hạn
của g19 là `2026-09-27T06:00:00Z` — bằng hạn g18, không nới thêm** (mốc trên).

- **F3 (P2), lớp mới — sai hành vi của công cụ v9 GỐC:** §0.17 đòi markup đóng cặp với markup mở trước câu, nhưng `NHAN` chỉ nuốt
  một dãy `*`/`_` bất kỳ. Câu trích có markup đóng mà KHÔNG có markup mở, hoặc mở một loại đóng loại khác, vẫn được nhận nhãn.
- **F2 (P2), vòng 8:** đột biến `NHAN.match(k, m.end())` thành `NHAN.match(kc, m.end())` — đọc nhãn trên bản đã che code, nên một
  đoạn code xen giữa câu và nhãn biến thành khoảng trắng — vẫn `234/234`.

**Đổi ở r19 — công cụ con trỏ v10, Phụ lục M, nguyên văn** (Phụ lục E–L giữ làm lịch sử). **Lời khai *chỉ `tu_kiem` đổi* của các
revision trước KHÔNG áp cho r19:** parser đổi. Toàn bộ thay đổi NGOÀI `tu_kiem` so với v9, do bộ dựng đặc tả trích bằng máy:

```diff
--- v9 (Phụ lục L)
+++ v10 (Phụ lục M)
@@ -8 +8,2 @@
-  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac: chuoi ay KHONG phai loi cua mot revision (K thuoc
+  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac (markup giua cau va nhan chi duoc la markup DONG, dao nguoc dung
+            markup MO ngay truoc cau; tu r19): chuoi ay KHONG phai loi cua mot revision (K thuoc
@@ -23 +24,2 @@
-NHAN = re.compile(r"[*_]*\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
+NHAN = re.compile(r"([*_]*)\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
+MO = re.compile(r"[*_]*\Z")  # markup MO ngay truoc dau ngoac mo cua cau (r19)
@@ -89 +91,2 @@
-            if NHAN.match(k, m.end()): dem["CO_NHAN"] += 1; continue
+            n = NHAN.match(k, m.end())  # r19: markup DONG giua cau va nhan phai la dao nguoc DUNG markup MO ngay truoc cau
+            if n and n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1]: dem["CO_NHAN"] += 1; continue
```

Luật mới của `kiem`: nhãn chỉ được tính cho câu trích khi dãy markup giữa dấu ngoặc đóng và nhãn BẰNG ĐÚNG dãy markup ngay trước
dấu ngoặc mở, đọc ngược (`**`↔`**`, `*_`↔`_*`; rỗng↔rỗng). Thiếu mở, mở mà không đóng, khác loại, khác độ dài, sai thứ tự ⇒ ÂM.
Nhãn đọc trên văn bản GỐC (không che code) như trước.

**Văn bản thật không mất nhãn nào — đo, không suy.** Chạy v9 và v10 trên CÙNG đầu vào, so từng bộ đếm: đặc tả r1–r18 (18 tệp) và
docstring (`--ham` ba hàm của N3) — **cả 19 bằng nhau từng bộ đếm**; r18 `DUNG 33 · CO_NHAN 27 · VI_PHAM 0` ở cả hai.

**Bảng CẶP MARKUP — CÓ THẨM QUYỀN** (đọc từ chính khối mã v10). Cột: markup mở trước câu, khoảng nối (bắt đầu bằng markup đóng), cực:

| lớp | markup mở | khoảng nối | cực |
|---|---|---|---|
| `dung_sao` | `'*'` | `'*'` | **DUONG** |
| `dung_gach` | `'_'` | `'_ '` | **DUONG** |
| `dung_sao_doi` | `'**'` | `'** '` | **DUONG** |
| `dung_gach_doi` | `'__'` | `'__'` | **DUONG** |
| `dung_tron` | `'*_'` | `'_* '` | **DUONG** |
| `dung_tron_nguoc` | `'_*'` | `'*_'` | **DUONG** |
| `dung_ba` | `'***'` | `'*** '` | **DUONG** |
| `thieu_mo_sao` | (rỗng) | `'* '` | **AM** |
| `thieu_mo_gach` | (rỗng) | `'_'` | **AM** |
| `thieu_mo_doi` | (rỗng) | `'** '` | **AM** |
| `khac_loai_sao_gach` | `'*'` | `'_ '` | **AM** |
| `khac_loai_gach_sao` | `'_'` | `'*'` | **AM** |
| `khac_loai_doi` | `'**'` | `'__ '` | **AM** |
| `khac_loai_sai_thu_tu` | `'*_'` | `'*_ '` | **AM** |
| `dai_ngan` | `'**'` | `'* '` | **AM** |
| `ngan_dai` | `'*'` | `'** '` | **AM** |
| `gach_ngan_dai` | `'_'` | `'__'` | **AM** |
| `ba_hai` | `'***'` | `'** '` | **AM** |
| `mo_khong_dong_sao` | `'*'` | `' '` | **AM** |
| `mo_khong_dong_doi` | `'**'` | (rỗng) | **AM** |
| `mo_khong_dong_gach` | `'_'` | `'\n'` | **AM** |

**Bảng RANH GIỚI code–văn bản — CÓ THẨM QUYỀN** (`{q}` = câu trích; kỳ vọng viết tay: `DUONG` `(0,0,0,0,1)`, `AM` `(0,0,0,1,0)`,
`KHONG` `(0,0,0,0,0)`):

| lớp | mẫu (sau `Theo r1: `; `NL` = nhãn hợp lệ `ma`) | cực |
|---|---|---|
| `code_xen` | `` {q} `x` NL `` | **AM** |
| `code_lien_sau_cau` | `` {q}`x` NL `` | **AM** |
| `code_truoc_cau` | `` `x` {q} NL `` | **DUONG** |
| `cau_trong_code` | `` `{q}` NL `` | **KHONG** |
| `nhan_trong_code` | `` {q} `NL` `` | **AM** |
| `nhan_lien_sau_cau` | `` {q}NL `` | **DUONG** |
| `markup_roi_code_xen` | `` *{q}* `x` NL `` | **AM** |
| `markup_mo_trong_code` | `` `*`{q}* NL `` | **AM** |

Cả hai bảng sinh ca theo hai kiểu ngoặc — tổng 58 ca mới. **Kiểm phủ bằng máy trên tệp ĐÃ SINH** (loại ô tính lại từ nội dung
tệp, không đọc lại bảng): mỗi ô cặp markup là (loại cặp, tập ký tự markup tham gia, một hay nhiều ký tự) — `dung` cần `*`, `_`
một ký tự, `*`, `_` nhiều ký tự và `*_` trộn; `thieu_mo` cần `*`, `_` một ký tự và `*` nhiều ký tự; `khac_loai` cần `*_` một và nhiều
ký tự; `khac_do_dai` cần `*` và `_` nhiều ký tự; `mo_khong_dong` cần `*` một và nhiều ký tự, `_` một ký tự. Ranh giới cần câu trong
code, code trước câu, nhãn trong code, nhãn liền sau câu, và code xen giữa câu–nhãn ở ba dạng (không liền, liền sau câu, sau markup
đóng). Mọi ô cho cả hai kiểu ngoặc; thiếu một ô ⇒ `tu-kiem` ĐỎ. Bản đầu của phép phủ thô hơn (một ô cho mỗi loại cặp, một ô cho code
xen): ba đột biến BỘ SINH bỏ một phần lớp — bỏ `thieu_mo` một ký tự, bỏ `khac_loai` một ký tự, bỏ dòng code xen thường — SỐNG vì
dòng anh em còn phủ ô; ô đã được tách như trên trước khi đóng băng, và cả ba đột biến nay ĐỎ.

**Fixture của reviewer, đo trực tiếp** (`kiem`, `rc` đọc trực tiếp):

| fixture | v9 | v10 |
|---|---|---|
| markup đóng không có mở | `CO_NHAN 1`, rc=0 | `VI_PHAM 1`, rc=1 |
| mở `*` đóng `_` | `CO_NHAN 1`, rc=0 | `VI_PHAM 1`, rc=1 |
| cặp `*` đúng (đối chứng) | `CO_NHAN 1`, rc=0 | `CO_NHAN 1`, rc=0 |
| code xen giữa câu và nhãn | `VI_PHAM 1`, rc=1 | `VI_PHAM 1`, rc=1 |

**Đo đột biến:** `tu-kiem` in `TU_KIEM DAT 292/292 (truc tiep 198, CLI 94)` — 292 ca, trong đó 94 ca CLI sinh từ bảng §0.14, rc=0. **76 đột biến** công cụ, mỗi cái một bản sao, một tiến trình, **cả 76 ĐỎ**: 64 của r18 (neo của 15 đột biến chạm dòng `NHAN` và của `l12_nhan_search` đặt lại lên dòng mới, GIỮ Ý — tiền tố đột biến giữ nguyên, chỉ bọc nhóm bắt markup đóng) và 12 mới: `NHAN.match(kc, …)` của reviewer; gỡ kiểm cặp (hành vi v9); so cặp không đảo; chỉ so độ dài; chỉ so tập ký tự; cho phép đóng rỗng; cho phép mở rỗng; `MO` tối đa một ký tự; và 4 đột biến BỘ SINH (bỏ lớp thiếu mở; bỏ lớp khác loại; bỏ lớp code xen; bảng cặp chỉ một kiểu ngoặc).

**Tiêu chí số:** N1–N3 của §0.13 giữ nguyên định nghĩa; bảng §0.14, phép phủ của §0.15, ca §0.16 và bảng khoảng nối §0.17 giữ
nguyên. Đo tại r19 bằng v10: N1 `292/292`, rc=0 · N2 `TONG {'DUNG': 33, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 28}`, rc=0 · N3 `TONG {'DUNG': 2, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 0}`, rc=0.

**Mã:** không đổi — head #588 vẫn `76f199e`. **Không đổi ở r19:** mọi số hạng, `A1`–`A12`, bảng §0.14, Phụ lục A–L, §7, §9,
`write_set`, điều kiện dừng, hạn lease.

### 0.19 — Vì sao có revision 20: ba trục mới cho bộ tự kiểm — vị trí câu, lần xuất hiện, độ dài markup

Cross-review lượt 15 (codex `gpt-6-astra` medium) trên head `76f199e` theo r19: `blocked`, **P1 0 · P2 1 · P3 0 · P4 0** (verdict
`pull/588#issuecomment-5845017940`; tái lập độc lập `issues/588#issuecomment-5845024132`). Nguồn của r20 — chủ kho 26-09-2026, trong
phiên điều phối, bản chiếu `issues/574#issuecomment-5847155947`: *"r20 + g20: thêm trục (đề xuất)"* ⟦nguon:chi-thi⟧. **Hạn của g20 là
`2026-09-27T06:00:00Z` — bằng hạn g19, không nới.**

- **Đã đóng:** F3 (parser cưỡng chế cặp markup — reviewer đo trên nhiều fixture, không sai cực); biểu hiện F2 vòng 8 (`NHAN.match(kc, …)`
  đỏ). Reviewer chứng minh `MO.search(kc, …)` TƯƠNG ĐƯƠNG, không phải lỗ.
- **F2 (P2), tiếp diễn:** bộ tự kiểm chưa có trục vị trí câu và biên dòng, lần xuất hiện, và độ dài markup vượt mẫu. Sáu đột biến
  (`new_mo_dollar`, `new_mo_bound3`, `new_nhan_bound3`, `new_first_quote`, `new_first_end`, `new_lstrip`) vẫn cho `tu-kiem` 292/292.

**Đổi ở r20 — công cụ con trỏ v11, Phụ lục N, nguyên văn** (Phụ lục E–M giữ làm lịch sử). **Chỉ `tu_kiem` đổi:** phần trước
`def tu_kiem` và từ `def main` trở đi bằng byte với v10 (Phụ lục M) — parser (`NHAN`, `MO`, `Q`, `kiem`) KHÔNG đổi, nên số đếm trên
văn bản thật không thể đổi vì công cụ; mã #588 không đổi.

**Ba bảng mới — CÓ THẨM QUYỀN, đọc từ chính khối mã v11** (`{q}` = câu trích, `{mo}`/`{dong}` = markup mở/đóng, `NL` = nhãn hợp lệ
`ma`; kỳ vọng viết tay, chỉ đọc cực hoặc vecto, không gọi regex nào của cổng):

(1) **Vị trí câu** — mỗi vị trí × mỗi cặp markup:

| vị trí | mẫu |
|---|---|
| `dau_khoi` | `` {mo}{q}{dong} NL theo r1. `` |
| `thut_le` | ``   Theo r1: {mo}{q}{dong} NL. `` |
| `sau_dong_ket_markup` | `` Theo r1: *\n{mo}{q}{dong} NL. `` |
| `sau_dong_thuong` | `` Theo r1:\n{mo}{q}{dong} NL. `` |

| cặp | markup mở | markup đóng | cực |
|---|---|---|---|
| `khong` | (rỗng) | (rỗng) | **DUONG** |
| `sao` | `'*'` | `'*'` | **DUONG** |
| `sao_thieu_mo` | (rỗng) | `'*'` | **AM** |
| `sao_doi_lech` | `'**'` | `'*'` | **AM** |

(2) **Lần xuất hiện** — cùng nội dung hai lần trên một dòng, sau `Theo r1: `; vecto `(VI_PHAM, CO_NHAN)` viết tay:

| lớp | mẫu | `(VI_PHAM, CO_NHAN)` |
|---|---|---|
| `dung_roi_thieu_mo` | `` *{q}* NL; {q}* NL `` | `(1, 1)` |
| `thieu_mo_roi_dung` | `` {q}* NL; *{q}* NL `` | `(1, 1)` |
| `co_nhan_roi_khong` | `` {q} NL; {q} khong nhan `` | `(1, 1)` |
| `khong_roi_co_nhan` | `` {q} khong nhan; {q} NL `` | `(1, 1)` |
| `nhan_dung_roi_sai` | `` {q} NL; {q} NL_SAI `` | `(1, 1)` |
| `ca_hai_dung_khac_cap` | `` *{q}* NL; **{q}** NL `` | `(0, 2)` |

(3) **Độ dài markup ≥ 4** — sau `Theo r1: `:

| lớp | markup mở | markup đóng | cực |
|---|---|---|---|
| `bon_bon` | `'****'` | `'****'` | **DUONG** |
| `nam_nam` | `'*****'` | `'*****'` | **DUONG** |
| `gach_bon` | `'____'` | `'____'` | **DUONG** |
| `bon_ba` | `'****'` | `'***'` | **AM** |
| `ba_bon` | `'***'` | `'****'` | **AM** |
| `bon_nam` | `'****'` | `'*****'` | **AM** |

Mọi bảng sinh theo HAI kiểu ngoặc — tổng 56 ca mới. **Kiểm phủ bằng máy trên tệp ĐÃ SINH** (ô tính lại từ nội dung tệp):
vị trí câu (đầu khối, thụt lề, sau dòng kết thúc bằng markup, sau dòng thường) × cực dương/âm; lần xuất hiện: (câu thứ nhất tốt/xấu, câu thứ hai tốt/xấu, khác nhau ở
cặp markup hay ở nhãn) — tốt-xấu và xấu-tốt theo cả hai kiểu khác nhau, tốt-tốt khác cặp; độ dài: dãy ≥ 4 ký tự, cặp bằng và lệch độ dài — mọi ô cho cả hai kiểu ngoặc. Thiếu một ô ⇒ `tu-kiem` ĐỎ. Bản đầu của ô lần xuất hiện thô hơn (chỉ câu tốt đứng trước / câu xấu đứng trước): đột biến bộ sinh bỏ lớp đúng-rồi-thiếu-mở SỐNG vì lớp anh em còn phủ ô; ô đã được tách như trên trước khi đóng băng, và đột biến ấy nay ĐỎ.

**Đo, không suy (`rc` đọc trực tiếp):** `tu-kiem` in `TU_KIEM DAT 348/348 (truc tiep 254, CLI 94)` — 348 ca, trong đó 94 ca CLI sinh từ bảng §0.14, rc=0. **86 đột biến** công cụ, mỗi cái một bản sao, một tiến trình, **cả 86 ĐỎ**: 76 của r19, sáu đột biến của lượt 15 (neo/thay nguyên văn phụ lục verdict) và 4 đột biến BỘ SINH của ba bảng mới (bỏ vị trí thụt lề; bỏ lớp câu tốt đứng trước; bỏ cặp lệch độ dài; bảng vị trí chỉ một kiểu ngoặc) — chỉ phép phủ bắt. Cùng sáu đột biến lượt 15 trên v10: `l15_new_mo_dollar` rc=0 `TU_KIEM DAT 292/292`; `l15_new_mo_bound3` rc=0 `TU_KIEM DAT 292/292`; `l15_new_nhan_bound3` rc=0 `TU_KIEM DAT 292/292`; `l15_new_first_quote` rc=0 `TU_KIEM DAT 292/292`; `l15_new_first_end` rc=0 `TU_KIEM DAT 292/292`; `l15_new_lstrip` rc=0 `TU_KIEM DAT 292/292` — tái lập phản chứng của reviewer.

**Tiêu chí số:** N1–N3 của §0.13 giữ nguyên định nghĩa; bảng §0.14–§0.18 giữ nguyên. Đo tại r20 bằng v11: N1 `348/348`, rc=0 · N2 `TONG {'DUNG': 33, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 29}`, rc=0 · N3 `TONG {'DUNG': 2, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 0}`, rc=0.

**Mã:** không đổi — head #588 vẫn `76f199e`. **Không đổi ở r20:** mọi số hạng, `A1`–`A12`, Phụ lục A–M, §7, §9, `write_set`, điều
kiện dừng, hạn lease.

### 0.20 — Vì sao có revision 21: bảng BIÊN độc lập cho mọi hàm có hành vi ranh giới của parser

Cross-review lượt 16 (codex `gpt-6-astra` medium) trên head `76f199e` theo r20: `blocked`, **P1 0 · P2 1 · P3 0 · P4 0** (verdict
`pull/588#issuecomment-5847927079`; tái lập `issues/588#issuecomment-5847934467`).

Nguồn của r21 — chủ kho 26-09-2026, trong phiên điều phối, bản chiếu `issues/574#issuecomment-5850653779`:
*"r21 + g21 + nới hạn (đề xuất)"* ⟦nguon:chi-thi⟧. **Hạn của g21 là `2026-09-28T06:00:00Z`** — chủ kho nới +24h so với g20; mốc
nới hạn là chính comment ấy.

- **Đã đóng:** sáu biểu hiện của lượt 15. `mo_masked` và `l16_reverse_q` là tương đương, reviewer đã chứng minh.
- **F2 (P2), tiếp diễn:** bảy đột biến parser vẫn cho `tu-kiem` 348/348 và qua cả N2/N3:
  - `l16_md_no_final_flush` — khối cuối không được đẩy khi tệp không có newline cuối (âm tính giả);
  - `l16_mo_bound5`, `l16_nhan_bound5` — trần 5 ký tự markup;
  - `l16_space_tab_newline` — chỉ nhận space/tab/LF giữa câu và nhãn;
  - `l16_chuan_no_strip` — `chuan` bỏ phép cắt khoảng trắng biên;
  - `l16_heading_stale` — tiêu đề không token không xoá được tiêu đề có token trước nó;
  - `l16_py_all_strings` — `khoi_py` quét cả chuỗi ngắn.

**Đổi ở r21 — công cụ con trỏ v12, Phụ lục O, nguyên văn** (Phụ lục E–N giữ làm lịch sử). **Chỉ `tu_kiem` đổi:** phần trước
`def tu_kiem` và từ `def main` trở đi bằng byte với v11 (Phụ lục N). Parser (`NHAN`, `MO`, `Q`, `khoi_md`, `khoi_py`, `chuan`,
`bo_dau`, `kiem`) KHÔNG đổi, nên số đếm trên văn bản thật không thể đổi vì công cụ. Mã #588 không đổi (`76f199e`).

**Sáu bảng biên mới trong `tu_kiem`, 217 ca.** Mỗi bảng sinh theo hai kiểu ngoặc, trừ bảng (f). Kỳ vọng là vecto viết tay; băm
của nguồn có khoảng trắng biên là LITERAL, tính độc lập từ chuỗi chuẩn hoá viết tay, không gọi `chuan`/`bam`/`sinh`/`kiem`:

| bảng | biên | số ca |
|---|---|---|
| (a) `khoi_md` — EOF | có/không newline cuối; nhiều newline; khối cuối sau khối khác; khối cuối là bảng (có/không newline); có nhãn; không token | 18 |
| (b) `khoi_md` — chuyển tiêu đề | có→không, không→có, có→có (liền dòng/cách dòng); mức 1 và 6; mức 7 và thiếu khoảng trắng KHÔNG phải tiêu đề; tiêu đề rồi rào code | 24 |
| (c) `khoi_py` — ngưỡng 40 | chuỗi dài 14, 39, 40 (KHÔNG quét), 41, 60 (quét) | 10 |
| (d) loại khoảng trắng giữa câu và nhãn | space, tab, LF, VT, FF, CR, U+00A0, U+00A0+space, U+2003, U+3000, U+1680, U+202F, U+2028, U+001C ⇒ DƯƠNG; U+200B, U+00AD, U+2060 ⇒ ÂM | 34 |
| (e) `NHAN`/`MO` — độ dài markup là THUỘC TÍNH | mọi L = 1..8, ký tự `*` và `_`: cặp (L,L) DƯƠNG, (L,L+1) và (L+1,L) ÂM; markup trộn L = 2..8: đảo đúng DƯƠNG, không đảo ÂM | 124 |
| (f) `chuan`/`bo_dau` — khoảng trắng biên | nguồn có khoảng trắng hai phía (một dòng, nhiều dòng), tab/U+00A0 ở giữa; mảnh có khoảng trắng biên, tab/U+00A0 ở giữa, và mảnh ngắn hơn 6 sau chuẩn hoá ⇒ VI_PHAM | 7 |

**Phép phủ tính trên tệp đã sinh**, thiếu một ô thì `tu-kiem` ĐỎ:
- EOF: có/không newline × nhiều newline × khối cuối là bảng × khối cuối sau khối khác × có token × có nhãn;
- tiêu đề: dãy cờ "tiêu đề thật có token" trước câu × có dòng trống × có tiêu đề giả; mức 1, 2, 6, 7;
- `.py`: đúng các độ dài 39, 40, 41, cùng một chuỗi ngắn và một chuỗi dài;
- khoảng trắng: đúng CHUỖI khe giữa câu và nhãn, cho từng loại, và ba ký tự vô hình không phải khoảng trắng;
- markup: (độ dài mở, độ dài đóng, tập ký tự, có đảo đúng không) cho mọi độ dài 1..8;
- `chuan`/`bo_dau`: tính TỪNG CON TRỎ từ chính các dòng nguồn được trỏ (một/nhiều dòng × biên đầu × biên cuối × khoảng trắng lạ ở
  giữa) và từ chính mảnh đã viết.

**Minh bạch:** bản phủ đầu thô hơn. Bốn đột biến bộ sinh đã SỐNG vì ca anh em còn giữ ô:
- bỏ ca EOF không newline;
- bỏ ca NBSP (ca `NBSP + space` còn giữ ký tự);
- bỏ ca `.py` 41 ký tự (ca 60 còn giữ dấu "trên ngưỡng");
- bỏ khoảng trắng biên của nguồn một dòng (nguồn nhiều dòng còn giữ ô).

Tôi đã tinh ô như trên trước khi đóng băng; cả bốn nay ĐỎ. Khi dựng bảng còn bắt được hai lỗi của chính fixture, và đã sửa trước khi
đóng băng: mẫu markup xen kẽ độ dài lẻ là palindrome, nên đảo vẫn bằng chính nó; nguồn mới đặt số trùng với ca `thieu_tep` có sẵn.

**Đo:**
- `tu-kiem` in `TU_KIEM DAT 565/565 (truc tiep 471, CLI 94)` — 565 ca, trong đó 94 ca CLI sinh từ bảng §0.14, rc=0.
- **99 đột biến** công cụ, mỗi cái một bản sao, một tiến trình, **cả 99 ĐỎ trong MỘT lượt chạy chung**: 86 của r20; bảy đột biến lượt 16 (neo/thay nguyên văn mục Recipe tái lập của verdict); và 6 đột biến BỘ SINH của bảng mới (bỏ ca EOF không newline; bỏ NBSP; markup chỉ tới 7; bỏ `.py` 41; bỏ tiêu đề có→không; bỏ khoảng trắng biên của nguồn) — chỉ phép phủ bắt. Cùng bảy đột biến lượt 16 trên v11: cả bảy `rc=0` `TU_KIEM DAT 348/348` — tái lập phản chứng của reviewer.
- N1 `565/565`, rc=0 · N2 (kiểm chính r21) `TONG {'DUNG': 33, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 30}`, rc=0 · N3 `TONG {'DUNG': 2, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 0}`, rc=0

### 0.21 — Vì sao có revision 22: khoá MIỀN của parser bằng bảng nhánh→ca, và phép phủ đo BYTE ĐỌC LẠI

Cross-review lượt 17 (codex `gpt-6-astra` medium) trên head `76f199e` theo r21: `blocked`, **P1 0 · P2 1 · P3 0 · P4 0** (verdict
`pull/588#issuecomment-5851298363`; tái lập của phiên điều phối `issues/574#issuecomment-5851303786`).

Nguồn của r22 — chủ kho 27-09-2026, trong phiên điều phối, bản chiếu `issues/574#issuecomment-5851330887`:
*"r22 + g22: khoá miền + readback (đề xuất)"* ⟦nguon:chi-thi⟧. **Hạn của g22 bằng hạn g21: `2026-09-28T06:00:00Z` — không nới.**

- **Đã đóng ở lượt 17:** bảy biểu hiện F2 của lượt 16; F3, F1d, L1, N1–N3 không hồi quy.
- **F2 (P2), tiếp diễn — `tu-kiem-con-tro-thieu-truc-dau-vao`:** 11 đột biến parser không tương đương vẫn cho `tu-kiem` 565/565:
  `new_py_strict_end`, `new_py_strict_start` (biên dòng của `--ham`); `new_ct_fragment_nonempty`, `new_ct_first`; `new_rv_ascii`,
  `new_rv_right_hyphen`; `new_code_no_empty`, `new_code_multiline`, `new_code_unclosed`; `new_table_no_strip`, `new_fence_no_strip`.
- **Và phép phủ đo Ý ĐỊNH, không đo tệp:** ghi fixture thêm một newline vẫn 565/565, kể cả khi bỏ luôn `day()` cuối (lỗi EOF lượt 16).

**Đổi ở r22 — công cụ con trỏ v13, Phụ lục P, nguyên văn** (Phụ lục E–O giữ làm lịch sử). **Chỉ `tu_kiem` đổi.** Máy kiểm trong
bộ dựng: phần trước `def tu_kiem` và từ `def main` trở đi bằng byte với v12; AST sau khi bỏ riêng hàm `tu_kiem` bằng nhau. Parser
(`CT`, `NHAN`, `MO`, `Q`, `CODE`, `RV`, `che_code`, `chuan`, `bo_dau`, `bam`, `nguon`, `sinh`, `khoi_md`, `khoi_py`, `kiem`, `main`)
KHÔNG đổi, nên số đếm trên văn bản thật không thể đổi vì công cụ. Mã #588 không đổi (`76f199e`).

#### (b) Phép phủ đo byte đọc lại từ đúng tệp mà `kiem` nhận — và đính chính lời khai của r21

**Đính chính.** §0.20 viết *phép phủ tính trên tệp đã sinh*. Câu ấy **sai ở bước I/O**: ở v12, `o_kn`, `o_cm`, `o_bc`, `o_r20` và
`o_r21` đều đọc `ca.items()` trong bộ nhớ, TRƯỚC khi tệp được ghi; chỉ `o_ch` đọc lại tệp NGUỒN. Reviewer lượt 17 đo được đúng điều đó.

**Cơ chế ở v13 — hai lớp độc lập:**
1. **Một chỗ ghi duy nhất** `tep_ca(ten)`: ghi BYTE (`write_bytes`, không dịch newline theo nền), rồi đọc lại byte từ CHÍNH tệp ấy vào
   `RB[ten]`. Mọi phép phủ (`PHU_KHOANG_NOI`, `PHU_CAP_MARKUP`, `PHU_RANH_GIOI_CODE`, `PHU_R20`, `PHU_R21`, mảnh của `PHU_CHUAN`, và
   `PHU_R22` mới) tính trên `RB`, không tính trên `ca[ten][1]`.
2. **Vòng chạy ca** mở đúng đường dẫn đó, đọc byte **lần nữa**, độc lập với `RB`, và so với ý định trước mọi phép chuẩn hoá. Lệch ⇒
   `GHI_LECH` ⇒ ĐỎ. Chỉ sau đó mới gọi `kiem` trên cùng đường dẫn.

**Vì sao ghi byte chứ không `write_text`:** trên Windows, `write_text` đổi LF thành CRLF, nên lớp 2 sẽ đỏ giả ở nền đó. Windows vẫn
**KHÔNG ĐO ĐƯỢC** ở lượt này. Neo đột biến của reviewer (`p.write_text(doc, encoding="utf-8")`) vì thế không còn; đột biến tương ứng neo
lại trên chỗ ghi mới (nhóm `g22:` ở Phụ lục P.1).

**Khai thêm, đo được khi dựng lớp readback:** `kiem` và `nguon` đọc bằng `read_text`, tức có dịch universal newline. CR và CRLF
thành LF TRƯỚC parser. Vì vậy hai ca `b21kt_*_cr` của r21 chỉ khoá TẦNG TỆP (readback thấy CR thật); ở tầng parser chúng tương đương ca
LF. Không đổi parser; ghi thành loại trừ `nguon.cr_crlf` trong bảng nhánh.

**Đo (rc đọc trực tiếp):** mỗi lớp tự giết được đột biến ghi thêm newline khi lớp kia bị gỡ, kể cả khi bỏ luôn `day()`:

| đột biến (Phụ lục P.1) | rc | bắt bởi |
|---|---|---|
| `g22:ghi_them_nl` | 1 | cả hai lớp (545 dòng hỏng) |
| `g22:ghi_them_nl+bo_day` | 1 | cả hai lớp |
| `g22:ghi_them_nl+bo_lop2` | 1 | lớp 1: `PHU_R21` thiếu ô EOF không newline |
| `g22:ghi_them_nl+bo_lop2+bo_day` | 1 | lớp 1: `PHU_R21` |
| `g22:ghi_them_nl+bo_lop1` (phủ đọc ý định) | 1 | lớp 2: `GHI_LECH` |
| `g22:ghi_them_nl+bo_lop1+bo_day` | 1 | lớp 2: `GHI_LECH` |
| `g22:ghi_crlf+bo_lop2` | 1 | lớp 1: `PHU_KHOANG_NOI`, `PHU_R20`, `PHU_R21`, `PHU_R22` |

Giới hạn: gỡ CẢ HAI lớp cùng lúc (đột biến bậc ba) thì không lớp nào còn đo tệp. Phạm vi của lời khai chỉ tới đó.

#### (a) Bảng biên B22 và bảng nhánh→ca

**73 ca trực tiếp mới** (kỳ vọng là vecto viết tay `V(...)`; băm literal `sha256("dong mot")[:8] = 2bf318fb` tính độc lập bằng hashlib
từ chuỗi viết tay; không gọi `chuan`/`bam`/`sinh`/`kiem` để sinh đáp án), và **2 ca CLI mới**:

| nhóm | biên | ca |
|---|---|---|
| `b22py` — `khoi_py` phạm vi dòng hàm | chuỗi dài ở dòng ĐẦU (hàm 1 dòng; tham số mặc định của hàm nhiều dòng), GIỮA, CUỐI; ngay TRƯỚC và ngay SAU hàm được chọn; cuối hàm KHÔNG chọn liền trước hàm được chọn; không `--ham`; hằng `bytes` | 10 |
| `b22ct` — mảnh con trỏ và `CT` | mảnh thiếu, rỗng, chỉ khoảng trắng (space; tab + U+00A0), 5 ký tự, đúng 6, đúng 6 sau khi bỏ `*`, `_` KHÔNG bị bỏ; hai con trỏ đúng→sai, sai→đúng, đúng→đúng; băm HOA, 7 hex, 9 hex; dòng 1; dòng CUỐI của nguồn không newline cuối; khoảng tới cuối; khoảng vượt cuối đúng 1; nguồn là thư mục | 19 |
| `b22rv` — token `rN` hai phía, × 2 kiểu ngoặc | trái/phải: chữ ASCII, chữ Unicode U+00E1, gạch nối; đầu khối; cuối khối; chữ số Unicode U+0663; `R` hoa | 20 |
| `b22code` — `CODE`/`che_code`, × 2 kiểu ngoặc | cặp rỗng; backtick qua dòng; backtick chưa đóng; hai cặp bao câu; `.py` KHÔNG che code | 10 |
| `b22ls` — `khoi_md` và `lstrip`, × 2 kiểu ngoặc | bảng thụt; bảng thụt rồi bảng (dòng trước thụt); rào thụt; rào chưa đóng; tiêu đề thụt; `##` + tab; dòng chỉ có khoảng trắng | 14 |
| CLI — `main` cộng dồn | hai tệp CÙNG cột: DUNG + DUNG, VI_PHAM + VI_PHAM | 2 |

**Hai ca CLI là lỗ SẴN CÓ, tìm được khi đo lại đột biến cũ.** `l11_sum_max_dung_vipham` (recipe lượt 11: cộng dồn dùng `max` cho
DUNG và VI_PHAM) cho `rc=0`, `TU_KIEM DAT 565/565` **trên v12**. Nguyên nhân: tổ hợp CLI sinh bằng `permutations`, không lặp tệp,
nên không lần chạy nào có hai tệp cùng DUNG hoặc cùng VI_PHAM. r21 khai *99/99 ĐỎ*; tập 99 ấy không lưu trong kho, reviewer lượt 17
đã ghi là KHÔNG ĐO ĐƯỢC. Đột biến này nằm trong recipe lượt 11 mà lại sống, nên tập 99 hoặc không chứa nó, hoặc lời khai sai. Hai
tổ hợp mới được nối vào CUỐI danh sách (`to_hop += ...`), nên tên và vị trí của 94 ca cũ giữ nguyên.

**Phép phủ `PHU_R22` đo trên byte đọc lại.** Ô tính từ nội dung tệp, không từ tên ca, không qua regex nào của cổng:
- `b22py`: dãy `(nhiều dòng?, vị trí chuỗi so với hàm, có được chọn?)` cho MỌI hàm trong tệp, tính bằng `ast`.
- `b22ct`: cho mỗi con trỏ (tách bằng ký tự ngoặc, không bằng `CT`): dạng băm; lớp mảnh; `*`, `_`, khoảng trắng lạ; biên dòng so với
  số dòng của tệp nguồn đọc lại.
- `b22rv`: lớp ký tự trái/phải của token đầu tiên, `r`/`R`, chữ số ASCII hay không.
- `b22code`: số backtick theo dòng, có cặp rỗng không, tệp `.py` hay không.
- `b22ls`: các dòng thụt, dòng tiêu đề, dòng chỉ có khoảng trắng, và tính chẵn/lẻ của số dòng rào.

Mỗi ca B22 giữ một ô riêng: bỏ BẤT KỲ ca nào trong 73 ca B22 ⇒ `PHU_R22` ĐỎ (nhóm `bo:` ở P.1, 73/73).

**Bảng nhánh→ca do máy kiểm.** `BANG_NHANH` trong `tu_kiem` có **120 nhánh/biên**: 99 trỏ tới ca, 21 mang lý do `LOAI_TRU`. Sau khi
sinh xong ca CLI, `tu-kiem` ĐỎ nếu (i) một tên ca trong bảng không tồn tại, hoặc (ii) một nhánh rỗng, hoặc mang chuỗi mà không phải
lý do loại trừ. Máy chỉ kiểm được rằng bảng **trỏ tới ca có thật**. Máy **không** kiểm được bảng đã **liệt kê đủ** mọi nhánh; phần
ấy dựa trên việc đọc parser. Ai chỉ ra một nhánh không có dòng nào trong bảng thì đó là finding. Bảng nguyên văn, sinh từ chính dict
trong Phụ lục P:

| nhánh / biên | ca khoá | loại trừ — lý do |
|---|---|---|
| `CT.rN_mot_chu_so` | `duong` | — |
| `CT.rN_nhieu_chu_so` | `rv_hai_chu_so_con_tro` | — |
| `CT.dong_mot_chu_so` | `duong` | — |
| `CT.dong_nhieu_chu_so` | `dong_hai_chu_so_con_tro` · `span_hai_chu_so` | — |
| `CT.khoang_vang` | `duong` | — |
| `CT.khoang_co` | `span_nhieu_dong_duong` · `b22ct_span_toi_cuoi_nguon` | — |
| `CT.bam_8_hex_thuong` | `duong` | — |
| `CT.bam_hex_hoa` | `b22ct_bam_hoa` | — |
| `CT.bam_7_hex` | `b22ct_bam_7` | — |
| `CT.bam_9_hex` | `b22ct_bam_9` | — |
| `CT.manh_thieu` | `thieu_manh` · `b22ct_manh_thieu` | — |
| `CT.manh_rong` | `b22ct_manh_rong` | — |
| `CT.manh_chi_khoang_trang` | `b22ct_manh_trang` · `b22ct_manh_trang_la` | — |
| `CT.manh_duoi_nguong` | `manh_4_am` · `manh_5_am` · `b22ct_manh_duoi_nguong` · `b21bd_manh_ngan_sau_chuan` | — |
| `CT.manh_dung_nguong` | `manh_6_duong` · `b22ct_manh_dung_nguong` · `b22ct_manh_nguong_sau_bo_sao` | — |
| `CT.nhieu_con_tro_moi_thu_tu` | `b22ct_dung_roi_sai` · `b22ct_sai_roi_dung` · `b22ct_hai_dung` | — |
| `NHAN.nhan_hop_le_ca_6` | `moi_nhan_hop_le` | — |
| `NHAN.nhan_khong_hop_le` | `nhan_khong_hop_le` · `kn_nhan_sai_roi_dung` | — |
| `NHAN.markup_dong_1_den_8` | `b21md_thang_sao_1_1` · `b21md_thang_gach_8_8` · `b21md_cong_sao_8_8` | — |
| `NHAN.khoang_trang_moi_loai` | `kn_thang_rong` · `kn_thang_tab` · `kn_thang_xuong_dong` · `b21kt_thang_nbsp` · `b21kt_thang_ls` · `b21kt_cong_fs` | — |
| `NHAN.khong_phai_khoang_trang` | `b21kt_thang_zwsp` · `b21kt_thang_shy` · `b21kt_thang_wj` · `kn_thang_chu` · `kn_thang_dau0` | — |
| `NHAN.ngay_sau_cau_khong_tim_xa` | `kn_thang_noi_dung_xen` · `nhan_xau_truoc_nhan_dung` · `kn_nhan_truoc_cau` | — |
| `MO.khong_markup` | `kn_thang_cach` | — |
| `MO.markup_1_den_8` | `b21md_thang_sao_1_1` · `b21md_thang_sao_8_8` · `dd_thang_nam_nam` | — |
| `MO.markup_tron_dao_nguoc` | `b21md_thang_tron_2_dao` · `b21md_thang_tron_8_khong_dao` · `cm_thang_khac_loai_sai_thu_tu` | — |
| `MO.do_dai_lech` | `b21md_thang_sao_1_2` · `b21md_thang_sao_2_1` · `dd_thang_bon_ba` · `cm_thang_dai_ngan` | — |
| `MO.vi_tri_cau` | `vt_thang_dau_khoi_sao` · `vt_thang_thut_le_sao_thieu_mo` · `vt_thang_sau_dong_ket_markup_sao_doi_lech` | — |
| `MO.tren_k_hay_kc` | — | tuong duong da chung minh (mo_masked, luot 16 va 17) |
| `Q.thang_7_8_9` | `trich_7_thang` · `trich_8_thang` · `trich_9_thang` | — |
| `Q.cong_7_8_9` | `trich_7_cong` · `trich_8_cong` · `trich_9_cong` | — |
| `Q.vat_dong` | `vat_dong` · `ngoac_cong_vat_dong` | — |
| `Q.nhieu_lan_cung_dong` | `lan_thang_dung_roi_thieu_mo` · `lan_cong_khong_roi_co_nhan` | — |
| `Q.luoi_hay_tham` | — | tuong duong da chung minh (new_q_greedy, new_q_curly_greedy, luot 17) |
| `Q.thu_tu_duyet` | — | tuong duong da chung minh (l16_reverse_q, luot 16) |
| `Q.cong_long_thang` | — | ngoai pham vi — ngoac cong long ngoac thang |
| `CODE.mot_cap` | `trong_code` · `bc_thang_cau_trong_code` | — |
| `CODE.cap_rong` | `b22code_thang_rong` · `b22code_cong_rong` | — |
| `CODE.qua_dong` | `b22code_thang_nhieu_dong` · `b22code_cong_nhieu_dong` | — |
| `CODE.chua_dong` | `b22code_thang_chua_dong` · `b22code_cong_chua_dong` | — |
| `CODE.hai_cap` | `b22code_thang_hai_cap` · `bc_thang_code_xen` | — |
| `CODE.nhieu_backtick` | — | code span nhieu backtick (CommonMark) ngoai pham vi; parser dong bang chi ghep backtick don |
| `che_code.giu_do_dai` | `bc_thang_code_truoc_cau` · `bc_thang_markup_mo_trong_code` | — |
| `che_code.chi_md` | `b22code_thang_py_khong_che` · `b22code_cong_py_khong_che` | — |
| `RV.trai_ascii` | `b22rv_thang_trai_ascii` · `rv_trong_tu_khong_phai_token` | — |
| `RV.trai_unicode` | `b22rv_thang_trai_unicode` · `b22rv_cong_trai_unicode` | — |
| `RV.trai_gach` | `b22rv_thang_trai_gach` · `rv_sau_gach_noi` | — |
| `RV.trai_dau_khoi` | `b22rv_thang_dau_khoi` · `vat_dong` | — |
| `RV.phai_ascii` | `b22rv_thang_phai_ascii` | — |
| `RV.phai_unicode` | `b22rv_thang_phai_unicode` · `b22rv_cong_phai_unicode` | — |
| `RV.phai_gach` | `b22rv_thang_phai_gach` · `b22rv_cong_phai_gach` | — |
| `RV.phai_cuoi_khoi` | `b22rv_thang_cuoi_khoi` · `b22rv_cong_cuoi_khoi` | — |
| `RV.chu_so_nhieu` | `rv_hai_chu_so_token` | — |
| `RV.chu_so_unicode` | `b22rv_thang_so_unicode` | — |
| `RV.chu_hoa` | `b22rv_thang_hoa` | — |
| `RV.token_o_tieu_de` | `chi_tieu_de` · `b21td_thang_co_cach` | — |
| `RV.ba_chu_so_tro_len` | — | revision/dong >= 3 chu so ngoai pham vi |
| `khoi_md.rao_mo_dong` | `rao_code_bo_qua` · `rao_code_ngoai_rao_van_do` · `rao_3_co_thong_tin` · `rao_4_co_thong_tin` | — |
| `khoi_md.rao_thut` | `b22ls_thang_rao_thut` · `b22ls_cong_rao_thut` | — |
| `khoi_md.rao_chua_dong` | `b22ls_thang_rao_chua_dong` | — |
| `khoi_md.rao_nga` | — | rao ~~~ ngoai pham vi |
| `khoi_md.bang_tach_doan` | `bang_tach_khoi_doan` · `bang_tu_nhac_ban` | — |
| `khoi_md.bang_thut` | `b22ls_thang_bang_thut` · `b22ls_cong_bang_thut` | — |
| `khoi_md.bang_dong_truoc_thut` | `b22ls_thang_bang_thut_roi_bang` | — |
| `khoi_md.bang_cuoi_tep` | `b21eof_thang_bang_khong_nl` · `b21eof_thang_bang_co_nl` | — |
| `khoi_md.tieu_de_1_den_6` | `tieu_de_cap_1` · `tieu_de_cap_2` · `tieu_de_cap_3` · `tieu_de_cap_4` · `tieu_de_cap_5` · `tieu_de_cap_6` | — |
| `khoi_md.tieu_de_7` | `bay_thang_khong_phai_tieu_de` · `b21td_thang_muc7_khong_la_tieu_de` | — |
| `khoi_md.tieu_de_thieu_cach` | `b21td_thang_thieu_cach_khong_la_tieu_de` · `gach_so_khong_phai_tieu_de` | — |
| `khoi_md.tieu_de_tab` | `b22ls_thang_tieu_de_tab` | — |
| `khoi_md.tieu_de_thut` | `b22ls_thang_tieu_de_thut` | — |
| `khoi_md.chuyen_tieu_de` | `b21td_thang_co_roi_khong` · `b21td_thang_khong_roi_co` · `b21td_thang_co_roi_co` · `b21td_thang_co_roi_rao` | — |
| `khoi_md.setext` | — | tieu de Setext ngoai pham vi |
| `khoi_md.danh_sach_long` | — | danh sach long ngoai pham vi |
| `khoi_md.dong_trong` | `b21eof_thang_hai_khoi_khong_nl` · `chi_tieu_de` | — |
| `khoi_md.dong_chi_khoang_trang` | `b22ls_thang_dong_chi_khoang_trang` | — |
| `khoi_md.eof` | `b21eof_thang_mot_khong_nl` · `b21eof_thang_mot_co_nl` · `b21eof_thang_mot_nhieu_nl` · `b21eof_thang_sau_khoi_khong_nl` | — |
| `khoi_md.so_dong_dau_khoi` | — | chi vao dong chan doan in ra, khong vao vecto dem |
| `khoi_py.nguong_40` | `b21py_thang_39` · `b21py_thang_40` · `b21py_thang_41` · `b21py_cong_60` | — |
| `khoi_py.khong_ham` | `py_docstring` · `b22py_khong_ham` | — |
| `khoi_py.chuoi_khong_phai_str` | `b22py_bytes` | — |
| `khoi_py.ham_mot_dong` | `b22py_mot_dong_chon` · `b22py_mot_dong_bo` | — |
| `khoi_py.dong_dau_ham` | `b22py_dau_chon` · `b22py_mot_dong_chon` | — |
| `khoi_py.dong_giua_ham` | `b22py_giua_chon` · `py_ham` | — |
| `khoi_py.dong_cuoi_ham` | `b22py_cuoi_chon` | — |
| `khoi_py.ngay_truoc_ham` | `b22py_ngay_truoc_ham` · `b22py_cuoi_bo_ham_sau_chon` | — |
| `khoi_py.ngay_sau_ham` | `b22py_ngay_sau_ham` · `b22py_mot_dong_bo` | — |
| `khoi_py.chon_bo` | `py_ham` · `b22py_mot_dong_bo` · `b22py_cuoi_bo_ham_sau_chon` | — |
| `khoi_py.ham_khong_ton_tai` | `cli_ham_truoc_zz` · `cli_ham_sau_zz` | — |
| `khoi_py.tach_doan` | `py_tach_doan` | — |
| `khoi_py.fullmatch_du` | — | khong the dat — doan chi khoang trang da bi `doan.strip()` loai truoc |
| `khoi_py.async_long_nhau` | — | async def / ham long nhau ngoai pham vi quyet dinh hien hanh |
| `khoi_py.f_string_chuoi_noi` | — | f-string / chuoi noi ngoai pham vi |
| `khoi_py.so_dong_chan_doan` | — | chi vao dong chan doan in ra, khong vao vecto dem |
| `chuan.bien_va_gop` | `b21ch_bien_hai_phia` · `b21ch_nhieu_dong` · `b21ch_tab_nbsp_giua` | — |
| `bo_dau.bo_sao_backtick` | `manh_bo_sao` · `manh_bo_backtick` · `b22ct_manh_nguong_sau_bo_sao` | — |
| `bo_dau.giu_gach_duoi` | `b22ct_manh_gach_duoi_giu` | — |
| `bo_dau.gop_va_cat` | `manh_gop_khoang_trang` · `b21bd_manh_bien` · `b21bd_manh_tab_nbsp` | — |
| `nguon.co_tep` | `duong` | — |
| `nguon.khong_co` | `thieu_tep` · `cli_co_truoc_thieu.md` | — |
| `nguon.la_thu_muc` | `b22ct_nguon_la_thu_muc` | — |
| `nguon.khong_newline_cuoi` | `b22ct_dong_cuoi_nguon` · `b22ct_span_vuot_cuoi_1` | — |
| `nguon.mau_ten` | `cli_co_truoc_sach.md` | — |
| `nguon.cr_crlf` | — | read_text dich CR/CRLF thanh LF truoc parser; ca b21kt_*_cr chi khoa TANG TEP, o parser tuong duong LF |
| `nguon.encoding_khac` | — | encoding khac UTF-8 ngoai pham vi |
| `kiem.khong_do_duoc` | `thieu_tep` · `b22ct_nguon_la_thu_muc` | — |
| `kiem.pham_vi` | `pv_dau_0` · `pv_dao` · `ngoai_pham_vi` · `pv_cuoi_vuot_mot_phan` · `b22ct_dong_dau` · `b22ct_dong_cuoi_nguon` · `b22ct_span_vuot_cuoi_1` | — |
| `kiem.bam_lech` | `sai_dong` · `sai_bam_manh_van_khop` | — |
| `kiem.manh_lech` | `sai_manh_dung_bam` · `b22ct_manh_gach_duoi_giu` | — |
| `kiem.manh_or_rong` | — | `manh or ""` khong the dat (manh da khac None o nhanh truoc) |
| `kiem.md_hay_py` | `py_docstring` · `b22code_thang_py_khong_che` | — |
| `kiem.co_nhan` | `trich_co_nhan` | — |
| `kiem.vi_pham` | `trich_khong_nhan` | — |
| `main.tu_kiem` | — | chinh lenh dang chay |
| `main.co_truoc_sau_xen` | `cli_co_truoc_sach.md` · `cli_co_sau_sach.md` · `cli_co_xen_sach.md` | — |
| `main.ham` | `cli_ham_truoc_a` · `cli_ham_sau_a,b` · `cli_khong_ham_h` | — |
| `main.cong_don_nhieu_tep` | `cli_co_sau_lech.md+lech2.md+vipham.md` · `cli_co_truoc_thieu.md+sach.md+thieu.md` · `cli_co_sau_lech.md+lech2.md+nhan.md+nhan_gach.md+sach.md+thieu.md+vipham.md` | — |
| `main.rc` | `cli_co_truoc_sach.md` · `cli_co_truoc_lech.md` | — |
| `main.cong_don_cung_cot` | `cli_co_xen_sach.md+sach.md` · `cli_co_truoc_vipham.md+vipham.md` | — |
| `main.sinh_tim` | — | lenh sinh/tim ngoai pham vi tu kiem |
| `main.lenh_la` | — | lenh khong hop le ngoai pham vi |
| `main.co_lap_thieu` | — | co lap / thieu gia tri / --nguon khong ton tai ngoai pham vi |

Chiều ngoài phạm vi, khai rõ (không phải finding, cũng không có ca): CommonMark đầy đủ; code span nhiều backtick; f-string và chuỗi
nối; rào `~~~`; tiêu đề Setext; danh sách lồng; revision/dòng ≥ 3 chữ số; encoding khác UTF-8; CR/CRLF ở tầng parser; `async def`
và hàm lồng; lệnh `sinh`/`tim`; cờ lặp hoặc thiếu giá trị; `--nguon` không tồn tại.

#### Đo — rc đọc trực tiếp, không qua pipe

| phép đo | kết quả |
|---|---|
| `tu-kiem` v13 | `TU_KIEM DAT 640/640 (truc tiep 544, CLI 96)`, rc=0 — 471 + 73 trực tiếp; 94 + 2 CLI |
| N1 | `640/640` |
| N2 (kiểm chính r22) | `TONG {'DUNG': 33, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 31}`, rc=0 — `CO_NHAN` +1 vì câu trích chủ kho mới có nhãn ở đầu mục này |
| N2 của v12 và v13 trên r21 | cùng `DUNG 33 · CO_NHAN 30`, rc=0 |
| N3 (`--ham _c378_ma_tran_phan_hang,_r378_classify,_c378_resolve_phai_o_trong_kho scripts/tl_selftest.py` tại `76f199e`) | `TONG {'DUNG': 2, 'LECH': 0, 'KHONG_DO_DUOC': 0, 'VI_PHAM': 0, 'CO_NHAN': 0}`, rc=0 — v12 cũng vậy |
| 11 đột biến lượt 17 trên v13 | **11/11 ĐỎ**, mỗi cái đỏ đúng ở ca khoá của nó (bảng dưới) |
| đột biến ghi thêm newline, kể cả kèm bỏ `day()` | ĐỎ — 7 biến thể `g22:` ở bảng (b) |
| toàn bộ Phụ lục P.1 trên v13 | `TONG 195 DO 186 SONG 5 NEO_HONG 4 KHAC 0`, rc=0 — chi tiết ngay dưới |

| đột biến lượt 17 | ca đỏ trên v13 |
|---|---|
| `new_py_strict_end` | `b22py_mot_dong_chon`, `b22py_cuoi_chon` |
| `new_py_strict_start` | `b22py_mot_dong_chon`, `b22py_dau_chon` |
| `new_ct_fragment_nonempty` | `b22ct_manh_rong` |
| `new_ct_first` | `b22ct_dung_roi_sai`, `b22ct_sai_roi_dung`, `b22ct_hai_dung` |
| `new_rv_ascii` | `b22rv_{thang,cong}_{trai,phai}_unicode` (4) |
| `new_rv_right_hyphen` | `b22rv_{thang,cong}_phai_gach` |
| `new_code_no_empty` · `new_code_multiline` · `new_code_unclosed` | `b22code_{thang,cong}_rong` · `_nhieu_dong` · `_chua_dong` |
| `new_table_no_strip` · `new_fence_no_strip` | `b22ls_{thang,cong}_bang_thut` · `_rao_thut` |

**Tập đột biến — vì sao KHÔNG phải 99 cũ, và nó là gì.** Tập 99 của r21 không lưu trong kho, không có recipe đầy đủ. Tôi không tái
dựng được nó và không khai là đã tái dựng. Thay vào đó, Phụ lục P.1 ghi **literal** một tập có nguồn gốc kiểm được:
- **101 `rv:`**: MỌI recipe khác tên trong verdict lượt 10–17 trên PR #588 (100 tên; bản cuối của mỗi tên), cộng
  `l16_reverse_q` (lượt 16 mô tả bằng lời). Dấu chấm than mà GitHub xoá khỏi lookbehind/lookahead (`(?<` và `(?`) đã được khôi phục.
- **4 `neo_lai:`**: bốn recipe có neo không dùng được trên v12. Ba recipe nhắm dạng `NHAN` trước r19; một recipe có neo
  `:(\d+)(?:-` khớp HAI lần ở v12 (`CT` và `o_ch`). Cả bốn được neo lại trên dòng `NHAN`/`CT` hiện hành.
- **7 `g22:`** ghi/đọc lại; **6 `g21:`** và **4 `g20:`**: các đột biến bộ sinh r21/r20, dựng lại theo mô tả bằng lời ở §0.20/§0.19.
- **73 `bo:`**: bỏ từng ca B22.

Kết quả trên v13, **một lượt chạy chung**:
- **186 ĐỎ.** Trong đó một ca, `rv:new_search_to_match`, đỏ vì NGOẠI LỆ (`AttributeError`, `MO.match` trả `None`), không đỏ vì
  assertion — v12 cũng vậy. Ghi riêng, không gộp vào nhóm đỏ vì assertion.
- **4 `NEO_HONG`**: đúng bốn recipe gốc đã neo lại ở trên. Chúng không chạy, và không được tính là đỏ.
- **5 SỐNG, cả năm tương đương:**
  - `mo_masked` — chứng minh ở lượt 16/17;
  - `l16_reverse_q` — lượt 16;
  - `new_q_greedy`, `new_q_curly_greedy` — lượt 17;
  - `neo_lai:new_label_punctuation@NHAN` (`[*_]*` → `[*_.,;:]*` trong nhóm markup của `NHAN`), chứng minh ở đây. Nếu
    `NHAN` gốc khớp với nhóm `g`, ký tự ngay sau `g` phải là khoảng trắng hoặc ngoặc mở của nhãn. Vậy nhóm tham lam của đột biến dừng
    đúng tại `g`, cho cùng nhóm. Nếu gốc không khớp mà đột biến khớp, nhóm của đột biến chứa dấu câu. Khi đó nó khác `MO[::-1]`,
    vì `MO` chỉ gồm `*_`. Kết quả vẫn VI_PHAM như gốc. Tương đương chỉ đúng từ khi có phép so cặp markup của r19. Recipe gốc thuộc parser
    trước r19.

Cùng 11 đột biến lượt 17 trên v12: cả 11 `rc=0` `TU_KIEM DAT 565/565` — tái lập phản chứng của reviewer.

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

## Phụ lục I — cổng CON TRỎ v6: hợp đồng CLI SINH ca từ bảng, §0.14 (MỚI ở r15, nguyên văn)

Cùng cách chạy như Phụ lục E. `tu-kiem` in: `TU_KIEM DAT 143/143 (truc tiep 62, CLI 81)` (số lấy từ lần chạy khi dựng đặc tả, không gõ tay). So với Phụ lục H chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `ddc8aa76693d90442f5f48cd62fb172cd11ac54038437066b9c0665eb2cbdd1e`.

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
            "nhan_sau_gach_duoi": ("a.md", "Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:doctrine" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
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
        # HOP DONG CLI — bang co tham quyen o dac ta r15 §0.14; cac ca SINH tu bang (to hop), khong liet ke tay.
        # Moi tep mau mang VEC TO ky vong viet tay (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN); ky vong cua mot lan chay
        # nhieu tep = TONG tung phan tu; rc ky vong = 1 khi LECH + KHONG_DO_DUOC + VI_PHAM > 0. Oracle chi cong va so sanh,
        # khong goi `kiem`/`main`/regex nao cua cong. Nguon CLI dung MAU TEN RIENG (`spec-r{n}.txt`) de `--mau` co rang.
        import itertools, subprocess as _sp
        nc = Path(t) / "nguon_cli"; nc.mkdir()
        (nc / "spec-r3.txt").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        dc = Path(t) / "cli"; dc.mkdir()
        TEP_CLI = {
            "sach.md": ("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", (1, 0, 0, 0, 0)),
            "lech.md": ("Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "lech2.md": ("Theo r3 " + CT0("r3:11 #00000000|so 11 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "thieu.md": ("Theo r9 " + CT0("r9:1 #00000000|khong co tep nao") + ".\n", (0, 0, 1, 0, 0)),
            "vipham.md": ("Theo r1: " + Q8 + ".\n", (0, 0, 0, 1, 0)),
            "nhan.md": ("Theo r1: " + Q8 + " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
            "nhan_gach.md": ("Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
        }
        for ten, (noi, _v) in TEP_CLI.items(): (dc / ten).write_text(noi, encoding="utf-8")
        COT = ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")
        CO = ["--nguon", str(nc), "--mau", "spec-r{n}.txt"]
        VI_TRI = {"co_truoc": lambda co, tep: co + tep, "co_sau": lambda co, tep: tep + co,
                  "co_xen": lambda co, tep: tep[:1] + co + tep[1:]}
        ds_tep = sorted(TEP_CLI)
        to_hop = [(x,) for x in ds_tep] + list(itertools.permutations(ds_tep, 2)) + [
            ("lech.md", "lech2.md", "vipham.md"), ("sach.md", "nhan.md", "nhan_gach.md"), ("thieu.md", "sach.md", "thieu.md"),
            tuple(ds_tep)]
        cli = {}
        for so, bo in enumerate(to_hop):
            vt = list(VI_TRI)[so % 3] if len(bo) > 1 else None
            for v in ([vt] if vt else list(VI_TRI)):
                mong = tuple(sum(TEP_CLI[x][1][c] for x in bo) for c in range(5))
                cli[f"cli_{v}_{'+'.join(bo)}"] = (VI_TRI[v](CO, [str(dc / x) for x in bo]), int(sum(mong[1:4]) > 0), mong)
        # --ham: tep 5 ham, XAU = {a, c, e}; ky vong VI_PHAM = so ten trong danh sach thuoc XAU (ten la khong tinh).
        XAU = {"a", "c", "e"}
        (dc / "h.py").write_text("".join(f"def {n}():\n    " + Q2 * 3 + f"Ham {n} nhac r1 " + (Q8 + " khong nhan" if n in XAU else "va khong trich gi")
                                 + ", du dai de qua nguong bon muoi.\n    " + Q2 * 3 + "\n\n\n" for n in "abcde"), encoding="utf-8")
        for so, ds_ham in enumerate(("a", "b", "c", "e", "a,b", "b,c", "d,e", "b,c,d", "d,c,b", "b,zz,d", "zz", "a,b,c,d,e", "b,d")):
            vi = len(set(ds_ham.split(",")) & XAU)
            tep = ["--ham", ds_ham, str(dc / "h.py")]
            cli[f"cli_ham_{ds_ham}"] = ((CO + tep) if so % 2 == 0 else (tep + CO), int(vi > 0), (0, 0, 0, vi, 0))
        cli["cli_khong_ham_h"] = (CO + [str(dc / "h.py")], 1, (0, 0, 0, 3, 0))
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", *doi], capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[0][5:]) if len(tong) == 1 else {}
            thuc = (r.returncode, len(tong), tuple(d.get(k) for k in COT))
            if thuc != (rc_mong, 1, mong): hong.append(f"{ten}: mong {(rc_mong, 1, mong)}, thuc {thuc}")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}", f"(truc tiep {len(ca)}, CLI {len(cli)})")
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

## Phụ lục J — cổng CON TRỎ v7: vị trí từng cờ là trục riêng, phủ bảng đo trên argv, §0.15 (MỚI ở r16, nguyên văn)

Cùng cách chạy như Phụ lục E. `tu-kiem` in: `TU_KIEM DAT 156/156 (truc tiep 62, CLI 94)` (số lấy từ lần chạy khi dựng đặc tả, không gõ tay). So với Phụ lục I chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `53c18e2357e47d943acfe13084461ad4b6a366869453224965cc4098bfba710d`.

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
            "nhan_sau_gach_duoi": ("a.md", "Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:doctrine" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
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
        # HOP DONG CLI — bang co tham quyen o dac ta r15 §0.14; cac ca SINH tu bang (to hop), khong liet ke tay.
        # Moi tep mau mang VEC TO ky vong viet tay (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN); ky vong cua mot lan chay
        # nhieu tep = TONG tung phan tu; rc ky vong = 1 khi LECH + KHONG_DO_DUOC + VI_PHAM > 0. Oracle chi cong va so sanh,
        # khong goi `kiem`/`main`/regex nao cua cong. Nguon CLI dung MAU TEN RIENG (`spec-r{n}.txt`) de `--mau` co rang.
        import itertools, subprocess as _sp
        nc = Path(t) / "nguon_cli"; nc.mkdir()
        (nc / "spec-r3.txt").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        dc = Path(t) / "cli"; dc.mkdir()
        TEP_CLI = {
            "sach.md": ("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", (1, 0, 0, 0, 0)),
            "lech.md": ("Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "lech2.md": ("Theo r3 " + CT0("r3:11 #00000000|so 11 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "thieu.md": ("Theo r9 " + CT0("r9:1 #00000000|khong co tep nao") + ".\n", (0, 0, 1, 0, 0)),
            "vipham.md": ("Theo r1: " + Q8 + ".\n", (0, 0, 0, 1, 0)),
            "nhan.md": ("Theo r1: " + Q8 + " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
            "nhan_gach.md": ("Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
        }
        for ten, (noi, _v) in TEP_CLI.items(): (dc / ten).write_text(noi, encoding="utf-8")
        COT = ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")
        CO = ["--nguon", str(nc), "--mau", "spec-r{n}.txt"]
        VI_TRI = {"co_truoc": lambda co, tep: co + tep, "co_sau": lambda co, tep: tep + co,
                  "co_xen": lambda co, tep: tep[:1] + co + tep[1:]}
        ds_tep = sorted(TEP_CLI)
        to_hop = [(x,) for x in ds_tep] + list(itertools.permutations(ds_tep, 2)) + [
            ("lech.md", "lech2.md", "vipham.md"), ("sach.md", "nhan.md", "nhan_gach.md"), ("thieu.md", "sach.md", "thieu.md"),
            tuple(ds_tep)]
        cli = {}
        for so, bo in enumerate(to_hop):
            vt = list(VI_TRI)[so % 3] if len(bo) > 1 else None
            for v in ([vt] if vt else list(VI_TRI)):
                mong = tuple(sum(TEP_CLI[x][1][c] for x in bo) for c in range(5))
                cli[f"cli_{v}_{'+'.join(bo)}"] = (VI_TRI[v](CO, [str(dc / x) for x in bo]), int(sum(mong[1:4]) > 0), mong)
        # --ham: tep 5 ham, XAU = {a, c, e}; ky vong VI_PHAM = so ten trong danh sach thuoc XAU (ten la khong tinh).
        XAU = {"a", "c", "e"}
        (dc / "h.py").write_text("".join(f"def {n}():\n    " + Q2 * 3 + f"Ham {n} nhac r1 " + (Q8 + " khong nhan" if n in XAU else "va khong trich gi")
                                 + ", du dai de qua nguong bon muoi.\n    " + Q2 * 3 + "\n\n\n" for n in "abcde"), encoding="utf-8")
        # r16 (luot 11): vi tri TUNG co la mot truc RIENG, tach khoi noi dung danh sach ham — moi danh sach x `--ham`
        # truoc / sau chinh tep; `--nguon`/`--mau` luan phien truoc / sau.
        for so, ds_ham in enumerate(("a", "b", "c", "e", "a,b", "b,c", "d,e", "b,c,d", "d,c,b", "b,zz,d", "zz", "a,b,c,d,e", "b,d")):
            vi = len(set(ds_ham.split(",")) & XAU)
            for vt_ham, tep in (("ham_truoc", ["--ham", ds_ham, str(dc / "h.py")]), ("ham_sau", [str(dc / "h.py"), "--ham", ds_ham])):
                cli[f"cli_{vt_ham}_{ds_ham}"] = ((CO + tep) if so % 2 == 0 else (tep + CO), int(vi > 0), (0, 0, 0, vi, 0))
        cli["cli_khong_ham_h"] = (CO + [str(dc / "h.py")], 1, (0, 0, 0, 3, 0))
        # KIEM PHU BANG MAY tren argv DA SINH (khong tren y dinh): moi o cua bang §0.14 phai co >= 1 ca. Vi tri cua moi co
        # tinh theo chi so trong argv so voi cac TEP (doi so khong phai co, khong phai gia tri cua co).
        def o_cua(doi):
            tep_i, co_i, i = [], {}, 0
            while i < len(doi):
                if doi[i] in ("--nguon", "--mau", "--ham"): co_i[doi[i]] = i; i += 2
                else: tep_i.append(i); i += 1
            vt = lambda i: "truoc" if i < tep_i[0] else "sau" if i > tep_i[-1] else "xen"
            return {("so_tep", len(tep_i))} | {(f"vi_tri{c}", vt(i)) for c, i in co_i.items()}
        can = ({("so_tep", n) for n in (1, 2, 3, 7)} | {(f"vi_tri{c}", v) for c in ("--nguon", "--mau") for v in ("truoc", "sau", "xen")}
               | {("vi_tri--ham", v) for v in ("truoc", "sau")})
        co_phu = set().union(*(o_cua(doi) for doi, _r, _m in cli.values()))
        if can - co_phu: hong.append(f"PHU_BANG: o chua co ca: {sorted(can - co_phu)}")
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", *doi], capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[0][5:]) if len(tong) == 1 else {}
            thuc = (r.returncode, len(tong), tuple(d.get(k) for k in COT))
            if thuc != (rc_mong, 1, mong): hong.append(f"{ten}: mong {(rc_mong, 1, mong)}, thuc {thuc}")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}", f"(truc tiep {len(ca)}, CLI {len(cli)})")
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

## Phụ lục K — cổng CON TRỎ v8: nhãn trộn đúng/sai/thiếu trong cùng khối, §0.16 (MỚI ở r17, nguyên văn)

Cùng cách chạy như Phụ lục E. `tu-kiem` in: `TU_KIEM DAT 163/163 (truc tiep 69, CLI 94)` (số lấy từ lần chạy khi dựng đặc tả, không gõ tay). So với Phụ lục J chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `10663fb6dc730e9fa61435e51738acf6f156123498c3588daab4b94732ebe9d6`.

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
            # r17 (luot 12): nhan DUNG / SAI / THIEU tron trong CUNG khoi, moi hoan vi thu tu — nhan phai dung NGAY sau cau
            # trich cua no; mot nhan hop le o CHO KHAC trong khoi khong duoc cuu mot cau trich thieu/sai nhan.
            **{ten: ("a.md", "Theo r1: " + "; ".join(Q2 + chu + Q2 + ({"dung": " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7),
                     "sai": " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7), "thieu": ""}[loai]) for chu, loai in zip(("abcdefgh", "ijklmnop", "qrstuvwx"), thu_tu)) + ".\n",
                     None, (0, 0, 0, sum(x != "dung" for x in thu_tu), sum(x == "dung" for x in thu_tu)))
               for ten, thu_tu in (("nhan_xau_truoc_nhan_dung", ("sai", "dung")), ("nhan_dung_truoc_nhan_xau", ("dung", "sai")),
                                   ("nhan_thieu_truoc_nhan_dung", ("thieu", "dung")), ("nhan_dung_truoc_nhan_thieu", ("dung", "thieu")),
                                   ("nhan_xau_thieu_dung", ("sai", "thieu", "dung")), ("nhan_thieu_xau_dung", ("thieu", "sai", "dung")),
                                   ("nhan_dung_xau_thieu", ("dung", "sai", "thieu")))},
            "nhan_sau_gach_duoi": ("a.md", "Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:doctrine" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
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
        # HOP DONG CLI — bang co tham quyen o dac ta r15 §0.14; cac ca SINH tu bang (to hop), khong liet ke tay.
        # Moi tep mau mang VEC TO ky vong viet tay (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN); ky vong cua mot lan chay
        # nhieu tep = TONG tung phan tu; rc ky vong = 1 khi LECH + KHONG_DO_DUOC + VI_PHAM > 0. Oracle chi cong va so sanh,
        # khong goi `kiem`/`main`/regex nao cua cong. Nguon CLI dung MAU TEN RIENG (`spec-r{n}.txt`) de `--mau` co rang.
        import itertools, subprocess as _sp
        nc = Path(t) / "nguon_cli"; nc.mkdir()
        (nc / "spec-r3.txt").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        dc = Path(t) / "cli"; dc.mkdir()
        TEP_CLI = {
            "sach.md": ("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", (1, 0, 0, 0, 0)),
            "lech.md": ("Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "lech2.md": ("Theo r3 " + CT0("r3:11 #00000000|so 11 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "thieu.md": ("Theo r9 " + CT0("r9:1 #00000000|khong co tep nao") + ".\n", (0, 0, 1, 0, 0)),
            "vipham.md": ("Theo r1: " + Q8 + ".\n", (0, 0, 0, 1, 0)),
            "nhan.md": ("Theo r1: " + Q8 + " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
            "nhan_gach.md": ("Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
        }
        for ten, (noi, _v) in TEP_CLI.items(): (dc / ten).write_text(noi, encoding="utf-8")
        COT = ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")
        CO = ["--nguon", str(nc), "--mau", "spec-r{n}.txt"]
        VI_TRI = {"co_truoc": lambda co, tep: co + tep, "co_sau": lambda co, tep: tep + co,
                  "co_xen": lambda co, tep: tep[:1] + co + tep[1:]}
        ds_tep = sorted(TEP_CLI)
        to_hop = [(x,) for x in ds_tep] + list(itertools.permutations(ds_tep, 2)) + [
            ("lech.md", "lech2.md", "vipham.md"), ("sach.md", "nhan.md", "nhan_gach.md"), ("thieu.md", "sach.md", "thieu.md"),
            tuple(ds_tep)]
        cli = {}
        for so, bo in enumerate(to_hop):
            vt = list(VI_TRI)[so % 3] if len(bo) > 1 else None
            for v in ([vt] if vt else list(VI_TRI)):
                mong = tuple(sum(TEP_CLI[x][1][c] for x in bo) for c in range(5))
                cli[f"cli_{v}_{'+'.join(bo)}"] = (VI_TRI[v](CO, [str(dc / x) for x in bo]), int(sum(mong[1:4]) > 0), mong)
        # --ham: tep 5 ham, XAU = {a, c, e}; ky vong VI_PHAM = so ten trong danh sach thuoc XAU (ten la khong tinh).
        XAU = {"a", "c", "e"}
        (dc / "h.py").write_text("".join(f"def {n}():\n    " + Q2 * 3 + f"Ham {n} nhac r1 " + (Q8 + " khong nhan" if n in XAU else "va khong trich gi")
                                 + ", du dai de qua nguong bon muoi.\n    " + Q2 * 3 + "\n\n\n" for n in "abcde"), encoding="utf-8")
        # r16 (luot 11): vi tri TUNG co la mot truc RIENG, tach khoi noi dung danh sach ham — moi danh sach x `--ham`
        # truoc / sau chinh tep; `--nguon`/`--mau` luan phien truoc / sau.
        for so, ds_ham in enumerate(("a", "b", "c", "e", "a,b", "b,c", "d,e", "b,c,d", "d,c,b", "b,zz,d", "zz", "a,b,c,d,e", "b,d")):
            vi = len(set(ds_ham.split(",")) & XAU)
            for vt_ham, tep in (("ham_truoc", ["--ham", ds_ham, str(dc / "h.py")]), ("ham_sau", [str(dc / "h.py"), "--ham", ds_ham])):
                cli[f"cli_{vt_ham}_{ds_ham}"] = ((CO + tep) if so % 2 == 0 else (tep + CO), int(vi > 0), (0, 0, 0, vi, 0))
        cli["cli_khong_ham_h"] = (CO + [str(dc / "h.py")], 1, (0, 0, 0, 3, 0))
        # KIEM PHU BANG MAY tren argv DA SINH (khong tren y dinh): moi o cua bang §0.14 phai co >= 1 ca. Vi tri cua moi co
        # tinh theo chi so trong argv so voi cac TEP (doi so khong phai co, khong phai gia tri cua co).
        def o_cua(doi):
            tep_i, co_i, i = [], {}, 0
            while i < len(doi):
                if doi[i] in ("--nguon", "--mau", "--ham"): co_i[doi[i]] = i; i += 2
                else: tep_i.append(i); i += 1
            vt = lambda i: "truoc" if i < tep_i[0] else "sau" if i > tep_i[-1] else "xen"
            return {("so_tep", len(tep_i))} | {(f"vi_tri{c}", vt(i)) for c, i in co_i.items()}
        can = ({("so_tep", n) for n in (1, 2, 3, 7)} | {(f"vi_tri{c}", v) for c in ("--nguon", "--mau") for v in ("truoc", "sau", "xen")}
               | {("vi_tri--ham", v) for v in ("truoc", "sau")})
        co_phu = set().union(*(o_cua(doi) for doi, _r, _m in cli.values()))
        if can - co_phu: hong.append(f"PHU_BANG: o chua co ca: {sorted(can - co_phu)}")
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", *doi], capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[0][5:]) if len(tong) == 1 else {}
            thuc = (r.returncode, len(tong), tuple(d.get(k) for k in COT))
            if thuc != (rc_mong, 1, mong): hong.append(f"{ten}: mong {(rc_mong, 1, mong)}, thuc {thuc}")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}", f"(truc tiep {len(ca)}, CLI {len(cli)})")
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

## Phụ lục L — cổng CON TRỎ v9: bảng lớp khoảng nối câu–nhãn, §0.17 (MỚI ở r18, nguyên văn)

Cùng cách chạy như Phụ lục E. `tu-kiem` in: `TU_KIEM DAT 234/234 (truc tiep 140, CLI 94)` (số lấy từ lần chạy khi dựng đặc tả, không gõ tay). So với Phụ lục K chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `4f8264a9546fda5df58418fbcb35b7a94ecc52b309788d6b6b89bdff369cff9a`.

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
            # r17 (luot 12): nhan DUNG / SAI / THIEU tron trong CUNG khoi, moi hoan vi thu tu — nhan phai dung NGAY sau cau
            # trich cua no; mot nhan hop le o CHO KHAC trong khoi khong duoc cuu mot cau trich thieu/sai nhan.
            **{ten: ("a.md", "Theo r1: " + "; ".join(Q2 + chu + Q2 + ({"dung": " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7),
                     "sai": " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7), "thieu": ""}[loai]) for chu, loai in zip(("abcdefgh", "ijklmnop", "qrstuvwx"), thu_tu)) + ".\n",
                     None, (0, 0, 0, sum(x != "dung" for x in thu_tu), sum(x == "dung" for x in thu_tu)))
               for ten, thu_tu in (("nhan_xau_truoc_nhan_dung", ("sai", "dung")), ("nhan_dung_truoc_nhan_xau", ("dung", "sai")),
                                   ("nhan_thieu_truoc_nhan_dung", ("thieu", "dung")), ("nhan_dung_truoc_nhan_thieu", ("dung", "thieu")),
                                   ("nhan_xau_thieu_dung", ("sai", "thieu", "dung")), ("nhan_thieu_xau_dung", ("thieu", "sai", "dung")),
                                   ("nhan_dung_xau_thieu", ("dung", "sai", "thieu")))},
            "nhan_sau_gach_duoi": ("a.md", "Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:doctrine" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "nhan_sau_markup_dam": ("a.md", "Theo r1: **" + Q8 + "** " + chr(0x27E6) + "nguon:verdict" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "ngoac_cong_vat_dong": ("a.md", "Theo r1: “abcd\nefgh”.\n", None, (0, 0, 0, 1, 0)),
            "rv_sau_gach_noi": ("a.md", "Theo ma-r1: " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "manh_5_am": ("a.md", "Theo r1 " + CT0("r1:1 #2bf318fb|ong m") + ".\n", None, (0, 0, 0, 1, 0)),
        })
        # r18 (luot 13, F2): BANG LOP KHOANG NOI cau-nhan, co tham quyen o dac ta r18 §0.17. Lop: (markup MO truoc cau,
        # khoang noi giua dau ngoac DONG va nhan, cuc). Ca SINH tu bang x hai kieu ngoac; ky vong chi doc CUC — DUONG
        # (0,0,0,0,1), AM (0,0,0,1,0) — khong qua regex nao cua cong. Markup phai DONG ngay sau cau roi moi toi khoang trang.
        DAU_CAU, NL = ";,.:!?", chr(0x27E6) + "nguon:ma" + chr(0x27E7)
        KHOANG_NOI = {"rong": ("", "", "DUONG"), "cach": ("", " ", "DUONG"), "cach_nhieu": ("", "   ", "DUONG"),
                      "tab": ("", "\t", "DUONG"), "xuong_dong": ("", "\n", "DUONG"), "cach_xuong_dong": ("", " \n  ", "DUONG"),
                      "sao": ("*", "*", "DUONG"), "sao_cach": ("*", "* ", "DUONG"), "gach": ("_", "_", "DUONG"),
                      "gach_cach": ("_", "_ ", "DUONG"), "sao_doi": ("**", "**", "DUONG"), "sao_doi_cach": ("**", "** ", "DUONG"),
                      "gach_doi_xuong_dong": ("__", "__\n", "DUONG"),
                      **{f"dau{i}": ("", c, "AM") for i, c in enumerate(DAU_CAU)},
                      **{f"dau{i}_cach": ("", c + " ", "AM") for i, c in enumerate(DAU_CAU)},
                      "sao_roi_dau": ("*", "*; ", "AM"), "cach_roi_dau": ("", " , ", "AM"), "cach_roi_sao": ("", " *", "AM"),
                      "chu": ("", " va ", "AM"), "chu_dinh": ("", "x ", "AM"), "noi_dung_xen": ("", " (ghi chu) ", "AM"),
                      "ngoac_dong": ("", ") ", "AM"), "gach_ngang": ("", " — ", "AM"), "doan_moi": ("", "\n\n", "AM")}
        MO_DAU = "Theo r1: "
        for lop, (mo, kn, cuc) in KHOANG_NOI.items():
            for kieu, q in (("thang", Q8), ("cong", C8)):
                ca[f"kn_{kieu}_{lop}"] = ("a.md", MO_DAU + mo + q + kn + NL + ".\n", None, (0, 0, 0, 0, 1) if cuc == "DUONG" else (0, 0, 0, 1, 0))
        # doi chung viet tay: nhan TRUOC cau; hai nhan hop le lien tiep; nhan sai roi nhan dung sau CUNG mot cau
        ca.update({"kn_nhan_truoc_cau": ("a.md", MO_DAU + NL + " " + Q8 + ".\n", None, (0, 0, 0, 1, 0)),
                   "kn_hai_nhan_lien_tiep": ("a.md", MO_DAU + Q8 + " " + NL + " " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
                   "kn_nhan_sai_roi_dung": ("a.md", MO_DAU + Q8 + " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7) + " " + NL + ".\n", None, (0, 0, 0, 1, 0))})
        # KIEM PHU BANG MAY tren tep DA SINH: tach khoang noi khoi chinh noi dung tep (khong doc lai bang), roi doi moi o.
        def o_kn(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; g = doc[doc.index(q) + len(q):doc.index(NL)]
            cuc = "DUONG" if ca[ten][3][4] else "AM"; than = g.lstrip("*_"); dau = g[:len(g) - len(than)]; o = set()
            if dau: o.add((kieu, cuc, "markup", dau, than != ""))
            if not g.strip(): o.add((kieu, cuc, "trang", g))
            if than and than[0] in DAU_CAU: o.add((kieu, cuc, "dau", than[0], than[1:] != ""))
            if any(c.isalnum() for c in g): o.add((kieu, cuc, "chu"))
            if g[:1].isspace() and g.strip()[:1] in ("*", "_"): o.add((kieu, cuc, "trang_roi_markup"))
            return o
        can_kn = {(k, "DUONG", "trang", w) for k in ("thang", "cong") for w in ("", " ", "\t", "\n")} | {
            (k, "DUONG", "markup", m, t) for k in ("thang", "cong") for m in ("*", "_", "**", "__") for t in ((False, True) if len(m) == 1 else (True,))} | {
            (k, "AM", "dau", c, t) for k in ("thang", "cong") for c in DAU_CAU for t in (False, True)} | {
            (k, "AM", x) for k in ("thang", "cong") for x in ("chu", "trang_roi_markup")} | {(k, "AM", "trang", "\n\n") for k in ("thang", "cong")}
        phu_kn = set().union(*(o_kn(ten, v[1]) for ten, v in ca.items() if ten.startswith(("kn_thang_", "kn_cong_"))))
        hong = [f"PHU_KHOANG_NOI: o chua co ca: {sorted(can_kn - phu_kn, key=str)}"] if can_kn - phu_kn else []
        for ten, (tep, doc, ham, mong) in ca.items():
            p = Path(t) / ten / tep; p.parent.mkdir(); p.write_text(doc, encoding="utf-8")
            d = kiem(t, "r{n}.md", p, ham)
            thuc = (d["DUNG"], d["LECH"], d["KHONG_DO_DUOC"], d["VI_PHAM"], d["CO_NHAN"])
            if thuc != mong: hong.append(f"{ten}: mong {mong}, thuc {thuc}")
        # HOP DONG CLI — bang co tham quyen o dac ta r15 §0.14; cac ca SINH tu bang (to hop), khong liet ke tay.
        # Moi tep mau mang VEC TO ky vong viet tay (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN); ky vong cua mot lan chay
        # nhieu tep = TONG tung phan tu; rc ky vong = 1 khi LECH + KHONG_DO_DUOC + VI_PHAM > 0. Oracle chi cong va so sanh,
        # khong goi `kiem`/`main`/regex nao cua cong. Nguon CLI dung MAU TEN RIENG (`spec-r{n}.txt`) de `--mau` co rang.
        import itertools, subprocess as _sp
        nc = Path(t) / "nguon_cli"; nc.mkdir()
        (nc / "spec-r3.txt").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        dc = Path(t) / "cli"; dc.mkdir()
        TEP_CLI = {
            "sach.md": ("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", (1, 0, 0, 0, 0)),
            "lech.md": ("Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "lech2.md": ("Theo r3 " + CT0("r3:11 #00000000|so 11 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "thieu.md": ("Theo r9 " + CT0("r9:1 #00000000|khong co tep nao") + ".\n", (0, 0, 1, 0, 0)),
            "vipham.md": ("Theo r1: " + Q8 + ".\n", (0, 0, 0, 1, 0)),
            "nhan.md": ("Theo r1: " + Q8 + " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
            "nhan_gach.md": ("Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
        }
        for ten, (noi, _v) in TEP_CLI.items(): (dc / ten).write_text(noi, encoding="utf-8")
        COT = ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")
        CO = ["--nguon", str(nc), "--mau", "spec-r{n}.txt"]
        VI_TRI = {"co_truoc": lambda co, tep: co + tep, "co_sau": lambda co, tep: tep + co,
                  "co_xen": lambda co, tep: tep[:1] + co + tep[1:]}
        ds_tep = sorted(TEP_CLI)
        to_hop = [(x,) for x in ds_tep] + list(itertools.permutations(ds_tep, 2)) + [
            ("lech.md", "lech2.md", "vipham.md"), ("sach.md", "nhan.md", "nhan_gach.md"), ("thieu.md", "sach.md", "thieu.md"),
            tuple(ds_tep)]
        cli = {}
        for so, bo in enumerate(to_hop):
            vt = list(VI_TRI)[so % 3] if len(bo) > 1 else None
            for v in ([vt] if vt else list(VI_TRI)):
                mong = tuple(sum(TEP_CLI[x][1][c] for x in bo) for c in range(5))
                cli[f"cli_{v}_{'+'.join(bo)}"] = (VI_TRI[v](CO, [str(dc / x) for x in bo]), int(sum(mong[1:4]) > 0), mong)
        # --ham: tep 5 ham, XAU = {a, c, e}; ky vong VI_PHAM = so ten trong danh sach thuoc XAU (ten la khong tinh).
        XAU = {"a", "c", "e"}
        (dc / "h.py").write_text("".join(f"def {n}():\n    " + Q2 * 3 + f"Ham {n} nhac r1 " + (Q8 + " khong nhan" if n in XAU else "va khong trich gi")
                                 + ", du dai de qua nguong bon muoi.\n    " + Q2 * 3 + "\n\n\n" for n in "abcde"), encoding="utf-8")
        # r16 (luot 11): vi tri TUNG co la mot truc RIENG, tach khoi noi dung danh sach ham — moi danh sach x `--ham`
        # truoc / sau chinh tep; `--nguon`/`--mau` luan phien truoc / sau.
        for so, ds_ham in enumerate(("a", "b", "c", "e", "a,b", "b,c", "d,e", "b,c,d", "d,c,b", "b,zz,d", "zz", "a,b,c,d,e", "b,d")):
            vi = len(set(ds_ham.split(",")) & XAU)
            for vt_ham, tep in (("ham_truoc", ["--ham", ds_ham, str(dc / "h.py")]), ("ham_sau", [str(dc / "h.py"), "--ham", ds_ham])):
                cli[f"cli_{vt_ham}_{ds_ham}"] = ((CO + tep) if so % 2 == 0 else (tep + CO), int(vi > 0), (0, 0, 0, vi, 0))
        cli["cli_khong_ham_h"] = (CO + [str(dc / "h.py")], 1, (0, 0, 0, 3, 0))
        # KIEM PHU BANG MAY tren argv DA SINH (khong tren y dinh): moi o cua bang §0.14 phai co >= 1 ca. Vi tri cua moi co
        # tinh theo chi so trong argv so voi cac TEP (doi so khong phai co, khong phai gia tri cua co).
        def o_cua(doi):
            tep_i, co_i, i = [], {}, 0
            while i < len(doi):
                if doi[i] in ("--nguon", "--mau", "--ham"): co_i[doi[i]] = i; i += 2
                else: tep_i.append(i); i += 1
            vt = lambda i: "truoc" if i < tep_i[0] else "sau" if i > tep_i[-1] else "xen"
            return {("so_tep", len(tep_i))} | {(f"vi_tri{c}", vt(i)) for c, i in co_i.items()}
        can = ({("so_tep", n) for n in (1, 2, 3, 7)} | {(f"vi_tri{c}", v) for c in ("--nguon", "--mau") for v in ("truoc", "sau", "xen")}
               | {("vi_tri--ham", v) for v in ("truoc", "sau")})
        co_phu = set().union(*(o_cua(doi) for doi, _r, _m in cli.values()))
        if can - co_phu: hong.append(f"PHU_BANG: o chua co ca: {sorted(can - co_phu)}")
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", *doi], capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[0][5:]) if len(tong) == 1 else {}
            thuc = (r.returncode, len(tong), tuple(d.get(k) for k in COT))
            if thuc != (rc_mong, 1, mong): hong.append(f"{ten}: mong {(rc_mong, 1, mong)}, thuc {thuc}")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}", f"(truc tiep {len(ca)}, CLI {len(cli)})")
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

## Phụ lục M — cổng CON TRỎ v10: parser cưỡng chế cặp markup; bảng cặp markup và ranh giới code, §0.18 (MỚI ở r19, nguyên văn)

Cùng cách chạy như Phụ lục E. `tu-kiem` in: `TU_KIEM DAT 292/292 (truc tiep 198, CLI 94)` (số lấy từ lần chạy khi dựng đặc tả, không gõ tay). So với Phụ lục L: parser đổi (xem §0.18) và `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `022858235b5e2962df892455edd856c8765786275f24e848ac50631588df2d73`.

```python
"""Con tro nguon cho dac ta R378 (r10 #574) — thay moi loi trich VIET TAY cua revision khac.

  CON TRO   ⟦rN:L #h|manh⟧ hoac ⟦rN:L-M #h|manh⟧ : dong L (den M) cua dac ta revision N; h = 8 hex dau cua
            sha256 noi dung cac dong ay sau chuan hoa (bo khoang trang dau/cuoi moi dong, gop khoang trang). Tro sai
            dong => h lech => DO. `manh` (BAT BUOC tu r11, >= 6 ky tu) la cum chu ma cau dan con tro dang noi toi; no
            phai NAM TRONG cac dong duoc tro (so sau khi bo `*` va dau backtick, gop khoang trang) — tro dung bam ma
            sai dong CAN TRO (F1d #574 luot 6: r3:322 thay vi 323-324) => DO. Sinh bang lenh `sinh`, KHONG go tay.
  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac (markup giua cau va nhan chi duoc la markup DONG, dao nguoc dung
            markup MO ngay truoc cau; tu r19): chuoi ay KHONG phai loi cua mot revision (K thuoc
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
NHAN = re.compile(r"([*_]*)\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
MO = re.compile(r"[*_]*\Z")  # markup MO ngay truoc dau ngoac mo cua cau (r19)
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
            n = NHAN.match(k, m.end())  # r19: markup DONG giua cau va nhan phai la dao nguoc DUNG markup MO ngay truoc cau
            if n and n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1]: dem["CO_NHAN"] += 1; continue
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
            # r17 (luot 12): nhan DUNG / SAI / THIEU tron trong CUNG khoi, moi hoan vi thu tu — nhan phai dung NGAY sau cau
            # trich cua no; mot nhan hop le o CHO KHAC trong khoi khong duoc cuu mot cau trich thieu/sai nhan.
            **{ten: ("a.md", "Theo r1: " + "; ".join(Q2 + chu + Q2 + ({"dung": " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7),
                     "sai": " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7), "thieu": ""}[loai]) for chu, loai in zip(("abcdefgh", "ijklmnop", "qrstuvwx"), thu_tu)) + ".\n",
                     None, (0, 0, 0, sum(x != "dung" for x in thu_tu), sum(x == "dung" for x in thu_tu)))
               for ten, thu_tu in (("nhan_xau_truoc_nhan_dung", ("sai", "dung")), ("nhan_dung_truoc_nhan_xau", ("dung", "sai")),
                                   ("nhan_thieu_truoc_nhan_dung", ("thieu", "dung")), ("nhan_dung_truoc_nhan_thieu", ("dung", "thieu")),
                                   ("nhan_xau_thieu_dung", ("sai", "thieu", "dung")), ("nhan_thieu_xau_dung", ("thieu", "sai", "dung")),
                                   ("nhan_dung_xau_thieu", ("dung", "sai", "thieu")))},
            "nhan_sau_gach_duoi": ("a.md", "Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:doctrine" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "nhan_sau_markup_dam": ("a.md", "Theo r1: **" + Q8 + "** " + chr(0x27E6) + "nguon:verdict" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "ngoac_cong_vat_dong": ("a.md", "Theo r1: “abcd\nefgh”.\n", None, (0, 0, 0, 1, 0)),
            "rv_sau_gach_noi": ("a.md", "Theo ma-r1: " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "manh_5_am": ("a.md", "Theo r1 " + CT0("r1:1 #2bf318fb|ong m") + ".\n", None, (0, 0, 0, 1, 0)),
        })
        # r18 (luot 13, F2): BANG LOP KHOANG NOI cau-nhan, co tham quyen o dac ta r18 §0.17. Lop: (markup MO truoc cau,
        # khoang noi giua dau ngoac DONG va nhan, cuc). Ca SINH tu bang x hai kieu ngoac; ky vong chi doc CUC — DUONG
        # (0,0,0,0,1), AM (0,0,0,1,0) — khong qua regex nao cua cong. Markup phai DONG ngay sau cau roi moi toi khoang trang.
        DAU_CAU, NL = ";,.:!?", chr(0x27E6) + "nguon:ma" + chr(0x27E7)
        KHOANG_NOI = {"rong": ("", "", "DUONG"), "cach": ("", " ", "DUONG"), "cach_nhieu": ("", "   ", "DUONG"),
                      "tab": ("", "\t", "DUONG"), "xuong_dong": ("", "\n", "DUONG"), "cach_xuong_dong": ("", " \n  ", "DUONG"),
                      "sao": ("*", "*", "DUONG"), "sao_cach": ("*", "* ", "DUONG"), "gach": ("_", "_", "DUONG"),
                      "gach_cach": ("_", "_ ", "DUONG"), "sao_doi": ("**", "**", "DUONG"), "sao_doi_cach": ("**", "** ", "DUONG"),
                      "gach_doi_xuong_dong": ("__", "__\n", "DUONG"),
                      **{f"dau{i}": ("", c, "AM") for i, c in enumerate(DAU_CAU)},
                      **{f"dau{i}_cach": ("", c + " ", "AM") for i, c in enumerate(DAU_CAU)},
                      "sao_roi_dau": ("*", "*; ", "AM"), "cach_roi_dau": ("", " , ", "AM"), "cach_roi_sao": ("", " *", "AM"),
                      "chu": ("", " va ", "AM"), "chu_dinh": ("", "x ", "AM"), "noi_dung_xen": ("", " (ghi chu) ", "AM"),
                      "ngoac_dong": ("", ") ", "AM"), "gach_ngang": ("", " — ", "AM"), "doan_moi": ("", "\n\n", "AM")}
        MO_DAU = "Theo r1: "
        for lop, (mo, kn, cuc) in KHOANG_NOI.items():
            for kieu, q in (("thang", Q8), ("cong", C8)):
                ca[f"kn_{kieu}_{lop}"] = ("a.md", MO_DAU + mo + q + kn + NL + ".\n", None, (0, 0, 0, 0, 1) if cuc == "DUONG" else (0, 0, 0, 1, 0))
        # doi chung viet tay: nhan TRUOC cau; hai nhan hop le lien tiep; nhan sai roi nhan dung sau CUNG mot cau
        ca.update({"kn_nhan_truoc_cau": ("a.md", MO_DAU + NL + " " + Q8 + ".\n", None, (0, 0, 0, 1, 0)),
                   "kn_hai_nhan_lien_tiep": ("a.md", MO_DAU + Q8 + " " + NL + " " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
                   "kn_nhan_sai_roi_dung": ("a.md", MO_DAU + Q8 + " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7) + " " + NL + ".\n", None, (0, 0, 0, 1, 0))})
        # KIEM PHU BANG MAY tren tep DA SINH: tach khoang noi khoi chinh noi dung tep (khong doc lai bang), roi doi moi o.
        def o_kn(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; g = doc[doc.index(q) + len(q):doc.index(NL)]
            cuc = "DUONG" if ca[ten][3][4] else "AM"; than = g.lstrip("*_"); dau = g[:len(g) - len(than)]; o = set()
            if dau: o.add((kieu, cuc, "markup", dau, than != ""))
            if not g.strip(): o.add((kieu, cuc, "trang", g))
            if than and than[0] in DAU_CAU: o.add((kieu, cuc, "dau", than[0], than[1:] != ""))
            if any(c.isalnum() for c in g): o.add((kieu, cuc, "chu"))
            if g[:1].isspace() and g.strip()[:1] in ("*", "_"): o.add((kieu, cuc, "trang_roi_markup"))
            return o
        can_kn = {(k, "DUONG", "trang", w) for k in ("thang", "cong") for w in ("", " ", "\t", "\n")} | {
            (k, "DUONG", "markup", m, t) for k in ("thang", "cong") for m in ("*", "_", "**", "__") for t in ((False, True) if len(m) == 1 else (True,))} | {
            (k, "AM", "dau", c, t) for k in ("thang", "cong") for c in DAU_CAU for t in (False, True)} | {
            (k, "AM", x) for k in ("thang", "cong") for x in ("chu", "trang_roi_markup")} | {(k, "AM", "trang", "\n\n") for k in ("thang", "cong")}
        phu_kn = set().union(*(o_kn(ten, v[1]) for ten, v in ca.items() if ten.startswith(("kn_thang_", "kn_cong_"))))
        hong = [f"PHU_KHOANG_NOI: o chua co ca: {sorted(can_kn - phu_kn, key=str)}"] if can_kn - phu_kn else []
        # r19 (luot 14, F3): BANG CAP MARKUP — markup DONG giua cau va nhan phai la dao nguoc DUNG markup MO ngay truoc cau.
        # (mo, khoang noi, cuc); ky vong chi doc CUC. Loai o tinh LAI tu tep da sinh, khong doc bang.
        CAP_MARKUP = {"dung_sao": ("*", "*", "DUONG"), "dung_gach": ("_", "_ ", "DUONG"), "dung_sao_doi": ("**", "** ", "DUONG"),
                      "dung_gach_doi": ("__", "__", "DUONG"), "dung_tron": ("*_", "_* ", "DUONG"), "dung_tron_nguoc": ("_*", "*_", "DUONG"),
                      "dung_ba": ("***", "*** ", "DUONG"), "thieu_mo_sao": ("", "* ", "AM"), "thieu_mo_gach": ("", "_", "AM"),
                      "thieu_mo_doi": ("", "** ", "AM"), "khac_loai_sao_gach": ("*", "_ ", "AM"), "khac_loai_gach_sao": ("_", "*", "AM"),
                      "khac_loai_doi": ("**", "__ ", "AM"), "khac_loai_sai_thu_tu": ("*_", "*_ ", "AM"), "dai_ngan": ("**", "* ", "AM"),
                      "ngan_dai": ("*", "** ", "AM"), "gach_ngan_dai": ("_", "__", "AM"), "ba_hai": ("***", "** ", "AM"),
                      "mo_khong_dong_sao": ("*", " ", "AM"), "mo_khong_dong_doi": ("**", "", "AM"), "mo_khong_dong_gach": ("_", "\n", "AM")}
        # r19 (luot 14, F2 vong 8): BANG RANH GIOI code–van ban; {q} = cau trich. Ky vong viet tay tung dong.
        BIEN_CODE = {"code_xen": ("{q} `x` " + NL, "AM"), "code_lien_sau_cau": ("{q}`x` " + NL, "AM"),
                     "code_truoc_cau": ("`x` {q} " + NL, "DUONG"), "cau_trong_code": ("`{q}` " + NL, "KHONG"),
                     "nhan_trong_code": ("{q} `" + NL + "`", "AM"), "nhan_lien_sau_cau": ("{q}" + NL, "DUONG"),
                     "markup_roi_code_xen": ("*{q}* `x` " + NL, "AM"), "markup_mo_trong_code": ("`*`{q}* " + NL, "AM")}
        VEC = {"DUONG": (0, 0, 0, 0, 1), "AM": (0, 0, 0, 1, 0), "KHONG": (0, 0, 0, 0, 0)}
        for kieu, q in (("thang", Q8), ("cong", C8)):
            for lop, (mo, kn, cuc) in CAP_MARKUP.items(): ca[f"cm_{kieu}_{lop}"] = ("a.md", MO_DAU + mo + q + kn + NL + ".\n", None, VEC[cuc])
            for lop, (mau, cuc) in BIEN_CODE.items(): ca[f"bc_{kieu}_{lop}"] = ("a.md", MO_DAU + mau.format(q=q) + ".\n", None, VEC[cuc])
        def o_cm(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; mo = doc[len(MO_DAU):doc.index(q)]
            g = doc[doc.index(q) + len(q):doc.index(NL)]; dong = g[:len(g) - len(g.lstrip("*_"))]; cuc = "DUONG" if ca[ten][3][4] else "AM"
            loai = ("dung" if dong == mo[::-1] else "thieu_mo" if not mo else "mo_khong_dong" if not dong
                    else "khac_do_dai" if len(dong) != len(mo) else "khac_loai")
            return {(kieu, cuc, loai, "".join(sorted(set(mo + dong))), max(len(mo), len(dong)) > 1)}  # loai x ky tu x nhieu ky tu
        def o_bc(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; a, b = doc.index(q), doc.index(q) + len(q); c = doc.index(NL)
            o = {(kieu, "nhan_lien_sau_cau")} if c == b else set()
            for x in re.finditer(r"`[^`\n]*`", doc):
                o |= {(kieu, "code_truoc_cau")} if x.end() <= a else {(kieu, "cau_trong_code")} if x.start() < a and b <= x.end() else set()
                o |= {(kieu, "code_xen", b == x.start(), doc[b:x.start()].strip() != "")} if b <= x.start() and x.end() <= c else {(kieu, "nhan_trong_code")} if x.start() < c < x.end() else set()
            return o
        O_CM = {"DUONG": {"dung": (("*", 0), ("_", 0), ("*", 1), ("_", 1), ("*_", 1))},
                "AM": {"thieu_mo": (("*", 0), ("_", 0), ("*", 1)), "khac_loai": (("*_", 0), ("*_", 1)),
                       "khac_do_dai": (("*", 1), ("_", 1)), "mo_khong_dong": (("*", 0), ("*", 1), ("_", 0))}}
        can_cm = {(k, cuc, loai, ky, bool(nhieu)) for k in ("thang", "cong") for cuc, d in O_CM.items() for loai, os_ in d.items() for ky, nhieu in os_}
        can_bc = {(k, x) for k in ("thang", "cong") for x in ("cau_trong_code", "code_truoc_cau", "nhan_lien_sau_cau", "nhan_trong_code")} | {
            (k, "code_xen", lien, markup) for k in ("thang", "cong") for lien, markup in ((False, False), (True, False), (False, True))}
        phu_cm = set().union(*(o_cm(t_, v[1]) for t_, v in ca.items() if t_.startswith("cm_")))
        phu_bc = set().union(*(o_bc(t_, v[1]) for t_, v in ca.items() if t_.startswith("bc_")))
        hong += [f"PHU_CAP_MARKUP: o chua co ca: {sorted(can_cm - phu_cm, key=str)}"] if can_cm - phu_cm else []
        hong += [f"PHU_RANH_GIOI_CODE: o chua co ca: {sorted(can_bc - phu_bc)}"] if can_bc - phu_bc else []
        for ten, (tep, doc, ham, mong) in ca.items():
            p = Path(t) / ten / tep; p.parent.mkdir(); p.write_text(doc, encoding="utf-8")
            d = kiem(t, "r{n}.md", p, ham)
            thuc = (d["DUNG"], d["LECH"], d["KHONG_DO_DUOC"], d["VI_PHAM"], d["CO_NHAN"])
            if thuc != mong: hong.append(f"{ten}: mong {mong}, thuc {thuc}")
        # HOP DONG CLI — bang co tham quyen o dac ta r15 §0.14; cac ca SINH tu bang (to hop), khong liet ke tay.
        # Moi tep mau mang VEC TO ky vong viet tay (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN); ky vong cua mot lan chay
        # nhieu tep = TONG tung phan tu; rc ky vong = 1 khi LECH + KHONG_DO_DUOC + VI_PHAM > 0. Oracle chi cong va so sanh,
        # khong goi `kiem`/`main`/regex nao cua cong. Nguon CLI dung MAU TEN RIENG (`spec-r{n}.txt`) de `--mau` co rang.
        import itertools, subprocess as _sp
        nc = Path(t) / "nguon_cli"; nc.mkdir()
        (nc / "spec-r3.txt").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        dc = Path(t) / "cli"; dc.mkdir()
        TEP_CLI = {
            "sach.md": ("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", (1, 0, 0, 0, 0)),
            "lech.md": ("Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "lech2.md": ("Theo r3 " + CT0("r3:11 #00000000|so 11 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "thieu.md": ("Theo r9 " + CT0("r9:1 #00000000|khong co tep nao") + ".\n", (0, 0, 1, 0, 0)),
            "vipham.md": ("Theo r1: " + Q8 + ".\n", (0, 0, 0, 1, 0)),
            "nhan.md": ("Theo r1: " + Q8 + " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
            "nhan_gach.md": ("Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
        }
        for ten, (noi, _v) in TEP_CLI.items(): (dc / ten).write_text(noi, encoding="utf-8")
        COT = ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")
        CO = ["--nguon", str(nc), "--mau", "spec-r{n}.txt"]
        VI_TRI = {"co_truoc": lambda co, tep: co + tep, "co_sau": lambda co, tep: tep + co,
                  "co_xen": lambda co, tep: tep[:1] + co + tep[1:]}
        ds_tep = sorted(TEP_CLI)
        to_hop = [(x,) for x in ds_tep] + list(itertools.permutations(ds_tep, 2)) + [
            ("lech.md", "lech2.md", "vipham.md"), ("sach.md", "nhan.md", "nhan_gach.md"), ("thieu.md", "sach.md", "thieu.md"),
            tuple(ds_tep)]
        cli = {}
        for so, bo in enumerate(to_hop):
            vt = list(VI_TRI)[so % 3] if len(bo) > 1 else None
            for v in ([vt] if vt else list(VI_TRI)):
                mong = tuple(sum(TEP_CLI[x][1][c] for x in bo) for c in range(5))
                cli[f"cli_{v}_{'+'.join(bo)}"] = (VI_TRI[v](CO, [str(dc / x) for x in bo]), int(sum(mong[1:4]) > 0), mong)
        # --ham: tep 5 ham, XAU = {a, c, e}; ky vong VI_PHAM = so ten trong danh sach thuoc XAU (ten la khong tinh).
        XAU = {"a", "c", "e"}
        (dc / "h.py").write_text("".join(f"def {n}():\n    " + Q2 * 3 + f"Ham {n} nhac r1 " + (Q8 + " khong nhan" if n in XAU else "va khong trich gi")
                                 + ", du dai de qua nguong bon muoi.\n    " + Q2 * 3 + "\n\n\n" for n in "abcde"), encoding="utf-8")
        # r16 (luot 11): vi tri TUNG co la mot truc RIENG, tach khoi noi dung danh sach ham — moi danh sach x `--ham`
        # truoc / sau chinh tep; `--nguon`/`--mau` luan phien truoc / sau.
        for so, ds_ham in enumerate(("a", "b", "c", "e", "a,b", "b,c", "d,e", "b,c,d", "d,c,b", "b,zz,d", "zz", "a,b,c,d,e", "b,d")):
            vi = len(set(ds_ham.split(",")) & XAU)
            for vt_ham, tep in (("ham_truoc", ["--ham", ds_ham, str(dc / "h.py")]), ("ham_sau", [str(dc / "h.py"), "--ham", ds_ham])):
                cli[f"cli_{vt_ham}_{ds_ham}"] = ((CO + tep) if so % 2 == 0 else (tep + CO), int(vi > 0), (0, 0, 0, vi, 0))
        cli["cli_khong_ham_h"] = (CO + [str(dc / "h.py")], 1, (0, 0, 0, 3, 0))
        # KIEM PHU BANG MAY tren argv DA SINH (khong tren y dinh): moi o cua bang §0.14 phai co >= 1 ca. Vi tri cua moi co
        # tinh theo chi so trong argv so voi cac TEP (doi so khong phai co, khong phai gia tri cua co).
        def o_cua(doi):
            tep_i, co_i, i = [], {}, 0
            while i < len(doi):
                if doi[i] in ("--nguon", "--mau", "--ham"): co_i[doi[i]] = i; i += 2
                else: tep_i.append(i); i += 1
            vt = lambda i: "truoc" if i < tep_i[0] else "sau" if i > tep_i[-1] else "xen"
            return {("so_tep", len(tep_i))} | {(f"vi_tri{c}", vt(i)) for c, i in co_i.items()}
        can = ({("so_tep", n) for n in (1, 2, 3, 7)} | {(f"vi_tri{c}", v) for c in ("--nguon", "--mau") for v in ("truoc", "sau", "xen")}
               | {("vi_tri--ham", v) for v in ("truoc", "sau")})
        co_phu = set().union(*(o_cua(doi) for doi, _r, _m in cli.values()))
        if can - co_phu: hong.append(f"PHU_BANG: o chua co ca: {sorted(can - co_phu)}")
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", *doi], capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[0][5:]) if len(tong) == 1 else {}
            thuc = (r.returncode, len(tong), tuple(d.get(k) for k in COT))
            if thuc != (rc_mong, 1, mong): hong.append(f"{ten}: mong {(rc_mong, 1, mong)}, thuc {thuc}")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}", f"(truc tiep {len(ca)}, CLI {len(cli)})")
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

## Phụ lục N — cổng CON TRỎ v11: trục vị trí câu, lần xuất hiện, độ dài markup, §0.19 (MỚI ở r20, nguyên văn)

Cùng cách chạy như Phụ lục E. `tu-kiem` in: `TU_KIEM DAT 348/348 (truc tiep 254, CLI 94)` (số lấy từ lần chạy khi dựng đặc tả, không gõ tay). So với Phụ lục M chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `9f9067a5c02f2d6e764b93c931f1f55654c378d418ec02b497feffc0f6496d2a`.

```python
"""Con tro nguon cho dac ta R378 (r10 #574) — thay moi loi trich VIET TAY cua revision khac.

  CON TRO   ⟦rN:L #h|manh⟧ hoac ⟦rN:L-M #h|manh⟧ : dong L (den M) cua dac ta revision N; h = 8 hex dau cua
            sha256 noi dung cac dong ay sau chuan hoa (bo khoang trang dau/cuoi moi dong, gop khoang trang). Tro sai
            dong => h lech => DO. `manh` (BAT BUOC tu r11, >= 6 ky tu) la cum chu ma cau dan con tro dang noi toi; no
            phai NAM TRONG cac dong duoc tro (so sau khi bo `*` va dau backtick, gop khoang trang) — tro dung bam ma
            sai dong CAN TRO (F1d #574 luot 6: r3:322 thay vi 323-324) => DO. Sinh bang lenh `sinh`, KHONG go tay.
  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac (markup giua cau va nhan chi duoc la markup DONG, dao nguoc dung
            markup MO ngay truoc cau; tu r19): chuoi ay KHONG phai loi cua mot revision (K thuoc
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
NHAN = re.compile(r"([*_]*)\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
MO = re.compile(r"[*_]*\Z")  # markup MO ngay truoc dau ngoac mo cua cau (r19)
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
            n = NHAN.match(k, m.end())  # r19: markup DONG giua cau va nhan phai la dao nguoc DUNG markup MO ngay truoc cau
            if n and n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1]: dem["CO_NHAN"] += 1; continue
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
            # r17 (luot 12): nhan DUNG / SAI / THIEU tron trong CUNG khoi, moi hoan vi thu tu — nhan phai dung NGAY sau cau
            # trich cua no; mot nhan hop le o CHO KHAC trong khoi khong duoc cuu mot cau trich thieu/sai nhan.
            **{ten: ("a.md", "Theo r1: " + "; ".join(Q2 + chu + Q2 + ({"dung": " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7),
                     "sai": " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7), "thieu": ""}[loai]) for chu, loai in zip(("abcdefgh", "ijklmnop", "qrstuvwx"), thu_tu)) + ".\n",
                     None, (0, 0, 0, sum(x != "dung" for x in thu_tu), sum(x == "dung" for x in thu_tu)))
               for ten, thu_tu in (("nhan_xau_truoc_nhan_dung", ("sai", "dung")), ("nhan_dung_truoc_nhan_xau", ("dung", "sai")),
                                   ("nhan_thieu_truoc_nhan_dung", ("thieu", "dung")), ("nhan_dung_truoc_nhan_thieu", ("dung", "thieu")),
                                   ("nhan_xau_thieu_dung", ("sai", "thieu", "dung")), ("nhan_thieu_xau_dung", ("thieu", "sai", "dung")),
                                   ("nhan_dung_xau_thieu", ("dung", "sai", "thieu")))},
            "nhan_sau_gach_duoi": ("a.md", "Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:doctrine" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "nhan_sau_markup_dam": ("a.md", "Theo r1: **" + Q8 + "** " + chr(0x27E6) + "nguon:verdict" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "ngoac_cong_vat_dong": ("a.md", "Theo r1: “abcd\nefgh”.\n", None, (0, 0, 0, 1, 0)),
            "rv_sau_gach_noi": ("a.md", "Theo ma-r1: " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "manh_5_am": ("a.md", "Theo r1 " + CT0("r1:1 #2bf318fb|ong m") + ".\n", None, (0, 0, 0, 1, 0)),
        })
        # r18 (luot 13, F2): BANG LOP KHOANG NOI cau-nhan, co tham quyen o dac ta r18 §0.17. Lop: (markup MO truoc cau,
        # khoang noi giua dau ngoac DONG va nhan, cuc). Ca SINH tu bang x hai kieu ngoac; ky vong chi doc CUC — DUONG
        # (0,0,0,0,1), AM (0,0,0,1,0) — khong qua regex nao cua cong. Markup phai DONG ngay sau cau roi moi toi khoang trang.
        DAU_CAU, NL = ";,.:!?", chr(0x27E6) + "nguon:ma" + chr(0x27E7)
        KHOANG_NOI = {"rong": ("", "", "DUONG"), "cach": ("", " ", "DUONG"), "cach_nhieu": ("", "   ", "DUONG"),
                      "tab": ("", "\t", "DUONG"), "xuong_dong": ("", "\n", "DUONG"), "cach_xuong_dong": ("", " \n  ", "DUONG"),
                      "sao": ("*", "*", "DUONG"), "sao_cach": ("*", "* ", "DUONG"), "gach": ("_", "_", "DUONG"),
                      "gach_cach": ("_", "_ ", "DUONG"), "sao_doi": ("**", "**", "DUONG"), "sao_doi_cach": ("**", "** ", "DUONG"),
                      "gach_doi_xuong_dong": ("__", "__\n", "DUONG"),
                      **{f"dau{i}": ("", c, "AM") for i, c in enumerate(DAU_CAU)},
                      **{f"dau{i}_cach": ("", c + " ", "AM") for i, c in enumerate(DAU_CAU)},
                      "sao_roi_dau": ("*", "*; ", "AM"), "cach_roi_dau": ("", " , ", "AM"), "cach_roi_sao": ("", " *", "AM"),
                      "chu": ("", " va ", "AM"), "chu_dinh": ("", "x ", "AM"), "noi_dung_xen": ("", " (ghi chu) ", "AM"),
                      "ngoac_dong": ("", ") ", "AM"), "gach_ngang": ("", " — ", "AM"), "doan_moi": ("", "\n\n", "AM")}
        MO_DAU = "Theo r1: "
        for lop, (mo, kn, cuc) in KHOANG_NOI.items():
            for kieu, q in (("thang", Q8), ("cong", C8)):
                ca[f"kn_{kieu}_{lop}"] = ("a.md", MO_DAU + mo + q + kn + NL + ".\n", None, (0, 0, 0, 0, 1) if cuc == "DUONG" else (0, 0, 0, 1, 0))
        # doi chung viet tay: nhan TRUOC cau; hai nhan hop le lien tiep; nhan sai roi nhan dung sau CUNG mot cau
        ca.update({"kn_nhan_truoc_cau": ("a.md", MO_DAU + NL + " " + Q8 + ".\n", None, (0, 0, 0, 1, 0)),
                   "kn_hai_nhan_lien_tiep": ("a.md", MO_DAU + Q8 + " " + NL + " " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
                   "kn_nhan_sai_roi_dung": ("a.md", MO_DAU + Q8 + " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7) + " " + NL + ".\n", None, (0, 0, 0, 1, 0))})
        # KIEM PHU BANG MAY tren tep DA SINH: tach khoang noi khoi chinh noi dung tep (khong doc lai bang), roi doi moi o.
        def o_kn(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; g = doc[doc.index(q) + len(q):doc.index(NL)]
            cuc = "DUONG" if ca[ten][3][4] else "AM"; than = g.lstrip("*_"); dau = g[:len(g) - len(than)]; o = set()
            if dau: o.add((kieu, cuc, "markup", dau, than != ""))
            if not g.strip(): o.add((kieu, cuc, "trang", g))
            if than and than[0] in DAU_CAU: o.add((kieu, cuc, "dau", than[0], than[1:] != ""))
            if any(c.isalnum() for c in g): o.add((kieu, cuc, "chu"))
            if g[:1].isspace() and g.strip()[:1] in ("*", "_"): o.add((kieu, cuc, "trang_roi_markup"))
            return o
        can_kn = {(k, "DUONG", "trang", w) for k in ("thang", "cong") for w in ("", " ", "\t", "\n")} | {
            (k, "DUONG", "markup", m, t) for k in ("thang", "cong") for m in ("*", "_", "**", "__") for t in ((False, True) if len(m) == 1 else (True,))} | {
            (k, "AM", "dau", c, t) for k in ("thang", "cong") for c in DAU_CAU for t in (False, True)} | {
            (k, "AM", x) for k in ("thang", "cong") for x in ("chu", "trang_roi_markup")} | {(k, "AM", "trang", "\n\n") for k in ("thang", "cong")}
        phu_kn = set().union(*(o_kn(ten, v[1]) for ten, v in ca.items() if ten.startswith(("kn_thang_", "kn_cong_"))))
        hong = [f"PHU_KHOANG_NOI: o chua co ca: {sorted(can_kn - phu_kn, key=str)}"] if can_kn - phu_kn else []
        # r19 (luot 14, F3): BANG CAP MARKUP — markup DONG giua cau va nhan phai la dao nguoc DUNG markup MO ngay truoc cau.
        # (mo, khoang noi, cuc); ky vong chi doc CUC. Loai o tinh LAI tu tep da sinh, khong doc bang.
        CAP_MARKUP = {"dung_sao": ("*", "*", "DUONG"), "dung_gach": ("_", "_ ", "DUONG"), "dung_sao_doi": ("**", "** ", "DUONG"),
                      "dung_gach_doi": ("__", "__", "DUONG"), "dung_tron": ("*_", "_* ", "DUONG"), "dung_tron_nguoc": ("_*", "*_", "DUONG"),
                      "dung_ba": ("***", "*** ", "DUONG"), "thieu_mo_sao": ("", "* ", "AM"), "thieu_mo_gach": ("", "_", "AM"),
                      "thieu_mo_doi": ("", "** ", "AM"), "khac_loai_sao_gach": ("*", "_ ", "AM"), "khac_loai_gach_sao": ("_", "*", "AM"),
                      "khac_loai_doi": ("**", "__ ", "AM"), "khac_loai_sai_thu_tu": ("*_", "*_ ", "AM"), "dai_ngan": ("**", "* ", "AM"),
                      "ngan_dai": ("*", "** ", "AM"), "gach_ngan_dai": ("_", "__", "AM"), "ba_hai": ("***", "** ", "AM"),
                      "mo_khong_dong_sao": ("*", " ", "AM"), "mo_khong_dong_doi": ("**", "", "AM"), "mo_khong_dong_gach": ("_", "\n", "AM")}
        # r19 (luot 14, F2 vong 8): BANG RANH GIOI code–van ban; {q} = cau trich. Ky vong viet tay tung dong.
        BIEN_CODE = {"code_xen": ("{q} `x` " + NL, "AM"), "code_lien_sau_cau": ("{q}`x` " + NL, "AM"),
                     "code_truoc_cau": ("`x` {q} " + NL, "DUONG"), "cau_trong_code": ("`{q}` " + NL, "KHONG"),
                     "nhan_trong_code": ("{q} `" + NL + "`", "AM"), "nhan_lien_sau_cau": ("{q}" + NL, "DUONG"),
                     "markup_roi_code_xen": ("*{q}* `x` " + NL, "AM"), "markup_mo_trong_code": ("`*`{q}* " + NL, "AM")}
        VEC = {"DUONG": (0, 0, 0, 0, 1), "AM": (0, 0, 0, 1, 0), "KHONG": (0, 0, 0, 0, 0)}
        for kieu, q in (("thang", Q8), ("cong", C8)):
            for lop, (mo, kn, cuc) in CAP_MARKUP.items(): ca[f"cm_{kieu}_{lop}"] = ("a.md", MO_DAU + mo + q + kn + NL + ".\n", None, VEC[cuc])
            for lop, (mau, cuc) in BIEN_CODE.items(): ca[f"bc_{kieu}_{lop}"] = ("a.md", MO_DAU + mau.format(q=q) + ".\n", None, VEC[cuc])
        def o_cm(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; mo = doc[len(MO_DAU):doc.index(q)]
            g = doc[doc.index(q) + len(q):doc.index(NL)]; dong = g[:len(g) - len(g.lstrip("*_"))]; cuc = "DUONG" if ca[ten][3][4] else "AM"
            loai = ("dung" if dong == mo[::-1] else "thieu_mo" if not mo else "mo_khong_dong" if not dong
                    else "khac_do_dai" if len(dong) != len(mo) else "khac_loai")
            return {(kieu, cuc, loai, "".join(sorted(set(mo + dong))), max(len(mo), len(dong)) > 1)}  # loai x ky tu x nhieu ky tu
        def o_bc(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; a, b = doc.index(q), doc.index(q) + len(q); c = doc.index(NL)
            o = {(kieu, "nhan_lien_sau_cau")} if c == b else set()
            for x in re.finditer(r"`[^`\n]*`", doc):
                o |= {(kieu, "code_truoc_cau")} if x.end() <= a else {(kieu, "cau_trong_code")} if x.start() < a and b <= x.end() else set()
                o |= {(kieu, "code_xen", b == x.start(), doc[b:x.start()].strip() != "")} if b <= x.start() and x.end() <= c else {(kieu, "nhan_trong_code")} if x.start() < c < x.end() else set()
            return o
        O_CM = {"DUONG": {"dung": (("*", 0), ("_", 0), ("*", 1), ("_", 1), ("*_", 1))},
                "AM": {"thieu_mo": (("*", 0), ("_", 0), ("*", 1)), "khac_loai": (("*_", 0), ("*_", 1)),
                       "khac_do_dai": (("*", 1), ("_", 1)), "mo_khong_dong": (("*", 0), ("*", 1), ("_", 0))}}
        can_cm = {(k, cuc, loai, ky, bool(nhieu)) for k in ("thang", "cong") for cuc, d in O_CM.items() for loai, os_ in d.items() for ky, nhieu in os_}
        can_bc = {(k, x) for k in ("thang", "cong") for x in ("cau_trong_code", "code_truoc_cau", "nhan_lien_sau_cau", "nhan_trong_code")} | {
            (k, "code_xen", lien, markup) for k in ("thang", "cong") for lien, markup in ((False, False), (True, False), (False, True))}
        phu_cm = set().union(*(o_cm(t_, v[1]) for t_, v in ca.items() if t_.startswith("cm_")))
        phu_bc = set().union(*(o_bc(t_, v[1]) for t_, v in ca.items() if t_.startswith("bc_")))
        hong += [f"PHU_CAP_MARKUP: o chua co ca: {sorted(can_cm - phu_cm, key=str)}"] if can_cm - phu_cm else []
        hong += [f"PHU_RANH_GIOI_CODE: o chua co ca: {sorted(can_bc - phu_bc)}"] if can_bc - phu_bc else []
        # r20 (luot 15, F2): ba TRUC moi, ky vong VIET TAY chi doc cuc/vecto, khong goi NHAN/MO/Q/kiem.
        # (1) VI TRI cau: dau khoi, dong thut le, sau newline ma dong truoc KET THUC bang markup, sau newline thuong.
        VI_TRI_CAU = {"dau_khoi": ("{mo}{q}{dong} " + NL + " theo r1.", "{c}"), "thut_le": ("  Theo r1: {mo}{q}{dong} " + NL + ".", "{c}"),
                      "sau_dong_ket_markup": ("Theo r1: *\n{mo}{q}{dong} " + NL + ".", "{c}"),
                      "sau_dong_thuong": ("Theo r1:\n{mo}{q}{dong} " + NL + ".", "{c}")}
        CAP_VT = {"khong": ("", "", "DUONG"), "sao": ("*", "*", "DUONG"), "sao_thieu_mo": ("", "*", "AM"), "sao_doi_lech": ("**", "*", "AM")}
        # (2) LAN XUAT HIEN: cung noi dung hai lan tren mot dong, khac nhan hoac khac cap; vecto viet tay (VI_PHAM, CO_NHAN).
        LAN = {"dung_roi_thieu_mo": ("*{q}* " + NL + "; {q}* " + NL, (1, 1)), "thieu_mo_roi_dung": ("{q}* " + NL + "; *{q}* " + NL, (1, 1)),
               "co_nhan_roi_khong": ("{q} " + NL + "; {q} khong nhan", (1, 1)), "khong_roi_co_nhan": ("{q} khong nhan; {q} " + NL, (1, 1)),
               "nhan_dung_roi_sai": ("{q} " + NL + "; {q} " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7), (1, 1)),
               "ca_hai_dung_khac_cap": ("*{q}* " + NL + "; **{q}** " + NL, (0, 2))}
        # (3) DO DAI markup >= 4 (vuot moi mau cu): cap dung va lech do dai.
        DO_DAI = {"bon_bon": ("****", "****", "DUONG"), "nam_nam": ("*****", "*****", "DUONG"), "gach_bon": ("____", "____", "DUONG"),
                  "bon_ba": ("****", "***", "AM"), "ba_bon": ("***", "****", "AM"), "bon_nam": ("****", "*****", "AM")}
        for kieu, q in (("thang", Q8), ("cong", C8)):
            for vt, (mau, _c) in VI_TRI_CAU.items():
                for cap, (mo, dong, cuc) in CAP_VT.items():
                    ca[f"vt_{kieu}_{vt}_{cap}"] = ("a.md", mau.format(mo=mo, q=q, dong=dong) + "\n", None, VEC[cuc])
            for ten, (mau, (vp, cn)) in LAN.items(): ca[f"lan_{kieu}_{ten}"] = ("a.md", "Theo r1: " + mau.format(q=q) + ".\n", None, (0, 0, 0, vp, cn))
            for ten, (mo, dong, cuc) in DO_DAI.items(): ca[f"dd_{kieu}_{ten}"] = ("a.md", "Theo r1: " + mo + q + dong + " " + NL + ".\n", None, VEC[cuc])
        # KIEM PHU BANG MAY tren tep DA SINH (tinh lai tu noi dung, khong doc bang).
        def o_r20(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; a = doc.index(q); dong_dau = doc[:a].rsplit("\n", 1)[-1]
            o = set()
            if ten.startswith("vt_"):
                truoc = doc[:a - len(dong_dau)]
                chi_markup = dong_dau.strip("*_") == ""
                vt = ("dau_khoi" if not truoc and chi_markup else "thut_le" if dong_dau[:1] == " " else "sau_dong_ket_markup"
                      if truoc and chi_markup and truoc.rstrip("\n")[-1:] in ("*", "_") else "sau_dong_thuong" if truoc and chi_markup else "giua_dong")
                o.add((kieu, "vi_tri", vt, "DUONG" if ca[ten][3][4] else "AM"))
            if ten.startswith("lan_") and doc.count(q) >= 2:  # moi lan: (markup truoc, markup sau, nhan hop le ngay sau?)
                def lan(i):
                    t = doc[:i]; mo = t[len(t.rstrip("*_")):]; d = doc[i + len(q):]; dong = d[:len(d) - len(d.lstrip("*_"))]
                    return mo, dong, dong == mo[::-1] and d[len(dong):].lstrip(" ").startswith(NL)
                l1, l2 = lan(a), lan(doc.index(q, a + 1))
                o.add((kieu, "lan", l1[2], l2[2], "cap" if l1[:2] != l2[:2] else "nhan"))
            if ten.startswith("dd_"):
                mo = dong_dau[len(dong_dau.rstrip("*_")):] if dong_dau.rstrip("*_") != dong_dau else ""
                d = doc[a + len(q):]; dong = d[:len(d) - len(d.lstrip("*_"))]
                o.add((kieu, "do_dai", max(len(mo), len(dong)) >= 4, len(mo) == len(dong)))
            return o
        can_r20 = {(k, "vi_tri", v, c) for k in ("thang", "cong") for v in ("dau_khoi", "thut_le", "sau_dong_ket_markup", "sau_dong_thuong")
                   for c in ("DUONG", "AM")} | {(k, "lan", t1, t2, x) for k in ("thang", "cong") for t1, t2, x in ((True, False, "cap"), (False, True, "cap"), (True, False, "nhan"),
                                                                         (False, True, "nhan"), (True, True, "cap"))} | {
                   (k, "do_dai", True, e) for k in ("thang", "cong") for e in (True, False)}
        phu_r20 = set().union(*(o_r20(t_, v[1]) for t_, v in ca.items() if t_.startswith(("vt_", "lan_", "dd_"))))
        hong += [f"PHU_R20: o chua co ca: {sorted(can_r20 - phu_r20, key=str)}"] if can_r20 - phu_r20 else []
        for ten, (tep, doc, ham, mong) in ca.items():
            p = Path(t) / ten / tep; p.parent.mkdir(); p.write_text(doc, encoding="utf-8")
            d = kiem(t, "r{n}.md", p, ham)
            thuc = (d["DUNG"], d["LECH"], d["KHONG_DO_DUOC"], d["VI_PHAM"], d["CO_NHAN"])
            if thuc != mong: hong.append(f"{ten}: mong {mong}, thuc {thuc}")
        # HOP DONG CLI — bang co tham quyen o dac ta r15 §0.14; cac ca SINH tu bang (to hop), khong liet ke tay.
        # Moi tep mau mang VEC TO ky vong viet tay (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN); ky vong cua mot lan chay
        # nhieu tep = TONG tung phan tu; rc ky vong = 1 khi LECH + KHONG_DO_DUOC + VI_PHAM > 0. Oracle chi cong va so sanh,
        # khong goi `kiem`/`main`/regex nao cua cong. Nguon CLI dung MAU TEN RIENG (`spec-r{n}.txt`) de `--mau` co rang.
        import itertools, subprocess as _sp
        nc = Path(t) / "nguon_cli"; nc.mkdir()
        (nc / "spec-r3.txt").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        dc = Path(t) / "cli"; dc.mkdir()
        TEP_CLI = {
            "sach.md": ("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", (1, 0, 0, 0, 0)),
            "lech.md": ("Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "lech2.md": ("Theo r3 " + CT0("r3:11 #00000000|so 11 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "thieu.md": ("Theo r9 " + CT0("r9:1 #00000000|khong co tep nao") + ".\n", (0, 0, 1, 0, 0)),
            "vipham.md": ("Theo r1: " + Q8 + ".\n", (0, 0, 0, 1, 0)),
            "nhan.md": ("Theo r1: " + Q8 + " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
            "nhan_gach.md": ("Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
        }
        for ten, (noi, _v) in TEP_CLI.items(): (dc / ten).write_text(noi, encoding="utf-8")
        COT = ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")
        CO = ["--nguon", str(nc), "--mau", "spec-r{n}.txt"]
        VI_TRI = {"co_truoc": lambda co, tep: co + tep, "co_sau": lambda co, tep: tep + co,
                  "co_xen": lambda co, tep: tep[:1] + co + tep[1:]}
        ds_tep = sorted(TEP_CLI)
        to_hop = [(x,) for x in ds_tep] + list(itertools.permutations(ds_tep, 2)) + [
            ("lech.md", "lech2.md", "vipham.md"), ("sach.md", "nhan.md", "nhan_gach.md"), ("thieu.md", "sach.md", "thieu.md"),
            tuple(ds_tep)]
        cli = {}
        for so, bo in enumerate(to_hop):
            vt = list(VI_TRI)[so % 3] if len(bo) > 1 else None
            for v in ([vt] if vt else list(VI_TRI)):
                mong = tuple(sum(TEP_CLI[x][1][c] for x in bo) for c in range(5))
                cli[f"cli_{v}_{'+'.join(bo)}"] = (VI_TRI[v](CO, [str(dc / x) for x in bo]), int(sum(mong[1:4]) > 0), mong)
        # --ham: tep 5 ham, XAU = {a, c, e}; ky vong VI_PHAM = so ten trong danh sach thuoc XAU (ten la khong tinh).
        XAU = {"a", "c", "e"}
        (dc / "h.py").write_text("".join(f"def {n}():\n    " + Q2 * 3 + f"Ham {n} nhac r1 " + (Q8 + " khong nhan" if n in XAU else "va khong trich gi")
                                 + ", du dai de qua nguong bon muoi.\n    " + Q2 * 3 + "\n\n\n" for n in "abcde"), encoding="utf-8")
        # r16 (luot 11): vi tri TUNG co la mot truc RIENG, tach khoi noi dung danh sach ham — moi danh sach x `--ham`
        # truoc / sau chinh tep; `--nguon`/`--mau` luan phien truoc / sau.
        for so, ds_ham in enumerate(("a", "b", "c", "e", "a,b", "b,c", "d,e", "b,c,d", "d,c,b", "b,zz,d", "zz", "a,b,c,d,e", "b,d")):
            vi = len(set(ds_ham.split(",")) & XAU)
            for vt_ham, tep in (("ham_truoc", ["--ham", ds_ham, str(dc / "h.py")]), ("ham_sau", [str(dc / "h.py"), "--ham", ds_ham])):
                cli[f"cli_{vt_ham}_{ds_ham}"] = ((CO + tep) if so % 2 == 0 else (tep + CO), int(vi > 0), (0, 0, 0, vi, 0))
        cli["cli_khong_ham_h"] = (CO + [str(dc / "h.py")], 1, (0, 0, 0, 3, 0))
        # KIEM PHU BANG MAY tren argv DA SINH (khong tren y dinh): moi o cua bang §0.14 phai co >= 1 ca. Vi tri cua moi co
        # tinh theo chi so trong argv so voi cac TEP (doi so khong phai co, khong phai gia tri cua co).
        def o_cua(doi):
            tep_i, co_i, i = [], {}, 0
            while i < len(doi):
                if doi[i] in ("--nguon", "--mau", "--ham"): co_i[doi[i]] = i; i += 2
                else: tep_i.append(i); i += 1
            vt = lambda i: "truoc" if i < tep_i[0] else "sau" if i > tep_i[-1] else "xen"
            return {("so_tep", len(tep_i))} | {(f"vi_tri{c}", vt(i)) for c, i in co_i.items()}
        can = ({("so_tep", n) for n in (1, 2, 3, 7)} | {(f"vi_tri{c}", v) for c in ("--nguon", "--mau") for v in ("truoc", "sau", "xen")}
               | {("vi_tri--ham", v) for v in ("truoc", "sau")})
        co_phu = set().union(*(o_cua(doi) for doi, _r, _m in cli.values()))
        if can - co_phu: hong.append(f"PHU_BANG: o chua co ca: {sorted(can - co_phu)}")
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", *doi], capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[0][5:]) if len(tong) == 1 else {}
            thuc = (r.returncode, len(tong), tuple(d.get(k) for k in COT))
            if thuc != (rc_mong, 1, mong): hong.append(f"{ten}: mong {(rc_mong, 1, mong)}, thuc {thuc}")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}", f"(truc tiep {len(ca)}, CLI {len(cli)})")
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

## Phụ lục O — cổng CON TRỎ v12: bảng biên độc lập (EOF, tiêu đề, ngưỡng `.py`, loại khoảng trắng, độ dài markup 1..8, khoảng trắng biên), §0.20 (MỚI ở r21, nguyên văn)

Cùng cách chạy như Phụ lục E. `tu-kiem` in: `TU_KIEM DAT 565/565 (truc tiep 471, CLI 94)` (số lấy từ lần chạy khi dựng đặc tả, không gõ tay). So với Phụ lục N chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `483caa7e6e0b0ae93244880a4a20f5a6201342144906ebce4ba7a6faf2a467d1`.

```python
"""Con tro nguon cho dac ta R378 (r10 #574) — thay moi loi trich VIET TAY cua revision khac.

  CON TRO   ⟦rN:L #h|manh⟧ hoac ⟦rN:L-M #h|manh⟧ : dong L (den M) cua dac ta revision N; h = 8 hex dau cua
            sha256 noi dung cac dong ay sau chuan hoa (bo khoang trang dau/cuoi moi dong, gop khoang trang). Tro sai
            dong => h lech => DO. `manh` (BAT BUOC tu r11, >= 6 ky tu) la cum chu ma cau dan con tro dang noi toi; no
            phai NAM TRONG cac dong duoc tro (so sau khi bo `*` va dau backtick, gop khoang trang) — tro dung bam ma
            sai dong CAN TRO (F1d #574 luot 6: r3:322 thay vi 323-324) => DO. Sinh bang lenh `sinh`, KHONG go tay.
  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac (markup giua cau va nhan chi duoc la markup DONG, dao nguoc dung
            markup MO ngay truoc cau; tu r19): chuoi ay KHONG phai loi cua mot revision (K thuoc
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
NHAN = re.compile(r"([*_]*)\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
MO = re.compile(r"[*_]*\Z")  # markup MO ngay truoc dau ngoac mo cua cau (r19)
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
            n = NHAN.match(k, m.end())  # r19: markup DONG giua cau va nhan phai la dao nguoc DUNG markup MO ngay truoc cau
            if n and n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1]: dem["CO_NHAN"] += 1; continue
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
            # r17 (luot 12): nhan DUNG / SAI / THIEU tron trong CUNG khoi, moi hoan vi thu tu — nhan phai dung NGAY sau cau
            # trich cua no; mot nhan hop le o CHO KHAC trong khoi khong duoc cuu mot cau trich thieu/sai nhan.
            **{ten: ("a.md", "Theo r1: " + "; ".join(Q2 + chu + Q2 + ({"dung": " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7),
                     "sai": " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7), "thieu": ""}[loai]) for chu, loai in zip(("abcdefgh", "ijklmnop", "qrstuvwx"), thu_tu)) + ".\n",
                     None, (0, 0, 0, sum(x != "dung" for x in thu_tu), sum(x == "dung" for x in thu_tu)))
               for ten, thu_tu in (("nhan_xau_truoc_nhan_dung", ("sai", "dung")), ("nhan_dung_truoc_nhan_xau", ("dung", "sai")),
                                   ("nhan_thieu_truoc_nhan_dung", ("thieu", "dung")), ("nhan_dung_truoc_nhan_thieu", ("dung", "thieu")),
                                   ("nhan_xau_thieu_dung", ("sai", "thieu", "dung")), ("nhan_thieu_xau_dung", ("thieu", "sai", "dung")),
                                   ("nhan_dung_xau_thieu", ("dung", "sai", "thieu")))},
            "nhan_sau_gach_duoi": ("a.md", "Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:doctrine" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "nhan_sau_markup_dam": ("a.md", "Theo r1: **" + Q8 + "** " + chr(0x27E6) + "nguon:verdict" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "ngoac_cong_vat_dong": ("a.md", "Theo r1: “abcd\nefgh”.\n", None, (0, 0, 0, 1, 0)),
            "rv_sau_gach_noi": ("a.md", "Theo ma-r1: " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "manh_5_am": ("a.md", "Theo r1 " + CT0("r1:1 #2bf318fb|ong m") + ".\n", None, (0, 0, 0, 1, 0)),
        })
        # r18 (luot 13, F2): BANG LOP KHOANG NOI cau-nhan, co tham quyen o dac ta r18 §0.17. Lop: (markup MO truoc cau,
        # khoang noi giua dau ngoac DONG va nhan, cuc). Ca SINH tu bang x hai kieu ngoac; ky vong chi doc CUC — DUONG
        # (0,0,0,0,1), AM (0,0,0,1,0) — khong qua regex nao cua cong. Markup phai DONG ngay sau cau roi moi toi khoang trang.
        DAU_CAU, NL = ";,.:!?", chr(0x27E6) + "nguon:ma" + chr(0x27E7)
        KHOANG_NOI = {"rong": ("", "", "DUONG"), "cach": ("", " ", "DUONG"), "cach_nhieu": ("", "   ", "DUONG"),
                      "tab": ("", "\t", "DUONG"), "xuong_dong": ("", "\n", "DUONG"), "cach_xuong_dong": ("", " \n  ", "DUONG"),
                      "sao": ("*", "*", "DUONG"), "sao_cach": ("*", "* ", "DUONG"), "gach": ("_", "_", "DUONG"),
                      "gach_cach": ("_", "_ ", "DUONG"), "sao_doi": ("**", "**", "DUONG"), "sao_doi_cach": ("**", "** ", "DUONG"),
                      "gach_doi_xuong_dong": ("__", "__\n", "DUONG"),
                      **{f"dau{i}": ("", c, "AM") for i, c in enumerate(DAU_CAU)},
                      **{f"dau{i}_cach": ("", c + " ", "AM") for i, c in enumerate(DAU_CAU)},
                      "sao_roi_dau": ("*", "*; ", "AM"), "cach_roi_dau": ("", " , ", "AM"), "cach_roi_sao": ("", " *", "AM"),
                      "chu": ("", " va ", "AM"), "chu_dinh": ("", "x ", "AM"), "noi_dung_xen": ("", " (ghi chu) ", "AM"),
                      "ngoac_dong": ("", ") ", "AM"), "gach_ngang": ("", " — ", "AM"), "doan_moi": ("", "\n\n", "AM")}
        MO_DAU = "Theo r1: "
        for lop, (mo, kn, cuc) in KHOANG_NOI.items():
            for kieu, q in (("thang", Q8), ("cong", C8)):
                ca[f"kn_{kieu}_{lop}"] = ("a.md", MO_DAU + mo + q + kn + NL + ".\n", None, (0, 0, 0, 0, 1) if cuc == "DUONG" else (0, 0, 0, 1, 0))
        # doi chung viet tay: nhan TRUOC cau; hai nhan hop le lien tiep; nhan sai roi nhan dung sau CUNG mot cau
        ca.update({"kn_nhan_truoc_cau": ("a.md", MO_DAU + NL + " " + Q8 + ".\n", None, (0, 0, 0, 1, 0)),
                   "kn_hai_nhan_lien_tiep": ("a.md", MO_DAU + Q8 + " " + NL + " " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
                   "kn_nhan_sai_roi_dung": ("a.md", MO_DAU + Q8 + " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7) + " " + NL + ".\n", None, (0, 0, 0, 1, 0))})
        # KIEM PHU BANG MAY tren tep DA SINH: tach khoang noi khoi chinh noi dung tep (khong doc lai bang), roi doi moi o.
        def o_kn(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; g = doc[doc.index(q) + len(q):doc.index(NL)]
            cuc = "DUONG" if ca[ten][3][4] else "AM"; than = g.lstrip("*_"); dau = g[:len(g) - len(than)]; o = set()
            if dau: o.add((kieu, cuc, "markup", dau, than != ""))
            if not g.strip(): o.add((kieu, cuc, "trang", g))
            if than and than[0] in DAU_CAU: o.add((kieu, cuc, "dau", than[0], than[1:] != ""))
            if any(c.isalnum() for c in g): o.add((kieu, cuc, "chu"))
            if g[:1].isspace() and g.strip()[:1] in ("*", "_"): o.add((kieu, cuc, "trang_roi_markup"))
            return o
        can_kn = {(k, "DUONG", "trang", w) for k in ("thang", "cong") for w in ("", " ", "\t", "\n")} | {
            (k, "DUONG", "markup", m, t) for k in ("thang", "cong") for m in ("*", "_", "**", "__") for t in ((False, True) if len(m) == 1 else (True,))} | {
            (k, "AM", "dau", c, t) for k in ("thang", "cong") for c in DAU_CAU for t in (False, True)} | {
            (k, "AM", x) for k in ("thang", "cong") for x in ("chu", "trang_roi_markup")} | {(k, "AM", "trang", "\n\n") for k in ("thang", "cong")}
        phu_kn = set().union(*(o_kn(ten, v[1]) for ten, v in ca.items() if ten.startswith(("kn_thang_", "kn_cong_"))))
        hong = [f"PHU_KHOANG_NOI: o chua co ca: {sorted(can_kn - phu_kn, key=str)}"] if can_kn - phu_kn else []
        # r19 (luot 14, F3): BANG CAP MARKUP — markup DONG giua cau va nhan phai la dao nguoc DUNG markup MO ngay truoc cau.
        # (mo, khoang noi, cuc); ky vong chi doc CUC. Loai o tinh LAI tu tep da sinh, khong doc bang.
        CAP_MARKUP = {"dung_sao": ("*", "*", "DUONG"), "dung_gach": ("_", "_ ", "DUONG"), "dung_sao_doi": ("**", "** ", "DUONG"),
                      "dung_gach_doi": ("__", "__", "DUONG"), "dung_tron": ("*_", "_* ", "DUONG"), "dung_tron_nguoc": ("_*", "*_", "DUONG"),
                      "dung_ba": ("***", "*** ", "DUONG"), "thieu_mo_sao": ("", "* ", "AM"), "thieu_mo_gach": ("", "_", "AM"),
                      "thieu_mo_doi": ("", "** ", "AM"), "khac_loai_sao_gach": ("*", "_ ", "AM"), "khac_loai_gach_sao": ("_", "*", "AM"),
                      "khac_loai_doi": ("**", "__ ", "AM"), "khac_loai_sai_thu_tu": ("*_", "*_ ", "AM"), "dai_ngan": ("**", "* ", "AM"),
                      "ngan_dai": ("*", "** ", "AM"), "gach_ngan_dai": ("_", "__", "AM"), "ba_hai": ("***", "** ", "AM"),
                      "mo_khong_dong_sao": ("*", " ", "AM"), "mo_khong_dong_doi": ("**", "", "AM"), "mo_khong_dong_gach": ("_", "\n", "AM")}
        # r19 (luot 14, F2 vong 8): BANG RANH GIOI code–van ban; {q} = cau trich. Ky vong viet tay tung dong.
        BIEN_CODE = {"code_xen": ("{q} `x` " + NL, "AM"), "code_lien_sau_cau": ("{q}`x` " + NL, "AM"),
                     "code_truoc_cau": ("`x` {q} " + NL, "DUONG"), "cau_trong_code": ("`{q}` " + NL, "KHONG"),
                     "nhan_trong_code": ("{q} `" + NL + "`", "AM"), "nhan_lien_sau_cau": ("{q}" + NL, "DUONG"),
                     "markup_roi_code_xen": ("*{q}* `x` " + NL, "AM"), "markup_mo_trong_code": ("`*`{q}* " + NL, "AM")}
        VEC = {"DUONG": (0, 0, 0, 0, 1), "AM": (0, 0, 0, 1, 0), "KHONG": (0, 0, 0, 0, 0)}
        for kieu, q in (("thang", Q8), ("cong", C8)):
            for lop, (mo, kn, cuc) in CAP_MARKUP.items(): ca[f"cm_{kieu}_{lop}"] = ("a.md", MO_DAU + mo + q + kn + NL + ".\n", None, VEC[cuc])
            for lop, (mau, cuc) in BIEN_CODE.items(): ca[f"bc_{kieu}_{lop}"] = ("a.md", MO_DAU + mau.format(q=q) + ".\n", None, VEC[cuc])
        def o_cm(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; mo = doc[len(MO_DAU):doc.index(q)]
            g = doc[doc.index(q) + len(q):doc.index(NL)]; dong = g[:len(g) - len(g.lstrip("*_"))]; cuc = "DUONG" if ca[ten][3][4] else "AM"
            loai = ("dung" if dong == mo[::-1] else "thieu_mo" if not mo else "mo_khong_dong" if not dong
                    else "khac_do_dai" if len(dong) != len(mo) else "khac_loai")
            return {(kieu, cuc, loai, "".join(sorted(set(mo + dong))), max(len(mo), len(dong)) > 1)}  # loai x ky tu x nhieu ky tu
        def o_bc(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; a, b = doc.index(q), doc.index(q) + len(q); c = doc.index(NL)
            o = {(kieu, "nhan_lien_sau_cau")} if c == b else set()
            for x in re.finditer(r"`[^`\n]*`", doc):
                o |= {(kieu, "code_truoc_cau")} if x.end() <= a else {(kieu, "cau_trong_code")} if x.start() < a and b <= x.end() else set()
                o |= {(kieu, "code_xen", b == x.start(), doc[b:x.start()].strip() != "")} if b <= x.start() and x.end() <= c else {(kieu, "nhan_trong_code")} if x.start() < c < x.end() else set()
            return o
        O_CM = {"DUONG": {"dung": (("*", 0), ("_", 0), ("*", 1), ("_", 1), ("*_", 1))},
                "AM": {"thieu_mo": (("*", 0), ("_", 0), ("*", 1)), "khac_loai": (("*_", 0), ("*_", 1)),
                       "khac_do_dai": (("*", 1), ("_", 1)), "mo_khong_dong": (("*", 0), ("*", 1), ("_", 0))}}
        can_cm = {(k, cuc, loai, ky, bool(nhieu)) for k in ("thang", "cong") for cuc, d in O_CM.items() for loai, os_ in d.items() for ky, nhieu in os_}
        can_bc = {(k, x) for k in ("thang", "cong") for x in ("cau_trong_code", "code_truoc_cau", "nhan_lien_sau_cau", "nhan_trong_code")} | {
            (k, "code_xen", lien, markup) for k in ("thang", "cong") for lien, markup in ((False, False), (True, False), (False, True))}
        phu_cm = set().union(*(o_cm(t_, v[1]) for t_, v in ca.items() if t_.startswith("cm_")))
        phu_bc = set().union(*(o_bc(t_, v[1]) for t_, v in ca.items() if t_.startswith("bc_")))
        hong += [f"PHU_CAP_MARKUP: o chua co ca: {sorted(can_cm - phu_cm, key=str)}"] if can_cm - phu_cm else []
        hong += [f"PHU_RANH_GIOI_CODE: o chua co ca: {sorted(can_bc - phu_bc)}"] if can_bc - phu_bc else []
        # r20 (luot 15, F2): ba TRUC moi, ky vong VIET TAY chi doc cuc/vecto, khong goi NHAN/MO/Q/kiem.
        # (1) VI TRI cau: dau khoi, dong thut le, sau newline ma dong truoc KET THUC bang markup, sau newline thuong.
        VI_TRI_CAU = {"dau_khoi": ("{mo}{q}{dong} " + NL + " theo r1.", "{c}"), "thut_le": ("  Theo r1: {mo}{q}{dong} " + NL + ".", "{c}"),
                      "sau_dong_ket_markup": ("Theo r1: *\n{mo}{q}{dong} " + NL + ".", "{c}"),
                      "sau_dong_thuong": ("Theo r1:\n{mo}{q}{dong} " + NL + ".", "{c}")}
        CAP_VT = {"khong": ("", "", "DUONG"), "sao": ("*", "*", "DUONG"), "sao_thieu_mo": ("", "*", "AM"), "sao_doi_lech": ("**", "*", "AM")}
        # (2) LAN XUAT HIEN: cung noi dung hai lan tren mot dong, khac nhan hoac khac cap; vecto viet tay (VI_PHAM, CO_NHAN).
        LAN = {"dung_roi_thieu_mo": ("*{q}* " + NL + "; {q}* " + NL, (1, 1)), "thieu_mo_roi_dung": ("{q}* " + NL + "; *{q}* " + NL, (1, 1)),
               "co_nhan_roi_khong": ("{q} " + NL + "; {q} khong nhan", (1, 1)), "khong_roi_co_nhan": ("{q} khong nhan; {q} " + NL, (1, 1)),
               "nhan_dung_roi_sai": ("{q} " + NL + "; {q} " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7), (1, 1)),
               "ca_hai_dung_khac_cap": ("*{q}* " + NL + "; **{q}** " + NL, (0, 2))}
        # (3) DO DAI markup >= 4 (vuot moi mau cu): cap dung va lech do dai.
        DO_DAI = {"bon_bon": ("****", "****", "DUONG"), "nam_nam": ("*****", "*****", "DUONG"), "gach_bon": ("____", "____", "DUONG"),
                  "bon_ba": ("****", "***", "AM"), "ba_bon": ("***", "****", "AM"), "bon_nam": ("****", "*****", "AM")}
        for kieu, q in (("thang", Q8), ("cong", C8)):
            for vt, (mau, _c) in VI_TRI_CAU.items():
                for cap, (mo, dong, cuc) in CAP_VT.items():
                    ca[f"vt_{kieu}_{vt}_{cap}"] = ("a.md", mau.format(mo=mo, q=q, dong=dong) + "\n", None, VEC[cuc])
            for ten, (mau, (vp, cn)) in LAN.items(): ca[f"lan_{kieu}_{ten}"] = ("a.md", "Theo r1: " + mau.format(q=q) + ".\n", None, (0, 0, 0, vp, cn))
            for ten, (mo, dong, cuc) in DO_DAI.items(): ca[f"dd_{kieu}_{ten}"] = ("a.md", "Theo r1: " + mo + q + dong + " " + NL + ".\n", None, VEC[cuc])
        # KIEM PHU BANG MAY tren tep DA SINH (tinh lai tu noi dung, khong doc bang).
        def o_r20(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; a = doc.index(q); dong_dau = doc[:a].rsplit("\n", 1)[-1]
            o = set()
            if ten.startswith("vt_"):
                truoc = doc[:a - len(dong_dau)]
                chi_markup = dong_dau.strip("*_") == ""
                vt = ("dau_khoi" if not truoc and chi_markup else "thut_le" if dong_dau[:1] == " " else "sau_dong_ket_markup"
                      if truoc and chi_markup and truoc.rstrip("\n")[-1:] in ("*", "_") else "sau_dong_thuong" if truoc and chi_markup else "giua_dong")
                o.add((kieu, "vi_tri", vt, "DUONG" if ca[ten][3][4] else "AM"))
            if ten.startswith("lan_") and doc.count(q) >= 2:  # moi lan: (markup truoc, markup sau, nhan hop le ngay sau?)
                def lan(i):
                    t = doc[:i]; mo = t[len(t.rstrip("*_")):]; d = doc[i + len(q):]; dong = d[:len(d) - len(d.lstrip("*_"))]
                    return mo, dong, dong == mo[::-1] and d[len(dong):].lstrip(" ").startswith(NL)
                l1, l2 = lan(a), lan(doc.index(q, a + 1))
                o.add((kieu, "lan", l1[2], l2[2], "cap" if l1[:2] != l2[:2] else "nhan"))
            if ten.startswith("dd_"):
                mo = dong_dau[len(dong_dau.rstrip("*_")):] if dong_dau.rstrip("*_") != dong_dau else ""
                d = doc[a + len(q):]; dong = d[:len(d) - len(d.lstrip("*_"))]
                o.add((kieu, "do_dai", max(len(mo), len(dong)) >= 4, len(mo) == len(dong)))
            return o
        can_r20 = {(k, "vi_tri", v, c) for k in ("thang", "cong") for v in ("dau_khoi", "thut_le", "sau_dong_ket_markup", "sau_dong_thuong")
                   for c in ("DUONG", "AM")} | {(k, "lan", t1, t2, x) for k in ("thang", "cong") for t1, t2, x in ((True, False, "cap"), (False, True, "cap"), (True, False, "nhan"),
                                                                         (False, True, "nhan"), (True, True, "cap"))} | {
                   (k, "do_dai", True, e) for k in ("thang", "cong") for e in (True, False)}
        phu_r20 = set().union(*(o_r20(t_, v[1]) for t_, v in ca.items() if t_.startswith(("vt_", "lan_", "dd_"))))
        hong += [f"PHU_R20: o chua co ca: {sorted(can_r20 - phu_r20, key=str)}"] if can_r20 - phu_r20 else []
        # r21 (luot 16, F2): BANG BIEN DOC LAP cho moi ham co hanh vi ranh gioi — khoi_md (EOF, chuyen tieu de), khoi_py
        # (nguong 40), chuan/bo_dau (khoang trang bien, nhieu dong, loai khoang trang), NHAN/MO (do dai markup 1..8 la
        # THUOC TINH), loai khoang trang giua cau va nhan. Ky vong VIET TAY; bam la LITERAL tinh doc lap (sha256 cua chuoi
        # chuan hoa viet tay), khong goi chuan/bam/sinh/kiem de sinh dap an.
        (Path(t) / "r41.md").write_text("  dong hai co noi dung  \n", encoding="utf-8")
        (Path(t) / "r42.md").write_text(" dong  mot\t\n" + chr(0xA0) + "dong hai co noi dung  \n", encoding="utf-8")
        (Path(t) / "r43.md").write_text("\tdong  ba" + chr(0xA0) + "co   noi dung\n", encoding="utf-8")
        V = lambda d=0, l=0, k=0, v=0, c=0: (d, l, k, v, c)
        for kieu, q in (("thang", Q8), ("cong", C8)):
            # (a) khoi_md — EOF co/khong newline, khoi cuoi, bang cuoi, nhieu khoi.
            for ten, (doc, mong) in {"mot_khong_nl": ("Theo r1: {q}.", V(v=1)), "mot_co_nl": ("Theo r1: {q}.\n", V(v=1)),
                                     "mot_nhieu_nl": ("Theo r1: {q}.\n\n\n", V(v=1)), "sau_khoi_khong_nl": ("Mo dau.\n\nTheo r1: {q}.", V(v=1)),
                                     "bang_khong_nl": ("| a | b |\n| r1 | {q} |", V(v=1)), "bang_co_nl": ("| a | b |\n| r1 | {q} |\n", V(v=1)),
                                     "nhan_khong_nl": ("Theo r1: {q} " + NL, V(c=1)), "hai_khoi_khong_nl": ("Theo r1: {q}.\n\nTheo r1: {q}.", V(v=2)),
                                     "khong_token_khong_nl": ("Mo dau {q}.", V())}.items():
                ca[f"b21eof_{kieu}_{ten}"] = ("a.md", doc.format(q=q), None, mong)
            # (b) khoi_md — chuyen TIEU DE co/khong token, ca hai chieu, lien/cach dong, muc 1..7, thieu khoang trang.
            for ten, (doc, mong) in {"co_roi_khong": ("## Nhan xet r1\n\nVan ban khong trich.\n\n## Chu de khac\n\n{q}.\n", V()),
                                     "co_roi_khong_lien": ("## Nhan xet r1\n## Chu de khac\n{q}.\n", V()),
                                     "khong_roi_co": ("## Chu de khac\n\n## Nhan xet r1\n\n{q}.\n", V(v=1)),
                                     "khong_roi_co_lien": ("## Chu de khac\n## Nhan xet r1\n{q}.\n", V(v=1)),
                                     "co_roi_co": ("## Nhan xet r1\n\n## Nhan xet r2\n\n{q}.\n", V(v=1)),
                                     "co_lien": ("## Nhan xet r1\n{q}.\n", V(v=1)), "co_cach": ("## Nhan xet r1\n\n{q}.\n", V(v=1)),
                                     "muc1": ("# Nhan xet r1\n\n{q}.\n", V(v=1)), "muc6": ("###### Nhan xet r1\n\n{q}.\n", V(v=1)),
                                     "muc7_khong_la_tieu_de": ("####### Nhan xet r1\n\n{q}.\n", V()),
                                     "thieu_cach_khong_la_tieu_de": ("##Nhan xet r1\n\n{q}.\n", V()),
                                     "co_roi_rao": ("## Nhan xet r1\n\n```\nx\n```\n\n{q}.\n", V(v=1))}.items():
                ca[f"b21td_{kieu}_{ten}"] = ("a.md", doc.format(q=q), None, mong)
            # (c) khoi_py — chuoi duoi / DUNG / tren nguong 40, va chuoi ngan; ky vong theo DO DAI viet tay.
            for n_ in (14, 39, 40, 41, 60):
                s_ = ("r1: " + q + " " + "x" * 60)[:n_] if n_ > 14 else "r1: " + q
                assert len(s_) == n_
                ca[f"b21py_{kieu}_{n_}"] = ("a.py", "X = " + repr(s_) + "\n", None, V(v=1) if n_ in (41, 60) else V())
            # (d) loai KHOANG TRANG giua dau ngoac dong va nhan: moi ky tu `str.isspace` -> DUONG; ky tu vo hinh khong
            # phai khoang trang -> AM.
            for ten, g in {"space": " ", "tab": "\t", "lf": "\n", "vt": "\x0b", "ff": "\x0c", "cr": "\r", "nbsp": chr(0xA0),
                           "nbsp_space": chr(0xA0) + " ", "em": chr(0x2003), "ideo": chr(0x3000), "ogham": chr(0x1680),
                           "hep": chr(0x202F), "ls": chr(0x2028), "fs": chr(0x1C)}.items():
                ca[f"b21kt_{kieu}_{ten}"] = ("a.md", "Theo r1: " + q + g + NL + ".\n", None, V(c=1))
            for ten, g in {"zwsp": chr(0x200B), "shy": chr(0xAD), "wj": chr(0x2060)}.items():
                ca[f"b21kt_{kieu}_{ten}"] = ("a.md", "Theo r1: " + q + g + NL + ".\n", None, V(v=1))
            # (e) NHAN/MO — do dai markup la THUOC TINH 1..8: cap dung (L,L) DUONG; lech (L,L+1), (L+1,L) AM; tron nguoc DUONG,
            # tron khong dao AM.
            for L_ in range(1, 9):
                for ch in "*_":
                    ca[f"b21md_{kieu}_{ch == '*' and 'sao' or 'gach'}_{L_}_{L_}"] = ("a.md", "Theo r1: " + ch * L_ + q + ch * L_ + " " + NL + ".\n", None, V(c=1))
                    ca[f"b21md_{kieu}_{ch == '*' and 'sao' or 'gach'}_{L_}_{L_ + 1}"] = ("a.md", "Theo r1: " + ch * L_ + q + ch * (L_ + 1) + " " + NL + ".\n", None, V(v=1))
                    ca[f"b21md_{kieu}_{ch == '*' and 'sao' or 'gach'}_{L_ + 1}_{L_}"] = ("a.md", "Theo r1: " + ch * (L_ + 1) + q + ch * L_ + " " + NL + ".\n", None, V(v=1))
                if L_ >= 2:
                    p_ = "*" * (L_ - 1) + "_"  # KHONG doi xung nen dao nguoc khac chinh no
                    ca[f"b21md_{kieu}_tron_{L_}_dao"] = ("a.md", "Theo r1: " + p_ + q + p_[::-1] + " " + NL + ".\n", None, V(c=1))
                    ca[f"b21md_{kieu}_tron_{L_}_khong_dao"] = ("a.md", "Theo r1: " + p_ + q + p_ + " " + NL + ".\n", None, V(v=1))
        # (f) chuan / bo_dau — khoang trang BIEN, nhieu dong, tab/NBSP; bam LITERAL: sha256("dong hai co noi dung")[:8] = b2ddf1aa,
        # sha256("dong mot\ndong hai co noi dung")[:8] = 0483e794, sha256("dong ba co noi dung")[:8] = 822746f7.
        ca.update({"b21ch_bien_hai_phia": ("a.md", "Theo r41 " + CT0("r41:1 #b2ddf1aa|hai co noi dung") + ".\n", None, V(d=1)),
                   "b21ch_nhieu_dong": ("a.md", "Theo r42 " + CT0("r42:1-2 #0483e794|dong hai co noi dung") + ".\n", None, V(d=1)),
                   "b21ch_tab_nbsp_giua": ("a.md", "Theo r43 " + CT0("r43:1 #822746f7|ba co noi dung") + ".\n", None, V(d=1)),
                   "b21bd_manh_bien": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|  hai co noi dung  ") + ".\n", None, V(d=1)),
                   "b21bd_manh_tab_nbsp": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai\tco  noi" + chr(0xA0) + "dung") + ".\n", None, V(d=1)),
                   "b21bd_manh_ngan_sau_chuan": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|  ab   ") + ".\n", None, V(v=1)),
                   "b21bd_manh_nguon_bien": ("a.md", "Theo r41 " + CT0("r41:1 #b2ddf1aa|  dong hai co") + ".\n", None, V(d=1))})
        # KIEM PHU BANG MAY tren tep DA SINH — thieu MOT o => DO.
        def o_r21(ten, doc):
            nhom, kieu = ten.split("_")[0][3:], ten.split("_")[1]; q = Q8 if kieu == "thang" else C8
            if nhom == "eof":
                cuoi = doc.rstrip("\n").rsplit("\n", 1)[-1]
                return {(kieu, "eof", doc.endswith("\n"), doc.endswith("\n\n"), cuoi.lstrip().startswith("|"), doc.count("\n\n") > 0 and not doc.endswith("\n"),
                         "r1" in doc, NL in doc)}
            if nhom == "td":
                tds = [l for l in doc.split("\n") if l.startswith("#")]
                that = [l for l in tds if re.fullmatch(r"#{1,6} .*", l) is not None and l[:7] != "#" * 7]
                return {(kieu, "td", tuple("r1" in l or "r2" in l for l in that), len(tds) != len(that), "\n\n" in doc.split(q)[0])} | {
                    (kieu, "muc", len(l) - len(l.lstrip("#"))) for l in tds}
            if nhom == "py":
                n_ = len(ast.literal_eval(doc[4:].strip()))
                return {(kieu, "py", n_ if 39 <= n_ <= 41 else "ngan" if n_ < 20 else "dai")}
            if nhom == "kt":
                g = doc[doc.index(q) + len(q):doc.index(NL)]
                return {(kieu, "kt", g, all(c_.isspace() for c_ in g))}
            if nhom == "md":
                mo = doc[len("Theo r1: "):doc.index(q)]; g = doc[doc.index(q) + len(q):doc.index(" " + NL)]
                return {(kieu, "md", len(mo), len(g), "".join(sorted(set(mo + g))), g == mo[::-1])}
            return set()
        can_r21 = set()
        for k in ("thang", "cong"):
            can_r21 |= {(k, "eof", nl, nhieu, bang, sau, tk, nh) for nl, nhieu, bang, sau, tk, nh in (
                        (False, False, False, False, True, False), (True, False, False, False, True, False), (True, True, False, False, True, False),
                        (False, False, False, True, True, False), (False, False, True, False, True, False), (True, False, True, False, True, False),
                        (False, False, False, False, True, True), (False, False, False, False, False, False))}
            can_r21 |= {(k, "td", seq, gia, cach) for seq, gia, cach in (((True, False), False, True), ((True, False), False, False),
                        ((False, True), False, True), ((False, True), False, False), ((True, True), False, True), ((True,), False, False),
                        ((True,), False, True), ((), True, True))} | {(k, "muc", m_) for m_ in (1, 2, 6, 7)}
            can_r21 |= {(k, "py", x_) for x_ in (39, 40, 41, "ngan", "dai")}
            can_r21 |= {(k, "kt", c_, True) for c_ in (" ", "\t", "\n", "\x0b", "\x0c", "\r", chr(0xA0), chr(0x2003), chr(0x3000),
                                                    chr(0x1680), chr(0x202F), chr(0x2028), chr(0x1C), chr(0xA0) + " ")} | {
                (k, "kt", c_, False) for c_ in (chr(0x200B), chr(0xAD), chr(0x2060))}
            can_r21 |= {(k, "md", L_, L_, ch, True) for L_ in range(1, 9) for ch in "*_"} | {
                (k, "md", a_, b_, ch, False) for L_ in range(1, 9) for ch in "*_" for a_, b_ in ((L_, L_ + 1), (L_ + 1, L_))} | {
                (k, "md", L_, L_, "*_", d_) for L_ in range(2, 9) for d_ in (True, False)}
        phu_r21 = set().union(*(o_r21(t_, v[1]) for t_, v in ca.items() if t_.split("_")[0] in ("b21eof", "b21td", "b21py", "b21kt", "b21md")))
        hong += [f"PHU_R21: o chua co ca: {sorted(can_r21 - phu_r21, key=str)}"] if can_r21 - phu_r21 else []
        # Phu cua chuan/bo_dau tinh tu NGUON va manh da viet: khoang trang bien ca hai phia, nhieu dong, ky tu khong phai space.
        def o_ch():  # moi ca con tro: tinh tu CHINH cac dong nguon duoc tro va manh da viet
            o = set()
            for t_, v in ca.items():
                if not t_.startswith(("b21ch_", "b21bd_")): continue
                m_ = re.search(r"r(\d+):(\d+)(?:-(\d+))? ", v[1]); a_, b_ = int(m_.group(2)), int(m_.group(3) or m_.group(2))
                ds = (Path(t) / f"r{m_.group(1)}.md").read_text(encoding="utf-8").split("\n")[a_ - 1:b_]
                o |= {("nguon", len(ds) > 1, all(l[:1].isspace() for l in ds), all(l[-1:].isspace() for l in ds),
                       any(c_.isspace() and c_ != " " for l in ds for c_ in l.strip()))}
                mh = v[1].split("|", 1)[1].split(chr(0x27E7))[0]
                o |= {("manh", mh != mh.strip(), any(c_.isspace() and c_ != " " for c_ in mh.strip()), len(mh.strip()) >= 6)}
            return o
        can_ch = {("nguon", False, True, True, False), ("nguon", True, True, True, False), ("nguon", False, True, False, True),
                  ("manh", True, False, True), ("manh", False, True, True), ("manh", True, False, False)}
        hong += [f"PHU_CHUAN: o chua co ca: {sorted(can_ch - o_ch())}"] if can_ch - o_ch() else []
        for ten, (tep, doc, ham, mong) in ca.items():
            p = Path(t) / ten / tep; p.parent.mkdir(); p.write_text(doc, encoding="utf-8")
            d = kiem(t, "r{n}.md", p, ham)
            thuc = (d["DUNG"], d["LECH"], d["KHONG_DO_DUOC"], d["VI_PHAM"], d["CO_NHAN"])
            if thuc != mong: hong.append(f"{ten}: mong {mong}, thuc {thuc}")
        # HOP DONG CLI — bang co tham quyen o dac ta r15 §0.14; cac ca SINH tu bang (to hop), khong liet ke tay.
        # Moi tep mau mang VEC TO ky vong viet tay (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN); ky vong cua mot lan chay
        # nhieu tep = TONG tung phan tu; rc ky vong = 1 khi LECH + KHONG_DO_DUOC + VI_PHAM > 0. Oracle chi cong va so sanh,
        # khong goi `kiem`/`main`/regex nao cua cong. Nguon CLI dung MAU TEN RIENG (`spec-r{n}.txt`) de `--mau` co rang.
        import itertools, subprocess as _sp
        nc = Path(t) / "nguon_cli"; nc.mkdir()
        (nc / "spec-r3.txt").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        dc = Path(t) / "cli"; dc.mkdir()
        TEP_CLI = {
            "sach.md": ("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", (1, 0, 0, 0, 0)),
            "lech.md": ("Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "lech2.md": ("Theo r3 " + CT0("r3:11 #00000000|so 11 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "thieu.md": ("Theo r9 " + CT0("r9:1 #00000000|khong co tep nao") + ".\n", (0, 0, 1, 0, 0)),
            "vipham.md": ("Theo r1: " + Q8 + ".\n", (0, 0, 0, 1, 0)),
            "nhan.md": ("Theo r1: " + Q8 + " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
            "nhan_gach.md": ("Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
        }
        for ten, (noi, _v) in TEP_CLI.items(): (dc / ten).write_text(noi, encoding="utf-8")
        COT = ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")
        CO = ["--nguon", str(nc), "--mau", "spec-r{n}.txt"]
        VI_TRI = {"co_truoc": lambda co, tep: co + tep, "co_sau": lambda co, tep: tep + co,
                  "co_xen": lambda co, tep: tep[:1] + co + tep[1:]}
        ds_tep = sorted(TEP_CLI)
        to_hop = [(x,) for x in ds_tep] + list(itertools.permutations(ds_tep, 2)) + [
            ("lech.md", "lech2.md", "vipham.md"), ("sach.md", "nhan.md", "nhan_gach.md"), ("thieu.md", "sach.md", "thieu.md"),
            tuple(ds_tep)]
        cli = {}
        for so, bo in enumerate(to_hop):
            vt = list(VI_TRI)[so % 3] if len(bo) > 1 else None
            for v in ([vt] if vt else list(VI_TRI)):
                mong = tuple(sum(TEP_CLI[x][1][c] for x in bo) for c in range(5))
                cli[f"cli_{v}_{'+'.join(bo)}"] = (VI_TRI[v](CO, [str(dc / x) for x in bo]), int(sum(mong[1:4]) > 0), mong)
        # --ham: tep 5 ham, XAU = {a, c, e}; ky vong VI_PHAM = so ten trong danh sach thuoc XAU (ten la khong tinh).
        XAU = {"a", "c", "e"}
        (dc / "h.py").write_text("".join(f"def {n}():\n    " + Q2 * 3 + f"Ham {n} nhac r1 " + (Q8 + " khong nhan" if n in XAU else "va khong trich gi")
                                 + ", du dai de qua nguong bon muoi.\n    " + Q2 * 3 + "\n\n\n" for n in "abcde"), encoding="utf-8")
        # r16 (luot 11): vi tri TUNG co la mot truc RIENG, tach khoi noi dung danh sach ham — moi danh sach x `--ham`
        # truoc / sau chinh tep; `--nguon`/`--mau` luan phien truoc / sau.
        for so, ds_ham in enumerate(("a", "b", "c", "e", "a,b", "b,c", "d,e", "b,c,d", "d,c,b", "b,zz,d", "zz", "a,b,c,d,e", "b,d")):
            vi = len(set(ds_ham.split(",")) & XAU)
            for vt_ham, tep in (("ham_truoc", ["--ham", ds_ham, str(dc / "h.py")]), ("ham_sau", [str(dc / "h.py"), "--ham", ds_ham])):
                cli[f"cli_{vt_ham}_{ds_ham}"] = ((CO + tep) if so % 2 == 0 else (tep + CO), int(vi > 0), (0, 0, 0, vi, 0))
        cli["cli_khong_ham_h"] = (CO + [str(dc / "h.py")], 1, (0, 0, 0, 3, 0))
        # KIEM PHU BANG MAY tren argv DA SINH (khong tren y dinh): moi o cua bang §0.14 phai co >= 1 ca. Vi tri cua moi co
        # tinh theo chi so trong argv so voi cac TEP (doi so khong phai co, khong phai gia tri cua co).
        def o_cua(doi):
            tep_i, co_i, i = [], {}, 0
            while i < len(doi):
                if doi[i] in ("--nguon", "--mau", "--ham"): co_i[doi[i]] = i; i += 2
                else: tep_i.append(i); i += 1
            vt = lambda i: "truoc" if i < tep_i[0] else "sau" if i > tep_i[-1] else "xen"
            return {("so_tep", len(tep_i))} | {(f"vi_tri{c}", vt(i)) for c, i in co_i.items()}
        can = ({("so_tep", n) for n in (1, 2, 3, 7)} | {(f"vi_tri{c}", v) for c in ("--nguon", "--mau") for v in ("truoc", "sau", "xen")}
               | {("vi_tri--ham", v) for v in ("truoc", "sau")})
        co_phu = set().union(*(o_cua(doi) for doi, _r, _m in cli.values()))
        if can - co_phu: hong.append(f"PHU_BANG: o chua co ca: {sorted(can - co_phu)}")
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", *doi], capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[0][5:]) if len(tong) == 1 else {}
            thuc = (r.returncode, len(tong), tuple(d.get(k) for k in COT))
            if thuc != (rc_mong, 1, mong): hong.append(f"{ten}: mong {(rc_mong, 1, mong)}, thuc {thuc}")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}", f"(truc tiep {len(ca)}, CLI {len(cli)})")
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

## Phụ lục P — cổng CON TRỎ v13: bảng biên B22, bảng nhánh→ca, phép phủ trên byte đọc lại, §0.21 (MỚI ở r22, nguyên văn)

Cùng cách chạy như Phụ lục E. `tu-kiem` in: `TU_KIEM DAT 640/640 (truc tiep 544, CLI 96)` (số lấy từ lần chạy khi dựng đặc tả, không gõ tay). So với Phụ lục O chỉ `tu_kiem` đổi. sha256 của khối mã dưới (tệp `con_tro.py`, không kể dòng rào): `a087b2ecd94fdb2f9b34173d34341cddcce1cf4d9955457376a23a3ab30ccf3f`.

```python
"""Con tro nguon cho dac ta R378 (r10 #574) — thay moi loi trich VIET TAY cua revision khac.

  CON TRO   ⟦rN:L #h|manh⟧ hoac ⟦rN:L-M #h|manh⟧ : dong L (den M) cua dac ta revision N; h = 8 hex dau cua
            sha256 noi dung cac dong ay sau chuan hoa (bo khoang trang dau/cuoi moi dong, gop khoang trang). Tro sai
            dong => h lech => DO. `manh` (BAT BUOC tu r11, >= 6 ky tu) la cum chu ma cau dan con tro dang noi toi; no
            phai NAM TRONG cac dong duoc tro (so sau khi bo `*` va dau backtick, gop khoang trang) — tro dung bam ma
            sai dong CAN TRO (F1d #574 luot 6: r3:322 thay vi 323-324) => DO. Sinh bang lenh `sinh`, KHONG go tay.
  NHAN NGUON ⟦nguon:K⟧ ngay sau mot chuoi trong ngoac (markup giua cau va nhan chi duoc la markup DONG, dao nguoc dung
            markup MO ngay truoc cau; tu r19): chuoi ay KHONG phai loi cua mot revision (K thuoc
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
NHAN = re.compile(r"([*_]*)\s*⟦nguon:(chi-thi|verdict|commit|ma|doctrine|issue)⟧")
MO = re.compile(r"[*_]*\Z")  # markup MO ngay truoc dau ngoac mo cua cau (r19)
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
            n = NHAN.match(k, m.end())  # r19: markup DONG giua cau va nhan phai la dao nguoc DUNG markup MO ngay truoc cau
            if n and n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1]: dem["CO_NHAN"] += 1; continue
            dem["VI_PHAM"] += 1
            print(f"VI_PHAM {tep}:{dong + k[:m.start()].count(chr(10))} chuoi trong ngoac khong nhan nguon: {(m.group(1) or m.group(2))[:90]!r}")
    return dem
def tu_kiem():
    """r12: them BANG LOP DAU VAO (pham vi dong, ngoac cong, nhan, do dai manh, dau markup, span, rao code, bien bang,
    doan docstring) voi con tro viet san — 11 dot bien song cua #574 luot 7 phai DO.
    Ca am/duong voi BO DEM KY VONG chinh xac (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN) — khong chi dat/khong
    dat. Phu MOI nhanh dau vao duoc dung cho hop dong: .md than doan, .md chi co token o TIEU DE, .py qua ast, .py voi
    --ham (vi pham ngoai ham bi bo qua), manh neo. Tung la lo cua r10 (#574 luot 6, F2): bo han nhanh .py hoac vi
    tieu de ma tu kiem van 8/8.
    r22 (luot 17, F2): moi phep PHU tinh tren BYTE DOC LAI tu dung tep `kiem` nhan (khong tren y dinh trong bo nho), va
    byte doc lai phai BANG y dinh truoc moi phep chuan hoa; them bang bien B22 va BANG NHANH -> CA cho moi nhanh parser."""
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
        # r22 (luot 17, F2): MOT cho ghi fixture DUY NHAT; ghi BYTE (khong dich newline theo nen) roi DOC LAI byte tu CHINH
        # tep ay — dung tep ma `kiem` se nhan. Moi phep phu ben duoi doc RB[ten], KHONG doc ca[ten][1].
        RB = {}
        def tep_ca(ten):
            p = Path(t) / ten / ca[ten][0]
            if ten not in RB:
                p.parent.mkdir(); p.write_bytes(ca[ten][1].encode("utf-8"))
                RB[ten] = p.read_bytes().decode("utf-8")
            return p
        def rb(ten): tep_ca(ten); return RB[ten]
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
            # r17 (luot 12): nhan DUNG / SAI / THIEU tron trong CUNG khoi, moi hoan vi thu tu — nhan phai dung NGAY sau cau
            # trich cua no; mot nhan hop le o CHO KHAC trong khoi khong duoc cuu mot cau trich thieu/sai nhan.
            **{ten: ("a.md", "Theo r1: " + "; ".join(Q2 + chu + Q2 + ({"dung": " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7),
                     "sai": " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7), "thieu": ""}[loai]) for chu, loai in zip(("abcdefgh", "ijklmnop", "qrstuvwx"), thu_tu)) + ".\n",
                     None, (0, 0, 0, sum(x != "dung" for x in thu_tu), sum(x == "dung" for x in thu_tu)))
               for ten, thu_tu in (("nhan_xau_truoc_nhan_dung", ("sai", "dung")), ("nhan_dung_truoc_nhan_xau", ("dung", "sai")),
                                   ("nhan_thieu_truoc_nhan_dung", ("thieu", "dung")), ("nhan_dung_truoc_nhan_thieu", ("dung", "thieu")),
                                   ("nhan_xau_thieu_dung", ("sai", "thieu", "dung")), ("nhan_thieu_xau_dung", ("thieu", "sai", "dung")),
                                   ("nhan_dung_xau_thieu", ("dung", "sai", "thieu")))},
            "nhan_sau_gach_duoi": ("a.md", "Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:doctrine" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "nhan_sau_markup_dam": ("a.md", "Theo r1: **" + Q8 + "** " + chr(0x27E6) + "nguon:verdict" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
            "ngoac_cong_vat_dong": ("a.md", "Theo r1: “abcd\nefgh”.\n", None, (0, 0, 0, 1, 0)),
            "rv_sau_gach_noi": ("a.md", "Theo ma-r1: " + Q8 + ".\n", None, (0, 0, 0, 0, 0)),
            "manh_5_am": ("a.md", "Theo r1 " + CT0("r1:1 #2bf318fb|ong m") + ".\n", None, (0, 0, 0, 1, 0)),
        })
        # r18 (luot 13, F2): BANG LOP KHOANG NOI cau-nhan, co tham quyen o dac ta r18 §0.17. Lop: (markup MO truoc cau,
        # khoang noi giua dau ngoac DONG va nhan, cuc). Ca SINH tu bang x hai kieu ngoac; ky vong chi doc CUC — DUONG
        # (0,0,0,0,1), AM (0,0,0,1,0) — khong qua regex nao cua cong. Markup phai DONG ngay sau cau roi moi toi khoang trang.
        DAU_CAU, NL = ";,.:!?", chr(0x27E6) + "nguon:ma" + chr(0x27E7)
        KHOANG_NOI = {"rong": ("", "", "DUONG"), "cach": ("", " ", "DUONG"), "cach_nhieu": ("", "   ", "DUONG"),
                      "tab": ("", "\t", "DUONG"), "xuong_dong": ("", "\n", "DUONG"), "cach_xuong_dong": ("", " \n  ", "DUONG"),
                      "sao": ("*", "*", "DUONG"), "sao_cach": ("*", "* ", "DUONG"), "gach": ("_", "_", "DUONG"),
                      "gach_cach": ("_", "_ ", "DUONG"), "sao_doi": ("**", "**", "DUONG"), "sao_doi_cach": ("**", "** ", "DUONG"),
                      "gach_doi_xuong_dong": ("__", "__\n", "DUONG"),
                      **{f"dau{i}": ("", c, "AM") for i, c in enumerate(DAU_CAU)},
                      **{f"dau{i}_cach": ("", c + " ", "AM") for i, c in enumerate(DAU_CAU)},
                      "sao_roi_dau": ("*", "*; ", "AM"), "cach_roi_dau": ("", " , ", "AM"), "cach_roi_sao": ("", " *", "AM"),
                      "chu": ("", " va ", "AM"), "chu_dinh": ("", "x ", "AM"), "noi_dung_xen": ("", " (ghi chu) ", "AM"),
                      "ngoac_dong": ("", ") ", "AM"), "gach_ngang": ("", " — ", "AM"), "doan_moi": ("", "\n\n", "AM")}
        MO_DAU = "Theo r1: "
        for lop, (mo, kn, cuc) in KHOANG_NOI.items():
            for kieu, q in (("thang", Q8), ("cong", C8)):
                ca[f"kn_{kieu}_{lop}"] = ("a.md", MO_DAU + mo + q + kn + NL + ".\n", None, (0, 0, 0, 0, 1) if cuc == "DUONG" else (0, 0, 0, 1, 0))
        # doi chung viet tay: nhan TRUOC cau; hai nhan hop le lien tiep; nhan sai roi nhan dung sau CUNG mot cau
        ca.update({"kn_nhan_truoc_cau": ("a.md", MO_DAU + NL + " " + Q8 + ".\n", None, (0, 0, 0, 1, 0)),
                   "kn_hai_nhan_lien_tiep": ("a.md", MO_DAU + Q8 + " " + NL + " " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", None, (0, 0, 0, 0, 1)),
                   "kn_nhan_sai_roi_dung": ("a.md", MO_DAU + Q8 + " " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7) + " " + NL + ".\n", None, (0, 0, 0, 1, 0))})
        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22): tach khoang noi khoi noi dung tep, roi doi moi o.
        def o_kn(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; g = doc[doc.index(q) + len(q):doc.index(NL)]
            cuc = "DUONG" if ca[ten][3][4] else "AM"; than = g.lstrip("*_"); dau = g[:len(g) - len(than)]; o = set()
            if dau: o.add((kieu, cuc, "markup", dau, than != ""))
            if not g.strip(): o.add((kieu, cuc, "trang", g))
            if than and than[0] in DAU_CAU: o.add((kieu, cuc, "dau", than[0], than[1:] != ""))
            if any(c.isalnum() for c in g): o.add((kieu, cuc, "chu"))
            if g[:1].isspace() and g.strip()[:1] in ("*", "_"): o.add((kieu, cuc, "trang_roi_markup"))
            return o
        can_kn = {(k, "DUONG", "trang", w) for k in ("thang", "cong") for w in ("", " ", "\t", "\n")} | {
            (k, "DUONG", "markup", m, t) for k in ("thang", "cong") for m in ("*", "_", "**", "__") for t in ((False, True) if len(m) == 1 else (True,))} | {
            (k, "AM", "dau", c, t) for k in ("thang", "cong") for c in DAU_CAU for t in (False, True)} | {
            (k, "AM", x) for k in ("thang", "cong") for x in ("chu", "trang_roi_markup")} | {(k, "AM", "trang", "\n\n") for k in ("thang", "cong")}
        phu_kn = set().union(*(o_kn(ten, rb(ten)) for ten in list(ca) if ten.startswith(("kn_thang_", "kn_cong_"))))
        hong = [f"PHU_KHOANG_NOI: o chua co ca: {sorted(can_kn - phu_kn, key=str)}"] if can_kn - phu_kn else []
        # r19 (luot 14, F3): BANG CAP MARKUP — markup DONG giua cau va nhan phai la dao nguoc DUNG markup MO ngay truoc cau.
        # (mo, khoang noi, cuc); ky vong chi doc CUC. Loai o tinh LAI tu tep da sinh, khong doc bang.
        CAP_MARKUP = {"dung_sao": ("*", "*", "DUONG"), "dung_gach": ("_", "_ ", "DUONG"), "dung_sao_doi": ("**", "** ", "DUONG"),
                      "dung_gach_doi": ("__", "__", "DUONG"), "dung_tron": ("*_", "_* ", "DUONG"), "dung_tron_nguoc": ("_*", "*_", "DUONG"),
                      "dung_ba": ("***", "*** ", "DUONG"), "thieu_mo_sao": ("", "* ", "AM"), "thieu_mo_gach": ("", "_", "AM"),
                      "thieu_mo_doi": ("", "** ", "AM"), "khac_loai_sao_gach": ("*", "_ ", "AM"), "khac_loai_gach_sao": ("_", "*", "AM"),
                      "khac_loai_doi": ("**", "__ ", "AM"), "khac_loai_sai_thu_tu": ("*_", "*_ ", "AM"), "dai_ngan": ("**", "* ", "AM"),
                      "ngan_dai": ("*", "** ", "AM"), "gach_ngan_dai": ("_", "__", "AM"), "ba_hai": ("***", "** ", "AM"),
                      "mo_khong_dong_sao": ("*", " ", "AM"), "mo_khong_dong_doi": ("**", "", "AM"), "mo_khong_dong_gach": ("_", "\n", "AM")}
        # r19 (luot 14, F2 vong 8): BANG RANH GIOI code–van ban; {q} = cau trich. Ky vong viet tay tung dong.
        BIEN_CODE = {"code_xen": ("{q} `x` " + NL, "AM"), "code_lien_sau_cau": ("{q}`x` " + NL, "AM"),
                     "code_truoc_cau": ("`x` {q} " + NL, "DUONG"), "cau_trong_code": ("`{q}` " + NL, "KHONG"),
                     "nhan_trong_code": ("{q} `" + NL + "`", "AM"), "nhan_lien_sau_cau": ("{q}" + NL, "DUONG"),
                     "markup_roi_code_xen": ("*{q}* `x` " + NL, "AM"), "markup_mo_trong_code": ("`*`{q}* " + NL, "AM")}
        VEC = {"DUONG": (0, 0, 0, 0, 1), "AM": (0, 0, 0, 1, 0), "KHONG": (0, 0, 0, 0, 0)}
        for kieu, q in (("thang", Q8), ("cong", C8)):
            for lop, (mo, kn, cuc) in CAP_MARKUP.items(): ca[f"cm_{kieu}_{lop}"] = ("a.md", MO_DAU + mo + q + kn + NL + ".\n", None, VEC[cuc])
            for lop, (mau, cuc) in BIEN_CODE.items(): ca[f"bc_{kieu}_{lop}"] = ("a.md", MO_DAU + mau.format(q=q) + ".\n", None, VEC[cuc])
        def o_cm(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; mo = doc[len(MO_DAU):doc.index(q)]
            g = doc[doc.index(q) + len(q):doc.index(NL)]; dong = g[:len(g) - len(g.lstrip("*_"))]; cuc = "DUONG" if ca[ten][3][4] else "AM"
            loai = ("dung" if dong == mo[::-1] else "thieu_mo" if not mo else "mo_khong_dong" if not dong
                    else "khac_do_dai" if len(dong) != len(mo) else "khac_loai")
            return {(kieu, cuc, loai, "".join(sorted(set(mo + dong))), max(len(mo), len(dong)) > 1)}  # loai x ky tu x nhieu ky tu
        def o_bc(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; a, b = doc.index(q), doc.index(q) + len(q); c = doc.index(NL)
            o = {(kieu, "nhan_lien_sau_cau")} if c == b else set()
            for x in re.finditer(r"`[^`\n]*`", doc):
                o |= {(kieu, "code_truoc_cau")} if x.end() <= a else {(kieu, "cau_trong_code")} if x.start() < a and b <= x.end() else set()
                o |= {(kieu, "code_xen", b == x.start(), doc[b:x.start()].strip() != "")} if b <= x.start() and x.end() <= c else {(kieu, "nhan_trong_code")} if x.start() < c < x.end() else set()
            return o
        O_CM = {"DUONG": {"dung": (("*", 0), ("_", 0), ("*", 1), ("_", 1), ("*_", 1))},
                "AM": {"thieu_mo": (("*", 0), ("_", 0), ("*", 1)), "khac_loai": (("*_", 0), ("*_", 1)),
                       "khac_do_dai": (("*", 1), ("_", 1)), "mo_khong_dong": (("*", 0), ("*", 1), ("_", 0))}}
        can_cm = {(k, cuc, loai, ky, bool(nhieu)) for k in ("thang", "cong") for cuc, d in O_CM.items() for loai, os_ in d.items() for ky, nhieu in os_}
        can_bc = {(k, x) for k in ("thang", "cong") for x in ("cau_trong_code", "code_truoc_cau", "nhan_lien_sau_cau", "nhan_trong_code")} | {
            (k, "code_xen", lien, markup) for k in ("thang", "cong") for lien, markup in ((False, False), (True, False), (False, True))}
        phu_cm = set().union(*(o_cm(t_, rb(t_)) for t_ in list(ca) if t_.startswith("cm_")))
        phu_bc = set().union(*(o_bc(t_, rb(t_)) for t_ in list(ca) if t_.startswith("bc_")))
        hong += [f"PHU_CAP_MARKUP: o chua co ca: {sorted(can_cm - phu_cm, key=str)}"] if can_cm - phu_cm else []
        hong += [f"PHU_RANH_GIOI_CODE: o chua co ca: {sorted(can_bc - phu_bc)}"] if can_bc - phu_bc else []
        # r20 (luot 15, F2): ba TRUC moi, ky vong VIET TAY chi doc cuc/vecto, khong goi NHAN/MO/Q/kiem.
        # (1) VI TRI cau: dau khoi, dong thut le, sau newline ma dong truoc KET THUC bang markup, sau newline thuong.
        VI_TRI_CAU = {"dau_khoi": ("{mo}{q}{dong} " + NL + " theo r1.", "{c}"), "thut_le": ("  Theo r1: {mo}{q}{dong} " + NL + ".", "{c}"),
                      "sau_dong_ket_markup": ("Theo r1: *\n{mo}{q}{dong} " + NL + ".", "{c}"),
                      "sau_dong_thuong": ("Theo r1:\n{mo}{q}{dong} " + NL + ".", "{c}")}
        CAP_VT = {"khong": ("", "", "DUONG"), "sao": ("*", "*", "DUONG"), "sao_thieu_mo": ("", "*", "AM"), "sao_doi_lech": ("**", "*", "AM")}
        # (2) LAN XUAT HIEN: cung noi dung hai lan tren mot dong, khac nhan hoac khac cap; vecto viet tay (VI_PHAM, CO_NHAN).
        LAN = {"dung_roi_thieu_mo": ("*{q}* " + NL + "; {q}* " + NL, (1, 1)), "thieu_mo_roi_dung": ("{q}* " + NL + "; *{q}* " + NL, (1, 1)),
               "co_nhan_roi_khong": ("{q} " + NL + "; {q} khong nhan", (1, 1)), "khong_roi_co_nhan": ("{q} khong nhan; {q} " + NL, (1, 1)),
               "nhan_dung_roi_sai": ("{q} " + NL + "; {q} " + chr(0x27E6) + "nguon:khong-hop-le" + chr(0x27E7), (1, 1)),
               "ca_hai_dung_khac_cap": ("*{q}* " + NL + "; **{q}** " + NL, (0, 2))}
        # (3) DO DAI markup >= 4 (vuot moi mau cu): cap dung va lech do dai.
        DO_DAI = {"bon_bon": ("****", "****", "DUONG"), "nam_nam": ("*****", "*****", "DUONG"), "gach_bon": ("____", "____", "DUONG"),
                  "bon_ba": ("****", "***", "AM"), "ba_bon": ("***", "****", "AM"), "bon_nam": ("****", "*****", "AM")}
        for kieu, q in (("thang", Q8), ("cong", C8)):
            for vt, (mau, _c) in VI_TRI_CAU.items():
                for cap, (mo, dong, cuc) in CAP_VT.items():
                    ca[f"vt_{kieu}_{vt}_{cap}"] = ("a.md", mau.format(mo=mo, q=q, dong=dong) + "\n", None, VEC[cuc])
            for ten, (mau, (vp, cn)) in LAN.items(): ca[f"lan_{kieu}_{ten}"] = ("a.md", "Theo r1: " + mau.format(q=q) + ".\n", None, (0, 0, 0, vp, cn))
            for ten, (mo, dong, cuc) in DO_DAI.items(): ca[f"dd_{kieu}_{ten}"] = ("a.md", "Theo r1: " + mo + q + dong + " " + NL + ".\n", None, VEC[cuc])
        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22; tinh lai tu noi dung tep, khong doc bang).
        def o_r20(ten, doc):
            kieu = ten.split("_")[1]; q = Q8 if kieu == "thang" else C8; a = doc.index(q); dong_dau = doc[:a].rsplit("\n", 1)[-1]
            o = set()
            if ten.startswith("vt_"):
                truoc = doc[:a - len(dong_dau)]
                chi_markup = dong_dau.strip("*_") == ""
                vt = ("dau_khoi" if not truoc and chi_markup else "thut_le" if dong_dau[:1] == " " else "sau_dong_ket_markup"
                      if truoc and chi_markup and truoc.rstrip("\n")[-1:] in ("*", "_") else "sau_dong_thuong" if truoc and chi_markup else "giua_dong")
                o.add((kieu, "vi_tri", vt, "DUONG" if ca[ten][3][4] else "AM"))
            if ten.startswith("lan_") and doc.count(q) >= 2:  # moi lan: (markup truoc, markup sau, nhan hop le ngay sau?)
                def lan(i):
                    t = doc[:i]; mo = t[len(t.rstrip("*_")):]; d = doc[i + len(q):]; dong = d[:len(d) - len(d.lstrip("*_"))]
                    return mo, dong, dong == mo[::-1] and d[len(dong):].lstrip(" ").startswith(NL)
                l1, l2 = lan(a), lan(doc.index(q, a + 1))
                o.add((kieu, "lan", l1[2], l2[2], "cap" if l1[:2] != l2[:2] else "nhan"))
            if ten.startswith("dd_"):
                mo = dong_dau[len(dong_dau.rstrip("*_")):] if dong_dau.rstrip("*_") != dong_dau else ""
                d = doc[a + len(q):]; dong = d[:len(d) - len(d.lstrip("*_"))]
                o.add((kieu, "do_dai", max(len(mo), len(dong)) >= 4, len(mo) == len(dong)))
            return o
        can_r20 = {(k, "vi_tri", v, c) for k in ("thang", "cong") for v in ("dau_khoi", "thut_le", "sau_dong_ket_markup", "sau_dong_thuong")
                   for c in ("DUONG", "AM")} | {(k, "lan", t1, t2, x) for k in ("thang", "cong") for t1, t2, x in ((True, False, "cap"), (False, True, "cap"), (True, False, "nhan"),
                                                                         (False, True, "nhan"), (True, True, "cap"))} | {
                   (k, "do_dai", True, e) for k in ("thang", "cong") for e in (True, False)}
        phu_r20 = set().union(*(o_r20(t_, rb(t_)) for t_ in list(ca) if t_.startswith(("vt_", "lan_", "dd_"))))
        hong += [f"PHU_R20: o chua co ca: {sorted(can_r20 - phu_r20, key=str)}"] if can_r20 - phu_r20 else []
        # r21 (luot 16, F2): BANG BIEN DOC LAP cho moi ham co hanh vi ranh gioi — khoi_md (EOF, chuyen tieu de), khoi_py
        # (nguong 40), chuan/bo_dau (khoang trang bien, nhieu dong, loai khoang trang), NHAN/MO (do dai markup 1..8 la
        # THUOC TINH), loai khoang trang giua cau va nhan. Ky vong VIET TAY; bam la LITERAL tinh doc lap (sha256 cua chuoi
        # chuan hoa viet tay), khong goi chuan/bam/sinh/kiem de sinh dap an.
        (Path(t) / "r41.md").write_text("  dong hai co noi dung  \n", encoding="utf-8")
        (Path(t) / "r42.md").write_text(" dong  mot\t\n" + chr(0xA0) + "dong hai co noi dung  \n", encoding="utf-8")
        (Path(t) / "r43.md").write_text("\tdong  ba" + chr(0xA0) + "co   noi dung\n", encoding="utf-8")
        V = lambda d=0, l=0, k=0, v=0, c=0: (d, l, k, v, c)
        for kieu, q in (("thang", Q8), ("cong", C8)):
            # (a) khoi_md — EOF co/khong newline, khoi cuoi, bang cuoi, nhieu khoi.
            for ten, (doc, mong) in {"mot_khong_nl": ("Theo r1: {q}.", V(v=1)), "mot_co_nl": ("Theo r1: {q}.\n", V(v=1)),
                                     "mot_nhieu_nl": ("Theo r1: {q}.\n\n\n", V(v=1)), "sau_khoi_khong_nl": ("Mo dau.\n\nTheo r1: {q}.", V(v=1)),
                                     "bang_khong_nl": ("| a | b |\n| r1 | {q} |", V(v=1)), "bang_co_nl": ("| a | b |\n| r1 | {q} |\n", V(v=1)),
                                     "nhan_khong_nl": ("Theo r1: {q} " + NL, V(c=1)), "hai_khoi_khong_nl": ("Theo r1: {q}.\n\nTheo r1: {q}.", V(v=2)),
                                     "khong_token_khong_nl": ("Mo dau {q}.", V())}.items():
                ca[f"b21eof_{kieu}_{ten}"] = ("a.md", doc.format(q=q), None, mong)
            # (b) khoi_md — chuyen TIEU DE co/khong token, ca hai chieu, lien/cach dong, muc 1..7, thieu khoang trang.
            for ten, (doc, mong) in {"co_roi_khong": ("## Nhan xet r1\n\nVan ban khong trich.\n\n## Chu de khac\n\n{q}.\n", V()),
                                     "co_roi_khong_lien": ("## Nhan xet r1\n## Chu de khac\n{q}.\n", V()),
                                     "khong_roi_co": ("## Chu de khac\n\n## Nhan xet r1\n\n{q}.\n", V(v=1)),
                                     "khong_roi_co_lien": ("## Chu de khac\n## Nhan xet r1\n{q}.\n", V(v=1)),
                                     "co_roi_co": ("## Nhan xet r1\n\n## Nhan xet r2\n\n{q}.\n", V(v=1)),
                                     "co_lien": ("## Nhan xet r1\n{q}.\n", V(v=1)), "co_cach": ("## Nhan xet r1\n\n{q}.\n", V(v=1)),
                                     "muc1": ("# Nhan xet r1\n\n{q}.\n", V(v=1)), "muc6": ("###### Nhan xet r1\n\n{q}.\n", V(v=1)),
                                     "muc7_khong_la_tieu_de": ("####### Nhan xet r1\n\n{q}.\n", V()),
                                     "thieu_cach_khong_la_tieu_de": ("##Nhan xet r1\n\n{q}.\n", V()),
                                     "co_roi_rao": ("## Nhan xet r1\n\n```\nx\n```\n\n{q}.\n", V(v=1))}.items():
                ca[f"b21td_{kieu}_{ten}"] = ("a.md", doc.format(q=q), None, mong)
            # (c) khoi_py — chuoi duoi / DUNG / tren nguong 40, va chuoi ngan; ky vong theo DO DAI viet tay.
            for n_ in (14, 39, 40, 41, 60):
                s_ = ("r1: " + q + " " + "x" * 60)[:n_] if n_ > 14 else "r1: " + q
                assert len(s_) == n_
                ca[f"b21py_{kieu}_{n_}"] = ("a.py", "X = " + repr(s_) + "\n", None, V(v=1) if n_ in (41, 60) else V())
            # (d) loai KHOANG TRANG giua dau ngoac dong va nhan: moi ky tu `str.isspace` -> DUONG; ky tu vo hinh khong
            # phai khoang trang -> AM.
            for ten, g in {"space": " ", "tab": "\t", "lf": "\n", "vt": "\x0b", "ff": "\x0c", "cr": "\r", "nbsp": chr(0xA0),
                           "nbsp_space": chr(0xA0) + " ", "em": chr(0x2003), "ideo": chr(0x3000), "ogham": chr(0x1680),
                           "hep": chr(0x202F), "ls": chr(0x2028), "fs": chr(0x1C)}.items():
                ca[f"b21kt_{kieu}_{ten}"] = ("a.md", "Theo r1: " + q + g + NL + ".\n", None, V(c=1))
            for ten, g in {"zwsp": chr(0x200B), "shy": chr(0xAD), "wj": chr(0x2060)}.items():
                ca[f"b21kt_{kieu}_{ten}"] = ("a.md", "Theo r1: " + q + g + NL + ".\n", None, V(v=1))
            # (e) NHAN/MO — do dai markup la THUOC TINH 1..8: cap dung (L,L) DUONG; lech (L,L+1), (L+1,L) AM; tron nguoc DUONG,
            # tron khong dao AM.
            for L_ in range(1, 9):
                for ch in "*_":
                    ca[f"b21md_{kieu}_{ch == '*' and 'sao' or 'gach'}_{L_}_{L_}"] = ("a.md", "Theo r1: " + ch * L_ + q + ch * L_ + " " + NL + ".\n", None, V(c=1))
                    ca[f"b21md_{kieu}_{ch == '*' and 'sao' or 'gach'}_{L_}_{L_ + 1}"] = ("a.md", "Theo r1: " + ch * L_ + q + ch * (L_ + 1) + " " + NL + ".\n", None, V(v=1))
                    ca[f"b21md_{kieu}_{ch == '*' and 'sao' or 'gach'}_{L_ + 1}_{L_}"] = ("a.md", "Theo r1: " + ch * (L_ + 1) + q + ch * L_ + " " + NL + ".\n", None, V(v=1))
                if L_ >= 2:
                    p_ = "*" * (L_ - 1) + "_"  # KHONG doi xung nen dao nguoc khac chinh no
                    ca[f"b21md_{kieu}_tron_{L_}_dao"] = ("a.md", "Theo r1: " + p_ + q + p_[::-1] + " " + NL + ".\n", None, V(c=1))
                    ca[f"b21md_{kieu}_tron_{L_}_khong_dao"] = ("a.md", "Theo r1: " + p_ + q + p_ + " " + NL + ".\n", None, V(v=1))
        # (f) chuan / bo_dau — khoang trang BIEN, nhieu dong, tab/NBSP; bam LITERAL: sha256("dong hai co noi dung")[:8] = b2ddf1aa,
        # sha256("dong mot\ndong hai co noi dung")[:8] = 0483e794, sha256("dong ba co noi dung")[:8] = 822746f7.
        ca.update({"b21ch_bien_hai_phia": ("a.md", "Theo r41 " + CT0("r41:1 #b2ddf1aa|hai co noi dung") + ".\n", None, V(d=1)),
                   "b21ch_nhieu_dong": ("a.md", "Theo r42 " + CT0("r42:1-2 #0483e794|dong hai co noi dung") + ".\n", None, V(d=1)),
                   "b21ch_tab_nbsp_giua": ("a.md", "Theo r43 " + CT0("r43:1 #822746f7|ba co noi dung") + ".\n", None, V(d=1)),
                   "b21bd_manh_bien": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|  hai co noi dung  ") + ".\n", None, V(d=1)),
                   "b21bd_manh_tab_nbsp": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai\tco  noi" + chr(0xA0) + "dung") + ".\n", None, V(d=1)),
                   "b21bd_manh_ngan_sau_chuan": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|  ab   ") + ".\n", None, V(v=1)),
                   "b21bd_manh_nguon_bien": ("a.md", "Theo r41 " + CT0("r41:1 #b2ddf1aa|  dong hai co") + ".\n", None, V(d=1))})
        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22) — thieu MOT o => DO.
        def o_r21(ten, doc):
            nhom, kieu = ten.split("_")[0][3:], ten.split("_")[1]; q = Q8 if kieu == "thang" else C8
            if nhom == "eof":
                cuoi = doc.rstrip("\n").rsplit("\n", 1)[-1]
                return {(kieu, "eof", doc.endswith("\n"), doc.endswith("\n\n"), cuoi.lstrip().startswith("|"), doc.count("\n\n") > 0 and not doc.endswith("\n"),
                         "r1" in doc, NL in doc)}
            if nhom == "td":
                tds = [l for l in doc.split("\n") if l.startswith("#")]
                that = [l for l in tds if re.fullmatch(r"#{1,6} .*", l) is not None and l[:7] != "#" * 7]
                return {(kieu, "td", tuple("r1" in l or "r2" in l for l in that), len(tds) != len(that), "\n\n" in doc.split(q)[0])} | {
                    (kieu, "muc", len(l) - len(l.lstrip("#"))) for l in tds}
            if nhom == "py":
                n_ = len(ast.literal_eval(doc[4:].strip()))
                return {(kieu, "py", n_ if 39 <= n_ <= 41 else "ngan" if n_ < 20 else "dai")}
            if nhom == "kt":
                g = doc[doc.index(q) + len(q):doc.index(NL)]
                return {(kieu, "kt", g, all(c_.isspace() for c_ in g))}
            if nhom == "md":
                mo = doc[len("Theo r1: "):doc.index(q)]; g = doc[doc.index(q) + len(q):doc.index(" " + NL)]
                return {(kieu, "md", len(mo), len(g), "".join(sorted(set(mo + g))), g == mo[::-1])}
            return set()
        can_r21 = set()
        for k in ("thang", "cong"):
            can_r21 |= {(k, "eof", nl, nhieu, bang, sau, tk, nh) for nl, nhieu, bang, sau, tk, nh in (
                        (False, False, False, False, True, False), (True, False, False, False, True, False), (True, True, False, False, True, False),
                        (False, False, False, True, True, False), (False, False, True, False, True, False), (True, False, True, False, True, False),
                        (False, False, False, False, True, True), (False, False, False, False, False, False))}
            can_r21 |= {(k, "td", seq, gia, cach) for seq, gia, cach in (((True, False), False, True), ((True, False), False, False),
                        ((False, True), False, True), ((False, True), False, False), ((True, True), False, True), ((True,), False, False),
                        ((True,), False, True), ((), True, True))} | {(k, "muc", m_) for m_ in (1, 2, 6, 7)}
            can_r21 |= {(k, "py", x_) for x_ in (39, 40, 41, "ngan", "dai")}
            can_r21 |= {(k, "kt", c_, True) for c_ in (" ", "\t", "\n", "\x0b", "\x0c", "\r", chr(0xA0), chr(0x2003), chr(0x3000),
                                                    chr(0x1680), chr(0x202F), chr(0x2028), chr(0x1C), chr(0xA0) + " ")} | {
                (k, "kt", c_, False) for c_ in (chr(0x200B), chr(0xAD), chr(0x2060))}
            can_r21 |= {(k, "md", L_, L_, ch, True) for L_ in range(1, 9) for ch in "*_"} | {
                (k, "md", a_, b_, ch, False) for L_ in range(1, 9) for ch in "*_" for a_, b_ in ((L_, L_ + 1), (L_ + 1, L_))} | {
                (k, "md", L_, L_, "*_", d_) for L_ in range(2, 9) for d_ in (True, False)}
        phu_r21 = set().union(*(o_r21(t_, rb(t_)) for t_ in list(ca) if t_.split("_")[0] in ("b21eof", "b21td", "b21py", "b21kt", "b21md")))
        hong += [f"PHU_R21: o chua co ca: {sorted(can_r21 - phu_r21, key=str)}"] if can_r21 - phu_r21 else []
        # Phu cua chuan/bo_dau tinh tu NGUON va manh da viet: khoang trang bien ca hai phia, nhieu dong, ky tu khong phai space.
        def o_ch():  # moi ca con tro: tinh tu CHINH cac dong nguon duoc tro va manh da viet
            o = set()
            for t_ in list(ca):
                if not t_.startswith(("b21ch_", "b21bd_")): continue
                doc_ = rb(t_)  # r22: manh lay tu BYTE DOC LAI
                m_ = re.search(r"r(\d+):(\d+)(?:-(\d+))? ", doc_); a_, b_ = int(m_.group(2)), int(m_.group(3) or m_.group(2))
                ds = (Path(t) / f"r{m_.group(1)}.md").read_text(encoding="utf-8").split("\n")[a_ - 1:b_]
                o |= {("nguon", len(ds) > 1, all(l[:1].isspace() for l in ds), all(l[-1:].isspace() for l in ds),
                       any(c_.isspace() and c_ != " " for l in ds for c_ in l.strip()))}
                mh = doc_.split("|", 1)[1].split(chr(0x27E7))[0]
                o |= {("manh", mh != mh.strip(), any(c_.isspace() and c_ != " " for c_ in mh.strip()), len(mh.strip()) >= 6)}
            return o
        can_ch = {("nguon", False, True, True, False), ("nguon", True, True, True, False), ("nguon", False, True, False, True),
                  ("manh", True, False, True), ("manh", False, True, True), ("manh", True, False, False)}
        hong += [f"PHU_CHUAN: o chua co ca: {sorted(can_ch - o_ch())}"] if can_ch - o_ch() else []
        # r22 (luot 17, F2): BANG BIEN B22 — mien con lai cua parser: pham vi dong `--ham` (dau/giua/cuoi, ham 1 dong/nhieu
        # dong, truoc/sau ham, chon/bo), manh con tro (thieu/rong/trang/duoi/dung nguong), nhieu con tro, bien dong nguon,
        # token rN hai phia (ASCII, Unicode, gach noi, dau/cuoi khoi), CODE (rong/nhieu dong/chua dong/hai cap; .py khong che),
        # lstrip bang/rao/tieu de. Ky vong VIET TAY; bam LITERAL: sha256("dong mot")[:8] = 2bf318fb.
        (Path(t) / "r44.md").write_bytes("dong mot\ndong hai co noi dung".encode("utf-8"))  # KHONG newline cuoi: dong 2 la phan tu cuoi
        (Path(t) / "r8.md").mkdir()  # thu muc mang ten nguon — khong phai tep
        S22 = "r1: " + Q2 + "abcdefgh" + Q2 + " va noi dung du dai de vuot bon muoi ky tu"
        assert len(S22) > 40
        SAI = CT0("r1:2 #00000000|hai co noi dung")
        ca.update({
            # (a) khoi_py — chuoi dai o dong DAU / GIUA / CUOI cua ham duoc chon; ham 1 dong va nhieu dong; ngay TRUOC / SAU ham.
            "b22py_mot_dong_chon": ("a.py", "def f(): " + repr(S22) + "\n", {"f"}, V(v=1)),
            "b22py_mot_dong_bo": ("a.py", "def g(): pass\ndef f(): " + repr(S22) + "\n", {"g"}, V()),
            "b22py_dau_chon": ("a.py", "def f(x=" + repr(S22) + "):\n    return x\n", {"f"}, V(v=1)),
            "b22py_giua_chon": ("a.py", "def f():\n    " + repr(S22) + "\n    return 1\n", {"f"}, V(v=1)),
            "b22py_cuoi_chon": ("a.py", "def f():\n    x = 1\n    " + repr(S22) + "\n", {"f"}, V(v=1)),
            "b22py_cuoi_bo_ham_sau_chon": ("a.py", "def f():\n    x = 1\n    " + repr(S22) + "\ndef g():\n    return 1\n", {"g"}, V()),
            "b22py_ngay_truoc_ham": ("a.py", repr(S22) + "\ndef f():\n    return 1\n", {"f"}, V()),
            "b22py_ngay_sau_ham": ("a.py", "def f():\n    return 1\n" + repr(S22) + "\n", {"f"}, V()),
            "b22py_khong_ham": ("a.py", "def f():\n    x = 1\n    " + repr(S22) + "\n", None, V(v=1)),
            "b22py_bytes": ("a.py", "X = " + repr(S22.encode("utf-8")) + "\n", None, V()),
            # (b) manh con tro — thieu / rong / chi khoang trang / duoi nguong / DUNG nguong 6; `*` bi bo, `_` KHONG bi bo.
            "b22ct_manh_thieu": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa") + ".\n", None, V(v=1)),
            "b22ct_manh_rong": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|") + ".\n", None, V(v=1)),
            "b22ct_manh_trang": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|   ") + ".\n", None, V(v=1)),
            "b22ct_manh_trang_la": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|\t" + chr(0xA0)) + ".\n", None, V(v=1)),
            "b22ct_manh_duoi_nguong": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai c") + ".\n", None, V(v=1)),
            "b22ct_manh_dung_nguong": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai co") + ".\n", None, V(d=1)),
            "b22ct_manh_nguong_sau_bo_sao": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|**hai co**") + ".\n", None, V(d=1)),
            "b22ct_manh_gach_duoi_giu": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|_hai co_") + ".\n", None, V(l=1)),
            # nhieu con tro trong cung khoi, MOI thu tu
            "b22ct_dung_roi_sai": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa|hai co noi dung") + " va " + SAI + ".\n", None, V(d=1, l=1)),
            "b22ct_sai_roi_dung": ("a.md", "Theo r1 " + SAI + " va " + CT0("r1:2 #b2ddf1aa|hai co noi dung") + ".\n", None, V(d=1, l=1)),
            "b22ct_hai_dung": ("a.md", "Theo r1 " + CT0("r1:1 #2bf318fb|dong mot") + " va " + CT0("r1:2 #b2ddf1aa|hai co noi dung") + ".\n", None, V(d=2)),
            # dang bam: chi 8 hex THUONG la con tro
            "b22ct_bam_hoa": ("a.md", "Theo r1 " + CT0("r1:2 #B2DDF1AA|hai co noi dung") + ".\n", None, V()),
            "b22ct_bam_7": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1a|hai co noi dung") + ".\n", None, V()),
            "b22ct_bam_9": ("a.md", "Theo r1 " + CT0("r1:2 #b2ddf1aa0|hai co noi dung") + ".\n", None, V()),
            # bien dong cua nguon: dong 1; dong CUOI cua nguon khong newline cuoi; khoang vuot cuoi 1 dong; nguon la thu muc
            "b22ct_dong_dau": ("a.md", "Theo r1 " + CT0("r1:1 #2bf318fb|dong mot") + ".\n", None, V(d=1)),
            "b22ct_dong_cuoi_nguon": ("a.md", "Theo r44 " + CT0("r44:2 #b2ddf1aa|hai co noi dung") + ".\n", None, V(d=1)),
            "b22ct_span_toi_cuoi_nguon": ("a.md", "Theo r44 " + CT0("r44:1-2 #0483e794|dong mot dong hai") + ".\n", None, V(d=1)),
            "b22ct_span_vuot_cuoi_1": ("a.md", "Theo r44 " + CT0("r44:1-3 #0483e794|dong mot dong hai") + ".\n", None, V(l=1)),
            "b22ct_nguon_la_thu_muc": ("a.md", "Theo r8 " + CT0("r8:1 #00000000|khong co tep nao") + ".\n", None, V(k=1)),
        })
        for kieu, q in (("thang", Q8), ("cong", C8)):
            # (c) token rN — ky tu hai phia: ASCII, Unicode (U+00E1), gach noi, dau/cuoi khoi; chu so Unicode (U+0663); `R` hoa.
            for ten, (doc, mong) in {"trai_ascii": ("Theo error1: {q}.\n", V()), "phai_ascii": ("Theo r1x: {q}.\n", V()),
                                     "trai_unicode": ("Ma " + chr(0xE1) + "r1: {q}.\n", V()), "phai_unicode": ("Theo r1" + chr(0xE1) + ": {q}.\n", V()),
                                     "trai_gach": ("Theo ma-r1: {q}.\n", V()), "phai_gach": ("Theo r1-r2: {q}.\n", V(v=1)),
                                     "dau_khoi": ("r1 viet {q}.\n", V(v=1)), "cuoi_khoi": ("Mo dau {q} theo r1\n", V(v=1)),
                                     "so_unicode": ("Theo r" + chr(0x663) + ": {q}.\n", V(v=1)), "hoa": ("Theo R1: {q}.\n", V())}.items():
                ca[f"b22rv_{kieu}_{ten}"] = ("a.md", doc.format(q=q), None, mong)
            # (d) CODE — cap rong, backtick qua dong, backtick chua dong, hai cap bao cau; .py KHONG che code.
            for ten, (doc, mong) in {"rong": ("Theo r1: ``{q}``.\n", V(v=1)), "nhieu_dong": ("Theo r1: `x\n{q}`.\n", V(v=1)),
                                     "chua_dong": ("Theo r1: `{q}.\n", V(v=1)), "hai_cap": ("Theo r1: `a` {q} `b`.\n", V(v=1))}.items():
                ca[f"b22code_{kieu}_{ten}"] = ("a.md", doc.format(q=q), None, mong)
            ca[f"b22code_{kieu}_py_khong_che"] = ("a.py", "X = " + repr("r1: `" + q + "` va noi dung du dai de vuot bon muoi ky tu") + "\n", None, V(v=1))
            # (e) khoi_md — lstrip cua bang/rao, bang thut roi bang, rao chua dong, tieu de thut/tab, dong chi khoang trang.
            for ten, (doc, mong) in {"bang_thut": ("Theo r1\n  | {q} |\n", V()), "bang_thut_roi_bang": ("  | r1 | x |\n| {q} | y |\n", V(v=1)),
                                     "rao_thut": ("  ```python\nr1: {q}\n  ```\n", V()), "rao_chua_dong": ("Theo r1:\n```\nr1 {q}\n", V()),
                                     "tieu_de_thut": ("  ## Nhan xet r1\n\n{q}.\n", V()), "tieu_de_tab": ("##\tNhan xet r1\n\n{q}.\n", V()),
                                     "dong_chi_khoang_trang": ("Theo r1:\n   \nMo {q}.\n", V())}.items():
                ca[f"b22ls_{kieu}_{ten}"] = ("a.md", doc.format(q=q), None, mong)
        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca, KHONG qua regex nao cua cong.
        def o_r22(ten, doc):
            nhom = ten.split("_")[0]; kieu = ten.split("_")[1]
            if nhom == "b22py":
                goc = ast.parse(doc); s_ = [n for n in ast.walk(goc) if isinstance(n, ast.Constant) and isinstance(n.value, str) and 40 < len(n.value)]
                if not s_: return {("py", "khong_str")}
                if ca[ten][2] is None: return {("py", "khong_ham")}
                s_ = s_[0].lineno
                return {("py", tuple((f.end_lineno > f.lineno, "truoc" if s_ < f.lineno else "sau" if s_ > f.end_lineno else "dau" if s_ == f.lineno
                                      else "cuoi" if s_ == f.end_lineno else "giua", f.name in ca[ten][2]) for f in goc.body if isinstance(f, ast.FunctionDef)))}
            if nhom == "b22ct":
                o = []
                for x in doc.split(chr(0x27E6))[1:]:
                    trong = x.split(chr(0x27E7))[0]; dau, manh = (trong.split("|", 1) + [None])[:2]
                    rv, h = dau.split(" #"); n_, ab = rv[1:].split(":"); a_, b_ = (ab.split("-") + [ab])[:2]
                    p_ = Path(t) / f"r{n_}.md"; so = len(p_.read_bytes().decode("utf-8").split("\n")) if p_.is_file() else None
                    hd = "sai" if h == "0" * 8 else "dung_dang" if len(h) == 8 and set(h) <= set("0123456789abcdef") else f"dang_{len(h)}_{h.isupper()}"
                    ml = None if manh is None else len(" ".join(manh.replace("*", "").split()))
                    mk = ("thieu" if manh is None else "rong" if manh == "" else "trang" if not manh.strip() else "duoi" if ml < 6 else "nguong" if ml == 6 else "dai",
                          "*" in (manh or ""), "_" in (manh or ""), any(c.isspace() and c != " " for c in (manh or "")))
                    bien = "thu_muc" if so is None else (int(a_) == 1, int(b_) == so, int(b_) > so)
                    o.append((hd, mk, bien))
                return {("ct", tuple(o))}
            if nhom == "b22rv":
                i = next(i for i in range(len(doc) - 1) if doc[i] in "rR" and doc[i + 1].isdigit()); j = i + 1
                while j < len(doc) and doc[j].isdigit(): j += 1
                lop = lambda c: ("bien" if c in ("", "\n") else "ascii_chu" if c.isascii() and (c.isalnum() or c == "_") else "unicode_chu" if c.isalnum()
                                 else "gach" if c == "-" else "khac")
                return {(kieu, "rv", lop(doc[i - 1:i]), lop(doc[j:j + 1]), doc[i], doc[i + 1:j].isascii())}
            if nhom == "b22code":
                bt = [l.count("`") for l in doc.split("\n")]
                return {(kieu, "code", ca[ten][0].endswith(".py"), "``" in doc, tuple(b % 2 for b in bt if b), sum(bt))}
            if nhom == "b22ls":  # moi dong thut le / tieu de / chi khoang trang: (chi so, phan thut, ky tu dau, ky tu sau day `#`)
                L_ = doc.split("\n")
                return {(kieu, "ls", tuple((i, l[:len(l) - len(l.lstrip())], l.lstrip()[:1], l.lstrip("#")[:1] if l.startswith("#") else "")
                                           for i, l in enumerate(L_) if (l != "" and l.strip() == "") or l[:1] in (" ", "#")),
                         sum(l.lstrip()[:3] == "```" for l in L_) % 2)}
            return set()
        CAN_R22 = {("py", x) for x in ("khong_ham", "khong_str")} | {("py", x) for x in (
            ((False, "dau", True),), ((False, "sau", True), (False, "dau", False)), ((True, "dau", True),), ((True, "giua", True),),
            ((True, "cuoi", True),), ((True, "cuoi", False), (True, "truoc", True)), ((True, "truoc", True),), ((True, "sau", True),))}
        D, S_ = ("dung_dang", ("dai", False, False, False), (False, False, False)), ("sai", ("dai", False, False, False), (False, False, False))
        CAN_R22 |= {("ct", x) for x in (
            (("dung_dang", ("thieu", False, False, False), (False, False, False)),), (("dung_dang", ("rong", False, False, False), (False, False, False)),),
            (("dung_dang", ("trang", False, False, False), (False, False, False)),), (("dung_dang", ("trang", False, False, True), (False, False, False)),), (("dung_dang", ("duoi", False, False, False), (False, False, False)),),
            (("dung_dang", ("nguong", False, False, False), (False, False, False)),), (("dung_dang", ("nguong", True, False, False), (False, False, False)),),
            (("dung_dang", ("dai", False, True, False), (False, False, False)),), (D, S_), (S_, D), ((("dung_dang", ("dai", False, False, False), (True, False, False))), D),
            (("dang_8_True", ("dai", False, False, False), (False, False, False)),), (("dang_7_False", ("dai", False, False, False), (False, False, False)),),
            (("dang_9_False", ("dai", False, False, False), (False, False, False)),), (("dung_dang", ("dai", False, False, False), (True, False, False)),),
            (("dung_dang", ("dai", False, False, False), (False, True, False)),), (("dung_dang", ("dai", False, False, False), (True, True, False)),),
            (("dung_dang", ("dai", False, False, False), (True, False, True)),), (("sai", ("dai", False, False, False), "thu_muc"),))}
        for k in ("thang", "cong"):
            CAN_R22 |= {(k, "rv", a_, b_, r_, s_) for a_, b_, r_, s_ in (
                ("ascii_chu", "khac", "r", True), ("khac", "ascii_chu", "r", True), ("unicode_chu", "khac", "r", True), ("khac", "unicode_chu", "r", True),
                ("gach", "khac", "r", True), ("khac", "gach", "r", True), ("bien", "khac", "r", True), ("khac", "bien", "r", True),
                ("khac", "khac", "r", False), ("khac", "khac", "R", True))}
            CAN_R22 |= {(k, "code", False, True, (0,), 4), (k, "code", False, False, (1, 1), 2), (k, "code", False, False, (1,), 1),
                        (k, "code", False, False, (0,), 4), (k, "code", True, False, (0,), 2)}
            CAN_R22 |= {(k, "ls", x, r_) for x, r_ in (
                (((1, "  ", "|", ""),), 0), (((0, "  ", "|", ""),), 0), (((0, "  ", "`", ""), (2, "  ", "`", "")), 0), ((), 1),
                (((0, "  ", "#", ""),), 0), (((0, "", "#", "\t"),), 0), (((1, "   ", "", ""),), 0))}
        phu_r22 = set().union(*(o_r22(t_, rb(t_)) for t_ in list(ca) if t_.startswith("b22")))
        hong += [f"PHU_R22: o chua co ca: {sorted(CAN_R22 - phu_r22, key=str)}"] if CAN_R22 - phu_r22 else []
        # BANG NHANH -> CA (§0.21): MOI nhanh/bien cua parser tro toi >= 1 ca CO THAT, hoac mang ly do LOAI_TRU ghi ro.
        # May kiem hai dieu (sau khi sinh ca CLI): moi ten ca ton tai; khong nhanh nao rong va khong nhanh nao thieu ly do.
        LT = lambda x: "LOAI_TRU: " + x
        BANG_NHANH = {
            "CT.rN_mot_chu_so": ("duong",), "CT.rN_nhieu_chu_so": ("rv_hai_chu_so_con_tro",),
            "CT.dong_mot_chu_so": ("duong",), "CT.dong_nhieu_chu_so": ("dong_hai_chu_so_con_tro", "span_hai_chu_so"),
            "CT.khoang_vang": ("duong",), "CT.khoang_co": ("span_nhieu_dong_duong", "b22ct_span_toi_cuoi_nguon"),
            "CT.bam_8_hex_thuong": ("duong",), "CT.bam_hex_hoa": ("b22ct_bam_hoa",), "CT.bam_7_hex": ("b22ct_bam_7",), "CT.bam_9_hex": ("b22ct_bam_9",),
            "CT.manh_thieu": ("thieu_manh", "b22ct_manh_thieu"), "CT.manh_rong": ("b22ct_manh_rong",),
            "CT.manh_chi_khoang_trang": ("b22ct_manh_trang", "b22ct_manh_trang_la"),
            "CT.manh_duoi_nguong": ("manh_4_am", "manh_5_am", "b22ct_manh_duoi_nguong", "b21bd_manh_ngan_sau_chuan"),
            "CT.manh_dung_nguong": ("manh_6_duong", "b22ct_manh_dung_nguong", "b22ct_manh_nguong_sau_bo_sao"),
            "CT.nhieu_con_tro_moi_thu_tu": ("b22ct_dung_roi_sai", "b22ct_sai_roi_dung", "b22ct_hai_dung"),
            "NHAN.nhan_hop_le_ca_6": ("moi_nhan_hop_le",), "NHAN.nhan_khong_hop_le": ("nhan_khong_hop_le", "kn_nhan_sai_roi_dung"),
            "NHAN.markup_dong_1_den_8": ("b21md_thang_sao_1_1", "b21md_thang_gach_8_8", "b21md_cong_sao_8_8"),
            "NHAN.khoang_trang_moi_loai": ("kn_thang_rong", "kn_thang_tab", "kn_thang_xuong_dong", "b21kt_thang_nbsp", "b21kt_thang_ls", "b21kt_cong_fs"),
            "NHAN.khong_phai_khoang_trang": ("b21kt_thang_zwsp", "b21kt_thang_shy", "b21kt_thang_wj", "kn_thang_chu", "kn_thang_dau0"),
            "NHAN.ngay_sau_cau_khong_tim_xa": ("kn_thang_noi_dung_xen", "nhan_xau_truoc_nhan_dung", "kn_nhan_truoc_cau"),
            "MO.khong_markup": ("kn_thang_cach",), "MO.markup_1_den_8": ("b21md_thang_sao_1_1", "b21md_thang_sao_8_8", "dd_thang_nam_nam"),
            "MO.markup_tron_dao_nguoc": ("b21md_thang_tron_2_dao", "b21md_thang_tron_8_khong_dao", "cm_thang_khac_loai_sai_thu_tu"),
            "MO.do_dai_lech": ("b21md_thang_sao_1_2", "b21md_thang_sao_2_1", "dd_thang_bon_ba", "cm_thang_dai_ngan"),
            "MO.vi_tri_cau": ("vt_thang_dau_khoi_sao", "vt_thang_thut_le_sao_thieu_mo", "vt_thang_sau_dong_ket_markup_sao_doi_lech"),
            "MO.tren_k_hay_kc": LT("tuong duong da chung minh (mo_masked, luot 16 va 17)"),
            "Q.thang_7_8_9": ("trich_7_thang", "trich_8_thang", "trich_9_thang"), "Q.cong_7_8_9": ("trich_7_cong", "trich_8_cong", "trich_9_cong"),
            "Q.vat_dong": ("vat_dong", "ngoac_cong_vat_dong"), "Q.nhieu_lan_cung_dong": ("lan_thang_dung_roi_thieu_mo", "lan_cong_khong_roi_co_nhan"),
            "Q.luoi_hay_tham": LT("tuong duong da chung minh (new_q_greedy, new_q_curly_greedy, luot 17)"),
            "Q.thu_tu_duyet": LT("tuong duong da chung minh (l16_reverse_q, luot 16)"),
            "Q.cong_long_thang": LT("ngoai pham vi — ngoac cong long ngoac thang"),
            "CODE.mot_cap": ("trong_code", "bc_thang_cau_trong_code"), "CODE.cap_rong": ("b22code_thang_rong", "b22code_cong_rong"),
            "CODE.qua_dong": ("b22code_thang_nhieu_dong", "b22code_cong_nhieu_dong"), "CODE.chua_dong": ("b22code_thang_chua_dong", "b22code_cong_chua_dong"),
            "CODE.hai_cap": ("b22code_thang_hai_cap", "bc_thang_code_xen"),
            "CODE.nhieu_backtick": LT("code span nhieu backtick (CommonMark) ngoai pham vi; parser dong bang chi ghep backtick don"),
            "che_code.giu_do_dai": ("bc_thang_code_truoc_cau", "bc_thang_markup_mo_trong_code"),
            "che_code.chi_md": ("b22code_thang_py_khong_che", "b22code_cong_py_khong_che"),
            "RV.trai_ascii": ("b22rv_thang_trai_ascii", "rv_trong_tu_khong_phai_token"), "RV.trai_unicode": ("b22rv_thang_trai_unicode", "b22rv_cong_trai_unicode"),
            "RV.trai_gach": ("b22rv_thang_trai_gach", "rv_sau_gach_noi"), "RV.trai_dau_khoi": ("b22rv_thang_dau_khoi", "vat_dong"),
            "RV.phai_ascii": ("b22rv_thang_phai_ascii",), "RV.phai_unicode": ("b22rv_thang_phai_unicode", "b22rv_cong_phai_unicode"),
            "RV.phai_gach": ("b22rv_thang_phai_gach", "b22rv_cong_phai_gach"), "RV.phai_cuoi_khoi": ("b22rv_thang_cuoi_khoi", "b22rv_cong_cuoi_khoi"),
            "RV.chu_so_nhieu": ("rv_hai_chu_so_token",), "RV.chu_so_unicode": ("b22rv_thang_so_unicode",), "RV.chu_hoa": ("b22rv_thang_hoa",),
            "RV.token_o_tieu_de": ("chi_tieu_de", "b21td_thang_co_cach"),
            "RV.ba_chu_so_tro_len": LT("revision/dong >= 3 chu so ngoai pham vi"),
            "khoi_md.rao_mo_dong": ("rao_code_bo_qua", "rao_code_ngoai_rao_van_do", "rao_3_co_thong_tin", "rao_4_co_thong_tin"),
            "khoi_md.rao_thut": ("b22ls_thang_rao_thut", "b22ls_cong_rao_thut"), "khoi_md.rao_chua_dong": ("b22ls_thang_rao_chua_dong",),
            "khoi_md.rao_nga": LT("rao ~~~ ngoai pham vi"),
            "khoi_md.bang_tach_doan": ("bang_tach_khoi_doan", "bang_tu_nhac_ban"), "khoi_md.bang_thut": ("b22ls_thang_bang_thut", "b22ls_cong_bang_thut"),
            "khoi_md.bang_dong_truoc_thut": ("b22ls_thang_bang_thut_roi_bang",), "khoi_md.bang_cuoi_tep": ("b21eof_thang_bang_khong_nl", "b21eof_thang_bang_co_nl"),
            "khoi_md.tieu_de_1_den_6": tuple(f"tieu_de_cap_{n}" for n in range(1, 7)), "khoi_md.tieu_de_7": ("bay_thang_khong_phai_tieu_de", "b21td_thang_muc7_khong_la_tieu_de"),
            "khoi_md.tieu_de_thieu_cach": ("b21td_thang_thieu_cach_khong_la_tieu_de", "gach_so_khong_phai_tieu_de"),
            "khoi_md.tieu_de_tab": ("b22ls_thang_tieu_de_tab",), "khoi_md.tieu_de_thut": ("b22ls_thang_tieu_de_thut",),
            "khoi_md.chuyen_tieu_de": ("b21td_thang_co_roi_khong", "b21td_thang_khong_roi_co", "b21td_thang_co_roi_co", "b21td_thang_co_roi_rao"),
            "khoi_md.setext": LT("tieu de Setext ngoai pham vi"), "khoi_md.danh_sach_long": LT("danh sach long ngoai pham vi"),
            "khoi_md.dong_trong": ("b21eof_thang_hai_khoi_khong_nl", "chi_tieu_de"), "khoi_md.dong_chi_khoang_trang": ("b22ls_thang_dong_chi_khoang_trang",),
            "khoi_md.eof": ("b21eof_thang_mot_khong_nl", "b21eof_thang_mot_co_nl", "b21eof_thang_mot_nhieu_nl", "b21eof_thang_sau_khoi_khong_nl"),
            "khoi_md.so_dong_dau_khoi": LT("chi vao dong chan doan in ra, khong vao vecto dem"),
            "khoi_py.nguong_40": ("b21py_thang_39", "b21py_thang_40", "b21py_thang_41", "b21py_cong_60"),
            "khoi_py.khong_ham": ("py_docstring", "b22py_khong_ham"), "khoi_py.chuoi_khong_phai_str": ("b22py_bytes",),
            "khoi_py.ham_mot_dong": ("b22py_mot_dong_chon", "b22py_mot_dong_bo"),
            "khoi_py.dong_dau_ham": ("b22py_dau_chon", "b22py_mot_dong_chon"), "khoi_py.dong_giua_ham": ("b22py_giua_chon", "py_ham"),
            "khoi_py.dong_cuoi_ham": ("b22py_cuoi_chon",), "khoi_py.ngay_truoc_ham": ("b22py_ngay_truoc_ham", "b22py_cuoi_bo_ham_sau_chon"),
            "khoi_py.ngay_sau_ham": ("b22py_ngay_sau_ham", "b22py_mot_dong_bo"), "khoi_py.chon_bo": ("py_ham", "b22py_mot_dong_bo", "b22py_cuoi_bo_ham_sau_chon"),
            "khoi_py.ham_khong_ton_tai": ("cli_ham_truoc_zz", "cli_ham_sau_zz"), "khoi_py.tach_doan": ("py_tach_doan",),
            "khoi_py.fullmatch_du": LT("khong the dat — doan chi khoang trang da bi `doan.strip()` loai truoc"),
            "khoi_py.async_long_nhau": LT("async def / ham long nhau ngoai pham vi quyet dinh hien hanh"),
            "khoi_py.f_string_chuoi_noi": LT("f-string / chuoi noi ngoai pham vi"),
            "khoi_py.so_dong_chan_doan": LT("chi vao dong chan doan in ra, khong vao vecto dem"),
            "chuan.bien_va_gop": ("b21ch_bien_hai_phia", "b21ch_nhieu_dong", "b21ch_tab_nbsp_giua"),
            "bo_dau.bo_sao_backtick": ("manh_bo_sao", "manh_bo_backtick", "b22ct_manh_nguong_sau_bo_sao"),
            "bo_dau.giu_gach_duoi": ("b22ct_manh_gach_duoi_giu",), "bo_dau.gop_va_cat": ("manh_gop_khoang_trang", "b21bd_manh_bien", "b21bd_manh_tab_nbsp"),
            "nguon.co_tep": ("duong",), "nguon.khong_co": ("thieu_tep", "cli_co_truoc_thieu.md"), "nguon.la_thu_muc": ("b22ct_nguon_la_thu_muc",),
            "nguon.khong_newline_cuoi": ("b22ct_dong_cuoi_nguon", "b22ct_span_vuot_cuoi_1"), "nguon.mau_ten": ("cli_co_truoc_sach.md",),
            "nguon.cr_crlf": LT("read_text dich CR/CRLF thanh LF truoc parser; ca b21kt_*_cr chi khoa TANG TEP, o parser tuong duong LF"),
            "nguon.encoding_khac": LT("encoding khac UTF-8 ngoai pham vi"),
            "kiem.khong_do_duoc": ("thieu_tep", "b22ct_nguon_la_thu_muc"),
            "kiem.pham_vi": ("pv_dau_0", "pv_dao", "ngoai_pham_vi", "pv_cuoi_vuot_mot_phan", "b22ct_dong_dau", "b22ct_dong_cuoi_nguon", "b22ct_span_vuot_cuoi_1"),
            "kiem.bam_lech": ("sai_dong", "sai_bam_manh_van_khop"), "kiem.manh_lech": ("sai_manh_dung_bam", "b22ct_manh_gach_duoi_giu"),
            "kiem.manh_or_rong": LT("`manh or \"\"` khong the dat (manh da khac None o nhanh truoc)"),
            "kiem.md_hay_py": ("py_docstring", "b22code_thang_py_khong_che"), "kiem.co_nhan": ("trich_co_nhan",), "kiem.vi_pham": ("trich_khong_nhan",),
            "main.tu_kiem": LT("chinh lenh dang chay"), "main.co_truoc_sau_xen": ("cli_co_truoc_sach.md", "cli_co_sau_sach.md", "cli_co_xen_sach.md"),
            "main.ham": ("cli_ham_truoc_a", "cli_ham_sau_a,b", "cli_khong_ham_h"), "main.cong_don_nhieu_tep": ("cli_co_sau_lech.md+lech2.md+vipham.md", "cli_co_truoc_thieu.md+sach.md+thieu.md",
                                        "cli_co_sau_lech.md+lech2.md+nhan.md+nhan_gach.md+sach.md+thieu.md+vipham.md"),
            "main.rc": ("cli_co_truoc_sach.md", "cli_co_truoc_lech.md"),
            "main.cong_don_cung_cot": ("cli_co_xen_sach.md+sach.md", "cli_co_truoc_vipham.md+vipham.md"),
            "main.sinh_tim": LT("lenh sinh/tim ngoai pham vi tu kiem"), "main.lenh_la": LT("lenh khong hop le ngoai pham vi"),
            "main.co_lap_thieu": LT("co lap / thieu gia tri / --nguon khong ton tai ngoai pham vi"),
        }
        for ten, (tep, doc, ham, mong) in ca.items():
            p = tep_ca(ten)  # r22: CHINH tep ma phep phu da doc lai o tren
            # lop hai, DOC LAI LAN NUA doc lap voi RB: byte tren dia phai BANG y dinh (EOF/CR/khoang trang) truoc moi chuan hoa
            if p.read_bytes() != doc.encode("utf-8"): hong.append(f"{ten}: GHI_LECH byte tren dia khac y dinh"); continue
            d = kiem(t, "r{n}.md", p, ham)
            thuc = (d["DUNG"], d["LECH"], d["KHONG_DO_DUOC"], d["VI_PHAM"], d["CO_NHAN"])
            if thuc != mong: hong.append(f"{ten}: mong {mong}, thuc {thuc}")
        # HOP DONG CLI — bang co tham quyen o dac ta r15 §0.14; cac ca SINH tu bang (to hop), khong liet ke tay.
        # Moi tep mau mang VEC TO ky vong viet tay (DUNG, LECH, KHONG_DO_DUOC, VI_PHAM, CO_NHAN); ky vong cua mot lan chay
        # nhieu tep = TONG tung phan tu; rc ky vong = 1 khi LECH + KHONG_DO_DUOC + VI_PHAM > 0. Oracle chi cong va so sanh,
        # khong goi `kiem`/`main`/regex nao cua cong. Nguon CLI dung MAU TEN RIENG (`spec-r{n}.txt`) de `--mau` co rang.
        import itertools, subprocess as _sp
        nc = Path(t) / "nguon_cli"; nc.mkdir()
        (nc / "spec-r3.txt").write_text("".join(f"dong so {i} co noi dung\n" for i in range(1, 13)), encoding="utf-8")
        dc = Path(t) / "cli"; dc.mkdir()
        TEP_CLI = {
            "sach.md": ("Theo r3 " + CT0("r3:12 #ab858a93|so 12 co noi dung") + ".\n", (1, 0, 0, 0, 0)),
            "lech.md": ("Theo r3 " + CT0("r3:12 #00000000|so 12 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "lech2.md": ("Theo r3 " + CT0("r3:11 #00000000|so 11 co noi dung") + ".\n", (0, 1, 0, 0, 0)),
            "thieu.md": ("Theo r9 " + CT0("r9:1 #00000000|khong co tep nao") + ".\n", (0, 0, 1, 0, 0)),
            "vipham.md": ("Theo r1: " + Q8 + ".\n", (0, 0, 0, 1, 0)),
            "nhan.md": ("Theo r1: " + Q8 + " " + chr(0x27E6) + "nguon:ma" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
            "nhan_gach.md": ("Theo r1: _" + Q8 + "_ " + chr(0x27E6) + "nguon:issue" + chr(0x27E7) + ".\n", (0, 0, 0, 0, 1)),
        }
        for ten, (noi, _v) in TEP_CLI.items(): (dc / ten).write_text(noi, encoding="utf-8")
        COT = ("DUNG", "LECH", "KHONG_DO_DUOC", "VI_PHAM", "CO_NHAN")
        CO = ["--nguon", str(nc), "--mau", "spec-r{n}.txt"]
        VI_TRI = {"co_truoc": lambda co, tep: co + tep, "co_sau": lambda co, tep: tep + co,
                  "co_xen": lambda co, tep: tep[:1] + co + tep[1:]}
        ds_tep = sorted(TEP_CLI)
        to_hop = [(x,) for x in ds_tep] + list(itertools.permutations(ds_tep, 2)) + [
            ("lech.md", "lech2.md", "vipham.md"), ("sach.md", "nhan.md", "nhan_gach.md"), ("thieu.md", "sach.md", "thieu.md"),
            tuple(ds_tep)]
        to_hop += [("sach.md", "sach.md"), ("vipham.md", "vipham.md")]  # r22: hai tep CUNG cot — tong, khong phai max
        cli = {}
        for so, bo in enumerate(to_hop):
            vt = list(VI_TRI)[so % 3] if len(bo) > 1 else None
            for v in ([vt] if vt else list(VI_TRI)):
                mong = tuple(sum(TEP_CLI[x][1][c] for x in bo) for c in range(5))
                cli[f"cli_{v}_{'+'.join(bo)}"] = (VI_TRI[v](CO, [str(dc / x) for x in bo]), int(sum(mong[1:4]) > 0), mong)
        # --ham: tep 5 ham, XAU = {a, c, e}; ky vong VI_PHAM = so ten trong danh sach thuoc XAU (ten la khong tinh).
        XAU = {"a", "c", "e"}
        (dc / "h.py").write_text("".join(f"def {n}():\n    " + Q2 * 3 + f"Ham {n} nhac r1 " + (Q8 + " khong nhan" if n in XAU else "va khong trich gi")
                                 + ", du dai de qua nguong bon muoi.\n    " + Q2 * 3 + "\n\n\n" for n in "abcde"), encoding="utf-8")
        # r16 (luot 11): vi tri TUNG co la mot truc RIENG, tach khoi noi dung danh sach ham — moi danh sach x `--ham`
        # truoc / sau chinh tep; `--nguon`/`--mau` luan phien truoc / sau.
        for so, ds_ham in enumerate(("a", "b", "c", "e", "a,b", "b,c", "d,e", "b,c,d", "d,c,b", "b,zz,d", "zz", "a,b,c,d,e", "b,d")):
            vi = len(set(ds_ham.split(",")) & XAU)
            for vt_ham, tep in (("ham_truoc", ["--ham", ds_ham, str(dc / "h.py")]), ("ham_sau", [str(dc / "h.py"), "--ham", ds_ham])):
                cli[f"cli_{vt_ham}_{ds_ham}"] = ((CO + tep) if so % 2 == 0 else (tep + CO), int(vi > 0), (0, 0, 0, vi, 0))
        cli["cli_khong_ham_h"] = (CO + [str(dc / "h.py")], 1, (0, 0, 0, 3, 0))
        # KIEM PHU BANG MAY tren argv DA SINH (khong tren y dinh): moi o cua bang §0.14 phai co >= 1 ca. Vi tri cua moi co
        # tinh theo chi so trong argv so voi cac TEP (doi so khong phai co, khong phai gia tri cua co).
        def o_cua(doi):
            tep_i, co_i, i = [], {}, 0
            while i < len(doi):
                if doi[i] in ("--nguon", "--mau", "--ham"): co_i[doi[i]] = i; i += 2
                else: tep_i.append(i); i += 1
            vt = lambda i: "truoc" if i < tep_i[0] else "sau" if i > tep_i[-1] else "xen"
            return {("so_tep", len(tep_i))} | {(f"vi_tri{c}", vt(i)) for c, i in co_i.items()}
        can = ({("so_tep", n) for n in (1, 2, 3, 7)} | {(f"vi_tri{c}", v) for c in ("--nguon", "--mau") for v in ("truoc", "sau", "xen")}
               | {("vi_tri--ham", v) for v in ("truoc", "sau")})
        co_phu = set().union(*(o_cua(doi) for doi, _r, _m in cli.values()))
        if can - co_phu: hong.append(f"PHU_BANG: o chua co ca: {sorted(can - co_phu)}")
        for ten, (doi, rc_mong, mong) in cli.items():
            r = _sp.run([sys.executable, "-B", str(Path(__file__).resolve()), "kiem", *doi], capture_output=True, text=True)
            tong = [x for x in r.stdout.splitlines() if x.startswith("TONG ")]
            d = ast.literal_eval(tong[0][5:]) if len(tong) == 1 else {}
            thuc = (r.returncode, len(tong), tuple(d.get(k) for k in COT))
            if thuc != (rc_mong, 1, mong): hong.append(f"{ten}: mong {(rc_mong, 1, mong)}, thuc {thuc}")
        khong_co = sorted({x for v in BANG_NHANH.values() if not isinstance(v, str) for x in v} - set(ca) - set(cli))
        if khong_co: hong.append(f"BANG_NHANH: tro toi ca khong ton tai {khong_co}")
        if [k for k, v in BANG_NHANH.items() if not v or (isinstance(v, str) and not v.startswith("LOAI_TRU: "))]:
            hong.append("BANG_NHANH: nhanh khong co ca va khong co ly do loai tru")
        n_ca = len(ca) + len(cli)
        print("TU_KIEM", "DAT" if not hong else f"HONG {hong}", f"{n_ca - len(hong)}/{n_ca}", f"(truc tiep {len(ca)}, CLI {len(cli)})")
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

## Phụ lục P.1 — bộ chạy đột biến r22, danh sách LITERAL, §0.21 (MỚI ở r22, nguyên văn)

Tái lập tập đột biến của §0.21 mà không cần tệp nào ngoài đặc tả. Trích khối Phụ lục P thành `con_tro.py`, và khối dưới thành `dot_bien_r22.py`, rồi chạy `python3 -B dot_bien_r22.py con_tro.py 8`. sha256 của khối mã dưới (không kể dòng rào): `f4a35d24c09ef3a0e7114d57e6f3896a45302a674991058d2f97b577cc9311a8`.

```python
"""Bo chay dot bien r22 (#574) cho cong con tro v13 — LITERAL, tai lap khong can tep nao ngoai dac ta.
Moi dot bien: moi neo phai khop DUNG 1 lan (khong thi NEO_HONG, khong chay); ghi ban sao vao MOT thu muc tam rieng, chay
MOT tien trinh `python -B con_tro.py tu-kiem` voi PYTHONDONTWRITEBYTECODE=1, doc `returncode` TRUC TIEP, xoa thu muc.
Nhom ten: rv: = recipe verdict luot 10–17 PR #588 (dau `!` da khoi phuc); neo_lai: = recipe cu neo lai tren parser hien
hanh; g22: = ghi/doc lai; g21:/g20: = bo sinh cu dung lai; bo: = bo MOT ca B22 (chi phep phu bat).
Dung: python dot_bien_r22.py CON_TRO.py [SO_LUONG_SONG_SONG]"""
import os, shutil, subprocess, sys, tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
DOT_BIEN = [
    ('rv:empty_close', [('n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1]', '(not n.group(1) or n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1])')]),
    ('rv:gen_code_xen', [('for lop, (mau, cuc) in BIEN_CODE.items(): ca[', 'for lop, (mau, cuc) in ((l, v) for l, v in BIEN_CODE.items() if l != "code_xen"): ca[')]),
    ('rv:gen_curly', [('for kieu, q in (("thang", Q8), ("cong", C8)):\n            for lop, (mo, kn, cuc) in CAP_MARKUP.items():', 'for kieu, q in (("thang", Q8),):\n            for lop, (mo, kn, cuc) in CAP_MARKUP.items():')]),
    ('rv:gen_missing_single', [('for lop, (mo, kn, cuc) in CAP_MARKUP.items(): ca[', 'for lop, (mo, kn, cuc) in ((l, v) for l, v in CAP_MARKUP.items() if not (l.startswith("thieu_mo") and len(v[1].strip()) == 1)): ca[')]),
    ('rv:gen_no_7', [(',\n            tuple(ds_tep)]', ']')]),
    ('rv:gen_no_ham_after', [('(("ham_truoc", ["--ham", ds_ham, str(dc / "h.py")]), ("ham_sau", [str(dc / "h.py"), "--ham", ds_ham]))', '(("ham_truoc", ["--ham", ds_ham, str(dc / "h.py")]),)')]),
    ('rv:gen_no_mau_xen', [('lambda co, tep: tep[:1] + co + tep[1:]', 'lambda co, tep: co[2:] + tep[:1] + co[:2] + tep[1:]')]),
    ('rv:gen_wrong_single', [('for lop, (mo, kn, cuc) in CAP_MARKUP.items(): ca[', 'for lop, (mo, kn, cuc) in ((l, v) for l, v in CAP_MARKUP.items() if not (l.startswith("khac_loai") and len(v[0]) == 1)): ca[')]),
    ('rv:l10_drop_cli_label', [('tong[k] = tong.get(k, 0) + v', 'tong[k] = tong.get(k, 0) + (0 if k == "CO_NHAN" else v)')]),
    ('rv:l10_first_file', [('for tep in rest:', 'for tep in rest[:1]:')]),
    ('rv:l10_fixed_mau', [('dir_, mau = co["--nguon"], co["--mau"]', 'dir_, mau = co["--nguon"], "r{n}.md"')]),
    ('rv:l10_ham_endpoints', [('set(co["--ham"].split(","))', '{co["--ham"].split(",")[0], co["--ham"].split(",")[-1]}')]),
    ('rv:l10_label_no_underscore', [('[*_]*\\s*⟦nguon:', '[*]*\\s*⟦nguon:')]),
    ('rv:l10_last_file', [('for tep in rest:', 'for tep in rest[-1:]:')]),
    ('rv:l10_option_after_file', [('if a[i] in ("--nguon", "--mau", "--ham"):', 'if not rest and a[i] in ("--nguon", "--mau", "--ham"):')]),
    ('rv:l10_sum_overwrite', [('tong[k] = tong.get(k, 0) + v', 'tong[k] = v')]),
    ('rv:l11_ham_after_file', [('if a[i] in ("--nguon", "--mau", "--ham"):', 'if a[i] in ("--nguon", "--mau") or (a[i] == "--ham" and not rest):')]),
    ('rv:l11_sum_max_dung_vipham', [('tong[k] = tong.get(k, 0) + v', 'tong[k] = max(tong.get(k, 0), v) if k in ("DUNG", "VI_PHAM") else tong.get(k, 0) + v')]),
    ('rv:l12_nhan_search', [('NHAN.match(k, m.end())', 'NHAN.search(k, m.end())')]),
    ('rv:l14_masked_gap', [('NHAN.match(k, m.end())', 'NHAN.match(kc, m.end())')]),
    ('rv:l16_chuan_no_strip', [('x.strip()) for x in ds', 'x) for x in ds')]),
    ('rv:l16_heading_stale', [('td = l; continue', 'td = td or l; continue')]),
    ('rv:l16_md_no_final_flush', [('day(); return kq', 'return kq')]),
    ('rv:l16_mo_bound5', [('MO = re.compile(r"[*_]*\\Z")', 'MO = re.compile(r"[*_]{0,5}\\Z")')]),
    ('rv:l16_nhan_bound5', [('NHAN = re.compile(r"([*_]*)', 'NHAN = re.compile(r"([*_]{0,5})')]),
    ('rv:l16_py_all_strings', [('len(n.value) > 40', 'len(n.value) > 0')]),
    ('rv:l16_space_tab_newline', [('([*_]*)\\s*⟦nguon:', '([*_]*)[ \\t\\n]*⟦nguon:')]),
    ('rv:l9_cli_ignore_lech', [('tong["LECH"] == tong["VI_PHAM"] == tong["KHONG_DO_DUOC"] == 0', 'tong["VI_PHAM"] == tong["KHONG_DO_DUOC"] == 0')]),
    ('rv:l9_cli_ignore_missing', [('tong["LECH"] == tong["VI_PHAM"] == tong["KHONG_DO_DUOC"] == 0', 'tong["LECH"] == tong["VI_PHAM"] == 0')]),
    ('rv:l9_cli_last_ham', [('set(co["--ham"].split(","))', 'set(co["--ham"].split(",")[-1:])')]),
    ('rv:l9_curly_no_multiline', [('([^”]{8,}?)', '([^”\\n]{8,}?)')]),
    ('rv:l9_label_no_markup', [('[*_]*\\s*⟦nguon:', '\\s*⟦nguon:')]),
    ('rv:l9_min_fragment5', [('if manh is None or len(bo_dau(manh)) < 6:', 'if manh is None or len(bo_dau(manh)) < 5:')]),
    ('rv:l9_rv_hyphen', [('(?<![\\w-])', '(?<![\\w])')]),
    ('rv:length_only', [('n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1]', 'len(n.group(1)) == len(MO.search(k, 0, m.start()).group(0))')]),
    ('rv:mo_masked', [('MO.search(k, 0, m.start())', 'MO.search(kc, 0, m.start())')]),
    ('rv:mo_one', [('MO = re.compile(r"[*_]*\\Z")', 'MO = re.compile(r"[*_]?\\Z")')]),
    ('rv:new_cli_ignore_ham', [('ham = set(co["--ham"].split(",")) if "--ham" in co else None', 'ham = None')]),
    ('rv:new_code_multiline', [('CODE = re.compile(r"`[^`\\n]*`")', 'CODE = re.compile(r"`[^`]*`")')]),
    ('rv:new_code_no_empty', [('CODE = re.compile(r"`[^`\\n]*`")', 'CODE = re.compile(r"`[^`\\n]+`")')]),
    ('rv:new_code_unclosed', [('CODE = re.compile(r"`[^`\\n]*`")', 'CODE = re.compile(r"`[^`\\n]*(?:`|$)")')]),
    ('rv:new_ct_first', [('for m in CT.finditer(van):', 'for m in list(CT.finditer(van))[:1]:')]),
    ('rv:new_ct_fragment_nonempty', [('([^⟧]*)', '([^⟧]+)')]),
    ('rv:new_fence_literal3', [('l.lstrip().startswith("```")', 'l.strip() == "```"')]),
    ('rv:new_fence_no_strip', [('if l.lstrip().startswith("```"):', 'if l.startswith("```"):')]),
    ('rv:new_first_end', [('NHAN.match(k, m.end())', 'NHAN.match(k, k.index(m.group(0)) + len(m.group(0)))')]),
    ('rv:new_first_quote', [('MO.search(k, 0, m.start())', 'MO.search(k, 0, k.index(m.group(0)))')]),
    ('rv:new_heading_h2_only', [('r"#{1,6} "', 'r"## "')]),
    ('rv:new_label_only_two', [('chi-thi|verdict|commit|ma|doctrine|issue', 'chi-thi|verdict')]),
    ('rv:new_label_punctuation', [('[*_]*\\s*⟦nguon:', '[*_.,;:]*\\s*⟦nguon:')]),
    ('rv:new_lstrip', [('MO.search(k, 0, m.start())', 'MO.search(k.lstrip(), 0, m.start())')]),
    ('rv:new_mo_bound3', [('MO = re.compile(r"[*_]*\\Z")', 'MO = re.compile(r"[*_]{0,3}\\Z")')]),
    ('rv:new_mo_dollar', [('MO = re.compile(r"[*_]*\\Z")', 'MO = re.compile(r"[*_]*$")')]),
    ('rv:new_nhan_bound3', [('NHAN = re.compile(r"([*_]*)', 'NHAN = re.compile(r"([*_]{0,3})')]),
    ('rv:new_nhan_start', [('NHAN.match(k, m.end())', 'NHAN.match(k, m.start())')]),
    ('rv:new_open_end', [('MO.search(k, 0, m.start())', 'MO.search(k, 0, m.end())')]),
    ('rv:new_pointer_single_line', [(':(\\d+)(?:-', ':(\\d)(?:-')]),
    ('rv:new_pointer_single_rev', [('⟦r(\\d+):', '⟦r(\\d):')]),
    ('rv:new_py_strict_end', [('a <= n.lineno <= b', 'a <= n.lineno < b')]),
    ('rv:new_py_strict_start', [('a <= n.lineno <= b', 'a < n.lineno <= b')]),
    ('rv:new_q_curly_greedy', [('“([^”]{8,}?)”', '“([^”]{8,})”')]),
    ('rv:new_q_greedy', [('"([^"]{8,}?)"', '"([^"]{8,})"')]),
    ('rv:new_quote_min9', [('Q = re.compile(r\'"([^"]{8,}?)"|“([^”]{8,}?)”\', re.S)', 'Q = re.compile(r\'"([^"]{9,}?)"|“([^”]{9,}?)”\', re.S)')]),
    ('rv:new_rv_ascii', [('(?<![\\w-])r\\d+(?![\\w])', '(?<![a-zA-Z0-9_-])r\\d+(?![a-zA-Z0-9_])')]),
    ('rv:new_rv_no_boundaries', [('(?<![\\w-])r\\d+(?![\\w])', 'r\\d+')]),
    ('rv:new_rv_right_hyphen', [('(?<![\\w-])r\\d+(?![\\w])', '(?<![\\w-])r\\d+(?![\\w-])')]),
    ('rv:new_rv_single_digit', [('(?<![\\w-])r\\d+(?![\\w])', '(?<![\\w-])r\\d(?![\\w])')]),
    ('rv:new_search_to_match', [('MO.search(k, 0, m.start())', 'MO.match(k, 0, m.start())')]),
    ('rv:new_table_no_strip', [('bang = l.lstrip().startswith("|")', 'bang = l.startswith("|")')]),
    ('rv:no_backtick', [('x.replace("*", "").replace("`", "")', 'x.replace("*", "")')]),
    ('rv:no_curly', [('|“([^”]{8,}?)”', '')]),
    ('rv:no_fence', [('if rao: continue', 'if False: continue')]),
    ('rv:no_fence_toan_bo', [('if l.lstrip().startswith("```"):', 'if False:')]),
    ('rv:no_label_validation', [('chi-thi|verdict|commit|ma|doctrine|issue', '[^⟧]+')]),
    ('rv:no_min_fragment', [('if manh is None or len(bo_dau(manh)) < 6:', 'if manh is None:')]),
    ('rv:no_pair', [('n and n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1]', 'n')]),
    ('rv:no_py_split', [('re.split(r"(\\n\\s*\\n)", n.value)', '[n.value]')]),
    ('rv:no_range', [('if not (1 <= a <= b <= len(L)): dem["LECH"]', 'if False: dem["LECH"]')]),
    ('rv:no_reverse', [('MO.search(k, 0, m.start()).group(0)[::-1]', 'MO.search(k, 0, m.start()).group(0)')]),
    ('rv:no_space', [('def bo_dau(x): return re.sub(r"\\s+", " ", x.replace("*", "").replace("`", "")).strip()', 'def bo_dau(x): return x.replace("*", "").replace("`", "").strip()')]),
    ('rv:no_span', [('int(m.group(3) or m.group(2))', 'int(m.group(2))')]),
    ('rv:no_star', [('x.replace("*", "").replace("`", "")', 'x.replace("`", "")')]),
    ('rv:no_table_boundary', [('(cur and bang != cur[-1].lstrip().startswith("|"))', 'False')]),
    ('rv:r18_no_tab', [('([*_]*)\\s*⟦nguon:', '([*_]*)[ \\n]*⟦nguon:')]),
    ('rv:r18_one_markup', [('([*_]*)\\s*⟦nguon:', '([*_]?)\\s*⟦nguon:')]),
    ('rv:r18_one_space', [('([*_]*)\\s*⟦nguon:', '([*_]*)\\s?⟦nguon:')]),
    ('rv:r18_required_space', [('([*_]*)\\s*⟦nguon:', '([*_]*)\\s+⟦nguon:')]),
    ('rv:r18_word_gap', [('([*_]*)\\s*⟦nguon:', '([*_]*)[\\s\\w]*⟦nguon:')]),
    ('rv:s010_heading_hash', [('if re.match(r"#{1,6} ", l):', 'if l.startswith("#"):')]),
    ('rv:s010_no_fragment', [('if bo_dau(manh or "") not in bo_dau(" ".join(L[a-1:b])):', 'if False:')]),
    ('rv:s010_no_ham', [('if ham else None', 'if False else None')]),
    ('rv:s010_no_hash', [('if bam(L[a-1:b]) != h:', 'if False:')]),
    ('rv:s010_no_heading', [('RV.search(k) or RV.search(td)', 'RV.search(k)')]),
    ('rv:s010_no_inline', [('else che_code(k)', 'else k')]),
    ('rv:s010_no_missing', [('if L is None: dem["KHONG_DO_DUOC"] += 1;', 'if L is None: dem["KHONG_DO_DUOC"] += 0;')]),
    ('rv:s010_no_py', [('khoi_py(van, ham) if str(tep).endswith(".py")', '[] if str(tep).endswith(".py")')]),
    ('rv:s010_no_range_report', [('if not (1 <= a <= b <= len(L)): dem["LECH"] += 1;', 'if not (1 <= a <= b <= len(L)): dem["LECH"] += 0;')]),
    ('rv:s010_no_violation', [('            dem["VI_PHAM"] += 1\n            print', '            dem["VI_PHAM"] += 0\n            print')]),
    ('rv:s010_optional_fragment', [('if manh is None or len(bo_dau(manh)) < 6:', 'if manh is not None and len(bo_dau(manh)) < 6:')]),
    ('rv:set_only', [('n.group(1) == MO.search(k, 0, m.start()).group(0)[::-1]', 'set(n.group(1)) == set(MO.search(k, 0, m.start()).group(0))')]),
    ('neo_lai:l9_label_no_markup@NHAN', [('NHAN = re.compile(r"([*_]*)\\s*⟦nguon:', 'NHAN = re.compile(r"()\\s*⟦nguon:')]),
    ('neo_lai:l10_label_no_underscore@NHAN', [('NHAN = re.compile(r"([*_]*)\\s*⟦nguon:', 'NHAN = re.compile(r"([*]*)\\s*⟦nguon:')]),
    ('neo_lai:new_label_punctuation@NHAN', [('NHAN = re.compile(r"([*_]*)\\s*⟦nguon:', 'NHAN = re.compile(r"([*_.,;:]*)\\s*⟦nguon:')]),
    ('neo_lai:new_pointer_single_line@CT', [('CT = re.compile(r"⟦r(\\d+):(\\d+)(?:-', 'CT = re.compile(r"⟦r(\\d+):(\\d)(?:-')]),
    ('rv:l16_reverse_q', [('for m in Q.finditer(kc):', 'for m in reversed(list(Q.finditer(kc))):')]),
    ('g22:ghi_them_nl', [('p.parent.mkdir(); p.write_bytes(ca[ten][1].encode("utf-8"))', 'p.parent.mkdir(); p.write_bytes((ca[ten][1] + "\\n").encode("utf-8"))')]),
    ('g22:ghi_them_nl+bo_day', [('p.parent.mkdir(); p.write_bytes(ca[ten][1].encode("utf-8"))', 'p.parent.mkdir(); p.write_bytes((ca[ten][1] + "\\n").encode("utf-8"))'), ('day(); return kq', 'return kq')]),
    ('g22:ghi_them_nl+bo_lop2', [('p.parent.mkdir(); p.write_bytes(ca[ten][1].encode("utf-8"))', 'p.parent.mkdir(); p.write_bytes((ca[ten][1] + "\\n").encode("utf-8"))'), ('if p.read_bytes() != doc.encode("utf-8"):', 'if False:')]),
    ('g22:ghi_them_nl+bo_lop2+bo_day', [('p.parent.mkdir(); p.write_bytes(ca[ten][1].encode("utf-8"))', 'p.parent.mkdir(); p.write_bytes((ca[ten][1] + "\\n").encode("utf-8"))'), ('if p.read_bytes() != doc.encode("utf-8"):', 'if False:'), ('day(); return kq', 'return kq')]),
    ('g22:ghi_them_nl+bo_lop1', [('p.parent.mkdir(); p.write_bytes(ca[ten][1].encode("utf-8"))', 'p.parent.mkdir(); p.write_bytes((ca[ten][1] + "\\n").encode("utf-8"))'), ('RB[ten] = p.read_bytes().decode("utf-8")', 'RB[ten] = ca[ten][1]')]),
    ('g22:ghi_them_nl+bo_lop1+bo_day', [('p.parent.mkdir(); p.write_bytes(ca[ten][1].encode("utf-8"))', 'p.parent.mkdir(); p.write_bytes((ca[ten][1] + "\\n").encode("utf-8"))'), ('RB[ten] = p.read_bytes().decode("utf-8")', 'RB[ten] = ca[ten][1]'), ('day(); return kq', 'return kq')]),
    ('g22:ghi_crlf+bo_lop2', [('p.parent.mkdir(); p.write_bytes(ca[ten][1].encode("utf-8"))', 'p.parent.mkdir(); p.write_bytes(ca[ten][1].replace("\\n", "\\r\\n").encode("utf-8"))'), ('if p.read_bytes() != doc.encode("utf-8"):', 'if False:')]),
    ('bo:b22ct_bam_7', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_bam_7")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_bam_9', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_bam_9")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_bam_hoa', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_bam_hoa")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_dong_cuoi_nguon', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_dong_cuoi_nguon")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_dong_dau', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_dong_dau")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_dung_roi_sai', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_dung_roi_sai")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_hai_dung', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_hai_dung")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_manh_dung_nguong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_manh_dung_nguong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_manh_duoi_nguong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_manh_duoi_nguong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_manh_gach_duoi_giu', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_manh_gach_duoi_giu")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_manh_nguong_sau_bo_sao', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_manh_nguong_sau_bo_sao")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_manh_rong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_manh_rong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_manh_thieu', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_manh_thieu")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_manh_trang', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_manh_trang")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_manh_trang_la', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_manh_trang_la")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_nguon_la_thu_muc', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_nguon_la_thu_muc")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_sai_roi_dung', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_sai_roi_dung")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_span_toi_cuoi_nguon', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_span_toi_cuoi_nguon")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ct_span_vuot_cuoi_1', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ct_span_vuot_cuoi_1")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_bytes', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_bytes")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_cuoi_bo_ham_sau_chon', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_cuoi_bo_ham_sau_chon")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_cuoi_chon', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_cuoi_chon")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_dau_chon', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_dau_chon")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_giua_chon', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_giua_chon")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_khong_ham', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_khong_ham")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_mot_dong_bo', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_mot_dong_bo")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_mot_dong_chon', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_mot_dong_chon")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_ngay_sau_ham', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_ngay_sau_ham")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22py_ngay_truoc_ham', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22py_ngay_truoc_ham")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_trai_ascii', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_trai_ascii")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_phai_ascii', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_phai_ascii")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_trai_unicode', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_trai_unicode")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_phai_unicode', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_phai_unicode")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_trai_gach', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_trai_gach")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_phai_gach', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_phai_gach")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_dau_khoi', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_dau_khoi")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_cuoi_khoi', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_cuoi_khoi")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_so_unicode', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_so_unicode")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_thang_hoa', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_thang_hoa")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_trai_ascii', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_trai_ascii")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_phai_ascii', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_phai_ascii")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_trai_unicode', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_trai_unicode")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_phai_unicode', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_phai_unicode")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_trai_gach', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_trai_gach")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_phai_gach', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_phai_gach")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_dau_khoi', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_dau_khoi")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_cuoi_khoi', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_cuoi_khoi")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_so_unicode', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_so_unicode")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22rv_cong_hoa', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22rv_cong_hoa")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_thang_rong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_thang_rong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_thang_nhieu_dong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_thang_nhieu_dong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_thang_chua_dong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_thang_chua_dong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_thang_hai_cap', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_thang_hai_cap")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_thang_py_khong_che', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_thang_py_khong_che")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_cong_rong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_cong_rong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_cong_nhieu_dong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_cong_nhieu_dong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_cong_chua_dong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_cong_chua_dong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_cong_hai_cap', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_cong_hai_cap")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22code_cong_py_khong_che', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22code_cong_py_khong_che")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_thang_bang_thut', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_thang_bang_thut")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_thang_bang_thut_roi_bang', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_thang_bang_thut_roi_bang")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_thang_rao_thut', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_thang_rao_thut")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_thang_rao_chua_dong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_thang_rao_chua_dong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_thang_tieu_de_thut', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_thang_tieu_de_thut")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_thang_tieu_de_tab', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_thang_tieu_de_tab")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_thang_dong_chi_khoang_trang', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_thang_dong_chi_khoang_trang")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_cong_bang_thut', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_cong_bang_thut")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_cong_bang_thut_roi_bang', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_cong_bang_thut_roi_bang")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_cong_rao_thut', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_cong_rao_thut")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_cong_rao_chua_dong', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_cong_rao_chua_dong")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_cong_tieu_de_thut', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_cong_tieu_de_thut")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_cong_tieu_de_tab', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_cong_tieu_de_tab")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('bo:b22ls_cong_dong_chi_khoang_trang', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca', '        ca.pop("b22ls_cong_dong_chi_khoang_trang")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI — o tinh tu noi dung tep, KHONG tu ten ca')]),
    ('g21:bo_eof_khong_nl', [('        can_r21 = set()', '        ca.pop("b21eof_thang_mot_khong_nl")\n        ca.pop("b21eof_cong_mot_khong_nl")\n        can_r21 = set()')]),
    ('g21:bo_nbsp', [('        can_r21 = set()', '        ca.pop("b21kt_thang_nbsp")\n        ca.pop("b21kt_cong_nbsp")\n        can_r21 = set()')]),
    ('g21:markup_toi_7', [('for L_ in range(1, 9):\n                for ch in "*_":', 'for L_ in range(1, 8):\n                for ch in "*_":')]),
    ('g21:bo_py_41', [('for n_ in (14, 39, 40, 41, 60):', 'for n_ in (14, 39, 40, 60):')]),
    ('g21:bo_td_co_roi_khong', [('        can_r21 = set()', '        ca.pop("b21td_thang_co_roi_khong")\n        ca.pop("b21td_cong_co_roi_khong")\n        ca.pop("b21td_thang_co_roi_khong_lien")\n        ca.pop("b21td_cong_co_roi_khong_lien")\n        can_r21 = set()')]),
    ('g21:bo_bien_nguon', [('write_text("  dong hai co noi dung  \\n"', 'write_text("dong hai co noi dung  \\n"')]),
    ('g20:bo_thut_le', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22; tinh lai tu noi dung tep, khong doc bang).', '        ca.pop("vt_thang_thut_le_khong")\n        ca.pop("vt_thang_thut_le_sao")\n        ca.pop("vt_thang_thut_le_sao_thieu_mo")\n        ca.pop("vt_thang_thut_le_sao_doi_lech")\n        ca.pop("vt_cong_thut_le_khong")\n        ca.pop("vt_cong_thut_le_sao")\n        ca.pop("vt_cong_thut_le_sao_thieu_mo")\n        ca.pop("vt_cong_thut_le_sao_doi_lech")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22; tinh lai tu noi dung tep, khong doc bang).')]),
    ('g20:bo_cau_tot_truoc', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22; tinh lai tu noi dung tep, khong doc bang).', '        ca.pop("lan_thang_dung_roi_thieu_mo")\n        ca.pop("lan_thang_co_nhan_roi_khong")\n        ca.pop("lan_thang_nhan_dung_roi_sai")\n        ca.pop("lan_cong_dung_roi_thieu_mo")\n        ca.pop("lan_cong_co_nhan_roi_khong")\n        ca.pop("lan_cong_nhan_dung_roi_sai")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22; tinh lai tu noi dung tep, khong doc bang).')]),
    ('g20:bo_lech_do_dai', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22; tinh lai tu noi dung tep, khong doc bang).', '        ca.pop("dd_thang_bon_ba")\n        ca.pop("dd_thang_ba_bon")\n        ca.pop("dd_thang_bon_nam")\n        ca.pop("dd_cong_bon_ba")\n        ca.pop("dd_cong_ba_bon")\n        ca.pop("dd_cong_bon_nam")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22; tinh lai tu noi dung tep, khong doc bang).')]),
    ('g20:vi_tri_mot_kieu_ngoac', [('        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22; tinh lai tu noi dung tep, khong doc bang).', '        ca.pop("vt_cong_dau_khoi_khong")\n        ca.pop("vt_cong_dau_khoi_sao")\n        ca.pop("vt_cong_dau_khoi_sao_thieu_mo")\n        ca.pop("vt_cong_dau_khoi_sao_doi_lech")\n        ca.pop("vt_cong_thut_le_khong")\n        ca.pop("vt_cong_thut_le_sao")\n        ca.pop("vt_cong_thut_le_sao_thieu_mo")\n        ca.pop("vt_cong_thut_le_sao_doi_lech")\n        ca.pop("vt_cong_sau_dong_ket_markup_khong")\n        ca.pop("vt_cong_sau_dong_ket_markup_sao")\n        ca.pop("vt_cong_sau_dong_ket_markup_sao_thieu_mo")\n        ca.pop("vt_cong_sau_dong_ket_markup_sao_doi_lech")\n        ca.pop("vt_cong_sau_dong_thuong_khong")\n        ca.pop("vt_cong_sau_dong_thuong_sao")\n        ca.pop("vt_cong_sau_dong_thuong_sao_thieu_mo")\n        ca.pop("vt_cong_sau_dong_thuong_sao_doi_lech")\n        # KIEM PHU BANG MAY tren BYTE DOC LAI (r22; tinh lai tu noi dung tep, khong doc bang).')]),
]
def chay(code, ten, thay):
    for o, n in thay:
        if code.count(o) != 1: return ten, None, f"NEO_HONG count={code.count(o)}"
        code = code.replace(o, n)
    d = tempfile.mkdtemp(prefix="db22_")
    try:
        (Path(d) / "con_tro.py").write_text(code, encoding="utf-8")
        r = subprocess.run([sys.executable, "-B", "con_tro.py", "tu-kiem"], cwd=d, capture_output=True, text=True,
                           env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
        dong = [x for x in r.stdout.splitlines() if x.startswith("TU_KIEM")]
        return ten, r.returncode, (dong[-1] if dong else "NGOAI_LE " + (r.stderr.strip().splitlines() or [""])[-1])
    finally:
        shutil.rmtree(d, ignore_errors=True)
if __name__ == "__main__":
    code = Path(sys.argv[1]).read_text(encoding="utf-8")
    with ThreadPoolExecutor(int(sys.argv[2]) if len(sys.argv) > 2 else 4) as ex:
        kq = list(ex.map(lambda x: chay(code, *x), DOT_BIEN))
    for ten, rc, ket in kq: print(f"{ten}\t{rc}\t{ket[:160]}")
    print("TONG", len(kq), "DO", sum(rc == 1 for _, rc, _ in kq), "SONG", sum(rc == 0 for _, rc, _ in kq),
          "NEO_HONG", sum(rc is None for _, rc, _ in kq), "KHAC", sum(rc not in (0, 1, None) for _, rc, _ in kq))
```
