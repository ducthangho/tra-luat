# ĐẶC TẢ — `DANG-LEASE-DAU-TRUOC-KIEM-SAU` — **revision 6, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `DANG-LEASE-DAU-TRUOC-KIEM-SAU` |
| `revision` | **6** |
| `thay_the_cho` | revision 5, `e0a496af20b4620102c2b01adecd327f3b3946b81ab11ebab15494e3a6495ae2` |
| `packet_issue` | **#579** |
| `nguon_cap_viec` | Chỉ thị chủ kho 21-09-2026: *"Chạy lặp cross review, vá, đăng verdict cho tới khi approve. Không CI, full CI. Chạy với #589, #592 và các PR chưa merge trong phiên"* và *"nới lên 10. chạy đến approve"*. r6 là hệ quả của cross-review lượt 5 — xem §12.4. Chỉ thị 21-09: *"Không CI, full CI cho tới khi đủ điều kiện merge. Chạy lặp vá, cross review theo phân lớp lỗi… lặp tới khi có cross approval."* Nguồn của r3: *"#589, #592 vá đi, rồi cho qua 1 lần cross-review codex"* (§11). Nguồn của r2: *"Anh soạn r2 gói cả ba đi"* (§0.2). |
| `review_class` | **`sensitive`** — chạm `ops/lease_publish.py`, tức cổng đọc lease (protocol §8). |
| `assurance_target` | **`human_audited`** — không đổi. **ĐÍNH CHÍNH lời khai của r2:** r2 viết `cross_approved` *"KHÔNG ĐẠT ĐƯỢC"* vì quota codex. Câu ấy **hết hiệu lực từ 08:24Z 21-09**: một lượt cross-review codex đã chạy trọn trên head `44a87d0` (§11). Hạn quota là trạng thái tại thời điểm đo, không phải thuộc tính của đường. |
| `executor` | `claude` |

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC** — trạng thái thứ ba làm cổng ĐỎ.

**r4 KHÔNG đổi bệnh, KHÔNG đổi `write_set`, KHÔNG đổi Q1–Q7, KHÔNG đổi M1–M11.** Nó sửa HAI lời
khai đã trôi của chính r3 mà cross-review lượt 3 đo ra, và thêm ba tiêu chí nghiệm thu cho ba ca
test mà lượt 2 và lượt 3 sinh ra. Vì `write_set` và `muc_tieu` KHÔNG đổi, r4 là một revision của
LỜI KHAI, không phải của phạm vi — nhưng §3.2 vẫn đòi một revision mới, vì `nghiem_thu` đổi.

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

### 0.4 — Vì sao có revision 4

Cross-review `codex` **lượt 3** (head `e2aa580`) ra `changes_requested` với **1 P2 + 3 P3**. Hai
cái vá được bằng mã đã vá ở `dea83a1`. **Hai cái còn lại là khuyết tật của CHÍNH r3**, nên lại
đúng §3.2: spec thiếu thì đi qua revision mới.

| finding | r3 sai ở đâu | r4 sửa ở |
|---|---|---|
| `post-fix-boolean-evidence-claims-drift` (vế spec) | §7.7 vẫn viết *"chưa có phép đo riêng cho ca bool"* trong khi `M11`/`A14`/`t178` đã đo | §7 |
| `spec-current-size-evidence-stale` | §8/§10 dùng số đo head CŨ (`396`, head `d3d45d0`) làm điều kiện hoàn tất HIỆN HÀNH | §8, §10 |

**Cả hai cùng một hình dạng, và hình dạng ấy là thứ đáng ghi**: r3 viết đúng ở chỗ nó đang sửa,
rồi để nguyên câu cũ ở chỗ có hiệu lực. `M11` sửa mã và `A14` sửa tiêu chí — mà §7 `chua_do_duoc`,
tức nơi packet TỰ KHAI mình còn mù, vẫn giữ câu "chưa đo". Y hệt `A5` của r2 mà chính r3 gọi là
*"đặc biệt đáng xấu hổ"*: **sửa lời khai ở chỗ dễ thấy mà để nguyên ở chỗ có hiệu lực thì chưa sửa
gì cả.** Lần này nạn nhân là đoạn viết ra để tố cáo đúng lỗi đó.

Đây là lần thứ **hai liên tiếp** cross-review đóng một finding SPEC thuộc lớp *"con số / lời khai
trôi sau khi head đổi"* (lượt 1: `spec-test-line-breakdown-drift`; lượt 3: hai cái trên). Chốt rút
ra, ghi ở đây để lần sau khỏi lặp: **mỗi lần head đổi, §7 và §8 phải được ĐO LẠI, không phải đọc
lại.** Một con số trong đặc tả không ghi ĐIỀU KIỆN ĐO thì sẽ trôi mà không ai biết.

### 0.6 — Vì sao có revision 6

Cross-review `codex` **lượt 5** — lượt ĐẦU chạy theo **trục LỚP** thay vì trục ĐIỂM, theo chỉ
thị chủ kho 21-09-2026: *"Cross-review tìm kiếm, phân theo LỚP, không phải từng lỗi riêng lẻ."*

Kết quả: **2/2 slug lượt 4 `ĐÃ VÁ THẬT`**, **4 P3 mới**, **KHÔNG P1/P2**. Hai P3 về MÃ đã vá ở
`94d3cd9`. Hai P3 dưới đây là khuyết tật của CHÍNH r5.

| finding | r5 sai ở đâu | r6 sửa ở |
|---|---|---|
| `spec-active-ci-budget-contradicts-done-condition` | §3 nói `manual_ci_budget: 0` **đang hiệu lực**, §10.5 nói đã gỡ và đòi full CI — hai chỉ thị CÒN HIỆU LỰC ngược nhau | §3, §10.5 |
| `spec-guarantees-still-lack-adjacent-measurements` | §2 viết ba vế "KHÔNG đổi" rồi để nguyên lời văn, **không áp chính luật §0.5 vừa đặt ra** | §2 |

**Đổi trục cho kết quả sâu hơn hẳn bốn lượt trước, và đó là dữ liệu chứ không phải cảm giác:**

```
L1  2.788 phép đo trên 22 ca qua `_goi_lop_gh`, 41 vị trí gọi, 68 nhãn factory
L2  kiểm kê 572 vị trí assertion (303 `bang`, 254 `chot`, 15 `assert`) bằng AST
L3  quét cả 743 dòng của r5, 75 dòng ứng viên mang lời BẢO ĐẢM
```

**Và lớp `L6 — DONG-NHAT-DIEU-KIEN-HIEU-LUC` là lớp REVIEWER TỰ NGHĨA RA.** Nó không có trong
danh sách lớp mà prompt giao. Đó là đóng góp lớn nhất của lượt 5, và nó phát biểu một thứ mà
năm revision trước không ai nêu: **hai câu cùng còn hiệu lực trong một đặc tả phải không được
chỉ đạo ngược nhau.** Một đặc tả tự mâu thuẫn không cần ai đo sai — người thực thi chỉ cần đọc
đúng phần của mình.

Mâu thuẫn ấy **đã cắn thật** trước khi r6 tồn tại: 21-09 phiên điều phối chạy
`rerun_workflow_run` sáu lượt — việc §3 liệt là ngoài phạm vi, còn §10.5 đòi phải làm.

### 0.5 — Vì sao có revision 5

Cross-review `codex` **lượt 4** (head `dea83a1`) ra `changes_requested`: **4/4 slug lượt 3 phán
`ĐÃ VÁ THẬT`**, **2 P3 mới**, **KHÔNG P1/P2 mới**. Một P3 là lỗi TEST (vá ở `d38de01`); một là
lỗi của CHÍNH r4.

| finding | r4 sai ở đâu | r5 sửa ở |
|---|---|---|
| `spec-section2-byte-preservation-false` | §2 khai *"giữ nguyên từng chữ"* trong khi câu cuối §2 đã đổi | §2 |

**Và cái chốt rút ra ở §0.4 vừa bị chính r4 vi phạm.** §0.4 viết: *"mỗi lần head đổi, §7 và §8
phải được ĐO LẠI"*. r4 làm đúng thế cho §7/§8 — rồi thêm một lời khai MỚI ở §2 mà không đo. Tức
không phải doctrine sai, mà là doctrine chỉ phủ đúng chỗ đã cháy lần trước. Hình dạng thật rộng
hơn: **bất kỳ câu nào mang một lời BẢO ĐẢM (byte-identical, không đổi, đã đạt, không còn) đều
phải có phép đo đứng ngay sau nó** — không riêng các con số ở §7/§8.

Đây là lần thứ **ba liên tiếp** một finding SPEC của packet này thuộc lớp `LOI-KHAI-RONG-HON-
PHEP-DO` (lượt 1, lượt 3, lượt 4). §6 đã ghi nó ở mức 5; r5 nâng thành 6.

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

**ĐÍNH CHÍNH MỘT LỜI KHAI SAI CỦA r4, VÀ NÓ NẰM ĐÚNG CHỖ NÀY.** r4 mở §2 bằng câu
*"r4 GIỮ NGUYÊN toàn bộ §2, từng chữ."* **Câu ấy SAI**, và nó sai trong chính cái sửa viết ra
nó: cùng lượt ấy đã đổi câu cuối của §2 (*"Vế DÒNG không đạt"* → *"Vế DÒNG vượt trần GỐC nhưng
trong trần đã nới"*). Cross-review lượt 4 bắt (`spec-section2-byte-preservation-false`) bằng một
phép so BYTE trên nguyên §2 của hai blob, và còn đi thêm một bước mà tôi không nghĩ tới: **bỏ
riêng đoạn dẫn mới ra rồi đọc lời khai theo cách rộng lượng nhất** — vẫn `false`.

**Khai lại cho ĐÚNG PHẠM VI, và đây là câu chịu trách nhiệm được:**

- **`write_set` KHÔNG đổi** qua r3 → r4 → r5 → r6: vẫn đúng ba đường dưới đây.
- **Các tiểu mục lịch sử §2.0 · §2.1 · §2.2 · §2.3 KHÔNG đổi.** Mọi câu trong chúng nói *"r3"*
  còn đúng nguyên.
- **Câu diễn giải vế DÒNG của `ADR-0044` ĐÃ ĐỔI ở r4**, theo trần mới — hợp lệ, và §8 là nơi có
  thẩm quyền cho nó.

**PHÉP ĐO CHO BA VẾ TRÊN — đo từ BLOB, ngay tại đây.** r5 viết ba vế ấy rồi để nguyên lời văn,
và cross-review lượt 5 bắt đúng chỗ đó (`spec-guarantees-still-lack-adjacent-measurements`):
r5 tự đặt luật *"mọi câu mang lời BẢO ĐẢM phải có phép đo đứng ngay sau nó"* ở §0.5 rồi **không
áp luật ấy cho chính §2 vừa viết**. Reviewer đo lại và ba vế ĐÚNG — lỗi là thiếu chứng cứ TẠI
CHỖ, không phải sai nội dung.

| vế | r3 → r4 | r4 → r5 |
|---|---|---|
| bảng `write_set` ba đường giống nhau | `True` | `True` |
| §2.0 byte-equal | `True` | `True` |
| §2.1 byte-equal | `True` | `True` |
| §2.2 byte-equal | `True` | `True` |
| §2.3 byte-equal | `True` | `True` |
| câu vế DÒNG | **ĐỔI** (`không đạt` → `vượt trần GỐC nhưng trong trần đã nới`) | giữ nguyên |

Lệnh tái lập, chạy được, không cần mạng:

```
git show c58d728:ops/specs/dang-lease-dau-truoc-kiem-sau-r3.md   # r3
git show e816f86:ops/specs/dang-lease-dau-truoc-kiem-sau-r4.md   # r4
git show bb7694e:ops/specs/dang-lease-dau-truoc-kiem-sau-r5.md   # r5
```
cắt từng tiểu mục theo cặp tiêu đề (`### 2.0` → `### 2.3`, …) rồi so `==` trên chuỗi.

Bài học, ghi ra vì nó là lần thứ BA liên tiếp cùng một lớp trên packet này: **đừng khai "byte-
identical" cho một mục mình vừa sửa.** Lời bảo đảm càng mạnh thì càng dễ sai, và một lời bảo đảm
về BYTE thì chỉ cần một ký tự là đổ. Muốn nói "phần lớn giữ nguyên" thì phải liệt kê ĐÚNG cái
giữ và ĐÚNG cái đổi — như ba gạch đầu dòng trên.

Đây là chỗ r2 khác r1 rõ nhất, và nó phải đọc được mà không cần mở tệp lease nào.

| # | đường |
|---|---|
| 1 | `ops/lease_publish.py` |
| 2 | `CLAUDE.md` |
| 3 | `ops/lease_publish_test.py` |

**3 tệp**, tức vế TỆP của `ADR-0044:5` đạt. Vế DÒNG vượt trần GỐC nhưng trong trần đã nới — xem §8.

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
| ~~Chạy CI tay / `workflow_dispatch` / lane `windows`~~ | **DÒNG NÀY HẾT HIỆU LỰC TỪ r6.** `manual_ci_budget: 0` đã được chủ kho GỠ cho đợt 21-09-2026; việc ấy nay là **ĐIỀU KIỆN HOÀN TẤT**, xem §10.5. Giữ dòng gạch để người đọc r1–r5 thấy nó đã đổi, không xoá lặng. |
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

`A1`, `A2`, `A4`, `A6`, `A8`–`A11` của r1 §5 giữ nguyên. `A3`, `A5`, `A7` viết lại ở r3;
`A12`–`A14` mới ở r3; `A15`–`A17` mới ở r4; **`A16` viết lại và `A18`–`A19` mới ở r5**.

**Vì sao `A15`–`A17` phải có, và vì sao chúng là khuyết tật của r3 chứ không phải bổ sung tuỳ ý:**
`t181`, `t182`, `t183` đã tồn tại trong mã (hai ca đầu từ lượt 2, ca cuối từ lượt 3) và docstring
của chúng viện dẫn `A15`/`A16`/`A17` — nhưng bảng nghiệm thu của r3 chỉ có tới `A14`. Một ca test
viện dẫn một tiêu chí KHÔNG TỒN TẠI thì cái nó viện dẫn không ràng buộc được gì: nó đọc như đã có
thẩm quyền trong khi không có. Cùng lớp *"cổng vắng mặt trông giống cổng xanh"*.

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A3** (viết lại) | Lease **còn hạn + ĐÃ có dấu** ⇒ mã **9** (hành vi cũ, không đổi). | Đột biến **gỡ HAI CỬA** (cả dò sớm lẫn chốt cuối) ⇒ `t176` ĐỎ. **KHÔNG** dùng đột biến "bỏ hẳn tiền kiểm": đã đo, nó làm `t176` QUA vì cửa cuối vẫn trả 9. Một tiêu chí nêu sai đột biến là một tiêu chí không thể đỏ. |
| **A5** (viết lại) | **M2 fail-close**, và khai đúng ca nào có răng: thiếu `lease_id` ⇒ `rc=8` · thiếu `packet_issue` ⇒ `rc=8` · `packet_issue` sai kiểu ⇒ `rc=8` · `packet_issue` là `bool` ⇒ `rc=8`. | Đột biến bỏ tiền kiểm miền: hai ca THIẾU TRƯỜNG **không đổi gì** (bộ tương đương — `_do_dau_da_dang` nuốt `KeyError` rồi `kiem()` dựng lại `rc=8`); chỉ ca **sai kiểu** đổi `8 → 9`. Đo bằng `rc` **và** SỐ LỜI GỌI GitHub: `0 → 1`. **Không** đòi ngoại lệ trần — đã đo là không có. |
| **A7** (siết) | Suite `ops/lease_publish_test.py` **N/N hai số BẰNG NHAU**, `bỏ qua = 0`, và `N ≥ 173`. | `rc` đọc **trực tiếp**, không qua pipe. Nền 166 + 6 ca của r2 + `t180` của r3 = 173. Bất đẳng thức chứ không phải số tuyệt đối — #578 đang ghi cùng tệp, xem §2.3. |
| **A12** (mới, cho `M9`) | Đột biến cho nhánh nuốt ném `Chan(RC_DA_DANG)` ⇒ ca `M9` **ĐỎ**. Và đột biến bỏ điều kiện `if c.ma == RC_DA_DANG` (ném lại MỌI `Chan`) cũng ⇒ ca ấy **ĐỎ**. | Hai đột biến ấy **cùng lớp** (phép dò tự phán thay cổng), nên đừng khai chúng là hai chốt độc lập. Chúng chứng minh ca có răng, không chứng minh có hai cửa. |

| **A13** (mới, cho `M10`) | Lease **chưa đăng** mắc HAI lỗi cùng lúc — tự cấp **và** `packet_issue` sai kiểu — ⇒ `rc=4`, **bằng đúng nền `origin/master`**, và **0** lời gọi GitHub. | Đột biến đưa `_tien_kiem_mien_dang` trở ra NGOÀI `try` (tức khôi phục hồi quy) ⇒ ca ĐỎ. Đã đo: đột biến ấy giết **đúng một** ca, `t174`–`t179` đều QUA — nên ca này KHÔNG phải bộ tương đương với ca nào có sẵn. |
| **A14** (mới, cho `M11`) | `packet_issue: True` ⇒ `rc=8` **và 0 lời gọi GitHub**. | Đột biến gỡ điều kiện `isinstance(so, bool)`, giữ nguyên mọi thứ khác ⇒ ca ĐỎ. Trước `M11` đột biến ấy **sống sót `172/172`**. Nó ĐỎ qua SỐ LỜI GỌI (`0 → 1`), **không** qua mã thoát — mã thoát là `8` ở cả hai bên, nên một tiêu chí chỉ đọc `rc` sẽ mù đúng chỗ này. |
| **A15** (mới ở r4, cho `t181`) | API `/comments` hỏng **vĩnh viễn** ⇒ cổng vẫn PHẢI chặn, không được coi "không đọc được" là "chưa đăng". | Đột biến **I** — gỡ hẳn lời gọi `_kiem_comment_da_co` ở cửa cuối của `kiem_github` ⇒ `t181` ĐỎ, và đỏ bằng `TinHieuChotCa` của chính nó. Đo lượt 2: toàn suite `174/175`, đỏ ĐÚNG MỘT ca. **Phép đếm `== 3` lời gọi trong ca này ghim SỐ INVOCATION của cài đặt hiện tại, KHÔNG tự chứng minh ba cửa độc lập** — reviewer lượt 3 (N3) đo ra điều đó, và r4 khai thẳng thay vì để người đọc suy ra một điều mạnh hơn phép đo. |
| **A16** (mới ở r4, **viết lại ở r5**, cho `t182`) | `lease` KHÔNG PHẢI ánh xạ (`None` · `[]` · `True` · `55` · `"55"`) ⇒ `Chan(rc=8)` **CÓ TÊN**, và **0** lời gọi GitHub. Không ngoại lệ TRẦN nào thoát khỏi cổng. | Đột biến **J** — đưa chốt HÌNH DẠNG trở vào trong `try` của `_do_dau_da_dang` ⇒ `t182` ĐỎ, **bằng chot RIÊNG của nó**. Đo `d38de01`: J ⇒ `176/177`, đỏ ĐÚNG MỘT ca, thông điệp *"lease là None: phải ném `Chan(rc=8)` có tên, được rc=KHÔNG-CÓ-MÃ (ngoại lệ TRẦN AttributeError: …)"*. **r5 đổi CƠ CHẾ, không đổi tiêu chí:** r4 đạt vế "tín hiệu riêng" bằng một helper dành RIÊNG cho `t182` (`_goi_bat_tron`); lượt 4 chứng minh cách ấy ĐÚNG mà HẸP (xem `A19`), nên `_goi_lop_gh` nay lo việc đó cho MỌI ca và helper riêng đã gỡ. |
| **A18** (mới ở r5, cho `t179`) | Phép dò ném một ngoại lệ **KHÔNG PHẢI `Chan`** ⇒ vẫn phải NHƯỜNG cho `kiem()` phán (`rc=4` cho lease tự cấp), và ca phải ĐỎ **bằng chot của chính nó** khi nhánh nuốt bị gỡ. | Đột biến **X** — nhánh `except Exception` của `_do_dau_da_dang`: `return` → `raise`. Đo `d38de01`: `176/177`, đỏ ĐÚNG `t179`, thông điệp *"ngoại lệ lạ từ phép dò cũng phải nhường cho `kiem()` (rc=4), được rc=KHÔNG-CÓ-MÃ (ngoại lệ TRẦN RuntimeError: …)"*. Trước `A19`, `X` làm `t179` đỏ bằng `RuntimeError` **thoát ra trước** chot — tức tín dụng giả, đúng thứ `A16` đã phải sửa một lần cho `t182`. |
| **A19** (mới ở r5, cho `t184` — ĐO CHÍNH CÁI THƯỚC ĐO) | `_goi_lop_gh` giữ **nguyên** hợp đồng cũ và thêm ĐÚNG một hình dạng: (a) cổng ném `Chan` ⇒ trả chính `Chan` ấy · (b) cổng ném ngoại lệ TRẦN ⇒ trả `_NgoaiLeLa`, `.ma` **`==` SAI** và **`!=` ĐÚNG** với mọi mã thoát, `str(.ma)` **nêu TÊN LỚP** · (c) không ném gì ⇒ `None` · (d) `KeyboardInterrupt` **KHÔNG** bị nuốt. | Mỗi vế một đột biến, chạy TOÀN suite trên bản sao rời, đo trên `d38de01` (nền `177/177`): `N1` helper trả `None` ⇒ ĐỎ đúng vế (b) · `N2` `except Exception`→`BaseException` ⇒ vế (d) · `N3` `__eq__`→`True` ⇒ vế (b `==`) · `N3b` `__ne__`→`False` ⇒ vế (b `!=`) · `N4` `__str__` bỏ tên lớp ⇒ vế (b `str`) — cả năm `176/177`, đỏ ĐÚNG MỘT ca. `N5` gộp `Chan` vào `_NgoaiLeLa` ⇒ `159/177` và `N6` trả `_NgoaiLeLa` khi không ném gì ⇒ `168/177`, cả hai gồm vế (a)/(c). **KHAI CHO ĐÚNG: `N5`/`N6` KHÔNG phải đột biến một-đích** — chúng phá hợp đồng cũ nên kéo theo nhiều ca; điều đó chứng minh vế (a)/(c) có răng, KHÔNG chứng minh chúng là chốt duy nhất cho hợp đồng ấy. |
| **A17** (mới ở r4, cho `t183`) | Phép dò đầu **KHÔNG ĐO ĐƯỢC** (mạng hỏng) rồi mạng **PHỤC HỒI** ⇒ cửa CUỐI vẫn phải trả `rc=9` cho một lease đã đăng, và phải có **≥ 2** lần đọc `/comments`. | Đột biến **K** — giữ nguyên lời gọi ở cửa cuối nhưng NUỐT riêng `Chan(RC_DA_DANG)` ⇒ `t183` ĐỎ. Trước `t183`, K **sống sót `175/175`**: cửa cuối CÓ MẶT, đủ ba lời gọi, mà PHÁN QUYẾT của nó không ai đo. Đo `dea83a1`: nền `176/176` ⇒ K `175/176`, đỏ ĐÚNG MỘT ca, bằng chính assertion của `t183`. Vế `>= 2` là bắt buộc: thiếu nó thì ca vẫn xanh cho một cài đặt **chưa hề thử lại**. |

**Không tiêu chí nào đóng bằng `rc=0`.** Mỗi dòng đòi bằng chứng dương: hai số bằng nhau, một mã
thoát cụ thể, hoặc một đột biến ĐỔI MÀU đúng ca đích.

## 6. `hinh_dang_ke_thua`

| hình dạng | số lần | nguồn |
|---|---|---|
| `LOI-KHAI-RONG-HON-PHEP-DO` | 5 → **6** | r1 đếm 4. **+1**: docstring `_tien_kiem_mien_dang` do chính phiên thi hành viết, khai *"thiếu trường sẽ thành `KeyError` TRẦN thoát ra khỏi cổng"* — đột biến gỡ hàm ấy ra **BÁC** câu đó: thiếu `lease_id` và thiếu `packet_issue` vẫn ra `rc=8`, vì phép dò vốn nuốt `KeyError`. Chỉ ca `packet_issue` SAI KIỂU mới đổi. Docstring đã viết lại theo đúng phép đo. |
| `DOT-BIEN-SONG-SOT-VI-NHANH-CHUA-AI-CHAM` | **1** | MỚI. Xem §4.1. Khác hẳn *"đột biến chưa từng được chạy"* (va chạm `.pyc`): ở đây đột biến CÓ chạy, mã CÓ đổi, mà không ca nào đi qua dòng ấy. |
| `VA-BANG-REGEX-RONG-HON-Y-DINH` | 1 | Chép từ #566. |
| `TIN-HIEU-DO-CHINH-MA-TEST-GIA-MAO` | 2 | Chép từ #566. |
| `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` | 1 → **2** | #513 là gốc; ca của r1: bản vá #195 đóng *"hết hạn + chưa đăng"* rồi bỏ sót *"hết hạn + đã đăng"*. **+1 ở r5**: bản vá lượt 3 cho `t182` (helper riêng cho MỘT ca) rồi lượt 4 tìm ra `t179` cùng lớp. Chữa bằng KIẾN TRÚC — đóng `_goi_lop_gh`, đường duy nhất 20+ ca đi qua — chứ không bằng ca thứ hai. |
| `CHOT-DO-SAI-TOAN-TU` | **1** | MỚI ở r5, và nó bắt được BỞI CHÍNH mình. `t184` vế (b) bản đầu chỉ chốt `all(ma != m …)`. Đột biến `N3` cho `_MaVang.__eq__` trả `True` mà để nguyên `__ne__` ⇒ **SỐNG SÓT `177/177`**. Mà MỌI ca trong tệp chốt bằng `ma == RC_X` ⇒ với `N3` một ngoại lệ trần khớp MỌI mã thoát và cả loạt ca thành XANH GIẢ. Vế `!=` đo đúng thứ **không ai dùng**. Python KHÔNG suy `__ne__` từ `__eq__` khi cả hai khai tường minh. Nay chốt CẢ HAI toán tử (`N3` và `N3b` mỗi cái giết đúng một vế). |
| `DEM-SU-CO-MAT-THAY-VI-KHA-NANG` | **1** | MỚI ở r4. Cửa cuối `_kiem_comment_da_co` CÓ MẶT, có đủ ba lời gọi API, và `t181` đếm đúng ba — mà **PHÁN QUYẾT** của nó không ca nào đo: đột biến `K` nuốt riêng `Chan(RC_DA_DANG)` ở đúng chỗ ấy vẫn sống `175/175`. Đóng bằng `t183`/`A17`. Cùng lớp với `t103` (*"`gh auth status` xanh trong khi mọi lệnh việc thật 403"*) và với `hook-phien` (*"tệp mới tinh vẫn có thể chưa từng chạy"*). |
| `GIET-NHUNG-KHONG-DUNG-LY-DO` | 1 → **2** | r4 đếm 1 (`t182`). **+1 ở r5**: `t179` mắc y hệt với đột biến `X` — tức bản vá của r4 ĐÚNG mà HẸP, và đó là lý do r5 vá ở HELPER chứ không ở ca. Nguồn r4: `t182` ĐỎ đúng lúc cần, mà đỏ bằng `AttributeError` thoát ra **trước khi** chot của nó chạy — vì `_goi_lop_gh` chỉ bắt `mod.Chan`. Tức một tín hiệu mà **mã ngoài ca cũng dựng được**. Đóng bằng `_goi_bat_tron` + vế thứ hai của `A16`. Đây là ca thứ ba của kho sau `#355`/`#359`, và cũng là ca đầu tiên mà thứ giả mạo tín hiệu là một *helper của chính bộ test*, không phải mã sản phẩm. |

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
4. **Bản vá có làm hai lượt đỏ kia thôi đỏ không** — vẫn **KHÔNG ĐO ĐƯỢC tại thời điểm viết r4**:
   hai lượt ấy đã chạy xong trên head cũ. `A11` đo **cơ chế**; nó không thay được một lượt CI
   thật. Lời khai đúng là *"cơ chế đã đóng, chưa có lượt workflow nào chạy lại để xác nhận"*.
   **ĐỔI SO VỚI r3:** chủ kho đã gỡ `manual_ci_budget: 0` cho đợt này (*"Không CI, full CI"*
   21-09-2026) ⇒ đây thôi là "CHỌN KHÔNG ĐO" và trở lại thành **việc phải làm trước khi xong**;
   xem §10.5.
5. **`gate (windows-latest)`** — r3 ghi **CHỌN KHÔNG ĐO** theo `manual_ci_budget: 0`. **Câu ấy hết
   hiệu lực**: ngân sách đã được gỡ. Lane Windows nay nằm trong §10 như một điều kiện hoàn tất,
   và phải gọi bằng `workflow_dispatch` trên ref đó — **gắn nhãn `windows` KHÔNG sinh lượt chạy
   nào**, vì `ci.yml` khai `pull_request:` mà không khai `types:`.
6. **`_kiem_bia_mo` vẫn đòi sửa tệp lease chết.** Q2 giữ nguyên. Nếp ở `M8` là thứ duy nhất canh
   chỗ đó, và **máy không canh nó**.
7. **Ca `bool` của `M2` — NAY ĐÃ ĐO. Câu cũ của r3 HẾT HIỆU LỰC.** r3 viết *"chưa có phép đo
   riêng cho ca ấy; nó suy từ cùng cơ chế với ca chuỗi, và suy không phải đo"*. Câu ấy đã sai
   **ngay lúc r3 được đóng băng**: cùng revision đó đã thêm `M11` và `A14`, và `t178` đo ca `bool`
   bằng CẢ HAI vế — `rc=8` **và 0 lời gọi GitHub** — với một đột biến riêng (gỡ
   `isinstance(so, bool)`) làm nó ĐỎ. Trước `M11` đột biến ấy sống sót `172/172`; sau `M11` nó
   chết, và chết qua SỐ LỜI GỌI chứ không qua mã thoát.

   Ghi nguyên cả cái sai thay vì sửa lặng, vì **chỗ nó nằm mới là bài học**: §7 là mục packet TỰ
   KHAI mình còn mù. Một dòng "chưa đo" để sót ở đây tệ hơn ở docstring — nó là lời khai CÓ THẨM
   QUYỀN, và người đọc sau sẽ đi làm lại một phép đo đã có, hoặc tệ hơn, tin rằng chỗ ấy còn hở.
   Cross-review lượt 3 bắt (`post-fix-boolean-evidence-claims-drift`); lượt 1 đã bắt vế docstring
   của cùng slug, và vế spec sống thêm trọn một revision.
8. **Đột biến `L` của cross-review lượt 4 SỐNG SÓT `176/176`** — và cả reviewer lẫn packet đều
   chưa đo được nó có khác biệt nguy hiểm ở cổng tổng hay không. Reviewer **không thổi thành
   P2** vì không có phản chứng được phép dùng (luật "đừng tự soạn nội dung tấn công"), chỉ mô
   tả hình dạng cần đo: `lease_id` sai kiểu. **Phiên này CHƯA ĐO.** Đây là NỢ, không phải một
   hướng đã loại — và ghi ở §7 chứ không ở §10 là có chủ đích.
9. **Ít nhất một ca `pwsh` của `tl.py --selftest` bị BỎ QUA NGẦM mà vẫn in `[OK]`** (reviewer
   lượt 4 đo). Cùng lớp với chuyện đã xảy ra ở #574. Là nợ KẾ THỪA của harness, ngoài
   `write_set` của packet này. Hệ quả phải nhớ: **`[FAIL]=0` KHÔNG hàm ý `bỏ qua = 0`** cho
   `tl.py --selftest` — khác hẳn `ops/lease_publish_test.py`, nơi dòng tổng kết in số bỏ qua
   tường minh.
10. **Suite `G` của lượt 4 có thêm `t139` đỏ ở lần chạy ĐẦU**, đối chứng sau đó cho head/`G`
   đều PASS. Reviewer không xoá lần đỏ ấy và **không khẳng định nguyên nhân**. r5 giữ nguyên
   cách ghi: một quan sát chưa có nguyên nhân, không phải một cổng đã xanh. Cùng họ với quan
   sát `t125`/`t154` của lượt 3 (mục 11), và **chưa ai chứng minh hai cái có cùng gốc hay không**.

## 8. Ngoại lệ `ADR-0044` — Q6

`ADR-0044` (Accepted 21-08-2026): packet `sensitive` **≤ 3 tệp và ≤ 300 dòng thêm**; vượt thì
*"dừng TRƯỚC review để revision thiết kế, **hoặc khai lý do trong spec**"*. Mục này là đường thứ hai.

**TRẦN ĐÃ ĐỔI — và đây là thứ phải đọc TRƯỚC con số.** Chủ kho chỉ thị 21-09-2026: *"nới lên
10"*. Phiên này đọc là **10 lần trần DÒNG: 300 → 3000**, đã nói thẳng cách đọc ấy ra lúc nhận chỉ
thị và để ngỏ cho chủ kho đính chính. Cross-review lượt 3 ghi nhận: *"trần packet **3000** được
USER xác nhận nên không có finding kích thước"*. **Trần TỆP không được nới** — vẫn 3.

Đây là một chỉ thị, **KHÔNG phải một sửa đổi `ADR-0044`**. `docs/adr/0044-*.md` chưa đổi một chữ,
và r4 không đổi hộ nó. Nghĩa là: trần `3000` có hiệu lực cho **đợt này**, neo vào chỉ thị trên,
không phải một luật mới của kho. Packet sau đọc lại `ADR-0044` sẽ thấy `300`, và đó là đúng.

**Phép đo, 21-09-2026, `git diff --numstat 714f36e6 d38de01` (base = `merge-base`):**

| tệp | dòng thêm |
|---|---|
| `CLAUDE.md` | 27 |
| `ops/lease_publish.py` | 119 |
| `ops/lease_publish_test.py` | 595 |
| **tổng** | **741** (xoá 2) |

**3 tệp ⇒ vế TỆP ĐẠT. 741 ≤ 3000 ⇒ vế DÒNG ĐẠT theo trần đã nới.**

**Nhưng KHÔNG được khai là "ĐẠT `ADR-0044`" trống không** — `741 > 300`, tức vượt trần GỐC 441
dòng, và chỉ đạt nhờ một chỉ thị neo vào đợt này. Cách khai đúng: *"3 tệp / 741 dòng thêm; vượt
trần gốc `ADR-0044` (300) **441 dòng**; đạt trần **3000** do chủ kho nới cho đợt 21-09-2026"*.

**Lịch sử con số, vì con số trong một ngoại lệ LÀ một phần của ngoại lệ:**

| mốc | head | dòng thêm | trần lúc ấy | trạng thái |
|---|---|---|---|---|
| r2 | `44a87d0` | 333 | 300 | vượt 33, xin ngoại lệ |
| r3 | `d3d45d0` | 396 | 300 | vượt 96, ngoại lệ phải xin LẠI |
| r4 | `dea83a1` | 603 | 3000 | trong trần đã nới; vượt trần GỐC 303 |
| **r5** | `d38de01` | **741** | **3000** | trong trần đã nới; vượt trần GỐC **441** |

r3 §8 khai `396` làm số hiện hành. Sau `e2aa580` (vá 5 finding lượt 2) và `dea83a1` (vá lượt 3),
con số ấy **đã cũ 207 dòng** trong khi vẫn đứng ở §10 làm điều kiện hoàn tất. Cross-review lượt 3
bắt (`spec-current-size-evidence-stale`). Đúng cái hình dạng mà `CLAUDE.md` đã trả giá ở
`LEASE-HOI-TOAN-KHO`: **một con số không ghi ĐIỀU KIỆN ĐO sẽ trôi mà không ai biết** — và ở đây nó
trôi qua trọn hai lần vá mà ba lượt đọc spec không ai dừng lại.

`d38de01` (vá lượt 4) thêm `138` dòng nữa, và **r5 đo lại thay vì chép** — đó là toàn bộ điểm của
mục này.

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

Đo lại theo ĐÚNG quy ước ấy trên head `d38de01` (script: `git diff --unified=0` + `ast`, chạy
được, không phải đếm bằng mắt):

| loại | `ops/lease_publish_test.py` | `ops/lease_publish.py` |
|---|---|---|
| mã | **204** | **19** |
| docstring | **292** (trong đó **64** dòng trống bên trong docstring) | **78** (trong đó **15** trống) |
| chú thích đứng riêng | **45** | **18** |
| trống ngoài docstring | **54** | **4** |
| **tổng** | **595** | **119** |

**Các con số của những revision trước là của những head KHÁC** — giữ làm mốc lịch sử, không dùng
làm điều kiện:

| revision | head | test: mã / docstring / chú thích / trống | tổng |
|---|---|---|---|
| r3 | `d3d45d0` | 86 / 149 / 10 / 27 | 272 |
| r4 | `dea83a1` | 157 / 240 / 23 / 37 | 457 |
| **r5** | `d38de01` | **204 / 292 / 45 / 54** | **595** |

**Lý do, và nó phải chịu được phản bác:** cắt 96 dòng là cắt vào phần docstring, vì 86 dòng mã
không cắt được mà không bỏ một ca. Mà docstring ở đây **không phải văn trang trí** — chúng mang
chính các phép đo làm cho từng ca có nghĩa: số `rc` của từng hình dạng, tên đột biến làm ca ĐỎ, và
ở `M9` là câu chuyện đột biến sống sót. Cắt chúng để vừa một con số là **tối ưu thước đo chống lại
mục đích của thước đo** — đúng lớp bệnh mà chính kho này đặt tên.

**Điều ngoại lệ này KHÔNG cho phép:**

- Không cho vượt vế **TỆP**. Ba đường là trần cứng, và chỉ thị *"nới lên 10"* **không** chạm vế
  này; đường thứ tư vẫn làm `A8` ĐỎ.
- Không cho gọi cổng `ADR-0044` là **"ĐẠT"** trống không ở bất kỳ đâu — thân PR, comment, hay báo
  cáo. Câu đúng phải nêu CẢ trần gốc, mức vượt, và thẩm quyền nới. Tiền lệ đã trả giá (`PLAT-X8`):
  con số trôi lần thứ tư khai sai rằng một thẩm quyền đã có.
- **Không cho gia hạn sang packet sau.** Trần `3000` neo vào chỉ thị của đợt 21-09-2026 cho
  **#579**. `ADR-0044` trong `docs/adr/` **vẫn là 300 và r4 không đổi nó**; packet sau đọc ADR sẽ
  thấy `300`, và đó là đúng.
- **Ngoại lệ này ĐÃ phải xin lại HAI lần** — `333` (r2) → `396` (r3) → nay trần nới thành `3000`.
  Con số trong một ngoại lệ là một phần của ngoại lệ, không phải một chú thích.

| trường | giá trị |
|---|---|
| `ai_nang` | `ducthangho` (OWNER) |
| `can_cu` | Chỉ thị trong phiên 21-09-2026: *"nới lên 10"*, trả lời cho câu hỏi về trần `ADR-0044` của đợt này. Cách đọc *"10 lần trần DÒNG, 300 → 3000"* do phiên này nêu ra và nói thẳng là cách đọc của mình, để ngỏ đính chính. Cross-review lượt 3 ghi nhận `3000` là trần được USER xác nhận. |
| `tran_goc` | **300** dòng thêm (`ADR-0044`, KHÔNG đổi) |
| `tran_dot_nay` | **3000** dòng thêm |
| `tran_tep` | **3** tệp — **KHÔNG nới** |
| `so_do_r2` | **333** dòng thêm, head `44a87d0` |
| `so_do_r3` | **396** dòng thêm, head `d3d45d0` |
| `so_do_r4` | **603** dòng thêm, head `dea83a1` |
| `so_do_r5` | **741** dòng thêm, head `d38de01` — **vượt trần GỐC 441**, trong trần đợt này |
| `KHÔNG ĐO ĐƯỢC` | Chỉ thị *"nới lên 10"* không nói rõ đơn vị. Cách đọc đã công bố và chưa bị đính chính, nhưng **đó là một cách đọc, không phải một phép đo**. Nếu chủ kho đọc khác thì con số trần đổi, và §8 phải sửa theo. |

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

1. Một lease của revision **5** đã cấp và đã đăng. `g3` neo `spec_hash` của **r2** — reviewer
   lượt 3 đo và ghi thẳng: *"Lease g3 giao kèm vẫn là revision 2 / generation 3 / hash r2; không
   dùng artifact đó để xác nhận đã cấp lease r3."* Nên tính tới r5 thì lease đang hiệu lực **trễ
   BA revision**. r5 đổi `nghiem_thu` (viết lại `A16`, thêm `A18`/`A19`) ⇒ §3.2 đòi **generation
   mới** neo vào băm của r5. **Cấp lease là thẩm quyền chủ kho** — phiên #579 soạn và xin, KHÔNG
   tự cấp.
2. `A1`–`A19` đều có phép đo dương, `rc` đọc TRỰC TIẾP. (r3 chỉ đòi tới `A14` trong khi `t181`–
   `t183` đã tồn tại; r4 tới `A17` trong khi `t184` chưa ra đời — xem §5.)
3. Thân PR khai kích thước theo ĐÚNG câu ở §8: **3 tệp / 741 dòng thêm; vượt trần gốc `ADR-0044`
   (300) 441 dòng; đạt trần 3000 do chủ kho nới cho đợt này**. Không khai "ĐẠT" trống không, và
   không dùng lại con số `333` (r2), `396` (r3) hay `603` (r4).
4. `human_audited`: một lượt thẩm định của NGƯỜI trên head thật. **Packet này KHÔNG LAND ĐƯỢC
   BẰNG MÁY**, và chữ ký không thay được phép đo. **Bốn** lượt cross-review máy đã chạy (§11,
   §12) — chúng **không** cấp được `human_audited`, và verdict của chúng tự nói đúng điều đó.
5. **Một lượt CI ĐẦY ĐỦ trên head cuối, GỒM lane `windows-latest`.** r3 ghi lane này là "CHỌN
   KHÔNG ĐO" theo `manual_ci_budget: 0`; chủ kho đã gỡ ngân sách (*"Không CI, full CI cho tới
   khi đủ điều kiện merge"*, 21-09-2026). Gọi bằng `workflow_dispatch` trên ref đó — **gắn nhãn
   `windows` KHÔNG sinh lượt chạy nào**, vì `ci.yml` khai `pull_request:` mà không khai `types:`.
   Chưa có lượt Windows nào trên head này ⇒ trạng thái hiện tại là **KHÔNG ĐO ĐƯỢC**, không phải
   "đã chọn bỏ qua".

   **ĐÂY LÀ MỤC CÓ THẨM QUYỀN VỀ CI, và §3 đã được sửa cho khớp** — r5 để hai mục chỉ đạo ngược
   nhau, xem §0.6. Nếu còn tìm thấy một câu nào khác trong đặc tả này nói `manual_ci_budget: 0`
   đang hiệu lực, câu ấy SAI và mục này thắng.

   Đọc đúng chỉ thị: *"Không CI"* nghĩa là **đừng CHẶN vòng lặp vá/review để chờ CI giữa các
   lượt**; *"full CI cho tới khi đủ điều kiện merge"* nghĩa là **một lượt đầy đủ trên head cuối
   trước khi bàn tới merge**. Hai vế ấy không mâu thuẫn — chúng nói về hai thời điểm khác nhau.
6. Cross-review đạt **`approve`** tường minh. Lượt 4 ra `changes_requested`; hai P3 của nó chưa
   đóng chừng nào reviewer chưa đo lại trên `d38de01` + r5 — **lời tự khai "đã sửa" KHÔNG đóng
   được chúng**, đúng câu §11 của chính r3: *"lời khai trung thực về một khoảng trống không lấp
   được khoảng trống ấy"*.
7. **Đột biến `L` đã được đo** — hoặc, nếu vẫn không đo được, thì nói thẳng là `KHÔNG ĐO ĐƯỢC`
   ở thân PR chứ không im lặng. Xem §7.8: reviewer lượt 4 để nó mở và mô tả hình dạng cần đo.

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

## 12. Cross-review lượt 2 và lượt 3 — `codex`, và r4 là hệ quả của lượt 3

### 12.1 — Lượt 2

| trường | giá trị |
|---|---|
| reviewer | `codex`, `model_reasoning_effort=xhigh` |
| `reviewed_sha` | `d3d45d0586f9ceb0eae879c066b198ff8346bcfc` |
| verdict | **`changes_requested`** |
| finding | 5 |
| đột biến | `A`–`I`, chạy toàn suite |

Finding nặng nhất là `unposted-error-precedence-changes` — **lần thứ HAI cùng slug**. Bản vá lượt
1 đưa CẢ `_tien_kiem_mien_dang` vào trong `try`, nên `Chan` nó ném cho một `lease` KHÔNG PHẢI ánh
xạ cũng bị nuốt, rồi `kiem()` gọi `.get()` và một `AttributeError` **TRẦN** thoát ra khỏi cổng.
Đo được năm hình dạng: `None` · `[]` · `True` · `55` · `"55"`.

Đóng bằng cách tách HAI chốt — HÌNH DẠNG ngoài `try`, MIỀN trong `try` — và bằng `t182`. Nền
`origin/master` CŨNG vỡ y hệt ở đây, nên nó KHÔNG phải hồi quy mới; nó là việc đánh mất một chốt
mà chính lượt 1 vừa thêm vào. Khai đúng mức đó, đừng phóng đại.

Reviewer cũng bác một recipe đột biến mà **chính phiên này** viết trong docstring `t180` (*"bỏ
`return` ở nhánh `Chan`"*) — Python không ném lại một ngoại lệ đã bắt, nên recipe ấy là bộ tương
đương và cả bảy ca vẫn QUA. Reviewer tìm ra bằng cách **chạy nó**. Ghi ra vì đây đúng lớp *"nghĩ
ra được phép thử mà không chạy thì phép thử ấy không tồn tại"* — và lần này thứ không chạy nằm
trong một docstring viết ra để hướng dẫn người sau đo.

### 12.2 — Lượt 3, và r4 là hệ quả

| trường | giá trị |
|---|---|
| reviewer | `codex`, họ model GPT-6 theo cấu hình phiên, provider OpenAI |
| `reviewed_sha` | `e2aa580f9fcea4dbd0f79421ca0033bf77313cdc` |
| verdict | **`changes_requested`** |
| finding | **1 P2 + 3 P3** |
| bảng săn | 7 hướng mới `N1`–`N7`, mỗi hướng có lệnh + output thật |
| đột biến | `A`–`K`, **toàn suite 175 ca, bỏ qua 0** |
| `VERDICT.md` | `sha256 2d53717d6bb5a0d9ae061a4a046d703b23cba045bc2d79fca96be2ba6a38ea3c`, 39242 B |

| slug | lớp | xử ở |
|---|---|---|
| `final-comment-already-posted-branch-mutant-survives` | P2 — TEST, đột biến sống sót | `t183` / `A17`, vá `dea83a1` |
| `t182-mutant-killed-before-own-assertion` | P3 — TEST, tín dụng giả | `_goi_bat_tron` + vế 2 của `A16`, vá `dea83a1` |
| `post-fix-boolean-evidence-claims-drift` | P3 — **SPEC** | §7.7 của r4 |
| `spec-current-size-evidence-stale` | P3 — **SPEC** | §8, §10 của r4 |

**Hai finding SPEC là của CHÍNH r3**, nên `changes_requested` là verdict đúng theo §3.2, và r4 tồn
tại vì bị BẮT — y như r3.

**Điều đáng giữ nhất từ lượt 3:** cả hai finding P2/P3 về TEST đều nói cùng một chuyện —
**thước đo nói dối theo hai chiều ngược nhau.** `K` sống sót: một cửa CÓ MẶT mà phán quyết không
ai đo (tín hiệu ÂM giả). `J` giết `t182`: một ca ĐỎ đúng lúc cần mà đỏ vì lỗi vô can (tín hiệu
DƯƠNG giả). Một bộ test chỉ đếm "đỏ hay xanh" mù với cả hai. Chỉ hai phép đo tách được chúng:
**đột biến phải ĐỔI MÀU ĐÚNG CA ĐÍCH**, *và* **ca ấy phải đỏ bằng TÍN HIỆU RIÊNG của nó**.

Reviewer còn ghi một quan sát mà r4 chép lại nguyên trạng thái, không nâng cũng không hạ: suite
nền lần chạy ĐẦU của lượt 3 cho **`174/175`, `rc=1`** vì `t125` thấy `t154` `ValueError` trong một
lượt con; chạy lại sau `A`–`K` thì **`175/175`, `rc=0`**. Hai thân hàm bằng master mới.
**Nguyên nhân chập chờn CHƯA được chứng minh** — reviewer không xoá lần đỏ ấy và cũng không dùng
nó làm finding hồi quy. r4 giữ đúng cách ghi đó: **một quan sát chưa có nguyên nhân, không phải
một cổng đã xanh.** Nó nằm ở §7 như một mục chưa đo được, không ở §10 như một điều kiện đã đạt.

### 12.3 — Lượt 4, và r5 là hệ quả

| trường | giá trị |
|---|---|
| reviewer | `codex`, họ model GPT-6 theo cấu hình phiên, provider OpenAI |
| `reviewed_sha` | `dea83a1aabcfe5bea597e1efea3e69a68aea039b` (#592: `6794440`) |
| verdict | **`changes_requested`** |
| finding | **2 P3. KHÔNG P1/P2 mới.** |
| bảng săn | 11 hướng, mỗi hướng có lệnh + output thật |
| đột biến | `A`–`K`, `L`, `X` — **13 biến thể, mỗi cái chạy TOÀN suite 176 ca, bỏ qua 0** |
| `VERDICT.md` | `sha256 5fb2a6cd2afc611f45fa74221191ccf9252b5ff19fd041b9c32a323a3a2eb664`, 63826 B |

**4/4 slug lượt 3 phán `ĐÃ VÁ THẬT`** — lần đầu tiên trong packet này mọi finding của lượt trước
đều đóng thật. `J` và `K` khớp cả **số ca đỏ**, **tên ca**, **lớp tín hiệu**.

| slug mới | lớp | xử ở |
|---|---|---|
| `spec-section2-byte-preservation-false` | P3 — **SPEC** | §2 của r5 |
| `t179-raw-fallback-mutant-killed-before-own-assertion` | P3 — TEST | `A18`/`A19`, vá `d38de01` |

**Điều đáng giữ nhất từ lượt 4** không phải hai finding mà là chuyện xảy ra KHI VÁ chúng.

Reviewer đề xuất vá `t179` bằng cách dùng helper riêng cho ca ấy, *"không nới helper toàn
suite"*. Packet **làm khác**, và khai thẳng: `CLAUDE.md` chốt rằng khi một lỗi có NHIỀU đường
vào thì đừng vá theo danh sách đường reviewer liệt kê — **tự liệt kê hết đường TRƯỚC, đóng cả
loạt**. Vá ca thứ hai theo cách đã vá ca thứ nhất là mời lượt 5 tìm ca thứ ba. Nên bản vá nằm ở
`_goi_lop_gh`, đường DUY NHẤT 20+ ca đi qua.

Rồi `t184` — ca dựng ra để đo chính bản vá ấy — **bắt được HAI lỗi của chính bản vá**, và cả hai
đều không lộ ra bằng đọc:

1. **Danh tính lớp `Chan` là THEO TỪNG LẦN NẠP.** Vế (a) bản đầu ném `_nap_cong().Chan(...)` từ
   một fixture ⇒ ca ĐỎ, vì `_nap_cong()` dựng module MỚI mỗi lần gọi nên lớp ấy KHÁC
   `mod.Chan` bên trong helper. Đường sản phẩm không dính (cùng một module instance), nhưng mọi
   fixture tự nạp rồi ném `Chan` sẽ bị phân hạng là ngoại lệ trần — **và trông y hệt một lỗi của
   helper**.
2. **Chốt đo SAI TOÁN TỬ.** Vế (b) bản đầu chỉ chốt `all(ma != m …)`. Đột biến `N3` cho
   `__eq__` trả `True` mà để nguyên `__ne__` ⇒ **SỐNG SÓT `177/177`**. Mà MỌI ca chốt bằng
   `ma == RC_X`, nên với `N3` một ngoại lệ trần khớp MỌI mã thoát và cả loạt ca thành **XANH
   GIẢ**. Vế `!=` đo đúng thứ **không ai dùng**.

Cái thứ hai đáng ghi hơn: **một chốt sinh ra để chống tín dụng giả, mà tự nó đo sai toán tử, thì
nó LÀ tín dụng giả.** Nó không lộ ra bằng đọc mã, bằng `py_compile`, hay bằng một suite xanh —
chỉ bằng đột biến. Đó là lý do `A19` tồn tại, và là lý do §6 có dòng `CHOT-DO-SAI-TOAN-TU`.

Ba thứ lượt 4 để MỞ, và r5 ghi chúng ở §7 chứ không ở §10: đột biến `L` sống sót chưa ai đo
(§7.8) · ít nhất một ca `pwsh` bỏ qua ngầm mà in `[OK]` (§7.9) · `t139` đỏ một lần rồi thôi,
không ai biết vì sao (§7.10).

### 12.4 — Lượt 5, lượt ĐẦU theo trục LỚP, và r6 là hệ quả

| trường | giá trị |
|---|---|
| `reviewed_sha` | `d38de01dd30f576ee9f0f5ec9f1d5a7c12c763d7` (#592: `bb7694e`) |
| verdict | **`changes_requested`** |
| finding | **4 P3. KHÔNG P1/P2.** |
| lớp khai | **6**, tất cả `HỞ` (một phần ĐÓNG cho cặp đã đo) |
| `VERDICT.md` | `sha256 9f376f2cf41c204ce55f906f40afc5907368a08714245abeca447f19298d63a1`, 95272 B, 601 dòng |

**Hai P3 về MÃ đã vá ở `94d3cd9`**, và cả hai đáng ghi vì chúng là cùng một lớp ở hai tầng:

- `helper-exception-formatting-escapes-own-assertion` — `_MaVang` gọi `str(ex)` thẳng, nên một
  ngoại lệ có `__str__` NÉM làm helper không trả về và vỡ **cả lớp** ca gọi nó (đo: 41 vị trí ×
  `StringFails` ⇒ `RAW 41/41`). **Đường CHẨN ĐOÁN làm vỡ phép đo.**
- `helper-contract-assertions-omit-code-domain-and-identity` — `A19` đòi `.ma` đúng nhưng không
  đòi **danh tính lớp**, và miền mã chỉ `{0,4,8,9}` trong khi `t177` chốt bằng `== 6`. Reviewer
  đo: sentinel nhận riêng `6` ⇒ `t184` PASS **và** một ngoại lệ trần ở lần gọi thứ ba của `t177`
  thành ca XANH. Lỗ miền không dừng ở ca khai nó.

**Và vế `(e)` dựng ra để đo bản vá thứ nhất TỰ SẬP đúng lớp nó đo:** bản đầu đọc `ex` SAU lời
gọi, nên với đột biến `P_str` helper không trả về và `chot` không bao giờ chạy — ca đỏ bằng
traceback trần. Mệnh đề thật là *"helper LUÔN TRẢ VỀ"*, và mệnh đề ấy chỉ kiểm được từ phía
NGƯỜI GỌI. Đây là lần thứ **ba** trong packet này một chốt mới tự sập vì đo sai chỗ
(`t184(b)` sai toán tử · `t178` sai đơn vị · `t184(e)` sai phía).

**Reviewer cũng ĐO và XÁC NHẬN một quyết định mà lượt 4 họ từng đề nghị khác:** việc nới
`_goi_lop_gh` toàn suite là CÓ CƠ SỞ — `contract_preservation.py` cho **21/21 ca cũ đạt** với
cả helper r4 tái dựng lẫn helper head; không ca đúng nào bị đổi sai, không mất tín hiệu dừng.
Ghi lại vì nó là tiền lệ: đi khác đề xuất của reviewer thì phải khai thẳng và chịu để họ đo.

**Nợ `L` đã đóng một phần.** Reviewer để `KHÔNG ĐO ĐƯỢC` vì luật cấm tự soạn nội dung, và yêu
cầu điều phối đo hộ với fixture `lease_id` SAI KIỂU. Điều phối đo (`ee28ebf`): ở đơn vị PHÉP DÒ,
nền `0` lời gọi / `L` `1` lời gọi; ở CỔNG TỔNG cả hai `rc=8` — mù. Đột biến `L` nay CHẾT
(`176/177`, đỏ đúng `t178`). **Nhưng câu "khác biệt ấy có nguy hiểm ở BIÊN CÔNG KHAI không" vẫn
`KHÔNG ĐO ĐƯỢC`** — reviewer cảnh báo đúng: *"không chỉ gọi `_tien_kiem_mien_dang` rồi suy rộng
ra workflow"*. Mutant đã chết và biên công khai chưa đo là HAI mệnh đề khác nhau; §7.8 giữ vế
thứ hai.
