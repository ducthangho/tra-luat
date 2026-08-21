# VÒNG 2 — HỘI TỤ (Fable 5, worktree chỉ-đọc `th2/kho`)

Phép đo mới của lượt này, chạy trước khi trả lời (tất cả ĐO ĐƯỢC trừ khi ghi khác):
- `spec_path`/`spec_sha256` trong `ops/lease_publish.py`: **0 lần** — cổng CHƯA kiểm hai trường ấy;
  chính lease `plat-m4-exec-2-claude-20260821.yaml` tự khai "Cổng chưa cưỡng chế hai trường ấy
  (việc của gói V4); lease này khai trước để làm tiền lệ".
- `required_checks` trong `docs/PROTOCOL_DA_PHIEN.md`: chỉ hai stub `required_checks: []`
  (dòng 155, 256), là trường **dispatcher-phái-sinh** — và kho không có dispatcher.
- ADR-0044, đoạn cuối: gói cưỡng chế `ops/lease_publish.py` "**phải làm SAU hai slice** vì write
  set giao nhau" (ĐỌC ĐƯỢC). Điều kiện dừng #9 của `ops/THAM_DINH_KE_HOACH_20260821.md`: "mọi
  lease mới thiếu `spec_path` + `spec_sha256` ⇒ rc=6, KHÔNG NGOẠI LỆ" — đã duyệt sẵn.
- `ops-publish-lease.yml:203`: prompt được đọc **từ head được đẩy**, không từ master ⇒ không thể
  đòi prompt resolve từ ref bền tại lúc cấp; SPEC thì đòi được (spec phải đóng băng TRƯỚC lease).
- `t36`–`t40` **ĐÃ tồn tại** trong `ops/lease_publish_test.py` (41 ca) — khớp dòng 62 của bản
  thẩm định ("đã có"), dù bảng slice vẫn liệt kê như việc phải làm.
- V6 của kế hoạch V0–V6 đã ghi sẵn "sandbox reviewer fail-đóng" như việc vệ sinh (ĐỌC ĐƯỢC).

---

## D1 — Một thứ hay hai thứ? MỘT thứ, nhưng chỉ ở những transition ĐANG TỒN TẠI

**SUY LUẬN từ hai phép đo:** `evidence-preflight` của codex và ba cổng hẹp của tôi là MỘT thứ ở
hai độ hạt — *khi và chỉ khi* có một cửa chuyển state để đứng. Kho hôm nay có đúng HAI cửa như
vậy: (a) lúc cấp/đăng lease (`lease_publish.py` — có thật, có RC_NEO, có workflow gọi), và
(b) lúc phiên chính DỰNG một lượt review (hiện dựng bằng tay — chính là chỗ vỡ 4 lần). Độ hạt
"runner tự chạy `required_checks`" của codex đòi hai thứ CHƯA TỒN TẠI: danh sách check máy-đọc
(hiện là stub `[]`, ĐO ĐƯỢC) và policy trigger→check (§3.5 mới là văn bản). Xây đủ nó = xây
dispatcher — vượt xa một packet, và cả hai vòng 1 đã cùng từ chối control-plane mới.

**Tôi chốt (và đây là ĐỔI Ý về thứ tự so với vòng 1):** cái xây trong MỘT packet là
**preflight tại cửa DỰNG-LƯỢT-REVIEW** — tức hiện thân của evidence-preflight codex, thu vào
đúng một transition, với **danh sách check CỨNG TRONG MÃ** (không tự khai) — chứa luôn ba cổng
hẹp của tôi ở phía tiêu thụ. Chiếu lên 3 ca vòng 1:

| ca | packet này | cái bị loại (full runner) mất gì |
|---|---|---|
| 1 — `$?`×3 | CHẶN instance đã cắn lượt review (`\| tail` nuốt rc): script tự chạy lệnh reviewer, đọc `returncode` qua subprocess, không pipeline. Mẫu trong cây → lint lát 3 (ratchet-tại-không, DO_DOC_LAP §2 đã đo = 0). | Không mất gì thêm: full runner cũng chỉ chặn được ở transition. |
| 2 — manifest/ratchet | **KHÔNG CHẶN — khai thẳng.** | Cũng KHÔNG chặn được hôm nay: thuốc của codex ("trigger `docs/**` chọn full selftest") giả định bản đồ trigger→check chưa tồn tại. Cái "mất" là một LỜI HỨA, không phải một cơ chế. |
| 3 — kế hoạch chưa merge | CHẶN ở phía TIÊU THỤ: mọi tài liệu lease/prompt trích phải resolve trong bundle trước khi spawn reviewer — đúng ca đã làm hỏng lượt plat-m4. Phía CẤP (grant) chặn ở lát 2. | Không mất: counterfactual #3 của codex chính là lát 2, chỉ bị XẾP HÀNG, không bị loại. |

Cái thật sự bị loại là **độ hạt full-runner**, và thứ nó mất là ca 2 — thứ nó cũng chưa mua nổi.

## D2 — Điểm mù của `evidence-preflight` nguyên dạng

1. **Nguồn danh sách check — điểm mù chí tử.** ĐO ĐƯỢC: `required_checks` là trường
   dispatcher-phái-sinh và dispatcher không tồn tại ⇒ hôm nay danh sách sẽ do CHÍNH NGƯỜI VIẾT
   SPEC khai — người đang muốn xanh. Rút ngắn danh sách là miễn phí và hợp lệ về schema. Ai
   ngăn? Không ai; muốn ngăn cần policy engine §3.5 = dựng đúng cái control plane kho đã từ
   chối. Cách bịt duy nhất vừa một packet: danh sách CỨNG trong mã, đổi danh sách = sửa mã =
   qua review, kèm mutant "rút một check ⇒ ca đích ĐỎ" (SUY LUẬN, có tiền lệ PR #104: đột biến
   nới danh sách cho phép phải làm ca đích đỏ).
2. **Lách rẻ nhất:** receipt máy do runner local phát vẫn là **self-report** — không ai đọc
   ngược thứ ĐÃ ĐẾN (đúng bài học tầng vận chuyển của kho). Forge receipt bằng tay không gì
   phân biệt được, cho tới khi một chốt phía sau ĐÒI receipt ấy theo băm.
3. **Báo động giả tệ nhất:** chạy lại heavy check ở mọi transition là TRÙNG CI — kho có hẳn
   skill `gate-targeted` sinh ra để *tránh* lặp full exact-SHA đã có trên CI (ĐỌC ĐƯỢC). Runner
   chậm ⇒ áp lực rút ngắn danh sách ⇒ **cơ chế tự đẻ đường lách của chính nó**. Cộng: fetch
   canonical qua mạng — "không đo được" phải là trạng thái thứ ba tách khỏi "đỏ", kẻo đỏ vặt
   vì mạng dạy người ta bypass.
4. **Chi phí ẩn:** runner đứng cùng bậc tin cậy với `lease_publish.py` — một mặt cắt authority
   mới, mà bài học "chốt chỉ một cửa đọc" đòi mỗi cửa một mutant riêng. Kho vừa đo được mình
   đang nghẹt quản trị (4 merge/ngày); thêm một thành phần authority là thêm nợ review vĩnh viễn.

## D3 — `chi_la_chu: true`: tôi ĐỔI Ý một nửa — codex đúng, nó là NỢ

- Ghi vào đâu: receipt/khối bài học mới, cộng một dòng trong `ops/NO_KY_THUAT.md`.
- Ai đọc: NGƯỜI, ở bước V6 "sổ nợ là SỔ". Máy không đọc giá trị ấy để quyết gì cả.
- **Phép đo làm nó ĐỎ: KHÔNG CÓ.** Tỷ lệ `chi_la_chu/tổng` không có ngưỡng chặn ⇒ là báo cáo,
  không phải bảo đảm. Đặt ngưỡng ratchet thì phản tác dụng: phạt đúng người chịu khai bài học,
  thưởng người im lặng — ngược 180° mục tiêu (SUY LUẬN).
⇒ Nói thẳng theo yêu cầu đề: **giá trị `chi_la_chu: true` là CHỈ LÀ CHỮ**, và tôi rút chữ ký
vòng 1 khỏi cách diễn đạt "sản phẩm phụ là bảng kiểm kê đo được" — bảng ấy có thật nhưng không
phải thứ để ký như bảo đảm. Thứ còn ký được là phần SCHEMA (cấm im lặng: hoặc `rxx` có răng,
hoặc khai nợ kèm lý do) — và nó KHÔNG nằm trong packet này, để dành cho gói V4.

## D4 — Chọn `plan_impact` enum của codex. ĐỔI Ý so với vòng 1

Khác nhau về thứ MÁY kiểm được: enum trỏ vào **hậu quả đã có định nghĩa trong protocol** —
`packet_revision` ⇒ kiểm được revision/generation mới tồn tại và lease cũ mất hiệu lực (§3.2);
`mcr_candidate` ⇒ kiểm được quyết định người trong MCR (§3.1.1); `new_mission` ⇒ issue tồn tại.
`mcr: <id>|null` của tôi chỉ là NHÁNH `mcr_candidate` của enum ấy.

**Ca enum bắt mà của tôi trượt (ĐỌC ĐƯỢC từ §3.2):** bài học làm sai SPEC CỦA PACKET nhưng không
đụng mission — schema của tôi cho phép `mcr: null + lý do` và im lặng hợp lệ về packet revision;
enum ép chọn `packet_revision` và máy kiểm được một revision mới đã sinh. Chiều ngược lại không
có ca nào enum trượt mà của tôi bắt. Giữ đúng một rider của tôi: `none` bắt buộc kèm người quyết
+ lý do (CẤM IM LẶNG). Là việc của gói V4, không thuộc packet này.

## D5 — PHẠM VI: MỘT packet, write set tối thiểu

**Packet ký (lát 1): `dung-sandbox-review` — script dựng sandbox reviewer fail-đóng.**
Class `systemic` (không đụng authority: không cấp lease, không sửa workflow). Write set:

```
ops/dung_sandbox_review.py          (MỚI — ~300–400 dòng)
ops/dung_sandbox_review_test.py     (MỚI — fixture tái dựng CẢ 4 sự cố + mutant từng check)
.claude/skills/cross-review/SKILL.md  (vài dòng adapter: trỏ tới script, đúng vai adapter mỏng)
```
3 tệp, ước +600–800 dòng ⇒ lọt trần packet thường của ADR-0044 (≤6 tệp, ≤1.000 dòng). Không giao
với write set slice A (`cai_actionlint.sh` + wrapper + `lease_publish_test.py`) hay slice B
(workflows + t25/t34/t35) ⇒ **không bị ADR-0044 xếp hàng, mở được NGAY** (ĐO ĐƯỢC từ bảng slice).

Bốn check cứng trong mã (mỗi check một mutant riêng — cửa không mutant là cửa hở lại):
1. **Neo trích dẫn:** mọi cặp (path, sha256) mà lease + prompt trích phải resolve TRONG bundle,
   đúng băm, trước khi spawn — chặn hình dạng "prompt trỏ tệp không có trong cây" (sự cố 1).
2. **Đủ bundle:** mọi vật lease liệt kê phải có mặt — chặn "bundle thiếu lease X4" (sự cố 2).
3. **rc trực tiếp:** script tự chạy lệnh reviewer qua subprocess, đọc `returncode`, cấm pipeline
   trên đường đọc mã thoát — chặn "`| tail` nuốt rc" (sự cố 3).
4. **Thăm dò GHI thật:** ghi thử một tệp vào đích báo cáo ngoài `./kho` rồi đọc lại, trước khi
   spawn — chặn "`-s read-only` nuốt báo cáo" (sự cố 4, lượt codex vòng 1).
Trạng thái ra: `có` · `không` · `KHÔNG ĐO ĐƯỢC` — trạng thái ba làm ĐỎ, in receipt máy kèm băm.

**Lát 2 (SAU slice A/B, theo đúng câu xếp hàng của ADR-0044):** trong `ops/lease_publish.py` +
`ops/lease_publish_test.py` — cưỡng chế `spec_path`+`spec_sha256` (điều kiện dừng #9 đã duyệt)
VÀ `spec` phải resolve đúng băm từ ref bền (`origin/master` hoặc `luu-tru/*`) TẠI lúc chạy cổng,
rc=6. Fixture đỏ: tái dựng đúng ca −1h53m/−1h28m của DO_DOC_LAP §4. Phạm vi chỉ SPEC, không
prompt — vì đã đo: workflow đọc prompt từ head được đẩy (dòng 203), đòi prompt trên master tại
lúc cấp là báo động giả cấu trúc. Đây là TOI_KY #3 vòng 1 của tôi + counterfactual #3 của codex,
giữ nguyên chữ ký, chỉ xếp sau vì write set.

**Lát 3 (ghép vào bất kỳ packet vệ sinh nào):** lint `$?`-sau-pipeline, ratchet-tại-không
(DO_DOC_LAP §2: 0 chỗ phải sửa), fail-close khi thiếu công cụ.

## D6 — Có, CẤM dựng tay; và CÓ, nó đi TRƯỚC mọi cạnh ở D1

**ĐO ĐƯỢC:** hình dạng "phiên chính dựng sandbox/bundle hỏng lượt review" = 4 lần/3 ngày ≥
ngưỡng 3 của chính kho ⇒ theo luật kho, câu hỏi đúng là "có nên dựng tay nữa không" — trả lời:
KHÔNG. Ba lý do nó đi trước:
1. Ngưỡng hình dạng đã vượt ở ĐÂY (4 lần), còn hình dạng grant-side mới đỏ 2 lần trong lịch sử.
2. **Write set rời** — mở được ngay hôm nay; lát 2 (grant-side) bị chính ADR-0044 xếp sau hai
   slice. Chọn thứ tự này không phải vì lát 2 kém quan trọng mà vì hàng đợi ĐO ĐƯỢC.
3. Script biến lớp sự cố mới nhất thành fixture chạy được — đúng doctrine "nghĩ ra phép thử mà
   không chạy thì phép thử không tồn tại": bốn sự cố đang là văn xuôi trong DO_DOC_LAP.

Script phải cưỡng chế đúng bốn check ở D5 — bốn sự cố, bốn check, bốn mutant, không thêm.

**Khai thẳng giới hạn (đừng để tôi nói quá như bài học "PHẠM VI TUYÊN BỐ = phạm vi ĐO ĐƯỢC"):**
lệnh CẤM "mọi lượt review phải qua script" là **CHỈ LÀ CHỮ** chừng nào chưa có chốt máy phía sau
đòi receipt của script (không gì ngăn phiên chính vẫn dựng tay). Cái MÁY được trong packet này
là: *nếu* script được chạy thì nó fail-đóng, không thể sinh ra sandbox hỏng theo 4 kiểu cũ. Cửa
đóng nốt phần chữ: gói V4 (lát 2) thêm một trường trong lease review trỏ receipt preflight theo
băm — hook đã để sẵn, không ký trước ở đây.

---

## TOI_KY

1. **Packet `dung-sandbox-review`** (write set 3 tệp ở D5, 4 check cứng, mutant từng check,
   fail-đóng, ba trạng thái, receipt máy) — **CƯỠNG CHẾ MÁY** cho hành vi của script; riêng mệnh
   đề "mọi lượt review phải đi qua nó" là **CHỈ LÀ CHỮ** cho tới khi lát 2 đòi receipt — khai
   thẳng ngay trong SKILL.md adapter.
2. **Lát 2 — grant-side, sau slice A/B:** cưỡng chế `spec_path`+`spec_sha256` + resolve từ ref
   bền tại lúc cấp, rc=6, fixture tái dựng ca −1h53m — **CƯỠNG CHẾ MÁY**. (Giữ nguyên chữ ký
   vòng 1, thêm thứ tự.)
3. **Lát 3 — lint `$?`-sau-pipeline** ratchet-tại-không, fail-close thiếu công cụ — **CƯỠNG CHẾ
   MÁY**. (Giữ nguyên chữ ký vòng 1.)
4. **`plan_impact` enum của codex** + rider `none` phải kèm người quyết và lý do — **CƯỠNG CHẾ
   MÁY** ở phần kiểm hậu quả (revision mới tồn tại / MCR có quyết định / issue tồn tại); việc
   CHỌN giá trị enum là **CHỈ LÀ CHỮ** có người chịu trách nhiệm. ĐỔI Ý: bỏ schema `mcr: id|null`
   riêng của tôi. Thuộc gói V4, không thuộc packet 1.

## TOI_KHONG_KY

1. `evidence-preflight` nguyên dạng full-runner: danh sách check tự khai trong spec khi chưa có
   dispatcher/policy engine — điểm mù D2.1 chưa có lời giải ngoài danh-sách-cứng-trong-mã.
2. `chi_la_chu: true` như bảo đảm hay "bảng kiểm kê đo được" — ĐỔI Ý vòng 1: không phép đo nào
   làm nó đỏ ⇒ nó là NỢ, chỉ ký phần schema cấm im lặng (và để V4).
3. Lệnh cấm dựng-tay bằng VĂN BẢN không kèm script — chữ không chặn ai; ký script, không ký câu.
4. Giữ nguyên mọi mục TOI_KHONG_KY vòng 1 của cả hai bên đã hội tụ: `hinh_dang_lap>=3` tự khai ·
   `doi_ke_hoach.can` boolean/oracle · chỗ đựng thứ 8 · KG/vector DB · hook in lời nhắc hàng loạt ·
   cổng "cùng seam" khi seam chưa máy-đọc (DO_DOC_LAP §1 đã xác nhận 0/24, 0/41).

## KHONG_DO_DUOC (khai)

- Kích thước thật của script (+600–800 là ƯỚC; nếu vượt 1.000 dòng thì tách test fixture sự cố
  3–4 thành packet nối tiếp trên integration branch, theo đúng §288-291).
- Môi trường phiên chính có fetch được `luu-tru/*` lúc chạy check neo hay không — phải đo khi thi
  công; không fetch được thì check ra `KHÔNG ĐO ĐƯỢC` (đỏ), không được im lặng tha.
- Trạng thái THẬT của kế hoạch V0–V6: `t36`–`t40` đã có trong cây trong khi bảng slice vẫn ghi
  như việc phải làm ⇒ slice A có thể đã land; nếu CẢ A lẫn B đã land thì hàng đợi ADR-0044 đã mở
  và lát 2 có thể đi song song — không đọc được điều này từ worktree, phải hỏi người giữ.
- Chi phí giờ-người của 4 lượt review hỏng — vẫn chỉ có lời kể, chưa có số.
- Hiệu quả hành vi của mọi lớp văn xuôi (baseline không tồn tại) — như vòng 1, không đổi.
