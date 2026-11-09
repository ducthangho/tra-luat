# GIAM-HOI-P2-ADR-E1-E5 r9 — ADR-0067 danh sách đóng E1–E5 và uỷ quyền thường trực; protocol §2, §12, §13, §20; skill soan-spec trỏ về ADR

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet_id | `GIAM-HOI-P2-ADR-E1-E5`, revision 9, generation 1. Lease khai đúng `packet_id: GIAM-HOI-P2-ADR-E1-E5` và `revision: 9`: tiêu đề H1 của tệp này là khai báo định danh theo grammar của `ADR-0063` (mục 11). Thay r8 (sha256 `03aafa50f8f70edd28722cd831f943859181871da4826e22734bebd840e1a05a`, được review lượt 7 approve, 0 finding, và được chủ kho duyệt băm ngày 08-11-2026 trên #1292; lời duyệt ấy neo băm r8 nên không chuyển sang bản này), r7 (sha256 `1eb538c3324065fc311d9363830c3d83fa2ea368a642bdffed78655c40148641`, được review lượt 6 approve kèm một P3), r6 (chưa review), r5 (sha256 `359dc5a9b602aed5514708a7b4bb8beb4f61377dc82007aee9e9b20e9f5c149d`, được review lượt 5 approve kèm hai P3), r4 (sha256 `078ec9d4286766f1d746a9db3b6b6ab0272726fb1f8243711ec18d1d50c387a0`), r3 (sha256 `2e78f63a54f49658e3c3b1c27204571e4519ec8335bc4c11497d7cf11e9cf2d0`), r2 (sha256 `15743c0056b2acb225d8dc8f0a236c4418fcda69d04cab46664df9bb75e4cc01`) và r1 (sha256 `7c74666df58dc57ca854f18091d9b4a1181f694d93f3dd4db117365b01d05aa2`), bảy bản này không được chủ kho duyệt; thay đổi ở mục 12 tới 19 |
| packet_issue | #1292 (tạo ngày 08-11-2026 cho r8). Comment duyệt băm của chủ kho trên Issue trỏ đặc tả; thân Issue đổi sang trỏ bản này sau khi chủ kho duyệt băm nó. Số Issue trong dòng Trạng thái của ADR lấy từ comment duyệt băm bản này |
| mission | lộ trình "Giảm việc hỏi chủ kho", packet 2/5. Chưa có Mission Issue |
| nguon_cap_viec | Chủ kho đồng ý cả năm khuyến nghị ở cột *Quyết định* của tài liệu https://claude.ai/artifact/6JUF8DsbHxfN5GjsbdAtHT ("Giảm việc hỏi chủ kho") trong phiên chat ngày 08-11-2026, nguyên văn: *"Bạn làm hộ cho tôi luôn. TÔi đồng ý duyệt 5 điểm và chốt nâng trần theo đề xuất"*. Packet này là mục 2 của phần *Lộ trình*. Bảng *Việc agent làm hộ, và chốt an toàn của từng việc* của tài liệu là phần chủ kho đã đọc khi duyệt; con số *"khoảng 220 trong 273 quyết định có loại rõ ràng sẽ không cần bạn nữa"* ở phần *Tóm tắt* chỉ đúng khi các dòng của bảng ấy cũng đổi theo. Ở những chỗ bảng ấy để ngỏ, ADR chọn hướng **không lỏng hơn** luật hiện hành (mục 10) |
| review_class | `sensitive`. Bộ phân lớp `ops/lease_publish.py` (`_BANG_LOP` dòng 59–67) trả `sensitive` cho mọi đường dẫn không có trong bảng |
| base | `origin/master` lúc cấp lease, và phải chứa commit land của `GIAM-HOI-P1-SOAN-SPEC` r6. Soạn trên `e3c639be40dba644ecbf9d729d72837691f59ff4` cộng ứng viên packet 1 dựng từ đặc tả của nó; các tệp neo không đổi tới `origin/master` `0166d30` (đo 14:0xZ 08-11-2026) |
| depends_on | `GIAM-HOI-P1-SOAN-SPEC` r6: các khối `cu` của `SKILL.md` ở §2 là văn bản packet ấy viết ra |
| executor | `codex`: Codex CLI, identity `openai_codex / codex_cli / machine`, họ model `openai`, theo chỉ đạo chủ kho ngày 08-11-2026 (UTC), nguyên văn: *"Đổi agy sang codex. Executor và reviewer đều là codex. Reviewer có koo hình hoặc nỗ lực cao hơn và có thể chạy ở máy khác"*. Model yêu cầu `gpt-6-astra`, effort `high`; model và effort thực phục vụ lấy từ biên nhận của lượt chạy, không suy từ cấu hình. Môi trường `local`. Adapter `.agents/skills/work-packet/SKILL.md`. Packet không dùng state của `.claude/dev/packet_loop.py` (`init`, `record-lease`, `begin-attempt`, `record-review`, `transition`): `init` chỉ nhận reviewer là một model provider khác họ executor (dòng 776), còn reviewer có thẩm quyền của packet này là chủ kho (hàng dưới). Không ghi tay state, không gọi `init` với reviewer khai sai |
| reviewer | `human`: chủ kho `ducthangho`, assurance `human_audited` (protocol §8); lease khai `reviewer: human` và `assurance_target: human_audited`. Chủ kho tự audit SHA ứng viên cục bộ H **trước khi H được đẩy** (`ADR-0060` M5, M12) bằng comment của chính mình trên Packet Issue, neo `reviewed_sha` (H), `reviewed_tree`, `spec_sha256` của tệp này, `verdict` và `open_findings`; comment do agent đăng hộ không phải audit (`ADR-0063`). Trước audit có một lượt phản biện bổ sung: Codex offline qua `.claude/dev/launcher.py run` trên H, phiên mới, read-only, không fork context của executor, model hoặc effort cao hơn lượt thi công (yêu cầu `gpt-6-astra` effort `xhigh`), chạy ở máy khác máy thi công khi có. Mức của lượt ấy là `same_provider_approved`, một mình không đủ cho lớp `sensitive`, nhưng verdict của nó vẫn chặn: M1 của `ADR-0060` xét trên verdict ấy, chủ kho chỉ audit H mà lượt ấy đã approve, và biên nhận của nó (`run.json`, stdout) là đầu vào K4 đường model của `kiem-merge`. Cộng connector `@codex review` trên PR draft (`ADR-0060` M6) |
| luật merge | `ADR-0060`, mặc định theo `ADR-0062` |
| windows | `not_required`: mọi tệp của diff là `*.md` (`ADR-0060` M3 bước 3) |
| full_mutant_audit | không áp: diff không chạm `.claude/dev/**`, `ops/**/*.py`, `.github/workflows/**` (`ADR-0060` M9) |
| pham_vi_e | **chạm E5**: packet tạo chính danh sách đóng và các uỷ quyền. Chủ kho duyệt băm, audit trên exact head và duyệt merge một lần neo SHA, theo cả luật hiện hành lẫn ADR này. Không chạm E4 |

## 1. Vì sao — số đo

Đo trên `origin/master` `e3c639b` lúc 10:30Z 08-11-2026, trừ chỗ ghi khác.

| # | sự kiện | số đo |
|---|---|---|
| S1 | số quyết định của chủ kho | Tài liệu nguồn, đo 07-11-2026 bằng `gh api` trên Issue/PR: 391 comment quyết định trong 31 ngày (08-10 → 07-11-2026), 226 trong số đó là agent ghi hộ; 253 lần đăng lease, lần nào cũng `granted_by: ducthangho`. Không đo lại ở phiên này |
| S2 | điểm hỏi do mã đòi | `NGUOI_CO_THAM_QUYEN = ("ducthangho",)` ở `.claude/dev/packet_loop.py:157` và `ops/lease_publish.py:274`. `ops/lease_publish.py:1058` từ chối `granted_by` ngoài danh sách. Trong `packet_loop.py`: `record-lease` (dòng 920), `void-attempt --khong-co-bang-chung` (dòng 1078; lý do `quota`, `rate_limit` không có đường bằng chứng máy, dòng 172–173), `nang-tran` (dòng 1318), `record-rescue` (dòng 1337), `ghi-uy-quyen` (dòng 1462); `kiem-merge` đòi dòng của chủ kho cho P3 còn mở (K5, dòng 3402), Windows `unknown` (K6, dòng 3408–3410), miễn mutant (K7, dòng 3418–3426); K4 human audit chỉ nhận comment của owner `ducthangho` (`ADR-0063`) |
| S3 | điểm hỏi chỉ sống trong văn bản | `ADR-0060` M5 *"Mỗi lần push thêm cần checkpoint chủ kho"* và protocol §12 bất biến (b): `kiem-merge` không có phép kiểm số lần push nào (`rg -n "push" .claude/dev/packet_loop.py`). Duyệt băm đặc tả: không điều nào của protocol bắt, là thói quen của skill `soan-spec` |
| S4 | số ADR kế tiếp | `ADR-0066` đã được packet #1265 giữ chỗ (143 lần nhắc trên `master`; chưa nhánh nào có `docs/adr/0066-*`). Không nhánh nào trong 748 nhánh máy chủ có `docs/adr/0067-*` hay `docs/adr/007*` (đo 11:38Z, `git ls-tree` trên từng ref sau khi fetch đủ); 0 lần nhắc `ADR-0067` trên `master` |
| S5 | người đang giữ write set | `ai-dang-giu` trên clone đủ nhánh máy chủ: `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` 0 người giữ (11:28Z); `.claude/skills/soan-spec/SKILL.md` 0 người giữ; `docs/PROTOCOL_DA_PHIEN.md` `NGƯỜI_GIỮ 1: wp1174-r17-g14-codex` (`lease_until` 18:03:01Z 08-11-2026). Lease của packet này chỉ cấp được khi cả ba ra 0 người giữ, và sau khi packet 1 land |
| S6 | adapter có nhắc thẩm quyền chủ kho | Quét `.claude/skills/{work-packet,cross-review,land-packets}/SKILL.md` và `.agents/skills/*/SKILL.md` trên `origin/master` `0166d30` (14:0xZ) theo `chủ kho`, `ducthangho`, `owner`, `mien`, `human audit`, `nang_tran`, `granted_by`, `disable-model-invocation`, `tự trigger`, `approval`: ngoài đường `gh api graphql` (thiếu quyền GraphQL, tức E2) có ba chỗ — `.claude/skills/work-packet/SKILL.md:159` (`--granted-by ducthangho` khi ghi lease), `.claude/skills/land-packets/SKILL.md:5,10` (`disable-model-invocation: true`, *"KHÔNG tự trigger"*), `.claude/skills/land-packets/SKILL.md:64` (dòng `full_mutant_audit: <head> mien` của chủ kho). Cả ba vẫn đúng sau packet này (mục 7). Bộ từ khoá của phép quét này không bắt được `.agents/skills/land-packets/SKILL.md:12` (câu về chặn tự kích hoạt, trỏ điều kiện gọi về §13); phép quét mở rộng ở mục *Cưỡng chế* của ADR bắt được nó, và bảng chỗ tiêu thụ xếp nó vào hàng *Tự merge* |
| S8 | chỗ tiêu thụ quyền chủ kho | Hai lệnh `git grep` in ở mục *Cưỡng chế* của ADR, chạy trên `bf9914c`: lệnh 1 ra 36 hit, lệnh 2 ra 23 hit (đo sau verdict lượt 4). Mỗi hit thuộc một hàng của mục *Chỗ tiêu thụ phải đổi theo* hay câu *"Giữ, không thuộc cơ chế nào"* ngay dưới nó; bảng đối chiếu từng hit ở biên nhận review đặc tả. Phép quét là phép kiểm tối thiểu: ba nghĩa vụ mà lượt 4 tìm ra (I01) không khớp từ khoá nào của bản r4, nên bảng là sàn và packet đổi cổng phải lập lại (mục 14, 15) |
| S7 | `CONTEXT.md` | nằm trong `RELEASE_MANIFEST.json` (184 mục). Dòng 42 nói *"Executor có thể kiêm Land Operator nhưng không nhờ đó trở thành Reviewer hay Approver của code mình"*, khớp quyết định 4 của ADR. Thêm từ vựng mới vào đó buộc phiên land tái sinh manifest; xem `ngoai_pham_vi` |

## 2. Thay đổi

### M1 → `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` (tệp mới)

Tệp ADR bằng **đúng từng byte** khối `adr` dưới đây, trừ ba loại chỗ trống:

- `{{TRANG_THAI}}` (dòng 3) thay bằng đúng một dòng dạng
  ``- **Trạng thái:** Accepted (<YYYY-MM-DD>, chủ kho `ducthangho` duyệt `spec_hash` `<64 hex>` của đặc tả `GIAM-HOI-P2-ADR-E1-E5` r9 trên Issue #<N>: <URL>)``,
  trong đó ngày là ngày land, `<64 hex>` là sha256 của chính tệp đặc tả này, `<N>` là số Issue của packet và `<URL>` là
  URL comment duyệt băm của chủ kho trên Issue ấy (`https://github.com/ducthangho/tra-luat/issues/<N>#issuecomment-<id>`).
- `{{SO}}` và `{{DONG}}` ở mục *Cưỡng chế*: số dòng chứa `ADR-0067` và số dòng (đếm ký tự xuống dòng) của tệp cổng ấy
  trên base của lease, đo bằng đúng lệnh in trên dòng.

~~~ adr
# ADR-0067 — Danh sách đóng E1–E5 cho việc hỏi chủ kho, và uỷ quyền thường trực

{{TRANG_THAI}}

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
| Tự merge | `ADR-0060` M7, M8 và câu *"agent không tự approve hay merge"*; protocol §8 câu *"Human Land Approver …"*; protocol §13 mục `land-packets`; `.claude/dev/packet_loop.py` `kiem-dong-wp` D1 (`duyet_chu_kho`), `ghi-uy-quyen`, `doi-chieu-uy-quyen`; `.claude/skills/land-packets/SKILL.md` (frontmatter `disable-model-invocation`, câu *"KHÔNG tự trigger"*); `.agents/skills/land-packets/SKILL.md` (câu về chặn tự kích hoạt) | đổi, ở packet làm tự merge, theo các câu ở mục *Thay những gì* |
| Huỷ lượt bằng mục sổ | `.claude/dev/packet_loop.py` `void-attempt` (`--ai-cho-phep`) | đổi, ở packet đổi cổng `void-attempt` |
| Push thêm; checkpoint P3 | protocol §12 bất biến (b); `ADR-0060` M1 vế checkpoint, M5 | đổi ngay khi ADR này land, theo mục *Thay những gì* |

Giữ, không thuộc cơ chế nào: `nang-tran` và `record-rescue` (nâng trần vẫn là câu trả lời E2 của chủ kho); mọi chỗ nói về
chạy hay miễn `full_mutant_audit` (K7; `ADR-0060` M9 và mục *Cưỡng chế* của nó; `.claude/skills/land-packets/SKILL.md`),
vì miễn mutant vẫn là câu trả lời E2 của chủ kho; `chu-kho-duyet` (nhánh `ADR-0054` đã đóng băng bởi `ADR-0062`); định nghĩa `NGUOI_CO_THAM_QUYEN`, `CHU_KHO`,
chú thích quanh chúng và hai hàm trợ giúp `_dong_chu_kho`, `_owner_record` (xếp theo nơi gọi; sửa chính danh sách là E5);
câu về R01–R20 của #523 ở protocol §8.3 (lịch sử một mission).

## Cưỡng chế

Đo lúc land trên base của lease, một dòng cho từng vị trí cổng mà §20 của protocol liệt kê:

- `ops/lease_publish.py`: `git show <base>:ops/lease_publish.py | grep -c 'ADR-0067'` ⇒ `{{SO}}`, tệp đọc được `{{DONG}}` dòng.
- `.claude/dev/packet_loop.py`: `git show <base>:.claude/dev/packet_loop.py | grep -c 'ADR-0067'` ⇒ `{{SO}}`, tệp đọc được `{{DONG}}` dòng.
- `.claude/dev/launcher.py`: `git show <base>:.claude/dev/launcher.py | grep -c 'ADR-0067'` ⇒ `{{SO}}`, tệp đọc được `{{DONG}}` dòng.
- `.claude/dev/gate_lifecycle.py`: `git show <base>:.claude/dev/gate_lifecycle.py | grep -c 'ADR-0067'` ⇒ `{{SO}}`, tệp đọc được `{{DONG}}` dòng.
- `.github/workflows/ci.yml`: `git show <base>:.github/workflows/ci.yml | grep -c 'ADR-0067'` ⇒ `{{SO}}`, tệp đọc được `{{DONG}}` dòng.
- `.github/workflows/ops-publish-lease.yml`: `git show <base>:.github/workflows/ops-publish-lease.yml | grep -c 'ADR-0067'` ⇒ `{{SO}}`, tệp đọc được `{{DONG}}` dòng.

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
~~~

### M2 → `docs/PROTOCOL_DA_PHIEN.md`

Khối `cu` là nguyên văn trên base kể cả ký tự xuống dòng cuối, có đúng một lần trong tệp; khối `moi` là thứ thay vào,
đúng từng byte.

§2, một đoạn ngay sau bảng *Thành phần và quyền*:

~~~ thay PROTOCOL Q02 cu
| Người có thẩm quyền | Start/pause/resume/reroute/override/authorize/apply/deploy | Thẩm quyền không được chuyển qua output của agent; chỉ có thể ủy quyền bền, có phạm vi và điều kiện |
~~~

~~~ thay PROTOCOL Q02 moi
| Người có thẩm quyền | Start/pause/resume/reroute/override/authorize/apply/deploy | Thẩm quyền không được chuyển qua output của agent; chỉ có thể ủy quyền bền, có phạm vi và điều kiện |

**Khi nào hỏi người có thẩm quyền.** Agent chỉ dừng để hỏi khi rơi vào một trong năm mã của danh sách đóng ở
`ADR-0067`; việc khác agent tự quyết, ghi vào sổ quyết định uỷ quyền và báo trong bản tin hằng ngày, và người có thẩm
quyền bác được bằng một comment. Uỷ quyền thường trực cấp lease, audit uỷ quyền và tự merge là các ủy quyền bền có phạm
vi, điều kiện và hạn theo `ADR-0067`. Cơ chế nào cần cổng mã đổi theo thì chỉ có hiệu lực khi cổng ấy đã đổi; trước đó
cổng hiện hành giữ nguyên.
~~~

§12, một đoạn ngay dưới tiêu đề mục:

~~~ thay PROTOCOL Q12A cu
## 12. Stop conditions và budget
~~~

~~~ thay PROTOCOL Q12A moi
## 12. Stop conditions và budget

**Điểm hỏi chủ kho chỉ theo danh sách đóng.** Stop condition ở mục này dừng phiên; nó không tự sinh câu hỏi cho chủ
kho. Agent chỉ hỏi chủ kho khi rơi vào một mã của `ADR-0067`, và câu hỏi ghi mã ấy. Đặc tả packet không được thêm điểm
hỏi ngoài năm mã. Một cổng mã hiện hành còn đòi quyền chỉ chủ kho có thì câu hỏi ấy mang mã E2 cho tới khi packet đổi
cổng ấy land, theo bảng chuyển tiếp của `ADR-0067`.
~~~

§12 bất biến (b): push thêm không còn cần checkpoint chủ kho.

~~~ thay PROTOCOL Q12B cu
**Bất biến (b) — push thêm vì CI đỏ.** Chỉ được sửa CI, không mang bản vá finding review. SHA mới phải review offline approve và chạy lại (a) trước push; ghi SHA trước/sau, check đỏ và nguyên nhân vào biên nhận. Mọi push thêm vẫn cần checkpoint chủ kho và chịu trần ADR-0060 M5. Nguồn ADR-0054 §1, ADR-0062.
~~~

~~~ thay PROTOCOL Q12B moi
**Bất biến (b) — push thêm vì CI đỏ.** Chỉ được sửa CI, không mang bản vá finding review. SHA mới phải review offline approve và chạy lại (a) trước push; ghi SHA trước/sau, check đỏ và nguyên nhân vào biên nhận. Push thêm không cần checkpoint chủ kho (`ADR-0067`) và chịu trần số lần của ADR-0060 M5; chạm trần ấy là E2. Nguồn ADR-0054 §1, ADR-0062, ADR-0067.
~~~

§12, một đoạn sau đoạn về lớp xuất hiện ở ba lượt review:

~~~ thay PROTOCOL Q12C cu
Một lớp xuất hiện ở ba lượt review khác nhau đòi xem lại cách làm tại checkpoint;
ba biểu hiện của lớp trong cùng một lượt chỉ là một lần xuất hiện. Revision/scope
cut không reset lịch sử đó, không tự cấp thêm review call hoặc attempt.
~~~

~~~ thay PROTOCOL Q12C moi
Một lớp xuất hiện ở ba lượt review khác nhau đòi xem lại cách làm tại checkpoint;
ba biểu hiện của lớp trong cùng một lượt chỉ là một lần xuất hiện. Revision/scope
cut không reset lịch sử đó, không tự cấp thêm review call hoặc attempt.

Checkpoint vì tín hiệu không hội tụ, hay vì một lớp hoặc một hình dạng lỗi lặp lần thứ ba, là điểm dừng của phiên,
không phải điểm hỏi chủ kho. Phiên đang giữ việc dừng vá và xét lại cách làm; lý do của hướng mới đi vào revision kế
tiếp hay handoff. Phiên chỉ hỏi chủ kho khi rơi vào E1 hay E3 của `ADR-0067`.
~~~

§12, câu cuối của đoạn Review Rescue Checkpoint:

~~~ thay PROTOCOL Q12D cu
không tự biến Packet thành thất bại nội dung và không cho phép gọi thêm bằng prompt/phiên khác để lách trần.
~~~

~~~ thay PROTOCOL Q12D moi
không tự biến Packet thành thất bại nội dung và không cho phép gọi thêm bằng prompt/phiên khác để lách trần.
Chạm hai trần này mà cần thêm lời gọi hay vòng là E2 của `ADR-0067`.
~~~

§13 `work-packet`:

~~~ thay PROTOCOL Q13A cu
Trigger khi agent nhận Issue có lease hợp lệ. Trình tự bắt buộc: đọc protocol → preflight spec/lease/worktree → heartbeat → chỉ sửa effective write set → worker gate → handoff → review offline → đẩy → PR theo ADR-0060. Hoàn tất khi SHA được approve đã đẩy và PR mở ở trạng thái `draft`; run kết thúc trước đó thì run kế nhiệm làm nốt.
~~~

~~~ thay PROTOCOL Q13A moi
Trigger khi agent nhận Issue có lease hợp lệ. Trình tự bắt buộc: đọc protocol → preflight spec/lease/worktree → heartbeat → chỉ sửa effective write set → worker gate → handoff → review offline → đẩy → PR theo ADR-0060. Hoàn tất khi SHA được approve đã đẩy và PR mở ở trạng thái `draft`; run kết thúc trước đó thì run kế nhiệm làm nốt.
Quyết định phiên tự đưa thay cho một câu hỏi trước đây (nợ P3, huỷ lượt vì hạ tầng, xét lại cách làm…) ghi vào sổ quyết định uỷ quyền theo `ADR-0067`.
~~~

§13 `land-packets`:

~~~ thay PROTOCOL Q13B cu
Phiên land chỉ nhận authorization bền cho exact SHA. Adapter không tự cấp approval; Land Operator ghi merge,
~~~

~~~ thay PROTOCOL Q13B moi
Phiên land chỉ nhận authorization bền cho exact SHA. Với packet không chạm E4, E5, khi cơ chế tự merge của `ADR-0067`
đã có hiệu lực, authorization ấy là mục sổ `tu_merge` của ADR ấy: neo exact SHA, mang đủ các ràng buộc ở §13.1, kèm review
approve, audit uỷ quyền đạt và đủ điều kiện `ADR-0060`. Adapter không tự cấp approval; Land Operator ghi merge,
~~~

§20 bảng A, một dòng cuối bảng (neo vào tiêu đề mục B ngay sau bảng, nên vẫn đúng khi dòng `ADR-0066` land trước):

~~~ thay PROTOCOL Q20 cu

### B. ADR ngoài phạm vi protocol — thuộc `scripts/tl.py` và đường phát hành
~~~

~~~ thay PROTOCOL Q20 moi
| `ADR-0067` | Danh sách đóng E1–E5: agent chỉ hỏi chủ kho trong năm tình huống; đóng băng đặc tả sau review độc lập, audit uỷ quyền, tự merge packet không chạm E4/E5, uỷ quyền thường trực cấp lease có hạn; sổ quyết định uỷ quyền, bản tin hằng ngày, comment ghi hộ có nhãn | Accepted — cơ chế cần cổng mã có hiệu lực khi cổng ấy đổi (bảng chuyển tiếp trong ADR) | **0 cổng**; đo lúc land trên sáu vị trí cổng (mục Cưỡng chế của ADR) |

### B. ADR ngoài phạm vi protocol — thuộc `scripts/tl.py` và đường phát hành
~~~

### M3 → `.claude/skills/soan-spec/SKILL.md`

L7 thôi chép định nghĩa E1–E3, trỏ về `ADR-0067`, và thêm mục `pham_vi_e` cùng luật đóng băng đặc tả của quyết định số 2.

~~~ thay SKILL K7 cu
**L7 — Đặc tả không tự đặt điểm hỏi chủ kho.** Một mẫu đã lan từ đặc tả này sang đặc tả khác mà
không ADR, protocol hay skill nào đặt ra: "ngân sách mềm N lời gọi; hai lượt liên tiếp chưa approve ⇒
Review Rescue Checkpoint". Đo 08-11-2026 trên `origin/master` `e3c639b`, đếm tệp trong 581 tệp của
`ops/specs/`: 26 tệp có cụm "liên tiếp chưa approve", 173 tệp có cụm "hỏi chủ kho" (kể cả câu phủ
định). Mỗi điểm hỏi tự đặt là một lần chủ kho phải dừng việc để trả lời.

- **Không khai ngân sách mềm** dưới trần của dòng khai, và không đặt luật kiểu "N lượt liên tiếp chưa
  approve thì dừng hay hỏi chủ kho". Mức dành sẵn của `ADR-0041` là ngân sách giữ trước, không phải
  trần hay điểm dừng. Lượt thứ hai trở đi theo điều kiện của `ADR-0052` và không cần hỏi ai.
- **Mục `luat_dung` chỉ có hai loại dòng.** (i) Điểm dừng mà protocol hay một ADR đang hiệu lực đã
  đặt: dẫn bằng tên mục hay ADR, không chép lại, không hạ ngưỡng. (ii) Một trong ba mã dưới đây, kèm
  thứ phải mang theo khi hỏi:
  - **E1 — hướng đi bế tắc:** đã xét lại cách làm mà không còn phương án nào có phép đo chống đỡ.
    Mang theo gốc rễ, các phương án đã thử và vì sao hỏng, một đề xuất.
  - **E2 — thiếu tài nguyên:** chạm trần cứng, hoặc thiếu máy, quota hay quyền. Mang theo mức đã
    dùng, còn thiếu bao nhiêu, để làm gì.
  - **E3 — phát hiện đảo ngược chỉ đạo:** bằng chứng mâu thuẫn với một quyết định của chủ kho. Mang
    theo quyết định nào, bằng chứng, hậu quả nếu giữ nguyên.
- **Câu nào trong đặc tả nói tới việc hỏi, báo hay chờ chủ kho thì phải mang một mã E.** Điểm dừng
  loại (i) chỉ dừng phiên; khi nó cần chủ kho quyết thì câu hỏi ấy cũng mang mã, thường là E2 vì quyền
  quyết thuộc chủ kho (chạm trần cứng, việc protocol giao chủ kho duyệt). Không gắn được mã nào thì đó
  không phải điểm hỏi: phiên đang giữ việc tự quyết, rồi ghi gốc rễ, phương án chọn và phép đo chống đỡ
  vào revision kế tiếp hay handoff.

Ba mã lấy từ chỉ đạo của chủ kho ngày 07-11-2026, được chủ kho đồng ý thành danh sách ngày 08-11-2026
(quyết định số 1 của tài liệu "Giảm việc hỏi chủ kho"). Khi ADR của danh sách đóng land, định nghĩa
chuyển về ADR ấy và mục này chỉ còn con trỏ.
~~~

~~~ thay SKILL K7 moi
**L7 — Đặc tả không tự đặt điểm hỏi chủ kho.** Một mẫu đã lan từ đặc tả này sang đặc tả khác mà
không ADR, protocol hay skill nào đặt ra: "ngân sách mềm N lời gọi; hai lượt liên tiếp chưa approve ⇒
Review Rescue Checkpoint". Đo 08-11-2026 trên `origin/master` `e3c639b`, đếm tệp trong 581 tệp của
`ops/specs/`: 26 tệp có cụm "liên tiếp chưa approve", 173 tệp có cụm "hỏi chủ kho" (kể cả câu phủ
định). Mỗi điểm hỏi tự đặt là một lần chủ kho phải dừng việc để trả lời. Danh sách những lần được
hỏi nằm ở `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md`; skill này không chép định nghĩa.

- **Không khai ngân sách mềm** dưới trần của dòng khai, và không đặt luật kiểu "N lượt liên tiếp chưa
  approve thì dừng hay hỏi chủ kho". Mức dành sẵn của `ADR-0041` là ngân sách giữ trước, không phải
  trần hay điểm dừng. Lượt thứ hai trở đi theo điều kiện của `ADR-0052` và không cần hỏi ai.
- **Mục `luat_dung` chỉ có hai loại dòng.** (i) Điểm dừng mà protocol hay một ADR đang hiệu lực đã
  đặt: dẫn bằng tên mục hay ADR, không chép lại, không hạ ngưỡng. (ii) Mã E1, E2 hay E3 của danh sách
  đóng, kèm thứ ADR ấy bắt mang theo khi hỏi.
- **Câu nào trong đặc tả nói tới việc hỏi, báo hay chờ chủ kho thì phải mang một mã E.** Điểm dừng
  loại (i) chỉ dừng phiên; khi nó cần chủ kho quyết thì câu hỏi ấy cũng mang mã, thường là E2 vì quyền
  quyết thuộc chủ kho (chạm trần cứng, việc protocol giao chủ kho duyệt). Không gắn được mã nào thì đó
  không phải điểm hỏi: phiên đang giữ việc tự quyết, rồi ghi gốc rễ, phương án chọn và phép đo chống đỡ
  vào revision kế tiếp hay handoff.
- **Mục `pham_vi_e` khai đặc tả có chạm E4, E5 không**, theo định nghĩa của ADR ấy; không rõ thì khai là
  chạm. Đặc tả của packet thuộc Mission chủ kho đã duyệt hướng, không chạm E4, E5 và không đảo quyết
  định nào của chủ kho, được người soạn đóng băng khi một review độc lập approve; đặc tả khác chờ chủ
  kho duyệt băm. Với packet như thế, vòng hỏi ở mục 1 lấy câu trả lời từ các quyết định Mission đã ghi;
  câu không trả lời được từ đó mà cũng không thuộc mã E nào thì người soạn tự quyết và ghi vào sổ quyết
  định uỷ quyền. Cho đúng loại packet ấy, luật này thắng hai câu của mục 1, "Quyết định thì luôn là của
  người dùng" và "Không hành động cho tới khi người dùng xác nhận đã hiểu giống nhau": thứ thay cho lần
  xác nhận là review độc lập approve.
~~~

~~~ thay SKILL K4 cu
| `luat_dung` | điểm dừng của protocol hay ADR dẫn bằng tên, và mã E1–E3 theo L7; không có ngân sách mềm |
~~~

~~~ thay SKILL K4 moi
| `luat_dung` | điểm dừng của protocol hay ADR dẫn bằng tên, và mã E1–E3 theo L7; không có ngân sách mềm |
| `pham_vi_e` | chạm E4, chạm E5 hay không chạm, theo L7; không rõ thì khai là chạm |
~~~

## 3. Write set

```yaml
write_set:
  - .claude/skills/soan-spec/SKILL.md
  - docs/PROTOCOL_DA_PHIEN.md
  - docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md
```

Diff PR: đúng **3 tệp**. Đo trên ứng viên dựng từ các khối của mục 2 trên base packet 1: ADR mới 332 dòng; protocol
thêm 22, bớt 2; skill thêm 13, bớt 13; tổng thêm 367. Trần `ADR-0053` cho packet `sensitive`
(≤ 6 tệp, ≤ 450 dòng thêm): **đạt**. Ba tệp không nằm trong `RELEASE_MANIFEST.json`. Handoff đăng thành comment trên
Packet Issue. Không sửa `VERSION`, `CHANGELOG.md`, `changelog.d/`, `CONTEXT.md`.

## 4. Nghiệm thu

Vị từ có một dạng duy nhất là script dưới đây. Người đo chép nó ra thư mục tạm (không đưa vào kho), rồi chạy ở gốc một
clone không shallow của ứng viên, sau `git fetch origin`:

```
python kiem_p2.py ops/specs/GIAM-HOI-P2-ADR-E1-E5-r9.md <OID base>
```

`ops/specs/GIAM-HOI-P2-ADR-E1-E5-r9.md` là bản đặc tả đúng băm trong lease. Mã thoát: 0 ĐẠT, 1 ĐỎ, 3 KHÔNG ĐO ĐƯỢC.
KHÔNG ĐO ĐƯỢC không phải ĐẠT.

```python
# kiem_p2.py: vị từ nghiệm thu của GIAM-HOI-P2-ADR-E1-E5 r9.
# Ứng viên là commit HEAD của checkout hiện tại; base là đối số thứ hai.
import datetime
import hashlib
import re
import subprocess
import sys

TEP = {"SKILL": ".claude/skills/soan-spec/SKILL.md", "PROTOCOL": "docs/PROTOCOL_DA_PHIEN.md"}
ADR = "docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md"
CONG = ("ops/lease_publish.py", ".claude/dev/packet_loop.py", ".claude/dev/launcher.py",
        ".claude/dev/gate_lifecycle.py", ".github/workflows/ci.yml", ".github/workflows/ops-publish-lease.yml")
TRANG_THAI = (r"- \*\*Trạng thái:\*\* Accepted \(([0-9]{4}-[0-9]{2}-[0-9]{2}), chủ kho `ducthangho` duyệt "
              r"`spec_hash` `([0-9a-f]{64})` của đặc tả `GIAM-HOI-P2-ADR-E1-E5` r9 trên Issue #([1-9][0-9]*): "
              r"(https://github\.com/ducthangho/tra-luat/issues/([1-9][0-9]*)#issuecomment-[1-9][0-9]*)\)")


def git(*doi_so, rc_nhan=(0,)):
    p = subprocess.run(["git", *doi_so], capture_output=True)
    if p.returncode not in rc_nhan:
        loi = p.stderr.decode("utf-8", "replace").strip()
        raise LookupError(f"git {' '.join(doi_so)} rc={p.returncode}: {loi}")
    return p


def doc_tep(rev, duong):
    return git("show", f"{rev}:{duong}").stdout.decode("utf-8")


def co_tep(rev, duong):
    return git("cat-file", "-e", f"{rev}:{duong}", rc_nhan=(0, 1, 128)).returncode == 0


def cac_khoi(van_ban):
    """({(tệp, mã): {"cu", "moi"}}, khuôn ADR) từ các khối `~~~ thay ...` và `~~~ adr`."""
    thay, khuon, dang_mo, dem = {}, None, None, []
    for dong in van_ban.splitlines(keepends=True):
        if dang_mo is None:
            m = re.fullmatch(r"~~~ (?:thay (SKILL|PROTOCOL) (\S+) (cu|moi)|(adr))\n", dong)
            if m:
                dang_mo, dem = m, []
        elif dong == "~~~\n":
            noi_dung = "".join(dem)
            if dang_mo.group(4):
                if khuon is not None:
                    raise LookupError("khối adr trùng")
                khuon = noi_dung
            else:
                muc = thay.setdefault((dang_mo.group(1), dang_mo.group(2)), {})
                if dang_mo.group(3) in muc:
                    raise LookupError(f"khối thay trùng: {dang_mo.group(0).strip()}")
                muc[dang_mo.group(3)] = noi_dung
            dang_mo = None
        else:
            dem.append(dong)
    if dang_mo is not None or khuon is None or any(set(v) != {"cu", "moi"} for v in thay.values()):
        raise LookupError("khối bị hở, thiếu cặp cu/moi hay thiếu khối adr")
    return thay, khuon


def ky_vong(goc, cap):
    vi_tri = []
    for ma, v in cap:
        so_lan = goc.count(v["cu"])
        if so_lan != 1:
            raise LookupError(f"{ma}: khối cu có {so_lan} lần trên base, cần đúng 1")
        dau = goc.index(v["cu"])
        vi_tri.append((dau, dau + len(v["cu"]), v["moi"]))
    vi_tri.sort()
    for (_, cuoi, _), (dau_sau, _, _) in zip(vi_tri, vi_tri[1:]):
        if dau_sau < cuoi:
            raise LookupError("hai khối cu chồng nhau")
    phan, con_tro = [], 0
    for dau, cuoi, moi in vi_tri:
        phan += [goc[con_tro:dau], moi]
        con_tro = cuoi
    return "".join(phan) + goc[con_tro:]


def mau_adr(khuon):
    phan = re.split(r"(\{\{TRANG_THAI\}\}|\{\{SO\}\}|\{\{DONG\}\})", khuon)
    if phan.count("{{TRANG_THAI}}") != 1 or phan.count("{{SO}}") != len(CONG) or phan.count("{{DONG}}") != len(CONG):
        raise LookupError("khuôn ADR sai số chỗ trống")
    nhom = {"{{TRANG_THAI}}": TRANG_THAI, "{{SO}}": r"(0|[1-9][0-9]*)", "{{DONG}}": r"(0|[1-9][0-9]*)"}
    return re.compile("".join(nhom.get(p, re.escape(p)) for p in phan))


def so_dong_co(van_ban, chuoi):
    return sum(1 for d in van_ban.split("\n") if chuoi in d)


def main():
    duong_spec, base = sys.argv[1], sys.argv[2]
    try:
        with open(duong_spec, "rb") as f:
            byte_spec = f.read()
    except OSError as e:
        raise LookupError(f"không đọc được tệp đặc tả: {e}") from None
    if b"\r" in byte_spec:
        raise LookupError("đặc tả có ký tự CR; K1 của ADR-0063 chỉ nhận LF")
    thay, khuon = cac_khoi(byte_spec.decode("utf-8"))
    if git("rev-parse", "--is-shallow-repository").stdout.strip() != b"false":
        raise LookupError("clone shallow")
    loi = []
    for ten, duong in TEP.items():
        cap = sorted((ma, v) for (t, ma), v in thay.items() if t == ten)
        if not cap:
            raise LookupError(f"không có khối nào cho {ten}")
        if doc_tep("HEAD", duong) != ky_vong(doc_tep(base, duong), cap):
            loi.append(f"{duong} khác bản kỳ vọng dựng từ base")
    doi = set(git("diff", "--name-only", base, "HEAD").stdout.decode("utf-8").split())
    if doi != set(TEP.values()) | {ADR}:
        loi.append(f"tập tệp đổi {sorted(doi)} khác write set")
    if co_tep(base, ADR):
        loi.append(f"{ADR} đã có trên base")
    if not co_tep("HEAD", ADR):
        loi.append(f"{ADR} chưa có ở ứng viên")
    else:
        m = mau_adr(khuon).fullmatch(doc_tep("HEAD", ADR))
        if not m:
            loi.append(f"{ADR} khác khuôn của đặc tả")
        else:
            ngay, sha_spec, issue, _, issue_url = m.groups()[:5]
            try:
                datetime.date.fromisoformat(ngay)
            except ValueError:
                loi.append(f"ngày {ngay!r} không hợp lệ")
            if sha_spec != hashlib.sha256(byte_spec).hexdigest():
                loi.append("spec_hash ở dòng Trạng thái khác sha256 của đặc tả")
            if issue != issue_url:
                loi.append("số Issue ở dòng Trạng thái khác số Issue trong URL")
            so = m.groups()[5:]
            for tep, so_nhac, so_dong in zip(CONG, so[0::2], so[1::2]):
                goc = doc_tep(base, tep)
                if int(so_nhac) != so_dong_co(goc, "ADR-0067") or int(so_dong) != goc.count("\n"):
                    loi.append(f"dòng Cưỡng chế của {tep} khác phép đo trên base")
    for tep in CONG:
        if so_dong_co(doc_tep("HEAD", tep), "ADR-0067"):
            loi.append(f"{tep} có nhắc ADR-0067 ở ứng viên, lời khai 0 cổng sai")
    for x in loi:
        print("ĐỎ:", x)
    print("ĐẠT" if not loi else f"ĐỎ: {len(loi)} lỗi")
    return 1 if loi else 0


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    try:
        sys.exit(main())
    except (LookupError, IndexError, UnicodeDecodeError) as e:
        print("KHÔNG ĐO ĐƯỢC:", e)
        sys.exit(3)
```

| ID | mục tiêu | phép đo | đột biến làm ĐỎ |
|---|---|---|---|
| A1 | M2, M3 | `kiem_p2.py` rc 0: `PROTOCOL_DA_PHIEN.md` và `SKILL.md` ở ứng viên bằng đúng từng byte bản dựng từ base bằng các khối `thay` | trả một đoạn §12 về bản cũ; giữ câu *"Mọi push thêm vẫn cần checkpoint chủ kho"*; giữ L7 của packet 1; ngắt dòng lại một đoạn mới ⇒ rc 1. Ngắt dòng lại ĐỎ là cố ý: đặc tả quy định cả chỗ ngắt dòng, nên phép so cả tệp đúng byte thay cho phép khớp cụm sau khi nối dòng (L6 vế b) |
| A2 | M1 | cùng script: ADR vắng trên base, có ở ứng viên, và khớp trọn khuôn `adr` (mọi byte ngoài ba loại chỗ trống) | đổi một chữ bất kỳ trong ADR; xoá một hàng của bảng E hay bảng chuyển tiếp; thụt lề một hàng bảng; đổi hậu tố một ô hiệu lực; ngắt dòng lại một đoạn ⇒ rc 1 |
| A3 | M1 | cùng script: dòng Trạng thái có ngày hợp lệ, `spec_hash` bằng sha256 của đặc tả này, số Issue trong câu bằng số Issue trong URL | ngày `2026-13-01`; băm của r1; Issue #1 với URL của Issue #2 ⇒ rc 1 |
| A4 | M1 | cùng script: mỗi dòng Cưỡng chế ghi đúng số dòng chứa `ADR-0067` và số dòng của tệp cổng trên base; sáu tệp cổng ở ứng viên không nhắc `ADR-0067` | ghi `0` cho số dòng của tệp; lệch số dòng một đơn vị ⇒ rc 1 |
| A5 | phạm vi | cùng script: `git diff --name-only <base> HEAD` bằng đúng ba tệp | thêm `CONTEXT.md` ⇒ rc 1 |
| A6 | neo | cùng script: mỗi khối `cu` có đúng một lần trên base, không chồng nhau; tệp đặc tả LF thuần; clone không shallow | base thiếu commit land của packet 1 (khối `cu` K4, K7 vắng) ⇒ rc 3; bản đặc tả CRLF ⇒ rc 3; clone shallow ⇒ rc 3; đường dẫn đặc tả vắng hay là thư mục ⇒ rc 3 |
| A7 | bất biến | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `python .claude/dev/packet_loop.py adr-song --root .` rc 0 (ADR mới có dòng §20); `git diff --check <base> HEAD` rc 0 | xoá dòng `ADR-0067` khỏi §20 ⇒ `adr-song` rc 9; chép một đoạn protocol mới vào `SKILL.md` ⇒ `doctrine-scan` rc 6 |
| A8 | bất biến (a) §12 | trên đúng SHA sẽ đẩy: `python scripts/tl.py --selftest` ra N/N với hai số bằng nhau | — (canh bất biến) |

Chạy thử trên base (ứng viên = base packet 1): A1, A2, A5 ĐỎ, đúng màu "chưa làm"; A7 xanh sẵn. Bằng chứng chạy thử của
từng đột biến ghi ở biên nhận review đặc tả.

## 5. `luat_dung`

- (i) Trần lời gọi Codex review của PR thi công: mười, theo dòng khai ở đầu tệp. Chạm trần mà chưa approve ⇒ Review
  Rescue Checkpoint (`ADR-0037`); đó là E2.
- (i) Số lần push thêm và điều kiện merge: `ADR-0060` M5, M7 (mặc định theo `ADR-0062`). Packet chạm E5 nên chủ kho duyệt
  merge một lần neo SHA, theo cả luật hiện hành lẫn quyết định 4 của ADR.
- (i) Cùng hình dạng lỗi lần thứ ba, hay tín hiệu không hội tụ: protocol §12. Phiên thi công tự xét lại cách làm và ghi lý
  do vào handoff; chỉ hỏi khi rơi vào E1 hay E3.
- (ii) E1: không còn phương án có phép đo chống đỡ, ví dụ văn bản bắt buộc không qua được `doctrine-scan` mà mọi cách viết
  lại đều đổi nghĩa. E2: thiếu tài nguyên, ví dụ không có clone không shallow để chạy vị từ. E3: bằng chứng mâu thuẫn với
  một quyết định của chủ kho, ví dụ một câu của ADR trái với năm quyết định ngày 08-11-2026.

Không có ngân sách mềm. Văn bản của các khối `adr`, `thay` mà reviewer chỉ ra là sai không sửa tại chỗ được, vì vị từ đòi
đúng byte: phiên thi công dừng và đề xuất revision đặc tả kèm văn bản mới; đó không phải điểm hỏi chủ kho.

## 6. Review và ngân sách

- Review đặc tả này (trước khi đóng băng): Codex offline trên commit cục bộ, chung lượt với đặc tả packet 1. Đặc tả chạm
  E5 nên sau review approve vẫn chờ chủ kho duyệt băm.
- Review mã: lượt phản biện Codex như hàng `reviewer`. Packet không có state `packet_loop.py`, nên trần mười lời gọi
  (dòng khai ở đầu tệp) đếm bằng biên nhận: mỗi lời gọi để lại `run.json` của `launcher.py run` và một dòng trên Packet
  Issue ghi số thứ tự lời gọi trên mười, SHA ứng viên và sha256 stdout. Lời gọi thứ mười một không được chạy. Connector
  `@codex review` trên PR draft theo `ADR-0060` M6.
- Audit: packet chạm E5 và có reviewer `human`: chủ kho audit H trước khi H được đẩy, như hàng `reviewer`. Sau push, đối
  chiếu PR head bằng H rồi dẫn lại audit và verdict vào PR (`ADR-0060` M12).
- CI: không tự kích `workflow_dispatch`; Windows `not_required`, M9 không áp.

## 7. `ngoai_pham_vi`

- Mã cổng: `NGUOI_CO_THAM_QUYEN`, `record-lease`, `void-attempt`, `kiem-merge` K4–K6, `ops/lease_publish.py`,
  `ops/bien_nhan_v2.py`, cổng quét đặc tả thêm điểm hỏi ngoài E1–E5: packet 3 và 4 của lộ trình. Packet đầu tiên trong số
  ấy sửa cột cổng của dòng `ADR-0067` ở §20.
- Adapter (đo ở S6): `.claude/skills/work-packet/SKILL.md:159` (`--granted-by ducthangho`) vẫn đúng cho tới khi cấp lease
  theo uỷ quyền có hiệu lực, nên sửa cùng packet đổi cổng lease (packet 3). `.claude/skills/land-packets/SKILL.md` dòng 5
  và 10 (không tự trigger) phải được xét lại cùng packet làm tự merge (packet 5). `.claude/skills/land-packets/SKILL.md:64`
  (dòng miễn mutant của chủ kho) vẫn đúng, vì ADR giữ việc miễn mutant là câu trả lời E2 của chủ kho. Adapter Codex
  `.agents/skills/land-packets/SKILL.md` (dòng 12, chặn tự kích hoạt) thuộc hàng *Tự merge* của bảng chỗ tiêu thụ, xét lại
  cùng packet làm tự merge.
- Tự mở phiên kế nhiệm, phiên reviewer, job đăng bản tin tự động, tự merge: packet 5.
- Tạo Issue bản tin, đăng comment cấp uỷ quyền thường trực: việc vận hành sau khi cơ chế có hiệu lực, không thuộc diff.
- `CONTEXT.md`: thêm từ vựng (danh sách đóng, sổ quyết định uỷ quyền, bản tin, uỷ quyền thường trực, audit uỷ quyền)
  buộc phiên land tái sinh `RELEASE_MANIFEST.json`; để packet sau, định nghĩa nằm trong ADR. Không có mâu thuẫn quyền
  cần sửa ngay (S7).
- Sửa nội dung `ADR-0037`, `ADR-0060`, `ADR-0063` hay ADR nào khác: không hồi tố; mục *Thay những gì* của ADR mới nêu
  câu nào bị thay.
- Protocol §1 bất biến 5 (*"người có thẩm quyền gọi"* `land apply`): giữ nguyên câu chữ; tự merge theo quyết định 4 là
  uỷ quyền bền của người có thẩm quyền, khớp câu cuối của hàng *Người có thẩm quyền* ở §2.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục.

## 9. `chua_do_duoc`

- Số lần chủ kho bị hỏi giảm bao nhiêu: chỉ đo được sau land các packet đổi cổng.
- Phiên audit uỷ quyền có thật sự bắt được E3: chưa có ca chạy thật; đo ở packet 4.
- Bản tin hằng ngày có đến được chủ kho đúng giờ không: phụ thuộc phiên điều phối mở trong ngày cho tới khi có job tự
  động (packet 5).
- Mục sổ mẫu trong ADR đúng bảng khoá: người soạn đã đối chiếu bằng tay (mục 11); bộ kiểm máy cho mục sổ là việc của
  packet 3.

## 10. Quyết định người soạn tự đưa (chủ kho bác được khi duyệt băm)

Các điểm dưới đây không thuộc E1–E5 nên người soạn tự quyết và ghi lại thay vì hỏi. Ở mọi chỗ tài liệu nguồn để ngỏ,
ADR chọn hướng không lỏng hơn luật hiện hành.

1. Sổ quyết định là comment YAML trên Issue của packet: mỗi mục một PR sẽ va làn sổ sách của `ADR-0060` M8; comment có
   URL ổn định để lease hay `record-rescue` trỏ vào, khớp `CAN_CU_RE` của `packet_loop.py`. Bảng khoá có kiểu và nghĩa,
   kèm ba mục mẫu.
2. Bản tin là comment trên một Issue riêng, không phải email: nằm trong control plane, đọc được trên Android, một lần đăng
   ký theo dõi là đủ. Giờ Việt Nam vì chủ kho ở đó.
3. Uỷ quyền thường trực là một (không phải một cho mỗi Mission), hạn 30 ngày; Mission nào được tính thì do câu về Mission
   đã duyệt hướng quyết.
4. Hiệu lực tách theo cơ chế để tài liệu không đi trước mã (nguyên nhân số 7 của tài liệu nguồn). Trong thời gian chuyển
   tiếp, câu hỏi do cổng cũ còn đòi mang mã E2 (thiếu quyền), không thành loại câu hỏi thứ sáu.
5. Windows và mutant giữ nguyên quyền của chủ kho: ca Windows đỏ thuộc tệp trong write set vẫn do chủ kho quyết theo
   `ADR-0060` M3(c), và lượt `full_mutant_audit` bắt buộc chỉ chủ kho miễn; cả hai câu hỏi mang mã E2 vì agent không có
   quyền ấy. Chỉ việc chốt `unknown` chuyển cho reviewer, đúng như văn bản M3 đã ghi; mã K6 hiện đòi chủ kho cho việc ấy
   là chỗ tài liệu và mã lệch nhau (nguyên nhân số 7 của tài liệu nguồn).
6. Huỷ lượt không có bằng chứng máy: chỉ đổi người cho phép (chủ kho → mục sổ kèm log gốc), giữ danh sách lý do và chốt
   không hoàn lượt đã có review; không có log gốc là E2.
7. E4, E5 không rõ thì coi là thuộc, cùng hướng fail-closed với `review_class`. Số ADR là `ADR-0067` vì `ADR-0066` đã được
   #1265 giữ chỗ (S4); nếu lúc cấp lease đã có tệp `docs/adr/0067-*` của packet khác, đặc tả cần revision.
8. Mục sổ `tu_merge` là authorization land nên mang đủ ràng buộc của protocol §13.1 (đích, phương thức, phạm vi, hạn, việc
   hậu merge); hạn 24 giờ sau `luc` để một authorization không đứng mãi trên một SHA cũ. `can_cu` có vai, và mỗi `loai` có
   vai bắt buộc, để không ai phải đoán URL nào chứng minh điều gì.

## 11. Tiền kiểm trước đóng băng

- Định danh: người soạn gọi chính hàm `_spec_merge` của `.claude/dev/packet_loop.py` với một lease giả có `packet_id`
  `GIAM-HOI-P2-ADR-E1-E5`, `revision` 9, `spec_path` là đường dẫn tệp này, `spec_ref` ghim OID commit chứa nó và
  `spec_hash` là sha256 của tệp; hàm phải trả về không lỗi. Kết quả ghi ở biên nhận review đặc tả.
- Mục sổ mẫu: ba khối YAML trong khuôn ADR được nạp bằng `yaml.safe_load` và đối chiếu với các bảng khoá (đủ khoá, đúng
  kiểu, `sha`, `spec_sha256`, `tree` là chuỗi hex đúng độ dài, `kiem_e` đủ năm khoá, `can_cu` đủ vai bắt buộc của `loai`,
  `tu_merge` đủ sáu khoá riêng và `het_han` không quá 24 giờ sau `luc`). Kết quả ghi ở biên nhận review đặc tả. PyYAML không
  phải phụ thuộc của kho; ai không có nó thì phép này là KHÔNG ĐO ĐƯỢC, không phải ĐẠT.

## 12. Thay đổi so với r1

Theo verdict review Codex lượt 1 (08-11-2026, `changes_requested`, 9 finding chung cho hai đặc tả):

- F01 (P1): tiêu đề H1 theo grammar của `ADR-0063`; hàng `packet_id` nói rõ lease khai đúng định danh; thêm mục 11.
- F02 (P1): câu hỏi do cổng cũ còn đòi trong thời gian chuyển tiếp mang mã E2, không còn *"không cần mã E"* (câu Hiệu lực
  của ADR, đoạn Q12A của protocol, mục 10 điểm 4).
- F03 (P2): bỏ câu cấm executor làm Land Operator; quyết định 4 của ADR giữ tách vai của `ADR-0034` (S7).
- F04 (P2): mục *Thay những gì* của ADR có câu thay thế cụ thể cho `ADR-0060` M1, M3, M5, M7, M9, `ADR-0063` K4 và
  `void-attempt`; Windows ca đỏ và mutant giữ chặt (mục 10 điểm 5, 6).
- F05, F06 (P2): ADR nay được quy định nguyên văn cả tệp, trừ dòng Trạng thái và các số đo của mục Cưỡng chế; vị từ so cả
  tệp với khuôn, kiểm dòng Trạng thái (ngày, băm đặc tả, số Issue) và kiểm từng số Cưỡng chế bằng phép đo trên base. Không
  còn phép khớp tiền tố hay đếm dòng có dấu `|`.
- F07 (P2): khối K7 bỏ con số mức dành sẵn của `ADR-0041`; các khối `cu` của skill dựng lại từ packet 1 r2.
- F08 (P2): S6 đo lại đủ adapter; mục 7 ghi đường dẫn và packet chịu trách nhiệm cho từng chỗ.
- F09 (P2): ADR có bảng khoá với kiểu và nghĩa cho `uy_quyen_quyet_dinh.v1` và `uy_quyen_thuong_truc.v1`, hai mục sổ mẫu
  có neo khác nhau; thêm mục 11 điểm 2. `sha` và `spec_sha256` phải viết trong nháy kép: tiền kiểm mục 11 bắt được ở bản
  nháp r2 rằng YAML đọc một chuỗi hex toàn chữ số thành số nguyên.

## 13. Thay đổi so với r2

Theo verdict review Codex lượt 2 (08-11-2026, `changes_requested`, 5 finding chung cho hai đặc tả):

- G01 (P2): sửa ở packet 1 r3 (câu về trần khi thiếu dòng khai); các khối `cu` K7 dựng lại từ packet 1 r3.
- G02 (P1): ADR không còn bỏ quyền của chủ kho ở `ADR-0060` M3(c). Ca Windows đỏ thuộc write set vẫn do chủ kho quyết,
  câu hỏi mang mã E2; reviewer chỉ nhận việc chốt `unknown`. Hàng *Windows* của bảng chuyển tiếp và mục 10 điểm 5 đổi theo;
  loại `mien_windows` đổi tên thành `phan_loai_windows`.
- G03 (P2): khối K7 đòi mọi câu hỏi chủ kho mang mã E, kể cả câu sinh từ điểm dừng loại (i); gạch đầu dòng `pham_vi_e` nói
  rõ luật đóng băng thắng cả câu *"Không hành động cho tới khi người dùng xác nhận đã hiểu giống nhau"* của mục 1.
- G04 (P2): `can_cu` thành danh sách có `vai`, kèm bảng vai bắt buộc theo `loai`; `tu_merge` mang thêm sáu khoá cho đủ ràng
  buộc §13.1 (`pr`, `dich`, `phuong_thuc`, `tree`, `het_han`, `hau_merge`) và có mục sổ mẫu thứ ba; khối Q13B của protocol
  trỏ đúng loại mục sổ ấy; mục 10 điểm 8.
- G05 (P2): `kiem_p2.py` băm byte thô của đặc tả và trả rc 3 khi có CR, thay vì đổi CRLF thành LF rồi mới băm.

## 14. Thay đổi so với r3, và xét lại cách làm

Verdict review Codex lượt 3 (08-11-2026, `changes_requested`, 2 P2 và 1 P3; năm finding G của lượt 2 đều đã vá thật; packet
1 r3 không còn lỗi riêng nên giữ nguyên r3).

**Xét lại cách làm** (protocol §12; luật dừng ở mục 5): H01 là lần thứ ba của lớp *thay quyền chủ kho mà sót chỗ tiêu thụ
quyền ấy* (F04 lượt 1, G02 lượt 2, H01 lượt 3). Hai lần trước đều vá đúng chỗ được chỉ. Lần này đổi cách: thay vì vá riêng
M8, người soạn quét toàn bộ chỗ đọc quyền chủ kho trong mã cổng, protocol, `ADR-0060` và adapter (S8), rồi đưa mọi hit vào
một mục mới của ADR, *Chỗ tiêu thụ phải đổi theo*, giao cho packet đổi cổng sửa cùng lúc. Phép quét được in nguyên văn trong
ADR để lượt sau đo lại. Không rơi vào E1 (có phương án và phép đo chống đỡ) hay E3 (không đảo quyết định nào), nên không hỏi
chủ kho.

- H01 (P2): câu thay cho trường *"lần duyệt của chủ kho"* của `ADR-0060` M8; mục *Chỗ tiêu thụ phải đổi theo* giao
  `kiem-dong-wp` D1, `ghi-uy-quyen`, `doi-chieu-uy-quyen` và adapter `land-packets` cho packet làm tự merge. Phép quét còn tìm
  thêm hai chỗ chưa finding nào nêu: bảng ngưỡng ở protocol §8 và vế checkpoint P3 của `ADR-0060` M1; cả hai đã có chỗ.
- H02 (P2): `kiem_p2.py` trả rc 3 trên clone shallow, như `kiem_p1.py`; A6 thêm hai đột biến.
- H03 (P3): mục 10 điểm 1 ghi ba mục mẫu.

## 15. Thay đổi so với r4

Verdict review Codex lượt 4 (08-11-2026): **P1 r3 approve**; P2 r4 `changes_requested` với 2 P2 (I01, I02) và 1 P3 (I03).

**Xét lại cách làm lần nữa** (lớp *thay quyền chủ kho mà sót chỗ tiêu thụ* xuất hiện lần thứ tư: F04, G02, H01, I01/I02).
Gốc của lần này khác lần trước: phép quét r4 đúng là bắt được mọi chỗ *có từ khoá*, nhưng nghĩa vụ không phải lúc nào cũng
mang từ khoá (I01), và gom hit theo hàm thì lẫn hai quyền khác nhau dùng chung một danh sách cho phép (I02). Hai cách chữa
cùng lúc: (1) bảng tiêu thụ có cột **xếp loại** (đổi / giữ / cần quyết định riêng) cho từng chỗ, nên một chỗ dùng chung
danh sách cho phép mà không thuộc quyết định nào thì ghi **giữ** chứ không bị kéo theo; (2) ADR nói thẳng bảng là sàn, và
mọi packet đổi cổng phải tự lập lại bảng tiêu thụ cho cơ chế của mình, đọc theo nghĩa vụ, trong đặc tả có review riêng.
Như vậy việc tìm chỗ tiêu thụ không còn là một danh sách vô hạn mà ADR này phải đúng hết, mà là nghĩa vụ có chủ của từng
packet sau. Vẫn không rơi vào E1 hay E3, nên không hỏi chủ kho.

- I01 (P2): ba câu mới ở mục *Thay những gì* cho câu *"agent không tự approve hay merge"* của `ADR-0060`, câu *"Human Land
  Approver …"* của protocol §8 và mục `land-packets` của protocol §13; hàng *Tự merge* của bảng tiêu thụ nêu thêm hai
  adapter `land-packets`; lệnh quét 2 thêm năm từ khoá và ra 23 hit.
- I02 (P2): `thu_hoi_boi` và đường `human_audit_transition.v1` tách thành hàng **giữ**, kèm lý do.
- I03 (P3): lỗi nằm ở hồ sơ bằng chứng của lượt 4, không ở đặc tả; EVIDENCE lượt 5 ghi đúng base `bf9914c` của ứng viên
  packet 1 và số hit đo lại.

## 16. Thay đổi so với r5

Verdict review Codex lượt 5 (08-11-2026): **approve** P2 r5, kèm hai P3. Sửa cả hai để PR đặc tả không còn P3 mở (theo
`ADR-0060` M1 đang hiệu lực, P3 mở phải đóng có bằng chứng hay được chủ kho miễn). Khối `adr`, các khối `thay` và write set
không đổi.

- J01 (P3): S6 và mục 7 thôi nói `.agents/skills/*` không có chỗ nào; adapter Codex `land-packets` thuộc hàng *Tự merge*.
- J02 (P3): `kiem_p2.py` trả rc 3 khi không đọc được tệp đặc tả (vắng, là thư mục, lỗi I/O); A6 thêm đột biến tương ứng.
  `kiem_p1.py` của packet 1 r3 có cùng hành vi; packet 1 r3 đã được approve nên giữ nguyên băm, và hành vi ấy chỉ xảy ra khi
  đưa sai đường dẫn đặc tả, không cho xanh giả.

## 17. Thay đổi so với r6

Chủ kho chỉ đạo ngày 08-11-2026: *"Do CLaude sắp hết quota, hãy chuyển sang agy 4.0 argon làm executor"*. Đổi hai hàng
`executor` và `reviewer` ở bảng đầu, và trỏ packet 1 r4 (cùng chỉ đạo, các khối `moi` không đổi nên khối `cu` ở đây không
đổi). Khối `adr`, các khối `thay`, write set và tiêu chí không đổi. Packet chạm E5 nên chủ kho vẫn duyệt băm, audit và
duyệt merge, bất kể executor là ai.

## 18. Thay đổi so với r7

Verdict review Codex lượt 6 (08-11-2026): **approve** P2 r7, kèm một P3 chung cho hai packet (K01). Sửa giống hệt packet 1 r5:
hàng `executor` nói rõ adapter chỉ dùng lại phần cú pháp, identity và đối số provider lấy từ lease Antigravity; hàng
`reviewer` nói rõ `init` từ chối cặp cùng họ nên reviewer phải đổi họ trước `init` nếu cần. Khối `adr`, các khối `thay`, write
set và tiêu chí không đổi.

## 19. Thay đổi so với r8

Chủ kho duyệt băm r8 ngày 08-11-2026 (UTC) trên #1292, rồi cùng ngày đổi executor, nguyên văn: *"Đổi agy sang codex. Executor và reviewer đều là codex. Reviewer có koo hình hoặc nỗ lực cao hơn và có thể chạy ở máy khác"*. Đổi giống hệt packet
1 r6 (mục 16 của đặc tả ấy): hàng `executor` sang Codex, packet không dùng state `packet_loop.py`; hàng `reviewer` sang
`human` (chủ kho, `human_audited`, audit H trước push), lượt Codex nỗ lực cao thành phản biện bổ sung; mục 6 đếm trần lời
gọi bằng biên nhận. Trỏ packet 1 r6; dòng Trạng thái của ADR và vị từ đổi định danh r8 thành r9. Khối `adr`, các khối
`thay`, write set và các tiêu chí khác không đổi.
