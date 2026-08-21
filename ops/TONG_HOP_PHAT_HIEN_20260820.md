# Tổng hợp phát hiện — phiên 20-08-2026 (PLAT-M4 · PLAT-X4 · PLAT-X5)

**Cách đọc.** Mỗi mục ghi **bằng chứng đo được**, không ghi cảm tưởng. Mục nào chưa đo lại độc
lập thì khai thẳng. Nhóm B là phần đáng giá nhất: nó nói về **quy trình của phiên điều phối**,
không về mã — và loại ấy tái phát nhanh hơn lỗi mã.

Trạng thái lúc viết: `#203`/PR `#205` chờ quyết định land · `#206`/PR `#207` CI xanh, đang
review chéo · `#194` còn một P2 chưa vá.

---

## A. Lỗi trong MÃ của kho

### A1. ĐÃ VÁ

| # | vấn đề | bằng chứng | vá ở |
|---|---|---|---|
| A1.1 | `t34` khớp CHUỖI caller — `run: echo preparing; python …` vẫn tính là đã cấp công cụ | `35/35` rc=0 khi gỡ hẳn installer | `#203` rev2 → danh sách CHO PHÉP |
| A1.2 | `t34` ràng theo TỆP, không theo JOB — installer ở job khác vẫn qua | `38/38` rc=0 | `#203` rev3 → ràng theo `(workflow, job)` + thứ tự |
| A1.3 | `AL_VER` dùng glob `case` — `1x.2y.3z` lọt | rc=0 | `#203` rev2 → regex bash |
| A1.4 | Gói tải từ mạng KHÔNG kiểm checksum; `--version` là binary TỰ KHAI | `rg 'sha256\|checksum'` → rc=1 | `#203` rev2 → ghim sha256, 4 mã thoát |
| A1.5 | **Windows:** `tar` đọc `C:` là TÊN MÁY (`HOST:PATH`) ⇒ installer LUÔN rc=5 | `tar (child): Cannot connect to C: resolve failed`, run `32368383473` | `#203` rev2 → chép về tên không dấu hai chấm |
| A1.6 | `sha256sum` THOÁT cả dòng khi tên tệp chứa `\` ⇒ băm dài thêm 1 ký tự, cổng báo sai trên gói ĐÚNG | `\7f12f18…` vs `7f12f18…`, run `32371632630` | `#203` rev2 → đọc từ stdin |
| A1.7 | `${TEN_GOI##*.}` trả CẢ đường dẫn khi tên không có dấu chấm | `nodot` rc=5; `co.tar.gz` rc=0 | `#203` rev3 |
| A1.8 | `t38` có nhánh **bỏ qua âm thầm** trên Windows (`bang(True,"")` vẫn đếm ĐẠT) | harness không có cơ chế skip | `#203` rev3 |
| A1.9 | Suy loại archive từ suffix — zip không đuôi / `.ZIP` hoa ⇒ rc=5 trên gói hợp lệ | rc=5 / rc=5 | `#206` → magic bytes, fail-close khi thiếu `od` |
| A1.10 | `t40` hỏng trên Windows: stub Python **native** mở thêm Git Bash rồi tái dùng PATH `;` | rc=32, run `32391121674` | `#206` lượt 2 |
| A1.11 | `invalid escape sequence '\`'` trong docstring `t38` — **lỗi của phiên điều phối** | `py_compile -W error` | `#206` lượt 2 (codex sửa hộ) |

### A2. CHƯA VÁ

| # | vấn đề | mức | ở đâu |
|---|---|---|---|
| A2.1 | `doctor` probe nhận URL có **credential nhúng** (`http://user:SECRET@host`) — kiểm scheme bằng TIỀN TỐ, không theo cấu trúc; credential vào `req.full_url` và `req.host` | P2 | `#194`, chưa đụng |
| A2.2 | `t34` vẫn fail-open với `python -m …` và `bash -c "…"`; installer `if: false` vẫn được tính | — | **CỐ Ý** — nợ có tên `PLAT-X5-required-status-check` |
| A2.3 | `curl --retry 2` có thể không bao lỗi 35 (thiếu `--retry-all-errors`) | P3 | có sẵn từ trước, ngoài phạm vi mọi packet đang mở |
| A2.4 | Chốt root-commit của launcher **không phân biệt "sai kho" với "clone nông"** | P2 | `.claude/dev/launcher.py` — xem C5 |

**A2.2 không phải bỏ sót.** Ba vòng review chứng minh mọi lần siết thêm mẫu khớp đều sinh một
dạng shell mới làm nó thua. Câu hỏi *"CI có thật sự chạy gate không"* **không thuộc thẩm quyền
một bộ test tự kiểm văn bản YAML của chính nó** — nhà của nó là required status checks.

---

## B. Lỗi trong QUY TRÌNH của phiên điều phối — phần đáng ghi nhất

### B1. PHÉP ĐO NÓI DỐI — bốn lần, bốn cơ chế khác nhau

Không lần nào là lỗi của mã đang đo. Cả bốn đều làm tôi suýt kết luận ngược:

1. `bash script.sh | tail -5` rồi đọc `$?` ⇒ lấy rc của `tail`. (Đã ghi trong `CLAUDE.md` từ trước; vẫn tái phát.)
2. `printf 'AL_VER=%-12s rc=%s' "$(printf …)" "$?"` ⇒ **command substitution chạy TRƯỚC và đặt lại `$?`**, nên **mọi** giá trị `AL_VER` xấu đều báo `rc=0`. Suýt kết luận "regex không cưỡng chế".
3. Dấu nháy ngược trong chuỗi `echo` ⇒ shell **thực thi** `nodot` như một lệnh ⇒ `rc=127`, trông như script hỏng.
4. Quên truyền `AL_VER`; truyền `SP="$SP"` như **đối số** thay vì biến môi trường ⇒ `rc=2`/`rc=4` giả.

> **NẾP:** gán `RC=$?` vào biến **NGAY dòng sau lệnh**, rồi mới in. Không đặt bất kỳ lời gọi nào
> — kể cả `printf`/`$( )` — giữa lệnh và chỗ đọc `$?`.

### B2. BỊA BĂM thay vì đo — hai lần, và CỔNG KHÔNG BẮT ĐƯỢC

Gõ tay 40 ký tự từ bản rút gọn: một lần trong prompt `#203`, một lần ở
`reviewed_sha_required` của lease review `#206` (sai từ ký tự thứ 9).

`ops/lease_publish.py check` **NHẬN cả hai** — nó kiểm **DẠNG** (40 hex thường) chứ không kiểm
**GIÁ TRỊ**. Băm sai dạng thì đỏ; băm sai giá trị thì xanh.

> **NẾP:** luôn `H=$(git rev-parse …)` rồi chèn biến. Không bao giờ gõ băm tay.

### B3. ĐẶC TẢ TỰ MÂU THUẪN — đếm PHẢN CHỨNG mà người đọc đếm FINDING

`#206` §5 viết *"Ba phản chứng của vòng 3"* rồi liệt kê ba mục — nhưng cả ba đến từ **finding 1
và 2**. Vòng 3 có **ba FINDING**, cái thứ ba là ZIP. Comment chốt trên `#203` lại hứa *"ba
finding vòng 3 chuyển sang #206"*, trong khi write set **không có** `ops/cai_actionlint.sh`.

Đặc tả **hứa một đằng, cấp phương tiện một nẻo**. Executor `codex` dừng theo điều kiện phạm vi
thay vì lách — 174k token, 0 dòng mã, nhưng bắt lỗi **trước khi có mã**.

> **NẾP:** khi liệt kê "N thứ phải xử", nói rõ N đếm **finding** hay **phản chứng**, và đối
> chiếu write set có đủ phương tiện cho từng cái không.

### B4. PHÉP THỬ KHÔNG THỂ SAI

Để phân giải chuyện mất chữ trên đường truyền, tôi nhúng một phép đo: *"dạng thô mất mà dạng đã
thoát còn ⇒ bộ đọc lọc thẻ"*. **Tiêu chí ấy sai** — đường GHI làm mất thẻ cũng cho **đúng kết
quả đó**, vì dạng đã thoát không chứa ký tự `<` nào. Hai giả thuyết dự đoán y hệt nhau.

Đã rút lại công khai. *Một phép kiểm không thể đỏ thì không phải bằng chứng* — câu này đã có
trong `CLAUDE.md`, và tôi vẫn viết ra một phép thử như thế.

### B5. RÚT LẠI một quan sát đã công bố

Tôi từng viết: khối ```` ```text ```` có thể an toàn hơn dòng thường trước hiện tượng mất chữ.
**Sai** — cả **ba** lần mất trong đợt đều nằm TRONG fence.

### B6. ĐỌC SAI THỨ TỰ BƯỚC

Nói bản vá `tar` "đã đi qua được chỗ cũ". Sai: bước 10 đứng **trước** bước 11, lượt ấy chết sớm
hơn và bước 11 `skipped` — **chưa từng chạy**. Cùng họ *"vắng mặt vì sạch" ≠ "vắng mặt vì chưa chạy"*.

### B7. ĐỌC SAI THÔNG BÁO TÁC VỤ NỀN — hai lần

Báo codex "đã xong, không có verdict" trong khi đó là **vỏ shell `nohup … &` thoát**, còn codex
vẫn chạy. Log không bị cắt; nó đang viết tiếp.

> **NẾP:** với tiến trình nền, đợi bằng điều kiện **trên chính tiến trình** (`pgrep`), đừng đọc
> mã thoát của lệnh khởi động.

### B8. GỘP HAI TRỤC NGÂN SÁCH

Tôi đếm **mỗi lần gọi `codex exec`** là một attempt. Đó là gộp đúng hai trục mà §10 đã tách cho
phía review (`review_rounds` canon vs `review_calls` chi phí), và nó **đo nhiễu**: lượt ấy phải
gọi lại codex chỉ vì sandbox mount `.git` read-only.

**Chốt của người giữ kho:** `attempt` = một lần executor **TUYÊN BỐ DONE**; `call` = trục chi
phí, cưỡng chế riêng. Báo **bị chặn** không tiêu attempt.

### B9. "ĐỪNG ĐỌC RA NGOÀI SANDBOX" — một dòng chữ, không phải cổng

Tôi đặt log chẩn đoán ở **thư mục cha** của sandbox root, nên codex đọc được. Lần này có ích
(nó đọc log Windows thật thay vì đoán), nhưng lệnh cấm ấy **không được cưỡng chế bởi gì cả**.

> **NẾP:** muốn "không ra ngoài" là thật thì đặt MỌI thứ *trong* sandbox root.

### B10. CHÉP GIÁ TRỊ TỪ BÀN GIAO CŨ — và kết luận sai về nó

Chép `--expected-root-commit` từ bàn giao PR `#150`. Launcher chặn; tôi **vội kết luận mình bịa
số**. Đo ra thì giá trị **đúng** — clone của tôi **nông** nên không kiểm được (xem C5).

> Bài học kép: (a) chép số mà không đo là rủi ro; (b) **một cổng đỏ chưa chứng minh số của bạn sai**.

---

## C. Sự thật về công cụ / môi trường — ĐO ĐƯỢC

| # | sự thật | bằng chứng |
|---|---|---|
| C1 | Bộ ĐỌC của MCP GitHub biến đổi nội dung: escape dấu nháy (`&#34;`) và **làm biến mất** token dạng ngoặc nhọn — **kể cả trong code fence** | 3 lần trong phiên; đối chứng bằng comment do workflow đăng |
| C2 | **Chưa quy được** C1 cho tầng GHI hay tầng ĐỌC: không có client thứ hai — REST thẳng tới `repos/…` bị proxy chặn **403** | đã đo, có/không token đều 403 |
| C3 | `get_job_logs` chỉ trả **phần ĐUÔI** log ⇒ không đọc được `N/N` của bước Windows | thử `tail_lines` 600/3000 vẫn không chạm bước |
| C4 | Banner `codex exec` **in lại nguyên văn** mọi `model_reasoning_effort`, kể cả giá trị bịa. Chỉ **mã thoát** phân biệt: bịa ⇒ rc=1+ERROR; `max`/`xhigh`/`high` ⇒ rc=0 | đo trực tiếp 4 giá trị |
| C5 | Chốt root-commit của launcher **không phân biệt "sai kho" với "clone nông"**; nó in các **biên nông** như thể là root, đẩy người đọc truy nhầm hướng | `CHAN [11]` liệt kê 6 "root" ngày 14–17/08; sau `fetch --unshallow` root thật là `394e934…` (02-07) |
| C6 | Sandbox của `codex exec` mount `.git` **read-only** ⇒ không commit được; phải commit hộ | 2 lượt, codex khai đúng nguyên nhân |
| C7 | `lease_publish check` kiểm **DẠNG** băm, không kiểm **GIÁ TRỊ** | B2 |
| C8 | Tải asset GitHub release từ runner **có flake thật**: `curl: (35) Recv failure` | 1 lần; chạy lại xác nhận |
| C9 | `codex models` đòi TTY ⇒ **không liệt kê được model** phi tương tác | `Error: stdin is not a terminal` |
| C10 | `GITHUB_PATH` chỉ có hiệu lực cho **BƯỚC KẾ TIẾP** ⇒ wrapper không dùng nó để cấp công cụ cho bộ test chạy **ngay sau** installer | codex phát hiện; wrapper tự `export PATH` |

---

## D. Quyết định doctrine đã chốt trong phiên

1. **Hai trục ngân sách executor** — `attempts` (lần tuyên bố DONE) tách khỏi `executor_calls`
   (chi phí). Đối xứng với `review_rounds` / `review_calls`.
2. **CI XANH TRÊN EXACT HEAD là điều kiện CẦN của `ready to review`.** Cụ thể: lượt
   `workflow_dispatch` trên đúng head, **cả hai job success, KHÔNG job nào có bước hỏng**.
   *"PR xanh" không đủ* — `ci.yml` chỉ chạy ubuntu cho PR thường.
3. **Trần vòng review là KỶ LUẬT VẬN HÀNH, chưa có cưỡng chế máy** (§10 tự khai nợ;
   `W0-R1` từng chạy 4 vòng). Nới trần là quyết định **ghi lại được** của chủ kho, không phải
   mở một cổng.
4. **Đảo vai executor/reviewer vẫn thoả §8** miễn khác nhà cung cấp.

---

## E. Đề xuất ghi vào đâu

### E1. `CLAUDE.md` — mục "Bài học đắt giá"

Ba mục **mới**, chưa có dạng nào tương đương:

- **B1.2** command substitution đặt lại `$?` — biến thể chưa ghi của bài học `MA=$?`. Nguy hơn
  vì nó làm **cả một bảng đo** báo sai cùng lúc.
- **B2 + C7** bịa băm, và **cổng kiểm DẠNG không kiểm GIÁ TRỊ**. Nêu cả hai cùng chỗ.
- **C5** chốt neo bị **clone nông** đánh lừa; kèm B10 ("cổng đỏ chưa chứng minh số của bạn sai").

Hai mục nên **nối vào** bài học sẵn có thay vì thêm mới:

- **B7** (đọc sai thông báo tác vụ nền) → nối vào cụm *"DÒNG IN CUỐI ≠ CA CHẠY CUỐI"*.
- **B5/B4** → nối vào cụm escaping/`doctrine-scan`, kèm câu **"cả ba lần mất đều trong fence"**.

### E2. Skill `work-packet`

- Thêm chốt soạn đặc tả: **nói rõ N đếm finding hay phản chứng**, và **đối chiếu write set** có
  đủ phương tiện cho từng mục (B3).
- Thêm: `attempts` đếm **lần tuyên bố DONE**, không đếm lần gọi tiến trình (B8/D1).

### E3. Skill `cross-review`

- Thêm điều kiện **ready-to-review** (D2) như tiền đề bắt buộc trước khi cấp lease reviewer.
- Thêm cách dựng sandbox: **artefact đặt TRONG sandbox root**, cây kho ở `./kho`, và **chốt sạch
  cây đo bằng `git -C kho status --short`** — lượt đầu của phiên này `blocked` vì đặt 5 artefact
  trong cây (B9 + sự cố preflight).
- Ghi C3 (chỉ đọc được đuôi log) để lượt sau **không khai là đã đọc `N/N` của Windows**.

### E4. `.claude/dev/launcher.py` — C5

Khi `git rev-parse --is-shallow-repository` = `true`, nói thẳng *"clone nông — không kiểm được
root, chạy `fetch --unshallow`"* thay vì liệt kê biên nông như thể là root. Thuộc write set của
`#194`; **chưa quyết** cho vào đó hay mở packet mới.

---

## F. Chưa đo lại độc lập — đừng trích như phép đo hai nguồn

- **A2.3** (`curl --retry` không bao lỗi 35): suy từ tài liệu `curl`, **chưa dựng phản chứng**.
- **C1/C2**: hiện tượng đo được 3 lần, nhưng **quy trách nhiệm tầng nào thì KHÔNG ĐO ĐƯỢC**.
- Finding ZIP của vòng 3 `#203`: số là của reviewer; phiên điều phối chỉ đo lại **sau khi** đã
  vá ở `#206`, không đo trên cây `#203`.
