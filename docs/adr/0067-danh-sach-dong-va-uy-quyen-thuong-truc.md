# ADR-0067 — Danh sách đóng E1–E5 cho việc hỏi chủ kho, và uỷ quyền thường trực

- **Trạng thái:** Accepted (2026-11-15, chủ kho `ducthangho` duyệt `spec_hash` `4d94f1fedd198547901cd310f04c83fa8984f310d9c3be72609e8c36d692a6e9` của đặc tả `GIAM-HOI-P2-ADR-E1-E5` r11 trên Issue #1292: https://github.com/ducthangho/tra-luat/issues/1292#issuecomment-6880923050)

## Bối cảnh

Đo ngày 07-11-2026 trên Issue/PR của kho bằng `gh api`, 31 ngày từ 08-10-2026: chủ kho có 391 comment quyết định, 226
trong số đó do agent ghi hộ từ câu trả lời trong phiên chat; kho có 253 lần đăng lease, lần nào cũng
`granted_by: ducthangho`. Nguồn là tài liệu "Giảm việc hỏi chủ kho" (https://claude.ai/artifact/6JUF8DsbHxfN5GjsbdAtHT),
do hai agent chỉ đọc đo trên `origin/master` `27fd808`. Tài liệu ước lượng khoảng 220 trong 273 quyết định có loại rõ
ràng sẽ không cần chủ kho nữa; đó là ước lượng theo loại, chưa đo trên việc thật.

Các lần hỏi đến từ ba nguồn chính: đặc tả tự thêm điểm hỏi; mã đòi đúng tên chủ kho (`NGUOI_CO_THAM_QUYEN` ở
`.claude/dev/packet_loop.py` và `ops/lease_publish.py`) cho lease, nâng trần, miễn trừ và huỷ lượt; và các câu trong ADR,
protocol đòi checkpoint chủ kho cho từng việc nhỏ. Ngày 07-11-2026 chủ kho chỉ đạo chỉ hỏi khi hướng đi bế tắc, thiếu tài
nguyên, hay phát hiện đảo ngược chỉ đạo. Ngày 08-11-2026 chủ kho đồng ý năm khuyến nghị của tài liệu nguồn, nguyên văn:
*"Bạn làm hộ cho tôi luôn. TÔi đồng ý duyệt 5 điểm và chốt nâng trần theo đề xuất"*.

## Quyết định

Agent chỉ dừng để hỏi chủ kho khi rơi vào một trong năm mã E1–E5 dưới đây; mọi việc khác agent tự quyết, ghi vào sổ
quyết định uỷ quyền và báo trong bản tin hằng ngày.

| mã | tình huống | ví dụ trong kho | phải mang theo khi hỏi |
|---|---|---|---|
| E1 | Hướng đi bế tắc: đã xét lại cách làm mà không còn phương án nào có phép đo chống đỡ | một hình dạng lỗi lặp lại sau khi đã đổi thiết kế; cùng một finding hai lần sau hai cách sửa khác nhau | gốc rễ, các phương án đã thử và vì sao hỏng, một đề xuất |
| E2 | Thiếu tài nguyên: chạm trần cứng, hoặc thiếu máy, quota hay quyền | hết lời gọi Codex theo trần của đặc tả; hết ngân sách CI; máy Windows offline quá hạn; credential Codex chết; một cổng mã đòi quyền chỉ chủ kho có | mức đã dùng, còn thiếu bao nhiêu, để làm gì |
| E3 | Phát hiện đảo ngược chỉ đạo: bằng chứng mâu thuẫn với một quyết định của chủ kho | thiết kế chủ kho chọn không đạt mục tiêu; một ADR chủ kho duyệt gây hại đo được | quyết định nào, bằng chứng, hậu quả nếu giữ nguyên |
| E4 | Hành động không hoàn tác được hay đi ra ngoài kho | đẩy Package lên Drive; `clasp`/GAS deploy; `--apply` lên registry, Drive, NLM; xoá ref hay tag ngoài luật của `.github/workflows/ops-don-ref.yml`; đọc hay ghi secrets; đổi ruleset | lệnh chính xác, đích, cách hoàn tác nếu có |
| E5 | Đổi chính thẩm quyền | sửa danh sách này; sửa `NGUOI_CO_THAM_QUYEN` hay danh sách cho phép tương đương; sửa mã cổng cấp lease hay cổng merge; sửa ADR này | diff, lý do, ai được thêm quyền gì |

E4 và E5 định nghĩa theo hậu quả, không theo tên lệnh; không rõ một việc có thuộc E4 hay E5 không thì coi là thuộc. Merge
commit hoàn tác được, nên merge tự nó không là E4.

Mỗi câu hỏi gửi chủ kho ghi mã E của nó và mang theo thứ cột cuối của bảng nêu; câu không gắn được mã nào thì agent
không hỏi mà tự quyết.

Năm quyết định ngày 08-11-2026:

1. Danh sách đóng là bảng trên, đủ năm mã.
2. Đặc tả packet thuộc một Mission chủ kho đã duyệt hướng được người soạn đóng băng khi một review độc lập approve,
   không cần comment duyệt băm của chủ kho; đặc tả đảo một quyết định của chủ kho (E3) hay chạm E4, E5 vẫn cần chủ kho
   duyệt băm.
3. Audit uỷ quyền áp cho mọi packet không chạm E5 và mang mức bảo đảm riêng `delegated_audited`, không bao giờ được
   ghi thành `human_audited`; packet chạm E5 vẫn cần chủ kho audit. Phiên audit uỷ quyền là phiên mới, không chung ngữ
   cảnh với executor hay reviewer, chỉ đọc, chạy trên đúng SHA; nó đối chiếu đặc tả và diff với các quyết định chủ kho đã
   ghi, và dừng để hỏi khi thấy E3, E4 hay E5.
4. Packet không chạm E4 hay E5 được tự merge khi đủ điều kiện merge của `ADR-0060`, review approve và audit uỷ quyền
   đạt; packet chạm E4 hay E5 cần một lần duyệt của chủ kho neo SHA. Tự merge giữ tách vai của `ADR-0034`: review
   approve và audit uỷ quyền đến từ phiên độc lập với executor, và executor làm Land Operator theo uỷ quyền bền cũng
   không nhờ đó tự review hay approve diff của mình.
5. Chủ kho uỷ quyền thường trực cho phiên điều phối cấp lease cho packet thuộc Mission chủ kho đã duyệt hướng, sau khi
   quét toàn kho ra không người giữ nào trên write set; uỷ quyền có hạn 30 ngày kể từ comment cấp, gia hạn bằng comment
   mới, và chủ kho thu hồi bằng một comment. Write set chạm E4 hay E5 thì phiên điều phối không cấp lease theo uỷ quyền
   thường trực mà hỏi chủ kho; lease cấp theo uỷ quyền ghi URL comment uỷ quyền nó dựa vào.

Một Mission được coi là đã duyệt hướng khi Mission Issue có comment của chủ kho, hay comment ghi hộ đúng luật ở mục
*Comment ghi hộ*, chấp nhận `plan_hash` của revision đang chạy.

## Sổ quyết định uỷ quyền

Mỗi quyết định agent đưa thay cho một câu hỏi trước đây là một comment trên Issue của packet, thân là đúng một khối YAML
`uy_quyen_quyet_dinh.v1` theo bảng dưới đây. Mục sổ là hồ sơ của một quyết định trong phạm vi uỷ quyền chủ kho đã cấp;
nó không tự cấp quyền (`ADR-0023`).

| khoá | kiểu | nghĩa |
|---|---|---|
| `schema` | chuỗi | đúng `uy_quyen_quyet_dinh.v1` |
| `loai` | chuỗi | một trong `cap_lease`, `dong_bang_dac_ta`, `mien_p3`, `phan_loai_windows`, `huy_luot`, `push_them`, `tu_merge`, `audit_uy_quyen`, `xet_lai_cach_lam`, `khac` |
| `packet` | chuỗi | `packet_id` như trong lease hay đặc tả |
| `revision` | số nguyên | revision của đặc tả packet |
| `sha` | OID 40 hex viết trong nháy kép, hay `null` | commit quyết định neo vào: commit chứa đặc tả với `dong_bang_dac_ta`; exact head H với `mien_p3`, `phan_loai_windows`, `tu_merge`, `audit_uy_quyen`; SHA mới với `push_them`; head của lượt với `huy_luot`; `null` với `cap_lease` và với quyết định không neo commit |
| `spec_sha256` | 64 hex viết trong nháy kép, hay `null` | sha256 của đặc tả mà quyết định dựa vào |
| `can_cu` | danh sách, ít nhất một | mỗi phần tử có `vai` (một trong `uy_quyen`, `review`, `audit`, `kiem_merge`, `luat`, `bi_bac`, `log`) và `url` (URL); vai bắt buộc theo `loai` ở bảng sau |
| `phep_do` | danh sách, ít nhất một | mỗi phần tử có `lenh` (chuỗi), `rc` (số nguyên), `ket_qua` (chuỗi) |
| `kiem_e` | ánh xạ | đủ năm khoá `E1`–`E5`, giá trị `khong` hay `co`; có một `co` thì agent không được tự quyết mà phải hỏi |
| `nguoi_quyet` | ánh xạ | `provider`, `model_family`, `session_id` của phiên đưa quyết định |
| `hoan_tac` | chuỗi | cách hoàn tác nếu chủ kho bác |
| `luc` | chuỗi | thời điểm UTC dạng `YYYY-MM-DDTHH:MM:SSZ` |

Vai bắt buộc trong `can_cu` theo `loai`; một mục sổ thiếu vai bắt buộc thì không có giá trị:

| `loai` | vai bắt buộc |
|---|---|
| `cap_lease` | `uy_quyen` |
| `dong_bang_dac_ta`, `mien_p3`, `phan_loai_windows`, `push_them`, `xet_lai_cach_lam` | `review` |
| `huy_luot` | `log` |
| `audit_uy_quyen` | `audit` |
| `tu_merge` | `review`, `audit`, `kiem_merge`, `luat` |
| `khac` | không có |

Mục sổ `tu_merge` là authorization land của protocol §13.1, nên mang thêm sáu khoá dưới đây; loại khác không mang
chúng. Vai `luat` của nó trỏ quyết định 4 của ADR này.

| khoá | kiểu | nghĩa |
|---|---|---|
| `pr` | số nguyên | số PR được merge |
| `dich` | chuỗi | nhánh đích, đúng `master` |
| `phuong_thuc` | chuỗi | đúng `merge` (merge commit) |
| `tree` | OID 40 hex viết trong nháy kép | tree của H |
| `het_han` | chuỗi | thời điểm UTC cùng dạng `luc`, không quá 24 giờ sau `luc`; quá hạn mà chưa merge thì phải có mục sổ mới |
| `hau_merge` | danh sách | đúng bốn việc M7 liệt kê: `bang_chung_hau_merge`, `ghi_so`, `nha_lease`, `dong_wp` |

Ba mục sổ mẫu: một không neo commit, một neo exact head, một là authorization land:

```yaml
schema: uy_quyen_quyet_dinh.v1
loai: cap_lease
packet: VI-DU-PACKET
revision: 1
sha: null
spec_sha256: "1111111111111111111111111111111111111111111111111111111111111111"
can_cu:
  - {vai: uy_quyen, url: "https://github.com/ducthangho/tra-luat/issues/1#issuecomment-1"}
phep_do:
  - lenh: python ops/lease_publish.py ai-dang-giu --root . docs/vi-du.md
    rc: 0
    ket_qua: "NGƯỜI_GIỮ 0: không có"
kiem_e: {E1: khong, E2: khong, E3: khong, E4: khong, E5: khong}
nguoi_quyet: {provider: claude, model_family: claude, session_id: vi-du-1}
hoan_tac: thu hồi lease theo luật thu hồi hiện hành
luc: "2026-11-08T00:00:00Z"
```

```yaml
schema: uy_quyen_quyet_dinh.v1
loai: mien_p3
packet: VI-DU-PACKET
revision: 1
sha: "2222222222222222222222222222222222222222"
spec_sha256: "1111111111111111111111111111111111111111111111111111111111111111"
can_cu:
  - {vai: review, url: "https://github.com/ducthangho/tra-luat/pull/2#issuecomment-2"}
phep_do:
  - lenh: đọc verdict review trên H, lớp vi-du-lop
    rc: 0
    ket_qua: "P3 duy nhất còn mở: vi-du-lop"
kiem_e: {E1: khong, E2: khong, E3: khong, E4: khong, E5: khong}
nguoi_quyet: {provider: claude, model_family: claude, session_id: vi-du-2}
hoan_tac: mở lại vi-du-lop thành finding phải sửa trước merge
luc: "2026-11-08T00:00:00Z"
```

```yaml
schema: uy_quyen_quyet_dinh.v1
loai: tu_merge
packet: VI-DU-PACKET
revision: 1
sha: "2222222222222222222222222222222222222222"
spec_sha256: "1111111111111111111111111111111111111111111111111111111111111111"
can_cu:
  - {vai: review, url: "https://github.com/ducthangho/tra-luat/pull/2#issuecomment-2"}
  - {vai: audit, url: "https://github.com/ducthangho/tra-luat/pull/2#issuecomment-3"}
  - {vai: kiem_merge, url: "https://github.com/ducthangho/tra-luat/issues/1#issuecomment-4"}
  - {vai: luat, url: "https://github.com/ducthangho/tra-luat/blob/master/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md"}
phep_do:
  - lenh: python .claude/dev/packet_loop.py kiem-merge …
    rc: 0
    ket_qua: "K0–K7 đạt trên H"
kiem_e: {E1: khong, E2: khong, E3: khong, E4: khong, E5: khong}
nguoi_quyet: {provider: claude, model_family: claude, session_id: vi-du-3}
hoan_tac: mở PR revert merge commit
luc: "2026-11-08T00:00:00Z"
pr: 2
dich: master
phuong_thuc: merge
tree: "3333333333333333333333333333333333333333"
het_han: "2026-11-09T00:00:00Z"
hau_merge: [bang_chung_hau_merge, ghi_so, nha_lease, dong_wp]
```

Chủ kho bác một quyết định bằng comment `bac: <URL mục sổ>`, kèm lý do nếu muốn; phiên kế tiếp chạm packet ấy hoàn tác
quyết định trước mọi việc khác và ghi mục sổ mới trỏ mục bị bác.

## Bản tin hằng ngày

Bản tin là một comment mỗi ngày trên Issue bản tin của kho, liệt kê theo loại mọi mục sổ đăng trong ngày hôm trước kèm
URL, các câu hỏi E1–E5 đang chờ, các mục đã bị bác và uỷ quyền thường trực còn dưới 7 ngày; ngày không có mục sổ nào thì
không đăng.

Cho tới khi có job tự động, phiên điều phối đầu tiên của mỗi ngày theo giờ Việt Nam (UTC+7) đăng bản tin của ngày hôm
trước; comment cấp, gia hạn và thu hồi uỷ quyền thường trực cũng nằm trên Issue bản tin.

Issue bản tin là Issue mở duy nhất có tiêu đề bắt đầu bằng `Bản tin quyết định uỷ quyền`; chưa có thì phiên đăng bản tin
đầu tiên tạo nó.

Comment cấp hay gia hạn uỷ quyền thường trực là đúng một khối YAML `uy_quyen_thuong_truc.v1`, và chỉ có hiệu lực khi
là comment của chủ kho hay comment ghi hộ đúng luật ở mục *Comment ghi hộ*:

| khoá | kiểu | nghĩa |
|---|---|---|
| `schema` | chuỗi | đúng `uy_quyen_thuong_truc.v1` |
| `pham_vi` | chuỗi | đúng `cap_lease` |
| `cap_luc` | chuỗi | thời điểm UTC cấp, dạng `YYYY-MM-DDTHH:MM:SSZ` |
| `het_han` | chuỗi | đúng 30 ngày sau `cap_luc`, cùng dạng |

Thu hồi bằng comment có dòng `thu_hoi_uy_quyen: <URL comment cấp>`. Uỷ quyền hết hiệu lực ở mốc `het_han` hay ở thời điểm
của comment thu hồi, mốc nào đến trước.

## Comment ghi hộ

Comment agent đăng thay chủ kho phải có dòng `Quyết định chủ kho — ghi hộ`, kèm nguyên văn câu của chủ kho và ngữ cảnh
câu hỏi; agent chỉ ghi hộ điều chủ kho đã quyết.

Phiên agent đăng bằng credential của chủ kho, nên tên tác giả của comment không chứng minh ai đã quyết; nhãn ghi hộ và
sổ quyết định là lời khai có cấu trúc, không phải bằng chứng danh tính.

Đăng xong, comment ghi hộ được đọc ngược bằng `gh api … --jq .body` và so với bản đã gửi. Ghi hộ không tự cấp lease hay
merge.

## Hiệu lực và chuyển tiếp

ADR này có hiệu lực từ commit land của nó trên first-parent master và không hồi tố. Cơ chế nào bảng chuyển tiếp ghi
hiệu lực từ land packet đổi cổng thì chỉ có hiệu lực từ commit land của packet đổi cổng ấy; trước đó cổng hiện hành giữ
nguyên, và câu hỏi cổng ấy còn đòi mang mã E2, vì agent thiếu quyền mà cổng chỉ cấp cho chủ kho.

| điểm hỏi hiện nay | cổng đang đòi | cách làm mới | mã E còn hỏi sau hiệu lực | hiệu lực |
|---|---|---|---|---|
| Cấp lease | `ops/lease_publish.py` (danh sách cho phép `granted_by`); `packet_loop.py` `record-lease` | phiên điều phối cấp theo uỷ quyền thường trực (quyết định 5), ghi mục sổ `cap_lease` | E4, E5 | từ land packet đổi cổng |
| Duyệt băm đặc tả | không cổng mã | người soạn đóng băng sau review độc lập (quyết định 2), ghi mục sổ `dong_bang_dac_ta` | E3, E4, E5 | từ land ADR này |
| Nâng trần | `packet_loop.py` `nang-tran` | đặc tả khai trần của `ADR-0055` từ đầu; không ngân sách mềm | E2 | từ land ADR này |
| Review Rescue Checkpoint vì chạm trần | `packet_loop.py` `record-rescue` | hỏi khi cần thêm lời gọi hay vòng | E2 | từ land ADR này |
| Checkpoint vì hình dạng lỗi lặp, không hội tụ hay vòng vá P3 không giảm lớp | không cổng mã | phiên tự xét lại cách làm, ghi mục sổ `xet_lai_cach_lam` | E1, E3 | từ land ADR này |
| Miễn P3 còn mở | `packet_loop.py` `kiem-merge` K5 | agent ghi nợ có tên bằng mục sổ `mien_p3` | không | từ land packet đổi cổng |
| Windows: `unknown`, ca đỏ trong write set, máy offline | `packet_loop.py` `kiem-merge` K6 | reviewer chốt `unknown`, ghi mục sổ `phan_loai_windows`; ca đỏ trong write set và máy offline vẫn hỏi chủ kho | E2 | từ land packet đổi cổng |
| Miễn mutant | `packet_loop.py` `kiem-merge` K7 | không miễn; không chạy được thì hỏi | E2 | từ land ADR này |
| Push thêm | không cổng mã | làm sau review offline và bất biến (a), ghi mục sổ `push_them` | E2 | từ land ADR này |
| Human audit | `packet_loop.py` `kiem-merge` K4 | audit uỷ quyền `delegated_audited` (quyết định 3) | E5 | từ land packet đổi cổng |
| Duyệt merge | không cổng mã riêng; cần audit uỷ quyền đã có hiệu lực | tự merge, ghi mục sổ `tu_merge` (quyết định 4) | E4, E5 | từ land packet đổi cổng |
| Huỷ lượt không có bằng chứng máy | `packet_loop.py` `void-attempt` | mục sổ `huy_luot` kèm log lỗi gốc | E2 | từ land packet đổi cổng |
| Mở phiên kế nhiệm và phiên reviewer | không cổng mã | phiên điều phối tự mở | không | từ land ADR này |

## Thay những gì

Mỗi câu dưới đây thay đúng câu được trích, từ mốc hiệu lực của hàng tương ứng trong bảng chuyển tiếp. Không sửa nội dung
tệp của các ADR ấy.

- `ADR-0060` M1, câu *"Agent không tự ghi nợ P3"* và vế *"hoặc chủ kho miễn"*: P3 còn mở mà không đóng được trên SHA ứng
  viên thì agent ghi nợ có tên bằng một mục sổ `mien_p3`: vai `review` của `can_cu` trỏ verdict xếp mức P3, `phep_do` ghi
  slug và lý do, `hoan_tac` ghi hướng xử lý; agent không được hạ mức, gộp slug hay ghi nợ cho P0, P1, P2.
- `ADR-0060` M1, vế *"vòng ấy không giảm số lớp P3 thì dừng, checkpoint chủ kho"*: phiên dừng vòng vá P3 và xét lại cách
  làm như hàng *Checkpoint vì hình dạng lỗi lặp, không hội tụ hay vòng vá P3 không giảm lớp*; chỉ hỏi chủ kho khi rơi vào E1
  hay E3.
- `ADR-0060` M3, việc chủ kho chốt `unknown` (cổng `kiem-merge` K6 đòi dòng `windows: <head> not_required` của chủ kho):
  `unknown` do reviewer chốt `required` hay `not_required` kèm lý do trong verdict, như văn bản M3 đã ghi, và ghi mục sổ
  `phan_loai_windows`. Vế *"(c) ca đỏ thuộc tệp trong write set ⇒ chủ kho quyết"* giữ nguyên: agent không có quyền chấp
  nhận ca đỏ ấy, nên câu hỏi mang mã E2 và dòng `windows: <head> mien` vẫn là câu trả lời của chủ kho. Máy Windows không
  `Online` quá hạn báo của M3 là E2.
- `ADR-0060` M5, vế *"cần checkpoint chủ kho"* trong câu về mỗi lần push thêm: push thêm được làm khi SHA mới đã qua
  review offline và bất biến (a), mỗi lần ghi một mục sổ `push_them`; dòng biên nhận và số lần tối đa của M5 giữ nguyên,
  chạm số ấy là E2. Protocol §12 bất biến (b) đổi theo.
- `ADR-0060` M7, câu *"Chủ kho duyệt một lần, neo SHA H"*, cho packet không chạm E4 hay E5: mục sổ `tu_merge` neo H, mang
  đủ sáu khoá riêng ở mục *Sổ quyết định uỷ quyền*, thay cho lần duyệt ấy và bao gồm đúng những việc M7 liệt kê.
- `ADR-0060` M8, trường *"lần duyệt của chủ kho"* của bản ghi hoàn tất, cho packet tự merge: trường ấy mang URL mục sổ
  `tu_merge`. Người quyết đọc từ khoá `nguoi_quyet` của mục sổ và từ quyết định 4 của ADR này; phiên land chỉ chở bản ghi.
- `ADR-0060` mục *Những gì KHÔNG đổi*, câu *"agent không tự approve hay merge"*: vế *"không tự approve"* giữ nguyên. Vế
  *"không tự merge"*, cho packet không chạm E4 hay E5, thành *"chỉ merge theo một mục sổ `tu_merge` hợp lệ"*.
- Protocol §8, câu *"Human Land Approver phải readback exact-head verdict/receipt trước khi land Packet `sensitive`"*, cho
  packet tự merge: phiên land làm phép readback ấy và ghi lệnh, kết quả vào `phep_do` của mục sổ `tu_merge`; câu ấy giữ
  nguyên cho packet chạm E4 hay E5.
- Protocol §13 mục `land-packets` (*"user-invoked client"*, *"Không tự trigger"*), cho packet tự merge: phiên điều phối
  được gọi land theo một mục sổ `tu_merge` hợp lệ; với packet chạm E4 hay E5, land vẫn chỉ chạy khi người có thẩm quyền
  gọi.
- `ADR-0060` M9 không đổi điều kiện bắt buộc: agent không được miễn một lượt `full_mutant_audit` bắt buộc; không chạy được
  vì thiếu máy, ngân sách hay quyền là E2, và dòng `full_mutant_audit: <head> mien` vẫn là câu trả lời của chủ kho.
- `ADR-0063` K4, vế *"Comment phải từ owner canonical `ducthangho`"*, cho packet không chạm E5: K4 nhận thêm biên nhận
  `delegated_audited` của phiên audit uỷ quyền neo đúng H; packet chạm E5 giữ nguyên K4.
- `void-attempt` không có bằng chứng máy (`.claude/dev/packet_loop.py`, dòng cho phép của chủ kho): lý do vẫn phải thuộc
  danh sách lý do của mã, và lượt đã có review vẫn không được hoàn; dòng cho phép của chủ kho thay bằng một mục sổ
  `huy_luot` kèm log lỗi gốc của lượt ấy. Không có log gốc thì là E2.

## Chỗ tiêu thụ phải đổi theo

Mỗi cơ chế cần cổng mã có những chỗ khác cũng đọc quyền hay nghĩa vụ cũ. Bảng dưới là **sàn, không phải danh sách đủ**:
đặc tả của packet đổi cổng phải tự lập lại bảng tiêu thụ cho cơ chế của mình trên protocol, các ADR đang hiệu lực, mã cổng
và adapter cả hai nền, đọc theo nghĩa vụ chứ không chỉ theo từ khoá, rồi xếp từng chỗ vào một trong ba loại: **đổi** (theo
một quyết định đã duyệt, bằng câu ở mục *Thay những gì*), **giữ** (không quyết định nào đổi nó), **cần quyết định riêng**
(đổi nó là E3 hay E5, phải hỏi chủ kho). Chỗ bảng này xếp **giữ** thì packet sau không đổi khi chưa có quyết định riêng.

| cơ chế | chỗ tiêu thụ | xếp loại |
|---|---|---|
| Cấp lease theo uỷ quyền | `ops/lease_publish.py`: danh sách cho phép người cấp `granted_by`, phép kiểm `GITHUB_ACTOR`; `.claude/dev/packet_loop.py` `record-lease`; `.claude/skills/work-packet/SKILL.md` (`--granted-by ducthangho`) | đổi, ở packet đổi cổng lease |
| Cấp lease theo uỷ quyền | `ops/lease_publish.py`: người thu hồi `thu_hoi_boi` | giữ: uỷ quyền chỉ có phạm vi `cap_lease`; thu hồi lease theo luật hiện hành |
| Miễn P3 bằng mục sổ | `.claude/dev/packet_loop.py` `kiem-merge` K5 và trợ giúp của `--chu-kho-comment`; protocol §8 bảng ngưỡng severity, ba hàng `routine`, `systemic`, `sensitive`; `ADR-0060` M1 và bảng *Tham số*, hàng *P3 còn mở* | đổi, ở packet đổi cổng K5 |
| Reviewer chốt Windows `unknown` | `.claude/dev/packet_loop.py` `kiem-merge` K6, dòng `windows: <head> not_required`; `ADR-0060` M3 | đổi, ở packet đổi cổng K6; dòng `windows: <head> mien` và vế (c) của M3 giữ |
| Audit uỷ quyền | `.claude/dev/packet_loop.py` `kiem-merge` K4, schema `human_exact_head_audit.v1`; `ops/bien_nhan_v2.py` (mức `delegated_audited`) | đổi, ở packet đổi cổng K4 |
| Audit uỷ quyền | `.claude/dev/packet_loop.py` đường `human_audit_transition.v1` (ngoại lệ thời điểm cho candidate lịch sử của `ADR-0063`) | giữ: quyết định 3 không đổi ngoại lệ ấy |
| Tự merge | `ADR-0060` M7, M8 và câu *"agent không tự approve hay merge"*; protocol §8 câu *"Human Land Approver …"*; protocol §13 mục `land-packets`; `.claude/dev/packet_loop.py` `kiem-dong-wp` D1 (`duyet_chu_kho`), `ghi-uy-quyen`, `doi-chieu-uy-quyen`; `.claude/skills/land-packets/SKILL.md` (frontmatter `disable-model-invocation`, câu *"KHÔNG tự trigger"*); .agents/skills/land-packets/SKILL.md (câu về chặn tự kích hoạt) | đổi, ở packet làm tự merge, theo các câu ở mục *Thay những gì* |
| Huỷ lượt bằng mục sổ | `.claude/dev/packet_loop.py` `void-attempt` (`--ai-cho-phep`) | đổi, ở packet đổi cổng `void-attempt` |
| Push thêm; checkpoint P3 | protocol §12 bất biến (b); `ADR-0060` M1 vế checkpoint, M5 | đổi ngay khi ADR này land, theo mục *Thay những gì* |

Giữ, không thuộc cơ chế nào: `nang-tran` và `record-rescue` (nâng trần vẫn là câu trả lời E2 của chủ kho); mọi chỗ nói về
chạy hay miễn `full_mutant_audit` (K7; `ADR-0060` M9 và mục *Cưỡng chế* của nó; `.claude/skills/land-packets/SKILL.md`),
vì miễn mutant vẫn là câu trả lời E2 của chủ kho; `chu-kho-duyet` (nhánh `ADR-0054` đã đóng băng bởi `ADR-0062`); định nghĩa `NGUOI_CO_THAM_QUYEN`, `CHU_KHO`,
chú thích quanh chúng và hai hàm trợ giúp `_dong_chu_kho`, `_owner_record` (xếp theo nơi gọi; sửa chính danh sách là E5);
câu về R01–R20 của #523 ở protocol §8.3 (lịch sử một mission).

## Cưỡng chế

Đo lúc land trên base của lease, một dòng cho từng vị trí cổng mà §20 của protocol liệt kê:

- `ops/lease_publish.py`: `git show <base>:ops/lease_publish.py | grep -c 'ADR-0067'` ⇒ `0`, tệp đọc được `2604` dòng.
- `.claude/dev/packet_loop.py`: `git show <base>:.claude/dev/packet_loop.py | grep -c 'ADR-0067'` ⇒ `0`, tệp đọc được `6247` dòng.
- `.claude/dev/launcher.py`: `git show <base>:.claude/dev/launcher.py | grep -c 'ADR-0067'` ⇒ `0`, tệp đọc được `5988` dòng.
- `.claude/dev/gate_lifecycle.py`: `git show <base>:.claude/dev/gate_lifecycle.py | grep -c 'ADR-0067'` ⇒ `0`, tệp đọc được `1688` dòng.
- `.github/workflows/ci.yml`: `git show <base>:.github/workflows/ci.yml | grep -c 'ADR-0067'` ⇒ `0`, tệp đọc được `1184` dòng.
- `.github/workflows/ops-publish-lease.yml`: `git show <base>:.github/workflows/ops-publish-lease.yml | grep -c 'ADR-0067'` ⇒ `0`, tệp đọc được `277` dòng.

Phép quét chỗ tiêu thụ, chạy trên base của lease:
`git grep -n -e NGUOI_CO_THAM_QUYEN -e CHU_KHO -e _dong_chu_kho -e _owner_record -e duyet_chu_kho <base> -- .claude/dev/packet_loop.py ops/lease_publish.py ops/bien_nhan_v2.py`
và `git grep -n -e "chủ kho miễn" -e "chủ kho quyết" -e "checkpoint chủ kho" -e "Chủ kho duyệt" -e "lần duyệt của chủ kho" -e "granted-by" -e full_mutant_audit -e "Land Approver" -e "tự trigger" -e "user-invoked" -e "không tự approve" -e "tự kích hoạt" <base> -- docs/PROTOCOL_DA_PHIEN.md docs/adr/0060-dieu-kien-merge-va-moc-ready.md .claude/skills .agents/skills`.
Phép quét theo từ khoá không bắt được mọi nghĩa vụ (một câu có thể ngắt dòng hay nói bằng chữ khác); nó là một phép kiểm
tối thiểu, và bảng ở mục trên là sàn.

Lúc land, danh sách đóng sống bằng kỷ luật đọc: không cổng nào đọc ADR này. Cổng đọc nó là việc của các packet đổi cổng
ở bảng chuyển tiếp, và packet đầu tiên trong số ấy sửa dòng `ADR-0067` ở §20.

## Phương án bị loại

- Giữ mặc định *"chưa được phép thì hỏi"*: chính nó sinh 391 quyết định trong 31 ngày.
- Danh sách cấm điểm hỏi thay cho danh sách đóng: danh sách cấm phải đoán trước mọi cách hỏi mới, nên luôn thiếu.
- Sổ quyết định là tệp trong kho: mỗi mục một PR, va làn sổ sách của `ADR-0060` M8; comment có URL ổn định để lease và
  `record-rescue` trỏ vào.
- Bản tin qua email: không nằm trong control plane GitHub, không đọc lại được bằng cùng công cụ.
- Uỷ quyền thường trực không hạn: một uỷ quyền quên thu hồi sống mãi; hạn 30 ngày buộc chủ kho nhìn lại.

## Giới hạn

- Audit uỷ quyền độc lập về ngữ cảnh nhưng cùng họ model với executor khi cả hai là Claude; chưa có họ model thứ ba dùng
  được trong kho.
- Danh tính chưa tách: phiên agent chạy bằng credential của chủ kho, nên mọi chốt theo tên tác giả chỉ là chốt theo nhãn.
- Ước lượng 220 trong 273 chưa đo trên việc thật; đo lại sau khi các packet đổi cổng land.
