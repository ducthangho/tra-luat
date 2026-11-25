tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# PX-LOC-MARKUP r1 — `proxima-control` lọc khối `<ElicitationsGroup>` khỏi câu trả lời (đặc tả)

## packet_id · packet_issue
- `packet_id`: `px-loc-markup`. Revision 1, generation 1. Role `executor` (Claude).
- `packet_issue`: #1529.

## nguon_cap_viec
- Packet #1457 (`px-gemini-500`), hồ sơ r2 `ops/acceptance/px-gemini-500/r2/RESULTS.md`: lời gọi C3 (`gemini:auto`, HTTP 200) trả `OK`
  kèm một khối `<ElicitationsGroup>` chứa gợi ý câu hỏi tiếp theo; lời gọi C2 (`gemini:3-5-flash-lite`) HTTP 500 vì luồng treo và
  không có fallback. Hồ sơ ấy mang khối đính chính (PR #1487): mọi kết luận là lời khai chưa xác minh trong kho.
- Đề xuất: https://github.com/ducthangho/tra-luat/issues/1457#issuecomment-7053599823 (mục 3.5 và mục 4).
- Chủ kho chốt Q1–Q8 trong phiên chat 25-11-2026 (*"Đồng ý hết, viết đặc tả đi"*); tiền lệ cấu trúc: `ops/specs/px-ask-r3.md` (#1446).

## review_class
`sensitive` — mã PowerShell của skill chạy trên máy chủ kho/VM, cùng lớp với tiền lệ `px-ask-r3`.

## Số đo nền (đo 25-11-2026 ~18:40Z trên `origin/master` `d0868db`)
- Câu trả lời đi qua đúng một chỗ: `Invoke-PxcAsk` (`.agents/skills/proxima-control/scripts/ProximaControl.psm1:285`), gán
  `answer` từ `choices[0].message.content` (dòng 304–306) và trả kèm `answerTrust = 'untrusted_data'`.
- Hình dạng khối (ĐÚNG MỘT mẫu, lượt C3 chủ kho dán 20-11-2026; chỉ ghi cấu trúc, không chép nội dung):
  `<ElicitationsGroup message="…">`, bên trong là các `<Elicitation label="…" query="…"/>`, đóng bằng `</ElicitationsGroup>`;
  không có dạng tự đóng của thẻ nhóm.
- `ModuleVersion` = `2.1.0`. Harness `ProximaControl.Tests.ps1`: 27 ca bắt buộc (`X1-01` … `X6-02`), counterexample `CX00`–`CX13`.
- CI không chạy harness này (`rg -l proxima .github/workflows` ⇒ 0 tệp); container phiên web không có `pwsh`.
- `ai-dang-giu` cho 4 tệp mã/tài liệu của module ⇒ `NGƯỜI_GIỮ 0` (sau khi fetch đủ ref).
- Module không có trong `RELEASE_MANIFEST.json` (`grep -c proxima-control` ⇒ 0) ⇒ không tái sinh manifest.
- Kích thước tham chiếu: tiền lệ `px-ask-r3` sửa module +50/−16 dòng trên 5 tệp (`git diff --numstat 94c425d^ 981f761`).

## write_set
- `.agents/skills/proxima-control/scripts/ProximaControl.psm1`
- `.agents/skills/proxima-control/scripts/ProximaControl.psd1`
- `.agents/skills/proxima-control/SKILL.md`
- `.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1`
- `.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1`
- `ops/specs/px-loc-markup-r1.md`
- `ops/leases/px-loc-markup-r1-g1-claude.yaml`
- `ops/acceptance/px-loc-markup/r1/RESULTS.md`

## ngoai_pham_vi
- Chặn bằng mã các model `gemini:<biến thể>` khác `auto` (Q4: module là bộ điều khiển Proxima chung; chỉ hướng dẫn trong `SKILL.md`).
- Lọc thẻ markup nào khác ngoài `ElicitationsGroup`/`Elicitation` (Q1: mới có một mẫu; không đoán "cùng họ").
- Sửa gateway Proxima (`gemini-engine.js`): phần mềm bên thứ ba, đề xuất upstream do chủ kho tự gửi.
- Đổi HTTP, timeout 300 s, nhật ký `px-active`, WhatIf, kiểm runtime, Remote, dịch vụ.
- Mọi lời gọi model thật. Kiểm thật sau merge là revision riêng (Q7).
- Đồng bộ phiên bản module trên VM (đang 1.0.1, vốn đã lệch).

## muc_tieu
1. `ProximaControl.psm1` — trong `Invoke-PxcAsk`, khi `answer` là chuỗi, bỏ mọi khối hoàn chỉnh
   `<ElicitationsGroup …>…</ElicitationsGroup>` (khớp tên thẻ Ordinal, phân biệt hoa thường; tên phải kết thúc ngay sau `ElicitationsGroup`
   bằng khoảng trắng, `>` hoặc `/`), kèm khoảng trắng/dòng trống dư mà khối để lại ở **cuối** chuỗi. Không đổi byte nào ngoài khối và
   phần khoảng trắng cuối ấy.
2. `ProximaControl.psm1` — khi có thẻ mở `<ElicitationsGroup` mà không có thẻ đóng tương ứng (cụt), hoặc thẻ lồng sai: **không** sửa
   `answer` (Q2).
3. `ProximaControl.psm1` — `data` của kết quả `ask` thêm `answerMarkup` ∈ {`none`, `removed`, `unterminated`} và
   `answerMarkupRemoved` (số nguyên ≥ 0, số khối đã bỏ). Nội dung đã bỏ **không** xuất hiện ở bất kỳ trường hay luồng đầu ra nào (Q3).
   Khi `answer` không phải chuỗi (`response_unparsed`) thì `answerMarkup` = `none`, `answerMarkupRemoved` = 0.
4. `ProximaControl.psm1` — help của `px` nêu hai trường mới.
5. `ProximaControl.psd1` — `ModuleVersion` `2.1.0` → `2.2.0` (Q5).
6. `SKILL.md` — frontmatter/mục *Phiên bản* theo 2.2.0; mô tả hai trường mới; thêm hướng dẫn: chạy tự động với Gemini thì dùng
   `gemini:auto`, vì model chỉ định không có fallback khi luồng treo (nguồn: #1457 r2) — câu này là hướng dẫn, không phải chốt mã (Q4);
   ghi hệ quả Remote (băm module đổi ⇒ handshake với endpoint bản cũ lệch), không xử lý.
7. `ProximaManifest.Tests.ps1` — `$Want`/CX tương ứng theo 2.2.0.
8. `ProximaControl.Tests.ps1` — thêm ca bắt buộc `X5-11` (27 → 28 id) và counterexample `CX14` (mục `nghiem_thu`).
9. `ops/acceptance/px-loc-markup/r1/RESULTS.md` — biên nhận chạy test trên Windows (lệnh, phiên bản PS, culture, rc, `passed/total`,
   danh sách CX `credited`).
10. `ops/specs/px-loc-markup-r1.md`, `ops/leases/px-loc-markup-r1-g1-claude.yaml` — đặc tả này và lease.

## nghiem_thu
Mỗi tiêu chí kèm phép đo làm nó ĐỎ. "Ca" = một id trong mảng `$Ids` của harness; "CX" = một counterexample.

- **N1 (mục tiêu 1–3, hành vi lọc)** — ca `X5-11` dựng phản hồi giả qua cùng cơ chế HTTP giả của các ca `ask` hiện có (không gateway
  thật) và đòi ĐÚNG giá trị, so Ordinal toàn chuỗi:
  - không khối: `answer` giữ nguyên byte, `answerMarkup` = `none`, `answerMarkupRemoved` = 0;
  - một khối sau `OK\n\n`: `answer` = `OK`, `removed`, 1;
  - hai khối (một giữa, một cuối): đúng phần văn bản ngoài hai khối, `removed`, 2;
  - khối cụt (mở không đóng): `answer` giữ nguyên byte, `unterminated`, 0;
  - `<ElicitationsGroupX …>…</ElicitationsGroupX>` và `<elicitationsgroup …>…</elicitationsgroup>`: giữ nguyên byte, `none`, 0;
  - chuỗi đánh dấu duy nhất đặt trong `label`/`query`/`message` của khối bị bỏ **không** xuất hiện trong kết quả trả về, trong mọi luồng
    (output/error/warning/verbose/debug/information) và trong bản ghi `px-active` (vế dương: cùng chuỗi đặt NGOÀI khối thì phải xuất hiện
    trong `answer` — L6a).
  ĐỎ khi: bất kỳ giá trị nào lệch; đột biến `CX14` (bên dưới) làm ca này đỏ với token có tên.
- **N2 (counterexample)** — `CX14`: bản sao module bỏ bước lọc (trả `answer` gốc) ⇒ harness chạy với `-Counterexamples` phải ghi `CX14`
  `credited` với rc 1 và token hành vi có tên trong `X5-11`. Thêm `CX15`: đổi phép so tên thẻ sang không phân biệt hoa thường ⇒ phải đỏ
  ở vế `elicitationsgroup` của `X5-11`. ĐỎ khi: mutant sống (harness báo không `credited`).
- **N3 (không hồi quy)** — 27 ca cũ vẫn đạt; `CX00`–`CX13` vẫn `credited`. ĐỎ khi: bất kỳ ca/CX cũ nào đổi màu.
- **N4 (phiên bản)** — `ProximaManifest.Tests.ps1` đạt với `2.2.0`; ĐỎ khi để `.psd1` ở `2.1.0` (đột biến tay, ghi vào RESULTS).
- **N5 (tài liệu, mục tiêu 6)** — trên `SKILL.md` đã nối dòng theo từng đoạn (L6b): vế dương — có câu hướng dẫn dùng `gemini:auto` cho
  chạy tự động **và** có tên hai trường `answerMarkup`, `answerMarkupRemoved`; vế âm — không còn chuỗi `2.1.0` ở frontmatter/mục
  *Phiên bản*. ĐỎ khi: xoá câu hướng dẫn (vế dương đỏ) hoặc để lại `2.1.0` (vế âm đỏ). Đếm theo từng vị trí (frontmatter, mục *Phiên
  bản*), không đếm gộp (L6c).
- **N6 (nền chạy)** — trên máy Windows của chủ kho (ASUS), từ clone sạch tại SHA ứng viên:
  `ProximaControl.Tests.ps1` với PS 7 và PS 5.1, mỗi bản `en-US` và `tr-TR`; `-Counterexamples` ở PS 7 `en-US`;
  `ProximaManifest.Tests.ps1` với PS 7 và PS 5.1. Đạt khi mọi lượt rc 0 và `passed == total` (hai số bằng nhau), mọi CX `credited`.
  ĐỎ khi: một lượt rc ≠ 0, `passed < total`, hay thiếu lượt nào trong ma trận. Báo cáo JSON của harness lưu ngoài cây, băm ghi vào RESULTS.
- **N7 (gate kho)** — `python3 scripts/tl.py --selftest` N/N và `git diff --check` sạch trên SHA ứng viên; `ops/lease_publish.py check`
  rc 0 cho lease. ĐỎ khi một trong ba không đạt.
- **N8 (phạm vi)** — `git diff --name-only <base>..<H>` ⊆ `write_set`. ĐỎ khi có đường dẫn ngoài danh sách.

Windows M3 (ADR-0060): `required` — diff chạm mã PowerShell chạy trên Windows; N6 là lượt Windows của packet.

## luat_dung
- Điểm dừng của `docs/PROTOCOL_DA_PHIEN.md` §12 (tín hiệu không hội tụ theo lớp; lớp/hình dạng lỗi lần thứ ba ⇒ xét lại cách làm) — dẫn,
  không chép, không hạ ngưỡng.
- Trần lời gọi Codex theo dòng khai `ADR-0055` ở đầu tệp; trần kích thước `sensitive` theo dòng khai `ADR-0053`. Chạm trần mà cần thêm
  ⇒ **E2**, mang theo mức đã dùng, còn thiếu bao nhiêu, để làm gì.
- Máy Windows của chủ kho không sẵn sàng để chạy N6 ⇒ **E2** (thiếu máy), mang theo ma trận lượt còn thiếu.
- Bằng chứng mâu thuẫn với Q1–Q8 (ví dụ mẫu thật cho thấy khối có dạng tự đóng hoặc tên khác) ⇒ **E3**, mang theo mẫu đã che, quyết
  định bị đảo, hậu quả nếu giữ.

## pham_vi_e
Không chạm E4 (không deploy, không Drive/NLM/registry, không secrets, không xoá ref/tag, không đổi ruleset) và không chạm E5. Packet
không thuộc Mission nào đã duyệt hướng ⇒ đặc tả chờ chủ kho duyệt băm trước khi cấp lease.

## hinh_dang_ke_thua
`khong_ap_dung` — không phải packet khắc phục của một lượt review. Ghi chú từ #1457 (không phải bộ đếm kế thừa): lớp
`runtime-claims-exceed-evidence` nhiều lần giữ P2 ở #1457; RESULTS của packet này chỉ được khai điều đã đo bằng harness, không suy
hành vi gateway thật.

## chua_do_duoc
- Khối `ElicitationsGroup` có biến thể nào khác mẫu duy nhất (tự đóng, lồng thẻ khác, thuộc tính khác): **KHÔNG ĐO ĐƯỢC** — chỉ có một
  mẫu, phản hồi thô của gateway không được lưu.
- Gateway có trả markup khác (ngoài thẻ này) trong câu trả lời Gemini hay không: **KHÔNG ĐO ĐƯỢC** trong phạm vi r1.
- Hành vi trên gateway thật sau khi lọc: chỉ đo được ở revision kiểm thật sau merge (Q7), cần chủ kho cấp lời gọi.
- Trạng thái đăng nhập Google của gateway lúc thi hành: không đo trong r1.
