# Đặc tả packet — QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG (revision 2)

- `packet_id`: **QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG**; ID bền `wp<packet_issue>`.
- `packet_issue`: **(để trống — chủ kho cấp)**
- `mission_issue`: **(để trống — chủ kho cấp)**
- `revision`: **2** · `generation`: 1 · soạn **08:1xZ 12-09-2026**
- `thay_the_cho`: **revision 1** (12:0xZ 11-09-2026) — r1 CHƯA từng được cấp packet hay lease, nên đây
  không phải sửa hợp đồng đang chạy; r1 giữ nguyên trên đĩa làm hồ sơ.
- `depends_on`: **`[wp<TRAN-VONG-REVIEW-LEN-BON r2>]`** — skill TRỎ trần, nên ADR trần phải land trước.
- `executor`: claude · `environment`: cloud
- `risk`: **sensitive** · `review_class`: **sensitive** (skill là hợp đồng hành vi của mọi phiên)

## `nguon_cap_viec`

Chỉ thị chủ kho **11-09-2026**, ba phần: lặp vá/cross-review/đăng verdict tới khi hết P1+P2 hoặc
approve · điều kiện dừng phân biệt theo tình huống · **vá theo LỚP lỗi, không theo từng lỗi**.

Chỉ thị chủ kho **12-09-2026** thêm **hai phần nữa**, và đây là lý do r2 tồn tại:

> *"ở bước mà dự đoán là còn 1 bước nữa là approve, kiểm tra head drift, nếu có thì merge trước khi bắt
> đầu vòng mới. khi đã quyết định merge thì sau khi merge xong kể cả head có đổi cũng chỉ cần chạy CI
> hậu merge là xong, không bắt cross-review merge lại trừ phi phát hiện lỗi"*

cùng *"không CI, full CI cho tới khi merge"* và *"trần nâng lên thành 10 vòng"*.

## ĐO ĐƯỢC 12-09-2026 — hai quy định mới KHÔNG có ở đâu cả, và skill đang nói NGƯỢC một cái

| quy định | ghi ở đâu | trạng thái |
|---|---|---|
| lặp tới khi hết P1+P2 hoặc approve | r1 dòng 13 | có, chờ lease |
| phân theo LỚP lỗi | r1 `M3` | có, chờ lease |
| **kiểm head drift trước vòng dự đoán là cuối, có drift thì MERGE rồi mới mở vòng** | **0 dòng** trong cả bốn đặc tả `ops/specs/*` mới; `PROTOCOL §5.1` nói chuyện KHÁC (*ngoại lệ master drift — merge thẳng, không chạy lại gate*) | **CHƯA CÓ** |
| **sau khi quyết merge: head đổi cũng chỉ chạy CI hậu merge, không bắt cross-review lại trừ khi phát hiện lỗi** | **0 dòng** | **CHƯA CÓ** |
| không chi CI tay tới khi merge | r1 `M7` (b)/(c) nói *"đúng `N` lượt, `N` đóng băng"* và *"CI thăm dò CẤM"* | **PHÁT BIỂU KHÁC** — cần hoà |

Và một mâu thuẫn SỐNG, đo tại `3c7df6d`: `.claude/skills/cross-review/SKILL.md:113` viết nguyên văn

> `Verdict neo reviewed_sha; head đổi thì làm lại, đừng review bản đã cũ.`

Câu ấy đúng cho head đổi vì **tác giả đẩy commit mới**, và NGƯỢC hướng cho head đổi vì **base trôi**:
quy định mới là merge base rồi mở vòng trên head sau merge, không phải "làm lại vòng cũ". Ai đọc skill
hôm nay sẽ làm trái chỉ thị mà vẫn đúng tài liệu — đúng hình dạng *"adapter lệch protocol thì ADAPTER
sai"*, chỉ khác là ở đây adapter lệch **chỉ thị chưa được ghi**.

**Số biện hộ cho quy định drift, đo trên `#512`:** hai lượt `thu-hoi` ĐỎ liên tiếp
(`f5bda2b`, `59a0ed4`) với cùng một chẩn đoán `CHAN [12]: KHÔNG_XÁC_ĐỊNH: S 3c7df6d678e1 không phải tổ
tiên của H …`, vì `master` trôi `a153c94` → `3c7df6d` giữa lúc nhánh còn neo base cũ. Merge master
xong ⇒ `thu-hoi` **success** trên `e6feddb`. Chốt drift bắt đúng thứ nó sinh ra để bắt, chỉ muộn **hai
lượt CI** vì nó chưa được ghi thành nghĩa vụ.

## `review_class` và ngưỡng

`sensitive` ⇒ `ADR-0044`: **≤ 3 tệp, ≤ 300 dòng thêm**. Packet này **2 tệp**.

## `write_set`

| # | đường dẫn | vì sao |
|---|---|---|
| 1 | `.claude/skills/cross-review/SKILL.md` | bên SINH ra bảng phân hạng và verdict; cũng là nơi có câu dòng 113 phải sửa |
| 2 | `.claude/skills/work-packet/SKILL.md` | bên ĐỌC bảng ấy và quyết vá tiếp, merge, hay dừng |

Không ký tự đại diện. **KHÔNG** đụng `docs/PROTOCOL_DA_PHIEN.md` — skill là **adapter MỎNG**;
`doctrine-scan` thoát khác 0 khi adapter **chép** doctrine. Skill phải **TRỎ** `§12`/`ADR-0037`/ADR trần
vòng, không chép luật. **KHÔNG** đụng `.claude/hooks/**` (packet `CONG-CHAN-CHI-CI-SOM`).
**KHÔNG** đụng r1 của chính đặc tả này.

## `ngoai_pham_vi`

1. **KHÔNG chép con số trần vòng vào skill** — trỏ ADR. Chép số là tái tạo đúng bệnh `ADR-0043` sinh ra
   để chữa.
2. **KHÔNG viết cổng cưỡng chế** — skill là chữ. Cưỡng chế chi CI ở packet riêng; `so-canon` là nợ.
   Khai thẳng điều này **trong chính skill**, kẻo người đọc tưởng đã có cơ chế.
3. **KHÔNG đổi định nghĩa P1/P2/P3** — đang dùng được; đổi là làm các lượt verdict cũ không so được.
4. **KHÔNG tự quyết thay chủ kho** khi vào Rescue Checkpoint; skill chỉ buộc **DỪNG và hỏi**.
5. **KHÔNG biến quy định hậu-merge thành "khỏi cần CI"** — nó nói chỉ cần **CI hậu merge**, không nói
   khỏi CI. Viết yếu đi là mở đường merge rồi không ai đo gì.

## `muc_tieu`

M1–M7 **giữ nguyên từ r1** (điều kiện dừng theo `review_class`; `sensitive` phải `approve`; BẢNG LỚP;
lớp lần thứ ba cấm vá lẻ; không hội tụ đo bằng PHÂN HẠNG; chống lách thu hẹp phạm vi; ba loại chi CI).
R2 thêm ba mục:

| # | mục tiêu | chiếu vào |
|---|---|---|
| M8 | **KIỂM DRIFT TRƯỚC VÒNG DỰ ĐOÁN LÀ CUỐI.** Trước khi phóng một vòng mà phiên dự đoán sẽ ra `approve`, phải đo `base` của PR so nhánh mặc định; **có drift ⇒ merge nhánh mặc định vào nhánh packet TRƯỚC khi phóng**, và verdict neo head SAU merge. Kèm sửa câu dòng 113: phân biệt **head đổi vì tác giả đẩy** (làm lại) với **head đổi vì base trôi** (merge rồi phóng trên head mới). | #1, #2 |
| M9 | **SAU KHI QUYẾT MERGE.** Khi đã quyết merge trên một head đã approve: head đổi tiếp **không** kéo theo một vòng cross-review mới; nghĩa vụ còn lại là **CI hậu merge**. Ngoại lệ duy nhất: **phát hiện lỗi** — lúc ấy mở vòng mới và khai lý do. | #2 |
| M10 | **CHI CI TRONG VÒNG LẶP = 0 TRƯỚC MERGE.** Hoà với `M7`: trong lúc lặp vá-review, `N` của loại (b) là **0** — chỉ nhận CI gác cổng do GitHub tự bắn theo push/PR. Gọi tay `workflow_dispatch`, lane `windows`, hay full CI trước merge là loại (c) **CẤM**. Lượt CI hậu merge của `M9` là loại (a), không tính vào `N`. | #2 |

## `nghiem_thu`

A1–A9 **giữ nguyên từ r1**. R2 thêm bốn ca, mỗi ca có **phép làm ĐỎ**:

**A10 (M8) — quy định drift có mặt VÀ phân biệt được hai nguyên nhân head đổi.**
`cross-review/SKILL.md` phải nêu: trước vòng dự đoán là cuối thì đo drift; có drift thì merge trước.
Và phải phân biệt tường minh **hai** nguyên nhân head đổi, với hành động KHÁC nhau.
**Phép làm ĐỎ:** giữ nguyên câu dòng 113 mà không phân biệt ⇒ ĐỎ · viết *"nên kiểm drift"* thay vì
**phải** ⇒ ĐỎ. Phép đo: đòi văn bản chứa cả hai nhánh hành động và một câu điều kiện gắn với *"vòng dự
đoán là cuối"*; một câu chung chung *"kiểm drift khi cần"* KHÔNG đạt.

**A11 (M9) — quy định hậu-merge nói ĐỦ và không nói QUÁ.**
Skill phải nêu ba mệnh đề tách rời: (i) head đổi sau khi quyết merge **không** đòi vòng review mới;
(ii) vẫn **phải** có CI hậu merge; (iii) phát hiện lỗi thì mở vòng mới.
**Phép làm ĐỎ:** bỏ (ii) ⇒ thành *"merge rồi khỏi đo"* ⇒ ĐỎ · bỏ (iii) ⇒ thành *"merge rồi không review
nữa bất kể gì"* ⇒ ĐỎ. Ba mệnh đề phải đếm được, không gộp thành một câu mơ hồ.

**A12 (M10) — `N = 0` trước merge, và nó KHÁC `M7` bản r1.**
Bảng ba loại chi CI của `M7` phải mang thêm cột hoặc câu nói `N = 0` cho giai đoạn TRƯỚC merge, và xếp
`workflow_dispatch`/lane `windows` gọi tay trước merge vào loại **(c) CẤM**.
**Phép làm ĐỎ:** để `N` mở ("đóng băng trong spec") mà không nói giai đoạn trước merge là 0 ⇒ một phiên
vẫn tự cấp cho mình vài lượt full CI mà vẫn đúng chữ ⇒ ĐỎ.
**Ca đối chiếu bắt buộc:** áp luật lên `#512` — phiên ấy đã **không** gọi `workflow_dispatch` nào trong
ba vòng cuối và chỉ nhận lượt tự động; luật mới phải cho ra *"đạt"* trên chuỗi ấy. Nếu luật mới làm một
chuỗi đã tuân thủ thành *"vi phạm"* thì luật viết sai ⇒ ĐỎ.

**A13 — hai quy định mới phải TRỎ, không CHÉP.**
`doctrine-scan` ⇒ `rc=0` sau khi thêm M8/M9/M10. Câu về trần vòng vẫn **trỏ** ADR.
**Phép làm ĐỎ:** chép `§5.1` hay con số trần vào skill ⇒ ĐỎ.

**Điều kiện dừng của CHÍNH packet này:** `sensitive` ⇒ đòi cross-review **`approve`** tường minh, và
packet này phải là packet đầu tiên tuân **chính** quy trình nó khai — gồm M8 và M10.

## `chua_do_duoc`

1. **Không cổng nào canh M8/M9/M10** — chúng là **kỷ luật đọc**, y như M1–M7. `§20` ghi `ADR-0037` và
   ADR trần vòng là **`0 cổng`**; cưỡng chế chi CI nằm ở packet `CONG-CHAN-CHI-CI-SOM`. Skill phải khai
   thẳng điều này (A8 của r1).
2. **"Dự đoán là còn một bước nữa tới approve" không đo được** — nó là phán đoán của phiên. M8 vì thế
   là nghĩa vụ **có điều kiện mềm**; cách đóng nó lại đo được là bắt đo drift ở MỌI vòng, nhưng thế thì
   tốn một `fetch` mỗi vòng và chưa ai đo chi phí ấy. Ghi thành nợ: `DIEU-KIEN-VONG-CUOI-KHONG-DO-DUOC`.
3. **Không đo được "phát hiện lỗi" ở M9 là lỗi mức nào** — cố ý để mở, vì hạ nó thành P1/P2 sẽ khiến
   một lỗi P3 rõ ràng bị bỏ qua sau merge. Reviewer và phiên land tự khai lý do.
