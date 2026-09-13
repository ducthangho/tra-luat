# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 11)

- `packet_id`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**; ID bền `wp523`.
- `packet_issue`: **523** · `mission_issue`: **499**
- `revision`: **11** · `generation`: 10 · soạn **13-09-2026**
- `thay_the_cho`: **revision 10** (`spec_sha256`
  `8bfa0a9e67c9fbef49227fa9688c842b3e9676ef82b5e2befb202634148a93cb`, đã cấp lease gen 9, đã chạy
  lượt cross-review 9 và nhận verdict **`blocked`** lần thứ bảy với 3 P2 + 1 P3 / 9 THỂ HIỆN; chín
  biên nhận đã vào kho ở `c08d845`). r10…r1 **giữ nguyên trên đĩa làm hồ sơ**.
- `executor`: **`codex`** *(ĐỔI — xem khối ngay dưới)* · `reviewer_provider`: **`claude`**

> **r6 ĐỔI PHÂN CÔNG, KHÔNG CHỈ ĐỔI TIÊU CHÍ.** Executor khai **NGHĨA VỤ** bằng lời; **reviewer dựng
> PHÉP ĐO** và phép đo ấy là thứ có thẩm quyền. Đọc mục *"VÌ SAO PHẢI CÓ r6"* trước khi đọc bất kỳ
> mục nghiệm thu nào — nếu không, bạn sẽ đọc r6 bằng mô hình của r1–r5 và hiểu ngược.

> **r11 ĐỔI EXECUTOR: `claude` → `codex`, và reviewer đổi theo thành `claude`.** Đây là LÝ DO DUY
> NHẤT r11 tồn tại. `§3.2` nói thẳng: *"Đổi objective, acceptance, write set, dependency, **executor**
> hoặc environment tạo revision mới và làm lease cũ mất hiệu lực"* — nên đổi vai KHÔNG đi bằng một
> lần bàn giao, nó đi bằng **revision mới + generation mới + cấp lại lease**.
> Cross-review **phải khác nền**, nên executor là `codex` thì reviewer **bắt buộc** là `claude`.
> **KHÔNG đổi gì khác**: `write_set` ba đường · `M16` và `N1`–`N8` NGUYÊN VĂN · `M17-GO` · `nang_tran`
> · `risk`/`review_class` · toàn bộ `dieu_kien_dung`.
>
> **r10 GỠ HẲN CỔNG QUÉT TÊN. Không có `M17''`.** Hai cơ chế liên tiếp — dán nhãn từng câu (r8) rồi
> phân vùng tài liệu (r9) — đều bị lượt kế tiếp phán **VÁ SINH LỖI MỚI**. Lượt 8 khuyến nghị thẳng:
> *"Bỏ cổng phân vùng tên; thu hồi nhất quán cơ chế cũ trong spec và lease; **reviewer ĐỌC NGHĨA có
> quyền chặn**"*. Bằng chứng mạnh nhất cho khuyến nghị ấy là của **chính executor**: cả BA lần lớp
> này bị bắt đều do reviewer **ĐỌC**, KHÔNG lần nào do bộ quét của executor — và bộ quét ấy **mù hai
> lần theo hai cách khác nhau** (lượt 5: tìm tên có dấu phẩy trên khi văn bản viết không dấu; lượt 8:
> tìm tên có dấu ngoặc ngược khi YAML viết trần). Đọc `M17-GO` bên dưới.
>
> **r8 CŨNG KHÔNG đổi phân công và KHÔNG đổi nghĩa vụ nào** — `M16` và `N1`–`N8` vẫn NGUYÊN VĂN
> (lượt 6 đã ĐO điều đó: `H6` cho `byte_identical` giữa r6 và r7). r8 sửa ĐÚNG MỘT THỨ: lượt 6 phán
> lớp `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` là **VÁ HỜ** vì r7 đóng **DANH SÁCH** `dieu_kien_dung`
> mà bỏ sót **VĂN XUÔI** quanh nó. Nguyên văn: *"sai là tuyên bố đã đóng cả cơ chế trong khi còn
> prose vận hành ngoài danh sách đó"*. Đọc `M17-GO` bên dưới trước mục nghiệm thu.
>
> **r7 KHÔNG đổi phân công và KHÔNG đổi nghĩa vụ nào.** `M16` và `N1`–`N8` của r6 giữ NGUYÊN VĂN.
> r7 tồn tại vì một lý do duy nhất: r6 **đã đóng băng** trong khi vẫn còn **văn bản vận hành** của
> luật đã rút. Lượt 5 gọi tên lớp ấy là `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` — nó sống sót qua
> r6 vì bản rút của r6 là một **bảng khai** chứ không phải một phép **xoá**.
- `depends_on`: **`[]`** · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive**

## `nguon_cap_viec`

Kế thừa r1–r5. Cộng chỉ thị MỚI của chủ kho 12-09-2026 — **đổi phân công: executor khai NGHĨA VỤ,
reviewer dựng PHÉP ĐO** — bản chiếu ở
[#issuecomment-5647574815](https://github.com/ducthangho/tra-luat/pull/529#issuecomment-5647574815),
trả lời báo cáo `blocked` lượt 4 ở
[#issuecomment-5647540610](https://github.com/ducthangho/tra-luat/pull/529#issuecomment-5647540610).

Hai chỉ thị của r5 vẫn nguyên hiệu lực về **nội dung** — giữ `M8` + kê vào whitelist, và **MỘT** phép
đo duy nhất cho phạm vi delta (nay là `N3`). r6 chỉ đổi **ai dựng thước** để kiểm chúng.
*(r8 viết lại câu này: bản r7 nêu tên một tiêu chí đã rút để chỉ một chỉ thị **đang còn hiệu lực** —
đúng cơ chế đã gỡ ở r10. Nội dung chỉ thị không đổi, chỉ đổi cách gọi tên sang nghĩa vụ hiện hành.)*

## VÌ SAO PHẢI CÓ r6 — sai ở QUYẾT ĐỊNH GỐC, không ở từng tiêu chí

Hai lượt liên tiếp trả `blocked`, và chúng bác **cùng một thứ**:

Bảng dưới kể lại các lượt đã qua; tên từng tiêu chí xem hồ sơ r3–r5 trên đĩa.

| lượt | tiêu chí do executor tự viết | kết quả |
|---|---|---|
| 3 | ba tiêu chí (xem hồ sơ r3 trên đĩa) | **cả ba bị bác** — hai sai ở ĐỊNH NGHĨA, một sai ở BỘ ĐO |
| 4 | ba tiêu chí ấy viết lại, cộng một tiêu chí mới (hồ sơ r4) | **cả bốn bị bác lần nữa** |

Cộng thêm: bộ đo của executor có **sáu** lỗi tự tìm được ở lượt 3, và lượt 4 tìm thêm **ba lớp** về
chính bộ đo ấy. Và chốt executor dựng **riêng để chống tự-nới** — *"ba phép làm ĐỎ phải VẪN ĐỎ"* —
bị bác đúng chỗ nó yếu: nó giữ **ba ĐIỂM KIỂM**, không giữ **TẬP CHẤP NHẬN**.

**Ba lần cùng một hình dạng là tín hiệu về quyết định gốc, không phải về bản vá.** Quyết định gốc ở
đây: **ai dựng phép đo cho tiêu chí mà chính người đó bị chấm.** r1–r5 để executor dựng cả hai, và
mỗi generation phải khai xung đột lợi ích rồi vẫn bị bác.

### Kho đã đo được rằng đây là HAI đòn bẩy khác nhau

> *"Bắt reviewer tự vá + tự test cải thiện **CHẤT LƯỢNG** finding; chỉ năng lực **ĐO** mới cải thiện
> **ĐỘ PHỦ** — hai đòn bẩy khác nhau, đừng nhầm cái này mua được cái kia."*

r6 chuyển năng lực **ĐO** sang phía reviewer cho đúng những nghĩa vụ mà executor là bên bị chấm.

### Phân công của r6

| vai | làm | KHÔNG làm |
|---|---|---|
| **executor** | khai **NGHĨA VỤ** bằng lời: adapter phải bảo đảm gì, vì sao, và phản chứng nào *nên* tồn tại (mô tả, không dựng). Nộp bản vá + **dữ kiện thô** không cần oracle tự dựng | **KHÔNG** nộp probe làm bằng chứng nghiệm thu · **KHÔNG** tự phán `ĐẠT` cho một nghĩa vụ · **KHÔNG** nộp *"N/N đột biến bị giết"* như lời khai |
| **reviewer** | dựng **PHÉP ĐO** cho từng nghĩa vụ, chạy, phán. Phép đo của reviewer **có thẩm quyền** | — |

**BA CHỐT giữ cho phân công này KHÔNG thành đường thoát trách nhiệm** — thiếu bất kỳ chốt nào thì r6
tệ hơn r5:

1. **Nghĩa vụ phải khai đủ cụ thể để reviewer dựng được phép đo.** Một nghĩa vụ mơ hồ đến mức không
   ai đo được là nghĩa vụ **THIẾU**, không phải nghĩa vụ đã đạt. Đây là nghĩa vụ của executor và nó
   đo được: reviewer khai thẳng nghĩa vụ nào nó không dựng nổi phép đo **vì văn bản**, chứ không vì
   năng lực.
2. **Reviewer không dựng được phép đo ⇒ `KHÔNG ĐO ĐƯỢC`, KHÔNG phải `ĐẠT`.** Chốt quan trọng nhất:
   thiếu nó thì phân công mới biến mọi nghĩa vụ khó đo thành xanh — đúng thứ một tiêu chí r5 **ĐÃ RÚT** của r5 suýt làm
   khi khai *"bộ đo là nháp nên không phải cổng"*.
3. **Executor vẫn chịu trách nhiệm về BẢN VÁ.** r6 đổi ai dựng **thước**, không đổi ai chịu trách
   nhiệm về **thứ được đo**.

**Nói rõ r6 KHÔNG phải gì:** nó **không** phải *"executor thôi đo"*. Executor vẫn đo để tự tin trước
khi đẩy — nhưng phép đo ấy là **việc nội bộ**, không được trình bày như bằng chứng nghiệm thu, và
**không có trọng lượng** trong verdict. Khác biệt ở **THẨM QUYỀN**, không ở sự cần mẫn.

### HAI CÂU MÂU THUẪN TRONG r5 — r6 ĐÁNH DẤU ĐÃ RÚT

Lớp `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` (lượt 4) đo được HAI câu quy phạm trong r5 **trái chính
tiêu chí mới của r5**, và không câu nào được đánh dấu đã rút. Executor tự bắt **một** (`ngoai_pham_vi`
mục 7) rồi **bỏ sót hai**. r6 rút tường minh:

| id | vị trí trong r5 | câu bị RÚT | thay bằng |
|---|---|---|---|
| `S9a` | `SPEC:94–98` | *"Phép đếm đúng là `…<merge commit>..<head>` **CỘNG** `…<base trước merge>..<head trước merge>`"* | **ĐÃ RÚT.** `N3` dưới đây là nghĩa vụ duy nhất về phạm vi delta |
| `S15a` | `SPEC:170` (`A2'`) | *"Được phép trỏ `§8`/`§12` cho ngưỡng và cho **định nghĩa P1/P2/P3**"* | **ĐÃ RÚT** phần *"và cho định nghĩa P1/P2/P3"*. Trỏ `§12` cho **ngưỡng lặp lại** thì GIỮ — đã đo là đúng đích |

**Và rà chỗ dẫn xuất, không vá một câu rồi bỏ chỗ chiếu:** `S2` của lease gen 4 cũng còn mô tả
*trước + sau merge*. Lease gen 5 phải phát biểu lại `S2` theo `N3`. Reviewer lượt 4 nêu đúng chỗ này;
bỏ nó là lặp lại chính lỗi vừa bị bác.

## `nang_tran` — kế thừa r3, KHÔNG nâng thêm

```yaml
nang_tran:
  same_failure_limit: 2 -> 10
  attempts_limit: 3 -> 10
  ai_nang: ducthangho
  can_cu: https://github.com/ducthangho/tra-luat/issues/523#issuecomment-5646812840
  xac_nhan_khuon: 'chủ kho xác nhận "Nâng như #522" — cùng khuôn đã nâng cho #522'
  r4_khong_nang_them: 'r4 KHÔNG xin thêm lượt nào; nó chỉ đổi acceptance theo (B)'
```

Nâng này **KHÔNG** chữa lớp nào; nó chỉ cho phép **đo tiếp**.

## `review_class` và ngưỡng — `ADR-0044` nói cho chật

`sensitive` ⇒ ≤ **3 tệp**, ≤ **300 dòng thêm**. Packet này giữ **đúng hai** tệp SẢN PHẨM.

`ops/reviews/` là **hiện vật review bất biến** — `ci.yml` khai thẳng chúng *"không phải mã sống để CI
chạy"* — nên **KHÔNG** tính vào phép đếm tệp sản phẩm của `ADR-0044`, đúng tiền lệ spec r3 của #522.

**Dòng thêm của phép MERGE không tính vào trần 300.** Một merge commit mang vào toàn bộ delta của
#521; đếm nó thành "dòng thêm của packet" là biến trần `ADR-0044` thành hàm số của việc người khác
làm. **Cách đo nằm ở `N3`, và `N3` là chỗ DUY NHẤT nói về phạm vi delta.** Mục này KHÔNG phát biểu
công thức nào.

> **ĐÃ XOÁ TẠI r7 — đọc dòng này trước khi đi tìm bản cũ.** r5 và r6 viết ở ĐÚNG CHỖ NÀY một công
> thức CỘNG hai khoảng, kèm con trỏ tới một tiêu chí nay không còn tồn tại (xem hồ sơ r5/r6).
> Chủ kho đã rút công thức ấy từ r5. r6 khai việc rút trong một **bảng**, nhưng để nguyên **câu vận
> hành** ở đây — nên người đọc mục `review_class` vẫn nhận công thức đã rút như thể nó có thẩm quyền.
> Đó là lớp `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` của lượt 5, và nó sống sót qua r6 vì **một bảng
> khai không phải một phép xoá**.

## `M17-GO` — GỠ CỔNG QUÉT TÊN, và nói thẳng vì sao

**r10 KHÔNG có cổng quét tên. Không `M17`, không `M17'`, không `M17''`.** Mục này tồn tại để ghi
**vì sao gỡ**, kẻo lượt sau lại dựng lại nó tưởng là một ý mới.

### Ba lần, và mỗi lần một cách hỏng khác nhau

| bản | cơ chế | lượt kế tiếp phán | hỏng ở đâu |
|---|---|---|---|
| r8 | dán **nhãn theo VỊ TRÍ** lên từng đơn vị | VÁ SINH LỖI MỚI | nhãn **hợp thức hoá** phần còn lại của đơn vị; đồng thời **bắt oan** lịch sử hợp lệ — hai lỗi kéo nhau **hai chiều ngược nhau** |
| r9 | **phân vùng tài liệu** (một phụ lục) | VÁ SINH LỖI MỚI | có răng thật, nhưng vẫn **bắt oan theo thiết kế**, và **bộ quét mù** với tên viết trần trong YAML |
| — | (không có bản ba) | — | **gỡ** |

### Điều quyết định, và nó là một phép đếm chứ không phải một cảm giác

Lớp này bị bắt **ba lần**. **Ba lần đều do reviewer ĐỌC.** **Không lần nào** do bộ quét của executor.
Và bộ quét ấy đã **mù hai lần theo hai cách khác nhau** — mỗi lần vì executor tìm **CÁI DẠNG MÌNH
ĐOÁN** thay vì tìm **KHÁI NIỆM**:

- lượt 5 — mẫu đòi tên **có dấu phẩy trên**, văn bản viết **không dấu** ⇒ quét xanh, finding lọt vào
  một đặc tả **đã đóng băng**;
- lượt 8 — mẫu đòi tên **có dấu ngoặc ngược**, chuỗi YAML viết **trần** ⇒ quét xanh, tên lọt vào một
  lease **đã đăng**.

Một cổng **chưa từng bắt được ca thật nào** và **đã bỏ sót hai lần** thì không phải một cổng yếu; nó
là một cổng **cho cảm giác đã soi tới nơi** trong khi việc soi thật do người khác làm. Giữ nó lại là
giữ đúng thứ nguy hiểm hơn cả việc không có gì.

### Nghĩa vụ thay vào chỗ ấy

**Không có cổng. Có NGHĨA VỤ ĐỌC, và nó thuộc REVIEWER:** mỗi lượt, reviewer đọc phần thân đặc tả và
tệp lease, rồi phán **có câu nào đang lấy một tiêu chí ĐÃ RÚT, hoặc một công thức đã rút, làm nghĩa
vụ vận hành hay không** — phán theo **nghĩa của câu**, không theo hình dạng của tên.

Ba điều phải nói kèm, nếu không mục này thành một lời từ bỏ:

1. **Phép đọc ấy KHÔNG tự động hoá được**, và đó là kết luận **đo được** chứ không phải lời bào chữa:
   hai cơ chế tự động liên tiếp đều hỏng, và cả ba ca thật đều do đọc mà ra.
2. **Nó là nghĩa vụ MỖI LƯỢT**, không phải một cổng chạy một lần rồi yên tâm. Reviewer không làm
   phép đọc ấy thì lượt đó **chưa chấm lớp này**, và `approve` khi đó là `KHÔNG ĐO ĐƯỢC`.
3. **Executor vẫn phải viết sạch**: khi rút một tiêu chí thì viết lại câu theo nghĩa vụ hiện hành,
   đừng để tên cũ mang nghĩa vận hành. Gỡ cổng **không** gỡ trách nhiệm — nó chỉ thôi giả vờ rằng
   trách nhiệm ấy đã được máy gánh.

*r10 cũng **xoá hẳn** `PHỤ LỤC A` của r9: phụ lục ấy chỉ tồn tại để phục vụ cổng vừa gỡ, nên giữ nó
lại là giữ một nửa cơ chế đã bị bác.*

## `ban_giao` — executor mới nhận gì, và bốn lớp còn mở

**Bốn lớp mở khi bàn giao**, đo ở lượt 9 trên `abb79df`:

| slug (KHOÁ ĐẾM — không đổi tên) | hạng | thể hiện | ai vá được |
|---|---|---:|---|
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | P2 | 1 | **executor** — `LEASE:130` (gen 10 đã sửa) |
| `bien-nhan-thieu-so-ci-da-chi` | P2 | 3 | **executor** 2 · **CHỦ KHO** 1 |
| `phep-do-doctrine-khong-du-rang` | P2 | 2 | **CHỦ KHO** — `S4` cấm, ngoài write set |
| `bien-nhan-luot-8-lan-du-lieu-luot-6` | P3 | 3 | **executor** |

Một lớp **ĐÃ ĐÓNG** ở lượt 9: `chu-giai-lease-neo-head-cu` — **không** đếm vào số mở.

**NÓI THẲNG VỚI EXECUTOR MỚI:** vòng lặp **không thể** tới `approve` nếu thiếu hai quyết định của
chủ kho. `phep-do-doctrine-khong-du-rang` đã `CHƯA VÁ` qua **năm** lượt liên tiếp; `S4` của chính
đặc tả này cấm packet vá `packet_loop.py`, và reviewer nói rõ *"`S4` giải thích vì sao không sửa
trong packet này, **KHÔNG phải căn cứ để chấm lớp là đóng**"*. Đừng vá nó. Đừng khai nó đã đóng.
Báo chủ kho và đi tiếp phần còn lại.

## `write_set` — GIỮ NGUYÊN ba đường của r3, không thêm

| # | đường dẫn | kiểu | vì sao |
|---|---|---|---|
| 1 | `.claude/skills/cross-review/SKILL.md` | exact | bên SINH bảng phân hạng và verdict; **cũng là tệp #521 vừa sửa** |
| 2 | `.claude/skills/work-packet/SKILL.md` | exact | bên ĐỌC bảng ấy và quyết vá / merge / dừng |
| 3 | `ops/reviews/` | prefix | `VERDICT.md` + `*.receipt.yaml` + hàng Mục lục của các lượt |

(B) **không** cần đường nào mới. **KHÔNG** đụng `docs/PROTOCOL_DA_PHIEN.md`, `.claude/hooks/**`,
`packet_loop.py`, r1/r2/r3 của chính đặc tả này, hay `VERDICT.md` đã giao.

## `ngoai_pham_vi`

Giữ **nguyên sáu mục của r3**. Thêm:

7. **KHÔNG hoàn nguyên bất kỳ phần nào của #521.** Phần được ĐƯA LẠI là **BA** nhóm
   (`A1'` · `A2'` · **`M8`**); mọi dòng khác của #521 giữ **nguyên byte**. Nghĩa vụ đo nó là `N2`.
   **Lịch sử của mục này đáng giữ vì nó là một bài học về CHÍNH tệp đặc tả:** bản r4 viết *"chỉ
   `A1'`/`A2'"`*, và giữ nguyên câu ấy sang r5 sẽ TỰ MÂU THUẪN với chỉ thị giữ `M8`. Executor bắt
   được **một** chỗ như thế trước khi đóng băng r5 rồi **bỏ sót hai** chỗ khác (xem bảng RÚT ở trên).
   Một mục `ngoai_pham_vi` nói hẹp hơn tiêu chí là cái bẫy: người đọc sẽ xoá `M8` để "tuân thủ", tức
   làm đúng điều chỉ thị cấm.
8. **KHÔNG chép lại nội dung `§` mà con trỏ đã trỏ tới.** Nếu một mục của `A1'`/`A2'`/`M8` có thể
   thay bằng một con trỏ mà **vẫn** làm ĐỎ được các đột biến đích, thì nó **phải** là con trỏ.
   Ngược lại, một con trỏ mà đích **KHÔNG chứa** thứ nó hứa thì tệ hơn câu bị thay — xem `N5`.
9. **KHÔNG tự định nghĩa `P1`/`P2`/`P3`.** Đo được: `§8` chứa `P1` nhưng KHÔNG `P2`/`P3`; `§12`
   KHÔNG chứa cả ba; toàn kho không có nguồn nào định nghĩa cả ba (`docs/WORKFLOW_RASOAT_TU_DONG.md`
   dùng `P1`–`P7` cho **nguyên lý**, nghĩa khác hẳn; chỗ duy nhất nói về severity là
   `docs/prompts/CLAUDE_REVIEWER_D0.md:199–200`, mà đó là **PROMPT, không phải doctrine**). Nên
   packet **bỏ** con trỏ sai và **khai nợ** — nó KHÔNG được lấp chỗ trống ấy. Đây là mục đã có từ
   r2 (*"không đổi định nghĩa P1/P2/P3"*), nay kèm phép đo.
10. **KHÔNG sửa biên nhận của các lượt đã giao** — chúng neo theo băm và `t26` canh. `N6` chỉ áp từ
   biên nhận lượt 4 trở đi (lượt 4 đã thi hành nó; chưa lượt nào chấm).
11. **KHÔNG nộp probe của executor làm bằng chứng nghiệm thu, và KHÔNG tự phán `ĐẠT`** cho bất kỳ
   nghĩa vụ `N1`–`N6`. Executor được đo cho riêng mình, nhưng phép đo ấy không có thẩm quyền và
   không được trình bày như bằng chứng. Vi phạm mục này làm r6 tụt về đúng mô hình r1–r5.
12. **KHÔNG dùng phân công mới để im lặng.** Nghĩa vụ khai mơ hồ để reviewer không dựng nổi thước là
   vi phạm `N7`, và hệ quả là `blocked` — không phải `ĐẠT`.

## `muc_tieu`

`M1`–`M12` **giữ nguyên từ r3** (r3 giữ từ r2, r2 giữ `M1`–`M7` từ r1 — **đọc r1 cho định nghĩa đầy
đủ, đừng đọc dòng liệt kê tóm tắt**; chính chỗ ấy đã sinh 1 P1 + 4 P2 ở lượt 1). r4 thêm:

| # | mục tiêu | chiếu vào |
|---|---|---|
| M16 | **Phép đo do REVIEWER dựng** cho mọi nghĩa vụ mà executor là bên bị chấm; executor khai nghĩa vụ + dữ kiện thô. Không dựng được thước ⇒ `KHÔNG ĐO ĐƯỢC`, không phải `ĐẠT`. | 1, 2 |
| M15 | **Con trỏ phải CHỨA thứ nó hứa**: mỗi `§` mà adapter trỏ tới phải thật sự có khái niệm được nêu. Thiếu thì khai **nợ**, KHÔNG tự định nghĩa và KHÔNG trỏ bừa. | 1 |
| M13 | **Hoà giải, không chọn phía**: `cross-review/SKILL.md` sau merge giữ cấu trúc con trỏ của #521 VÀ mang phần bắt buộc của #523 ở dạng tối thiểu. Không hoàn nguyên #521, không bỏ `M1`–`M3`. | 1 |
| M14 | **Tối thiểu phải CHỨNG MINH được là còn răng**: mỗi chốt rút gọn phải có một đột biến làm tiêu chí đích ĐỎ. Không được nhận *"ngắn hơn mà vẫn đủ"* bằng lời. | 1, 2 |

## `nghiem_thu` — NGHĨA VỤ, không phải phép đo

**ĐỌC MỤC NÀY KHÁC HẲN r1–r5.** Dưới đây là **NGHĨA VỤ** (`N1`–`N8`): điều adapter phải bảo đảm.
**Phép đo do reviewer dựng.** Mỗi nghĩa vụ kèm hai thứ để reviewer dựng được thước:

- **ĐO ĐƯỢC BẰNG GÌ** — executor khai *loại* bằng chứng có thể quyết nghĩa vụ ấy, đủ cụ thể để dựng
  thước, **không** kèm script.
- **PHẢN CHỨNG NÊN TỒN TẠI** — mô tả bằng lời cấu hình mà một thước tốt phải bắt được. Đây là
  **mô tả, không phải bộ đo**; reviewer tự dựng và **được quyền dựng ca khác hoặc ca mạnh hơn**.

`A3`–`A8`, `A10`–`A15` **giữ nguyên từ r1–r3** (chúng không nói về phép đo của executor).
`A1'`/`A2'` **giữ nguyên từ r4** — lượt 3 VÀ lượt 4 đều phán chúng còn răng, và chúng nói về **nội
dung** adapter chứ không về bộ đo.

Sáu tiêu chí của r5 **ĐÃ RÚT** ở r6 và thay bằng `N1`–`N6` dưới đây; tên sáu tiêu chí ấy trong hồ sơ
r5 trên đĩa.

**`N1` — bộ chấm đột biến phải chỉ cấp tín dụng khi ĐÚNG TIÊU CHÍ ĐÍCH đỏ.**
Nghĩa vụ: một ca đột biến chỉ được tính là *giết* khi tiêu chí **đích** đỏ **và** quan sát cho các
tiêu chí **không-đích** có mặt đầy đủ và đúng kỳ vọng.
*ĐO ĐƯỢC BẰNG GÌ:* thay bộ chấm bằng các oracle cố ý sai rồi xem nó có từ chối không.
*PHẢN CHỨNG NÊN TỒN TẠI:* oracle mà tiêu chí đích luôn ĐẠT · oracle mà mọi tiêu chí luôn ĐỎ ·
oracle **bỏ hẳn** quan sát cho tiêu chí không-đích (lượt 4 đo được: thiếu quan sát cho phép chấm
*vắng mặt* thành *đúng kỳ vọng*, vì phép hợp trên tập rỗng là đúng) · oracle chỉ đỏ đúng các ca đích.
*NỀN ĐÃ ĐO, ĐỂ RIÊNG KHỎI LỜI KHAI:* bộ chấm của r5 cho **9/9** với oracle loại thứ ba. Đó là một
**dữ kiện**, không phải lời khai `ĐẠT`.

**`N2` — audit dòng được thêm phải quyết theo TỪNG ĐƠN VỊ NGHĨA, không theo lân cận.**
Nghĩa vụ: mỗi câu/ô được thêm phải tự thuộc một nhóm được phép; **không** được để một dòng nhận diện
hợp thức hoá phần còn lại của đoạn.
*ĐO ĐƯỢC BẰNG GÌ:* đưa cùng một nội dung vô hại vào hai vị trí khác nhau và đòi kết quả **giống
nhau**.
*PHẢN CHỨNG NÊN TỒN TẠI:* một câu vô hại đứng **riêng** so với **kề** một khối được phép · một câu
vô hại chứa từ khoá của nhóm nhưng **không** mô tả nghĩa vụ nào của nhóm · và — ca lượt 4 nêu mà r5
không phủ — một thay đổi **đúng nhóm nhưng SAI NỘI DUNG** (ví dụ đảo ô trong bảng `M8`).
*GIỚI HẠN PHẢI KHAI:* phân nhóm theo *nhóm* không phát hiện được sai *nội dung*. Nghĩa vụ này
**không** tự nhận đóng được ca ấy; nó chỉ đòi khai ra.

**`N3` — phạm vi delta phải phủ CẢ trục thời gian LẪN trục đường dẫn.**
Nghĩa vụ: phép đếm dòng thêm phải (a) bao trọn phần viết trong lúc giải xung đột, và (b) không mất
đường dẫn nào đáng kiểm vì đã lọc trước.
*ĐO ĐƯỢC BẰNG GÌ:* so kết quả của một phép đếm **đã lọc** với một phép liệt kê **toàn diff**, trên
cùng một cây.
*PHẢN CHỨNG NÊN TỒN TẠI:* thêm một đường **ngoài** tập được phép rồi xem phép đếm đã lọc có bỏ qua
không (lượt 4 đo được: có) · hai đường **đúng tiền tố nhưng sai tên** so với tập hai tên exact ·
cấu hình mà phần lớn delta được viết **trong** lúc giải xung đột.
*Trần `ADR-0044` không đổi: tổng dòng thêm của hai tệp sản phẩm ≤ **300**.*
**Đây là nghĩa vụ DUY NHẤT về phạm vi delta.** Câu *"phép đếm đúng là … CỘNG …"* của r5 **ĐÃ RÚT**.

**`N4` — mọi đối chứng phải CHI PHỐI KẾT LUẬN, không chỉ được in ra.**
Nghĩa vụ: một đối chứng (dương hoặc âm) phải có khả năng làm phép đo **ĐỎ**. Đối chứng chỉ xuất hiện
trong log là **không tồn tại** với người đọc kết luận.
*ĐO ĐƯỢC BẰNG GÌ:* làm đối chứng thất bại rồi xem kết luận có đổi không.
*PHẢN CHỨNG NÊN TỒN TẠI:* một phép đo mà đối chứng dương ĐỎ nhưng kết luận vẫn xanh — lượt 4 đo được
ca ấy (nối đối chứng vào điều kiện thoát thì cùng một failure đổi từ đạt sang đỏ) trên một tiêu chí
của r5 **ĐÃ RÚT**, nêu ở đây chỉ để kể lại nguồn gốc phản chứng.
*Cùng gốc với bài học đã có của kho: **một phép kiểm không thể đỏ thì không phải bằng chứng**.*

**`N5` — con trỏ `§` phải CHỨA thứ nó hứa; thiếu thì khai NỢ.**
Nghĩa vụ: mỗi con trỏ adapter thêm vào phải dẫn tới mục thật sự có khái niệm được nêu. Không có
nguồn ⇒ **khai nợ**, KHÔNG tự định nghĩa, KHÔNG trỏ bừa.
*ĐO ĐƯỢC BẰNG GÌ:* trích đúng thân mục được trỏ và kiểm khái niệm ở đó.
*PHẢN CHỨNG NÊN TỒN TẠI:* con trỏ tới mục không chứa khái niệm · và hai bẫy executor đã trả giá, nêu
ra để reviewer đừng mất thời gian lặp lại: bộ trích chỉ nhận một cấp tiêu đề sẽ **bắt oan** một con
trỏ tới mục con; và khớp cụm nhiều từ trên văn bản **bó dòng cứng** sẽ bắt oan vì cụm bị cắt qua
dòng.
*NỀN ĐÃ ĐO:* `§8` chứa `P1` nhưng **không** `P2`/`P3`; `§12` **không** chứa cả ba. Bản vá ở `a97d95c`
đã bỏ con trỏ sai ấy, và lượt 4 phán **ĐÃ VÁ THẬT**.

**`N6` — biên nhận phải tách NGÂN SÁCH khỏi SỐ ĐÃ CHI.**
Nghĩa vụ: hai trường riêng — ngân sách `N` mà `M10` cho phép, và số lượt CI loại (b) **thực đã chi**
kèm `run_id`. Danh sách **rỗng** khi đã đo và không có; **`KHONG_DO_DUOC`** khi không đo được. Không
dùng `N` thay số đã chi; không dùng `session_run_id` của lượt review làm `run_id` CI.
*ĐO ĐƯỢC BẰNG GÌ:* đọc biên nhận và đối chiếu với lịch sử lượt chạy của nền.
*PHẢN CHỨNG NÊN TỒN TẠI:* biên nhận khai `N = 0` mà bỏ trống số đã chi · biên nhận khai số đã chi mà
cửa sổ đo **không phủ** trọn đời packet (một `0` từ cửa sổ quá hẹp thì vô nghĩa).
*GIỚI HẠN: lược đồ `bien_nhan_v2` XANH **không** chứng thực nghĩa vụ này — schema-pass khác N6-pass.*

**`N7` — nghĩa vụ phải khai đủ cụ thể để dựng được thước.**
Nghĩa vụ (áp lên chính `N1`–`N6`): reviewer phải dựng được phép đo **từ văn bản**, không phải đoán ý.
*ĐO ĐƯỢC BẰNG GÌ:* reviewer khai thẳng nghĩa vụ nào **không** dựng nổi phép đo **vì văn bản thiếu**.
*Nghĩa vụ nào rơi vào đó là nghĩa vụ **THIẾU** — trạng thái `blocked`, không phải `ĐẠT`.*

**`N8` — không dựng được thước là `KHÔNG ĐO ĐƯỢC`, không phải `ĐẠT`.**
Nghĩa vụ (áp lên cách đọc verdict): nghĩa vụ nào reviewer không đo được thì verdict ghi **KHÔNG ĐO
ĐƯỢC** và nó **KHÔNG** tính là đạt. Đây là chốt duy nhất ngăn phân công mới biến mọi nghĩa vụ khó đo
thành xanh.

### Điều kiện dừng

`sensitive` ⇒ `approve` **tường minh**. `N7`/`N8` nghĩa là: `approve` đòi **mọi** nghĩa vụ `N1`–`N6`
được reviewer **ĐO** và **ĐẠT** — một mục `KHÔNG ĐO ĐƯỢC` nào cũng chặn `approve`.

### Executor nộp gì ở lượt này

Chỉ hai thứ: **bản vá** (nếu có) và **dữ kiện thô** không cần oracle tự dựng — `git diff --numstat`,
`rc` của các cổng **đã có sẵn trong kho** (`doctrine-scan`, `adr-song`, `doc-claims-check`,
`release-verify`, `bien_nhan_v2`, `lease-publish`, `tl.py --selftest`, `idiom-ba-ten`).

**Nói thẳng một điều có thể gây ngạc nhiên:** năm trong sáu lớp còn mở của lượt 4 là khuyết tật của
**bộ đo mà executor từng nộp**, và r6 **không nộp bộ đo nữa**. Nên r6 có thể **không cần bản vá mã
nào mới** — bản vá con trỏ ở `a97d95c` đã được lượt 4 phán ĐÃ VÁ THẬT. Nếu đúng vậy thì executor
khai đúng như vậy, **không** dựng thêm thay đổi cho trông giống có làm việc. Đó là kết quả hợp lệ của
việc đổi phân công, không phải việc bỏ dở.

## `chua_do_duoc`

Giữ **bốn mục của r3** (không cổng nào canh M1–M12; `DIEU-KIEN-VONG-CUOI-KHONG-DO-DUOC`;
`HEAD-DOI-VI-HIEN-VAT-REVIEW`; `grep -i` không đo được tiêu chí văn bản tiếng Việt). Thêm:

5. **`ADAPTER-VUA-CON-TRO-VUA-CO-RANG`** — (B) **giả định** tồn tại một dạng *"ngắn nhất còn đủ răng"*.
   Điều đó **chưa được đo**: chưa ai chứng minh một bảng rút gọn kèm con trỏ `§` vẫn làm ĐỎ đúng những
   đột biến mà bản dài làm ĐỎ. Dưới `M16`, câu hỏi ấy thuộc **`N1`/`N2`** và **reviewer** dựng thước —
   phạm vi vẫn là **packet này**, KHÔNG tổng quát cho mọi mục doctrine khác. Nếu thước của reviewer cho
   thấy một chốt mất răng khi rút gọn thì kết luận đúng là **báo chủ kho** (`S7`), không phải nới
   `A1'`/`A2'` cho hết đỏ.
   *(r8 viết lại đoạn này. Bản r7 còn để một tiêu chí ĐÃ RÚT quyết phép đo và cách dừng ở đây — lượt 6
   đo được và gọi đúng tên: prose vận hành sống ngoài danh sách `dieu_kien_dung`. Xem `M17-GO`.)*
6. **`#521` có lease hay không: KHÔNG ĐO ĐƯỢC, và theo chỉ thị KHÔNG đi tìm thêm.** Xem mục
   *"VÌ SAO PHẢI CÓ r4"*. Đừng đọc bản đo ở comment `5647008786` thành một kết luận về #521.
7. **Lượt cổng tự động trên `6b46012`**: tới lúc soạn r4 **chưa có lượt nào** (`actions_list` lọc theo
   `ci.yml`, head gần nhất của nhánh là `56cfce5`). `M10` cấm gọi tay, nên trạng thái là **KHÔNG ĐO
   ĐƯỢC**, không phải xanh. Lượt cổng của master cho chính commit merge #521 (`dc02c9b`, run
   `34702466800`) kết luận **`cancelled`** — ghi ra vì nó KHÔNG phải bằng chứng master xanh, và cũng
   không phải việc của packet này.
8. **`DINH-NGHIA-PHAN-HANG-KHONG-CO-NGUON`** — `P1`/`P2`/`P3` KHÔNG có nguồn có thẩm quyền trong
   protocol (bảng đo ở `ngoai_pham_vi` mục 9). Mọi verdict của kho dùng ba hạng ấy, nên đây là nợ
   **đang sống**, không phải chuyện của riêng packet này. Cách đóng thuộc chủ kho qua một packet
   sửa `docs/PROTOCOL_DA_PHIEN.md` — **ngoài** write set hiện tại.
9. **`A9-KHONG-TACH-DUOC-AI-VIET-DONG-NAO`** — nhược điểm ĐÃ CHỌN, nay thuộc `N3`: một phép đếm
   endpoint không tách được dòng viết TRƯỚC merge với dòng viết TRONG resolution. Chủ kho chọn tường
   minh ở r5 và r6 giữ nguyên lựa chọn ấy. Giữ tên nợ CŨ vì nó là **khoá đếm** — đổi tên một nợ cũ
   làm hỏng phép đối chiếu giữa các lượt, đúng lý do slug finding phải giữ nguyên.
10. **`phep-do-doctrine-khong-du-rang` vẫn KHÔNG đóng được** — `S4`: `packet_loop.py` ngoài write
   set. Lượt 3 đo lại: scanner gốc 0 · chép trần ADR 0 · chép §5.1 0 · chép §12 **6** ⇒ hai phản
   chứng còn SỐNG. Skill khai ĐÚNG giới hạn và KHÔNG tự nhận đã đóng lớp; *cải thiện LỜI KHAI không
   sửa CƠ CHẾ*, và r5 không khai ngược lại.
11. **`ADAPTER-VUA-CON-TRO-VUA-CO-RANG` vẫn KHÔNG đóng** — hai lượt cho thấy phép chứng minh
   *"tối thiểu còn răng"* của executor có lỗ ở luật cấp tín dụng (lượt 3) rồi ở phạm vi chấp nhận
   (lượt 4). Dưới r6, câu hỏi ấy thuộc `N1`/`N2` và **reviewer** dựng thước. Điều r6 KHÔNG khai được:
   rằng dạng *"ngắn nhất còn đủ răng"* đúng tổng quát cho mọi mục doctrine khác.

## `dieu_kien_dung` — DANH SÁCH ĐẦY ĐỦ, KHÔNG kế thừa qua con trỏ

**r7 viết lại mục này thành danh sách ĐẦY ĐỦ, và đó là một thay đổi có chủ đích chứ không phải chép
lại cho dài.** r6 phát biểu mục này là *"kế thừa `S1`–`S8` của lease gen 3, thêm hai"*. Câu ấy hỏng
theo **ba** cách đo được, và không ai gọi tên hai cách sau:

| # | hỏng ở đâu | đo được thế nào |
|---|---|---|
| 1 | *"thêm **hai**"* trong khi liệt kê **ba** (`S9'`, `S10'`, `S11'`) | đếm gạch đầu dòng của chính mục ấy trong r6 |
| 2 | kéo về `S2` của lease gen 3, mà `S2` ấy phát biểu **ĐÚNG công thức CỘNG đã bị rút** (*"trước merge + sau merge"*) | `git show <ref>:ops/leases/…-r4-exec-3-….yaml` |
| 3 | kéo về `S8` của lease gen 3, mà `S8` ấy neo vào một tiêu chí r6 **ĐÃ RÚT** | cùng lệnh trên |

Tức luật đã rút có **bốn** đường vào, không phải một: câu vận hành ở mục `review_class` (lượt 5 chỉ
ra), `dieu_kien_dung` của lease gen 5 (lượt 5 chỉ ra), và **hai** đường (2)/(3) ở trên — sinh ra bởi
chính câu *"kế thừa"*. Vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba là hình dạng kho đã trả giá; nên
r7 **bỏ hẳn cơ chế kế thừa qua con trỏ** ở mục này. Danh sách dưới đây là bản có thẩm quyền DUY NHẤT,
và lease gen 6 phải chép **đúng** nó — spec và lease không còn chỗ để trôi lệch nhau.

- **`S1`** — cần đường dẫn thứ TƯ ngoài hai tệp skill + prefix `ops/reviews/`.
- **`S2`** (phát biểu theo `N3`) — tổng dòng thêm của **HAI tệp sản phẩm**, đo từ `base_sha` tới head
  cuối, **> 300**. **KHÔNG cộng hai khoảng.** Bản `S2` của lease gen 3 còn viết *"trước merge + sau
  merge"*; câu ấy **ĐÃ RÚT** và không được kế thừa.
- **`S3`** — muốn đụng `docs/PROTOCOL_DA_PHIEN.md` hay `.claude/hooks/**`.
- **`S4`** — muốn vá `packet_loop.py` / `doctrine-scan`: KHÔNG trong write set; nợ riêng.
- **`S5`** — muốn sửa `VERDICT.md` của một lượt đã giao (chúng neo theo băm).
- **`S6`** — muốn đổi định nghĩa `P1`/`P2`/`P3` hay đổi slug của một lớp cũ.
- **`S7`** — một ca làm ĐỎ của `A1'`/`A2'` KHÔNG đỏ được, tức một chốt MẤT RĂNG khi rút gọn. DỪNG và
  báo chủ kho; KHÔNG nới `A1'`/`A2'` cho hết đỏ, và KHÔNG dựng lại bản dài để lách.
  (`A1'`/`A2'` **còn hiệu lực** dưới r6/r7 — lượt 3 và lượt 4 đều phán chúng còn răng.)
- **`S8` ĐÃ RÚT — không có `S8` từ r7 trở đi.** `S8` của lease gen 3 neo vào một tiêu chí đã bị rút ở
  r6. Một điều kiện dừng trỏ tới tiêu chí không còn tồn tại thì **không dừng được gì**; giữ nó
  chỉ để danh sách liền số là đổi một chốt lấy một con số đẹp. Số `S8` **để trống có chủ đích** —
  KHÔNG đánh số lại `S9'`–`S11'` xuống, vì các slug ấy là **khoá đếm** giữa các lượt.
- **`S9'`** — reviewer dựng được thước cho một nghĩa vụ `N1`–`N6` và nghĩa vụ ấy **KHÔNG ĐẠT** theo
  thước đó, mà cách chữa đòi đổi chính nghĩa vụ. Khi ấy **DỪNG và báo chủ kho**; KHÔNG viết lại
  nghĩa vụ cho vừa bản vá.
  *Đổi so `S9` của gen 4:* `S9` cũ nói về *"phép làm ĐỎ của executor mất răng"*, mà từ r6 executor
  **không** dựng phép làm ĐỎ nữa — nên `S9` cũ không còn đối tượng. `S9'` nói về thứ còn tồn tại.
- **`S10'`** — reviewer khai một nghĩa vụ là **KHÔNG ĐO ĐƯỢC vì văn bản** (`N7`). Đó là nghĩa vụ
  THIẾU: DỪNG, báo chủ kho, và **không** tự bồi thêm chữ vào nghĩa vụ giữa lượt để lách.
- **`S11'`** — executor thấy mình đang muốn nộp một probe làm bằng chứng, hoặc muốn tự phán `ĐẠT`.
  Đó là dấu hiệu đang tụt về mô hình r1–r5: DỪNG và đọc lại `ngoai_pham_vi` 11.

**`S12'` (r7, SIẾT ở r8)** — chuẩn bị đóng băng một revision mà phép quét *"còn sót luật cũ"* chỉ khớp theo
**TÊN** tiêu chí, **HOẶC** hạ một luật của phép quét xuống thành *"báo cáo để người đọc tự phán"*. Đó không phải phép đo; nó là phép dò chính tả. DỪNG và dựng lại phép quét theo
**KHÁI NIỆM** (công thức, con trỏ, câu vận hành), rồi mới đóng băng.
*Vì sao có mặt:* trước khi đóng băng r6, executor CÓ chạy phép quét ấy và nó cho **0 dòng**. Mẫu
dùng là một mẫu liệt kê **toàn tên CÓ dấu phẩy trên**, trong khi văn bản còn sót viết **cùng tên đó
KHÔNG có dấu ấy** — nên phép khớp trả `False` cho chính dòng đang vi phạm, còn một phép khớp viết
đúng lại trả `True`. (Cặp tên cụ thể trong hồ sơ lượt 5.) Một phép quét xanh vì
**hỏi sai tên** đã để một finding lọt vào một đặc tả ĐÃ ĐÓNG BĂNG.
*SIẾT Ở r8 — vì lượt 6 cho thấy `S12'` bản r7 KHÔNG đủ, và nó không đủ theo một cách bất ngờ.* Trước
khi đóng băng r7, executor **đã sửa đúng chỗ r7 dạy**: viết chốt theo KHÁI NIỆM (công thức, con trỏ),
miễn trừ theo **vị trí cấu trúc** chứ không theo cụm từ, kèm hai đột biến chứng minh răng. Chốt ấy
**sạch thật**. Nhưng luật thứ ba — *viện dẫn tiêu chí đã rút* — không tách được bằng regex giữa câu
**VẬN HÀNH** và câu **KỂ LẠI LỊCH SỬ**, nên executor **tự hạ nó xuống thành BÁO CÁO** rồi tự phân
loại 10 đoạn, **sai 3**. **Hạ một chốt xuống thành báo cáo rồi tự mình làm người phán là BỎ chốt,
không phải GIỮ chốt** — và tệ hơn không có chốt, vì bản báo cáo cho cảm giác đã soi tới nơi.
Lối ra KHÔNG phải một regex khôn hơn — r8 và r9 đã thử hai cách và cả hai hỏng. Lối ra là **gỡ
cổng** và trả việc ấy cho **phép đọc nghĩa của reviewer**; xem `M17-GO`.
