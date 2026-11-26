tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# PX-LOC-MARKUP r4 — `proxima-control` lọc khối `<ElicitationsGroup>` khỏi câu trả lời (đặc tả, thay r3)

## packet_id · packet_issue
- `packet_id`: `px-loc-markup`. Revision 4, generation 1. Role `executor` (Claude).
- `packet_issue`: #1529.

## nguon_cap_viec
- Đặc tả r3 `ops/specs/px-loc-markup-r3.md` (sha256 `ebf6f2779f0759a9a3168037f9877e4546a027c752e10ef006e9934e47c1adda`, duyệt
  `issuecomment-7174094220`), chưa land. r2: `5584a9f1…`; r1: `631a8beb…` (commit `b01f3dd`).
- Review offline §8.3 lượt 5 trên ứng viên r3 `d0edb21`: 1/3 (`issuecomment-7174610534`). Chuyển tiếp L4→L5 lại dưới 50% ⇒ §12 dừng
  lần thứ hai (mục sổ `7174610982`); lớp `markup-leak-test-loses-evidence` xuất hiện lượt thứ năm ⇒ E1.
- Chủ kho chọn A (đặc tả r4 thu hẹp phạm vi theo đề xuất của phiên): `issuecomment-7180137523`.
- Gốc việc #1457 r2, đề xuất `issuecomment-7053599823`; Q1–Q8 chủ kho chốt 25-11-2026; tiền lệ cấu trúc `ops/specs/px-ask-r3.md`.

## r4 đổi gì so với r3 (gốc rễ: harness cố chứng minh một mệnh đề "không rò rỉ")
1. **N1 chỉ còn đo CHỨC NĂNG của bộ lọc.** r1–r3 đều bắt harness chứng minh nội dung đã bỏ không xuất hiện ở đâu khác; năm lượt review
   liên tiếp tìm ra một bề mặt mới (luồng, khoá, kiểu, thuộc tính mở rộng, ETS, journal, metadata). Đó là một danh sách cấm, không bao giờ
   đủ. r4 bỏ cam kết ấy khỏi harness: `X5-11` khẳng định `answer`, `answerMarkup`, `answerMarkupRemoved`, `reportedModel` và byte của
   journal. Việc mã giao có đưa nội dung đã bỏ ra nơi khác hay không là việc của **review mã** (đọc diff `ProximaControl.psm1`), có tiêu chí
   ở mục N9. Lớp `markup-leak-test-loses-evidence` vì thế đóng theo PHẠM VI: reviewer không báo lại nó như lỗi của harness.
2. **`reportedModel` = `$null` (gán tường minh) mỗi khi `answerMarkup` = `removed`**, bất kể danh sách quảng bá. Ngoài ca ấy, luật r3 giữ
   nguyên: chỉ trả khi là chuỗi bằng (Ordinal) một id mà chính lời gọi nhận từ `GET /v1/models`, ngược lại `$null` **gán tường minh**.
   Đóng F8c (id quảng bá trùng nội dung đã bỏ) và F9 (giá trị không phát ra thành `PSCustomObject` rỗng qua CLIXML).
3. **F10:** phản hồi mặc định của HTTP giả (`$DefaultHttp`) giữ nguyên byte so với nền; phản hồi riêng chỉ đặt trong ca cần nó.
4. **F11:** `CX00` (đối chứng không đột biến) đạt khi báo `CONTROL_PASSED`; `CX01`–`CX16` đạt khi `credited`.
5. Write set đổi đặc tả/lease/RESULTS sang r4.

## review_class
`sensitive` — mã PowerShell của skill chạy trên máy chủ kho/VM, cùng lớp với tiền lệ `px-ask-r3`.

## nang_tran
```yaml
nang_tran:
  ai_nang: ducthangho (chủ kho, thẩm quyền §2 protocol; quyết định ghi hộ issuecomment-7172063543)
  can_cu: >-
    git diff --numstat d0868db..8776803 (đo ~19:2xZ 25-11-2026): 8 tệp, 329 dòng thêm. Phần mã đúng 5 tệp của module
    (SKILL.md, ProximaControl.psm1, ProximaControl.psd1, ProximaControl.Tests.ps1, ProximaManifest.Tests.ps1, cộng 116 dòng);
    3 tệp còn lại là sổ sách bắt buộc của packet (đặc tả, lease, RESULTS). Tách mã ra nhiều packet sẽ tách hành vi khỏi ca test và
    khỏi phiên bản của nó; bỏ RESULTS khỏi kho vẫn còn 7 tệp.
  tran_cu: 6 tệp / 450 dòng thêm (ADR-0053)
  tran_moi: 8 tệp / 450 dòng thêm
```
Giữ nguyên quyết định nâng trần của r2 (`issuecomment-7172063543`); r4 không đổi số tệp (đặc tả/lease/RESULTS r4 thay bản r3 trên nhánh).
Đo ứng viên r3 cuối `d0edb21` (01:5xZ 26-11-2026): 8 tệp, 432 dòng thêm.

## Số đo nền (đo 25-11-2026 ~18:40Z trên `origin/master` `d0868db`; đo lại 26-11-2026 01:5xZ: `origin/master` = `a89c83a`, không commit
nào chạm module kể từ `base_sha` của r3)
- Câu trả lời đi qua đúng một chỗ: `Invoke-PxcAsk` (`.agents/skills/proxima-control/scripts/ProximaControl.psm1`), gán `answer` từ
  `choices[0].message.content` và trả kèm `answerTrust = 'untrusted_data'`.
- Hình dạng khối (ĐÚNG MỘT mẫu, lượt C3 chủ kho dán 20-11-2026; chỉ ghi cấu trúc): `<ElicitationsGroup message="…">`, bên trong các
  `<Elicitation label="…" query="…"/>`, đóng bằng `</ElicitationsGroup>`; không có dạng tự đóng của thẻ nhóm.
- Nền: `ModuleVersion` = `2.1.0`. Harness `ProximaControl.Tests.ps1`: 27 ca bắt buộc, counterexample `CX00`–`CX13`.
- CI không chạy harness này; container phiên web không có `pwsh` sẵn.
- Module không có trong `RELEASE_MANIFEST.json` ⇒ không tái sinh manifest.

## write_set
- `.agents/skills/proxima-control/scripts/ProximaControl.psm1`
- `.agents/skills/proxima-control/scripts/ProximaControl.psd1`
- `.agents/skills/proxima-control/SKILL.md`
- `.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1`
- `.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1`
- `ops/specs/px-loc-markup-r4.md`
- `ops/leases/px-loc-markup-r4-g1-claude.yaml`
- `ops/acceptance/px-loc-markup/r4/RESULTS.md`

Đặc tả, lease và RESULTS của r1–r3 không có trong diff cuối của nhánh (gỡ khỏi nhánh trước push); bản cũ tra được qua commit và các
comment trên #1529.

## ngoai_pham_vi
- Chặn bằng mã các model `gemini:<biến thể>` khác `auto` (Q4: chỉ hướng dẫn trong `SKILL.md`).
- Lọc thẻ markup nào khác ngoài `ElicitationsGroup`/`Elicitation` (Q1), kể cả dạng tự đóng của thẻ nhóm (chưa quan sát; coi là thẻ hỏng).
- **Harness chứng minh "không rò rỉ"**: khẳng định rằng nội dung đã bỏ không xuất hiện ở luồng, khoá, kiểu, thuộc tính mở rộng, tệp hay
  biến nào khác. Thuộc review mã (N9).
- Sửa gateway Proxima. Đổi HTTP, timeout 300 s, nhật ký `px-active`, WhatIf, kiểm runtime, Remote, dịch vụ.
- Mọi lời gọi model thật; kiểm thật sau merge là revision riêng (Q7). Đồng bộ phiên bản module trên VM.

## muc_tieu
1. `ProximaControl.psm1` — trong `Invoke-PxcAsk`, khi `answer` là chuỗi, bỏ mọi khối hoàn chỉnh. Một khối hoàn chỉnh khi:
   - thẻ mở bắt đầu bằng `<ElicitationsGroup` (Ordinal), tên kết thúc ngay sau đó bằng khoảng trắng, `>`, `/` hoặc hết chuỗi;
   - thẻ mở kết thúc bằng `>` nằm ngoài dấu nháy kép, không gặp `<` ngoài dấu nháy trước đó, và ký tự trước `>` không phải `/`;
   - thẻ đóng `</ElicitationsGroup>` (Ordinal) đầu tiên sau `>` ấy đến trước bất kỳ thẻ mở `<ElicitationsGroup` nào khác.
   Khoảng trắng cuối chuỗi chỉ được cắt khi sau khối cuối cùng không còn gì ngoài khoảng trắng; khi ấy cắt mọi khoảng trắng ở cuối phần
   văn bản còn lại. Không đổi byte nào khác.
2. `ProximaControl.psm1` — gặp bất kỳ thẻ mở nào không thoả mục 1 (cụt, thiếu `>`, dấu nháy chưa đóng, tự đóng, thiếu thẻ đóng, lồng):
   **không** sửa `answer` chút nào, kể cả các khối hợp lệ đứng trước nó (Q2).
3. `ProximaControl.psm1` — `data` của kết quả `ask` thêm `answerMarkup` ∈ {`none`, `removed`, `unterminated`} và `answerMarkupRemoved`
   (`[int]` ≥ 0); `answer` không phải chuỗi ⇒ `none`, 0. `reportedModel`:
   - `answerMarkup` = `removed` ⇒ `$null`;
   - ngược lại, giá trị `model` của phản hồi **chỉ khi** nó là chuỗi bằng (Ordinal) một id trong danh sách `GET /v1/models` mà chính lời
     gọi `ask` ấy đã nhận; ngược lại `$null`.
   Mọi nhánh `$null` là gán tường minh (giữ `$null` qua tuần tự hoá CLIXML của đường Remote).
4. `ProximaControl.psm1` — help của `px` nêu hai trường mới.
5. `ProximaControl.psd1` — `ModuleVersion` `2.1.0` → `2.2.0` (Q5).
6. `SKILL.md` — phiên bản 2.2.0; mô tả hai trường, luật cắt đuôi và luật `reportedModel` của mục 3; hướng dẫn chạy tự động với Gemini thì
   nên dùng `gemini:auto`, nêu căn cứ đúng mức: #1457 r2 là lời khai chưa xác minh, kể một lời gọi model chỉ định HTTP 500 vì luồng treo và
   một lời gọi `gemini:auto` trả được câu trả lời; không khẳng định cơ chế gateway hay nguồn gốc khối như sự thật đã đo; ghi hệ quả
   handshake Remote.
7. `ProximaManifest.Tests.ps1` — `$Want` và `CX04` theo 2.2.0.
8. `ProximaControl.Tests.ps1` — ca bắt buộc `X5-11` (27 → 28 id), `CX14`, `CX15`, `CX16`; đổi kỳ vọng `reportedModel` của `X5-01`, `X6-01`
   (mục N3); thêm móc `Chat` cho HTTP giả (mục N3).
9. `ops/acceptance/px-loc-markup/r4/RESULTS.md` — biên nhận phép đo và chạy test Windows.
10. `ops/specs/px-loc-markup-r4.md`, `ops/leases/px-loc-markup-r4-g1-claude.yaml` — đặc tả này và lease.

## nghiem_thu
"Ca" = một id trong `$Ids` của harness; "CX" = một counterexample.

- **N1 (mục tiêu 1–3; chức năng)** — `X5-11` dựng phản hồi giả qua móc `Chat` của HTTP giả (không gateway thật), gọi `px ask` ở chế độ
  Local, với các ca: không khối; một khối ở cuối (`OK`); hai khối (giữa và cuối); khối giữa câu, đuôi space + CRLF (giữ nguyên); khối giữa
  câu, đuôi NBSP (giữ nguyên); thẻ mở không có thẻ đóng; khối lồng; thẻ mở thiếu `>`; dấu nháy chưa đóng; thẻ nhóm tự đóng; tên
  `ElicitationsGroupX`; tên viết thường; văn bản giữ lại có marker riêng; khối bị bỏ trong khi `model` của phản hồi là id được quảng bá;
  khối bị bỏ trong khi `model` bằng một id được quảng bá trùng nhãn của khối; `model` không được quảng bá, không có khối; `model` là id
  được quảng bá, không có khối. Với mỗi ca, kết quả `ok` và:
  - `answer` là `[string]` và bằng kỳ vọng (Ordinal);
  - `answerMarkup` là `[string]` và bằng kỳ vọng; `answerMarkupRemoved` là `[int]` và bằng kỳ vọng;
  - `reportedModel`: ca kỳ vọng `$null` thì đúng `$null` (`$null -eq`); ca kỳ vọng chuỗi thì `[string]` bằng kỳ vọng (Ordinal);
  - **journal:** sau khi dọn journal của ca, bản ghi của `recordId` tồn tại và **byte** của nó bằng đúng byte dựng từ năm trường đã biết
    (`schema`, `action`, `targetFingerprint`, `requestedModel`, `state`), UTF-8 không BOM, không parse JSON để so.
  ĐỎ khi một trong các khẳng định trên sai; `CX14`/`CX15`/`CX16` (N2) làm ca đỏ với token có tên.
  N1 **không** khẳng định tập khoá, số đối tượng trên luồng, thuộc tính mở rộng hay vắng mặt của nội dung đã bỏ ở bề mặt khác — xem
  `ngoai_pham_vi` và N9. Review không báo việc thiếu các khẳng định ấy là lỗi của harness.
- **N2** — `CX14` (bỏ bước lọc) `credited` với token `X5-11:MARKUP_ANSWER[one block]`; `CX15` (so tên thẻ `OrdinalIgnoreCase`) với
  `X5-11:MARKUP_STATE[case variant]`; `CX16` (bỏ nhánh `removed` ⇒ `$null` của `reportedModel`) với token `MARKUP_REPORTED_MODEL` của
  ca "khối bị bỏ, `model` trùng nhãn". ĐỎ khi một mutant sống.
- **N3** — 27 ca cũ vẫn đạt; `CX01`–`CX13` vẫn `credited`. Diff của harness so với nền chỉ được:
  - thêm khoá `Chat` (rỗng mặc định) vào trạng thái HTTP giả và vào `Reset-T`; nhánh `POST /v1/chat/completions` của `$DefaultHttp` trả
    `Chat` khi khác rỗng, còn khi rỗng trả **đúng chuỗi body của nền** (so byte);
  - đổi kỳ vọng `reportedModel` của `X5-01` và `X6-01` thành một id được quảng bá trong chính ca ấy, kèm dữ liệu phản hồi riêng của hai ca
    đó (qua `Chat` hoặc route của wire server trong ca) để gateway giả trả id ấy;
  - thêm `X5-11`, `CX14`–`CX16`, id và chú thích đầu tệp tương ứng.
  Mọi thay đổi khác ở ca cũ hay ở dữ liệu giả dùng chung là vi phạm N3. ĐỎ khi một ca/CX cũ đổi màu, hoặc diff vượt danh sách trên.
- **N4** — `ProximaManifest.Tests.ps1` đạt với `2.2.0`; ĐỎ khi để `.psd1` ở `2.1.0` (đột biến tay, ghi vào RESULTS).
- **N5 (mục tiêu 6)** — trên `SKILL.md` nối dòng theo từng đoạn: vế dương — có câu hướng dẫn dùng `gemini:auto` khi chạy tự động, có
  cụm "lời khai chưa xác minh" trong cùng đoạn ấy, có tên `answerMarkup` và `answerMarkupRemoved`; vế âm — không còn `2.1.0` ở frontmatter
  và ở mục *Phiên bản* (đếm từng vị trí). ĐỎ khi xoá câu hướng dẫn, xoá cụm lời khai, hay để lại `2.1.0`.
- **N6 (nền chạy) và M3 (ADR-0060)** — trên một máy Windows của chủ kho, dựng trong một lệnh hai cây: nền B (`base_sha` của lease r4) và
  ứng viên H (head của PR lúc chạy). **Mỗi vế chạy harness của chính cây ấy** (chép ra ngoài cây): `ProximaControl.Tests.ps1` với PS 7 và
  PS 5.1, mỗi bản `en-US` và `tr-TR`, `-Counterexamples` ở PS 7 `en-US`; `ProximaManifest.Tests.ps1` với PS 7 và PS 5.1. Báo cáo JSON
  lưu ngoài cây, băm ghi vào RESULTS.
  Đạt khi: (N6) mọi lượt của H rc 0, `passed == total`; `CX00` của H báo `CONTROL_PASSED` và mọi `CX01`–`CX16` của H `credited`;
  (M3a) đủ lượt ở cả hai vế, không lỗi setup, không ca bắt buộc `skipped`/`not_run`/`NOT_EXECUTED` ở vế nào; (M3b) tập id đỏ của H ⊆ tập
  id đỏ của B — với H 0 đỏ theo N6 thì điều này đúng trên toàn tập; (M3c) H có ca đỏ thuộc write set thì chủ kho quyết. Id chỉ H có
  (`X5-11`, `CX14`–`CX16`) xét theo N6. ĐỎ khi thiếu lượt nào hoặc một điều kiện trên sai.
- **N7 (gate kho)** — `python3 scripts/tl.py --selftest` N/N, `git diff --check` sạch, `ops/lease_publish.py check` rc 0 cho lease r4.
- **N8 (phạm vi và trần)** — `git diff --name-only <base>..<H>` ⊆ `write_set` và `git diff --numstat` ≤ 8 tệp / ≤ 450 dòng thêm
  (`tran_moi`). ĐỎ khi có đường dẫn ngoài danh sách hoặc vượt `tran_moi`.
- **N9 (review mã, không phải harness)** — reviewer đọc diff `ProximaControl.psm1` và báo nếu mã giao đưa nội dung đã bỏ (khối, nhãn,
  query, message) vào bất kỳ đâu ngoài biến cục bộ của `Invoke-PxcAsk`/`Remove-PxcElicitation`: kết quả, luồng, tệp, biến script/global,
  thuộc tính mở rộng, request. Tiêu chí là ĐỌC MÃ GIAO; đột biến cố ý chuyển dữ liệu ra ngoài không phải finding của harness.

Windows M3 (ADR-0060): `required`; N6 là lượt Windows của packet.

## luat_dung
- Điểm dừng của `docs/PROTOCOL_DA_PHIEN.md` §12 — dẫn, không chép. Lịch sử lớp ở `hinh_dang_ke_thua`; r4 KHÔNG reset bộ đếm.
- Trần lời gọi Codex theo dòng khai `ADR-0055`; đã dùng 5 (offline lượt 1–5). Chạm trần mà cần thêm ⇒ **E2**.
- Trần kích thước theo `nang_tran`; vượt `tran_moi` ⇒ **E2**.
- Máy Windows của chủ kho không sẵn sàng cho N6 ⇒ **E2**, mang theo ma trận lượt còn thiếu.
- Mẫu thật mâu thuẫn Q1–Q8 ⇒ **E3**, mang theo mẫu đã che.
- Lease r4 chỉ cấp khi `ai-dang-giu` ra 0 cho cả write set r4 (lease r3 `px-loc-markup-r3-g1-claude`, chưa push, hết hạn
  2026-11-26T00:47:27Z). Không bia mộ.

## pham_vi_e
Không chạm E4, không chạm E5. Packet không thuộc Mission đã duyệt hướng ⇒ đặc tả chờ chủ kho duyệt băm trước khi cấp lease.

## hinh_dang_ke_thua
Số lượt review mà mỗi lớp xuất hiện (L1 `8a33ddb`, L2 `c4e9711`, L3 `86fc431`, L4 `8060930`, L5 `d0edb21`):
- `markup-leak-test-loses-evidence`: **5** (L1–L5), VÁ MỘT PHẦN ở L5 — r4 đóng theo phạm vi (mục *r4 đổi gì* 1, N1, N9). Lượt review
  đầu của r4 gắn nhãn cho lớp này theo N1 r4; xuất hiện lại dưới dạng lỗi CHỨC NĂNG của bộ lọc thì vẫn tính lần thứ sáu.
- `markup-echo-in-reported-model`: **3** (L3–L5), VÁ MỘT PHẦN — r4 đổi luật (mục tiêu 3).
- `reported-model-null-lost-in-remoting` (F9): **1** (L5) — r4 gán `$null` tường minh.
- `shared-chat-fixture-changes-old-cases` (F10): **1** (L5) — r4 N3.
- `cx00-credit-receipt-mismatch` (F11, P3): **1** (L5) — r4 N6.
- Đã đóng: `windows-m3-baseline-omitted` (3, L2–L4, ĐÃ VÁ THẬT ở L5), `markup-trims-unrelated-tail` (1), `markup-pairs-incomplete-opener`
  (1), `runtime-claims-exceed-evidence` (1), `sensitive-diff-exceeds-file-cap` (1), `lease-expiry-prerequisite-stale` (1).
Tỷ lệ §12 theo chuyển tiếp: L1→L2 4/5, L2→L3 1/3, L3→L4 0/3, L4→L5 1/3. Lượt review đầu của r4 là chuyển tiếp L5→L6; dưới 50% thì
§12 dừng lần ba và phiên dừng packet, báo chủ kho (không đề xuất r5 cùng hình dạng).

## chua_do_duoc
- Biến thể khác của khối `ElicitationsGroup`: **KHÔNG ĐO ĐƯỢC** — một mẫu, phản hồi thô của gateway không được lưu.
- Markup khác trong câu trả lời Gemini: **KHÔNG ĐO ĐƯỢC** trong r4.
- Hành vi trên gateway thật sau khi lọc: chỉ đo ở revision kiểm thật sau merge (Q7).
- Trạng thái đăng nhập Google của gateway lúc thi hành: không đo.
