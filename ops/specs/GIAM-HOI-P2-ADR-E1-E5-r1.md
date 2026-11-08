# Đặc tả packet `GIAM-HOI-P2-ADR-E1-E5` r1: `ADR-0067` danh sách đóng E1–E5 và uỷ quyền thường trực; protocol §2, §12, §13, §20; skill `soan-spec` trỏ về ADR

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet_id | `GIAM-HOI-P2-ADR-E1-E5`, revision 1, generation 1 |
| packet_issue | chưa tạo. Issue trỏ đặc tả này bằng `spec_hash`; đặc tả không ghi số Issue. Nháp thân Issue nằm ngoài tệp này |
| mission | lộ trình "Giảm việc hỏi chủ kho", packet 2/5. Chưa có Mission Issue |
| nguon_cap_viec | Chủ kho đồng ý cả năm khuyến nghị ở cột *Quyết định* của tài liệu https://claude.ai/artifact/6JUF8DsbHxfN5GjsbdAtHT ("Giảm việc hỏi chủ kho") trong phiên chat ngày 08-11-2026, nguyên văn: *"Bạn làm hộ cho tôi luôn. TÔi đồng ý duyệt 5 điểm và chốt nâng trần theo đề xuất"*. Packet này là mục 2 của phần *Lộ trình*. Bảng *Việc agent làm hộ, và chốt an toàn của từng việc* của tài liệu là phần chủ kho đã đọc khi duyệt: con số *"khoảng 220 trong 273 quyết định có loại rõ ràng sẽ không cần bạn nữa"* ở phần *Tóm tắt* chỉ đúng khi các dòng của bảng ấy (miễn trừ Windows, mutant, P3; push thêm; checkpoint vì hình dạng lỗi) cũng đổi theo, nên đặc tả này coi các dòng ấy thuộc phạm vi đã duyệt |
| review_class | `sensitive`. Bộ phân lớp `ops/lease_publish.py` (`_BANG_LOP` dòng 59–67) trả `sensitive` cho mọi đường dẫn không có trong bảng |
| base | `origin/master` lúc cấp lease, và phải chứa commit land của `GIAM-HOI-P1-SOAN-SPEC`. Soạn trên `e3c639be40dba644ecbf9d729d72837691f59ff4` cộng ứng viên packet 1 dựng từ đặc tả của nó (đo 10:30Z 08-11-2026) |
| depends_on | `GIAM-HOI-P1-SOAN-SPEC`: các khối `cu` của `SKILL.md` ở §2 là văn bản packet 1 viết ra |
| executor | `claude` (Claude Code), môi trường `cloud` hay `local` đều được |
| reviewer | `codex` offline qua `.claude/dev/launcher.py run` (`ADR-0060` M12), cộng connector `@codex review` trên PR draft (`ADR-0060` M6) |
| luật merge | `ADR-0060`, mặc định theo `ADR-0062` |
| windows | `not_required`: mọi tệp của diff là `*.md` (`ADR-0060` M3 bước 3) |
| full_mutant_audit | không áp: diff không chạm `.claude/dev/**`, `ops/**/*.py`, `.github/workflows/**` (`ADR-0060` M9) |
| pham_vi_e | **chạm E5**: packet tạo chính danh sách đóng và các uỷ quyền. Hệ quả theo chính ADR này và theo luật hiện hành: chủ kho duyệt băm đặc tả, audit, và duyệt merge một lần neo SHA. Không chạm E4 |

## 1. Vì sao — số đo

Đo trên `origin/master` `e3c639b` lúc 10:30Z 08-11-2026, trừ chỗ ghi khác.

| # | sự kiện | số đo |
|---|---|---|
| S1 | số quyết định của chủ kho | Tài liệu nguồn, đo 07-11-2026 bằng `gh api` trên Issue/PR: 391 comment quyết định trong 31 ngày (08-10 → 07-11-2026), 226 trong số đó là agent ghi hộ; 253 lần đăng lease, lần nào cũng `granted_by: ducthangho`. Không đo lại ở phiên này |
| S2 | điểm hỏi do mã đòi | `NGUOI_CO_THAM_QUYEN = ("ducthangho",)` ở `.claude/dev/packet_loop.py:157`; dùng ở `record-lease` (dòng 920), `void-attempt --khong-co-bang-chung` (dòng 1078), `nang-tran` (dòng 1318), `record-rescue` (dòng 1337), `ghi-uy-quyen` (dòng 1462). `kiem-merge` đòi dòng của chủ kho cho P3 còn mở (K5, dòng 3402), Windows `unknown` (K6, dòng 3408–3410), miễn mutant (K7, dòng 3418–3426); human audit K4 chỉ nhận comment của owner `ducthangho` (`ADR-0063`) |
| S3 | điểm hỏi chỉ sống trong văn bản | `ADR-0060` M5 *"Mỗi lần push thêm cần checkpoint chủ kho"* và protocol §12 bất biến (b): không lệnh nào của `kiem-merge` đếm lần push (đo: `rg -n "push" .claude/dev/packet_loop.py` không ra phép kiểm số lần push nào). Duyệt băm đặc tả: không điều nào của protocol bắt, là thói quen của skill `soan-spec` |
| S4 | số ADR kế tiếp | `ADR-0066` đã được packet #1265 giữ chỗ (143 lần nhắc trong `ops/`, `docs/`, `.claude/` trên `master`; chưa nhánh nào có tệp `docs/adr/0066-*`). Không nhánh nào trong 748 nhánh máy chủ có `docs/adr/0067-*` hay `docs/adr/007*` (đo 11:38Z, `git ls-tree` trên từng ref sau khi fetch đủ); 0 lần nhắc `ADR-0067` trên `master` |
| S5 | người đang giữ write set | `ai-dang-giu` trên clone đủ 745 nhánh máy chủ: `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` 0 người giữ (11:28Z); `.claude/skills/soan-spec/SKILL.md` 0 người giữ; `docs/PROTOCOL_DA_PHIEN.md` `NGƯỜI_GIỮ 1: wp1174-r17-g14-codex` (`lease_until` 18:03:01Z 08-11-2026). Lease của packet này chỉ cấp được khi cả ba ra 0 người giữ, và sau khi packet 1 land |
| S6 | adapter có nhắc điểm hỏi chủ kho | `.claude/skills/{work-packet,cross-review,land-packets}/SKILL.md` và `.agents/skills/*/SKILL.md` chỉ nhắc chủ kho ở đường `gh api graphql` (thiếu quyền GraphQL, tức E2). Không adapter nào phải sửa ngoài `soan-spec` |
| S7 | `CONTEXT.md` | nằm trong `RELEASE_MANIFEST.json` (184 mục). Thêm từ vựng vào đó buộc phiên land tái sinh manifest; xem `ngoai_pham_vi` |

## 2. Thay đổi

### M1 → `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` (tệp mới)

Dòng đầu bắt đầu bằng `# ADR-0067 — `. Dòng thứ ba bắt đầu bằng `- **Trạng thái:** Accepted (`, ghi ngày land, chủ kho
`ducthangho`, packet `GIAM-HOI-P2-ADR-E1-E5` r1, số Issue và URL comment duyệt của chủ kho trên Issue ấy (neo băm đặc tả
này), không dẫn phiên chat. Sau đó đúng mười tiêu đề mục dưới đây, theo thứ tự, mỗi tiêu đề là nguyên một dòng:

~~~ tieu_de
## Bối cảnh
## Quyết định
## Sổ quyết định uỷ quyền
## Bản tin hằng ngày
## Comment ghi hộ
## Hiệu lực và chuyển tiếp
## Thay những gì
## Cưỡng chế
## Phương án bị loại
## Giới hạn
~~~

Mỗi khối `cau` dưới đây là một câu phải có **nguyên văn** trong mục ghi ở dòng mở khối, đúng một lần trong cả ADR; được
ngắt dòng tuỳ ý trong cùng một đoạn, không được tách sang hai đoạn. Câu khác của ADR viết tự do.

**Bối cảnh:** số đo S1–S3 kèm nguồn và ngày đo; nhắc rằng số của tài liệu nguồn là ước lượng theo loại, chưa đo trên
việc thật.

**Quyết định.** Câu mở mục:

~~~ cau quyet_dinh D1
Agent chỉ dừng để hỏi chủ kho khi rơi vào một trong năm mã E1–E5 dưới đây; mọi việc khác agent tự quyết, ghi vào sổ
quyết định uỷ quyền và báo trong bản tin hằng ngày.
~~~

Một bảng bốn cột `mã | tình huống | ví dụ trong kho | phải mang theo khi hỏi`, đúng năm hàng E1–E5. Mỗi dòng của khối
`ma_e` dưới đây cho một hàng: cột 1 bằng đúng trường thứ nhất, cột 2 bằng đúng trường thứ hai (hai trường cách nhau
bằng ` ; `). Cột ví dụ và cột mang theo lấy từ bảng *Năm tình huống vẫn phải hỏi bạn* của tài liệu nguồn, khác rỗng.

~~~ ma_e
E1 ; Hướng đi bế tắc: đã xét lại cách làm mà không còn phương án nào có phép đo chống đỡ
E2 ; Thiếu tài nguyên: chạm trần cứng, hoặc thiếu máy, quota hay quyền
E3 ; Phát hiện đảo ngược chỉ đạo: bằng chứng mâu thuẫn với một quyết định của chủ kho
E4 ; Hành động không hoàn tác được hay đi ra ngoài kho
E5 ; Đổi chính thẩm quyền
~~~

~~~ cau quyet_dinh D2
E4 và E5 định nghĩa theo hậu quả, không theo tên lệnh; không rõ một việc có thuộc E4 hay E5 không thì coi là thuộc.
~~~

~~~ cau quyet_dinh D3
Mỗi câu hỏi gửi chủ kho ghi mã E của nó và mang theo thứ cột cuối của bảng nêu; câu không gắn được mã nào thì agent
không hỏi mà tự quyết.
~~~

Năm quyết định ngày 08-11-2026, mỗi quyết định một đoạn:

~~~ cau quyet_dinh D4
Đặc tả packet thuộc một Mission chủ kho đã duyệt hướng được người soạn đóng băng khi một review độc lập approve, không
cần comment duyệt băm của chủ kho; đặc tả đảo một quyết định của chủ kho (E3) hay chạm E4, E5 vẫn cần chủ kho duyệt
băm.
~~~

~~~ cau quyet_dinh D5
Audit uỷ quyền áp cho mọi packet không chạm E5 và mang mức bảo đảm riêng `delegated_audited`, không bao giờ được ghi
thành `human_audited`; packet chạm E5 vẫn cần chủ kho audit.
~~~

~~~ cau quyet_dinh D6
Phiên audit uỷ quyền là phiên mới, không chung ngữ cảnh với executor hay reviewer, chỉ đọc, chạy trên đúng SHA; nó đối
chiếu đặc tả và diff với các quyết định chủ kho đã ghi, và dừng để hỏi khi thấy E3, E4 hay E5.
~~~

~~~ cau quyet_dinh D7
Packet không chạm E4 hay E5 được tự merge khi đủ điều kiện merge của `ADR-0060`, review approve và audit uỷ quyền đạt;
packet chạm E4 hay E5 cần một lần duyệt của chủ kho neo SHA.
~~~

~~~ cau quyet_dinh D8
Người bấm merge theo uỷ quyền là phiên điều phối hay phiên land, không phải executor của chính packet ấy.
~~~

~~~ cau quyet_dinh D9
Chủ kho uỷ quyền thường trực cho phiên điều phối cấp lease cho packet thuộc Mission chủ kho đã duyệt hướng, sau khi quét
toàn kho ra không người giữ nào trên write set; uỷ quyền có hạn 30 ngày kể từ comment cấp, gia hạn bằng comment mới, và
chủ kho thu hồi bằng một comment.
~~~

~~~ cau quyet_dinh D10
Write set chạm E4 hay E5 thì phiên điều phối không cấp lease theo uỷ quyền thường trực mà hỏi chủ kho; lease cấp theo
uỷ quyền ghi URL comment uỷ quyền nó dựa vào.
~~~

~~~ cau quyet_dinh D11
Một Mission được coi là đã duyệt hướng khi Mission Issue có comment của chủ kho, hay comment ghi hộ đúng luật ở mục
Comment ghi hộ, chấp nhận `plan_hash` của revision đang chạy.
~~~

Mục Quyết định còn ghi: E4 gồm ít nhất đẩy Package lên Drive, `clasp`/GAS deploy, `--apply` lên registry, Drive hay NLM,
xoá ref hay tag ngoài luật sẵn có của `.github/workflows/ops-don-ref.yml`, đọc hay ghi secrets, đổi ruleset; E5 gồm ít
nhất sửa danh sách E1–E5, sửa `NGUOI_CO_THAM_QUYEN` hay danh sách cho phép tương đương, sửa mã cổng cấp lease hay cổng
merge, sửa ADR này. Merge commit hoàn tác được nên merge tự nó không là E4. Giới hạn độc lập của audit uỷ quyền (cùng họ
model với executor Claude) ghi ở mục Giới hạn.

**Sổ quyết định uỷ quyền.**

~~~ cau so D12
Mỗi quyết định agent đưa thay cho một câu hỏi trước đây là một comment trên Issue của packet, thân là đúng một khối
YAML `uy_quyen_quyet_dinh.v1`.
~~~

~~~ cau so D13
Mục sổ là hồ sơ của một quyết định trong phạm vi uỷ quyền chủ kho đã cấp; nó không tự cấp quyền (`ADR-0023`).
~~~

~~~ cau so D14
Chủ kho bác một quyết định bằng comment `bac: <URL mục sổ>`, kèm lý do nếu muốn; phiên kế tiếp chạm packet ấy hoàn tác
quyết định trước mọi việc khác và ghi mục sổ mới trỏ mục bị bác.
~~~

Mục này liệt kê các khoá của khối YAML, mỗi khoá viết trong dấu `` ` ``: `schema_version`, `loai`, `packet`, `sha`,
`can_cu`, `phep_do`, `kiem_e`, `nguoi_quyet`, `hoan_tac`; và các giá trị của `loai`: `cap_lease`, `dong_bang_dac_ta`,
`mien_p3`, `mien_windows`, `huy_luot`, `push_them`, `tu_merge`, `audit_uy_quyen`, `xet_lai_cach_lam`, `khac`. `kiem_e`
ghi kết quả xét từng mã E1–E5 cho quyết định ấy. `nguoi_quyet` ghi provider, họ model và mã phiên của agent.

**Bản tin hằng ngày.**

~~~ cau ban_tin D15
Bản tin là một comment mỗi ngày trên Issue bản tin của kho, liệt kê theo loại mọi mục sổ đăng trong ngày hôm trước kèm
URL, các câu hỏi E1–E5 đang chờ, các mục đã bị bác và uỷ quyền thường trực còn dưới 7 ngày; ngày không có mục sổ nào
thì không đăng.
~~~

~~~ cau ban_tin D16
Cho tới khi có job tự động, phiên điều phối đầu tiên của mỗi ngày theo giờ Việt Nam (UTC+7) đăng bản tin của ngày hôm
trước; comment cấp, gia hạn và thu hồi uỷ quyền thường trực cũng nằm trên Issue bản tin.
~~~

~~~ cau ban_tin D17
Issue bản tin là Issue mở duy nhất có tiêu đề bắt đầu bằng `Bản tin quyết định uỷ quyền`; chưa có thì phiên đăng bản tin
đầu tiên tạo nó.
~~~

Mục này nêu khối YAML `uy_quyen_thuong_truc.v1` của comment cấp uỷ quyền (khoá tối thiểu `pham_vi`, `cap_luc`,
`het_han`) và dòng thu hồi `thu_hoi_uy_quyen: <URL comment cấp>`.

**Comment ghi hộ.**

~~~ cau ghi_ho D18
Comment agent đăng thay chủ kho phải có dòng `Quyết định chủ kho — ghi hộ`, kèm nguyên văn câu của chủ kho và ngữ cảnh
câu hỏi; agent chỉ ghi hộ điều chủ kho đã quyết.
~~~

~~~ cau ghi_ho D19
Phiên agent đăng bằng credential của chủ kho, nên tên tác giả của comment không chứng minh ai đã quyết; nhãn ghi hộ và
sổ quyết định là lời khai có cấu trúc, không phải bằng chứng danh tính.
~~~

Mục này ghi thêm: comment ghi hộ phải đọc ngược bằng `gh api … --jq .body` sau khi đăng, và ghi hộ không tự cấp lease hay
merge.

**Hiệu lực và chuyển tiếp.**

~~~ cau hieu_luc D20
ADR này có hiệu lực từ commit land của nó trên first-parent master và không hồi tố. Cơ chế nào bảng chuyển tiếp ghi
hiệu lực từ land packet đổi cổng thì chỉ có hiệu lực từ commit land của packet đổi cổng ấy; trước đó cổng hiện hành giữ
nguyên, và điểm hỏi cổng ấy đòi được hỏi như điểm chuyển tiếp, không cần mã E.
~~~

Sau câu ấy là bảng chuyển tiếp năm cột
`điểm hỏi hiện nay | cổng đang đòi | cách làm mới | mã E còn hỏi | hiệu lực`, đúng mười ba hàng; mục này không có bảng
nào khác. Mỗi dòng của khối
`chuyen_tiep` dưới đây cho một hàng: cột 1 bằng đúng trường thứ nhất, cột 4 bằng đúng trường thứ hai, cột 5 bắt đầu
bằng đúng trường thứ ba (hai trường cách nhau bằng ` ; `). Cột 2 ghi tệp và dòng của cổng, đo trên base của lease, hoặc
`không cổng mã`. Cột 3 tóm tắt cách làm mới theo tài liệu nguồn.

~~~ chuyen_tiep
Cấp lease ; E4, E5 ; từ land packet đổi cổng
Duyệt băm đặc tả ; E3, E4, E5 ; từ land ADR này
Nâng trần ; E2 ; từ land ADR này
Review Rescue Checkpoint vì chạm trần ; E2 ; từ land ADR này
Checkpoint vì hình dạng lỗi lặp hay không hội tụ ; E1, E3 ; từ land ADR này
Miễn P3 còn mở ; không ; từ land packet đổi cổng
Windows: `unknown`, ca đỏ trong write set, máy offline ; E2 ; từ land packet đổi cổng
Miễn mutant ; E2 ; từ land packet đổi cổng
Push thêm ; E2 ; từ land ADR này
Human audit ; E5 ; từ land packet đổi cổng
Duyệt merge ; E4, E5 ; từ land packet đổi cổng
Huỷ lượt không có bằng chứng máy ; không ; từ land packet đổi cổng
Mở phiên kế nhiệm và phiên reviewer ; không ; từ land ADR này
~~~

**Thay những gì.** Mục này nêu từng câu bị thay và từ khi nào (theo bảng chuyển tiếp), mỗi mục nhắc đúng định danh sau,
mỗi định danh có mặt ít nhất một lần trong mục: `ADR-0060` M1, `ADR-0060` M3, `ADR-0060` M5, `ADR-0060` M7, `ADR-0060`
M9, `ADR-0063` K4, protocol §12 bất biến (b). Không sửa nội dung tệp của các ADR ấy.

**Cưỡng chế.** Một dòng cho từng vị trí cổng mà §20 của protocol liệt kê: `ops/lease_publish.py`,
`.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`, `.github/workflows/ci.yml`,
`.github/workflows/ops-publish-lease.yml`. Mỗi dòng ghi lệnh `git show <base>:<tệp> | grep -c 'ADR-0067'`, số dòng của tệp
đã đọc và kết quả; kỳ vọng 0 ở cả sáu. Kết luận: lúc land, danh sách đóng sống bằng kỷ luật đọc; cổng đọc nó là việc của
packet đổi cổng.

**Phương án bị loại**, mỗi phương án kèm lý do: giữ mặc định *"chưa được phép thì hỏi"*; danh sách cấm điểm hỏi thay cho
danh sách đóng; sổ quyết định là tệp trong kho (mỗi mục một PR); bản tin qua email (không nằm trong control plane);
uỷ quyền thường trực không hạn.

**Giới hạn:** audit uỷ quyền độc lập về ngữ cảnh nhưng cùng họ model khi executor là Claude; chưa có họ model thứ ba dùng
được trong kho; danh tính chưa tách (phiên chạy bằng credential của chủ kho); ước lượng 220/273 chưa đo trên việc thật.

### M2 → `docs/PROTOCOL_DA_PHIEN.md`

Cùng quy ước khối `cu`/`moi` như đặc tả packet 1: khối `cu` là nguyên văn trên base kể cả ký tự xuống dòng cuối, có đúng
một lần trong tệp; khối `moi` là thứ thay vào, đúng từng byte.

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
hỏi ngoài năm mã. Điểm hỏi mà một cổng mã hiện hành còn đòi được hỏi tiếp theo bảng chuyển tiếp của `ADR-0067` cho tới
khi cổng ấy đổi.
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
đã có hiệu lực, authorization ấy là mục sổ quyết định uỷ quyền neo exact SHA, kèm review approve, audit uỷ quyền đạt và
đủ điều kiện `ADR-0060`. Adapter không tự cấp approval; Land Operator ghi merge,
~~~

§20 bảng A, một dòng cuối bảng (neo vào tiêu đề mục B ngay sau bảng, nên vẫn đúng khi dòng `ADR-0066` land trước):

~~~ thay PROTOCOL Q20 cu

### B. ADR ngoài phạm vi protocol — thuộc `scripts/tl.py` và đường phát hành
~~~

~~~ thay PROTOCOL Q20 moi
| `ADR-0067` | Danh sách đóng E1–E5: agent chỉ hỏi chủ kho trong năm tình huống; đóng băng đặc tả sau review độc lập, audit uỷ quyền, tự merge packet không chạm E4/E5, uỷ quyền thường trực cấp lease 30 ngày; sổ quyết định uỷ quyền, bản tin hằng ngày, comment ghi hộ có nhãn | Accepted — cơ chế cần cổng mã có hiệu lực khi cổng ấy đổi (bảng chuyển tiếp trong ADR) | **0 cổng**; đo lúc land trên sáu vị trí cổng (mục Cưỡng chế của ADR) |

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
  approve thì dừng hay hỏi chủ kho". Mức dành sẵn hai lượt của `ADR-0041` là ngân sách giữ trước,
  không phải trần hay điểm dừng. Lượt thứ hai trở đi theo điều kiện của `ADR-0052` và không cần hỏi ai.
- **Mục `luat_dung` chỉ có hai loại dòng.** (i) Điểm dừng mà protocol hay một ADR đang hiệu lực đã
  đặt: dẫn bằng tên mục hay ADR, không chép lại, không hạ ngưỡng. (ii) Một trong ba mã dưới đây, kèm
  thứ phải mang theo khi hỏi:
  - **E1 — hướng đi bế tắc:** đã xét lại cách làm mà không còn phương án nào có phép đo chống đỡ.
    Mang theo gốc rễ, các phương án đã thử và vì sao hỏng, một đề xuất.
  - **E2 — thiếu tài nguyên:** chạm trần cứng, hoặc thiếu máy, quota hay quyền. Mang theo mức đã
    dùng, còn thiếu bao nhiêu, để làm gì.
  - **E3 — phát hiện đảo ngược chỉ đạo:** bằng chứng mâu thuẫn với một quyết định của chủ kho. Mang
    theo quyết định nào, bằng chứng, hậu quả nếu giữ nguyên.
- **Câu nào trong đặc tả nói tới việc hỏi, báo hay chờ chủ kho thì phải thuộc loại (i) hoặc mang một
  mã E.** Không thuộc loại nào thì đó không phải điểm hỏi: phiên đang giữ việc tự quyết, rồi ghi gốc
  rễ, phương án chọn và phép đo chống đỡ vào revision kế tiếp hay handoff.

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
  approve thì dừng hay hỏi chủ kho". Mức dành sẵn hai lượt của `ADR-0041` là ngân sách giữ trước,
  không phải trần hay điểm dừng. Lượt thứ hai trở đi theo điều kiện của `ADR-0052` và không cần hỏi ai.
- **Mục `luat_dung` chỉ có hai loại dòng.** (i) Điểm dừng mà protocol hay một ADR đang hiệu lực đã
  đặt: dẫn bằng tên mục hay ADR, không chép lại, không hạ ngưỡng. (ii) Mã E1, E2 hay E3 của danh sách
  đóng, kèm thứ ADR ấy bắt mang theo khi hỏi.
- **Câu nào trong đặc tả nói tới việc hỏi, báo hay chờ chủ kho thì phải thuộc loại (i) hoặc mang một
  mã E.** Không thuộc loại nào thì đó không phải điểm hỏi: phiên đang giữ việc tự quyết, rồi ghi gốc
  rễ, phương án chọn và phép đo chống đỡ vào revision kế tiếp hay handoff.
- **Mục `pham_vi_e` khai đặc tả có chạm E4, E5 không**, theo định nghĩa của ADR ấy; không rõ thì khai là
  chạm. Đặc tả của packet thuộc Mission chủ kho đã duyệt hướng, không chạm E4, E5 và không đảo quyết
  định nào của chủ kho, được người soạn đóng băng khi một review độc lập approve; đặc tả khác chờ chủ
  kho duyệt băm. Với packet như thế, vòng hỏi ở mục 1 lấy câu trả lời từ các quyết định Mission đã ghi;
  câu không trả lời được từ đó mà cũng không thuộc mã E nào thì người soạn tự quyết và ghi vào sổ quyết
  định uỷ quyền. Luật này thắng câu "Quyết định thì luôn là của người dùng" ở mục 1 cho đúng loại packet ấy.
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

Diff PR: đúng **3 tệp**. Ước lượng: ADR mới ≤ 200 dòng; protocol thêm 22 dòng, bớt 2; skill thêm
11, bớt 13 (hai số sau đo trên ứng viên dựng từ các khối `thay` trên base packet 1). Trần `ADR-0053` cho
packet `sensitive` (≤ 6 tệp, ≤ 450 dòng thêm): **đạt** nếu ADR ≤ 417 dòng; vượt thì dừng và đề xuất revision cắt
bớt ADR, không xin nâng trần. Ba tệp không nằm trong `RELEASE_MANIFEST.json`. Handoff đăng thành comment trên Packet
Issue. Không sửa `VERSION`, `CHANGELOG.md`, `changelog.d/`, `CONTEXT.md`.

## 4. Nghiệm thu

Vị từ có một dạng duy nhất là script dưới đây, chạy như ở packet 1: chép ra thư mục tạm, chạy ở gốc một clone không
shallow của ứng viên sau `git fetch origin`:

```
python kiem_p2.py ops/specs/GIAM-HOI-P2-ADR-E1-E5-r1.md <OID base>
```

Mã thoát: 0 ĐẠT, 1 ĐỎ, 3 KHÔNG ĐO ĐƯỢC.

```python
# kiem_p2.py: vị từ nghiệm thu của GIAM-HOI-P2-ADR-E1-E5 r1.
# Ứng viên là commit HEAD của checkout hiện tại; base là đối số thứ hai.
import re
import subprocess
import sys

TEP = {"SKILL": ".claude/skills/soan-spec/SKILL.md", "PROTOCOL": "docs/PROTOCOL_DA_PHIEN.md"}
ADR = "docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md"
MUC = {"quyet_dinh": "## Quyết định", "so": "## Sổ quyết định uỷ quyền", "ban_tin": "## Bản tin hằng ngày",
       "ghi_ho": "## Comment ghi hộ", "hieu_luc": "## Hiệu lực và chuyển tiếp"}
CONG = (".claude/dev/packet_loop.py", ".claude/dev/launcher.py", ".claude/dev/gate_lifecycle.py",
        ".github/workflows/ci.yml", ".github/workflows/ops-publish-lease.yml", "ops/lease_publish.py")
CHUOI = {
    "## Sổ quyết định uỷ quyền": ["`schema_version`", "`loai`", "`packet`", "`sha`", "`can_cu`", "`phep_do`",
                                  "`kiem_e`", "`nguoi_quyet`", "`hoan_tac`", "`cap_lease`", "`dong_bang_dac_ta`",
                                  "`mien_p3`", "`mien_windows`", "`huy_luot`", "`push_them`", "`tu_merge`",
                                  "`audit_uy_quyen`", "`xet_lai_cach_lam`", "`khac`"],
    "## Bản tin hằng ngày": ["`uy_quyen_thuong_truc.v1`", "`pham_vi`", "`cap_luc`", "`het_han`",
                              "`thu_hoi_uy_quyen: <URL comment cấp>`"],
    "## Thay những gì": ["`ADR-0060` M1", "`ADR-0060` M3", "`ADR-0060` M5", "`ADR-0060` M7", "`ADR-0060` M9",
                          "`ADR-0063` K4", "protocol §12 bất biến (b)"],
}


def git(*doi_so, rc_nhan=(0,)):
    p = subprocess.run(["git", *doi_so], capture_output=True)
    if p.returncode not in rc_nhan:
        loi = p.stderr.decode("utf-8", "replace").strip()
        raise LookupError(f"git {' '.join(doi_so)} rc={p.returncode}: {loi}")
    return p


def doc_tep(rev, duong):
    return git("show", f"{rev}:{duong}").stdout.decode("utf-8")


def gon(van_ban):
    """Gộp khoảng trắng trong từng đoạn; đoạn cách nhau bằng dòng trống."""
    doan = re.split(r"\n[ \t]*\n", van_ban)
    return "\n\n".join(" ".join(d.split()) for d in doan if d.strip())


def cac_khoi(van_ban):
    """Đọc mọi khối `~~~ <loại> ...` của đặc tả: thay, cau, tieu_de, chuyen_tiep."""
    thay, cau, khac, dang_mo, dem = {}, {}, {}, None, []
    for dong in van_ban.splitlines(keepends=True):
        if dang_mo is None:
            m = re.fullmatch(r"~~~ (thay (SKILL|PROTOCOL) (\S+) (cu|moi)|cau (\w+) (\w+)|tieu_de|chuyen_tiep|ma_e)\n",
                             dong)
            if m:
                dang_mo, dem = m, []
        elif dong == "~~~\n":
            noi_dung = "".join(dem)
            if dang_mo.group(2):
                muc = thay.setdefault((dang_mo.group(2), dang_mo.group(3)), {})
                if dang_mo.group(4) in muc:
                    raise LookupError(f"khối thay trùng: {dang_mo.group(0).strip()}")
                muc[dang_mo.group(4)] = noi_dung
            elif dang_mo.group(5):
                if dang_mo.group(6) in cau:
                    raise LookupError(f"khối cau trùng: {dang_mo.group(6)}")
                cau[dang_mo.group(6)] = (dang_mo.group(5), noi_dung)
            else:
                if dang_mo.group(1) in khac:
                    raise LookupError(f"khối trùng: {dang_mo.group(1)}")
                khac[dang_mo.group(1)] = noi_dung
            dang_mo = None
        else:
            dem.append(dong)
    if dang_mo is not None or any(set(v) != {"cu", "moi"} for v in thay.values()) or not cau \
            or set(khac) != {"tieu_de", "chuyen_tiep", "ma_e"}:
        raise LookupError("khối bị hở, thiếu cặp cu/moi, hay thiếu khối cau/tieu_de/chuyen_tiep/ma_e")
    return thay, cau, khac


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


def cac_muc(adr, tieu_de):
    """{tiêu đề: văn bản của mục}; tiêu đề `## ` phải đúng danh sách và thứ tự."""
    dong = adr.split("\n")
    vi_tri = [i for i, d in enumerate(dong) if d.startswith("## ")]
    if [dong[i] for i in vi_tri] != tieu_de:
        raise ValueError(f"tiêu đề mục {[dong[i] for i in vi_tri]} khác danh sách")
    return {dong[i]: "\n".join(dong[i + 1:j]) for i, j in zip(vi_tri, vi_tri[1:] + [len(dong)])}


def o_bang(dong):
    return [o.strip() for o in dong.strip().strip("|").split("|")]


def main():
    duong_spec, base = sys.argv[1], sys.argv[2]
    with open(duong_spec, encoding="utf-8", newline="") as f:
        thay, cau, khac = cac_khoi(f.read().replace("\r\n", "\n"))
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
    if git("cat-file", "-e", f"{base}:{ADR}", rc_nhan=(0, 1, 128)).returncode == 0:
        loi.append(f"{ADR} đã có trên base")
    if git("cat-file", "-e", f"HEAD:{ADR}", rc_nhan=(0, 1, 128)).returncode != 0:
        loi.append(f"{ADR} chưa có ở ứng viên")
    else:
        loi += kiem_adr(doc_tep("HEAD", ADR), cau, khac)
    for x in loi:
        print("ĐỎ:", x)
    print("ĐẠT" if not loi else f"ĐỎ: {len(loi)} lỗi")
    return 1 if loi else 0


def kiem_adr(adr, cau, khac):
    loi = []
    dong = adr.split("\n")
    if not dong[0].startswith("# ADR-0067 — ") or not dong[2].startswith("- **Trạng thái:** Accepted ("):
        loi.append("dòng 1 hay dòng 3 của ADR sai mẫu")
    try:
        muc = cac_muc(adr, khac["tieu_de"].split("\n")[:-1])
    except ValueError as e:
        loi.append(str(e))
        muc = {}
    for ma, (ten_muc, van) in sorted(cau.items()):
        can = " ".join(van.split())
        if gon(adr).count(can) != 1:
            loi.append(f"câu {ma}: {gon(adr).count(can)} lần trong ADR, cần 1")
        elif muc and gon(muc.get(MUC[ten_muc], "")).count(can) != 1:
            loi.append(f"câu {ma} không nằm trong mục {MUC[ten_muc]}")
    for ten_muc, ds in CHUOI.items():
        for chuoi in ds:  # `(?!\w)`: `ADR-0060` M1 không được khớp nhờ `ADR-0060` M10
            if muc and not re.search(re.escape(chuoi) + r"(?!\w)", gon(muc.get(ten_muc, ""))):
                loi.append(f"mục {ten_muc} thiếu {chuoi}")
    hang_e = [o_bang(d) for d in muc.get(MUC["quyet_dinh"], "").split("\n") if d.startswith("|")]
    dong_e = khac["ma_e"].strip("\n").split("\n")
    for dong_m in dong_e:
        ma, dinh_nghia = (x.strip() for x in dong_m.split(" ; "))
        khop = [h for h in hang_e if h and h[0] == ma]
        if len(khop) != 1 or len(khop[0]) != 4 or khop[0][1] != dinh_nghia or not khop[0][2] or not khop[0][3]:
            loi.append(f"bảng E: hàng {ma} thiếu hay sai")
    if len([h for h in hang_e if h and re.fullmatch(r"E[0-9]+", h[0])]) != len(dong_e):
        loi.append("bảng E không có đúng năm hàng E1–E5")
    hang = [o_bang(d) for d in muc.get(MUC["hieu_luc"], "").split("\n") if d.startswith("|")]
    for dong_ct in khac["chuyen_tiep"].strip("\n").split("\n"):
        nhan, ma_e, hieu_luc = (x.strip() for x in dong_ct.split(" ; "))
        khop = [h for h in hang if h and h[0] == nhan]
        if len(khop) != 1 or len(khop[0]) != 5 or khop[0][3] != ma_e or not khop[0][4].startswith(hieu_luc) \
                or not khop[0][1] or not khop[0][2]:
            loi.append(f"bảng chuyển tiếp: hàng {nhan!r} thiếu hay sai")
    if len([h for h in hang if len(h) == 5 and not set(h[0]) <= set("-: ")]) != 14:
        loi.append("bảng chuyển tiếp không có đúng mười ba hàng nội dung (cộng hàng tiêu đề)")
    cuong_che = muc.get("## Cưỡng chế", "")
    for tep in CONG:
        if tep not in cuong_che:
            loi.append(f"mục Cưỡng chế thiếu {tep}")
        elif doc_tep("HEAD", tep).count("ADR-0067") != 0:
            loi.append(f"{tep} có nhắc ADR-0067, lời khai 0 cổng sai")
    return loi


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
| A1 | M2, M3 | `kiem_p2.py` rc 0: `PROTOCOL_DA_PHIEN.md` và `SKILL.md` ở ứng viên bằng đúng từng byte bản dựng từ base bằng các khối `thay` | trả một đoạn §12 về bản cũ; giữ câu *"Mọi push thêm vẫn cần checkpoint chủ kho"*; giữ định nghĩa E1–E3 cũ trong L7; ngắt dòng lại một đoạn mới ⇒ rc 1. Ngắt dòng lại ĐỎ là cố ý, như A1 của packet 1 |
| A2 | M1 | cùng script: ADR mới, vắng trên base; dòng 1 và dòng 3 đúng tiền tố; mười tiêu đề `## ` đúng thứ tự. Phần còn lại của dòng Trạng thái (ngày, Issue, URL comment duyệt) và nội dung mục Bối cảnh, Phương án bị loại, Giới hạn: reviewer đọc, **chưa có phép đo máy** | đổi thứ tự hai mục; xoá mục *Giới hạn* ⇒ rc 1 |
| A3 | M1 | cùng script: mỗi khối `cau` có đúng một lần trong ADR sau khi gộp khoảng trắng theo đoạn, và nằm trong đúng mục; bảng E có đúng năm hàng, cột 1 và cột 2 bằng đúng khối `ma_e` | bỏ vế *"không bao giờ được ghi thành `human_audited`"* của D5; bỏ *"hạn 30 ngày"* của D9; chuyển D12 sang mục khác; chép D1 hai lần; thêm chữ vào cuối ô định nghĩa E5 ⇒ rc 1. Ngắt dòng lại trong đoạn vẫn rc 0 (L6 vế b) |
| A4 | M1 | cùng script: khoá YAML, giá trị `loai`, khoá uỷ quyền thường trực, định danh mục *Thay những gì* có mặt trong đúng mục | xoá `hoan_tac` khỏi mục Sổ; xoá `` `ADR-0063` K4 `` ⇒ rc 1 |
| A5 | M1 | cùng script: bảng chuyển tiếp có đúng mười ba hàng nội dung; mỗi hàng của khối `chuyen_tiep` có đúng một hàng cùng nhãn, năm cột, cột 4 bằng mã E, cột 5 bắt đầu bằng mốc hiệu lực, cột 2 và 3 khác rỗng | đổi cột 5 của *Cấp lease* thành `từ land ADR này`; xoá hàng *Push thêm*; thêm hàng thứ mười bốn ⇒ rc 1 |
| A6 | M1 | cùng script: mục *Cưỡng chế* nhắc đủ sáu tệp cổng, và sáu tệp ở ứng viên nhắc `ADR-0067` 0 lần | xoá dòng `ci.yml` khỏi mục ⇒ rc 1 |
| A7 | phạm vi | cùng script: `git diff --name-only <base> HEAD` bằng đúng ba tệp | thêm `CONTEXT.md` ⇒ rc 1 |
| A8 | neo | cùng script: mỗi khối `cu` có đúng một lần trên base, không chồng nhau | base thiếu commit land của packet 1 (khối `cu` K7 vắng) ⇒ rc 3 |
| A9 | bất biến | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `python .claude/dev/packet_loop.py adr-song --root .` rc 0 (ADR mới có dòng §20); `git diff --check <base> HEAD` rc 0 | xoá dòng `ADR-0067` khỏi §20 ⇒ `adr-song` ĐỎ; chép một đoạn protocol mới vào `SKILL.md` ⇒ `doctrine-scan` rc 6 |
| A10 | bất biến (a) §12 | trên đúng SHA sẽ đẩy: `python scripts/tl.py --selftest` ra N/N với hai số bằng nhau | — (canh bất biến) |

Chạy thử trên base (ứng viên = base packet 1): A1–A7 ĐỎ, đúng màu "chưa làm"; A9 xanh sẵn. Bằng chứng chạy thử của từng
đột biến ghi ở biên nhận review đặc tả.

## 5. `luat_dung`

- (i) Trần lời gọi Codex review của PR thi công: mười, theo dòng khai ở đầu tệp. Chạm trần mà chưa approve ⇒ Review
  Rescue Checkpoint (`ADR-0037`); đó là E2.
- (i) Số lần push thêm và điều kiện merge: `ADR-0060` M5, M7 (mặc định theo `ADR-0062`). Packet chạm E5 nên chủ kho duyệt
  merge một lần neo SHA, theo cả luật hiện hành lẫn D7.
- (i) Cùng hình dạng lỗi lần thứ ba, hay tín hiệu không hội tụ: protocol §12. Phiên thi công tự xét lại cách làm và ghi lý
  do vào handoff; chỉ hỏi khi rơi vào E1 hay E3.
- (ii) E1: không còn phương án có phép đo chống đỡ, ví dụ ADR không giữ được dưới trần `ADR-0053` mà không bỏ một câu bắt
  buộc. E2: thiếu tài nguyên, ví dụ không có clone không shallow. E3: bằng chứng mâu thuẫn với một quyết định của chủ
  kho, ví dụ một câu bắt buộc trái với năm quyết định ngày 08-11-2026.

Không có ngân sách mềm. Câu bắt buộc hay khối `moi` mà reviewer chỉ ra là sai không sửa tại chỗ được, vì vị từ A1–A3
đòi nguyên văn: phiên thi công dừng và đề xuất revision đặc tả kèm văn bản mới; đó không phải điểm hỏi chủ kho.

## 6. Review và ngân sách

- Review đặc tả này (trước khi đóng băng): Codex offline trên commit cục bộ, chung một lượt với đặc tả packet 1. Đặc tả
  chạm E5 nên sau review approve vẫn chờ chủ kho duyệt băm.
- Review mã: Codex offline qua `launcher.py run`, `init --codex-review-calls-limit 10`, mỗi lời gọi ghi
  `record-codex-call`. Connector `@codex review` trên PR draft theo `ADR-0060` M6.
- Audit: packet chạm E5 nên cần chủ kho audit trên exact head (`ADR-0063` K4) trước merge.
- CI: không tự kích `workflow_dispatch`; Windows `not_required`, M9 không áp.

## 7. `ngoai_pham_vi`

- Mã cổng: `NGUOI_CO_THAM_QUYEN`, `record-lease`, `void-attempt`, `kiem-merge` K4–K7, `ops/lease_publish.py`,
  `ops/bien_nhan_v2.py`, cổng quét đặc tả thêm điểm hỏi ngoài E1–E5: packet 3 và 4 của lộ trình.
- Tự mở phiên kế nhiệm, phiên reviewer, job đăng bản tin tự động, tự merge: packet 5.
- Tạo Issue bản tin, đăng comment cấp uỷ quyền thường trực: việc vận hành sau khi cơ chế có hiệu lực, không thuộc diff.
- `CONTEXT.md`: thêm từ vựng (danh sách đóng, sổ quyết định uỷ quyền, bản tin, uỷ quyền thường trực, audit uỷ quyền)
  buộc phiên land tái sinh `RELEASE_MANIFEST.json`; để packet sau, định nghĩa nằm trong ADR.
- Sửa nội dung `ADR-0037`, `ADR-0060`, `ADR-0063` hay ADR nào khác: không hồi tố; mục *Thay những gì* của ADR mới nêu
  câu nào bị thay.
- Protocol §1 bất biến 5 (*"người có thẩm quyền gọi"* `land apply`): giữ nguyên câu chữ; tự merge theo D7 là uỷ quyền bền
  của người có thẩm quyền, khớp câu cuối của hàng *Người có thẩm quyền* ở §2.
- Adapter `work-packet`, `cross-review`, `land-packets` (Claude và Codex): đo ở S6, không có điểm hỏi nào phải sửa.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục.

## 9. `chua_do_duoc`

- Số lần chủ kho bị hỏi giảm bao nhiêu: chỉ đo được sau land các packet đổi cổng.
- Phiên audit uỷ quyền có thật sự bắt được E3: chưa có ca chạy thật; đo ở packet 4.
- Bản tin hằng ngày có đến được chủ kho đúng giờ không: phụ thuộc phiên điều phối mở trong ngày cho tới khi có job tự
  động (packet 5).
- Lời khai *"0 cổng"* của dòng §20 chỉ đúng lúc land; packet 3 phải sửa dòng ấy khi thêm cổng.

## 10. Quyết định người soạn tự đưa (chủ kho bác được khi duyệt băm)

Theo đúng luật đặc tả này viết ra, các điểm dưới đây không thuộc E1–E5 nên người soạn tự quyết và ghi lại thay vì hỏi:

1. Sổ quyết định là comment trên Issue của packet (D12), không phải tệp trong kho: mỗi mục một PR sẽ va làn sổ sách của
   `ADR-0060` M8; comment có URL ổn định để `can_cu` của lease hay `record-rescue` trỏ vào, khớp `CAN_CU_RE` của
   `packet_loop.py`.
2. Bản tin là comment trên một Issue riêng (D15–D17), không phải email: nằm trong control plane, đọc được trên Android,
   và một lần đăng ký theo dõi là đủ. Giờ Việt Nam vì chủ kho ở đó.
3. Uỷ quyền thường trực là một (không phải một cho mỗi Mission), hạn 30 ngày; Mission nào được tính thì do D11 quyết.
4. Hiệu lực tách theo cơ chế (D20 và bảng chuyển tiếp) để tài liệu không đi trước mã: nguyên nhân số 7 của tài liệu
   nguồn là *"Tài liệu và mã lệch nhau"*.
5. E4, E5 không rõ thì coi là thuộc (D2), cùng hướng fail-closed với `review_class`.
6. Số ADR là `ADR-0067` vì `ADR-0066` đã được #1265 giữ chỗ (S4). Nếu lúc cấp lease đã có tệp `docs/adr/0067-*` của packet
   khác, đặc tả cần revision; đo lại trước khi cấp.
