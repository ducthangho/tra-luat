# ĐẶC TẢ PACKET — WP570-BASH-NEN-MOT-BO-GIAI, revision 12

- **Issue:** https://github.com/ducthangho/tra-luat/issues/570
- **Trạng thái:** ĐÓNG BĂNG khi lease `wp570-bash-nen-r12-g12-fable` được cấp. Mọi thay đổi
  objective / acceptance / write set / executor / environment ⇒ revision mới, generation mới,
  cấp lại lease (§3.2 `docs/PROTOCOL_DA_PHIEN.md`).

## 0. Vì sao có revision 12 — ĐỔI EFFORT xuống `low`, và BỐN mặt của "đọc INDEX cho đúng"

r12 tồn tại vì **hai** lý do độc lập.

### Lý do thứ nhất: chủ kho hạ EFFORT của cả executor lẫn reviewer xuống `low`

Chỉ thị 2026-09-23: *"Executor: fable 5.1, effort **low**. Review codex gpt-6-astra, effort
**low**."* r11 đóng băng `effort: medium` cho cả hai, **và §7.0 nêu đích danh hai con số ấy**.
Đổi một thuộc tính của executor ⇒ `docs/PROTOCOL_DA_PHIEN.md` §3.2 đòi revision + generation
mới — cùng hình dạng r8 (đổi executor `claude` → `fable`). Không phải một sửa nhỏ trong lease.

### Lý do thứ hai: cross-review codex vòng 6 trên `1d63f80` — 4 × P2, tái hiện cả bốn

| | đo được trên `1d63f80` |
|---|---|
| **F12** `git replace` | sau `git replace <xấu> <sạch>`: `ngoai_danh_sach` **RỖNG**; đặt `GIT_NO_REPLACE_OBJECTS=1` ⇒ `['vi_pham.py']` |
| **F13** INDEX chưa hoà giải | `ls-files -s` phát stage **1/2/3**; bản ghi rơi mất trường stage ⇒ blob SHA lớn nhất thắng ⇒ `ngoai=[]` |
| **F14** PEP 263 / BOM | `# coding: latin-1` và BOM UTF-8 đều ra `rc=3 KHONG_DO_DUOC` — Python **hợp lệ** chặn vĩnh viễn cả kho |
| **F15** `VI_PHAM.PY` / `.pyw` | `ls-files --cached -s -- '*.py'` trả **RỖNG** ⇒ cả hai vô hình |

**F12 là MẶT THỨ TÁM của lớp *phán quyết phụ thuộc trạng thái LOCAL của máy*** — nhưng nó
**không** đòi một quyết định kiến trúc thứ ba. Nó là đúng món **nợ spec r11 đã KHAI TRƯỚC**:
*"Danh sách biến git bị gỡ KHÔNG BAO GIỜ ĐỦ… Một biến git mới mà r11 chưa biết sẽ KHÔNG bị gỡ."*
Nợ ấy nay đến hạn. Cơ chế không đổi (gỡ môi trường + ghim nguồn đối tượng), chỉ thêm một biến
và một cờ. Ghi ra để người sau phân biệt *"lớp sống lại"* với *"nợ đã khai đến hạn"*.

**F15 là thực thể THỨ BA của lớp *so khớp theo MỘT cách viết*** (sau hoa/thường ở r7 và hằng
byte ở r11). Lần thứ ba thì chữa bằng **cơ chế**: hậu tố ra một hàm `_la_nguon_py` dùng
`casefold()`, và pathspec `*.py` bị bỏ hẳn — lọc trong Python, không nhờ git so chuỗi.

### Một khuyết tật của chính bản vá r12, tự bắt trước khi đo

Bản đầu đặt HAI hàng rào cho ref thay thế ở **hai nơi** (biến môi trường trong
`_moi_truong_git_sach`, cờ `--no-replace-objects` tại chỗ gọi). Hậu quả: **không đột biến nào
đo được cái nào** — bỏ một hàng rào thì hàng rào kia vẫn che, nên ca đích vẫn xanh. *Một luật
không thể ĐỎ thì không phải luật.* Đã gom cả hai vào **một** hàm `_chay_git`, nơi dựng mọi tiến
trình git con của cổng; một đột biến gỡ cả hai, và `t47` chốt (1) ĐỎ được.

## 0. Vì sao có revision 11 — LỚP ẤY CÒN PHỦ "BYTE NÀO" và "INDEX NÀO", và CỔNG CHƯA TỪNG ĐƯỢC NỐI

Cross-review codex vòng 5 trên `6131cbd` ra **1 × P1 + 5 × P2** — **P1 đầu tiên** của packet.
Executor **đo lại cả sáu, cả sáu tái hiện chính xác**.

### P1 — cái cổng cả packet sinh ra để dựng CHƯA TỪNG được nối vào chỗ nó gác

`.github/workflows/ci.yml` gọi `python ops/cong_cu_test.py` ở **BA** chỗ và **KHÔNG** chỗ nào
gọi `ops/bash_nen.py quet`. `main()` thì chỉ chạy ca trên cây **GIẢ** cộng bán kính đột biến.
Đo lại trên một **bản sao kho** (không chạm tệp ngoài write set), **bằng chứng dương**:

```
them `vi_pham_moi.py` co shutil.which("bash") roi `git add`:
  python3 ops/bash_nen.py quet --root .  =>  rc=2 DO, ngoai_danh_sach=['vi_pham_moi.py']
  python3 ops/cong_cu_test.py            =>  rc=1 (chi la nen t2_go_canary)
                                             ten tep vi pham xuat hien 0 LAN trong ca bao cao
```

Một cổng không ai gọi thì không phải cổng. Đây là hình dạng **nặng nhất** packet gặp: bốn
revision trước đi hoàn thiện một cái cổng mà không ai kiểm xem nó có được cắm vào không.

### Hai P2 là MẶT THỨ SÁU và THỨ BẢY của lớp r9 đã "giết bằng kiến trúc"

| mặt | đo được trên `6131cbd` |
|---|---|
| **symlink** — mục `*.py` trong INDEX là symlink | `read_text()` đi theo **ra ngoài kho**; sửa tệp đích bên ngoài làm phán quyết đổi `['ops/lien_ket.py']` → `[]` trong khi INDEX **không đổi một byte**, `nguon_tep` vẫn khai `git` |
| **`GIT_INDEX_FILE`** kế thừa | cùng một kho: index THẬT trả `['bad.py']`, đặt `GIT_INDEX_FILE` trả `[]` — **cả hai lần đều khai `nguon_tep=git`** |

r9 lấy **DANH SÁCH** từ INDEX và tưởng thế là giết xong lớp *phán quyết phụ thuộc trạng thái
LOCAL của máy*. Nhưng lớp ấy còn phủ **"BYTE nào"** (nội dung vẫn đọc từ cây làm việc) và
**"INDEX nào"** (`git -C` không ghim được kho khi biến môi trường chọn index có mặt).
Chủ kho quyết ở r11: **nội dung cũng lấy từ INDEX** (`cat-file --batch` trên blob đã stage),
và **gỡ mọi biến git chọn kho / chọn index / tiêm cấu hình** khỏi tiến trình con.
Đây là lần thứ HAI chủ kho quyết kiến trúc cho cùng một lớp — ghi ra vì nó là dữ kiện về LỚP,
không phải về một bản vá.

### Ba P2 còn lại — hai trong số đó là mặt mới của hai lớp đã có tên

- **`global` / `nonlocal`** (lớp của N27: *phân loại ràng buộc theo TÊN mà bỏ một TRƯỜNG*).
  Sai **cả hai hướng**: `def f(): global subprocess; import subprocess; …run(["bash"])` ⇒ `[]`
  (LỌT một lời gọi thật); `def f(): global subprocess; subprocess = gia()` rồi gọi ở module ⇒
  `[(5, 0)]` (OAN). `nonlocal` cùng bệnh: `[(6, 4)]`.
- **walrus trong comprehension** (cùng lớp). PEP 572: `:=` trong comprehension ràng buộc ở
  phạm vi **CHỨA** nó. Bỏ qua ⇒ `[(3, 0)]` — cổng CHẶN một phép che hợp lệ.
- **hằng byte** (lớp *so hằng theo MỘT kiểu biểu diễn*, cùng lớp với mặt hoa/thường ở r7).
  `shutil.which(b"bash")`, `run([b"bash"])`, `run(b"bash")`, `executable=b"bash"`,
  `which(b"BASH.EXE")` — **cả năm** ra `[]`, một đường vòng không cần phân tích luồng dữ liệu.

### CÁI GIÁ, khai thẳng

- **Tệp đã `git add` rồi sửa tiếp trên đĩa được quét ở DẠNG ĐÃ STAGE.** Cổng thôi phản ánh đĩa.
  Trong CI không khác gì (checkout sạch); tại chỗ nghĩa là "cổng xử thứ anh đã stage" — đúng
  mạch N23. `t46` chốt (3) trói đúng đánh đổi ấy.
- **Mục `*.py` là symlink ⇒ fail-close có tên.** Đo trên kho hôm nay: `git ls-files -s -- '*.py'`
  có **0** mục mode `120000` trên **264** — luật này không tốn gì ở hiện tại, nó là hàng rào cho
  ngày mai.
- **Danh sách biến git bị gỡ KHÔNG BAO GIỜ ĐỦ.** Đó chính là lý do nó đi KÈM việc đọc blob:
  hai hàng rào phải cùng thủng thì phán quyết mới sai. Một biến git mới mà r11 chưa biết sẽ
  KHÔNG bị gỡ — ghi ra thay vì để người sau tưởng danh sách là đủ.
- **Nhánh `nonlocal` chỉ đo được theo CHIỀU BỚT OAN.** `nonlocal x` đòi `x` đã bị ràng buộc ở
  một phạm vi hàm bao, nên tên ấy **luôn** có ≥2 ràng buộc ⇒ bộ giải luôn trả `None`. Không
  dựng được ca dương cho nhánh ấy; khai thẳng thay vì giả vờ phủ hai chiều.
- **Fixture nguyên văn của codex cho `global` vẫn ra `[]` sau khi vá** — nhưng vì **lý do khác
  và đúng**: nó có thêm `subprocess = object()` ở module, nên tên bị ràng buộc **hai lần** ⇒ mơ
  hồ ⇒ bộ giải từ chối theo luật bảo thủ của chính nó. Ca cô lập (`def f(): global subprocess;
  import subprocess; …`) nay **BẮT** `[(4, 4)]`, tức cơ chế codex nêu ĐÃ được vá.

## 0. Vì sao có revision 10 — CỬA SAU của một lớp đã tưởng giết xong, và một PHƯƠNG PHÁP được đóng băng

r10 tồn tại vì **hai** lý do, và cả hai đổi tiêu chí nghiệm thu nên §3.2 đòi revision mới.

### Lý do thứ nhất: N23 để hở một đường LÙI, và đường ấy mở lại đúng cái lớp r9 vừa giết

Cross-review codex vòng 4 trên `e290f99` ra **2 × P2**. Executor **đo lại cả hai, cả hai tái
hiện chính xác** — không nhận lời khai:

| | Đo lại được trên `e290f99` |
|---|---|
| **F5** không fail-close khi INDEX hỏng | cây có `.git` GIẢ ⇒ `_liet_ke_py` trả `rac_bi_ignore.py` kèm `rglob-git-hong`; `quet` ra **`rc=2 DO`** |
| **F6** `ImportFrom.level` bị bỏ qua | `from .subprocess import run; run(args=["bash"])` ⇒ **`[(2, 0)]`** — bắt oan một API nội bộ |

**F5 KHÔNG phải "một lỗi nữa".** Lớp *phán quyết phụ thuộc trạng thái LOCAL của máy* đã lộ BỐN
mặt qua ba bản vá nối tiếp, và r9 giết nó bằng kiến trúc: danh sách = INDEX, không còn luật
ignore nào để nghe. Nhưng r9 **giữ lại một đường LÙI** khi git hỏng, và trên đường ấy danh sách
lại là `rglob` — tức lại nghe trạng thái máy. r9 **đặt tên** cho đường lùi (`rglob-git-hong`)
với lý lẽ *"người đọc phải thấy"*. Một **TRƯỜNG** cho người đọc không phải một **CỔNG**: đúng
thứ `CLAUDE.md` gọi là *lời dặn bằng miệng không phải hàng rào*, lần này nằm trong chính mã của
packet. Không lấy được INDEX thì **không có danh sách**, nên **không có phán quyết**.

**Quét theo LỚP ra mặt thứ BA codex không chỉ.** Chỉ thị chủ kho: *"cross-review tìm kiếm, phân
theo LỚP, không phải từng lỗi riêng lẻ"*. Lớp của F6 là *"một ràng buộc được phân loại theo cái
TÊN mà bỏ qua một TRƯỜNG của nút AST quyết định ý nghĩa"*. Ba mặt, **hai chiều ngược nhau**:

| mặt | chiều | đo được trước vá | codex chỉ? |
|---|---|---|---|
| `ImportFrom.level >= 1` | **bắt oan** | `[(2, 0)]` | có |
| `import subprocess.x` (ràng buộc `subprocess` vào module THẬT) | **bỏ sót** | `[]` | **không** |
| `from subprocess import *` | bỏ sót | `[]` | không — **nợ có tên** từ trước, không phải mặt mới |

### Lý do thứ hai: PHƯƠNG PHÁP của vòng lặp chưa từng được đóng băng ở đâu

Chủ kho (phiên 2026-09-21 ~18:2xZ, nhắc lại 2026-09-23) đổi điều kiện thoát vòng lặp từ *"tới
khi APPROVE"* sang **"tới khi không còn finding P1, P2, P3"**, và ghi thêm phương pháp: review
bằng **codex phiên bản/effort cao hơn**, **hint patch** cho vấn đề phức tạp, **phân theo lớp
lỗi**, **đăng verdict** mỗi vòng, **không CI** tới khi đủ điều kiện merge, **không cần CI
Windows** (lỗi đã biết từ trước).

**ĐO, không đoán:** spec r9 §7 chỉ liệt kê điều kiện dừng của **EXECUTOR**; `dieu_kien_dung`
của lease g9 cũng vậy. **Không chỗ nào** ghi điều kiện thoát của VÒNG LẶP REVIEW. Nên đây là
**ghi lần đầu**, không phải sửa một tiêu chí đã đóng băng. Nó vào §7.0.

### CÁI GIÁ, khai thẳng

- `KHONG_DO_DUOC` **nhiều hơn** trước: mọi cây có `.git` mà git hỏng (hết giờ, rc khác 0, không
  sinh được tiến trình) nay làm cổng dừng thay vì ra số. Đó là **cố ý** — `None ≠ False`.
- `rglob` **vẫn sống** cho cây KHÔNG phải kho git. Bộ ca dựng cây giả phụ thuộc đường ấy, nên nó
  có ca giữ riêng (`t44` chốt (2)); thiếu chiều ấy thì một đột biến *"lúc nào cũng
  KHÔNG_ĐO_ĐƯỢC"* sẽ sống và cả bộ ca chết theo.
- **LỠ HẠN LEASE g9 ĐÃ TỐN MỘT NGÀY.** g9 hết hạn 2026-09-22T06:25Z với bản vá r10 đã viết xong
  nhưng chưa land. Phiên KHÔNG tự gia hạn, KHÔNG đẩy — đúng luật — và cái giá là 26 giờ. Ghi ra
  để hạn của g10 được đặt theo phép đo ấy chứ không theo thói quen.

## 0. Vì sao có revision 9 — GIẾT CẢ MỘT LỚP BẰNG KIẾN TRÚC, không vá mặt thứ tư

r9 **thu hẹp N17**. Đó là đổi tiêu chí nghiệm thu, nên `docs/PROTOCOL_DA_PHIEN.md` §3.2 đòi
revision mới. N17 (r4) khai *"cổng quét TOÀN CÂY"*; r9 đọc lại cho đúng: **toàn cây, phần
ĐÃ THEO DÕI** — danh sách tệp là `git ls-files --cached`, không hơn.

### Lý do: một lớp đã vá BA mặt nối tiếp, và mặt thứ tư đo được

Lớp *"phán quyết phụ thuộc trạng thái LOCAL của máy chạy"*:

| vòng | mặt được bịt | mặt hở ra |
|---|---|---|
| 1 | thư mục rác (`node_modules/`) — `rglob` chạm cả thứ `.gitignore` đã loại | `core.excludesFile` TOÀN CỤC |
| 2 | `core.excludesFile`, `.git/info/exclude` | `.gitignore` CHƯA THEO DÕI trong cây làm việc |
| r8 | blob `.gitignore` ĐÃ THEO DÕI, `XDG_CONFIG_HOME` | **kho nào trả lời** khi `.git` lồng nhau |

Mỗi bản vá **đúng, có răng, và để hở mặt kế**. `CLAUDE.md` gọi tên hình dạng ấy: *"vá đúng chỗ
được chỉ rồi bỏ sót đường thứ ba"*. Đến mặt thứ ba, executor **DỪNG** theo `dieu_kien_dung` và
hỏi *"có nên làm việc này không"* thay vì *"vá mặt thứ tư thế nào"*.

**Gốc của cả lớp là một quyết định kiến trúc ở r7:** cổng quét cả tệp **CHƯA THEO DÕI**, nên nó
buộc phải tự trả lời *"tệp nào bị ignore"* — và câu ấy **luôn còn một tầng máy nữa**.

**CHỦ KHO QUYẾT: chỉ quét INDEX.** Khi cổng không đọc luật ignore nào, cả lớp **chết theo kiến
trúc**, không phải theo bản vá. ~110 dòng kho tạm + trích blob bị gỡ hẳn.

### CÁI GIÁ, khai thẳng — đây là một ĐÁNH ĐỔI, không phải một tính chất tự nhiên

Tệp **chưa `git add`** không được quét. Trong CI cây luôn đã commit nên độ phủ không giảm; tại
chỗ, ai quên `add` sẽ thấy ở PR. **Câu sau là LÝ LẼ về CI, CHƯA ĐO** — ghi đúng như thế.

Hệ quả đo được: `ls-files --cached -- '*.py'` = **264 tệp**, `--others` thô = **0** ⇒ chênh **0**
trên kho hôm nay. Con số ấy **sẽ khác** trên một cây có tệp chưa add.

Và kỳ vọng "nhanh hơn" **KHÔNG THÀNH**: `quet` kho thật 3,04 / 3,04 / 3,12s, so HEAD 2,8–3,1s.
Chi phí nằm ở `ast.parse` 264 tệp, không ở việc liệt kê (6–8ms ở cả hai bản). Khai ra thay vì
im, vì một kỳ vọng sai được giữ lại sẽ thành lý lẽ cho quyết định sau.

## 0. Vì sao có revision 8 — ĐỔI EXECUTOR sang Fable 5.1

r8 không bác r7. Nó đổi **executor**, và `docs/PROTOCOL_DA_PHIEN.md:115` nói rõ đó là thứ đòi
revision mới: *"Packet đổi objective/acceptance/write-set/dependency/**executor**/environment
phải có [revision mới, generation mới, cấp lại lease]"*. Chạy executor khác dưới lease g7 —
vốn khai `executor: claude` — là thi công ngoài thứ lease khai, đúng loại sai mà `t24` (ghi
chú SAI SỰ THẬT) sinh ra để bắt.

**Chỉ thị chủ kho** (phiên 2026-09-21 ~16:1xZ): *"Sử dụng fable7.1 executor cho #581 tới
approve"*.

### "Fable 7.1" KHÔNG TỒN TẠI trong môi trường này — khai thẳng thay vì đoán

Phiên **không** tự dịch "7.1" thành một bản có thật. Nó DỪNG và hỏi, vì lệch phiên bản đúng là
loại nhầm lẫn packet này đã trả giá ở bộ đo `570-do-9` (chạy đúng nhưng trên **cây sai**, và
không có chốt nào bắt). Đo được trong môi trường phiên:

```
Agent model enum:  sonnet | opus | haiku | fable
Fable duy nhất với tới được:  claude-fable-5-1   (Fable 5.1)
```

Chủ kho xác nhận **Fable 5.1**. Lease g8 khai `model: claude-fable-5-1`, **không** khai "7.1".

### CÁI GIÁ, khai trước khi ai phải tự tìm ra

Executor mới **không sống qua** bảy lần lặp của hình dạng *"một ca khẳng định KẾT QUẢ trong khi
thuộc tính phải trói là CƠ CHẾ"*, cũng không sống qua năm lần mắc bẫy *"đột biến tệp không cắn
được mã đã nạp trong tiến trình"*. Những bài học ấy hiện chỉ sống ở ba chỗ:

1. **Đặc tả này** (N20, N21, N22 và §0 của r4/r6/r7);
2. **Docstring từng ca** — mỗi ca nêu THUỘC TÍNH nó trói ngay dòng đầu;
3. **Cổng đo được** — 44 ca, 52 đột biến, bán kính 1/44, cộng luật `t39` (N22).

Chỗ (3) là chỗ duy nhất **không phụ thuộc trí nhớ ai**. Đó là lý do việc đổi executor ở giữa
packet chịu được: thứ giữ chất lượng là **phép đo**, không phải người. Nhưng nói cho đủ —
`t39` chỉ bắt hình dạng "chốt trên PHÁN QUYẾT"; lần thứ BẢY (chốt cuối của `t41`) **không**
phải hình dạng ấy nên nó lọt qua `t39` và chỉ bị **bán kính đột biến** bắt. Phần còn lại vẫn
dựa vào người đọc. Đó là **nợ có tên**, không phải chỗ đã kín.

### Cái KHÔNG đổi

`assurance_target: human_audited` và `cross_reviewer_requirement` giữ nguyên: **cấm
`self_review` và `self_approve`**. Đổi executor **không** làm Fable được tự duyệt. *"Tới
approve"* trong chỉ thị nghĩa là **codex hết finding** cộng **chủ kho nghiệm thu** — không
phải executor tự tuyên bố xong.

Và một ràng buộc kế thừa: phiên claude hiện tại **là tác giả** của bản vá đang nằm trong #581,
nên nó cũng không được đóng vai reviewer cho Fable ở phần mã ấy. Vai của nó từ r8 là **điều
phối và đo**, không phải duyệt.

## 0. Vì sao có revision 7 — BỐN finding P2 của codex, và một LUẬT cho bộ ca

r7 không bác r6. Nó nhận một lượt **cross-review codex**, và — quan trọng hơn — nhận một
**hình dạng lỗi đã lặp SÁU lần** mà `dieu_kien_dung` bắt phải dừng lại từ lần thứ ba.

### Bốn finding — đo lại cả bốn, cả bốn tái hiện chính xác

Connector `codex` hồi phục hạn mức (lượt trước trên #571 nó trả *"You have reached your Codex
usage limits"*) và review `55f9bce` lúc 07:35–07:44Z: `COMMENTED`, **4×P2**, tất cả trên
`ops/bash_nen.py`. Executor **đo lại** thay vì nhận lời khai:

| | codex khai | executor đo được |
|---|---|---|
| **A** ratchet tha CẢ TỆP | thêm lời gọi thứ hai vào mục khai 1 vẫn `DAT` | `rc=0 DAT`, `co_loi_goi_tran=[2,3]` |
| **B** quét cả thư mục bị `.gitignore` | báo động giả | `node_modules/x.py` ⇒ **DO**; `hong.py` ⇒ **rc=3 KHONG_DO_DUOC** |
| **C** khoá cache thiếu `cwd`/`PATHEXT` | trả bản nhớ sai | đổi `cwd` ⇒ **cùng kết quả** |
| **D** tên thực thi so PHÂN BIỆT hoa/thường | `BASH.EXE` lọt | `BASH.EXE` ⇒ `[]`, `Bash.exe` ⇒ `[]` |

**D đắt nhất:** cổng vừa mở ra toàn cây bị **đi vòng bằng một phím Shift**, trên đúng cái nền
mà packet này sinh ra để phục vụ. **B nặng hơn lời khai:** vế *fail-close CẢ KHO* vì một tệp
rác không phân tích được là executor đo thêm — codex không nói.

Cách vá: (A) mỗi mục `CHUA_CHUYEN` mang **số lần được phép**, lệch chiều nào cũng ĐỎ;
(B) **hỏi git** (`ls-files --cached --others --exclude-standard`) thay vì chép một danh sách
cấm, và khai `nguon_tep` ba trạng thái; (C) `getcwd()` + `PATHEXT` vào khoá — khai thẳng rằng
`PATHEXT` **chưa đo được** trên nền Linux, nó vào khoá vì lý lẽ đọc từ mã; (D) `casefold()`
một phía, kèm chắn `isinstance(str)`.

### Hình dạng lặp lần thứ SÁU — lý do thật khiến r7 tồn tại

Một ca khẳng định **KẾT QUẢ / PHÁN QUYẾT** trong khi thuộc tính nó phải trói là một **CƠ CHẾ**,
hoặc là thứ ca khác **đã** trói:

| | chỗ | bắt ở |
|---|---|---|
| 1 | `_ket_luan_ban_kinh` in NGUYÊN NHÂN khi mới chỉ ĐẾM | r4 |
| 2 | `t33` chốt (3) cấm chuỗi trên TOÀN docstring | r4 |
| 3 | `t35` chốt (1) khẳng định `rc == 2` — thuộc tính của `t25` | r4 |
| 4 | `t34` khẳng định `sau == khac` — cơ chế là KHOÁ CACHE | r6 |
| 5 | `t38` khẳng định `t1 != t2` — giá trị trả về là chuỗi TƯƠNG ĐỐI | r7, bắt trước khi đẩy |
| 6 | `t37` chốt (3) khẳng định `rc == 2` — lại thuộc tính của `t25` | r7, cổng bán kính bắt |

`dieu_kien_dung` của g6 ghi: *"Một hình dạng lỗi lặp lần thứ BA ⇒ DỪNG, hỏi **có nên làm việc
này không**, không hỏi **vá thế nào**."* Đã quá gấp đôi ngưỡng, và mỗi lần chỉ lộ ra **sau**
một lượt đột biến 55 phút.

**CHỦ KHO QUYẾT: thêm LUẬT, không vá từng ca** — chỉ thị 2026-09-21, chọn *"Thêm LUẬT cấm,
không vá từng ca"* trong ba phương án đã trình (hai phương án kia: chỉ sửa `t37`; hoặc dừng
hẳn). Đó là **N22**.

## 0. Vì sao có revision 6 — `t34` ĐỎ trên Windows, và NGUYÊN NHÂN CHƯA ĐO ĐƯỢC

r6 không bác r4. Nó nhận một **phép đo Windows** mà r4 chưa có, và sửa một khuyết tật nằm trong
**chính bộ đo** của r4.

**Vì sao có khoảng trống generation 5.** `wp570-bash-nen-r5-g5-bia-mo` là một lease **bia mộ**,
`write_set` RỖNG, cấp 2026-09-20T19:44Z theo chỉ thị *"thu hồi sớm lease g4 của #570 bằng bia
mộ đi"* (`issuecomment-5752188461`), với lý do **packet đã LAND** (PR #571 merge `395bc7b1`).
Đo lúc 2026-09-21T01:4xZ: `ai-dang-giu` trả `NGƯỜI_GIỮ 0` cho cả bốn đường — thu hồi **đã có
hiệu lực thật**, không phải khai suông.

**Nhưng tiền đề "packet đã LAND" là KHÔNG ĐỦ, và đây là chỗ phải ghi thẳng.** Bản merge
`395bc7b1` mang r3: `thu_muc = goc / "ops"`, `CHUA_CHUYEN = {}`, 35 ca. Ba finding của
cross-review **không nằm trong bản đã merge**; chúng còn dang dở lúc `af0d261` được lấy, và nay
sống ở PR **#581** (`c0bc5a5`). Tức lease bị thu hồi trên một tiền đề đúng-một-nửa. Không ai
làm sai: người ra chỉ thị đọc "PR đã merge" là hợp lý. Ghi ra để lần sau *"packet đã land"* được
đọc là **"nhánh đã hết việc chưa?"**, không phải *"có PR nào merge chưa?"*.

### Phép đo sinh ra r6

Bộ đo `570-do-10` (máy chủ kho, 2026-09-21, HEAD `c0bc5a5`, chốt cây ĐẠT) đóng **hai** finding
và mở lại **một**:

| | Trên Windows, bản `c0bc5a5` |
|---|---|
| **F1** độ phủ | ✅ ĐÓNG — `E_hinh_dang_PHU_bi_bo_sot: []`, `E_hinh_dang_KHONG_PHU_bi_bat_oan: []` |
| **F2** phạm vi | ✅ ĐÓNG — `pham_vi: toan-cay`, 4 tệp/11 lời gọi đều trong `chua_chuyen`, `ngoai_danh_sach` rỗng |
| **F3** cache | ❌ **CHƯA ĐÓNG** — `t34` ĐỎ, `cong_cu_test: 37/38 đạt` |

```
ĐỎ  t34_cache_tim_bash_phai_theo_doi_MOI_TRUONG:
    trước='C:\Program Files\Git\bin\bash.exe'
    đặt  ='…\Temp\tmppjuaw8uq\bash'
    nhận ='C:\Program Files\Git\bin\bash.exe'
```

Và vì `t34` đỏ **độc lập với mọi đột biến**, nó tự cộng vào bán kính của **từng** đột biến —
19 dòng `ĐỎ … bán kính 2/38`. Chúng là **hệ quả của một ca đỏ**, không phải 19 khuyết tật. Đây
là lần đầu kho đo được hình dạng ấy, và nó đáng ghi: *một ca đỏ cố định làm hỏng phép đo bán
kính của TOÀN BỘ bộ đột biến*.

### NGUYÊN NHÂN: KHÔNG ĐO ĐƯỢC — hai giả thuyết, log không phân biệt nổi

- **(a)** khoá cache vẫn nuốt môi trường trên Windows;
- **(b)** cache **đã** tính lại và có XÉT ứng viên mới, nhưng ứng viên bị **năng lực** từ chối
  nên bộ giải lùi về Git Bash — tức `tim_bash` làm đúng việc của nó.

Cả hai **dự đoán cùng một `nhận == trước`**, nên con số ấy không phân biệt được. Thứ phân biệt
được là `chan_doan` của lần gọi **thứ hai** — mà cả `t34` lẫn phép `F` của bộ đo đều **vứt nó
đi** (`sau, _ = tim_bash()`). Đúng bài học `_ket_luan_ban_kinh` đã ghi ở r4: khẳng định một kết
quả trong khi ném mất bằng chứng giải thích nó.

Có một dấu hiệu **khớp hình dạng** (b): `t34` làm `shutil.copy2(bash → tmp/'bash')`, tức một bản
sao **trơ**, mất đuôi `.exe` và không có DLL bên cạnh; trên Git for Windows, `bash.exe` cần
`msys-2.0.dll` nằm cùng thư mục. Trên Linux bản sao chạy được nên Linux xanh. **Khớp hình dạng
KHÔNG phải đã đo** — r6 không viết nó thành nguyên nhân, r6 dựng phép đo phân biệt được.

## 0. Vì sao có revision 4 — MỞ PHẠM VI CỔNG ra TOÀN CÂY

r4 không bác r3. Nó mở **phạm vi quét của cổng**, và lý do là một lượt cross-review ĐO ĐƯỢC,
không phải một ý hay.

Lượt `advisory_review` trên `05ec2eb5` (PR #571, 20-09-2026T15:56Z, `VERDICT.md`
sha256 `59eec0aa4245a0a6073799f3085dae778e4eee1dad5e32bab0a554cdd3c22ef6`) ra
`verdict: changes_requested` với ba finding. Phiên executor **đo lại cả ba** thay vì nhận lời
khai, và **cả ba tái hiện chính xác**:

| finding | reviewer khai | executor đo lại |
|---|---|---|
| F1 `_loi_goi_tran` khai "MỌI" | BẮT 3 / LỌT 9 trên 12 hình dạng | BẮT 3 / LỌT 9 |
| F2 cổng chỉ phủ `ops/**` | 11 lời gọi / 4 tệp ngoài phạm vi | 11 / 4, y hệt danh sách |
| F3 cache bỏ qua môi trường | `B != C` khi đặt `CONG_CU_BASH` sau lần gọi đầu | khoá cache `[[], false]`, B≠C |

**F2 là cái đắt nhất, và nó bác một câu của chính packet này.** PR mở đầu bằng *"một bộ giải
dùng chung + một CỔNG chặn bản sao thứ tư"*. Nhưng bản sao thứ tư **đã sống sẵn ngoài hàng
rào** trước khi cổng ra đời:

```
.claude/dev/launcher_test.py:6004
    bash = (shutil.which("bash") if not LA_WINDOWS else
            ("C:/Program Files/Git/bin/bash.exe" if Path(...).exists() else shutil.which("bash")))
```

Đó là một bộ giải RIÊNG quyết bằng **ĐƯỜNG DẪN GHI CỨNG** — đúng hình dạng vừa bị gỡ khỏi
`_bash_posix` (r2) và `_bash_windows` (r3). Và `.claude/hooks/session_start.py:58` chạy ở
**mọi phiên**.

Nên r3 §N4 khoanh cổng vào `ops/**` là một lời khai **hẹp hơn thứ packet hứa**, trong khi
docstring của cổng lại khai **rộng hơn thứ nó làm**. Hai cái sai ngược chiều nhau, gặp nhau ở
giữa thành một cổng trông như đã chặn xong.

**CHỦ KHO QUYẾT: mở phạm vi ra toàn cây** (chỉ thị 20-09-2026 ~16:0xZ, chọn "Mở phạm vi cổng ra
toàn cây" trong ba phương án đã trình: thu hẹp lời khai · mở phạm vi · để nguyên).

**KHAI THẲNG CÁI GIÁ:** ratchet sẽ **DÀI RA** thay vì ngắn đi — từ rỗng lên 4 mục. Đó là đi
ngược tinh thần "ratchet phải NGẮN đi" của N5/N13. Chấp nhận có điều kiện: mỗi mục phải mang
**NGÀY GỠ** và lý do đo được, và N13 được viết lại cho đúng (xem §5). Một danh sách dài ra mà
không có ngày gỡ thì đúng là nghĩa trang mà N5 sinh ra để chặn.

## 0. Vì sao có revision 3 — MỞ WRITE SET sang `ops/cong_cu.py`

r3 KHÔNG bác r2. Nó mở đúng một đường, vì hai điều kiện đã đổi và cả hai đo được.

**(a) Lý do loại trừ của r2 đã hết hiệu lực.** r2 §4 viết: *"`ops/cong_cu.py` — hợp nhất
`_bash_windows` vào `ops/bash_nen.py` là việc ĐÚNG nhưng lease `wp541-path-r3-g3-claude` khai
nó trong `khong_duoc_cham`"*. Lease ấy **đã bị thu hồi** bằng bia mộ hai chiều (lease kế nhiệm
`wp541-path-r4-g4-bia-mo`). Đo 20-09-2026T05:05Z, đọc `rc` TRỰC TIẾP:

```
ai-dang-giu ops/cong_cu.py   rc=0   NGƯỜI_GIỮ 0: không có
```

Tức rào chắn không còn là "có người khác giữ" mà chỉ còn là write set của chính packet này —
thứ sửa được bằng revision. Đây là lý do DUY NHẤT r2 nêu để loại `ops/cong_cu.py`.

**(b) Phép đo Windows lượt 5 cho một lý do THUẬN mà r2 chưa có.** Bộ đo `570-do-5`
(`DO-570-LUOT5.ps1`, `sha256 01a2bc92e69aa735212490f5b5d35dc73b6c9a1ca9936939d88f2e7a1e97a6cc`,
`HEAD 4fc3ca8f`): đột biến `t22_bash_lay_ca_system_root` cho bán kính **không đọc được** trên
Windows, và **hai lượt cho hai kết quả KHÁC NHAU**:

| lượt | HEAD | bán kính | ca oan | phân hạng |
|---|---|---|---|---|
| `570-do-3` | `42dd49db` | 9/31 | `t3 t4 t7 t8 t9 t11 t21 t24` | tất cả `giet_that` |
| `570-do-5` | `4fc3ca8f` | 2/32 | `t2` | `tin_dung_gia` |

Cùng đột biến, cùng máy, cách ~2,5 giờ, và `_bash_windows` / `_chay` / tám ca kia KHÔNG đổi giữa
hai commit. **Nguyên nhân của chênh lệch ấy đứng ở `KHÔNG ĐO ĐƯỢC`** — cấm dựng giả thuyết cho
nó, y như hai chỗ chưa khép ở §6.

Nhưng thứ ĐO ĐƯỢC đủ để ra quyết định: `t22` tồn tại **chỉ để canh một bộ lọc theo TÊN**
(`%SystemRoot%`) trong bộ giải RIÊNG thứ hai. Đó đúng hình dạng *"danh sách CẤM không bao giờ
đủ"* mà §2 đã nêu, và là bộ giải cuối cùng còn sót. Hợp nhất nó vào `tim_bash()` làm bộ lọc theo
tên biến mất, `t22` mất đối tượng, và cả lớp bất ổn này chết **theo KIẾN TRÚC** chứ không theo
bản vá — đúng cách kho đã thoát khỏi "bảy phát hiện cùng một đường".

**KHAI THẲNG MỘT CÁI GIÁ.** Hợp nhất bây giờ thì mất phép so trước/sau cho câu hỏi ở (b).
Phiên này đã nêu cái giá ấy và chủ kho quyết vẫn làm (chỉ thị *"Cấp lease r3/g3 đi, rồi chuyển
cong_cu.py"*). Ghi ra đây để không ai đọc ngược rằng câu hỏi ấy đã được trả lời — nó **bị bỏ
lại**, không bị giải.

**(c) r2 có một lời khai nay đã cũ.** r2 §6 ghi hợp nhất `_bash_windows` là *"ngoài phạm vi"*.
r3 đưa nó VÀO phạm vi. Không xoá câu cũ ở §6 mà đánh dấu — một đặc tả sửa lặng lẽ lời khai cũ
là thứ khó kiểm nhất.

## 0. Vì sao có revision 2 — r1 SAI ở ba chỗ, và phép đo là thứ chỉ ra

r1 không bị bác về hướng. Nó sai ở ba câu, và cả ba chỉ lộ ra sau khi lượt đo Windows
`570-do-3` chạy thật (`DO-570-LUOT3.ps1`, `sha256 99380e45ee03f361a18c040686c78ad1bced2cd4787f4099c81ba862829666ad`,
log 20-09-2026T01:49 giờ máy).

**(a) Điều kiện bắt đầu KHÔNG BAO GIỜ THOẢ ĐƯỢC.** r1 §7 và `DIEU_KIEN_BAT_DAU` của lease g1
viết *"cho tới khi `ai-dang-giu` trả `rc=0` / `NGƯỜI_GIỮ 0`"*. Nhưng lease của CHÍNH packet này
giữ `ops/lease_publish_test.py`, nên `NGƯỜI_GIỮ` không bao giờ về 0 trong khi lease còn sống.
Ý định là *"không còn người giữ NÀO KHÁC"*. Câu viết quá rộng, và một điều kiện không thoả được
sẽ bị người sau lặng lẽ diễn giải lại — đó là cách một chốt chết mà vẫn trông như còn sống.

**(b) N9 KHÔNG ĐO ĐƯỢC bằng công cụ đang có.** r1 đòi log Windows cho thấy
`C:\Windows\system32\bash.EXE` *"đã được THỬ rồi bị TỪ CHỐI vì phép argv"*. Đo được: `tim_bash`
DỪNG ở ứng viên đầu tiên đạt, mà Git Bash trên PATH đạt trước, nên System32 **chưa từng được thử**
và chẩn đoán chỉ có một dòng. Tiêu chí đòi một thứ mà CLI không sinh ra được.

**(c) Năm ca nghiệm thu nằm trong một tệp KHÔNG CHẠY NỔI trên nền cần đo.** Đo được:
`ops/cong_cu_test.py::_chay_batch` gọi `subprocess.run([bash, "./cai_cong_cu.sh", "--bat-buoc"])`
với `bash` lấy bằng `shutil.which("bash")` ⇒ `C:\Windows\system32\bash.EXE` ⇒ **TREO**, hết hạn
60s, rồi `TemporaryDirectory` chết tiếp bằng `WinError 32` / `WinError 5`. Cả suite chết trong
`batch_behavior_test()` — TRƯỚC vòng lặp ca của `main()`. Nên `T23`–`T27` **chưa từng chạy trên
Windows**, dù chúng sinh ra để đo Windows. Đúng bệnh *"ca có MẶT khác ca có ĐO"*.

Và (c) phơi ra một **dạng hỏng THỨ BA của cùng bộ phóng WSL**, chưa từng được đo ở lượt 1 hay 2:
không chỉ `rc=127` và nuốt argv, mà **TREO**. Phép năng lực của `ops/bash_nen.py` có hạn 30s nên
nó vẫn bắt được — nhưng đó là MAY, không phải thiết kế: chưa có ca nào canh mặt ấy.

## 1. Vì sao có packet này — ĐÃ ĐO, không phải giả thuyết

Sáu ca `t35`–`t40` của `ops/lease_publish_test.py` ĐỎ trên Windows thật với `rc=127`. Issue #570
nêu giả thuyết *"script chưa từng chạy"* và yêu cầu **ĐO**, cấm xác nhận bằng suy luận.

Đã đo, 19-09-2026, `Windows-11-10.0.26200`, `python 3.13.1`, máy chủ kho. Bộ đo `DO-570.ps1`
(`sha256 f7d235ab2375c6d88bdd40a8eb4c94a9fde9884e4cb5208686ebb4f4c273f396`, bản `570-do-1`) và
`DO-570-LUOT2.ps1` (`sha256 233ea1b14f4aaac627fea0c2c1f684819abf0f4f212aa56b4d2642319abb11b8`,
bản `570-do-2`). Đính chính đã đăng: #570#issuecomment-5743594728.

**Phán quyết:** `a_GIAN_HONG_SCRIPT_LANH`, ra giống nhau trên CẢ HAI hình dạng đường dẫn.

- `shutil.which("bash")` trên máy ấy trả `C:\Windows\system32\bash.EXE` — **bộ phóng WSL**.
  Tự khai: `ARGV0=/bin/bash`, `UNAME=…microsoft-standard-WSL2`, `CYGPATH=KHONG_CO`.
- Đưa nó đường dẫn Windows ⇒ `rc=127` + `No such file or directory`, trùng từng chữ với log #570.
- Truyền đối số vị trí qua `-c` ⇒ **đối số không tới nơi**: `$0=/bin/bash`, `$#=0`; với một
  script 6 dòng, lỗi hiện ở **dòng 7** nội dung `t40` — đối số bị nối vào THÂN SCRIPT rồi chạy
  như một lệnh. Từ đó `$1`/`$2`/`$3` rỗng nên `exec "$3"` chết `exec: : not found`.
- `ops/cai_actionlint.sh` **LÀNH**: trên `C:\Program Files\Git\bin\bash.exe`, cùng máy, cùng các
  đường dẫn ấy, **26/26** khẳng định của sáu ca ĐẠT, và **6/6** đột biến bị giết ĐÚNG LÝ DO.
- **KHÔNG phải nguyên nhân: dạng đường dẫn.** Git Bash nhận đúng chuỗi `str(Path)` có dấu, có
  khoảng trắng, có dấu chéo ngược. Hai lượt đổi đúng một biến (`D:\Quốc hội\…` so với
  `C:\…\Temp\…` ASCII) cho kết quả y hệt. Cấm vá bằng cách `cygpath` hoá đường dẫn.

## 2. Hình dạng kế thừa — LẦN THỨ BA, nên không vá theo kiểu cũ

| lần | nơi | neo |
|---|---|---|
| 1 | `_bash_posix()` trong `ops/lease_publish_test.py` | `master e03c6d28`, run `32351777642` |
| 2 | `_bash_windows()` trong `ops/cong_cu.py` | run `33612364175`, 02-09-2026 |
| 3 | `t35`–`t40` gọi `shutil.which("bash")` trần | #570, 19-09-2026 |

`CLAUDE.md`: hình dạng lặp lần thứ ba thì câu hỏi đúng là *"có nên làm việc này không"*. Chủ kho
đã quyết: **MỘT bộ giải dùng chung + một CỔNG làm ĐỎ mọi lời gọi trần mới**. Bản vá thứ tư theo
kiểu cũ (thêm bộ giải riêng thứ ba) bị TỪ CHỐI có chủ đích.

Ràng buộc thiết kế kèm theo, có bằng chứng: hai bộ giải cũ lọc theo TÊN (`"system32"`,
`%SystemRoot%`) — đúng hình dạng *"danh sách CẤM không bao giờ đủ"*. Phép đo lượt 2 cho thấy
**không lọc theo tên nào diễn tả nổi "con bash này làm hỏng argv"**. Nên bộ giải phải quyết bằng
**phép thử NĂNG LỰC**.

## 3. Objective

Sáu ca `t35`–`t40` đo được ĐÚNG điều tên chúng nói, trên Windows thật; và khuyết tật
"phân giải `bash` theo TÊN rồi coi hit đầu tiên là dùng được" không thể tái sinh lặng lẽ trong
`ops/**`.

## 4. Write set

```yaml
write_set:
  - type: exact
    path: ops/bash_nen.py
  - type: exact
    path: ops/cong_cu.py          # THÊM ở r3 — xem §0(a)
  - type: exact
    path: ops/cong_cu_test.py
  - type: exact
    path: ops/lease_publish_test.py
```

**KHAI THẲNG — công việc TRƯỚC LEASE.** `ops/bash_nen.py` và `ops/cong_cu_test.py` ĐÃ được thay
đổi ở PR #571 (`010fb281f52b27364e4e3e3515d125b084f9d20e`) theo chỉ thị *"Vá đi"* của chủ kho,
lúc packet này CHƯA có lease. Lease r1 bao trùm chúng về sau; nó KHÔNG hợp thức hoá ngược việc
đã làm, chỉ ghi nhận đúng sự thật để không ai đọc nhầm rằng phần ấy đã qua cổng lease.

~~Hai đường KHÔNG vào write set~~ — **r3 rút xuống còn MỘT**:
- ~~`ops/cong_cu.py` — … lease `wp541-path-r3-g3-claude` khai nó trong `khong_duoc_cham`~~
  **HẾT HIỆU LỰC ở r3.** Lease ấy đã bị thu hồi; `ai-dang-giu ops/cong_cu.py` ⇒ `rc=0`,
  `NGƯỜI_GIỮ 0`. Nay nằm TRONG write set (§0(a), N14).
- `ops/cai_actionlint.sh` — đã đo là LÀNH; không có gì để sửa. **Vẫn ngoài write set.**

## 5. Tiêu chí nghiệm thu

Mỗi tiêu chí NEO LÝ DO, không chỉ neo `rc`. Ca nào không phân biệt được bằng đầu vào thì khai
thẳng là bộ TƯƠNG ĐƯƠNG, không giả vờ có nhiều chốt.

- **N1 — bộ giải quyết bằng NĂNG LỰC.** `ops/bash_nen.py::_do_nang_luc` chạy hai phép thật:
  (1) trung thực argv — `-c <script> <nhãn> A1 A2 A3` phải cho `$0 == nhãn`, `$# == 3`,
  `$1 == A1`; (2) mở được đường dẫn bản địa — chạy được script truyền bằng `str(Path)`.
  Thiếu một trong hai ⇒ TỪ CHỐI. Không ứng viên nào đạt ⇒ `None`, người gọi fail-close.
- **N2 — ba chốt con của phép argv có răng RIÊNG.** Ba `bash` giả, mỗi con hỏng đúng một chốt
  (`$0`, `$#`, `$1`); ba đột biến, mỗi đột biến gỡ đúng một chốt, cả ba phải làm ca đích ĐỎ.
  (Sinh ra vì đột biến đầu tiên SỐNG SÓT — nó chỉ gỡ một trong ba chốt.)
- **N3 — hai phép KHÔNG suy ra nhau.** Con giả "nuốt argv" vẫn mở được tệp; con giả "không mở
  được tệp" truyền đúng argv. Mỗi con chỉ bị đúng một phép bắt.
- **N4 — cổng chặn bản sao thứ tư.** `ops/**` có lời gọi `bash` trần ngoài danh sách cho phép
  ⇒ ĐỎ. Đột biến nới danh sách phải làm ca đích ĐỎ.
- **N5 — ratchet HAI CHIỀU.** Mục trong `CHUA_CHUYEN` mà đã SẠCH cũng làm cổng ĐỎ. Đột biến bỏ
  chiều ngược phải làm ca đích ĐỎ.
- **N6 — cổng đo CẤU TRÚC, không đo chuỗi.** Tệp chỉ NHẮC TỚI lời gọi trần trong chú thích,
  docstring hay một chuỗi hằng KHÔNG được làm cổng ĐỎ. Đột biến đổi sang khớp chuỗi thô phải làm
  ca đích ĐỎ. (Sinh ra vì bản đầu của cổng đếm luôn hai lần nhắc trong chính docstring của nó —
  đúng bệnh `t43` đã ĐỎ oan.)
- **N7 — sáu ca dùng bộ giải chung.** `t35`–`t40` lấy `bash` qua `ops/bash_nen.py`, không gọi
  `shutil.which("bash")` trần. Sau đó `ops/lease_publish_test.py` phải RỜI khỏi `CHUA_CHUYEN`,
  và N5 là thứ bắt việc quên xoá.
- **N8 — thiếu bash dùng được thì ĐỎ, không bỏ qua.** Sáu ca phải fail-close với thông điệp nêu
  chẩn đoán (ứng viên nào bị từ chối vì lý do gì), KHÔNG được `return` sớm rồi được đếm là ĐẠT —
  bệnh `t24` kho đã ghi sổ.
- **N9 — nghiệm thu trên WINDOWS THẬT.** ADR-0049: cổng hai nền là CỔNG TẠI CHỖ, không phải lane
  `master`. Nên N1–N8 phải có một lượt đo trên máy chủ kho, và log phải TỰ KHAI `sha256` bộ đo,
  `HEAD` đã đo, và REF nào trỏ tới `HEAD` ấy. Hai điều kiện, vì r1 đòi một thứ không sinh ra được:
  · `ops/bash_nen.py` phải có đường chẩn đoán thử **MỌI** ứng viên (không dừng ở cái đầu tiên đạt),
    và log phải cho thấy `C:\Windows\system32\bash.EXE` **đã được THỬ rồi bị TỪ CHỐI vì phép
    argv** — chọn đúng thôi chưa đủ, phải từ chối ĐÚNG LÝ DO;
  · lượt ấy phải CHẠY ĐƯỢC `T23`–`T27` trên Windows, tức N12 phải xong trước. Một lượt chết ở
    `batch_behavior_test()` là **KHÔNG ĐO ĐƯỢC**, KHÔNG phải "đạt".
- **N10 — delta nền = 0.** Mọi cổng chạy lại trên `origin/master` sạch để so DELTA. Đỏ sẵn thì
  khai "đỏ sẵn, delta = 0", không vá lung tung.
- **N11 — mặt TREO phải có răng.** Một `bash` giả KHÔNG BAO GIỜ trả phải bị `_do_nang_luc` TỪ
  CHỐI trong hạn, và đột biến bỏ/nới hạn phải làm ca đích ĐỎ. Hôm nay hạn 30s chặn được mặt ấy
  nhưng KHÔNG ca nào canh — tức nó đang đúng do may. (Sinh từ phép đo `570-do-3`: WSL bash làm
  `./cai_cong_cu.sh` treo tới 60s thay vì `rc=127`.)
- **N12 — `ops/cong_cu_test.py` phải chạy được trên Windows.** Ba lời gọi `bash` trần của nó phải
  đi qua `tim_bash()`, và suite phải tới được vòng lặp ca trên Windows. Không có N12 thì N9 vô
  nghĩa: năm ca nghiệm thu nằm trong chính tệp không khởi động nổi.
- **N14 — `ops/cong_cu.py` dùng bộ giải chung, và `CHUA_CHUYEN` về RỖNG.** `_bash_windows()`
  uỷ quyền cho `ops/bash_nen.py::tim_bash()`; không còn bộ lọc theo TÊN nào RA QUYẾT ĐỊNH trong
  `ops/**`. Sau đó `ops/cong_cu.py` phải RỜI `CHUA_CHUYEN`, và vì nó là mục cuối cùng, danh sách
  ấy phải RỖNG. N5 (ratchet hai chiều) là thứ bắt việc quên xoá — tức N14 đo được bằng chính
  cổng, không bằng mắt.
- **N15 — `t22` phải ĐO THỨ MỚI, không được giữ lại làm cảnh.** Ca `t22` hôm nay khẳng định
  `_bash_windows` LOẠI ứng viên dưới `%SystemRoot%` theo ĐƯỜNG DẪN. Sau N14 mệnh đề ấy không còn
  đúng theo nghĩa cũ: thứ loại bộ phóng WSL là PHÉP NĂNG LỰC. Nên `t22` phải được viết lại để đo
  hành vi MỚI, và phải có đột biến riêng làm nó ĐỎ. **Giữ nguyên `t22` cũ là cấm** — một ca còn
  MẶT mà không còn ĐO là đúng bệnh `t24` kho đã ghi sổ.
- **N16 — báo cáo bán kính nêu LÝ DO ở MỌI nhánh ĐỎ.** Không nhánh nào được chỉ in TÊN ca oan.
  Mỗi nhánh (`oan`, `gia`) phải có đột biến RIÊNG làm ca đích ĐỎ, phân biệt được bằng ĐẦU VÀO —
  nếu không phân biệt được thì khai thẳng là bộ TƯƠNG ĐƯƠNG. (Sinh ra vì bản vá sáng 20-09 chỉ
  gắn lý do vào nhánh `oan`, rồi lượt đo `570-do-5` rơi vào nhánh `gia` và lại không đọc được gì
  — *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"*.)
- **N17 — cổng quét TOÀN CÂY, không chỉ `ops/**`.** `quet()` đi hết cây kho (trừ `.git/` và
  `ops/reviews/` — ảnh chụp đông cứng). Bốn tệp đo được ở §0 nạp vào `CHUA_CHUYEN`, MỖI MỤC
  kèm **ngày gỡ** và lý do. Đột biến thu phạm vi về `ops/**` phải làm ca đích ĐỎ — nếu không
  thì không ai biết cổng đang phủ tới đâu.
- **N18 — độ phủ của `_loi_goi_tran` phải ĐO ĐƯỢC THEO HÌNH DẠNG.** Một bảng hình dạng lời gọi
  (ít nhất: `which` chuỗi · `which` keyword · `which("bash.exe")` · `run`/`Popen` list ·
  `run(args=)`), mỗi hình dạng một khẳng định. Và **docstring phải khai ĐÚNG phạm vi** — cấm
  chữ "MỌI" khi phép đo chỉ phủ một tập. (Sinh từ F1: hàm khai "mọi lời gọi phân giải `bash`
  theo TÊN", đo được 3/12. Đáng kể nhất là `which("bash.exe")` — đúng cách viết Windows của
  đúng khuyết tật Windows mà packet này sinh ra để chặn.)
- **N19 — cache của `tim_bash` phải theo dõi MÔI TRƯỜNG, hoặc khai thẳng là không.** `ung_vien`
  đọc `CONG_CU_BASH`/`PATH`/`SystemRoot`/`ProgramFiles` từ `os.environ` khi tham số là `None`,
  nên khoá cache phải gồm chúng. Phản chứng hai chiều: đặt `CONG_CU_BASH` SAU lần gọi đầu thì
  lần gọi sau phải thấy. (Sinh từ F3. Hôm nay chưa cắn ca nào vì bộ test tiêm qua `env=` của
  tiến trình con, nhưng đó là bẫy nằm chờ.)
- **N23 — DANH SÁCH TỆP LÀ INDEX, KHÔNG HƠN. SINH TỪ r9.**
  `_liet_ke_py` chạy đúng `git ls-files --cached -z -- '*.py'`: **không cờ exclude nào**,
  không `--others`, không kho tạm. `nguon_tep` giữ ba trạng thái, nghĩa đọc lại:
  `git` = danh sách từ INDEX · `rglob` = cây KHÔNG phải kho git (bộ ca dựng cây giả) ·
  `git-hong: …` = có `.git` mà lệnh git hỏng. **SỬA Ở r10 (N26):** trạng thái thứ ba trước đây
  trả một danh sách `rglob` kèm nhãn `rglob-git-hong`; nay nó **không trả danh sách nào** và
  `quet()` biến nó thành `KHONG_DO_DUOC`. Xem N26.
  Chốt: **không luật ignore nào đổi được danh sách** — `.gitignore` chưa/đã theo dõi,
  `.git/info/exclude`, `core.excludesFile` cục bộ, `GIT_CONFIG_GLOBAL`,
  `$XDG_CONFIG_HOME/git/ignore` — sáu mặt, danh sách y hệt nền. Và một tệp `add -f` khớp
  `.gitignore` đã commit **vẫn phải có mặt**. Đột biến nghe lại luật ignore phải làm ca đích ĐỎ.
  ĐÁNH ĐỔI: tệp chưa `add` KHÔNG được quét — `t37` chốt cả hai chiều và docstring gọi thẳng
  đó là quyết định của chủ kho, không phải tính chất tự nhiên.
- **N32 — REF THAY THẾ CỦA MÁY KHÔNG ĐƯỢC ĐỔI BYTES CỔNG ĐỌC. SINH TỪ r12.**
  Mọi tiến trình `git` con đi qua **một** hàm `_chay_git`, mang `--no-replace-objects` **và**
  `GIT_NO_REPLACE_OBJECTS=1`. Hai hàng rào phải ở CÙNG một chỗ: tách ra hai nơi thì không đột
  biến nào đo được cái nào.
- **N33 — INDEX CHƯA HOÀ GIẢI ⇒ KHÔNG ĐO ĐƯỢC, NÊU TÊN. SINH TỪ r12.**
  Bản ghi mang **cả ba** trường `(đường, chế_độ, sha)` cộng **stage**; chỉ stage `0` được nhận.
  Còn stage 1/2/3 ⇒ `KHONG_DO_DUOC` nêu tên đường. Chọn bừa một stage là tự bịa ra một cây
  chưa từng tồn tại.
- **N34 — GIẢI MÃ NGUỒN THEO KHAI BÁO CỦA CHÍNH TỆP. SINH TỪ r12.**
  `tokenize.detect_encoding` trên blob thô (PEP 263 + BOM), cho **cả** đường git lẫn đường
  `rglob`. Fail-close đúng chỗ là khi KHÔNG ĐO ĐƯỢC; một tệp Python hợp lệ mà làm cổng chặn cả
  kho là đọc sai cách, không phải không đo được. **Chiều ngược** phải có ca: tệp BOM **mang**
  lời gọi trần vẫn phải bị bắt.
- **N35 — HẬU TỐ NGUỒN PYTHON SO KHÔNG PHÂN BIỆT HOA/THƯỜNG, GỒM `.pyw`. SINH TỪ r12.**
  Một hàm `_la_nguon_py` dùng `casefold()`; **không** dùng pathspec `*.py` của git. **Chiều
  ngược** phải có ca: `.txt` mang lời gọi trần vẫn KHÔNG được quét.
- **N28 — DANH SÁCH *VÀ* NỘI DUNG ĐỀU TỪ INDEX; MÔI TRƯỜNG GIT PHẢI SẠCH. SINH TỪ r11.**
  Nội dung lấy bằng `git cat-file --batch` trên blob đã stage, không `read_text()` trên cây làm
  việc. Mục mode `120000` (symlink) ⇒ **`KHONG_DO_DUOC` nêu tên**, không im lặng bỏ qua. Mọi
  tiến trình git con chạy với môi trường đã gỡ `GIT_DIR`, `GIT_INDEX_FILE`, `GIT_WORK_TREE`,
  `GIT_COMMON_DIR`, `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES`,
  `GIT_CEILING_DIRECTORIES`, `GIT_DISCOVERY_ACROSS_FILESYSTEM`, `GIT_NAMESPACE`,
  `GIT_INDEX_VERSION`, `GIT_CONFIG*`, `GIT_CONFIG_KEY_n`, `GIT_CONFIG_VALUE_n`. Báo cáo mang
  `nguon_noi_dung` và `bien_git_da_go` — đọc được, không phải tin lời.
  **Ba chiều** phải có ca: sửa trên đĩa sau `git add` KHÔNG đổi phán quyết · `GIT_INDEX_FILE`
  KHÔNG đổi danh sách · symlink ⇒ `KHONG_DO_DUOC` nêu tên.
- **N29 — GIẢI TÊN PHẢI TÔN TRỌNG `global`/`nonlocal` VÀ WALRUS TRONG COMPREHENSION. SINH TỪ r11.**
  Ràng buộc khai `global`/`nonlocal` thuộc phạm vi **SỞ HỮU**, không phải phạm vi cú pháp chứa
  nó; khai **đọc không** (không gán gì trong thân) KHÔNG chuyển gì. `:=` trong comprehension
  ràng buộc ở phạm vi **CHỨA** comprehension (PEP 572). Hai chiều: LỌT và OAN đều phải có ca.
- **N30 — HẰNG CHƯƠNG TRÌNH SO THEO MỌI KIỂU BIỂU DIỄN. SINH TỪ r11.**
  `str` và `bytes` ASCII, không phân biệt hoa/thường. Byte ngoài ASCII KHÔNG giải mã bừa.
  Cùng lớp với mặt hoa/thường ở r7: *một bảng hằng chỉ phủ một cách viết là một đường vòng*.
- **N31 — CỔNG PHẢI ĐƯỢC NỐI VÀO ĐIỂM VÀO MÀ CI GỌI. SINH TỪ r11 (P1).**
  `ops/cong_cu_test.py` — chính lệnh CI chạy — phải chạy `quet` trên cây **THẬT** đúng MỘT lần,
  **TRƯỚC** bộ đột biến (đột biến dựng cây SAO và tráo `BASH_NEN`), và kéo mã thoát khác 0 khi
  cổng `DO` **hoặc** `KHONG_DO_DUOC` — hai nhãn riêng, không gộp. **Hai chiều** phải có ca: cây
  sạch ⇒ qua; cây có lời gọi trần đã `git add` ⇒ hỏng **và nêu tên tệp**.
- **N26 — KHÔNG LẤY ĐƯỢC INDEX ⇒ KHÔNG ĐO ĐƯỢC, KHÔNG LÙI. SINH TỪ r10.**
  Cây có `.git` mà `git ls-files` hết giờ / trả rc khác 0 / không sinh được tiến trình ⇒
  `_liet_ke_py` trả `([], "git-hong: <lý do đo được>")` và `quet()` trả **`RC_KHONG_DO_DUOC`**
  kèm `nguon_tep` khai VÌ SAO. **Cấm lùi về `rglob`**: danh sách rộng hơn thì phán quyết lại
  phụ thuộc trạng thái LOCAL của máy — đúng lớp r9 giết bằng kiến trúc, sống qua cửa sau.
  Đo được trước vá trên `e290f99`: cây `.git` giả ⇒ `rc=2 DO`, `ngoai_danh_sach=['rac…py']`.
  **HAI CHIỀU:** cây KHÔNG có `.git` vẫn `rglob` và vẫn phán quyết được — thiếu chiều này thì
  đột biến *"lúc nào cũng KHÔNG_ĐO_ĐƯỢC"* sống. Ca đích chốt trên `rc == 3`, nên nó KHÔNG thuộc
  `CA_PHAN_QUYET` (N22 chỉ phủ `rc == 2` / `trang_thai == "DO"`).
- **N27 — RÀNG BUỘC IMPORT PHÂN LOẠI THEO CÁC TRƯỜNG CỦA NÚT, KHÔNG THEO MỖI CÁI TÊN. SINH TỪ r10.**
  `ImportFrom` chỉ là stdlib khi **`level == 0`**; `from .subprocess import run` là module CÙNG
  GÓI. `Import` tên CÓ CHẤM và KHÔNG `as` (`import subprocess.x`) **ràng buộc** tên `subprocess`
  vào chính module stdlib ấy — luật Python, không phải suy diễn. `import subprocess.x as y`
  KHÔNG ràng buộc `subprocess`. Bảng hình dạng của N18 phải mang **cả ba chiều**: một hình dạng
  PHỦ mới, hai hình dạng KHÔNG PHỦ mới, và `from . import subprocess` giữ lại làm chiều thứ ba
  để một bản vá cho `level` không âm thầm làm hỏng nó.
  **KHÔNG PHỦ, nợ có tên (không đổi):** `from subprocess import *` — `*` đòi biết module xuất ra
  những gì, tức phải NẠP nó, chứ không phải đọc cây cú pháp. Cùng hàng `shell=True`.
- **N24 — MỘT ca ĐỎ Ở NỀN không được đầu độc phép đo bán kính của TOÀN BỘ bộ đột biến. SINH TỪ r9.**
  Nghiệm thu Windows `570-do-14` đo được: `t38` đỏ ở nền ⇒ **45/46 đột biến** in
  `giết THÊM ['t38_…']`, `lỗi đột biến=45`. Cả 45 dòng là hệ quả của **MỘT** ca; người đọc phải
  lội hết mới thấy điều duy nhất có thật. Đây là **lần thứ HAI** (lần đầu `570-do-10` với `t34`,
  spec r6 §0) — lặp lần thứ hai thì chữa bằng cơ chế.
  Phải: chạy bộ ca trên NỀN trước; ca đỏ ở nền bị **loại khỏi cả tử số lẫn mẫu số** của bán
  kính; báo **một lần** kèm tên; đích đỏ ở nền ⇒ **KHÔNG ĐO ĐƯỢC**, không phải "giết đúng";
  và **vẫn kéo mã thoát khác 0** — KHÔNG ĐO ĐƯỢC không được lặng lẽ thành xanh.
- **N25 — ca đo phải chốt TIỀN ĐỀ trước khi chốt kết luận. SINH TỪ r9.**
  `t38` bản cũ kết luận *"khoá cache không gồm `cwd`"* trong khi log Windows cho thấy `cwd=a`
  đã trả **Git Bash**, tức bản ghi đè chưa bao giờ được chọn — **một nguyên nhân chưa đo**.
  Phải: chốt tiền đề (`normcase(abspath(t1))` == bản ghi đè, tính NGAY trong tiến trình con khi
  cwd còn ở `a/`, vì tên ứng viên là TƯƠNG ĐỐI); không đạt ⇒ KHÔNG ĐO ĐƯỢC kèm `chan_doan`
  **đo được**, không phải suy đoán. Đạt rồi mới chốt kết luận.
  GIỚI HẠN CÓ TÊN: phép so chứng minh bộ giải đã CHỌN tên trỏ vào `a/`, **không** chứng minh
  tệp ấy đã chạy — đo được: bản sao `chmod 644` cộng `/usr/bin` trên PATH thì `execvp` giải tên
  tương đối sang `/usr/bin/bash`. Với `PATH='.'` hai câu trùng nhau; đó là lý do PATH phải là `.`.
- **N22 — KHÔNG ca nào ngoài CA PHÁN QUYẾT được chốt trên `rc`/`trang_thai`. SINH TỪ r7.**
  Một ca tự kiểm quét **`ast`** toàn bộ `ops/cong_cu_test.py`: trong thân mỗi hàm ca, nếu có
  một `bang(...)`/`dung(...)` mà biểu thức điều kiện so `rc` với `2`, hoặc so
  `trang_thai` / `bao["trang_thai"]` với `"DO"`, thì hàm ấy **phải** nằm trong danh sách
  `CA_PHAN_QUYET` khai tường minh. Ngoài danh sách ⇒ ĐỎ, nêu **tên hàm và số dòng**.
  **Hai chiều**, như mọi ratchet của packet này: một tên trong `CA_PHAN_QUYET` mà **không còn**
  chốt phán quyết nào cũng ĐỎ — kẻo danh sách thành nghĩa trang (đúng bệnh N5 sinh ra để chặn).
  Hai đột biến riêng: (a) bỏ phép quét; (b) bỏ chiều ngược. Cả hai phải làm ca đích ĐỎ.

  **VÌ SAO LÀ LUẬT CHỨ KHÔNG PHẢI LỜI KHUYÊN:** sáu lần trước đều là người viết ĐÃ BIẾT nguyên
  tắc ấy rồi vẫn vi phạm — ba lần trong số đó do chính phiên vừa ghi nguyên tắc vào docstring.
  Một nguyên tắc chỉ sống trong docstring thì không phải hàng rào, nó là một lời nhắc mà người
  đang vội sẽ đi qua.

  **NỢ CÓ TÊN:** luật này bắt theo HÌNH DẠNG CÚ PHÁP, nên nó KHÔNG bắt được một ca trói lại
  phán quyết bằng đường vòng — gọi qua hàm phụ, so chuỗi `ly_do`, hay đọc `ngoai_danh_sach`
  rồi suy ra. Nó **thu hẹp cửa, không đóng cửa**. Khai ra thay vì để người sau tưởng đã kín.
- **N20 — ca cache phải đo VIỆC TÍNH LẠI, và phải GIỮ bằng chứng. SINH TỪ r6.**
  `t34` bản r4 khẳng định `sau == khac` — một **kết quả**, trong khi thuộc tính N19 nói về
  **khoá cache**. Hai thứ ấy trùng nhau trên Linux và TÁCH RA trên Windows, nơi ứng viên ghi đè
  có thể bị **năng lực** từ chối. Ca ấy vì thế đỏ mà không nói được vì sao (xem §0).
  Ba chốt, theo đúng thứ tự:
  1. **Chốt CHÍNH, độc lập nền:** `chan_doan` của lần gọi THỨ HAI phải **chứa** đường ghi đè
     như một ứng viên ĐÃ ĐƯỢC XÉT. Đây đúng là thứ N19 sửa: khoá cũ trả bản nhớ mà không hỏi
     ứng viên nào, nên đường ghi đè sẽ KHÔNG có mặt. Đột biến `t34_khoa_cache_bo_moi_truong`
     phải làm ca đích ĐỎ **qua chốt này**.
  2. Nếu ứng viên ghi đè được CHẤP NHẬN (`dat == true`) ⇒ chốt thêm `sau == khac`.
  3. Nếu nó bị TỪ CHỐI ⇒ **KHÔNG ĐO ĐƯỢC**, kèm `ly_do` **đo được** lấy từ `chan_doan`, không
     phải kèm một suy đoán. `None ≠ False`.
  Và bộ dựng ứng viên phải cố tạo một bản ghi đè **CHẠY ĐƯỢC** trước đã: giữ nguyên **tên tệp**
  (kể cả đuôi `.exe`) và chép kèm các `*.dll` cùng thư mục. Bỏ qua bước ấy là tự chế một ứng
  viên hỏng rồi đổ cho bộ giải.
- **N21 — bộ đo Windows phải CHỐT CÂY trước khi đo. SINH TỪ r6.**
  Lượt `570-do-9` chạy đúng nhưng trên **cây sai**: clone lúc 16:27:55Z, bản vá `c0bc5a5` đẩy
  lúc ~16:33Z, nên nó đo `af0d261` — bản TRƯỚC vá — và vẫn in ra một bảng số trông hợp lệ. Bộ đo
  **tự khai** đủ thông tin để phát hiện (`HEAD` + ba băm) nhưng **không chốt**.
  Bộ đo phải GHIM commit + ba băm và **DỪNG** `rc≠0` khi lệch, in cả hai bên; lệch mà vẫn chạy
  thì kết quả phải mang dấu `KHONG_DO_DUOC_CAY_KHAC` và mã thoát khác 0. Lời dặn bằng miệng
  ("đừng chạy vội") KHÔNG phải hàng rào.
- **N13 — ratchet phải NGẮN đi thật. VIẾT LẠI Ở r4.** Bản r3 nói "danh sách phải ngắn đi", và
  r4 làm nó DÀI RA (0 → 4 mục) vì mở phạm vi. Nói cho đúng: thứ phải ngắn đi là **số lời gọi
  trần CHƯA ĐƯỢC NHÌN THẤY**, không phải độ dài danh sách. Mở phạm vi làm danh sách dài ra
  nhưng làm số-chưa-nhìn-thấy về **0** — đó mới là chiều đúng.
  Chốt thay thế: (a) mọi mục `CHUA_CHUYEN` phải có **ngày gỡ**; (b) `ops/lease_publish_test.py`
  và `ops/cong_cu_test.py` và `ops/cong_cu.py` KHÔNG được quay lại danh sách; (c) N5 (chiều
  ngược) vẫn bắt việc quên xoá khi một mục đã sạch.

## 6. Ngoài phạm vi

**r4 RÚT một mục ra khỏi đây:** phạm vi cổng. Cổng nay phủ toàn cây (N17). Việc SỬA 11 lời gọi
ngoài `ops/**` thì **vẫn ngoài phạm vi** — r4 chỉ làm chúng NHÌN THẤY ĐƯỢC và có ngày gỡ; sửa
chúng đụng `.claude/**` và `scripts/**`, không nằm trong write set.

- `t131` `t132` (chưa có chỗ) · `t150` (#552) · `t125` (#562) · `t171` và mọi thứ thuộc write set
  của #541 ngoài `ops/lease_publish_test.py`.
- `ops/cai_actionlint.sh` — đã đo LÀNH.
- ~~Hợp nhất `_bash_windows` của `ops/cong_cu.py`~~ — **HẾT HIỆU LỰC ở r3**, nay là N14. Điều
  kiện câu cũ nêu (*"sau khi … rời khỏi tay lease khác"*) ĐÃ THOẢ: đo 20-09T05:05Z,
  `ai-dang-giu ops/cong_cu.py` ⇒ `rc=0`, `NGƯỜI_GIỮ 0`. `_bash_posix` thì đã hợp nhất ở r2.
- Giải thích cơ chế marshalling argv của `bash.exe` WSL. Hai chỗ dữ liệu chưa khép (hai `$0` khác
  nhau trong một lượt; `command -v cygpath` trả KHÔNG CÓ mà ba lời gọi `cygpath` vẫn chạy) đứng ở
  **KHÔNG ĐO ĐƯỢC**. Cấm dựng giả thuyết cho chúng: bản vá không phụ thuộc vào chúng, và ghi một
  nguyên nhân sai vào doctrine còn tệ hơn không ghi gì.

## 7. Điều kiện dừng

### 7.0 ĐIỀU KIỆN THOÁT CỦA VÒNG LẶP REVIEW — ghi lần đầu ở r10

Chủ kho, phiên 2026-09-21 ~18:2xZ và nhắc lại 2026-09-23. **Trước r10 điều kiện này chưa từng
được ghi ở đâu** — không ở spec r9 §7, không ở `dieu_kien_dung` của lease g9 — nên đây là ghi
lần đầu, không phải sửa một tiêu chí đã đóng băng.

- **THOÁT khi: không còn finding P1, P2, P3.** KHÔNG phải "khi approve".
  - CHẶT hơn ở chỗ nó **nêu rõ ngưỡng**: một phép ĐẾM trên nhãn mức độ, hết chỗ diễn giải.
  - LỎNG hơn ở chỗ nó **cho phép** finding dưới P3 (P4 / nit / informational) còn lại.
  - **HỆ QUẢ THAO TÁC:** mỗi verdict phải **ĐẾM THEO MỨC ĐỘ**, không chỉ đếm tổng. Ô chưa
    review ghi `chưa review`, **không** ghi `0` — `None ≠ False`.
- **MỘT VÒNG =** vá → review chéo → **đọc finding và ĐO LẠI từng cái** (không nhận lời khai) →
  **trừu tượng hoá thành LỚP rồi quét cả cây tìm thực thể khác** → vá theo lớp → chạy trọn bộ ca
  + bán kính đột biến → **đăng verdict kèm bảng đếm theo mức độ** → lặp.
- **Review chéo dùng phiên bản / effort CAO HƠN executor.** r10: reviewer `codex gpt-6-astra`
  effort `low`; executor `fable` (`claude-fable-5-1`) effort `low` (r12; r10–r11 là `medium`).
- **HINT PATCH** cho vấn đề phức tạp: verdict phải nêu **CƠ CHẾ** và chỗ sửa, không chỉ triệu
  chứng — để vòng sau không phải tự tìm lại.
- **KHÔNG chạy CI, không `workflow_dispatch`, không full CI** cho tới khi đủ điều kiện merge.
  **KHÔNG cần CI Windows** — chủ kho: lỗi Windows đã biết từ trước. Đo cục bộ, cộng bộ đo
  Windows chạy TAY trên máy chủ kho.
- Chưa tới ngưỡng thoát mà lease hết hạn ⇒ **DỪNG, xin thế hệ mới. KHÔNG tự gia hạn.**
  Đã xảy ra hai lần: g6 lỡ hạn 09:45Z; g9 lỡ hạn 2026-09-22T06:25Z và mất 26 giờ.

### 7.1 Điều kiện dừng của EXECUTOR

- Một hình dạng lỗi lặp lần thứ BA ⇒ DỪNG, hỏi *"có nên làm việc này không"*.
- Cần chạm bất kỳ đường nào ngoài write set ⇒ DỪNG, xin revision.
- `ai-dang-giu` cho `ops/lease_publish_test.py` còn cho thấy một NGƯỜI GIỮ NÀO KHÁC ngoài lease
  của chính packet này ⇒ KHÔNG chạm tệp ấy. Đo TRƯỚC mỗi lần chạm, đọc `rc` TRỰC TIẾP, và đọc cả
  `da_bi_thay_the`. "Hết hạn" KHÔNG phải "đã nhả"; "đã land" cũng KHÔNG phải "đã nhả".
  **Đây là câu r1 viết SAI** — r1 đòi `rc=0` / `NGƯỜI_GIỮ 0`, mà lease của chính packet luôn giữ
  đường ấy nên điều kiện không bao giờ thoả được. Một điều kiện không thoả được sẽ bị diễn giải
  lại trong im lặng; nêu ra đây thay vì để nó chết âm thầm.
- Ba chốt của N2 không phân biệt được bằng đầu vào ⇒ khai thẳng là bộ TƯƠNG ĐƯƠNG, báo lại, không
  tự quyết.
- **Sau N14, nếu `ops/cong_cu.py` cần một phép lọc theo TÊN để chạy được ⇒ DỪNG và báo.** Đó là
  dấu hiệu bộ giải năng lực chưa đủ cho đường ấy, và vá bằng cách nhét lại một danh sách cấm là
  tái sinh đúng khuyết tật packet này sinh ra để giết.
- **Nếu hợp nhất xong mà bán kính đột biến trên Windows VẪN không đọc được ⇒ DỪNG.** Đó là lần
  thứ BA của cùng một hình dạng, và câu hỏi đúng lúc ấy là *"có nên đo bằng bán kính không"*,
  không phải *"nới ngưỡng thế nào"*.
