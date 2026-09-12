# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 5)

- `packet_id`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**; ID bền `wp523`.
- `packet_issue`: **523** · `mission_issue`: **499**
- `revision`: **5** · `generation`: 4 · soạn **12-09-2026**
- `thay_the_cho`: **revision 4** (`spec_sha256`
  `78388d3e25f780fd18581a47353e5560965d92f2f347379ef5da235e1e941bfa`, đã cấp lease gen 3, đã chạy
  lượt cross-review 3 và nhận verdict **`blocked`** với 8 LỚP / 11 THỂ HIỆN; ba biên nhận đã vào kho
  ở `6c26fe0`). r4, r3, r2 và r1 **giữ nguyên trên đĩa làm hồ sơ**.
- `depends_on`: **`[]`** · `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive**

## `nguon_cap_viec`

Kế thừa r1, r2, r3, r4. Cộng **HAI chỉ thị MỚI** của chủ kho 12-09-2026 — bản chiếu ở
[#issuecomment-5647309978](https://github.com/ducthangho/tra-luat/pull/529#issuecomment-5647309978),
trả lời verdict `blocked` của lượt 3 ở
[#issuecomment-5647286763](https://github.com/ducthangho/tra-luat/pull/529#issuecomment-5647286763):

1. **`M8` GIỮ trong adapter**, và `A17` của r5 **kê nó vào whitelist**, đồng thời **audit cả dòng
   CỘNG** chứ không chỉ dòng XOÁ.
2. **`A9` là MỘT phép đo duy nhất** `git diff --numstat <base_sha>..<head cuối>` cho hai tệp sản
   phẩm — một số hạng, không cộng.

Chỉ thị (B) của r4 vẫn nguyên hiệu lực
([#issuecomment-5647027599](https://github.com/ducthangho/tra-luat/pull/529#issuecomment-5647027599)).

## VÌ SAO PHẢI CÓ r5 — verdict `blocked`, và khiếm khuyết nằm trong TIÊU CHÍ của r4

Cross-review lượt 3 (codex, khác nền) trên `7f028a7` trả **`blocked`**, 0 P1 + **8 P2** = 8 LỚP,
11 THỂ HIỆN. `§3.2` nói rõ: *finding cho thấy chính spec thiếu thì verdict là `blocked` và đi qua
revision mới*. **HAI** finding nhắm vào tiêu chí của r4, nên packet KHÔNG được tự vá.

### `A9` của r4 có BA khiếm khuyết, cả ba đo được

| # | khiếm khuyết | phép đo |
|---|---|---|
| 1 | khoảng thứ hai (*merge commit → head cuối*) là **RỖNG** trên head thật, vì phần hoà giải nằm **TRONG** chính commit merge | `literal A9 after: ''` |
| 2 | **cộng đôi** khi hai khoảng chia một tệp: #521 không chạm `work-packet/SKILL.md` nên `+139` bị cộng hai lần ⇒ `410 > 300` báo động giả | `(1) 85fcbf8..6b46012` = +139 · `(2) dc02c9b..cây` = +139 |
| 3 | **bỏ lọt** delta viết TRONG resolution ⇒ có thể đếm **THIẾU** và che một vi phạm | fixture: `B→H` = (2, 2), `M→F` = (2, 2) ⇒ tổng `4 ≤ 300` **ĐẠT**, trong khi `B→F` = **(305, 2)** với **301** dòng viết lúc giải xung đột |

Khiếm khuyết **3** bác thẳng lời khai *"fail-closed, không thể che vi phạm"* mà r4 và `EVIDENCE.md`
của lượt 3 đã dùng. Cái sai không phải con số: nó là **suy một LỚP HÀNH VI từ MỘT quan sát**
(`410 > 194`) — đúng lỗi *"lời khai rộng hơn phép đo"*. Và `EVIDENCE.md` còn **âm thầm THAY** khoảng
thứ hai bằng một khoảng KHÁC (`dc02c9b..head`) mà không nói ra.

### `A17` của r4 loại bỏ `M8` khỏi tập được thêm, trong khi hợp đồng vẫn giữ `M8`

`A17` chỉ cho phép thêm dòng thuộc `A1'`/`A2'`. Nhưng phép hoà giải thêm **18 dòng bảng `M8`** ở hunk
đầu, và `M8` **không** thuộc hai tiêu chí ấy. Hai lối ra đều mất một thứ: xoá 18 dòng ⇒ mất nghĩa vụ
`M8` đang giữ; giữ ⇒ tự nhận `A17` đạt là không đúng hợp đồng hẹp đã viết. Reviewer nói thẳng *"phải
phân xử spec, không bắt executor tuỳ tiện chọn một phía"*.

Kèm một phép đo nữa: `A17` đo **`−0`** và phiên đọc đó thành "bảo toàn". `−0` chỉ chứng minh **bảo
toàn BYTE**, không chứng minh **bảo toàn NGHĨA** — thêm một câu phủ định một giới hạn vẫn cho `−0`.

### Và một con số của phiên thi công SAI, ghi ra vì nó đã được đăng

`A17` được khai **+39/−0**. Đo lại bằng `git diff --numstat`: **+55/−0**. Phép đếm của phiên là
`grep -c '^+[^+]'`, mà mẫu ấy đòi một ký tự sau dấu `+` nên **bỏ sót 16 dòng TRỐNG được thêm**.
`numstat` là nguồn có thẩm quyền và nó nói 55 từ đầu. Riêng `−0` thì ĐÚNG.

Chủ kho chốt: **giữ `M8` + kê vào whitelist**, và **`A9` là một phép đo duy nhất** ⇒ đổi acceptance
⇒ `§3.2`/`§5` đòi revision 5 + generation 4 + cấp lại lease.

### Bối cảnh hai writer của r4 — GIỮ làm hồ sơ, không nhắc lại số

Lý do r4 tồn tại (PR #521 land và sửa cùng một tệp trong write set; 2 hunk / 82 dòng xung đột; sổ
lease không có lease nào của #521 ⇒ **KHÔNG ĐO ĐƯỢC**, chủ kho chốt *chỉ ghi nhận*) nằm nguyên trong
r4 và trong hai comment `5647008786` / `5647027599`. r5 **không** chép lại các số ấy — chép một con
số vào hai chỗ là mở đường cho chúng trôi lệch.

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
làm. Phép đếm đúng là `git diff --numstat <merge commit>..<head>` cho phần packet viết SAU merge, cộng
`git diff --numstat <base trước merge>..<head trước merge>` cho phần đã viết trước — và `A9` dưới đây
nói thẳng cách đo.

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

7. **KHÔNG hoàn nguyên bất kỳ phần nào của #521.** Phép merge chỉ được ĐƯA LẠI phần mà **`A17'`
   liệt kê** — nay là **BA** nhóm (`A1'` · `A2'` · **`M8`**), không phải hai; mọi dòng khác của #521
   giữ **nguyên byte**. Đây là chốt có thể ĐO, xem `A17'`.
   **Bản r4 của mục này viết "chỉ `A1'`/`A2'"`, và giữ nguyên câu ấy trong r5 sẽ TỰ MÂU THUẪN với
   chỉ thị 1** — `M8` được chủ kho cho giữ. Một mục `ngoai_pham_vi` nói hẹp hơn tiêu chí là một cái
   bẫy: người đọc nó sẽ xoá `M8` để "tuân thủ", tức làm đúng điều chỉ thị 1 cấm.
8. **KHÔNG chép lại nội dung `§` mà con trỏ đã trỏ tới.** Nếu một mục của `A1'`/`A2'`/`M8` có thể
   thay bằng một con trỏ mà **vẫn** làm ĐỎ được các đột biến đích, thì nó **phải** là con trỏ.
   Ngược lại, một con trỏ mà đích **KHÔNG chứa** thứ nó hứa thì tệ hơn câu bị thay — xem `A19`.
9. **KHÔNG tự định nghĩa `P1`/`P2`/`P3`.** Đo được: `§8` chứa `P1` nhưng KHÔNG `P2`/`P3`; `§12`
   KHÔNG chứa cả ba; toàn kho không có nguồn nào định nghĩa cả ba (`docs/WORKFLOW_RASOAT_TU_DONG.md`
   dùng `P1`–`P7` cho **nguyên lý**, nghĩa khác hẳn; chỗ duy nhất nói về severity là
   `docs/prompts/CLAUDE_REVIEWER_D0.md:199–200`, mà đó là **PROMPT, không phải doctrine**). Nên
   packet **bỏ** con trỏ sai và **khai nợ** — nó KHÔNG được lấp chỗ trống ấy. Đây là mục đã có từ
   r2 (*"không đổi định nghĩa P1/P2/P3"*), nay kèm phép đo.
10. **KHÔNG sửa hai biên nhận của lượt 1–2** — chúng neo theo băm và `t26` canh. `A16'` chỉ áp từ
   biên nhận lượt 4.

## `muc_tieu`

`M1`–`M12` **giữ nguyên từ r3** (r3 giữ từ r2, r2 giữ `M1`–`M7` từ r1 — **đọc r1 cho định nghĩa đầy
đủ, đừng đọc dòng liệt kê tóm tắt**; chính chỗ ấy đã sinh 1 P1 + 4 P2 ở lượt 1). r4 thêm:

| # | mục tiêu | chiếu vào |
|---|---|---|
| M15 | **Con trỏ phải CHỨA thứ nó hứa**: mỗi `§` mà adapter trỏ tới phải thật sự có khái niệm được nêu. Thiếu thì khai **nợ**, KHÔNG tự định nghĩa và KHÔNG trỏ bừa. | 1 |
| M13 | **Hoà giải, không chọn phía**: `cross-review/SKILL.md` sau merge giữ cấu trúc con trỏ của #521 VÀ mang phần bắt buộc của #523 ở dạng tối thiểu. Không hoàn nguyên #521, không bỏ `M1`–`M3`. | 1 |
| M14 | **Tối thiểu phải CHỨNG MINH được là còn răng**: mỗi chốt rút gọn phải có một đột biến làm tiêu chí đích ĐỎ. Không được nhận *"ngắn hơn mà vẫn đủ"* bằng lời. | 1, 2 |

## `nghiem_thu`

`A3`–`A8`, `A10`–`A15` **giữ nguyên từ r1–r3**. `A1'`/`A2'` **giữ nguyên từ r4** (lượt 3 phán chúng
ĐẠT). **VIẾT LẠI**: `A9'` · `A16'` · `A17'` · `A18'`. **MỚI**: `A19` · `A20`.

**`A1'` và `A2'` KHÔNG đổi, và đó là một phép đo chứ không phải bỏ qua:** lượt 3 chạy lại ba ca của
`A1'` và bốn ca của `A2'`, và chúng vẫn có răng. Thứ lượt 3 bác là **BỘ ĐO** (`A18`) và **hai tiêu
chí về phạm vi/đếm** (`A9`, `A17`), không phải hai tiêu chí nội dung.

**A1' (M1, M2, M13) — bảng điều kiện dừng: ba lớp PHÂN BIỆT ĐƯỢC, ở dạng tối thiểu.**
`cross-review/SKILL.md` phải có bảng ánh xạ `review_class → điều kiện dừng` với **đúng ba** hàng; hàng
`sensitive` phải nói **`approve`**, **không** nói *"0 P1 + 0 P2"*. Bảng được phép **rút ngắn tối đa**
và trỏ `§3.2` cho định nghĩa trục `review_class` — điều `A1` của r1 đòi mà r4 **bỏ** là phần diễn giải
văn xuôi quanh bảng; điều r4 **giữ** là chính bảng và câu phân biệt hàng `sensitive`.
**Phép làm ĐỎ (bắt buộc chạy, cả ba):** đổi hàng `sensitive` thành *"hết P1, P2"* ⇒ ĐỎ · gộp `routine`
với `systemic` ⇒ ĐỎ · **thay cả bảng bằng một con trỏ trần** (`"điều kiện dừng: xem §12"`) ⇒ **ĐỎ**.
Phép đo: parse bảng Markdown, đòi tập `review_class` **bằng** `{routine, systemic, sensitive}` và ba
giá trị điều kiện **đôi một khác nhau**.
Ca thứ ba là ca phân biệt r4 với (A): nếu con trỏ trần cũng ĐẠT thì `A1'` không đo gì, và (B) đã tụt
thành (A) mà không ai nói ra.

**A2' (M3, M13) — `BẢNG LỚP` và đơn vị đếm: nghĩa vụ, ở dạng tối thiểu.**
`cross-review/SKILL.md` phải đòi verdict mang mục `BẢNG LỚP` với **ba** cột
`(lop_loi, các slug thuộc lớp, bản vá theo lớp | lý do vá lẻ)`, và phải khai **đơn vị đếm**:
`so_p1`/`so_p2`/`so_p3` đếm **LỚP**, `so_the_hien` đếm **THỂ HIỆN**, `findings_ids` là slug **LỚP**.
`work-packet/SKILL.md` phải đòi vòng vá **ĐỌC** bảng ấy trước khi sửa dòng nào.
Được phép trỏ `§8`/`§12` cho ngưỡng và cho định nghĩa P1/P2/P3; **không** được chép số trần.
**Phép làm ĐỎ (bắt buộc chạy, cả bốn):** bỏ cột `bản vá theo lớp` ⇒ ĐỎ · bỏ bảng đơn vị đếm ⇒ ĐỎ ·
bỏ câu *mỗi finding thuộc đúng một lớp* ⇒ ĐỎ · thay cả mục bằng một con trỏ trần ⇒ **ĐỎ**.

**A17' (chỉ thị 1) — whitelist GỒM `M8`, và audit CẢ dòng CỘNG.**

Trên head cuối, `git diff <base_sha>..<head> -- .claude/skills/cross-review/SKILL.md` chỉ được chứa
dòng thuộc **một trong ba** nhóm:

| # | nhóm được thêm | căn cứ |
|---|---|---|
| 1 | `A1'` — bảng điều kiện dừng theo `review_class` | tiêu chí r4, giữ nguyên |
| 2 | `A2'` — `BẢNG LỚP` + bảng đơn vị đếm | tiêu chí r4, giữ nguyên |
| 3 | **`M8` — bảng phân biệt hai nguyên nhân head đổi** | **chỉ thị 1 của chủ kho**; `§8`/`§13` cho hợp đồng `reviewed_sha` nhưng KHÔNG phân xử VÌ SAO head đổi |

**HAI chiều phải audit, không chỉ một:**

- **dòng XOÁ**: mọi dòng `−` phải nằm trong một vùng đã xung đột VÀ có lý do thuộc nhóm 1–3. Số
  dòng `−` ngoài các vùng ấy = **0**. Đo bằng `git diff --numstat` (**KHÔNG** bằng `grep` tự viết).
- **dòng CỘNG**: mọi dòng `+` phải thuộc nhóm 1–3. Một dòng thêm **ngoài** ba nhóm ⇒ ĐỎ, kể cả khi
  nó vô hại — vì `−0` chỉ chứng minh **bảo toàn BYTE**, không chứng minh **bảo toàn NGHĨA**.

**Phép làm ĐỎ (bắt buộc chạy, cả ba):** xoá một dòng của #521 mà ba nhóm không đòi ⇒ ĐỎ · thêm một
câu **phủ định một giới hạn** của #521 (giữ `−0`) ⇒ **ĐỎ** — ca này là ca bác chính lời khai
*"`−0` ⇒ bảo toàn"* · gỡ `M8` khỏi whitelist rồi đo lại ⇒ ĐỎ (chứng minh nhóm 3 có răng, không phải
một hàng trang trí).

**Đếm bằng `numstat`, không bằng bộ đếm tự viết.** Lượt 3 đo được: `grep -c '^+[^+]'` bỏ sót **16**
dòng TRỐNG (`+39` thay vì `+55`). Mọi con số dòng của `A17'` phải lấy từ `git diff --numstat`.

**A18' (M14, lớp `dem-dot-bien-khong-theo-tieu-chi-dich`) — mỗi ca neo vào TIÊU CHÍ ĐÍCH.**

Bộ đo phải, cho **từng** ca đột biến:

1. khai **tiêu chí ĐÍCH** của ca ấy (`A1'` hay `A2'` hay `A17'`) TRƯỚC khi chạy;
2. đọc kết quả **RIÊNG từng tiêu chí**, **KHÔNG** đọc mã thoát tiến trình;
3. đòi tiêu chí ĐÍCH **ĐỎ**, và kiểm tiêu chí **KHÔNG-đích** đúng như ca ấy dự kiến;
4. giữ **ĐỐI CHỨNG DƯƠNG** (bản gốc ĐẠT mọi tiêu chí) và chốt đột biến **thật sự đổi nội dung**.

**CẤM luật `rc != 0`.** Lượt 3 đo được: một oracle **SAI ĐÍCH** (`A1'` là stub luôn ĐẠT, `A2'` chỉ
dò *"văn bản có đổi không"*) **QUA được đối chứng dương** và vẫn báo **7/7 bị giết**, cấp tín dụng
cho ba ca nhắm `A1'` mà `A1'` chưa từng đỏ. Một mã thoát cho nhiều tiêu chí thì không phân biệt được
tiêu chí nào đã đỏ.

**Phép làm ĐỎ của chính `A18'` (bắt buộc):** chạy lại oracle SAI ĐÍCH ấy và đòi bộ đo MỚI **từ chối**
nó — tức báo *tín dụng giả* cho ba ca `A1'`. Không có phép ấy thì `A18'` chưa chứng minh đã đóng lớp.

**Ghi cho đúng, vì nó dễ bị đọc quá mạnh:** output GỐC của bộ đo r4 in riêng `A1'`/`A2'` từng ca và
cho thấy **bảy ca THẬT SỰ đúng đích**. Nên cái sai là **LUẬT CẤP TÍN DỤNG**, KHÔNG phải kết quả —
đừng kết luận bảy ca sai đích.

**A20 (lớp `bo-doc-bang-vuot-ranh-gioi-muc` và `bo-do-bang-chi-kiem-ten-khong-kiem-nghia`) — bộ đo
phải khoá theo CẤU TRÚC.**
Bộ đo `A1'`/`A2'` phải: (a) **dừng ở tiêu đề `##` kế tiếp** — không lấy bảng ngoài mục đang nghiệm
thu; (b) giữ **cardinality** (số hàng, số cột) và quan hệ **trường → đơn vị**, không chỉ kiểm TẬP
TÊN. Áp cùng nguyên tắc cho **cả hai** bộ đọc.
**Phép làm ĐỎ:** đọc sang bảng của mục khác ⇒ ĐỎ · một bảng đủ tên mà **thiếu hàng** hoặc **lệch
đơn vị** vẫn ĐẠT ⇒ ĐỎ.
**Giới hạn, khai thẳng:** bộ đo là **NHÁP** của phiên, sống trong sandbox, **KHÔNG** vào write set
và **KHÔNG** commit. Nên `A20` đo **phép đo**, không dựng một cổng của kho — và không được khai
ngược lại.

**A9' (chỉ thị 2) — MỘT phép đo duy nhất, không cộng.**

```
git diff --numstat <base_sha của lease>..<head cuối> -- .claude/skills/
```

⇒ **đúng hai** đường dẫn (`cross-review/SKILL.md`, `work-packet/SKILL.md`), và **tổng `additions`
của hai đường ấy ≤ 300** (`ADR-0044`, trần dòng KHÔNG được nâng). Đường thứ ba nào ngoài
`ops/reviews/` ⇒ ĐỎ.

`base_sha` của lease gen 4 là **`dc02c9b`** — master SAU khi #521 land. Nên phép đo này **không**
tính delta mà merge mang vào từ #521, vì #521 đã nằm TRONG `dc02c9b`.

**Vì sao MỘT số hạng, không phải hai:** cả ba khiếm khuyết của `A9` r4 đến từ việc CỘNG hai khoảng.
Một số hạng thì không cộng đôi được (khiếm khuyết 2), không có khoảng rỗng nào để bỏ lọt (khiếm
khuyết 1), và bao trọn delta viết TRONG resolution vì resolution nằm giữa `base_sha` và `head`
(khiếm khuyết 3). Đây cũng ĐÚNG phép đo `A17'` dùng, nên r5 **không** còn hai phép đếm không nhất
quán như r4.

**NHƯỢC ĐIỂM ĐÃ CHỌN, khai thẳng chứ không che:** phép đo này **KHÔNG** tách được dòng viết TRƯỚC
merge với dòng viết TRONG resolution. Khi `base_sha` lùi xa thì nó tính mọi dòng packet thêm trên
base ấy — đúng thứ trần `ADR-0044` muốn chặn, nhưng không trả lời được *"ai viết dòng nào"*. Chủ kho
đã chọn đánh đổi này tường minh. Nợ có tên: `A9-KHONG-TACH-DUOC-AI-VIET-DONG-NAO`.

**Phép làm ĐỎ (bắt buộc chạy, cả ba):** thêm một đường thứ ba ngoài `ops/reviews/` ⇒ ĐỎ · đẩy
`additions` của hai tệp sản phẩm vượt 300 ⇒ ĐỎ · **dựng lại fixture đã bác r4** (delta viết TRONG
resolution, `B→F` = 305) và đòi `A9'` **BẮT được** nó ⇒ nếu nó vẫn lọt thì `A9'` cũng sai và phải
báo chủ kho, KHÔNG tự đổi công thức.

**A16' (lớp `bien-nhan-thieu-so-ci-da-chi`) — NGÂN SÁCH khác SỐ ĐÃ CHI.**
Biên nhận phải có **hai trường riêng**: `ngan_sach_ci_loai_b` (giá trị `N` mà `M10` cho phép) và
`da_chi_ci_loai_b` (số lượt THỰC ĐÃ CHI) kèm `run_id` của chúng. Danh sách **RỖNG** khi đã đo và
không có lượt nào; **`KHONG_DO_DUOC`** khi không đo được. **KHÔNG** được dùng `N` thay cho số đã chi,
và **KHÔNG** được dùng `session_run_id` của lượt review làm `run_id` CI.
**Phép làm ĐỎ:** khai `N = 0` mà bỏ trống `da_chi_ci_loai_b` ⇒ ĐỎ — đó chính là thể hiện `C1` mà
lượt 3 tìm được, và `bien_nhan_v2` XANH vẫn **không** chứng thực nghĩa vụ này (*"schema-pass không
tương đương A16-pass"*).
**Giới hạn:** hai biên nhận của lượt 1–2 **KHÔNG** được sửa — chúng neo theo băm và `t26` canh. `A16'`
chỉ áp từ biên nhận lượt 4 trở đi.

**A19 (M15) — con trỏ phải CHỨA thứ nó hứa, và điều đó ĐO ĐƯỢC.**
Với mỗi con trỏ `§` mà hai tệp skill thêm vào, trích ĐÚNG mục ấy từ `docs/PROTOCOL_DA_PHIEN.md` và
kiểm nó thật sự có khái niệm được nêu. **Không** coi "có xuất hiện chuỗi" là "có định nghĩa".
**Phép làm ĐỎ:** trỏ một `§` không chứa khái niệm đã hứa ⇒ ĐỎ.
**Nền đã ĐO, và nó ĐỎ ở r4:** dòng *"định nghĩa P1/P2/P3: xem §8/§12"* — `§8` chứa `P1` nhưng
**KHÔNG** `P2`/`P3`; `§12` **KHÔNG** chứa cả ba. r5 đòi bỏ con trỏ ấy.

**Điều kiện dừng:** `sensitive` ⇒ `approve` **tường minh**. Packet này phải là packet đầu tiên tuân
**chính** quy trình nó khai — gồm `M8` (base trôi ⇒ merge base TRƯỚC, rồi review head SAU merge) và
`M10` (`N = 0` trước merge).

**Mọi tiêu chí `A1'`–`A18` phải ĐÚNG Ở CẢ HAI PHÍA của lần merge.** Một tiêu chí chỉ đo được trên bản
nhánh là tiêu chí **chết đúng lúc merge** — đúng bài học *"câu mô tả vị trí của một artefact phải đúng
ở CẢ HAI phía của lần merge"*. Nên mọi phép đo của r4 neo vào **head sau merge**, và nêu `dc02c9b` làm
mốc so thay vì "nhánh mặc định hiện tại".

## `chua_do_duoc`

Giữ **bốn mục của r3** (không cổng nào canh M1–M12; `DIEU-KIEN-VONG-CUOI-KHONG-DO-DUOC`;
`HEAD-DOI-VI-HIEN-VAT-REVIEW`; `grep -i` không đo được tiêu chí văn bản tiếng Việt). Thêm:

5. **`ADAPTER-VUA-CON-TRO-VUA-CO-RANG`** — (B) **giả định** tồn tại một dạng *"ngắn nhất còn đủ răng"*.
   Điều đó **chưa được đo**: chưa ai chứng minh một bảng rút gọn kèm con trỏ `§` vẫn làm ĐỎ đúng những
   đột biến mà bản dài làm ĐỎ. `A18` biến giả định ấy thành phép đo **cho packet này**, nhưng **không**
   chứng minh nó đúng tổng quát cho mọi mục doctrine khác — và nếu `A18` cho thấy một chốt mất răng khi
   rút gọn, thì kết luận đúng là **báo chủ kho**, không phải nới `A1'`/`A2'` cho hết đỏ.
6. **`#521` có lease hay không: KHÔNG ĐO ĐƯỢC, và theo chỉ thị KHÔNG đi tìm thêm.** Xem mục
   *"VÌ SAO PHẢI CÓ r4"*. Đừng đọc bản đo ở comment `5647008786` thành một kết luận về #521.
8. **`DINH-NGHIA-PHAN-HANG-KHONG-CO-NGUON`** — `P1`/`P2`/`P3` KHÔNG có nguồn có thẩm quyền trong
   protocol (bảng đo ở `ngoai_pham_vi` mục 9). Mọi verdict của kho dùng ba hạng ấy, nên đây là nợ
   **đang sống**, không phải chuyện của riêng packet này. Cách đóng thuộc chủ kho qua một packet
   sửa `docs/PROTOCOL_DA_PHIEN.md` — **ngoài** write set hiện tại.
9. **`A9-KHONG-TACH-DUOC-AI-VIET-DONG-NAO`** — nhược điểm ĐÃ CHỌN của `A9'`: một phép đo duy nhất
   không tách được dòng viết TRƯỚC merge với dòng viết TRONG resolution. Chủ kho chọn tường minh.
10. **`phep-do-doctrine-khong-du-rang` vẫn KHÔNG đóng được** — `S4`: `packet_loop.py` ngoài write
   set. Lượt 3 đo lại: scanner gốc 0 · chép trần ADR 0 · chép §5.1 0 · chép §12 **6** ⇒ hai phản
   chứng còn SỐNG. Skill khai ĐÚNG giới hạn và KHÔNG tự nhận đã đóng lớp; *cải thiện LỜI KHAI không
   sửa CƠ CHẾ*, và r5 không khai ngược lại.
11. **`ADAPTER-VUA-CON-TRO-VUA-CO-RANG` vẫn KHÔNG đóng** — `A18'` đo được `A1'`/`A2'` còn răng cho
   packet NÀY, và lượt 3 cho thấy chính phép chứng minh ấy từng có lỗ ở luật cấp tín dụng. Không
   khái quát cho mọi mục doctrine khác.
7. **Lượt cổng tự động trên `6b46012`**: tới lúc soạn r4 **chưa có lượt nào** (`actions_list` lọc theo
   `ci.yml`, head gần nhất của nhánh là `56cfce5`). `M10` cấm gọi tay, nên trạng thái là **KHÔNG ĐO
   ĐƯỢC**, không phải xanh. Lượt cổng của master cho chính commit merge #521 (`dc02c9b`, run
   `34702466800`) kết luận **`cancelled`** — ghi ra vì nó KHÔNG phải bằng chứng master xanh, và cũng
   không phải việc của packet này.

## `dieu_kien_dung` — kế thừa `S1`–`S8` của lease gen 3, thêm hai

- **`S9`** — một phép làm ĐỎ của `A9'`, `A17'`, `A18'`, `A19` hoặc `A20` **KHÔNG đỏ được**, tức một
  chốt MẤT RĂNG. Khi ấy **DỪNG và báo chủ kho**; KHÔNG nới tiêu chí cho hết đỏ, và KHÔNG dựng lại
  bản cũ để lách.
- **`S10`** — phát hiện cho thấy `A9'` (một phép đo) **cũng** bỏ lọt một cấu hình. Khi ấy DỪNG: đó
  là quyết định thiết kế của chủ kho, không phải chỗ executor tự đổi công thức lần thứ ba.
