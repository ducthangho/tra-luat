# ĐẶC TẢ ĐÓNG BĂNG — `N8-REVIEW-KEM-PATCH`

Packet Issue: #421 · Sinh từ phiên `2026-08-30`, sau lượt cross-review của #419/#420.

Đặc tả này ĐÓNG BĂNG khi lease neo băm của nó. Sửa sau khi cấp lease là làm `spec_hash` trỏ
vào thứ không còn tồn tại — đường đi vòng qua §3.2, không phải một lần sửa chính tả.

## 1. Vấn đề — nêu bằng phép đo

Đo `2026-08-30` trên ba finding của connector codex (PR #419, #420):

```
suggestion block : KHONG  (0/3)
diff / patch     : KHONG  (0/3)
do dai than      : 991 / 981 / 749 ky tu — thuan van xuoi
```

Findings **có hướng vá bằng lời** nhưng **không có bản vá áp được**. Người nhận phải tự dựng
lại bản vá từ văn xuôi, và đó là chỗ nghĩa bị trôi.

Đối chứng đo được trong cùng phiên: lượt cross-review **cục bộ** chạy `codex exec` với
`-c model_reasoning_effort=xhigh` và một prompt bắt buộc bốn phần (phép đo · phản chứng ·
bản vá · phân hạng) trả về **một P1 kèm diff `git apply --check` đi qua**, và P1 ấy là lỗi
THẬT mà lượt connector không thấy. Hai kênh, hai chất lượng khác nhau.

## 2. Hai kênh KHÁC NHAU — đừng gộp, vì chỉ một kênh sửa được từ kho

| kênh | trigger | model/effort đặt ở đâu | ta chỉnh được gì |
|---|---|---|---|
| connector GitHub | `PR opened`, `@codex review` | **ChatGPT cloud settings**, NGOÀI kho | chỉ ảnh hưởng qua `AGENTS.md` |
| `codex exec` cục bộ | skill `cross-review` | cờ CLI trong kho | đặt được `xhigh` trực tiếp |

Đo được: `codex exec -c model_reasoning_effort=xhigh` chạy `rc=0`. Còn effort của connector
**KHÔNG đặt được từ kho** — ai muốn đổi phải bấm ở `chatgpt.com/codex/cloud/settings/general`.
Packet này **KHÔNG** hứa đổi effort của connector; nói thẳng để không ai đọc nhầm.

Bằng chứng connector CÓ đọc `AGENTS.md`: hai finding của nó trích thẳng `AGENTS.md:L103-L105`
và `AGENTS.md:L29-L34` làm căn cứ. Nên `AGENTS.md` là đòn bẩy duy nhất với kênh ấy.

## 3. Write set — ĐÚNG 3 tệp

```
AGENTS.md
.claude/skills/cross-review/SKILL.md
RELEASE_MANIFEST.json
```

`RELEASE_MANIFEST.json` vào write set từ revision 2, KHÔNG phải vì packet nở phạm vi mà vì
phiên điều phối soạn THIẾU: `AGENTS.md` nằm trong manifest (`files[2]`) và `ci.yml` chạy
`release-verify --strict` **không có `if:`** — mọi packet chạm `AGENTS.md` mà không tái sinh
manifest đều ĐỎ CI theo kiến trúc.

CẢNH BÁO ĐÃ TRẢ GIÁ: khi mở write set ở r2, tôi sửa `write_set` và trần nhưng **quên §3 này và
quên dòng `S6`** — ba hiện vật cùng nói về một con số, tôi sửa một. Connector bắt được cả hai
(P1 trên PR #425). Ai nới write set lần sau phải sửa ĐỦ BA CHỖ: `write_set`,
`ngan_sach_kich_thuoc`, và dòng `S6` — cộng mục này.

Đo `2026-08-30`, cả hai `NGƯỜI_GIỮ 0` (`SKILL.md` chỉ có hai lease đã HẾT_HẠN).

## 4. Việc phải làm

### 4.1 `AGENTS.md` — mục `### Reviewer`

Thêm yêu cầu về **định dạng đầu ra của finding**. Mục ấy hiện quy định *verdict phải neo exact
`reviewed_sha`*, *khai đúng model/provider/transport* — nhưng **không dòng nào** nói finding
phải mang gì. Thêm: mỗi finding phải có **phép đo** (lệnh + output thật, hoặc khai
`KHÔNG ĐO ĐƯỢC` và vì sao), **phản chứng**, và **bản vá** dạng diff áp được hoặc patch plan
đánh số.

### 4.1b `AGENTS.md` — CON TRỎ sang §8 protocol về patch-as-hint, KHÔNG chép luật

Thêm ở mục `### Reviewer` **đúng một con trỏ**: quy tắc reviewer đính patch nằm ở
`docs/PROTOCOL_DA_PHIEN.md` §8 (patch là ARTIFACT không phải ref; nhãn nguyên văn bắt buộc;
executor phải tự áp và tự đo; `hint_provenance` bắt buộc khai; với packet `sensitive` chỉ đủ
điều kiện cho tệp TEST thuần hoặc tooling ngoài authority/gate/runtime).

**CẤM CHÉP NỘI DUNG LUẬT SANG `AGENTS.md`.** Ba lý do, và lý do thứ ba là lý do đắt nhất:

1. Protocol là nguồn quy tắc duy nhất; hai bản sẽ trôi lệch.
2. Bản protocol CHẶT HƠN mọi bản tóm tắt — nó phân loại theo LOẠI TỆP, thứ dễ bị bỏ khi tóm.
3. `doctrine-scan` quét `.claude/skills/**/*.md` và `CLAUDE.md`, **KHÔNG quét `AGENTS.md`** (đo
   30-08-2026 bằng cách đọc `cmd_doctrine_scan`). Nên nếu chép vào đó thì **máy sẽ không bắt
   được**. Cổng im lặng KHÔNG có nghĩa việc ấy đúng — đây đúng chỗ phải tự giữ kỷ luật.

Con trỏ nên ngắn: một tới hai dòng, theo giọng gạch đầu dòng của mục ấy.

Xuất xứ yêu cầu này: phiên điều phối trả lời một câu hỏi của chủ kho về "reviewer gửi patch,
executor áp thấy đạt thì có được approve luôn không" **bằng suy luận từ đầu**, rồi mới phát hiện
§8 đã quy định trọn vẹn và chặt hơn. Con trỏ này tồn tại để phiên sau tra được ngay, thay vì lại
nghĩ lại từ đầu.

### 4.2 `.claude/skills/cross-review/SKILL.md` — lệnh phóng codex

Lệnh hiện tại (dòng ~145) **không có cờ effort nào**:

```
codex exec -s workspace-write --skip-git-repo-check --cd <sandbox> - < PROMPT.md
```

Bảng model/effort ở đầu skill là của lane **Claude**, KHÔNG áp cho lane codex — nên lane codex
đang chạy ở effort mặc định một cách **im lặng**. Thêm `-c model_reasoning_effort=<bậc>` theo
đúng bảng thang đã có, và yêu cầu prompt mang bốn phần ở §4.1.

## 5. CHỐT BẮT BUỘC — cờ effort phải ĐO được, không được suy

Chính skill này đã ghi (đo 27-08-2026) rằng `--effort` sai tên **chỉ cảnh báo rồi lùi im lặng**
về mặc định, và `rc` lẫn `subtype` **cùng nói dối**. Nên:

- đặt `xhigh` xong **PHẢI đo** là nó có hiệu lực, không được suy từ `rc=0`;
- một bậc effort **không tồn tại** phải làm cổng ĐỎ, không được lùi im lặng;
- ba trạng thái: có hiệu lực · không có hiệu lực · **KHÔNG ĐO ĐƯỢC**, và cái thứ ba làm ĐỎ.

Chưa biết `codex exec` phơi bậc effort đã dùng ở đâu (log? JSON?). **Đó là việc phải ĐO trong
packet, không phải giả định.** Nếu đo ra là **không phơi ở đâu cả** thì phải khai thẳng
`KHÔNG ĐO ĐƯỢC` trong skill, chứ không được viết một câu hứa mà không ai kiểm được.

## 6. Điều kiện dừng

- `S1` cần đường dẫn thứ ba ngoài write set ⇒ DỪNG, trình phép đo.
- `S2` phát hiện phải sửa cấu hình ChatGPT cloud ⇒ DỪNG, đó NGOÀI kho và ngoài thẩm quyền packet.
- `S3` không đo được bậc effort đã dùng ⇒ **KHÔNG** được khai là đã đặt xhigh; ghi `KHÔNG ĐO
  ĐƯỢC` và trình người giữ.
- `S4` `origin/master` đi tiếp so `base_sha` mà chưa đo lại ⇒ DỪNG.
- `S5` muốn sửa `docs/PROTOCOL_DA_PHIEN.md` ⇒ DỪNG: adapter lệch protocol thì ADAPTER sai, và
  `doctrine-scan` sẽ đỏ nếu adapter chép doctrine.

## 7. Nghiệm thu

- `python .claude/dev/packet_loop.py doctrine-scan --root .` **rc=0** (adapter không chép doctrine).
- Phép đo chứng minh bậc effort có hiệu lực, HOẶC một khai báo `KHÔNG ĐO ĐƯỢC` tường minh.
- Không tự khai cổng ADR-0044 là ĐẠT.

## 8. Chưa đo được — gọi tên tử tế

- Connector có thật sự tuân `AGENTS.md` về ĐỊNH DẠNG đầu ra hay không — mới biết nó ĐỌC tệp ấy
  (nó trích số dòng), **chưa** biết nó tuân một yêu cầu định dạng. Chỉ lượt review kế tiếp mới trả lời.
- `codex exec` có phơi bậc effort đã dùng ở đâu không — xem §5.
