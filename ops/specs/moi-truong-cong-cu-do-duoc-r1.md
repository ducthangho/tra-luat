# ĐẶC TẢ PACKET — `MOI-TRUONG-CONG-CU-DO-DUOC`, revision 1

## Authority và identity

| trường | giá trị |
|---|---|
| `packet_id` | `MOI-TRUONG-CONG-CU-DO-DUOC` |
| `packet_issue` | **CHƯA MỞ** — đặc tả đóng băng TRƯỚC, Issue và lease đi sau. Skill `soan-spec` §5: spec KHÔNG phải lease; phiên nào đọc tệp này rồi bắt tay làm là tự cấp việc cho mình. |
| `revision` | 1 |
| `nguon_cap_viec` | Chỉ thị chủ kho, phiên điều phối 16-09-2026: *"Mở packet môi trường/công cụ đi"*, sau yêu cầu gốc cùng phiên: *"môi trường luôn phải đủ công cụ, biến môi trường cần thiết để chạy"*. Không phải một dòng trong kế hoạch thi công — đây là packet sinh từ phép đo của chính phiên ấy. |
| `review_class` | **`sensitive`** — `docs/PROTOCOL_DA_PHIEN.md:668` nêu đích danh *"launcher hoặc gate lifecycle"*. Không khai thấp hơn được. |
| `base` | `dd274415408bd1c6b4279c8e2cf9671057520f23` (`master`, đo 16-09-2026 13:2xZ) |

**Ngưỡng ADR-0044 cho `sensitive`: ≤ 3 tệp và ≤ 300 dòng thêm.** Write set dưới đây đúng **3 tệp**;
không xin ngoại lệ. Nếu lúc thi công vượt 300 dòng thêm thì **DỪNG và xin chủ kho khai ngoại lệ**,
đừng tự đi tiếp — bài học `PLAT-X8`: một con số trôi đã biến ô *"trần ADR-0044"* thành lời khai sai
về THẨM QUYỀN, không phải sai một chữ số.

## Baseline — số đã ĐO, không phải trí nhớ

Mọi số dưới đây đo **16-09-2026, khoảng 12:3xZ–13:2xZ**, trên `master dd27441` và trên máy Windows
của chủ kho. Đo lại trước mỗi bước công bố (skill `soan-spec` L5).

| phép đo | lệnh | kết quả |
|---|---|---|
| `doctor` có đo `actionlint`/`shellcheck` không | `grep -c 'actionlint\|shellcheck' .claude/dev/launcher.py` | **0** |
| hook có cài `actionlint` không | `grep -c 'actionlint\|shellcheck' .claude/hooks/session-start.sh` | **0** |
| hook có để lại DẤU VẾT nào không | đọc toàn tệp | **không có** — nên *"hook đã chạy chưa"* hiện **không đo được** |
| `CLAUDE_PROJECT_DIR` trong container remote này | `echo "${CLAUDE_PROJECT_DIR:-KHONG DAT}"` | **KHÔNG ĐẶT** ⇒ lệnh hook giải ra `/.claude/hooks/session-start.sh`, không có tệp |
| `AL_VER` ghim ở mấy chỗ trong `ci.yml` | `grep -c 'AL_VER:'` | **4** chỗ, đều `1.7.7` |
| `PYTHONUTF8` / `PYTHONIOENCODING` trong `ci.yml` | `grep -c` | **3** / **3** (mức job) |
| `launcher_test.py` | `grep -c '^def t[0-9]'` | **148 ca** |
| lease giữ 3 đường write set | `ops/lease_publish.py ai-dang-giu <đường>` | **NGƯỜI_GIỮ 0**, `rc=0`, cả ba |
| `lease_publish_test` trong container này, THIẾU `actionlint` | `python3 ops/lease_publish_test.py` | **152/155**, 3 ca `KHÔNG ĐO ĐƯỢC` (fail-close) |
| — cùng lệnh, SAU khi cài `AL_VER=1.7.7` | | **155/155**, `rc=0` |

**Phép đo hai vế trên máy Windows thật của chủ kho** (đơn vị: **ca test** của
`ops/lease_publish_test.py`, tổng 148, bỏ qua 7):

| vế | đỏ | đạt |
|---|---:|---|
| không đặt biến nào | 39 | **109/148** |
| đặt `PYTHONUTF8=1` + `PYTHONIOENCODING=utf-8` | 22 | **126/148** |
| CI `gate (windows-latest)`, cùng bộ test | 15 | **133/148** |

`126 + 6 + 1 = 133`, và tập đỏ của CI **nằm trọn** trong tập đỏ của máy chủ kho (`CI \ sau` = **RỖNG**).
Phần dư đúng bằng hai nguyên nhân đã đặt tên: **6** ca lớp B (đường dẫn có dấu cách) và **1** ca `t125`.

## Nguồn gốc — bốn lỗ, mỗi lỗ một phép đo

**L1 — `doctor` KHÔNG ĐO hai công cụ mà cổng cần.** Bảng `CONG_CU` không có mục nào cho `actionlint`
lẫn `shellcheck`. Hệ quả đo được ngay trong container này: `doctor` kết luận `KET LUAN: THIEU claude`
— không một chữ về `actionlint` — trong khi `lease_publish_test` cho `152/155` vì thiếu đúng nó.
Đây là lớp *"đếm sự CÓ MẶT thay vì KHẢ NĂNG"* mà `CLAUDE.md` khai đã trả giá bốn lần; lần này biến
thể là **không đếm gì cả**.

**L2 — hook KHÔNG CÀI `actionlint`.** Hook cài `ripgrep`, `@anthropic-ai/claude-code`, `@openai/codex`
— hết. Nên không có chuyện *"đã fix rồi mà hỏng lại"*: hai công cụ ấy **chưa bao giờ** nằm trong phạm
vi của hook.

**L3 — hook CÓ THỂ KHÔNG CHẠY LẦN NÀO, và `doctor` không nói ra.** Mục `hook-phien`
(`.claude/dev/launcher.py:3663`, `_do_hook_cu`) so **BĂM tệp hook** đang checkout với `origin/master`.
Nó trả lời *"tệp có mới không"*, KHÔNG trả lời *"hook đã chạy chưa"* — hai câu hỏi khác nhau, và tệp
mới tinh vẫn có thể chưa từng chạy. `CLAUDE.md` đã ghi đúng ca này (đo 17-08-2026) và chốt hiện tại
vẫn không bắt được nó.

**L4 — lỗi thiếu `encoding=` rộng hơn một tệp.** Đếm **lời gọi** `subprocess.run/Popen/check_output/
check_call` có `text=True` hoặc `universal_newlines=True` mà **không** nêu `encoding=`:
**112 lời gọi / 23 tệp** trong mã SỐNG (ngoài `ops/reviews/**`), trong đó `ops/lease_publish_test.py`
= **24**. Hiện vật review đã đóng băng dưới `ops/reviews/**` có thêm **67** lời gọi — **không đụng tới**.

> **ĐÍNH CHÍNH một con số của chính phiên soạn spec này.** Bản báo cáo miệng trước đó khai *"28 chỗ"*.
> **28** là số lần xuất hiện CHUỖI `text=True` trong một tệp, không phải số LỜI GỌI thiếu `encoding=`.
> Hai đơn vị khác nhau. Số đúng cho tệp ấy là **24**, và cho toàn kho sống là **112**. Ghi ra đây vì
> luật L1 của skill `soan-spec` sinh ra từ đúng lỗi này: con số nào cũng phải khai nó ĐẾM GÌ.

## Vì sao CI mù với L4

`ci.yml` đặt `PYTHONIOENCODING: utf-8` và `PYTHONUTF8: "1"` ở **mức job**, 3 chỗ mỗi biến. UTF-8 mode
đổi `locale.getencoding()`, nên `text=True` giải mã bằng UTF-8 và lỗi không bao giờ hiện. Máy chạy tay
không ai đặt hai biến ấy ⇒ máy Việt dùng **cp1258** ⇒ `UnicodeDecodeError` trong reader thread ⇒
`stdout` thành `None` ⇒ `TypeError: argument of type 'NoneType' is not iterable`.

Bài học gốc **đã có** trong `CLAUDE.md` (*"Console máy Việt là cp1258… Mọi CLI phải ép stdout/stderr
sang UTF-8 TRƯỚC khi in gì"*). Nó được **cưỡng chế ở CI** và **không** ở đường chạy tay. Đó là hình
dạng *"cổng vắng mặt ở đúng nơi nó cần"*, không phải hình dạng *"chưa ai biết"*.

## Objective

Mỗi mục chiếu vào MỘT đường dẫn trong `write_set` (skill `soan-spec` L2).

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | `doctor` **ĐO** `actionlint` và `shellcheck`: có/không, phiên bản, lệnh cài theo nền. Chúng **KHÔNG** được tính vào `DUNG_DUOC` của một đường nào — chỉ là mục công cụ, đúng bài học `t103` (*"chỉ đường LÀM ĐƯỢC VIỆC mới được tính"*). | `.claude/dev/launcher.py` |
| **M2** | `doctor` **ĐO** `PYTHONUTF8` và `PYTHONIOENCODING`, và **CẢNH BÁO** khi nền không phải UTF-8 mà hai biến vắng. In cả khi xanh (như phần biến môi trường hiện có), để không ai kết luận từ chỗ rỗng. | `.claude/dev/launcher.py` |
| **M3** | `doctor` **ĐO** *"hook đã CHẠY chưa"* bằng **dấu vết hook để lại**, tách hẳn khỏi mục `hook-phien` hiện có (mục ấy đo tệp có mới không — giữ nguyên, không thay). Ba trạng thái: `ĐÃ CHẠY` · `CHƯA CHẠY` · `KHÔNG ĐO ĐƯỢC`. | `.claude/dev/launcher.py` |
| **M4** | Hook **CÀI** `actionlint` qua `ops/cai_actionlint.sh` với `AL_VER` ghim **cùng một số** với `ci.yml`, **ĐẶT** `PYTHONUTF8`/`PYTHONIOENCODING`, và **GHI dấu vết** mà M3 đọc. Thất bại cài phải in cảnh báo, không được im lặng. | `.claude/hooks/session-start.sh` |
| **M5** | `doctor` **ĐO** đường dẫn kho: có dấu cách hoặc ký tự ngoài ASCII thì **NÊU RA** kèm số ca đã biết sẽ đỏ vì nó. Chỉ ĐO và BÁO — **không** vá `ops/cai_actionlint.sh` ở packet này. | `.claude/dev/launcher.py` |
| **M6** | Mỗi chốt của M1–M5 có phản chứng riêng trong bộ test launcher, và **mỗi chốt một đột biến** làm ca đích ĐỎ. | `.claude/dev/launcher_test.py` |

## Write set

Đúng ba đường, không ký tự đại diện. Đã quét lease toàn kho (`refs/heads/*` + `refs/remotes/origin/*`,
`comm -23` rỗng nên không mù): **NGƯỜI_GIỮ 0** cho cả ba, `rc=0`, đo 13:0xZ 16-09-2026.

```
.claude/dev/launcher.py
.claude/hooks/session-start.sh
.claude/dev/launcher_test.py
```

## Ngoài phạm vi — CỐ Ý không làm

| thứ | vì sao |
|---|---|
| **112 lời gọi thiếu `encoding=`** (23 tệp) | Sửa cơ học, rộng, lớp `systemic` — không thể nằm trong một packet `sensitive` trần 3 tệp. **Packet thứ hai**, làm SAU, vì nó chỉ đáng làm khi đã có cổng canh. Quyết định của chủ kho, 16-09-2026. |
| **`.claude/settings.json`** | Sửa nó là đổi hành vi khởi động phiên của mọi người dùng kho. M3 bắt được L3 bằng cách ĐO, không cần đổi cấu hình của ai. |
| **`ops/cai_actionlint.sh`, `ops/lease_publish_test.py`** (lớp B, 6 ca `t35`–`t40`) | Ngoài trần 3 tệp. M5 chỉ ĐO và BÁO; bản vá thật là packet riêng. |
| **`t125` / `AB_SUITE_DO_DUOC_GIAY`** (lớp G) | Không phải lỗi môi trường — là một hằng hiệu chuẩn trên MỘT máy (`= 350`, chú thích: *"đo Windows M4 lượt 4: t125 = 344.438 s"*) đang dùng làm ngân sách cho MỌI máy. Nâng số là đúng thứ chú thích ngay tại chỗ ấy cấm (*"nâng hạn ngoài cho tới khi hết treo là đổi cổng lấy sự im lặng"*). **Nợ có tên**, không vá ở đây. |
| **`/usr/bin:/bin` ở `ops/lease_publish.py:1106`** (lớp C, 12 ca) | Đã có **WP541**. Không gộp. |
| **`t150`** (Q13 policy) | Cùng WP541. |
| **`AL_VER` ghim 4 chỗ trong `ci.yml` có thể trôi lệch** | Tiền lệ đúng hình dạng đã có: `t31` canh `PyYAML` ghim cùng một bản. Cần một ca tương tự cho `AL_VER`, nhưng nó sống ở `ops/lease_publish_test.py` — ngoài write set. **Nợ có tên.** |

## Acceptance

**A1 — `doctor` ĐO hai công cụ, và ca ÂM phải tồn tại.** Chạy `doctor` trên một `PATH` **không có**
`actionlint` ⇒ đầu ra phải nêu nó thiếu kèm lệnh cài; chạy với `actionlint` trên `PATH` ⇒ phải nêu
phiên bản. **ĐỎ khi**: đột biến xoá mục `actionlint` khỏi `CONG_CU` mà ca đích vẫn xanh.
Đọc `rc` TRỰC TIẾP, không qua pipe.

**A2 — `doctor` ĐO hai biến, và KHÔNG được im lặng khi xanh.** Chạy với `PYTHONUTF8` vắng ⇒ phải có
cảnh báo; chạy với cả hai đặt ⇒ vẫn phải IN ra chúng. **ĐỎ khi**: đột biến làm phần biến chỉ in khi
thiếu (tức im lặng lúc xanh) mà ca đích vẫn xanh — đó chính là cách người đọc kết luận từ chỗ rỗng.

**A3 — M3 phân biệt được ĐÃ CHẠY với TỆP MỚI.** Bắt buộc **hai** ca, và chúng phải cho kết quả
KHÁC nhau trên cùng một cây: (a) tệp hook khớp băm `origin/master` nhưng **chưa chạy lần nào** ⇒
M3 báo `CHƯA CHẠY` trong khi `hook-phien` vẫn xanh; (b) hook đã chạy ⇒ M3 báo `ĐÃ CHẠY`.
**ĐỎ khi**: đột biến làm M3 đọc băm tệp thay vì dấu vết ⇒ ca (a) phải ĐỎ. Thiếu ca (a) thì không
biết M3 đang đo *"đã chạy"* hay đang đo lại đúng thứ `hook-phien` đã đo.

**A4 — hook cài và đặt, và `AL_VER` khớp `ci.yml`.** Ca đo: đọc `AL_VER` hook dùng và so **bằng
nhau** với cả **4** chỗ ghim trong `.github/workflows/ci.yml`. **ĐỎ khi**: đổi `AL_VER` ở hook thành
số khác ⇒ ca đích ĐỎ. (Chiều ngược — đổi trong `ci.yml` — thuộc nợ `AL_VER` ở trên, ngoài write set.)

**A5 — M5 nêu đúng đường dẫn nguy hiểm, và có ca ÂM.** Cây ở đường dẫn có dấu cách hoặc ký tự ngoài
ASCII ⇒ `doctor` NÊU RA; cây ở đường dẫn thuần ASCII không dấu cách ⇒ **không** nêu. **ĐỎ khi**:
đột biến bỏ phép kiểm ký tự ngoài ASCII (chỉ còn kiểm dấu cách) ⇒ ca đích ĐỎ. Thiếu ca âm thì không
biết cổng đang đo đường dẫn hay đang cảnh báo vô điều kiện.

**A6 — MỖI chốt MỘT đột biến riêng.** Đột biến chạy trên **BẢN SAO TẠM**, không đụng tệp thật
(bài học *"bom hẹn giờ"*: lượt chạy bị cắt thì `finally` không chạy và tệp ở lại méo). Đột biến bị
giết phải giết **đúng lý do** — chết bằng chốt của ca đích, không bằng một lỗi vô can; khai rõ ca nào
giết ca nào. **ĐỎ khi**: hai chốt không phân biệt được bằng đầu vào ⇒ chúng là bộ TƯƠNG ĐƯƠNG và
chỉ đang đo một cái.

**A7 — KHÔNG HỒI QUY.** `launcher_test.py` phải N/N với **hai số BẰNG NHAU**, và delta so nền
`dd27441` phải cho **0 ca đỏ mới**. Nền hiện đo được **148 ca**. Phép đo delta phải dựng **cả hai vế
trong MỘT lệnh, cùng rig**; và dùng **clone**, không dùng `git worktree` — `chay_cac_probe()` ném
`Chan(MA_WORKTREE)` khi `.git` là TỆP và sẽ đẻ ra hồi quy giả.

**A8 — CỔNG.** Trước khi báo xong, mỗi cái `rc=0`, đọc trực tiếp: `packet_loop.py doctrine-scan` ·
`packet_loop.py adr-song` · `tl.py doc-claims-check --strict` (`core.abbrev=7`) · `git diff --check` ·
`ops/bien_nhan_v2.py`. **`RELEASE_MANIFEST.json` nằm NGOÀI write set**: `.claude/**` không có trong
manifest nên sửa ba tệp này KHÔNG làm manifest lệch — nếu đo ra lệch thì **DỪNG và báo**, đừng tái
sinh manifest.

**A9 — REVIEW.** Xem mục *Đường review* dưới đây. Không `P1`/`P2` thì mới `approve`. Verdict + biên
nhận v2 commit vào `ops/reviews/` **TẦNG ĐẦU** (không thư mục con — `bien_nhan_v2` dòng 879 và 989,
`t26`/`t27` đều glob tầng đầu; đây là caveat vừa được đóng ở `r374`, đừng mở lại). Comment GitHub chỉ
là **bản chiếu**; nguồn có thẩm quyền là tệp có băm.

## Đường review — và nó đang có một mâu thuẫn phải nói thẳng

`docs/PROTOCOL_DA_PHIEN.md:668` cho `sensitive`: *"Phải có Codex `cross_approved` hoặc `human_audited`;
hết quota mà chưa có human thì pause."*

Đo 16-09-2026 13:1xZ, `launcher.py doctor --kiem-song` (đo SỐNG, không đọc dòng trạng thái):

| provider | kết quả |
|---|---|
| `codex` | **kiểm sống HỎNG, `rc=1`** — ảnh chụp token 165,6h đã bị vòng xoay vô hiệu; cộng connector báo hết quota trên PR #544 |
| `claude` | **CHƯA_XÁC_THỰC** — không có `~/.claude/.credentials.json`, không có biến |
| `doctor --kiem-song` | **`rc=12`** |

Và `antigravity` xuất hiện **0 lần** trong toàn bộ `docs/PROTOCOL_DA_PHIEN.md` — nó chưa phải provider
hợp lệ cho `cross_approved`.

**Quyết định chủ kho 16-09-2026: `human_audited` cho lượt này.** Không khai `cross_approved` bằng agy —
đó đúng lớp "khai vượt" mà biên nhận WP540 vừa bị cổng `bien_nhan_v2` bác.

**Nợ có tên, mở ra từ chính đây:** `PROTOCOL-CHUA-BIET-ANTIGRAVITY` — §8 viết khi kho chỉ có hai
provider, nên nó nêu đích danh *"Codex"* thay vì nêu *"provider KHÁC executor"*. Với executor
`antigravity`, `claude` LÀ provider khác, nhưng chữ của §8 không cho. Sửa §8 là packet `sensitive`
khác, và nó kẹt đúng vòng này — nên phải đi bằng `human_audited` ít nhất một lượt.

## Hình dạng kế thừa

`khong_ap_dung`. Đây **không** phải packet khắc phục: đo được rằng `actionlint`/`shellcheck` chưa bao
giờ nằm trong hook lẫn trong `CONG_CU`, nên không có biên nhận tiền nhiệm để chép bộ đếm hình dạng lỗi
sang. Chủ kho đã xác nhận không có Issue cũ để neo (16-09-2026).

**Nhưng bộ đếm bắt đầu từ 1, không phải 0**, cho một hình dạng đã đếm được ngay trong phiên này:
*"cổng/công cụ đo được cưỡng chế ở CI mà KHÔNG ở đường chạy tay"*. Thể hiện thứ nhất là L4
(hai biến UTF-8). Nếu packet này phát hiện thể hiện thứ hai và thứ ba, đó là lúc hỏi *"có nên làm
việc này theo cách đang làm không"* thay vì vá tiếp.

## Chưa đo được

| thứ | vì sao |
|---|---|
| **Lớp B có thật sự phụ thuộc đường dẫn không** | Phép thử một biến — clone kho sang `C:\tl` rồi chạy lại `ops/lease_publish_test.py` — **CHƯA AI CHẠY**. Sáu ca `t35`–`t40` xanh ở đó thì mới xác nhận; chưa có thì A5 đang dựa trên một suy luận từ thông điệp lỗi, không từ phép đo. Tiêu chí A5 vì thế chỉ đòi `doctor` **ĐO và BÁO**, không đòi chứng minh nhân quả. |
| **Reviewer độc lập** | Không phóng được từ container này (bảng trên). Mức assurance thật của lượt này do đường review quyết, không do đặc tả hứa. |
| **`AL_VER` trôi lệch giữa hook và 4 chỗ trong `ci.yml`** | A4 chỉ canh được chiều hook→ci. Chiều ci→hook cần một ca ở `ops/lease_publish_test.py`, ngoài write set. Nợ có tên. |
| **Container này thiếu `actionlint`** | Đã cài tay `AL_VER=1.7.7` vào `/tmp/actionlint` để đo `155/155`. Bản cài ấy **KHÔNG bền** — mất theo container. Phiên thi công phải cài lại và ĐO, đừng suy từ tệp đặc tả này. |

## Điều kiện dừng

Ba ca, dừng và báo chứ không tự đi tiếp:

1. **Vượt 300 dòng thêm** ⇒ dừng, xin chủ kho khai ngoại lệ ADR-0044 trước khi đẩy.
2. **Một mục tiêu M1–M6 cần sửa tệp ngoài 3 đường** ⇒ dừng; đó là phát hiện về chính đặc tả này, phải
   đi qua revision mới (§3.2), không được lặng lẽ nới write set.
3. **Cùng một hình dạng lỗi lặp lần thứ ba** ⇒ dừng, hỏi *"có nên làm việc này không"*, không hỏi
   *"vá thế nào"*.

## Ghi chú về băm

Tệp này đóng băng. Băm của nó là `spec_hash` trong lease. Cần đổi thì đi qua **revision 2**, không sửa
đè — sửa đè làm băm trong lease trỏ vào một thứ không còn tồn tại.
