# ĐẶC TẢ — `DANG-LEASE-DAU-TRUOC-KIEM-SAU` — **revision 3, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `DANG-LEASE-DAU-TRUOC-KIEM-SAU` |
| `revision` | **3** |
| `thay_the_cho` | revision 2, `c5b9a9465b658e43d76bf0d04b051b443d8b0e4e7b11ba775fdbd584c83e6778` |
| `packet_issue` | **#579** |
| `nguon_cap_viec` | Chỉ thị chủ kho 21-09-2026: *"#589, #592 vá đi, rồi cho qua 1 lần cross-review codex"*. r3 là hệ quả của lượt ấy — xem §11. Nguồn của r2:  *"Anh soạn r2 gói cả ba đi"* — trả lời cho ba chặn mà phiên điều phối trình cùng lượt (§0.2). |
| `review_class` | **`sensitive`** — chạm `ops/lease_publish.py`, tức cổng đọc lease (protocol §8). |
| `assurance_target` | **`human_audited`** — không đổi. **ĐÍNH CHÍNH lời khai của r2:** r2 viết `cross_approved` *"KHÔNG ĐẠT ĐƯỢC"* vì quota codex. Câu ấy **hết hiệu lực từ 08:24Z 21-09**: một lượt cross-review codex đã chạy trọn trên head `44a87d0` (§11). Hạn quota là trạng thái tại thời điểm đo, không phải thuộc tính của đường. |
| `executor` | `claude` |

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC** — trạng thái thứ ba làm cổng ĐỎ.

**r3 KHÔNG đổi bệnh, KHÔNG đổi Q1/Q2/Q4, KHÔNG đổi M1–M9.** Nó sửa BA khuyết tật của chính r2 mà
cross-review lượt 1 đo ra, cộng hai mục tiêu mới `M10`/`M11` cho hai finding về mã. Chi tiết bệnh,
cơ chế và hiện vật: đọc r1 §1.

---

## 0. Vì sao có revision 2, rồi revision 3

### 0.1 — Bốn quyết định của r1, GIỮ NGUYÊN

| câu | quyết định |
|---|---|
| **Q1** vá ở đâu | `kiem_github`: dò dấu "đã đăng" TRƯỚC, gọi `kiem()` SAU |
| **Q2** phạm vi | vá cổng + ghi nếp vào `CLAUDE.md`; `_kiem_bia_mo` giữ nguyên |
| **Q3** đường qua chặn write set | hỏi #578 và #570 nhả sớm; không cấp lease trước khi đo `NGƯỜI_GIỮ 0` |
| **Q4** bảo chứng | `human_audited` |

### 0.2 — Ba quyết định MỚI của r2

| câu | quyết định | mục |
|---|---|---|
| **Q5** write set trong lúc #578 còn giữ | **Thu hẹp tạm thời**: gỡ `ops/lease_publish_test.py` khỏi write set cho tới `2026-09-21T10:30:00Z`, rồi TRẢ LẠI | §2 |
| **Q6** vượt trần `ADR-0044` | **Khai lý do trong spec** — đúng một trong hai đường mà chính ADR cho phép | §8 |
| **Q7** chỗ lease lệch Q3 | **Hoà bằng r2**, không sửa r1 và không giả vờ Q3 đã được thoả mãn | §9 |

---

### 0.3 — Vì sao có revision 3

Cross-review `codex` lượt 1 (08:24Z 21-09, head `44a87d0`) ra verdict **`blocked`** với **5 finding
P2**. Ba trong năm là khuyết tật của CHÍNH r2, và §3.2 của protocol chốt: *finding cho thấy chính
spec thiếu thì verdict là `blocked` và đi qua một revision mới*. Nên r3 tồn tại vì bị BẮT, không
phải vì có ý tưởng mới.

| finding | r2 sai ở đâu | r3 sửa ở |
|---|---|---|
| `frozen-spec-effective-write-set` | một `spec_hash` đại diện HAI write set | §2 |
| `inherited-acceptance-contradicts-measurement` | kế thừa `A3`/`A5` mà chính phép đo của r2 đã bác | §5 |
| `spec-test-line-breakdown-drift` | phân rã `93/105/31` không tái lập được | §8 |

Hai finding còn lại là lỗi MÃ, đã vá trong `d3d45d0` và thành `M10`/`M11` ở §4.

## 1. Bệnh — không đổi

Đọc r1 §1. Tóm đúng một câu để người đọc r2 không phải nhảy tệp: `kiem_github` gọi `kiem()` ở
dòng đầu, mà `kiem()` ném `rc=8` cho lease hết hạn **trước** khi chốt `rc=9` của
`_kiem_comment_da_co` kịp chạy — nên một lease **đã đăng rồi mới hết hạn** không bao giờ tới
được nhánh `rc=9` mà workflow đã có sẵn và viết đúng.

**Đo lại 21-09-2026 để câu trên không thành lời khai cũ** (L5), `kiem_github` với `_doc_gh` giả,
nền `origin/master` `a1bbdc1`:

```
còn hạn + ĐÃ có dấu   ->  rc=9
HẾT HẠN + ĐÃ có dấu   ->  rc=8     <- bệnh, chưa vá
HẾT HẠN + KHÔNG dấu   ->  rc=8
còn hạn + KHÔNG dấu   ->  rc=0
```

## 2. `write_set` — MỘT tập duy nhất

Đây là chỗ r2 khác r1 rõ nhất, và nó phải đọc được mà không cần mở tệp lease nào.

| # | đường |
|---|---|
| 1 | `ops/lease_publish.py` |
| 2 | `CLAUDE.md` |
| 3 | `ops/lease_publish_test.py` |

**3 tệp**, tức vế TỆP của `ADR-0044:5` đạt. Vế DÒNG không đạt — xem §8.

### 2.0 — Vì sao r3 bỏ cách khai THEO THỜI GIAN của r2

r2 khai write set bằng một bảng hai hàng theo mốc `10:30Z` rồi tự tuyên bố như thế là tuân thủ
§3.2. **Cross-review lượt 1 bác đúng câu ấy** (`frozen-spec-effective-write-set`), và nó đúng:

> §3.2 đòi đổi **revision** khi write set đổi, và `effective_write_set` nằm TRONG `spec_hash`.
> Một băm khai hai phạm vi thì băm ấy còn định danh được BYTE, nhưng **không còn định danh được
> một write set bất biến**. Hai phiên cùng đọc `c5b9a946…` có thể chọn hai phạm vi khác nhau tuỳ
> đồng hồ và tuỳ lease chúng đang cầm.

Đó không phải lỗi chữ nghĩa. Write-set exclusion là thứ duy nhất chặn hai phiên ghi đè nhau, và
một hợp đồng mà hai bên đọc ra hai phạm vi thì nó **không chặn được gì**.

r2 nghĩ mình lách được vì đã khai TRƯỚC cả hai hình dạng. Nhưng khai trước một sự mơ hồ không làm
nó hết mơ hồ — nó chỉ làm người viết yên tâm. Cùng lớp với bài học *"một phép kiểm không thể đỏ thì
không phải bằng chứng"*.

**r3 khai MỘT tập ba đường.** Chuyện thu hẹp còn hai đường rồi trả lại là **LỊCH SỬ ĐÃ XẢY RA**,
ghi ở §2.1/§2.2 để đọc được vết, **không phải một hợp đồng còn hiệu lực**. Lease nào muốn một
write set khác thì cần một revision khác, đúng §3.2.

### 2.3 — Điều kiện §2.2 đã KHÔNG đạt lúc cấp `g3`, và r3 không sửa lịch sử

`g3` được cấp `05:45Z` 21-09, sớm hơn mốc `10:30Z` mà §2.2 của r2 đòi, và lúc ấy
`ai-dang-giu ops/lease_publish_test.py` vẫn ra `NGƯỜI_GIỮ 1`. Lease khai chỗ lệch ấy ở
`LECH_DIEU_KIEN_CAP` với `dat_khong: false`. Căn cứ duy nhất là chỉ thị mới của chủ kho, người
đã đặt ra §2.2 — chồng lấn với #578 là **CÓ Ý** và được chấp nhận tường minh.

**r3 KHÔNG khai rằng điều kiện ấy đã đạt, và KHÔNG hồi tố.** Nó chỉ thôi đòi một điều kiện mà
chính chủ kho đã bỏ qua có chủ đích. Một revision mới không được dùng để biến một ngoại lệ đã
cấp thành một sự tuân thủ hồi tố.

### 2.1 — Vì sao thu hẹp (Q5), và nó gỡ một thế kẹt có thật

Phiên #578 trình ba đường cho chủ kho lúc `20:07Z` 20-09; chủ kho chọn đường 1 và bảo *"soạn
commit cho tôi duyệt"*. Bản nháp nằm ở `claude/nhap-thu-hep-579-20260921` (`c78991c`).

Thế kẹt, viết bằng lời của chính bản nháp ấy và đã kiểm lại:

- Lease #578 đòi *"không còn người giữ nào NGOÀI chính nó"* trên `ops/lease_publish_test.py`.
- Lease #579 g1 **là** một người giữ — mà chính nó khai ở `DIEU_KIEN_BAT_DAU` rằng **không**
  chạm đường ấy trước 10:30Z.
- Nên hai bên chờ nhau, và kết cục duy nhất là #578 hết hạn lúc 10:30Z **mà chưa ghi một dòng**.

Giữ một đường mình tự khai là không dùng đúng là thứ write-set exclusion sinh ra để chặn. Gỡ nó
**không làm #579 mất việc nào trong cửa sổ ấy**, vì `A1`–`A6` vốn đã không đạt được trước 10:30Z.

**XUNG ĐỘT LỢI ÍCH, khai thẳng:** bản sửa do phiên **#578** soạn, và #578 là bên HƯỞNG LỢI. Phiên
ấy trình ba đường chứ không tự chọn; chủ kho chọn. Và phiên ấy **không** đẩy lên `ops/**` — hành
vi CẤP là lần push, và lần push ấy là việc của chủ kho.

### 2.2 — Đường TRẢ LẠI (g3), và vì sao nó phải nằm trong đặc tả chứ không trong một dòng ghi chú

**Thu hẹp KHÔNG tự đảo ngược.** Sau 10:30Z, nếu không ai làm gì thì #579 vẫn thiếu
`ops/lease_publish_test.py`, `A1`–`A6` vẫn không đạt, và packet dừng ở một PR tự khai CHƯA ĐỦ.
Đó là kết cục xấu nhất của Q5, nên nó được viết to ở đây.

| trường | giá trị |
|---|---|
| khi nào | sớm nhất `2026-09-21T10:30:00Z`, **và** chỉ sau khi đo lại `ai-dang-giu ops/lease_publish_test.py` (`rc` đọc TRỰC TIẾP) thấy không còn người giữ nào ngoài lease của chính #579 |
| ai làm | chủ kho cấp; phiên #579 xin; phiên #578 không dính vào |
| hình thức | **generation 3** của revision 2 này — KHÔNG phải một revision mới, vì mục tiêu và nghiệm thu không đổi |

> **r3 BÁC CÂU DƯỚI ĐÂY, giữ lại để đọc được vết.** r2 viết: *"§3.2 đòi revision mới khi đổi
> write set. r2 tuân thủ bằng cách khai **cả hai** hình dạng write set ngay trong đặc tả, nên bước
> g2 → g3 là thi hành đúng r2 chứ không phải một lần đổi phạm vi không có căn cứ."*
>
> Cross-review lượt 1 bác: khai trước hai hình dạng **không** thoả §3.2, vì `effective_write_set`
> nằm trong `spec_hash` — một băm khai hai phạm vi thì nó không còn định danh được write set nào.
> Xem §2.0. `g2` và `g3` vẫn là hai lease có thật đã cấp; thứ sai là lý lẽ r2 dùng để gọi đó là
> tuân thủ.

## 3. `ngoai_pham_vi`

| thứ CỐ Ý không làm | lý do |
|---|---|
| Sửa `_kiem_bia_mo` | Q2 giữ nguyên: đổi một cổng an toàn của hệ lease ⇒ packet RIÊNG theo §3.2. |
| Sửa `.github/workflows/ops-publish-lease.yml` | Q1 chốt vá ở cổng đọc; bước `đăng` đã có sẵn nhánh `rc=9` đúng. |
| Nới `_kiem_bia_mo` cho chạm XUYÊN PACKET | Khe `AG-T0-01B` đã lách BẢY lần; packet này không đụng và không đếm thêm lần nào. |
| Sửa hai tệp lease gen 1 của #566/#568 | Hiện vật ĐÃ CÔNG BỐ. Bản vá làm cổng thôi đỏ ở lượt SAU, không viết lại lịch sử. |
| Chạy CI tay / `workflow_dispatch` / lane `windows` | `manual_ci_budget: 0` đang hiệu lực. |
| Đăng lại hai lease gen 2 của #566/#568 | Đã đăng rồi (`rc=9` là đường đúng cho chúng sau bản vá). |

### 3.1 — Một LỜI KHAI CŨ mà packet này CỐ Ý để lại, và phải khai vì nó sẽ sai sau khi vá

`.github/workflows/ops-publish-lease.yml`, khối chú thích của bước `tìm lease vừa đổi`, mang đúng
câu mà `M5` sửa trong `t32`: *"chốt `posted_comment_id` lo phần không đăng trùng — đúng cho lease
ĐÃ đăng (rc=9, bỏ qua), sai cho lease chưa từng đăng"*.

Tệp ấy **cố ý ngoài write set** (Q1: không phải sửa một dòng YAML nào). Hệ quả đo được: sau khi
`M1` land, câu ấy **sai ở cả hai vế** chứ không chỉ một, và không ai sửa nó trong packet này.
Ghi ra đây để lần sau nó không bị đọc thành một chỗ mù — nó là một chỗ **đã biết và đã chọn**.

## 4. `muc_tieu`

`M1`–`M8` **giữ nguyên byte nghĩa** của r1 §4. Chép lại để r2 tự đủ:

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | `kiem_github` dò dấu "đã đăng" TRƯỚC khi gọi `kiem()`: có dấu ⇒ `Chan(RC_DA_DANG)` ngay. | `ops/lease_publish.py` |
| **M2** | Tiền kiểm miền fail-close: thiếu `lease_id`/`packet_issue`, hoặc `packet_issue` sai kiểu ⇒ `Chan(RC_NOI_DUNG)`, không ngoại lệ trần. | `ops/lease_publish.py` |
| **M3** | Không dấu ⇒ hành vi KHÔNG ĐỔI so `origin/master`: cùng thứ tự lỗi, cùng mã thoát — **kể cả khi lease mắc NHIỀU lỗi cùng lúc**. Vế sau là chỗ r2 khai thiếu và bản vá đầu làm sai; xem `M10`. | `ops/lease_publish.py` |
| **M4** | Docstring `kiem_github` khai GIÁ PHẢI TRẢ: lease đã đăng thì các chốt của `kiem()` không chạy nữa trên đường này. | `ops/lease_publish.py` |
| **M5** | Sửa docstring `t32` — bỏ vế sai *"đúng cho lease ĐÃ đăng (rc=9)"*, ghi lại đúng phép đo. | `ops/lease_publish_test.py` |
| **M6** | Ca mới phủ nửa còn thiếu: hết hạn + ĐÃ có dấu ⇒ `rc=9`; hết hạn + KHÔNG dấu ⇒ `rc=8`. | `ops/lease_publish_test.py` |
| **M7** | Ca mới cho M2: ba ca âm, và khai đúng ca nào THẬT SỰ có răng. | `ops/lease_publish_test.py` |
| **M8** | Nếp vào `CLAUDE.md`: bia mộ hai chiều chỉ dùng cho lease CÒN SỐNG. | `CLAUDE.md` |

### 4.1 — `M9`, MỚI ở r2: đóng nhánh mà không ca nào chạm

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M9** | Một ca phủ nhánh NUỐT của phép dò: `_kiem_comment_da_co` ném một lớp **ngoài họ `OSError`** ⇒ phép dò phải nhường lại cho chuỗi cũ phán, KHÔNG được tự kết luận "đã đăng" và KHÔNG được tự ném lỗi của mình thay cổng. | `ops/lease_publish_test.py` |

**`M9` sinh ra từ một ĐỘT BIẾN SỐNG SÓT, và đó là lý do nó tồn tại.** Lượt đo 21-09 dựng năm đột
biến cho `M1`–`M7`; bốn cái chết đúng ca của nó, cái thứ năm — nhánh nuốt ném `Chan(RC_DA_DANG)`
— **sống sót 10/10**. Không phải vì mã đúng: vì năm ca kia chỉ dựng hai hình dạng
(`_kiem_comment_da_co` thấy dấu, hoặc trả về êm), nên nhánh nuốt **chưa từng được chạy**.

Thêm một ca cho endpoint hỏng "tử tế" vẫn **không** đủ — `_doc_gh` bắt `OSError` rồi bọc mọi thứ
khác thành `Chan`, nên đột biến vẫn sống (đo: `11/11`). Chỉ một ngoại lệ lọt qua `_doc_gh` mới
phơi được nhánh ấy.

Đột biến sống sót ở đây là một khoảng **TRỐNG của bộ test**, không phải một chứng cứ về mã — và
đó chính là bài học `ĐỘT BIẾN SỐNG SÓT KHÔNG LUÔN NGHĨA LÀ TEST YẾU` đọc theo chiều còn lại.

### 4.2 — `M10` và `M11`, MỚI ở r3: hai finding về MÃ của cross-review lượt 1

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M10** | `_tien_kiem_mien_dang` phải nằm TRONG khối bắt `Chan` của `_do_dau_da_dang`, để dữ liệu thiếu miền làm phép dò **nhường** quyền phán cho chuỗi `kiem()` cũ thay vì tự phán. | `ops/lease_publish.py` |
| **M11** | Bộ test phải có ca `packet_issue: True` đo **cả mã thoát lẫn SỐ LỜI GỌI GitHub**, để chốt `isinstance(so, bool)` có răng. | `ops/lease_publish_test.py` |

**`M10` là một HỒI QUY THẬT, không phải một chỗ viết chưa đẹp.** Bản vá đầu đặt tiền kiểm NGOÀI
`try`, nên `Chan(RC_NOI_DUNG)` của nó thoát khỏi cả `kiem_github` và cướp quyền phán của `kiem()`.
Phản chứng của reviewer, tái hiện được — lease CHƯA ĐĂNG vừa tự cấp vừa có `packet_issue` sai kiểu:

    nền `origin/master`   -> rc=4   `kiem()` bắt authority trước
    bản vá đầu            -> rc=8   tiền kiểm bắn trước, ĐỔI thứ tự lỗi
    sau `M10`             -> rc=4   nhường lại, khớp nền

`M3` của r1/r2 khai *"cùng thứ tự lỗi, cùng mã thoát"*, và câu ấy **đúng khi lease mắc MỘT lỗi,
sai khi mắc HAI**. `t177` chỉ dựng từng lỗi RIÊNG nên không bắt được. Đây đúng lớp bài học
*"vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"*: một cổng đúng trên mọi lỗi đơn lẻ vẫn có thể
sai về THỨ TỰ khi hai lỗi gặp nhau.

**`M11` là một khoảng trống mà chính docstring của packet đã TỰ KHAI rồi để nguyên.** `t178` bản
đầu ghi nguyên văn *"KHÔNG ĐO: riêng ca `packet_issue: True`"*. Reviewer dựng đột biến gỡ đúng
điều kiện `bool` ấy và nó **sống sót `172/172`** — ba ca cũ đều không chạm nhánh bool, vì với
chuỗi `"55"` thì `not isinstance(so, int)` đã đủ ném.

Khai đúng cái lỗ mà không bịt nó thì lời khai ấy chỉ làm người viết yên tâm. Nó không phải một
phép đo, và nó **không** làm cổng đỏ.

## 5. `nghiem_thu`

**r2 KHAI SAI CHỖ NÀY, và r3 thôi kế thừa trọn gói.** r2 viết *"`A1`–`A11` giữ nguyên, trừ `A7`"*,
và câu ấy kéo vào hai tiêu chí mà **chính phép đo của r2 đã bác** — cross-review lượt 1 bắt
(`inherited-acceptance-contradicts-measurement`):

| tiêu chí r1 | nó đòi gì | đo được là gì |
|---|---|---|
| `A3` | đột biến **bỏ hẳn tiền kiểm** ⇒ ca *còn hạn + đã có dấu* ĐỎ | đột biến ấy làm `t176` **QUA** — cửa dò cuối vẫn trả `9` |
| `A5` | đột biến bỏ tiền kiểm miền ⇒ ném `KeyError`/`TypeError` **trần** | đo thật `rc=8/8/9`, **không ngoại lệ trần nào** |

`A5` đặc biệt đáng xấu hổ: `M5` sửa docstring `t32` vì **đúng** lý do ấy, rồi tiêu chí nghiệm thu
có thẩm quyền vẫn giữ nguyên câu sai. Sửa lời khai ở chỗ dễ thấy mà để nguyên ở chỗ có hiệu lực
thì chưa sửa gì cả.

`A1`, `A2`, `A4`, `A6`, `A8`–`A11` của r1 §5 giữ nguyên. `A3`, `A5`, `A7` viết lại; `A12`–`A14` mới.

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A3** (viết lại) | Lease **còn hạn + ĐÃ có dấu** ⇒ mã **9** (hành vi cũ, không đổi). | Đột biến **gỡ HAI CỬA** (cả dò sớm lẫn chốt cuối) ⇒ `t176` ĐỎ. **KHÔNG** dùng đột biến "bỏ hẳn tiền kiểm": đã đo, nó làm `t176` QUA vì cửa cuối vẫn trả 9. Một tiêu chí nêu sai đột biến là một tiêu chí không thể đỏ. |
| **A5** (viết lại) | **M2 fail-close**, và khai đúng ca nào có răng: thiếu `lease_id` ⇒ `rc=8` · thiếu `packet_issue` ⇒ `rc=8` · `packet_issue` sai kiểu ⇒ `rc=8` · `packet_issue` là `bool` ⇒ `rc=8`. | Đột biến bỏ tiền kiểm miền: hai ca THIẾU TRƯỜNG **không đổi gì** (bộ tương đương — `_do_dau_da_dang` nuốt `KeyError` rồi `kiem()` dựng lại `rc=8`); chỉ ca **sai kiểu** đổi `8 → 9`. Đo bằng `rc` **và** SỐ LỜI GỌI GitHub: `0 → 1`. **Không** đòi ngoại lệ trần — đã đo là không có. |
| **A7** (siết) | Suite `ops/lease_publish_test.py` **N/N hai số BẰNG NHAU**, `bỏ qua = 0`, và `N ≥ 173`. | `rc` đọc **trực tiếp**, không qua pipe. Nền 166 + 6 ca của r2 + `t180` của r3 = 173. Bất đẳng thức chứ không phải số tuyệt đối — #578 đang ghi cùng tệp, xem §2.3. |
| **A12** (mới, cho `M9`) | Đột biến cho nhánh nuốt ném `Chan(RC_DA_DANG)` ⇒ ca `M9` **ĐỎ**. Và đột biến bỏ điều kiện `if c.ma == RC_DA_DANG` (ném lại MỌI `Chan`) cũng ⇒ ca ấy **ĐỎ**. | Hai đột biến ấy **cùng lớp** (phép dò tự phán thay cổng), nên đừng khai chúng là hai chốt độc lập. Chúng chứng minh ca có răng, không chứng minh có hai cửa. |

| **A13** (mới, cho `M10`) | Lease **chưa đăng** mắc HAI lỗi cùng lúc — tự cấp **và** `packet_issue` sai kiểu — ⇒ `rc=4`, **bằng đúng nền `origin/master`**, và **0** lời gọi GitHub. | Đột biến đưa `_tien_kiem_mien_dang` trở ra NGOÀI `try` (tức khôi phục hồi quy) ⇒ ca ĐỎ. Đã đo: đột biến ấy giết **đúng một** ca, `t174`–`t179` đều QUA — nên ca này KHÔNG phải bộ tương đương với ca nào có sẵn. |
| **A14** (mới, cho `M11`) | `packet_issue: True` ⇒ `rc=8` **và 0 lời gọi GitHub**. | Đột biến gỡ điều kiện `isinstance(so, bool)`, giữ nguyên mọi thứ khác ⇒ ca ĐỎ. Trước `M11` đột biến ấy **sống sót `172/172`**. Nó ĐỎ qua SỐ LỜI GỌI (`0 → 1`), **không** qua mã thoát — mã thoát là `8` ở cả hai bên, nên một tiêu chí chỉ đọc `rc` sẽ mù đúng chỗ này. |

**Không tiêu chí nào đóng bằng `rc=0`.** Mỗi dòng đòi bằng chứng dương: hai số bằng nhau, một mã
thoát cụ thể, hoặc một đột biến ĐỔI MÀU đúng ca đích.

## 6. `hinh_dang_ke_thua`

| hình dạng | số lần | nguồn |
|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 4 → **5** | r1 đếm 4. **+1**: docstring `_tien_kiem_mien_dang` do chính phiên thi hành viết, khai *"thiếu trường sẽ thành `KeyError` TRẦN thoát ra khỏi cổng"* — đột biến gỡ hàm ấy ra **BÁC** câu đó: thiếu `lease_id` và thiếu `packet_issue` vẫn ra `rc=8`, vì phép dò vốn nuốt `KeyError`. Chỉ ca `packet_issue` SAI KIỂU mới đổi. Docstring đã viết lại theo đúng phép đo. |
| `DOT-BIEN-SONG-SOT-VI-NHANH-CHUA-AI-CHAM` | **1** | MỚI. Xem §4.1. Khác hẳn *"đột biến chưa từng được chạy"* (va chạm `.pyc`): ở đây đột biến CÓ chạy, mã CÓ đổi, mà không ca nào đi qua dòng ấy. |
| `VA-BANG-REGEX-RONG-HON-Y-DINH` | 1 | Chép từ #566. |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 2 | Chép từ #566. |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | 1 | #513 là gốc; ca mới: bản vá #195 đóng *"hết hạn + chưa đăng"* rồi bỏ sót *"hết hạn + đã đăng"*. |

**`LOI-KHAI-RONG-HON-PHEP-DO` chạm 5.** r1 §6 chốt: gặp lần thứ 5 thì DỪNG và hỏi có nên tiếp
cách làm này không. **ĐÃ DỪNG, ĐÃ HỎI, chủ kho trả lời 21-09: *"M5 cứ sửa docstring theo đúng
phép đo"*.** Nên cách làm giữ nguyên, và ràng buộc cũng giữ nguyên: mọi câu bản vá thêm vào phải
nêu phép đo đứng sau nó, hoặc nói thẳng KHÔNG ĐO ĐƯỢC.

Đáng ghi vì nó tự chứng minh ràng buộc ấy có răng: **lần thứ 5 bị bắt bởi chính một đột biến của
packet này**, không phải bởi một lượt review.

## 7. `chua_do_duoc`

1. **Số dòng thêm — NAY ĐÃ ĐO, không còn là ước.** Xem §8.
2. **`ops/lease_publish_test.py` còn người giữ.** Đo `05:0xZ` 21-09: `rc=11` · **NGƯỜI_GIỮ 2** —
   lease của chính #579 (`dang-lease-dau-truoc-kiem-sau-r1-g1-claude`) và
   `windows-fixture-posix-r1-g1-claude` (#578, hết `2026-09-21T10:30:00Z`).
   `wp570-bash-nen-r4-g4-claude` đã được phiên khác **thu hồi** bằng bia mộ hai chiều — câu
   *"wp570 vẫn giữ"* của r1 §7.2 nay **HẾT HIỆU LỰC**. Đo lại, đừng chép.
3. **Bẫy `ai-dang-giu` `rc=12` có HAI dạng, cả hai đều FAIL-CLOSE.** `NHÁNH_CỤC_BỘ_TỤT_SAU`
   (chữa: `rev-list --count` = 0 rồi `git branch -f`) và `KHÔNG_XÁC_ĐỊNH: cache thiếu nhánh máy
   chủ` (chữa: fetch lại — phiên khác vừa đẩy nhánh). Gặp cả hai trong ngày 20/21-09; dạng thứ
   hai r1 chưa khai.
4. **Bản vá có làm hai lượt đỏ kia thôi đỏ không** — **KHÔNG ĐO ĐƯỢC**: hai lượt ấy đã chạy xong
   trên head cũ và `manual_ci_budget: 0` cấm gọi lại. `A11` đo **cơ chế**; nó không thay được một
   lượt CI thật. Lời khai đúng sau khi vá là *"cơ chế đã đóng, chưa có lượt workflow nào chạy lại
   để xác nhận"*.
5. **`gate (windows-latest)`** — **CHỌN KHÔNG ĐO** theo `manual_ci_budget: 0`, không phải không
   đo được.
6. **`_kiem_bia_mo` vẫn đòi sửa tệp lease chết.** Q2 giữ nguyên. Nếp ở `M8` là thứ duy nhất canh
   chỗ đó, và **máy không canh nó**.
7. **Ca `bool` của `M2`** — `isinstance(True, int)` là `True` trong Python, nên `packet_issue: true`
   lọt phép kiểm kiểu ngây thơ. Tiền kiểm loại `bool` tường minh, nhưng **chưa có phép đo riêng
   cho ca ấy**; nó suy từ cùng cơ chế với ca chuỗi, và suy không phải đo.

## 8. Ngoại lệ `ADR-0044` — Q6

`ADR-0044` (Accepted 21-08-2026): packet `sensitive` **≤ 3 tệp và ≤ 300 dòng thêm**; vượt thì
*"dừng TRƯỚC review để revision thiết kế, **hoặc khai lý do trong spec**"*. Mục này là đường thứ hai.

**Phép đo, `05:0xZ` 21-09-2026, `git diff --numstat origin/master` trên cây đã hoàn chỉnh:**

| tệp | dòng thêm |
|---|---|
| `CLAUDE.md` | 27 |
| `ops/lease_publish.py` | 97 |
| `ops/lease_publish_test.py` | 272 |
| **tổng** | **396** (xoá 2) |

**3 tệp ⇒ vế TỆP ĐẠT. 396 > 300 ⇒ vế DÒNG KHÔNG ĐẠT, vượt 96.**

Số này đo trên head `d3d45d0` so `a1bbdc1`. Nó **lớn hơn con số 333 của r2** vì `M10`/`M11` thêm
một ca, một hình dạng và hai docstring giải thích hồi quy. Ngoại lệ vì thế **rộng hơn**, và nói
thẳng ra đây chứ không để nó trôi: vượt `33` và vượt `96` là hai mức khác nhau.

### 8.1 — Phân rã, và QUY ƯỚC ĐẾM, vì r2 khai một con số không tái lập được

**r2 khai `93` mã / `105` docstring-chú thích / `31` trống. Không bộ đếm nào tái lập được.**
Cross-review lượt 1 bắt (`spec-test-line-breakdown-drift`), và chỗ này đáng ghi vì nó là hình dạng
mà `CLAUDE.md` đã trả giá: **tổng vẫn đúng `229` trong khi mọi số hạng đều sai.** Một quan hệ đúng
trông y hệt các số hạng đúng.

Đau hơn: khi phiên điều phối tự nghi con số ấy và đếm lại, nó ra **`103` mã / `95` docstring** —
tức **cũng sai**, và sai theo một chiều khác. Ba bộ đếm, ba kết quả. Cái duy nhất kèm bản đồ từng
dòng là của reviewer.

Nên r3 **không khai một con số trần**. Nó khai con số KÈM quy ước, và quy ước ấy chạy được:

> Lấy các dòng `+` của `git diff --unified=0 <base> <head> -- <tệp>`, định vị từng dòng theo số
> dòng trong tệp HEAD. Dùng `ast` để lấy khoảng dòng của MỌI docstring. Phân loại: nằm trong
> khoảng docstring ⇒ `docstring` (kể cả dòng trống); ngoài ra rỗng ⇒ `trống`; ngoài ra bắt đầu
> bằng `#` ⇒ `chú thích`; còn lại ⇒ `mã`.

Đo `272` dòng thêm của `ops/lease_publish_test.py` theo đúng quy ước ấy:

| loại | số dòng |
|---|---|
| mã | **86** |
| docstring | **149** (trong đó **34** dòng trống nằm bên trong docstring) |
| chú thích đứng riêng | **10** |
| trống ngoài docstring | **27** |
| **tổng** | **272** |

**Lý do, và nó phải chịu được phản bác:** cắt 96 dòng là cắt vào phần docstring, vì 86 dòng mã
không cắt được mà không bỏ một ca. Mà docstring ở đây **không phải văn trang trí** — chúng mang
chính các phép đo làm cho từng ca có nghĩa: số `rc` của từng hình dạng, tên đột biến làm ca ĐỎ, và
ở `M9` là câu chuyện đột biến sống sót. Cắt chúng để vừa một con số là **tối ưu thước đo chống lại
mục đích của thước đo** — đúng lớp bệnh mà chính kho này đặt tên.

**Điều ngoại lệ này KHÔNG cho phép:**

- Không cho vượt vế **TỆP**. Ba đường là trần cứng; đường thứ tư vẫn làm `A8` ĐỎ.
- Không cho gọi cổng `ADR-0044` là **"ĐẠT"** ở bất kỳ đâu — thân PR, comment, hay báo cáo. Nó
  **VƯỢT TRẦN, CÓ NGOẠI LỆ ĐÃ DUYỆT**. Tiền lệ đã trả giá (`PLAT-X8`): con số trôi lần thứ tư khai
  sai rằng một thẩm quyền đã có.
- Không cho gia hạn sang packet sau. Ngoại lệ này chỉ cho **#579**, chỉ cho con số **396**; vượt
  thêm thì phải dừng và xin lại.
- **Và nó ĐÃ phải xin lại một lần.** r2 chốt ngoại lệ ở `333`; `M10`/`M11` đẩy lên `396`. Con số
  trong một ngoại lệ là một phần của ngoại lệ, không phải một chú thích — thay nó mà không khai
  là đúng thứ `spec-test-line-breakdown-drift` vừa bắt.

| trường | giá trị |
|---|---|
| `ai_nang` | `ducthangho` (OWNER) |
| `can_cu` | Chỉ thị trong phiên 21-09-2026, chọn đường *"Revision 2 — khai lý do"* khi được trình ba đường (revision 2 · cắt xuống dưới 300 · tách slice thứ hai) |
| `tran_cu` | 300 dòng thêm |
| `so_do_r2` | **333** dòng thêm, đo `05:0xZ` 21-09 trên head `44a87d0` — **vượt 33** |
| `so_do_that` | **396** dòng thêm, đo `08:5xZ` 21-09 trên head `d3d45d0` (sau `M10`/`M11`) |
| `vuot` | **96** |

## 9. Hoà chỗ lease lệch Q3 — Q7

Lease `dang-lease-dau-truoc-kiem-sau-r1-g1-claude` được cấp `19:48Z` 20-09 trong lúc
`ai-dang-giu ops/lease_publish_test.py` vẫn trả **NGƯỜI_GIỮ 2** — ngược vế sau của Q3. Lease tự
khai chỗ lệch ấy ở khoá `LECH_SO_VOI_SPEC` thay vì giấu.

**r2 hoà bằng cách sửa LUẬT, không bằng cách sửa lời khai.** Q3 của r1 giả định đúng một đường:
chờ tới khi sạch. Thực tế cho thấy đường ấy có thể **không bao giờ tới** — hai lease chờ nhau
(§2.1). Nên Q5 thay nó bằng một luật mô tả được cả thế kẹt:

> Đường bị giữ mà packet tự khai là **không dùng trong cửa sổ này** thì **gỡ khỏi write set** của
> generation hiện tại, kèm một đường TRẢ LẠI có mốc thời gian và người cấp. Không giữ một đường
> mình không dùng, và không chờ một điều kiện mà chính mình đang làm cho nó không xảy ra.

**KHÔNG khai rằng Q3 "đã được thoả mãn".** Nó không được thoả mãn. Lịch sử không sửa được: lúc cấp
g1, đường ấy vẫn trong write set và vẫn có người giữ.

**ĐÍNH CHÍNH của r3 với chính câu tiếp theo của r2.** r2 viết thêm rằng nó *"khiến trạng thái hiện
tại không còn lệch"*. Cross-review lượt 1 bác đúng câu ấy, và nó đúng: lease `g3` đang hiệu lực
vẫn mang `LECH_DIEU_KIEN_CAP` với `dat_khong: false`, và `ai-dang-giu ops/lease_publish_test.py`
vẫn ra `NGƯỜI_GIỮ 2`. Trạng thái hiện tại **vẫn lệch** — nó lệch CÓ Ý và được chấp nhận tường
minh, nhưng "được chấp nhận" không phải "không còn lệch".

Đây lại là một lời khai rộng hơn phép đo, nằm trong chính đoạn viết ra để tố cáo lời khai rộng
hơn phép đo. Ghi ra đây thay vì sửa lặng, vì vết ấy mới là thứ đáng giữ.

## 10. Thứ phải có trước khi coi packet là xong

1. Một lease của revision **3** đã cấp và đã đăng. `g3` neo `spec_hash` của r2; r3 đổi
   `nghiem_thu` và `write_set`, nên theo §3.2 nó cần một **generation mới** neo vào băm của r3.
   **Cấp lease là thẩm quyền chủ kho** — phiên #579 soạn và xin, không tự cấp.
2. `A1`–`A14` đều có phép đo dương, `rc` đọc TRỰC TIẾP.
3. Thân PR khai `ADR-0044` là **VƯỢT TRẦN + CÓ NGOẠI LỆ** ở mức **96 dòng**, dẫn §8 — không khai
   "ĐẠT", và không dùng lại con số `33` của r2.
4. `human_audited`: một lượt thẩm định của NGƯỜI trên head thật. **Packet này KHÔNG LAND ĐƯỢC
   BẰNG MÁY**, và chữ ký không thay được phép đo. Một lượt cross-review máy đã chạy (§11) —
   nó **không** cấp được `human_audited`, và verdict của nó tự nói đúng điều đó.

## 11. Cross-review lượt 1 — `codex`, `blocked`, và r3 là hệ quả

| trường | giá trị |
|---|---|
| reviewer | `codex` (`codex-cli 0.155.1`), `model_reasoning_effort=xhigh` |
| `reviewed_sha` | `44a87d0701eef3b984394a5157337a70d8800a76` |
| lúc | `08:24Z` 21-09-2026, chạy trọn, `rc=0`, 182.678 token |
| verdict | **`blocked`** |
| finding | 5 × P2 |
| bảng săn | 19 hướng, mỗi hướng có lệnh + output thật |
| đột biến | 7 (`A`–`G`), chạy toàn suite, hoàn nguyên sạch |

**Reviewer TÁI LẬP được phần lớn lời khai của executor**, và đó cũng là một kết quả: suite
`172/172`, numstat từng số hạng, `release-verify` `180 == 180`, bốn cổng `rc=0`, spec khớp từng
byte với blob, phân vùng với #578 rỗng ở cả base lẫn head. `A`/`B` đỏ **ngược chiều thật**, và
`A`–`F` đều chết bằng `TinHieuChotCa` của đúng ca đích — không cái nào ăn tín dụng giả.

Năm finding:

| slug | lớp | đã xử |
|---|---|---|
| `unposted-error-precedence-changes` | MÃ — hồi quy thứ tự lỗi | vá ở `d3d45d0`, thành `M10`/`A13` |
| `boolean-precheck-mutant-survives` | TEST — đột biến sống sót | vá ở `d3d45d0`, thành `M11`/`A14` |
| `spec-test-line-breakdown-drift` | SPEC — số hạng trôi | §8.1 |
| `frozen-spec-effective-write-set` | SPEC — một băm hai write set | §2/§2.0 |
| `inherited-acceptance-contradicts-measurement` | SPEC — kế thừa tiêu chí đã bị bác | §5 |

**Ba finding cuối là của CHÍNH r2**, nên `blocked` là verdict đúng theo §3.2 chứ không phải
reviewer khó tính. Một đặc tả tự mâu thuẫn không vá được bằng một dòng ghi chú.

**Điều đáng giữ nhất từ lượt này** không phải năm finding mà là hình dạng của chúng: **bốn trong
năm là chỗ packet TỰ KHAI rồi không đi tiếp.** `t178` tự khai *"KHÔNG ĐO ca bool"*. `M3` tự khai
*"cùng thứ tự lỗi"* mà chỉ thử từng lỗi riêng. r2 tự khai hai write set rồi tuyên bố là tuân thủ.
r2 tự khai kế thừa `A1`–`A11` mà không đọc lại `A3`/`A5`. Không cái nào là chỗ tối; tất cả đều
được viết ra, đọc qua, rồi để nguyên.

Lời khai trung thực về một khoảng trống **không lấp được khoảng trống ấy** — nó chỉ làm người viết
yên tâm rằng mình đã trung thực. Chỉ một phép đo mới đóng được, và ở đây phép đo ấy phải do người
khác chạy.
