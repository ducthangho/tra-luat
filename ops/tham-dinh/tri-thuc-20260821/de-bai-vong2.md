# VÒNG 2 — HỘI TỤ. Đề bài cho cả codex và Fable 5.

Bạn đã trả lời vòng 1. Vòng này KHÔNG lặp lại vòng 1: nhiệm vụ là **chốt MỘT thiết kế xây được trong
MỘT packet**, hoặc nói thẳng rằng không nên xây gì.

Đọc ba tệp (cùng thư mục với tệp này):
- `codex/vong1.md` — báo cáo vòng 1 của codex
- `fable/vong1.md` — báo cáo vòng 1 của Fable 5
- `DO_DOC_LAP_V1.md` — phép đo ĐỘC LẬP do phiên chính chạy SAU vòng 1

Kho CHỈ ĐỌC ở `./kho`. Mọi tệp bạn tạo phải nằm ngoài `./kho`; nếu sandbox chặn ghi thì IN NGUYÊN VĂN
báo cáo vào câu trả lời cuối (vòng 1 codex đã phải làm vậy — đó là lỗi của phiên chính, không phải của bạn).

## Những gì vòng 1 đã CHỐT (đừng tranh lại, trừ khi có phép đo mới bác được)

Hai bên ĐỘC LẬP cùng bác khung của đề bài, và cùng bác theo hướng gần nhau:
- codex: *"nút thắt là kích hoạt đúng phép kiểm tại đúng quyết định"*
- Fable: *"vấn đề không phải LƯU, không phải TRUY XUẤT, mà là DẠNG TỒN TẠI"*

Hai bên cùng TỪ CHỐI: cạnh `hinh_dang_lap >= 3` (số tự khai) · `doi_ke_hoach.can` dạng boolean ·
chỗ đựng tri thức thứ 8 · knowledge graph/vector DB · hook in hàng loạt lời nhắc.

Phiên chính đã KIỂM và CHẤP NHẬN ba chỗ codex sửa đề bài (đề bài SAI, codex ĐÚNG):
- khối "Bài học đắt giá" là **160** dòng kể tiêu đề (đề bài ghi 161)
- `verdict_usage_caveats` có ở **14/24** receipt
- `t26`/`t27` CÓ cưỡng chế máy (receipt↔verdict↔băm, nâng caveat lên mục lục) — nên câu
  "0 cổng máy đòi bất kỳ chỗ đựng nào" của đề bài là SAI. Câu đúng và hẹp hơn: **0 cổng đòi một
  BÀI HỌC phải được khai**; tính toàn vẹn receipt/verdict thì ĐÃ có cổng.

## Phép đo mới, quyết định — cả hai vòng 1 đều KHÔNG chạy nó

Chi tiết ở `DO_DOC_LAP_V1.md` §4. Tóm tắt:

- Hậu kiểm trên cây hiện tại: 18/41 lease có trích tài liệu ngoài `prompt_path`; số trích dẫn KHÔNG
  resolve được từ `origin/master` = **0**. Nhìn qua tưởng "không có bệnh".
- Đo lại tại **thời điểm cấp lease**: `ops/specs/plat-m4-v0.md` lên master lúc **03:58:21Z**, mà hai
  lease trích nó được cấp lúc **02:05Z** và **02:30Z** ⇒ lệch **−1h53m** và **−1h28m**.
- Đó đúng là ca đã làm hỏng một lượt review thật (prompt trỏ tệp không có trong cây reviewer).

Tức là: cổng "tài liệu lease trích phải resolve được từ ref bền" sẽ **ĐỎ ĐÚNG HAI LẦN NÓ CẦN ĐỎ**,
và xanh hôm nay chỉ vì lịch sử đã đuổi kịp. Nó trùng với **counterfactual số 3 của codex** ("không
resolve được `plan/spec path + hash` từ canonical ⇒ không cấp lease") và với **TOI_KY số 3 của Fable**
("chốt neo tài liệu vào ref bền, mở rộng `_kiem_neo_prompt` sẵn có").

Phép đo phụ đã chạy: mẫu `$?`-sau-pipeline hiện còn trong cây = **0** (47 dòng có pipeline kết bằng
lệnh lọc, nhưng 0 chỗ đọc `$?` ngay sau pipeline) ⇒ lint đó là **ratchet-tại-không**.
`_kiem_neo_prompt` có thật tại `ops/lease_publish.py:153`; `prompt_path` + `prompt_sha256_required`
có ở **82/82** khối lease.

## Sáu câu phải trả lời

**D1 — codex đề `evidence-preflight` (một runner ở cửa chuyển state, tự chạy `required_checks`, phát
receipt máy). Fable đề ba cổng hẹp (neo tài liệu · lint `$?` · cấm im lặng `mcr`).**
Đây là MỘT thứ ở hai độ hạt, hay hai thứ khác nhau? Nếu chỉ được xây MỘT trong hai trong một packet,
chọn cái nào, và **cái bị loại mất gì cụ thể**? Trả lời bằng phản thực trên đúng 3 ca của đề bài vòng 1.

**D2 — `evidence-preflight` của codex có ĐIỂM MÙ nào?** Tấn công nó như bạn đã tấn công đề bài vòng 1:
cách lách rẻ nhất, báo động giả tệ nhất, và chi phí ẩn. Đặc biệt: runner tự chạy check nghĩa là nó
phải BIẾT chạy check nào — danh sách ấy đến từ đâu, và ai ngăn người ta rút ngắn nó?

**D3 — `chi_la_chu: true` — Fable ký như "sản phẩm phụ là bảng kiểm kê đo được"; codex nói nó phải
được tính là NỢ, không phải bảo đảm.** Chốt: nó ghi vào đâu, ai đọc, và **phép đo nào làm nó ĐỎ**?
Nếu không có phép đo nào làm nó đỏ thì nói thẳng nó là **CHỈ LÀ CHỮ** và đừng ký.

**D4 — `plan_impact: none|packet_revision|mcr_candidate|new_mission` (codex) so với `mcr: <id> | null +
lý do` (Fable).** Hai cái này khác nhau ở đâu về thứ MÁY kiểm được? Chọn một, và nêu ca mà cái bị loại
bắt được còn cái được chọn thì không (nếu có).

**D5 — PHẠM VI. Viết write set tối thiểu** (danh sách đường dẫn) cho thứ bạn ký, đủ để mở một packet.
Kho này có ngưỡng kích thước packet theo đo lường (ADR 0044). Nếu thứ bạn ký KHÔNG lọt một packet thì
cắt nó thành các lát, và nói lát nào đi TRƯỚC.

**D6 — Câu hỏi ngược. `DO_DOC_LAP_V1.md` §5 khai: bốn lượt review trong ba ngày bị hỏng vì cách PHIÊN
CHÍNH dựng sandbox/bundle — cùng một hình dạng, lần thứ tư.** Theo luật của kho ("cùng hình dạng ≥3 lần
⇒ hỏi có nên làm việc này không, đừng hỏi vá thế nào"): việc dựng sandbox reviewer bằng tay có nên
BỊ CẤM và thay bằng script không, và nếu có thì **script ấy phải cưỡng chế cái gì** để lần thứ năm
không xảy ra? Đây có phải thứ đáng đi TRƯỚC mọi cạnh ở D1 không?

## Định dạng đầu ra
`D1`..`D6`, rồi `TOI_KY` (mỗi mục ghi rõ **CƯỠNG CHẾ MÁY** hay **CHỈ LÀ CHỮ**), rồi `TOI_KHONG_KY`,
rồi `KHONG_DO_DUOC`. Mỗi khẳng định gắn nhãn `ĐO ĐƯỢC` / `ĐỌC ĐƯỢC` / `SUY LUẬN`.
Ngắn và dứt khoát. Vòng này quý sự HỘI TỤ hơn sự sắc bén: nếu bạn đổi ý so với vòng 1, nói thẳng
là đổi ý và vì sao.
