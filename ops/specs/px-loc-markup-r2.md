tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# PX-LOC-MARKUP r2 — `proxima-control` lọc khối `<ElicitationsGroup>` khỏi câu trả lời (đặc tả, thay r1)

## packet_id · packet_issue
- `packet_id`: `px-loc-markup`. Revision 2, generation 1. Role `executor` (Claude).
- `packet_issue`: #1529.

## nguon_cap_viec
- Đặc tả r1 `ops/specs/px-loc-markup-r1.md` (sha256 `631a8bebbc22ba281312ae468142fee0892f302914ed8fb1c25eae41f6b8ecb6`, commit
  `b01f3ddcf67760c6678e3de18d942208538dae63`, chủ kho duyệt `issuecomment-7171310505`). r1 chưa land.
- Review offline §8.3 lượt 1 trên ứng viên r1 `8a33ddbe284a369f686f145169d02af7a8008e58`: `changes_requested`, 5 lớp P2
  (https://github.com/ducthangho/tra-luat/issues/1529#issuecomment-7171976816). Một lớp là lỗi của đặc tả r1: diff vượt trần số tệp của
  `ADR-0053` mà r1 không khai `nang_tran`.
- Chủ kho chọn nâng trần (E2): https://github.com/ducthangho/tra-luat/issues/1529#issuecomment-7172063543.
- Gốc việc: #1457 r2 (`ops/acceptance/px-gemini-500/r2/RESULTS.md`, hồ sơ mang khối đính chính — mọi kết luận là lời khai chưa xác minh
  trong kho), đề xuất `issuecomment-7053599823`. Chủ kho chốt Q1–Q8 ngày 25-11-2026; tiền lệ cấu trúc `ops/specs/px-ask-r3.md`.

## r2 đổi gì so với r1
1. Khai `nang_tran` (mục dưới).
2. Mục tiêu 1–2 chỉnh theo hai lớp P2 của lượt 1: cắt khoảng trắng cuối chỉ khi sau khối cuối không còn gì ngoài khoảng trắng; thẻ mở
   phải hoàn chỉnh mới được ghép.
3. N1 đo rò rỉ trên đối tượng thô của mọi luồng (lớp P2 thứ ba của lượt 1); thêm ca biên.
4. Mục tiêu 6 neo hướng dẫn vào đúng mức lời khai #1457 r2 (lớp P2 thứ tư của lượt 1).
5. Write set đổi đặc tả/lease/RESULTS sang r2; tệp r1 tương ứng rời khỏi nhánh (chưa land, lease r1 chưa từng push).

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

## Số đo nền (đo 25-11-2026 ~18:40Z trên `origin/master` `d0868db`; không đổi so với r1)
- Câu trả lời đi qua đúng một chỗ: `Invoke-PxcAsk` (`.agents/skills/proxima-control/scripts/ProximaControl.psm1`), gán `answer` từ
  `choices[0].message.content` và trả kèm `answerTrust = 'untrusted_data'`.
- Hình dạng khối (ĐÚNG MỘT mẫu, lượt C3 chủ kho dán 20-11-2026; chỉ ghi cấu trúc): `<ElicitationsGroup message="…">`, bên trong các
  `<Elicitation label="…" query="…"/>`, đóng bằng `</ElicitationsGroup>`; không có dạng tự đóng của thẻ nhóm.
- `ModuleVersion` = `2.1.0`. Harness `ProximaControl.Tests.ps1`: 27 ca bắt buộc, counterexample `CX00`–`CX13`.
- CI không chạy harness này; container phiên web không có `pwsh` sẵn.
- Module không có trong `RELEASE_MANIFEST.json` ⇒ không tái sinh manifest.

## write_set
- `.agents/skills/proxima-control/scripts/ProximaControl.psm1`
- `.agents/skills/proxima-control/scripts/ProximaControl.psd1`
- `.agents/skills/proxima-control/SKILL.md`
- `.agents/skills/proxima-control/tests/ProximaControl.Tests.ps1`
- `.agents/skills/proxima-control/tests/ProximaManifest.Tests.ps1`
- `ops/specs/px-loc-markup-r2.md`
- `ops/leases/px-loc-markup-r2-g1-claude.yaml`
- `ops/acceptance/px-loc-markup/r2/RESULTS.md`

Đặc tả, lease và RESULTS của r1 không có trong diff cuối của nhánh (tệp r1 bị gỡ khỏi nhánh trước push); bản r1 còn tra được qua
commit `b01f3dd` và các comment trên #1529.

## ngoai_pham_vi
- Chặn bằng mã các model `gemini:<biến thể>` khác `auto` (Q4: chỉ hướng dẫn trong `SKILL.md`).
- Lọc thẻ markup nào khác ngoài `ElicitationsGroup`/`Elicitation` (Q1), kể cả dạng tự đóng của thẻ nhóm (chưa quan sát; coi là thẻ hỏng).
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
   (`[int]` ≥ 0). Nội dung đã bỏ không xuất hiện ở bất kỳ trường, luồng hay bản ghi nào (Q3). `answer` không phải chuỗi ⇒ `none`, 0.
4. `ProximaControl.psm1` — help của `px` nêu hai trường mới.
5. `ProximaControl.psd1` — `ModuleVersion` `2.1.0` → `2.2.0` (Q5).
6. `SKILL.md` — phiên bản 2.2.0; mô tả hai trường và luật cắt đuôi; hướng dẫn chạy tự động với Gemini thì nên dùng `gemini:auto`, nêu
   căn cứ đúng mức: #1457 r2 là lời khai chưa xác minh, kể một lời gọi model chỉ định HTTP 500 vì luồng treo và một lời gọi
   `gemini:auto` trả được câu trả lời; không khẳng định cơ chế gateway hay nguồn gốc khối như sự thật đã đo; ghi hệ quả handshake Remote.
7. `ProximaManifest.Tests.ps1` — `$Want` và `CX04` theo 2.2.0.
8. `ProximaControl.Tests.ps1` — ca bắt buộc `X5-11` (27 → 28 id), `CX14`, `CX15` (mục `nghiem_thu`).
9. `ops/acceptance/px-loc-markup/r2/RESULTS.md` — biên nhận phép đo và chạy test Windows.
10. `ops/specs/px-loc-markup-r2.md`, `ops/leases/px-loc-markup-r2-g1-claude.yaml` — đặc tả này và lease.

## nghiem_thu
"Ca" = một id trong `$Ids` của harness; "CX" = một counterexample.

- **N1 (mục tiêu 1–3)** — `X5-11` dựng phản hồi giả qua cơ chế HTTP giả của harness (không gateway thật), so Ordinal toàn chuỗi `answer`,
  cùng `answerMarkup` và `answerMarkupRemoved` (kiểu `[int]`), trên đủ các ca: không khối; một khối ở cuối (`OK`); hai khối (giữa và
  cuối); khối giữa câu, đuôi có space + CRLF (đuôi giữ nguyên); khối giữa câu, đuôi NBSP (giữ nguyên); thẻ mở không có thẻ đóng; khối lồng;
  thẻ mở thiếu `>`; dấu nháy chưa đóng trong thẻ mở; thẻ nhóm tự đóng; tên `ElicitationsGroupX`; tên viết thường; văn bản giữ lại có
  marker riêng đứng ngoài khối.
  Rò rỉ: với verbose và debug bật, marker đặt **trong** khối bị bỏ không được có mặt trong đối tượng thô của mọi luồng (chuỗi output, đối
  tượng output tuần tự hoá JSON, error, warning, verbose, debug, information) và trong bản ghi `px-active` của đúng `recordId`; bản ghi
  ấy **phải** tồn tại (vắng ⇒ đỏ). Marker phần giữ lại khác marker phần bỏ.
  ĐỎ khi: một giá trị lệch; bản ghi vắng; marker phần bỏ lộ ra; `CX14`/`CX15` (N2) làm ca đỏ với token có tên.
- **N2** — `CX14` (bỏ bước lọc trong `Invoke-PxcAsk`) phải `credited` với token `X5-11:MARKUP_ANSWER[one block]`; `CX15` (so tên thẻ
  `OrdinalIgnoreCase`) phải `credited` với token `X5-11:MARKUP_STATE[case variant]`. ĐỎ khi một mutant sống.
- **N3** — 27 ca cũ vẫn đạt; `CX00`–`CX13` vẫn `credited`. ĐỎ khi bất kỳ ca/CX cũ đổi màu.
- **N4** — `ProximaManifest.Tests.ps1` đạt với `2.2.0`; ĐỎ khi để `.psd1` ở `2.1.0` (đột biến tay, ghi vào RESULTS).
- **N5 (mục tiêu 6)** — trên `SKILL.md` nối dòng theo từng đoạn: vế dương — có câu hướng dẫn dùng `gemini:auto` khi chạy tự động, có
  cụm "lời khai chưa xác minh" trong cùng đoạn ấy, có tên `answerMarkup` và `answerMarkupRemoved`; vế âm — không còn `2.1.0` ở frontmatter
  và ở mục *Phiên bản* (đếm từng vị trí). ĐỎ khi xoá câu hướng dẫn, xoá cụm lời khai, hay để lại `2.1.0`.
- **N6 (nền chạy)** — trên máy Windows của chủ kho, từ clone sạch tại SHA ứng viên: `ProximaControl.Tests.ps1` với PS 7 và PS 5.1, mỗi bản
  `en-US` và `tr-TR`; `-Counterexamples` ở PS 7 `en-US`; `ProximaManifest.Tests.ps1` với PS 7 và PS 5.1. Đạt khi mọi lượt rc 0,
  `passed == total`, mọi CX `credited`. ĐỎ khi một lượt rc ≠ 0, `passed < total`, hay thiếu lượt nào. Báo cáo JSON lưu ngoài cây, băm
  ghi vào RESULTS.
- **N7 (gate kho)** — `python3 scripts/tl.py --selftest` N/N, `git diff --check` sạch, `ops/lease_publish.py check` rc 0 cho lease r2.
- **N8 (phạm vi và trần)** — `git diff --name-only <base>..<H>` ⊆ `write_set` và `git diff --numstat` ≤ 8 tệp / ≤ 450 dòng thêm
  (`tran_moi`). ĐỎ khi có đường dẫn ngoài danh sách hoặc vượt `tran_moi`.

Windows M3 (ADR-0060): `required`; N6 là lượt Windows của packet.

## luat_dung
- Điểm dừng của `docs/PROTOCOL_DA_PHIEN.md` §12 (tỷ lệ đóng lớp; lớp/hình dạng lỗi lần thứ ba) — dẫn, không chép. Lịch sử lớp của lượt 1
  ở `hinh_dang_ke_thua`.
- Trần lời gọi Codex theo dòng khai `ADR-0055`; đã dùng 1 (offline lượt 1). Chạm trần mà cần thêm ⇒ **E2**.
- Trần kích thước theo `nang_tran` trên; vượt `tran_moi` ⇒ **E2**.
- Máy Windows của chủ kho không sẵn sàng cho N6 ⇒ **E2**, mang theo ma trận lượt còn thiếu.
- Mẫu thật mâu thuẫn Q1–Q8 (khối tự đóng, tên khác) ⇒ **E3**, mang theo mẫu đã che.
- Lease r2 chỉ cấp sau khi lease r1 (`px-loc-markup-r1-g1-claude`, chưa push) hết hạn lúc 2026-11-25T22:45:09Z và `ai-dang-giu` ra 0
  cho cả write set; không bia mộ.

## pham_vi_e
Không chạm E4, không chạm E5. Packet không thuộc Mission đã duyệt hướng ⇒ đặc tả chờ chủ kho duyệt băm trước khi cấp lease.

## hinh_dang_ke_thua
Lớp đã xuất hiện ở review offline lượt 1 (ứng viên r1 `8a33ddb`), mỗi lớp **1** lần xuất hiện:
`markup-trims-unrelated-tail` · `markup-pairs-incomplete-opener` · `markup-leak-test-loses-evidence` · `runtime-claims-exceed-evidence` ·
`sensitive-diff-exceeds-file-cap`. Riêng `runtime-claims-exceed-evidence` đã giữ P2 nhiều lượt ở packet #1457 — lớp ấy nằm ở packet khác
nên không cộng vào bộ đếm của packet này, nhưng là dấu hiệu phải viết tài liệu sát lời khai.

## chua_do_duoc
- Biến thể khác của khối `ElicitationsGroup`: **KHÔNG ĐO ĐƯỢC** — một mẫu, phản hồi thô của gateway không được lưu.
- Markup khác trong câu trả lời Gemini: **KHÔNG ĐO ĐƯỢC** trong r2.
- Hành vi trên gateway thật sau khi lọc: chỉ đo ở revision kiểm thật sau merge (Q7).
- Trạng thái đăng nhập Google của gateway lúc thi hành: không đo.
