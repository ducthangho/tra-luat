# ĐẶC TẢ — `DANG-LEASE-DAU-TRUOC-KIEM-SAU` — **revision 12, ĐÓNG BĂNG**

| trường | giá trị |
|---|---|
| `packet_id` | `DANG-LEASE-DAU-TRUOC-KIEM-SAU` |
| `revision` | **12** |
| `thay_the_cho` | revision 11, `3cc2011efb25abb19f1c2588355ba24d6d5f00a5ea9bea99e5450b1ae0c9d443` |
| `packet_issue` | **#579** |
| `nguon_cap_viec` | Chỉ thị chủ kho 21-09-2026: *"Chạy lặp cross review, vá, đăng verdict cho tới khi approve. Không CI, full CI. Chạy với #589, #592 và các PR chưa merge trong phiên"* và *"nới lên 10. chạy đến approve"*. r6 là hệ quả của cross-review lượt 5 — xem §12.4. Chỉ thị 21-09: *"Không CI, full CI cho tới khi đủ điều kiện merge. Chạy lặp vá, cross review theo phân lớp lỗi… lặp tới khi có cross approval."* Nguồn của r3: *"#589, #592 vá đi, rồi cho qua 1 lần cross-review codex"* (§11). Nguồn của r2: *"Anh soạn r2 gói cả ba đi"* (§0.2). **Nguồn của r7 — chỉ thị 21-09-2026, bản chiếu `issues/579#issuecomment-5765688081`:** *"Chuyển điều kiện dừng là tới khi không còn findings P1, P2, P3"*. Xem §0.7. **Nguồn của r8 — chủ kho 24-09-2026, trả lời đề nghị "mở spec r8 và lease thế hệ mới cho #579":** *"Đồng ý cả 2. Làm đi"*. Xem §0.8. **Nguồn của r9 — chủ kho 25-09-2026, trả lời đề nghị mở r9 + lease g7 cho F2/F4 của cross-review lượt 14:** *"Mở r9 + g7"*. Xem §0.9. **Nguồn của r12 — chủ kho 25-09-2026, sau cross-review lượt 18, trong phiên điều phối (bản chiếu `issues/579#issuecomment-5831890719`):** *"Mở r12 + g10 (đề xuất)"*. Xem §0.12. |
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

### 0.7 — Vì sao có revision 7

**HAI lý do độc lập, cả hai đều buộc phải qua §3.2.**

**(a) Chủ kho đổi ĐIỀU KIỆN DỪNG.** Nguyên văn: *"Chuyển điều kiện dừng là tới khi không còn
findings P1, P2, P3"*. `dieu_kien_dung` là **acceptance**, và §3.2 nói thẳng: *"Đổi objective,
acceptance, write set, dependency, executor hoặc environment tạo revision mới và làm lease cũ
mất hiệu lực."* Không có đường nào để một chỉ thị như thế vào mà không qua một revision.

Luật mới **CHẶT HƠN**, không phải một lần nới: protocol cho phép một verdict `approve` kèm P3,
và luật mới KHÔNG dừng ở một verdict như thế. *(r8 sửa: bản r7 viết "lượt 5 và lượt 6 của chính
packet này đều thế" — SAI; bảng lịch sử của chính tệp này ghi lượt 5 `changes_requested` (§12.4),
lượt 6 `blocked` (§12.5), và chưa lượt nào của packet ra `approve`. Xem §0.8.)*

**(b) Cross-review lượt 6 phán `blocked` VÌ ĐẶC TẢ.** Reviewer nói rõ: *"`blocked` vì SPEC đóng
băng còn thiếu/lệch điều kiện nghiệm thu, phải qua revision theo protocol §3.2 … nếu chỉ xét lỗi
test thì yêu cầu là `changes_requested`."* Phân rã: **0 P1 · 0 P2 · 9 P3**, trong đó **4 nằm
trong mã** (đã đóng ở `d27cba2`) và **5 nằm trong đặc tả này**:

| # | slug lượt 6 | r7 sửa ở |
|---|---|---|
| 3 | `spec-guarantees-still-lack-adjacent-measurements` | §2 — thêm cột `r5 → r6` và `r6 → r7`, đo tại chỗ |
| 6 | `spec-current-size-evidence-stale` | §8, §10.3 — `741/441` → số ĐO ở head `d27cba2` |
| 7 | `spec-current-revision-contradicts-done-condition` | §10.1 — neo revision/hash HIỆN HÀNH |
| 8 | `spec-active-review-count-stale` | §10.4 — *"Bốn lượt"* → số đếm được |
| 9 | `spec-a19-omits-diagnostic-return-contract` | `A19` — thêm vế (e); `A20`–`A22` mới |

**Bốn lớp đã đóng trong mã, mỗi lớp một CỬA chứ không một chốt** — chi tiết và bộ đột biến ở
§12.5. Đáng ghi nhất: đột biến `R_probe` **SỐNG 177/177** trên head cũ, vì *"0 lời gọi vì tiền
kiểm chặn"* và *"0 lời gọi vì ngoại lệ bay ra trước mạng"* là **hai trạng thái cho cùng một con
số**, và ca chỉ chốt con số.

### 0.8 — Vì sao có revision 8

**MỘT lý do, và nó thuộc đúng lớp mà r7 sinh ra để đóng.** Cross-review codex lượt 7 (phiên điều
phối khác, `gpt-6-astra` medium, neo `2715d20`) phán `blocked` với `spec-review-verdict-history-
contradicts-itself` (P3), và mọi lượt sau — lượt 4 tới lượt 12 của vòng executor, cùng các lượt
song song — giữ nguyên finding ấy vì nó nằm trong đặc tả đóng băng: §0.7(a) và §10 mục 6 viết
lượt 5 và lượt 6 *"đều thế"* (tức `approve` kèm P3), trong khi bảng lịch sử của CHÍNH tệp này ghi
lượt 5 `changes_requested` (§12.4) và lượt 6 `blocked` (§12.5). Hai câu tự mâu thuẫn trong cùng
một văn bản — chứng minh được mà không cần gì ngoài tệp.

**Quét cả lớp, không chỉ hai câu được chỉ.** Liệt kê MỌI dòng chứa `approve` trong r7 (6 dòng,
`grep -i -n`) và MỌI dòng khai verdict của một lượt (bảng `| verdict |` và câu văn ở §0.3,
§0.4, §0.5, §0.7, §10, §11, §12). Kết quả: đúng HAI câu gán `approve` cho một lượt — hai câu
trên; mọi câu verdict khác khớp bảng lịch sử (lượt 1 `blocked`; 2, 3, 4, 5 `changes_requested`;
6 `blocked`). Phạm vi phép quét: các dòng chứa chuỗi `approve` và các dòng khai verdict; một
câu gán verdict mà không dùng tên verdict thì phép quét không thấy.

**Chỗ thứ BA, không reviewer nào nêu — tìm ra khi soạn r8:** §10 mục 1 ghi cứng `revision: 7`
ngay trong mục tự khai *"CỐ Ý không ghi cứng một con số revision khác"*. Giữ nguyên thì r8 tái
tạo đúng finding `spec-current-revision-contradicts-done-condition` (lượt 6). r8 đổi câu ấy sang
trỏ vào bảng đầu tệp, và đối chứng của phép kiểm sang "lease neo revision TRƯỚC".

*(r11: câu dưới là lúc đóng băng r8; vế `A1`–`A22` đã lệch phép đo sau bản vá P1 — §0.9, §0.10.)*
**Không đổi ở r8:** bệnh, `write_set`, `muc_tieu`, `M1`–`M11`, `A1`–`A22`, điều kiện dừng (vẫn
`0` finding P1/P2/P3), `human_audited`, §8 và §10 mục 3–5 (các số ở đó neo lúc đóng băng r7, có
ghi điều kiện đo). r8 là một revision của LỜI KHAI; §3.2 vẫn đòi revision vì tệp đóng băng.

### 0.9 — Vì sao có revision 9

Cross-review codex lượt 14 (25-09, `gpt-6-astra` medium) trên head `1d91d4e` theo r8: `blocked`, **P1 0 · P2 2 · P3 2**.
Mã: P1 của connector codex GitHub trên #589 (review 5311667334 — *lease đã đăng mà tệp bị SỬA vẫn ra `rc=9`*, HỒI
QUY của packet, vá ở `8d04b78`) được xác nhận ĐÓNG; F1/F3 của lượt 14 vá ở `0093149`. Hai finding còn lại nằm trong
CHÍNH đặc tả này, nên cần revision:

- **F2 (P2) `frozen-spec-posted-validation-contract-stale`:** M1 đòi *"có dấu ⇒ `Chan(RC_DA_DANG)` ngay"*, M4 đòi khai
  *"các chốt của `kiem()` không chạy nữa"* — tức đặc tả ĐÒI đúng hành vi là lỗ P1. A5 còn đòi ca sai kiểu đổi `8 → 9`,
  nay là `8 → 8`. Và §5/§10.2 chỉ tới `A22` trong khi `t190` viện `A23`. r9 viết lại M1, M4, A5 theo mã hiện hành
  (giữ lời khai cũ, đánh dấu tại chỗ) và thêm `A23`.
- **F4 (P3) `spec-current-size-evidence-stale`, LẦN THỨ BA:** §8 kết luận vế dòng bằng `1272` (head `d27cba2`) trong
  khi head đã ở `2398`. r9 KHÔNG chỉ cập nhật con số — lần thứ tư sẽ đến y hệt — mà đổi CÁCH KHAI: tiêu chí là phép
  đo tại head, mọi con số trong §8 là lịch sử có ghi điều kiện đo.

**Quét cả lớp, không chỉ chỗ được chỉ:** tìm mọi câu trong r8 mô tả nhánh đã-có-dấu (`Chan(RC_DA_DANG)` ngay · không
chạy nữa · né sạch · `8 → 9` · `rc=9`) — đúng M1, M4 (bảng §4) và A5 (bảng §5); M6 (hết hạn + có dấu ⇒ `rc=9`) vẫn
đúng. Phạm vi phép quét: các cụm từ ấy; một câu diễn đạt khác thì phép quét không thấy.

*(r10: câu dưới SAI ở vế `A1`–`A4`, `A6`–`A22` — r9 không đổi chúng, nhưng chúng đã lệch phép đo sau bản vá P1; cross-review lượt 15 bắt, §0.10.)*
**Không đổi ở r9:** bệnh, `write_set`, `M2`, `M3`, `M5`–`M11`, `A1`–`A4`, `A6`–`A22`, điều kiện dừng (vẫn `0` finding
P1/P2/P3), `human_audited`, trần 3000/3.

### 0.10 — Vì sao có revision 10

Cross-review codex lượt 15 (25-09, `gpt-6-astra` medium) trên head `0093149` theo r9: `blocked`, **P1 0 · P2 2 · P3 1**.
F4 ĐÓNG bằng r9. F1 (P2, chốt cần đường dẫn tệp ở nhánh đã-có-dấu) và F3 (P3, lời khai `t178`) nằm trong MÃ, vá ở
`af6b54c` (không đổi đặc tả). Còn **F2 (P2) `frozen-spec-posted-validation-contract-stale`** nằm trong CHÍNH tệp này —
LẦN THỨ HAI của lớp ấy (lượt 14 → M1/M4/A5/A23; lượt 15 → A2/A4/A13 và câu §4 *"M1–M8 giữ nguyên byte nghĩa"*). Chỉ thị
chủ kho 25-09: *"Mở r10 + g8"*.

**Đường đã chọn — MỘT đường, khai rõ:** SỬA acceptance cùng revision. **§5.0 là bảng nghiệm thu DUY NHẤT có thẩm
quyền**, chép ĐỦ `A1`–`A23` (kể cả phần trước đây kế thừa BẰNG THAM CHIẾU từ r1 §5), và cột tập đỏ của MỌI dòng là số
đo lại tại `af6b54c` trên TOÀN suite. Các bảng r3–r9 lùi thành **§5.1 LỊCH SỬ**, không chi phối nghiệm thu. Không còn
câu nào trong r10 nói một tiêu chí được "giữ nguyên" từ revision khác — chính kiểu câu ấy là đường lớp lỗi này đi vào.

**Quét CẢ LỚP, không chỉ bốn chỗ được chỉ.** Hai phép quét:

- **Phép đo** (không phải phép đọc): MỌI đột biến mà bất kỳ tiêu chí `A*` nào viện dẫn — **40** đột biến (20 + 11 + 9), gồm 20 công thức
  docstring `t174`–`t184`, 11 đột biến bản vá P1, `A5`/`A6`/`A14`/`A19 N3b`/`A20 D1 D2 R_probe`/`A21 D3`/`A22 Pstr` —
  chạy TOÀN suite (185 ca) trên bản sao tạm, mỗi đột biến một tiến trình, `PYTHONDONTWRITEBYTECODE=1`, phân hạng mỗi ca
  `QUA`/`CHOT` (`TinHieuChotCa`)/`ASSERT` (`AssertionError` khác — kiểu `bang` của ca cũ)/`TRAN`. **Nền 185/185, 0 đỏ.**
  Lượt đầu của phép đo này ra nền **16 đỏ `ModuleNotFoundError`** — lỗi RIG (tiến trình con không đưa `ops/` vào
  `sys.path` như `python3 ops/lease_publish_test.py`); bỏ kết quả ấy, sửa rig, đo lại. Mọi tập đỏ ở §5.0 là của lượt
  sau.
- **Phép quét cụm từ** trên r9, tìm mọi lời bảo đảm về tập đỏ, mã thoát hoặc sự kế thừa: `giữ nguyên` · `ĐÚNG MỘT` ·
  `đúng một ca` · `Đã đo` · `cả ba ĐỎ` · `chỉ một trong hai` · `ĐỎ NGƯỢC CHIỀU` · `không chạy nữa` · `né sạch` · `8 → 9` ·
  `(r8: \`8\`)` · `đang ở đúng` · `Không đổi ở r9` · các cặp `N/N` (`177/177` `176/177` `174/175` `179/180` `180/180`).
  Phạm vi: đúng các cụm ấy; một câu diễn đạt khác thì phép quét KHÔNG thấy — phép đo ở trên mới là lưới chính.

**Kết quả quét cụm từ, và cách xử từng chỗ:**

| chỗ trong r9 | lệch gì | r10 |
|---|---|---|
| §4 *"M1–M8 giữ nguyên byte nghĩa"* | r9 đổi nghĩa M1, M4 | viết lại câu, đánh dấu tại chỗ |
| §5 *"A1, A2, A4, A6, A8–A11 của r1 §5 giữ nguyên"* | kế thừa bằng tham chiếu; A2, A4 lệch | hết hiệu lực; §5.0 chép đủ |
| r1 **A2** *"chỉ một trong hai đỏ nghĩa là bộ tương đương"* | ngược phép đo: hai đột biến của cặp mỗi cái đỏ ĐÚNG ca của nó, đó mới là phân biệt | §5.0 A2 viết lại |
| r1 **A4** *"tiền kiểm nuốt cả bốn ca ⇒ cả ba ĐỎ"* | công thức ấy SỐNG ở `t177`; ba lỗi vẫn bị `kiem()` chặn sau P1 (đo 9/4/6/8) | §5.0 A4 đổi đột biến |
| **A13** *"giết đúng một ca, t174–t179 đều QUA"* | đo: `{t178, t180}` | đánh dấu r3 + §5.0 |
| A15, A16, A17, A18, A19, A20 — các câu *"đỏ ĐÚNG MỘT ca"*, `176/177`, `179/180`… | số của head cũ; một số tập đã rộng ra (A15: `{t179, t181, t183}`) | §5.1 lịch sử; §5.0 số đo mới |
| §0.9 *"Không đổi ở r9: … A1–A4, A6–A22"* | đúng về VIỆC r9 làm, sai về hiệu lực | đánh dấu tại chỗ |
| §10.1 *"(r8: \`8\`)"* | cũ ngay ở r9 | đổi thành "con số ở ô `revision` của chính tệp" |
| §10 mục 6 *"Lượt 6 đang ở đúng hình dạng…"* | hiện tại đã cũ | đánh dấu "lúc đóng băng r7" |

**Nếu lần thứ BA cùng hình dạng** (acceptance/lời khai đóng băng lệch sau một bản vá) thì DỪNG và hỏi chủ kho, không
mở r11 tự động — ràng buộc do phiên điều phối chuyển lại, ghi vào đây để nó sống trong đặc tả chứ không trong một
tin nhắn.

**Không đổi ở r10:** bệnh, `write_set`, `M1`–`M11` (chỉ sửa câu dẫn §4), mã head `af6b54c`, điều kiện dừng (`0`
finding P1/P2/P3), `human_audited`, trần 3000/3.

### 0.11 — Vì sao có revision 11: `t190` thôi liệt kê TAY — `t191` liệt kê BẰNG MÁY

Cross-review lượt 16 trên head `af6b54c` theo r10 (reviewer `claude-fable-5-1`, cùng nhà cung cấp ⇒ `advisory_review`, vì
codex hết hạn mức khi ấy): `changes_requested`, **P1 0 · P2 1 · P3 0 · P4 3**. §5.0 của r10 khớp phép đo trên 14 đột biến lấy
mẫu. Finding:

- **F1 (P2) `posted-branch-neo-prompt-with-file-path-untested`:** đột biến C1 — `neo = "" if bo_qua_han else
  _kiem_neo_prompt(...)` — SỐNG 185/185. Vế (ii) của `t190` đo neo prompt KHÔNG kèm `tep`; vế (v) có `tep` mà fixture không
  có neo; trong khi workflow LUÔN gọi `kiem-github "$tep"`. Mã đúng; lỗ ở bộ test.
- **F2 (P4):** C2 (miễn regex `lease_id` khi `bo_qua_han`) và C3 (miễn `packet_issue > 0`) cũng sống.
- **F3 (P4):** hai câu kiểu "giữ nguyên" còn sót — §4 và §0.8.
- **F4 (P4):** chốt loại số hiệu ở nhánh có dấu — đã khai từ lượt 7.

**Hình dạng, lần thứ BA liền:** lượt 14 thêm vế (iv), lượt 15 thêm vế (v), lượt 16 cần vế (vi) — mỗi lần `A23` lệch vì nó
LIỆT KÊ TAY số vế và danh sách đột biến. Chủ kho 25-09 chọn: *"r11 + đổi kiến trúc (đề xuất)"* ⟦nguon:chi-thi⟧ — nhận
QUA phiên điều phối.

**Kiến trúc mới (mã `4e82a06`):**

1. **`t191`** — `_liet_ke_chot_kiem` duyệt AST thân `kiem()` lấy MỌI chốt trực tiếp: mọi câu lệnh `raise Chan(...)` và mọi
   lời gọi hàm tên `_kiem_*`/`_doc_*` đứng thành câu lệnh hoặc làm vế phải phép gán. Với MỖI chốt, `_mien_mot_chot` dựng đột
   biến "miễn chốt này khi `bo_qua_han`" (bọc `if not bo_qua_han:`, hoặc vế phải thành `"" if bo_qua_han else …`) và đòi
   `t190` ĐỎ bằng `TinHieuChotCa`. Một chốt mới trong `kiem()` mà `t190` không có vế cho nó ⇒ `t191` ĐỎ, nêu tên và dòng.
2. Ba chốt tự kiểm của `t191`: ĐỐI CHỨNG XANH (nguồn dựng lại bằng `ast.unparse` không đột biến ⇒ `t190` QUA); đúng MỘT
   miễn trừ sẵn — chốt hạn — được nhận ra; CA ÂM trong suite (chèn một chốt giả không fixture nào chạm ⇒ phép liệt kê thấy
   thêm đúng một, và miễn nó ⇒ `t190` QUA, tức "không được phủ").
3. **`t190` vế (vi):** neo prompt CÓ `tep` (đúng băm ⇒ đã đăng `rc=9`; lệch băm / tệp không có ⇒ `rc=6` cả hai trạng thái),
   `lease_id` sai ký tự và `packet_issue = 0` (`rc=8` cả hai).
4. **`t191` bắt ngay một chốt mà không reviewer nào nêu:** chốt "`granted_by` là tên provider" bị chốt allowlist ngay sau nó
   CHE về mã thoát (cùng `rc=4`; hai tập không giao nhau), nên miễn nó khi `bo_qua_han` vẫn ra `rc=4` và MỌI vế đo mã thoát
   QUA. **Vế (vi-b):** nhánh đã-có-dấu phải nêu CÙNG lý do với nhánh chưa đăng. Không có phép liệt kê bằng máy thì chốt này
   sẽ là vế (vii) của lượt 17.

**Phép đo tại `4e82a06` — TOÀN suite (186 ca), bản sao tạm, mỗi đột biến một tiến trình, `PYTHONDONTWRITEBYTECODE=1`:**

| đột biến | tập đỏ tại `4e82a06` |
|---|---|
| nền | 186/186, 0 đỏ |
| `C1` miễn neo prompt khi `bo_qua_han` | `t190`, `t191` |
| `C2` miễn regex `lease_id` | `t190`, `t191` |
| `C3` miễn `packet_issue > 0` | `t190`, `t191` — đo trên bản sao riêng (184/186): neo văn bản của lượt chung trượt vì một dòng chú thích nằm giữa |
| miễn chốt provider (chốt `t191` bắt, không reviewer nào nêu) | `t190`, `t191` |
| bỏ chốt neo ở nhánh không `tep` | `t177`, `t190`, `t191` |
| `skip_file_gates`, `drop_path` (lượt 15) | mỗi cái `t190`, `t191` |
| **CA ÂM:** chèn một chốt giả vào `kiem()` mà không thêm vế nào | **ĐÚNG `t191`** — cổng liệt kê ĐỎ được, và đỏ đúng ca |

`t191` in: 13 chốt của `kiem()` đều được `t190` phủ ở nhánh đã-có-dấu; miễn sẵn đúng một (chốt hạn). Toàn bộ 40 đột biến mà §5.0
viện dẫn được đo lại tại `4e82a06` và đối chiếu bằng máy với dữ liệu thô: khớp mọi dòng (§5.0).

**PHẠM VI CÒN HỞ của phép liệt kê — khai, đừng đọc rộng hơn:**

- **Chốt NGOÀI `kiem()`:** `_kiem_loai_so_hieu` nằm trong `kiem_github`, không trong `kiem()` — đúng F4 lượt 16 (nhánh có
  dấu KHÔNG chạy nó; đã khai từ lượt 7). `t191` không thấy nó.
- **Lời gọi chốt LỒNG trong biểu thức** (điều kiện `if`, đối số của hàm khác): không được liệt kê. *(r12: câu này SAI từ `ede00c6` — lời gọi lồng nay ĐƯỢC liệt kê; cả mục PHẠM VI CÒN HỞ này là lịch sử, văn bản hiện hành ở §0.12. Cross-review lượt 18, F3.)*
- **Chốt BÊN TRONG từng hàm `_kiem_*`:** mỗi hàm được tính MỘT chốt (miễn cả hàm). Một nhánh con bên trong, ví dụ ba lý do
  `RC_NEO` khác nhau của `_kiem_neo_prompt`, KHÔNG được liệt kê riêng.
- **Ngoại lệ không phải `Chan`**, và chốt không có dạng câu lệnh `raise` / lời gọi `_kiem_*`·`_doc_*`: không thấy.
- **Đột biến duy nhất** mà `t191` dựng cho mỗi chốt là "miễn khi `bo_qua_han`" — đúng hình dạng hồi quy đang canh. Các hình
  dạng khác (đổi mã thoát, đổi thông điệp) là việc của các vế và của `t174`–`t189`.

**Sửa hai câu F3** theo cách r10 đã làm với câu sinh đôi: §4 thôi khai "giữ nguyên nghĩa của r1 §4" (M3 và M7 khác chữ
so với r1 §4) — bảng §4 là văn bản có thẩm quyền; §0.8 câu "Không đổi ở r8" đánh dấu tại chỗ.

**Giữ nguyên §0.10:** lần thứ TƯ cùng hình dạng (acceptance/lời khai đóng băng lệch sau một bản vá) thì DỪNG và hỏi chủ kho.

**Không đổi ở r11:** bệnh, `write_set`, `M1`–`M11`, điều kiện dừng, `human_audited`, trần 3000/3. Mã: `ops/lease_publish.py`
KHÔNG đổi; chỉ `ops/lease_publish_test.py` (`t190` vế (vi)/(vi-b), `t191` và ba hàm phụ).

### 0.12 — Vì sao có revision 12: `t191` phán PHỦ bằng phép miễn TRUNG THÀNH; khai miền duyệt và hợp đồng phân loại

Cross-review lượt 18 (codex `gpt-6-astra` medium, run `4fb0ac87`, `ma_thoat=0`) trên head `b30e4e0` theo r11: `blocked`,
**P1 0 · P2 1 · P3 2 · P4 1**. Hai biểu hiện lượt 17 (AnnAssign, match) đã đóng; A23 chưa đóng cấp lớp. Nguồn của r12 —
chủ kho 25-09-2026, trong phiên điều phối, bản chiếu `issues/579#issuecomment-5831890719`: *"Mở r12 + g10 (đề xuất)"*.

- **F1 (P2) `gate-coverage-credits-nonfaithful-mutant-failure`:** đột biến "miễn" của `t191` thay lời gọi chốt bằng `""`, nên
  nó phá cả đường SẠCH hoặc đổi luồng; `t191` nhận mọi `TinHieuChotCa` làm "đã phủ". Bốn dạng chốt mới không fixture nào chạm
  — `assert … is None`, gán rồi `assert`, `len([1] if … is None else None)`, `if … is not None: return` — đều cho 186/186.
- **F2 (P3) `gate-inventory-selfchecks-omit-branch-semantics`:** bỏ nhánh riêng của guard `case`, của `and`/`or`, hay dừng ở
  phạm vi lồng trong bộ liệt kê mà tự kiểm vẫn xanh.
- **F3 (P3) `frozen-spec-inventory-scope-drift`:** §0.11 r11 khai lời gọi chốt LỒNG trong biểu thức KHÔNG được liệt kê; từ
  `ede00c6` chúng ĐƯỢC liệt kê. Lời khai đóng băng lệch mã sau một bản vá.
- **F4 (P4):** nhãn cột §5.0 r11 ghi `af6b54c` trong khi bảng đo tại `4e82a06`.

**Đếm hình dạng (§0.10):** F3 là cùng hình dạng "lời khai đóng băng lệch sau một bản vá". Luật §0.10 bắt DỪNG và hỏi — phiên
điều phối đã hỏi, chủ kho chọn mở r12 (mốc trên). Không phải executor tự mở.

**Kiến trúc hiện hành của `t191` (mã head ghi ở §5.0) — văn bản CÓ THẨM QUYỀN, thay mục "PHẠM VI CÒN HỞ" của §0.11:**

1. **Miền duyệt.** `_liet_ke_chot_kiem` đi MỌI nút con của thân `kiem()` (`ast.iter_child_nodes`), kể cả biểu thức lồng:
   điều kiện, đối số, vế phải, thân `for`/`with`/`try`/`match`. **Ranh giới:** không đi vào `def`, `async def`, `lambda`,
   `class` lồng trong `kiem()`.
2. **Nhận diện chốt.** `raise Chan(...)` (lời gọi TÊN `Chan`), và mọi lời gọi TÊN bắt đầu `_kiem_` hoặc `_doc_`. Mỗi chốt định
   danh bằng `(tên, dòng, cột)`.
3. **Phân loại miễn.** Chốt là miễn trừ đã được phép khi một tổ tiên nhắc `bo_qua_han` ở: điều kiện `if`/`while`/`… if … else …`;
   một vế ĐỨNG TRƯỚC nó trong `and`/`or`; guard `case … if`. Đúng MỘT miễn được phép: chốt hạn.
4. **Phép đếm độc lập** `_dem_chot_tho`: `ast.walk` thô trên toàn `kiem()`, kể cả phạm vi lồng. Lệch với bộ liệt kê ⇒ ĐỎ. Chốt
   trong phạm vi lồng làm hai số lệch, tức ĐỎ chứ không được tha.
5. **Phép miễn TRUNG THÀNH** (`_mien_mot_chot`): chốt vẫn CHẠY thật qua `_t191_mien(bo_qua_han, lambda: …)`, trả đúng giá trị
   thật khi chốt không ném; chỉ khi `bo_qua_han` mà chốt ném `Chan` mới nuốt (trả `None`) và ghi nhật ký. `raise … from …` ⇒
   không dựng, `KHONG_DO_DUOC`.
6. **Nhận bằng chứng** (`_phan_quyet_phu`): `PHU` khi và chỉ khi (a) bản TRONG SUỐT — ghi rồi ném lại — cho `t190` QUA, (b) bản
   miễn làm `t190` đỏ bằng `TinHieuChotCa`, (c) phép miễn đã nuốt ít nhất một `Chan`. Nhãn khác: `KHONG_CHAM` (không fixture nào
   làm chốt ném), `CHAM_KHONG_BAT` (có chạm mà `t190` không thấy), `TIN_HIEU_KHONG_MIEN`, `KHONG_DO_DUOC`.
7. **Tự kiểm của `t191`:** đối chứng xanh (`ast.unparse` không đột biến); đúng một miễn sẵn; hai phía đếm bằng nhau; **hợp đồng
   phân loại** `_PHAN_LOAI_T191` — mười dòng `(+ds, +miễn, +đếm thô)` cho guard `case` có/không nhắc `bo_qua_han`, `or`/`and`
   có nhắc ở vế trước, `or` nhắc ở vế SAU, `or` thường, và `def`/`async def`/`lambda`/`class` lồng, kèm kiểm chốt mới nằm
   đúng dòng chèn; **ca âm** `_CHOT_GIA_T191` — mười một dạng chốt giả THỰC THI ĐƯỢC (ném `Chan` khi `chot_gia_t191`), mỗi dạng
   phải được liệt kê thêm đúng một và phán `KHONG_CHAM`.

**PHẠM VI CÒN HỞ — hiện hành, đừng đọc rộng hơn:**

- Chốt NGOÀI `kiem()` (F4 lượt 16: `_kiem_loai_so_hieu` trong `kiem_github`).
- Chốt BÊN TRONG từng hàm `_kiem_*`: mỗi lời gọi là MỘT chốt; nhánh con bên trong không được liệt kê riêng.
- Lời gọi qua bí danh hoặc thuộc tính (`f = _kiem_x; f(…)`, `mod._kiem_x(…)`): không nhận diện.
- Ngoại lệ không phải `Chan`; chốt không có dạng `raise Chan` / lời gọi `_kiem_*`·`_doc_*`.
- Biểu thức gán `:=` NẰM TRONG đối số của một chốt: lambda bọc đổi phạm vi của nó.
- Miễn qua biến trung gian (`skip = bo_qua_han; if not skip: …`): KHÔNG được xếp là miễn, nên chốt ấy vào `ds` và phải được
  phủ — hỏng theo hướng ĐỎ, không theo hướng tha.
- **Hai vế phòng thủ của `_phan_quyet_phu` không có ca âm phân biệt:** điều kiện (c) và phép chặn khi bản trong suốt không QUA.
  Với phép bọc hiện tại, bản không nuốt thì hành vi giống hệt nguồn, nên không dựng được đầu vào làm (c) hay (a) đổi kết quả;
  đột biến gỡ từng vế SỐNG (đo ở bảng dưới). Khai là tương đương TRONG MIỀN phép bọc hiện tại, không phải tương đương tuyệt đối.

**Mã head `1ae3cff`** = `962b84b` (bản vá `t191`) + hoà master `b7973df` (#623, không chạm write set). `ops/lease_publish.py`
và `CLAUDE.md` KHÔNG đổi từ `8d04b78`/lượt 17. Suite `186/186; đã chạy=186, bỏ qua=0`, `rc=0`; `t191` in: 13 chốt đều `PHU`,
miễn sẵn `('raise Chan', 895, 8)`, phân loại 10 dòng, ca âm 11 dạng. Trần: +2792 dòng thêm, 3 tệp (merge-base `b7973df`).

**Vế `t190` bắt từng chốt thật** (phép miễn trung thành, bản miễn; mọi hàng: đã nuốt, `TinHieuChotCa`) — khớp bảng của reviewer
lượt 18 từng hàng:

| dòng | chốt | vế `t190` |
|---:|---|---|
| 824 | thiếu trường | (ii) thiếu `granted_by` — `KeyError` trần ở fixture thiếu trường, không phải vế sạch |
| 831 | người cấp là provider | (vi-b) lý do khác giữa chưa/đã đăng |
| 838 · 851 | allowlist người cấp · `GITHUB_ACTOR` | người cấp / actor không thẩm quyền, mong 4 nhận 9 |
| 859 · 863 | `packet_issue` · regex `lease_id` | (vi) mong 8 nhận 9 |
| 866 · 867 | `_kiem_con_tro_treo` · `_kiem_bia_mo` | (v) fixture `t99` / `t100`, mong 8 nhận 9 |
| 873 | dạng SHA | mong 8 nhận 9 |
| 876 | `_kiem_lop_review` | fixture `t74`, mong 10 nhận 9 |
| 884 · 888 | neo không `tep` · `_kiem_neo_prompt` | (ii) / (vi) mong 6 nhận 9 |
| 890 | `_doc_han` | (ii) hạn hỏng dạng, mong 8 nhận 9 |

**Đo lại TOÀN bảng §5.0 tại `1ae3cff`** — 61 đột biến (41 của r11 + 20 của lượt 16–18), toàn suite, cùng phép đo chung của
§5.0; so bằng máy với dữ liệu thô `4e82a06`: 37/41 hàng cũ KHỚP tập đỏ nguyên văn; bốn hàng còn lại lệch
đúng MỘT ca, và ca ấy thuộc một trong hai ca không tất định: `t125` (ASSERT, ca A/B, Issue #619) mất ở `tiền kiểm nuốt cả bốn`
và thêm ở `P1 miễn GITHUB_ACTOR`; `t154` (TRAN `ValueError`, ca đo thời gian, chạy dưới tải ba tiến trình) thêm ở `P1 không
kiem` và `P1 thiếu bo_qua_han`. Không ca nào trong họ `t174`–`t191` lệch. Nên cột tập đỏ của §5.0 giữ nguyên chữ, nhãn cột đổi
sang `1ae3cff` (F4), trừ các ô đổi ghi dưới.

| đột biến lượt 18 | tập đỏ toàn suite tại `1ae3cff` |
|---|---|
| chốt mới ASSERT · ASSERT_ASSIGN · LEN · IF_RETURN (hàm giả đặt trước `def kiem(`) | mỗi cái **ĐÚNG `t191`** (trước bản vá: 186/186) |
| bộ liệt kê bỏ nhánh `match_case` · `BoolOp` · dừng phạm vi · `If` | mỗi cái **ĐÚNG `t191`** |
| phép miễn kiểu cũ (trả `""`, không chạy chốt) | **ĐÚNG `t191`** |
| gỡ vế "đã nuốt" · gỡ chặn bản trong suốt | **SỐNG** — xem PHẠM VI CÒN HỞ |

**Không đổi ở r12:** bệnh, `write_set`, `M1`–`M11`, điều kiện dừng (`0` finding P1/P2/P3), `human_audited`, trần 3000/3, mọi
tiêu chí A1–A22 (chỉ ô số đo A4/A7–A10 và nhãn cột).

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

| vế | r3 → r4 | r4 → r5 | **r5 → r6** | **r6 → r7** |
|---|---|---|---|---|
| bảng `write_set` ba đường giống nhau | `True` | `True` | `True` | `True` |
| §2.0 byte-equal | `True` | `True` | `True` (1215 B) | `True` |
| §2.1 byte-equal | `True` | `True` | `True` (1066 B) | `True` |
| §2.2 byte-equal | `True` | `True` | `True` (1328 B) | `True` |
| §2.3 byte-equal | `True` | `True` | `True` (642 B) | `True` |
| câu vế DÒNG | **ĐỔI** (`không đạt` → `vượt trần GỐC nhưng trong trần đã nới`) | giữ nguyên | giữ nguyên | **ĐỔI** (con số, xem §8) |

Hai cột cuối là thứ lượt 6 đòi (`spec-guarantees-still-lack-adjacent-measurements`): r6 mở rộng
lời bảo đảm tới chính nó mà bảng đo dừng ở r5. Reviewer đo giúp và ba vế ĐÚNG — lỗi là **thiếu
chứng cứ TẠI CHỖ**, không phải sai nội dung. Nay chứng cứ nằm ngay đây.

**PHÉP ĐO NÀY ĐÃ SAI MỘT LẦN, ghi lại vì cái sai đáng hơn con số.** Bản đo đầu cắt các tiểu mục
theo **thứ tự SỐ** (`2.0 → 2.1 → 2.2 → 2.3`) và ra: §2.0 `False` (1857 vs 2539 B), §2.3 `False`
(3036 vs 4921 B), §2.2 *"không cắt được"*. Suýt thành một finding về chính r6. Nhưng tệp xếp các
mục theo thứ tự **`2.0, 2.3, 2.1, 2.2`** — không theo số — nên mọi khoảng cắt đều sai. Cắt theo
thứ tự THẬT (duyệt `^### (2\.\d)` rồi lấy khoảng giữa hai mốc liên tiếp) ⇒ cả bốn `True`.

Cùng LỚP với hai lời khai sai ở §12.2: **đo bằng một giả định về HÌNH THỨC rồi khai thành một
SỰ KIỆN CẤU TRÚC.** Dấu hiệu rẻ đã cứu lần này: một phần của phép đo trả *"không tìm thấy"* thì
**nghi BỘ ĐO trước khi nghi DỮ LIỆU**.
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

**Bảng dưới là văn bản CÓ THẨM QUYỀN của `M1`–`M11`.** r1 §4 là lịch sử; nhiều dòng đã đổi nghĩa qua các revision (M3 và M7 khác chữ so với r1 §4 — so hai bảng; M1/M4 đổi nghĩa ở r9) và đánh dấu tại dòng. *(r11 sửa: r2–r9 viết `M1`–`M8` giữ nguyên byte nghĩa của r1 §4; r10 viết `M2`, `M3`, `M5`–`M8` giữ nguyên nghĩa — cả hai sai, vì M3 và M7 đã khác chữ r1 §4; cross-review lượt 16, F3, §0.11.)*

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | `kiem_github` dò dấu "đã đăng" TRƯỚC khi gọi `kiem()`. Có dấu ⇒ tệp HIỆN TẠI vẫn phải qua MỌI chốt của `kiem()` TRỪ chốt hạn, rồi mới `Chan(RC_DA_DANG)`. *(r9 sửa: r1–r8 viết "có dấu ⇒ `Chan(RC_DA_DANG)` ngay" — đúng là hành vi đã dựng, và chính là lỗ P1 connector codex bắt trên #589; §0.9.)* | `ops/lease_publish.py` |
| **M2** | Tiền kiểm miền fail-close: thiếu `lease_id`/`packet_issue`, hoặc `packet_issue` sai kiểu ⇒ `Chan(RC_NOI_DUNG)`, không ngoại lệ trần. | `ops/lease_publish.py` |
| **M3** | Không dấu ⇒ hành vi KHÔNG ĐỔI so `origin/master`: cùng thứ tự lỗi, cùng mã thoát — **kể cả khi lease mắc NHIỀU lỗi cùng lúc**. Vế sau là chỗ r2 khai thiếu và bản vá đầu làm sai; xem `M10`. | `ops/lease_publish.py` |
| **M4** | Docstring `kiem_github` khai GIÁ PHẢI TRẢ, ĐÚNG với mã hiện hành: miễn trừ DUY NHẤT của nhánh đã-có-dấu là chốt hạn (`bo_qua_han`); giá CÒN LẠI là một người CÓ thẩm quyền sửa lease đã đăng thì bản chiếu cũ đi. *(r9 sửa: r1–r8 đòi khai "các chốt của `kiem()` không chạy nữa" — không còn đúng sau bản vá P1.)* | `ops/lease_publish.py` |
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

### 5.0 — Bảng nghiệm thu CÓ THẨM QUYỀN (r12) — mọi tập đỏ đo tại `1ae3cff`, TOÀN suite

**Phép đo chung của mọi dòng:** bản sao tạm của `1ae3cff`, đột biến áp lên bản sao, chạy MỌI ca trong `CA` (186) trong
một tiến trình con mới với `ops/` ở đầu `sys.path`, `PYTHONDONTWRITEBYTECODE=1`, `GITHUB_ACTOR` gỡ, `commit.gpgsign=false`
chỉ cho tiến trình đo. Mỗi ca: `CHOT` = `TinHieuChotCa`; `ASSERT` = `AssertionError` khác (họ `bang` của ca cũ, không
phải tín hiệu riêng). **Nền: 186/186, 0 đỏ.** Từ r11 hầu như mọi đột biến chạm `t190` cũng làm `t191` đỏ — đúng thiết kế, vì `t191` chạy `t190` dưới đột biến của chính nó và dưới đối chứng. "Tập đỏ" dưới đây là ĐỦ các ca đỏ trên toàn suite, không chỉ trong họ
`t174`–`t191`. Mọi tiêu chí đòi ca đích nằm TRONG tập đỏ; tiêu chí nào đòi hơn thế (ĐÚNG MỘT ca, không đỏ ca kia) thì
nói ra ở cột tiêu chí.

| # | tiêu chí | đột biến | tập đỏ đo tại `1ae3cff` |
|---|---|---|---|
| **A1** | Hết hạn + ĐÃ có dấu ⇒ `rc=9`. | dò dấu về SAU `kiem()` | `t174`, `t182`, `t190`, `t191` — `t175` QUA |
| **A2** | Hết hạn + KHÔNG dấu ⇒ `rc=8`. **Cặp A1/A2 phân biệt:** đột biến của A1 phải làm `t174` ĐỎ mà `t175` QUA; đột biến của A2 phải làm `t175` ĐỎ mà `t174` QUA. Một đột biến làm CẢ HAI đỏ, hoặc hai ca luôn cùng màu, nghĩa là cặp đang đo một thứ. | phép dò ném `rc=9` vô điều kiện | `t43` `t44` `t45` `t46` `t49` (ASSERT), `t175`, `t177`, `t178`, `t179`, `t181`, `t183`, `t184`, `t185`, `t187`, `t191` — `t174` QUA |
| **A3** | Còn hạn + ĐÃ có dấu ⇒ `rc=9`. | gỡ HAI cửa (dò sớm + chốt cuối) | `t46` (ASSERT), `t174`, `t176`, `t179`, `t181`, `t182`, `t183`, `t190`, `t191` |
| **A4** | Còn hạn + KHÔNG dấu ⇒ `rc=0`, và mọi chốt của `kiem()` vẫn chạy: tự cấp ⇒ 4, neo prompt không kiểm được ⇒ 6, thiếu trường ⇒ 8. | phép dò ném `rc=9` khi KHÔNG có dấu (sau lời gọi dò) — bốn kết quả `9/4/6/8` (cross-review lượt 15 đo): lease sạch nhận 9, ba lỗi vẫn bị `kiem()` chặn | `t43` `t44` `t45` `t46` `t49` (ASSERT), `t175`, `t177`, `t185`, `t191`. *Đột biến cũ "tiền kiểm nuốt cả bốn ca" SỐNG ở `t177` (tập đỏ `t178` `t179` `t181` `t183` `t184` `t187`; `t125` (ASSERT) có ở `4e82a06`, không có ở `1ae3cff` — ca A/B không tất định, Issue #619) — không dùng.* |
| **A5** | M2 fail-close: thiếu `lease_id` · thiếu `packet_issue` · `packet_issue` sai kiểu · `bool` ⇒ `rc=8`, không ngoại lệ trần. Răng DUY NHẤT sau P1 là SỐ LỜI GỌI GitHub (`0` so `1`). | `_tien_kiem_mien_dang` trả về ngay | `t178`, `t180` |
| **A6** | `t32` đạt; bước `tìm lease vừa đổi` chỉ lấy lease NHÁNH ẤY thêm. | bước ấy quét cả `ops/leases/` (`find`) — trên bản sao, workflow ngoài write set | `t32` (ASSERT) |
| **A7** | Suite `N/N` hai số BẰNG NHAU, `bỏ qua = 0`, `N ≥ 173`. | — | `186/186; đã chạy=186, bỏ qua=0`, `rc=0` đọc trực tiếp (`actionlint 1.7.7` trên PATH) — tại `1ae3cff`, máy yên. Lượt chạy CÙNG LÚC với ba tiến trình đo cho 185/186: `t154` (TRAN `ValueError` khi đọc tệp nhịp tim rỗng) — chạy riêng 5/5 QUA; ca đo thời gian, ngoài write set đổi |
| **A8** | `git diff --numstat` merge-base..HEAD chạm ĐÚNG ba đường write set. | — | `CLAUDE.md` 27/0 · `ops/lease_publish.py` 161/2 · `ops/lease_publish_test.py` 2604/5 (merge-base `b7973df`; tổng +2792, trần 3000) — ĐO LẠI tại head đang xét |
| **A9** | `doctrine-scan` `rc=0`. | — | `rc=0` tại `1ae3cff` |
| **A10** | `adr-song` · `doc-claims-check --strict` · `git diff --check` `rc=0`; `actionlint` DELTA so master = 0. | — | ba lệnh `rc=0`; `actionlint 1.7.7` + `shellcheck 0.9.0`: master và head đều `rc=1`, cùng một finding `ops-don-ref.yml:117 SC1003:info` ⇒ DELTA 0. Tại `1ae3cff`: `.github` bằng byte master `b7973df` (`git diff` rỗng), `actionlint` `rc=1` cùng finding ấy; `git diff --check` so merge-base `b7973df` `rc=0` |
| **A11** | Phản chứng hai chiều: lease đã đăng + đã hết hạn ⇒ master `rc=8`, ứng viên `rc=9`. | — (đối chứng âm là master) | fixture `_lease_579` hết hạn 48h qua `_dung_gh_579`: `601a0f1` có dấu 8 · không dấu 8; ứng viên (mã `ops/lease_publish.py` không đổi từ `af6b54c`) có dấu **9** · không dấu 8. Hiện vật của lượt `35519177197` KHÔNG dựng lại — giới hạn khai |
| **A12** | Nhánh nuốt của phép dò không được tự phán: ném `rc=9` ⇒ `t179` ĐỎ; bỏ điều kiện `c.ma == RC_DA_DANG` ⇒ `t179` ĐỎ. Hai đột biến cùng LỚP, không phải hai chốt độc lập. | (i) nhánh nuốt ném 9 · (ii) ném lại mọi `Chan` | (i) `t179`, `t184`, `t187` · (ii) `t178`, `t179`, `t180`, `t181`, `t183` |
| **A13** | Chưa đăng + tự cấp + `packet_issue` sai kiểu ⇒ `rc=4`, bằng nền master, 0 lời gọi GitHub. | tiền kiểm ra NGOÀI `try` | `t178`, `t180` |
| **A14** | `packet_issue: True` ⇒ `rc=8` và 0 lời gọi GitHub. | gỡ `isinstance(so, bool)` | `t178` |
| **A15** | `/comments` hỏng vĩnh viễn ⇒ cổng vẫn chặn. | `I` — gỡ lời gọi ở cửa cuối | `t179`, `t181`, `t183` |
| **A16** | `lease` không phải ánh xạ ⇒ `Chan(rc=8)` có tên, 0 lời gọi, không ngoại lệ trần. | `J` — chốt hình dạng vào trong `try` | `t182` — đúng một ca |
| **A17** | Dò đầu KHÔNG ĐO ĐƯỢC rồi mạng phục hồi ⇒ cửa cuối trả `rc=9`, ≥ 2 lần đọc. | `K` — cửa cuối nuốt riêng `rc=9` | `t183` — đúng một ca |
| **A18** | Phép dò ném ngoại lệ KHÔNG phải `Chan` ⇒ nhường `kiem()` (`rc=4`), ca đỏ bằng chot của nó khi nhánh nuốt bị gỡ. | `X` — gỡ `except Exception` | `t179` — đúng một ca |
| **A19** | Hợp đồng `_goi_lop_gh` (a)–(e), (a2), chẩn đoán `str` thuần. | `N1` trả `None` · `N2` `BaseException` · `N3` `__eq__`→`True` · `N3b` `__ne__`→`False` · `N4` `__str__` bỏ tên lớp (`_NgoaiLeLa` / `_MaVang`) · `N5` gộp `Chan` vào `_NgoaiLeLa` · `N6` trả `_NgoaiLeLa(None)` khi không ném | `N1` `t184` `t187` · `N2` `t184` `t187` · `N3` `t184` `t191` · `N3b` `t179` `t184` · `N4` `t184` `t187` (cả hai biến thể) · `N5` 21 ca (`t43` `t44` `t46` `t48` `t55a` `t57` `t126` ASSERT; `t174`–`t185` cả 12 ca, `t190` và `t191`) · `N6` 11 ca (`t45` `t46` `t47` `t54` `t55b` `t57` `t126` ASSERT; `t177` `t178` `t184` `t185`). *Đột biến "bỏ hẳn `__eq__`" SỐNG — `object.__eq__` so danh tính nên vẫn `False`; không dùng.* |
| **A20** | Mọi chốt SỐ LỜI GỌI chốt KẾT QUẢ trước, qua cửa `_goi_dem_lop_gh`. | `D1` gỡ vế kết quả · `D2` gỡ vế đếm · `R_probe` ném `ValueError` đầu `_do_dau_da_dang` với `lease_id` không phải `str` | `D1` `t185` · `D2` `t185` · `R_probe` `t178` |
| **A21** | Không chốt số lời gọi NGOÀI cửa (đo bằng `ast`). | `D3` thêm một hàm chốt `len(gh.calls)` ngoài cửa | `t186` — đúng một ca |
| **A22** | Chẩn đoán hạ về `str` THUẦN. | `Pstr` trả nguyên `x` khi `isinstance(x, str)` | `t187`, `t189` |
| **A23** | Lease ĐÃ ĐĂNG mà tệp bị SỬA vẫn phải qua `kiem()` trừ chốt hạn. **Danh sách chốt KHÔNG liệt kê tay và phán quyết phủ KHÔNG nhận đỏ bất kỳ:** `t191` liệt kê theo §0.12 mục 1–4, phán `PHU` theo mục 5–6 (bản trong suốt QUA · bản miễn đỏ bằng `TinHieuChotCa` · phép miễn đã nuốt `Chan`); đúng MỘT miễn sẵn (chốt hạn); đối chứng xanh; hợp đồng phân loại 10 dòng; 11 dạng ca âm đều phải `KHONG_CHAM`. Tại `1ae3cff`: 13 chốt, cả 13 `PHU`, vế `t190` bắt từng chốt ở bảng §0.12; miễn sẵn đúng một. Phạm vi còn hở: §0.12. | (a) 11 đột biến bản vá P1 (như r11) · (b) lượt 16: `C1` · `C2` · `C3` · miễn chốt provider · `C6~` bỏ neo nhánh không `tep` · chốt giả không vế · (c) lượt 17: chốt mới dạng AnnAssign · dạng `match` · NGƯỢC: neo thành AnnAssign · (d) lượt 18: chốt mới ASSERT · ASSERT_ASSIGN · LEN · IF_RETURN · bộ liệt kê bỏ nhánh `match_case` / `BoolOp` / dừng phạm vi / `If` · phép miễn kiểu cũ (trả `""` không chạy chốt) · gỡ vế "đã nuốt" · gỡ chặn bản trong suốt | (a) chín đột biến: `t190`, `t191`; thiếu `bo_qua_han`: `t174`, `t190`, `t191`; ném mã khác: `t46` (ASSERT), `t174`, `t176`, `t190`, `t191` · (b) `C1`, `C2`, `C3`, provider: mỗi cái `t190`, `t191`; `C6~`: `t177`, `t190`, `t191`; chốt giả: **ĐÚNG `t191`** · (c) AnnAssign, `match`: **ĐÚNG `t191`**; NGƯỢC: không đỏ (186/186) · (d) bốn dạng chốt mới: mỗi cái **ĐÚNG `t191`**; bốn nhánh bộ liệt kê: mỗi cái **ĐÚNG `t191`**; phép miễn kiểu cũ: **ĐÚNG `t191`**; hai vế phòng thủ: **SỐNG** — tương đương trong miền phép bọc hiện tại, khai ở §0.12 |

**Không tiêu chí nào đóng bằng `rc=0`.** Tập đỏ đổi khi mã đổi: người đo sau phải ĐO LẠI tại head đang xét, không chép
cột trên. Công cụ đo và bảng thô nằm ngoài kho (bản sao tạm của phiên executor) — đây là giới hạn khai, không phải
bằng chứng; reviewer phải tự chạy lại.

### 5.1 — LỊCH SỬ r3–r9: KHÔNG chi phối nghiệm thu từ r10 (và bảng §5.0 của r10, tập đỏ tại `af6b54c`, cũng là lịch sử từ r11)

Mọi thứ trong mục này là LỊCH SỬ có neo: cột *phép đo* ghi số của lượt/head nêu kèm, và chỗ nào không nêu head thì là số tại lúc revision ấy đóng băng. Nghiệm thu từ r10 đọc **§5.0**. Giữ lại vì các ca test và các verdict cũ viện dẫn các dòng này.


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

*(r10: câu kế thừa dưới đây HẾT HIỆU LỰC — `A2` và `A4` của r1 đã lệch phép đo; §5.0 chép lại đủ.)* `A1`, `A2`, `A4`, `A6`, `A8`–`A11` của r1 §5 giữ nguyên. `A3`, `A5`, `A7` viết lại ở r3;
`A12`–`A14` mới ở r3; `A15`–`A17` mới ở r4; `A16` viết lại và `A18`–`A19` mới ở r5; **`A19` thêm vế (e)/(a2) và `A20`–`A22` mới ở r7**.

**Vì sao `A15`–`A17` phải có, và vì sao chúng là khuyết tật của r3 chứ không phải bổ sung tuỳ ý:**
`t181`, `t182`, `t183` đã tồn tại trong mã (hai ca đầu từ lượt 2, ca cuối từ lượt 3) và docstring
của chúng viện dẫn `A15`/`A16`/`A17` — nhưng bảng nghiệm thu của r3 chỉ có tới `A14`. Một ca test
viện dẫn một tiêu chí KHÔNG TỒN TẠI thì cái nó viện dẫn không ràng buộc được gì: nó đọc như đã có
thẩm quyền trong khi không có. Cùng lớp *"cổng vắng mặt trông giống cổng xanh"*.

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A3** (viết lại) | Lease **còn hạn + ĐÃ có dấu** ⇒ mã **9** (hành vi cũ, không đổi). | Đột biến **gỡ HAI CỬA** (cả dò sớm lẫn chốt cuối) ⇒ `t176` ĐỎ. **KHÔNG** dùng đột biến "bỏ hẳn tiền kiểm": đã đo, nó làm `t176` QUA vì cửa cuối vẫn trả 9. Một tiêu chí nêu sai đột biến là một tiêu chí không thể đỏ. |
| **A5** (viết lại) | **M2 fail-close**, và khai đúng ca nào có răng: thiếu `lease_id` ⇒ `rc=8` · thiếu `packet_issue` ⇒ `rc=8` · `packet_issue` sai kiểu ⇒ `rc=8` · `packet_issue` là `bool` ⇒ `rc=8`. | Đột biến bỏ tiền kiểm miền: hai ca THIẾU TRƯỜNG **không đổi gì** (bộ tương đương — `_do_dau_da_dang` nuốt `KeyError` rồi `kiem()` dựng lại `rc=8`); ca **sai kiểu** đổi `8 → 9` TRƯỚC bản vá P1; SAU bản vá P1 (nhánh đã-có-dấu chạy `kiem()`) mã thoát KHÔNG đổi (`8 → 8`, đo 25-09), nên răng DUY NHẤT còn lại là SỐ LỜI GỌI GitHub: `0 → 1`. *(r9 sửa theo cross-review lượt 14.)* **Không** đòi ngoại lệ trần — đã đo là không có. |
| **A7** (siết) | Suite `ops/lease_publish_test.py` **N/N hai số BẰNG NHAU**, `bỏ qua = 0`, và `N ≥ 173`. | `rc` đọc **trực tiếp**, không qua pipe. Nền 166 + 6 ca của r2 + `t180` của r3 = 173. Bất đẳng thức chứ không phải số tuyệt đối — #578 đang ghi cùng tệp, xem §2.3. |
| **A12** (mới, cho `M9`) | Đột biến cho nhánh nuốt ném `Chan(RC_DA_DANG)` ⇒ ca `M9` **ĐỎ**. Và đột biến bỏ điều kiện `if c.ma == RC_DA_DANG` (ném lại MỌI `Chan`) cũng ⇒ ca ấy **ĐỎ**. | Hai đột biến ấy **cùng lớp** (phép dò tự phán thay cổng), nên đừng khai chúng là hai chốt độc lập. Chúng chứng minh ca có răng, không chứng minh có hai cửa. |

| **A13** (mới, cho `M10`) | Lease **chưa đăng** mắc HAI lỗi cùng lúc — tự cấp **và** `packet_issue` sai kiểu — ⇒ `rc=4`, **bằng đúng nền `origin/master`**, và **0** lời gọi GitHub. | Đột biến đưa `_tien_kiem_mien_dang` trở ra NGOÀI `try` (tức khôi phục hồi quy) ⇒ ca ĐỎ. Đã đo (r3): đột biến ấy giết **đúng một** ca, `t174`–`t179` đều QUA — nên ca này KHÔNG phải bộ tương đương với ca nào có sẵn. *(r10: tập ấy đã đổi — đo lại tại `af6b54c` toàn suite: `{t178, t180}`; §5.0.)* |
| **A14** (mới, cho `M11`) | `packet_issue: True` ⇒ `rc=8` **và 0 lời gọi GitHub**. | Đột biến gỡ điều kiện `isinstance(so, bool)`, giữ nguyên mọi thứ khác ⇒ ca ĐỎ. Trước `M11` đột biến ấy **sống sót `172/172`**. Nó ĐỎ qua SỐ LỜI GỌI (`0 → 1`), **không** qua mã thoát — mã thoát là `8` ở cả hai bên, nên một tiêu chí chỉ đọc `rc` sẽ mù đúng chỗ này. |
| **A15** (mới ở r4, cho `t181`) | API `/comments` hỏng **vĩnh viễn** ⇒ cổng vẫn PHẢI chặn, không được coi "không đọc được" là "chưa đăng". | Đột biến **I** — gỡ hẳn lời gọi `_kiem_comment_da_co` ở cửa cuối của `kiem_github` ⇒ `t181` ĐỎ, và đỏ bằng `TinHieuChotCa` của chính nó. Đo lượt 2: toàn suite `174/175`, đỏ ĐÚNG MỘT ca. **Phép đếm `== 3` lời gọi trong ca này ghim SỐ INVOCATION của cài đặt hiện tại, KHÔNG tự chứng minh ba cửa độc lập** — reviewer lượt 3 (N3) đo ra điều đó, và r4 khai thẳng thay vì để người đọc suy ra một điều mạnh hơn phép đo. |
| **A16** (mới ở r4, **viết lại ở r5**, cho `t182`) | `lease` KHÔNG PHẢI ánh xạ (`None` · `[]` · `True` · `55` · `"55"`) ⇒ `Chan(rc=8)` **CÓ TÊN**, và **0** lời gọi GitHub. Không ngoại lệ TRẦN nào thoát khỏi cổng. | Đột biến **J** — đưa chốt HÌNH DẠNG trở vào trong `try` của `_do_dau_da_dang` ⇒ `t182` ĐỎ, **bằng chot RIÊNG của nó**. Đo `d38de01`: J ⇒ `176/177`, đỏ ĐÚNG MỘT ca, thông điệp *"lease là None: phải ném `Chan(rc=8)` có tên, được rc=KHÔNG-CÓ-MÃ (ngoại lệ TRẦN AttributeError: …)"*. **r5 đổi CƠ CHẾ, không đổi tiêu chí:** r4 đạt vế "tín hiệu riêng" bằng một helper dành RIÊNG cho `t182` (`_goi_bat_tron`); lượt 4 chứng minh cách ấy ĐÚNG mà HẸP (xem `A19`), nên `_goi_lop_gh` nay lo việc đó cho MỌI ca và helper riêng đã gỡ. |
| **A18** (mới ở r5, cho `t179`) | Phép dò ném một ngoại lệ **KHÔNG PHẢI `Chan`** ⇒ vẫn phải NHƯỜNG cho `kiem()` phán (`rc=4` cho lease tự cấp), và ca phải ĐỎ **bằng chot của chính nó** khi nhánh nuốt bị gỡ. | Đột biến **X** — nhánh `except Exception` của `_do_dau_da_dang`: `return` → `raise`. Đo `d38de01`: `176/177`, đỏ ĐÚNG `t179`, thông điệp *"ngoại lệ lạ từ phép dò cũng phải nhường cho `kiem()` (rc=4), được rc=KHÔNG-CÓ-MÃ (ngoại lệ TRẦN RuntimeError: …)"*. Trước `A19`, `X` làm `t179` đỏ bằng `RuntimeError` **thoát ra trước** chot — tức tín dụng giả, đúng thứ `A16` đã phải sửa một lần cho `t182`. |
| **A19** (mới ở r5, cho `t184` — ĐO CHÍNH CÁI THƯỚC ĐO) | `_goi_lop_gh` giữ **nguyên** hợp đồng cũ và thêm ĐÚNG một hình dạng: (a) cổng ném `Chan` ⇒ trả chính `Chan` ấy · (b) cổng ném ngoại lệ TRẦN ⇒ trả `_NgoaiLeLa`, `.ma` **`==` SAI** và **`!=` ĐÚNG** với mọi mã thoát, `str(.ma)` **nêu TÊN LỚP** · (c) không ném gì ⇒ `None` · (d) `KeyboardInterrupt` **KHÔNG** bị nuốt · **(e) mới ở r7** — helper **LUÔN TRẢ VỀ**, không bao giờ NÉM, và mọi vế đòi trả về phải đo điều đó TỪ PHÍA NGƯỜI GỌI (cửa `_goi_doi_tra_ve`) · **(a2) mới ở r7** — vế (a) đo DANH TÍNH ĐỐI TƯỢNG (`returned is expected`), không chỉ danh tính LỚP · **chẩn đoán phải là `str` THUẦN**, không phải chỉ `isinstance(..., str)`. | Mỗi vế một đột biến, chạy TOÀN suite trên bản sao rời, đo trên `d38de01` (nền `177/177`): `N1` helper trả `None` ⇒ ĐỎ đúng vế (b) · `N2` `except Exception`→`BaseException` ⇒ vế (d) · `N3` `__eq__`→`True` ⇒ vế (b `==`) · `N3b` `__ne__`→`False` ⇒ vế (b `!=`) · `N4` `__str__` bỏ tên lớp ⇒ vế (b `str`) — cả năm `176/177`, đỏ ĐÚNG MỘT ca. `N5` gộp `Chan` vào `_NgoaiLeLa` ⇒ `159/177` và `N6` trả `_NgoaiLeLa` khi không ném gì ⇒ `168/177`, cả hai gồm vế (a)/(c). **KHAI CHO ĐÚNG: `N5`/`N6` KHÔNG phải đột biến một-đích** — chúng phá hợp đồng cũ nên kéo theo nhiều ca; điều đó chứng minh vế (a)/(c) có răng, KHÔNG chứng minh chúng là chốt duy nhất cho hợp đồng ấy. |
| **A20** (mới ở r7, cho `t185`) | **Mọi chốt SỐ LỜI GỌI phải chốt KẾT QUẢ trước.** `_goi_dem_lop_gh` là cửa DUY NHẤT, chốt cả hai vế; `_do_kiem_github` **KHÔNG còn trả** số lời gọi, nên không ai lấy được vế ấy ra mà quên vế kia. Nhãn `DA_TRA_VE` riêng, KHÔNG dùng `0` (vì `RC_OK` cũng `0`). | Ba đột biến, mỗi vế một cái, đo trên `d27cba2` (nền `180/180`): `D1` gỡ vế KẾT QUẢ ⇒ `t185` (a) ĐỎ · `D2` gỡ vế ĐẾM ⇒ `t185` (b) ĐỎ · và phản chứng gốc `R_probe` (ném trước khi chạm mạng, đúng năm đầu vào của vế `lease_id`) ⇒ `t178` ĐỎ. **`R_probe` từng SỐNG `177/177`** trên `94d3cd9` — đó là lý do tiêu chí này tồn tại. Cả ba `179/180`, đỏ ĐÚNG MỘT ca. `t185` có ĐỐI CHỨNG XANH chạy TRƯỚC hai vế đỏ; thiếu nó thì "cửa đỏ với mọi thứ" cũng qua. |
| **A21** (mới ở r7, cho `t186`) | **KHÔNG ca nào được chốt số lời gọi NGOÀI cửa.** Đo bằng `ast` (không `grep`): mọi `Compare` có `len(<x>.calls)` phải nằm trong `_goi_dem_lop_gh`. Danh sách CHO PHÉP đúng MỘT phần tử và biết trước. | Đột biến `D3` viết lại một chốt đếm ngoài cửa ⇒ `t186` ĐỎ, nêu ĐÚNG dòng và ĐÚNG hàm. `179/180`. Ca còn tự kiểm bộ dò: bơm một hình dạng bị cấm vào `ast.parse` phải thấy ĐÚNG 1 — **một phép kiểm không thể ĐỎ thì không phải bằng chứng**. KHÔNG cấm `t48` (`not any(POST in calls)`): đó là VỊ TỪ, không phải SỐ ĐẾM, và nó nằm chung biểu thức với vế kết quả. |
| **A22** (mới ở r7, cho `t187`) | **Chẩn đoán phải hạ về `str` THUẦN.** `isinstance(x, str)` ĐÚNG với LỚP CON, mà lớp con ghi đè được `__str__`/`__format__`/`__repr__` — thông điệp rồi nổ trong f-string của `chot`. Áp cho CẢ hai trường của `_MaVang` (`kieu` cũng có thể là `str` con). | Đột biến `Pstr` trả nguyên `x` khi `isinstance` đúng ⇒ `t187` ĐỎ, `179/180`. Ca đo theo **HỌ 6 thành viên** (hỏng `__str__` · `__format__` · `__repr__` · cả ba · `__getattribute__` · ném TÍN HIỆU DỪNG) — một nhãn một đại diện là nhãn rộng hơn tập fixture (#574 `m12/m13/m14`). Có **ĐỐI CHỨNG XANH**: chuỗi thường phải qua NGUYÊN VẸN, nếu không một cài đặt trả hằng cũng qua hết. Ba cách hạ đều đo được cho `str` thuần: `str.__str__(x)` · `x[:]` · `"".join((x,))`; `str(x)`, `"%s" %`, f-string đều NÉM. |
| **A23** (mới ở r9, cho `t190`) | **Lease ĐÃ ĐĂNG mà tệp bị SỬA vẫn phải qua `kiem()` trừ chốt hạn.** Dấu "đã đăng" chỉ nói TÊN lease đã đăng, không nói tệp HIỆN TẠI là tệp đã đăng. Sạch ⇒ `rc=9`; tự cấp ⇒ 4; neo prompt không kiểm được ⇒ 6; thiếu trường ⇒ 8; hạn hỏng dạng ⇒ 8; hết hạn ⇒ 9; hết hạn + tự cấp ⇒ 4; và CẢ HỌ chốt khác (lớp review ⇒ 10, người cấp ngoài danh sách ⇒ 4, `reviewed_sha` sai dạng ⇒ 8, `GITHUB_ACTOR` không thẩm quyền ⇒ 4) cùng mã ở cả chưa đăng lẫn đã đăng. | Chín đột biến một-đích, mỗi cái chết ở `t190` bằng `TinHieuChotCa`: gỡ lời gọi `kiem(..., bo_qua_han=True)`; gọi không kèm `bo_qua_han`; `bo_qua_han` thoát sớm; `bo_qua_han` bỏ luôn việc đọc hạn; nhánh đã-có-dấu ném mã khác; và bốn "miễn thêm một chốt khi `bo_qua_han`" (lớp review, danh sách người cấp, `GITHUB_ACTOR`, dạng SHA). |
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
20. **Đột biến `L` của cross-review lượt 4 SỐNG SÓT `176/176`** — và cả reviewer lẫn packet đều
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

**r9 ĐỔI CÁCH KHAI — không còn một con số "hiện hành" trong đặc tả.** Lớp `spec-current-size-evidence-stale`
đã lặp BA lần (lượt 3, lượt 6, lượt 14): mỗi lần head đổi, con số đóng băng ở đây cũ đi, mà đặc tả đóng băng thì không
sửa tại chỗ được. Chữa theo cấu trúc: **tiêu chí là PHÉP ĐO tại head đang xét**, không phải con số —
`git diff --numstat $(git merge-base HEAD origin/master) HEAD` ⇒ vế TỆP ≤ 3, vế DÒNG THÊM ≤ 3000. Mọi con số
dưới đây là **LỊCH SỬ có ghi điều kiện đo**, không phải lời khai về head hiện tại.

**Phép đo LỊCH SỬ, 21-09-2026, `git diff --numstat 714f36e6 d27cba2` (base = `merge-base`, lúc đóng băng r7):**

| tệp | dòng thêm |
|---|---|
| `CLAUDE.md` | 27 |
| `ops/lease_publish.py` | 119 |
| `ops/lease_publish_test.py` | 1126 |
| **tổng** | **1272** (xoá 3) |

**Lúc ấy:** 3 tệp ⇒ vế TỆP đạt; 1272 ≤ 3000 ⇒ vế DÒNG đạt theo trần đã nới. **Lúc đóng băng r9 (25-09, head
`0093149`, merge-base `601a0f1`):** 3 tệp / **2398** dòng thêm (27 + 159 + 2212) — vẫn trong trần 3000; vượt trần GỐC
2098. Câu này cũng sẽ cũ; phép đo tại head là thứ có thẩm quyền.

**Nhưng KHÔNG được khai là "ĐẠT `ADR-0044`" trống không** — `1272 > 300`, tức vượt trần GỐC 972
dòng, và chỉ đạt nhờ một chỉ thị neo vào đợt này. Cách khai đúng: *"3 tệp / 1272 dòng thêm; vượt
trần gốc `ADR-0044` (300) **972 dòng**; đạt trần **3000** do chủ kho nới cho đợt 21-09-2026"*.

Lượt 6 bắt con số cũ (`spec-current-size-evidence-stale`, slug đã có từ lượt 3 — **lần thứ HAI**
cùng slug): r6 ghi `741/441` trong khi thực tế lúc ấy đã là `925/625`. Nay đo lại ở head
`d27cba2`. **Con số này SẼ trôi lần nữa** — mỗi lần head đổi là phải đo lại, và điều kiện hoàn
tất ở §10.3 phải đổi theo. Đó là lý do §10.3 trỏ về ĐÂY thay vì chép số.

**Lịch sử con số, vì con số trong một ngoại lệ LÀ một phần của ngoại lệ:**

| mốc | head | dòng thêm | trần lúc ấy | trạng thái |
|---|---|---|---|---|
| r2 | `44a87d0` | 333 | 300 | vượt 33, xin ngoại lệ |
| r3 | `d3d45d0` | 396 | 300 | vượt 96, ngoại lệ phải xin LẠI |
| r4 | `dea83a1` | 603 | 3000 | trong trần đã nới; vượt trần GỐC 303 |
| r5 | `d38de01` | 741 | 3000 | trong trần đã nới; vượt trần GỐC 441 |
| r6 | `94d3cd9` | 925 | 3000 | trong trần đã nới; vượt trần GỐC 625 — **r6 khai nhầm là 741** |
| r7 | `d27cba2` | 1272 | 3000 | trong trần đã nới; vượt trần GỐC 972 |
| r8 | — | KHÔNG ĐO | 3000 | r8 chỉ sửa lịch sử verdict, không đo lại kích thước — lượt 14 bắt số cũ |
| **r9** | `0093149` | **2398** | **3000** | trong trần đã nới; vượt trần GỐC **2098** |

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
| `so_do_r7` | 1272 dòng thêm, head `d27cba2` — vượt trần GỐC 972, trong trần đợt này |
| `so_do_r9` | **2398** dòng thêm, head `0093149`, merge-base `601a0f1` — **vượt trần GỐC 2098**, trong trần đợt này |
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

1. **Một lease neo ĐÚNG revision HIỆN HÀNH của đặc tả này — tức `revision` ghi ở bảng đầu tệp
   (con số ở ô `revision` của CHÍNH tệp này — r10 sửa: r8/r9 ghi "(r8: `8`)", câu ấy đã cũ ngay ở r9) và `spec_hash` của chính tệp này** — đã cấp và đã đăng. *(r8 sửa: bản r7 ghi cứng
   `revision: 7` ngay trong mục khai "CỐ Ý không ghi cứng" — giữ nguyên thì r8 tái tạo đúng
   finding `spec-current-revision-contradicts-done-condition` mà r7 sinh ra để sửa.)* **Mục này CỐ Ý không ghi cứng một con số revision
   khác**: lượt 6 bắt r6 đúng chỗ đó (`spec-current-revision-contradicts-done-condition`) — tiêu
   đề khai r6 trong khi điều kiện hoàn tất vẫn đòi lease r5, và lease `g4` neo r6 đã tồn tại và
   khớp. Một điều kiện hoàn tất trỏ vào một revision CŨ thì nó vừa sai vừa không thể đạt.

   **Phép kiểm, chạy được:** so bộ ba `(revision, spec_hash, reviewed_sha)` của TỆP NÀY với của
   lease đang hiệu lực. Lệch bất kỳ vế nào ⇒ ĐỎ. Đối chứng phải có: một lease neo revision TRƯỚC
   (ở r8: lease neo r7) phải bị BÁC khi revision hiện hành có hiệu lực — nếu không, phép kiểm
   không phân biệt được gì.

   Lịch sử để không ai đọc nhầm: `g3` neo `spec_hash` của **r2**, và reviewer lượt 3 đã ghi
   thẳng *"không dùng artifact đó để xác nhận đã cấp lease r3"*. `g4` neo **r6**, `g5` neo **r7**, `g6` neo **r8**, `g7` neo **r9**, `g8` neo **r10**, `g9` neo **r11**; lease neo r12 là `g10`.
   **Cấp lease là thẩm quyền chủ kho** — phiên #579 soạn và xin, KHÔNG tự cấp.
2. `A1`–`A23` đều có phép đo dương THEO BẢNG §5.0, `rc` đọc TRỰC TIẾP. *(r10: bảng có thẩm quyền là §5.0; §5.1 là lịch sử.)* (r3 chỉ đòi tới `A14` trong khi `t181`–
   `t183` đã tồn tại; r4 tới `A17` trong khi `t184` chưa ra đời — xem §5.)
3. Thân PR khai kích thước theo ĐÚNG câu ở **§8**, **ĐO LẠI Ở HEAD ĐANG XÉT** — mục này CỐ Ý
   không chép con số, vì chép là cách nó đã cũ BA lần. Số ở §8 lúc đóng băng r9 (LỊCH SỬ): **3 tệp /
   2398 dòng thêm; vượt trần gốc `ADR-0044` (300) 2098 dòng; đạt trần 3000 do chủ kho nới cho đợt
   này** (head `0093149`). Không khai "ĐẠT" trống không; không dùng lại `333` (r2), `396` (r3),
   `603` (r4), `741` (r5) hay `925` (head r6).
4. `human_audited`: một lượt thẩm định của NGƯỜI trên head thật. **Packet này KHÔNG LAND ĐƯỢC
   BẰNG MÁY**, và chữ ký không thay được phép đo. **SÁU** lượt cross-review máy đã chạy tới lúc
   đóng băng r7 (§11, §12) — chúng **không** cấp được `human_audited`, và verdict của chúng tự
   nói đúng điều đó.

   **Con số này ĐẾM ĐƯỢC, đừng chép:** mỗi lượt có một `reviewed_sha` riêng, nên số lượt = số
   `reviewed_sha` PHÂN BIỆT trong hồ sơ, không phải số lần chữ *"review"* xuất hiện. r6 khai
   *"Bốn lượt"* trong khi chính nó đã dẫn verdict lượt 5 — lượt 6 bắt
   (`spec-active-review-count-stale`), và nó lọt qua mọi bộ lọc chỉ-đếm-chữ-số vì con số ấy viết
   bằng CHỮ.
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

6. **ĐIỀU KIỆN DỪNG VÒNG LẶP — MỚI Ở r7, và nó là lý do r7 tồn tại.**

   Chỉ thị chủ kho 21-09-2026 (bản chiếu `issues/579#issuecomment-5765688081`):

   > *"Chuyển điều kiện dừng là tới khi không còn findings P1, P2, P3"*

   **Vòng lặp vá / cross-review dừng khi một lượt cho `0` finding ở CẢ BA mức `P1`, `P2`, `P3`.**
   Bốn điều phải khai kèm, vì chúng quyết định luật này chặt hay lỏng:

   - **Chặt hơn `cross_approved`.** Protocol cho phép một verdict `approve` kèm P3; dưới luật
     mới một verdict như thế **KHÔNG dừng**. Đây là KHẢ NĂNG, chưa từng xảy ra ở packet này: lượt
     1–6 lần lượt `blocked`, `changes_requested` ×4, `blocked` (§11, §12). *(r8 sửa: bản r7 viết
     lượt 5 và 6 "đều thế" — trái bảng lịch sử của chính tệp; xem §0.8.)*
   - **`P4` / "giới hạn đã khai" KHÔNG nằm trong điều kiện dừng**, theo đúng chữ của chỉ thị.
     Nhưng `KHÔNG ĐO ĐƯỢC` **vẫn làm cổng ĐỎ** theo doctrine ba trạng thái — nó không biến mất,
     chỉ không phải thứ được đếm ở đây.
   - **Executor KHÔNG được xin hạ mức một finding để đóng vòng lặp.** Mức nặng là phán quyết của
     reviewer. Một luật dừng đếm theo MỨC thì cám dỗ đầu tiên là đi xin hạ mức, và đó là cách
     luật này chết. Mọi lần hạ mức phải do reviewer tự làm, tự nêu lý do ĐO ĐƯỢC.
   - **`0` finding mà verdict KHÔNG phải `approve` là MÂU THUẪN phải giải, không phải điểm
     dừng.** *(Câu sau là lúc đóng băng r7.)* Lượt 6 đang ở đúng hình dạng ngược lại (`blocked` với 0 P1/P2 nhưng 9 P3).

   Điều kiện dừng **KHÔNG thay** `human_audited` ở mục 4, cũng không thay lượt CI ở mục 5. Nó là
   một điều kiện THÊM.
7. Cross-review đạt **`approve`** tường minh **VÀ** thoả điều kiện dừng ở mục 6 (`0` finding
   P1/P2/P3). Hai vế, không phải một: lượt 5 ra `changes_requested`, lượt 6 ra `blocked` với
   `0 P1 · 0 P2 · 9 P3` — tức một lượt có thể sạch P1/P2 mà vẫn còn xa điểm dừng.
   **Lời tự khai "đã sửa" KHÔNG đóng được một finding**; chỉ một lượt review mới, đo lại trên
   head mới, mới đóng được. Đúng câu §11 của chính r3: *"lời khai trung thực về một khoảng trống
   không lấp được khoảng trống ấy"*.
8. **Đột biến `L` đã được đo** — hoặc, nếu vẫn không đo được, thì nói thẳng là `KHÔNG ĐO ĐƯỢC`
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

### 12.5 — Lượt 6, và r7 là hệ quả

| trường | giá trị |
|---|---|
| reviewer | `codex`, `model_reasoning_effort=xhigh`, trục LỚP |
| `reviewed_sha` | `94d3cd94174e78f2337cb32cb7016921bf2e890b` (#589) · `9a131f2b82695367ee340dd081e7f23f4ba78407` (#592, r6) |
| `reviewed_tree` | `2e20a0c6c4543073ede55e21780d5c8739177fca` |
| verdict | **`blocked`** |
| finding | **0 P1 · 0 P2 · 9 P3** |
| đối chiếu lượt 5 | 3 slug **VÁ HỜ**, 1 **ĐÃ VÁ THẬT** |

**Vì sao `blocked` chứ không `changes_requested`** — nguyên văn reviewer: *"`blocked` vì SPEC
đóng băng còn thiếu/lệch điều kiện nghiệm thu, phải qua revision theo protocol §3.2 … Nếu chỉ
xét lỗi test thì yêu cầu là `changes_requested`."* Tức bốn finding mã vá được tại chỗ; năm
finding đặc tả thì không — chúng đòi chính tệp này.

**LƯỢT NÀY BỊ HẠ TẦNG GIẾT HAI LẦN**, và cách nó lộ ra đáng ghi: container của phiên điều phối
khởi động lại lúc ~17:18Z và ~18:11Z, giết tiến trình `codex`. `run.json` của launcher **vẫn ghi
`trang_thai: dang_chay`** ở cả hai lượt — vì launcher chết cùng lúc nên không bao giờ ghi được
bản ghi kết thúc. Phép đo thật là `kill -0 <pid>` ⇒ đã chết. Đúng lớp *"đếm sự CÓ MẶT thay vì
KHẢ NĂNG"*, lần này nạn nhân là chính cuốn sổ dựng ra để một lượt chết vẫn được ghi nhận.

**Và một bản NHÁP suýt được nâng thành verdict.** Lượt 1 để lại `evidence/canonical-draft.md`
(26 KB) có đủ `verdict:`, `reviewed_sha:`, bảng lớp `L1`–`L7`, 9 finding — đọc lướt thì đó là
kết luận. Nhưng lời nhắn cuối của chính reviewer nói *"**Bảy lượt full suite đột biến đang chạy**
tuần tự"*, tức bản nháp viết TRƯỚC khi số liệu nó dựa vào có. Nâng nó lên là cấp tín dụng cho
một phép đo chưa xảy ra. Lượt tiếp thứ ba chạy trọn (`ma_thoat=0`) mới có kết luận canonical
trong `VERDICT.md`.

**Bốn lớp mã đã đóng ở `d27cba2`, mỗi lớp một CỬA:**

| lớp | đường vào liệt kê bằng `ast` | cửa |
|---|---|---|
| `CHOT-SO-LOI-GOI-MA-KHONG-CHOT-KET-QUA` | **5** chỗ, đúng **1** hở | `_goi_dem_lop_gh`; `_do_kiem_github` BỎ HẲN vế đếm; `t186` cấm chốt đếm ngoài cửa |
| `CHAN-DOAN-MANG-CALLBACK-CUA-BEN-BI-DO` | 2 trường của `_MaVang` | `_chuoi_thuan` |
| `DO-LOP-THAY-VI-DO-DOI-TUONG` | `t184` (a) | vế (a2) + móc `truoc_khi_chay` |
| `VE-DOI-TRA-VE-MA-KHONG-BOC` | 4 vế | `_goi_doi_tra_ve` |

Bộ đột biến, TUẦN TỰ, nền `180/180`: `R_probe` · `D1` · `D2` · `D3` · `Pident` · `Pstr` · `N1`
— **cả bảy `179/180`, bảy ca/vế KHÁC NHAU, không cặp nào trùng đích**.

**`R_probe` là phép đo đắt nhất của lượt này:** trên head cũ `94d3cd9` nó **SỐNG `177/177`**.
Nó ném `ValueError` ngay đầu `_do_dau_da_dang`, chỉ với đúng năm đầu vào của vế `lease_id` sai
kiểu. Ca khi ấy bỏ giá trị trả về rồi chỉ chốt `len(gh.calls) == 0` — mà **"0 lời gọi vì tiền
kiểm chặn" và "0 lời gọi vì ngoại lệ bay ra trước mạng" là HAI trạng thái cho CÙNG một con số**.
Số đếm chỉ biết mạng chưa bị chạm; nó không biết VÌ SAO.
