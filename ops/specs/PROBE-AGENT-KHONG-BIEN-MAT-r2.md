# ĐẶC TẢ PACKET — `PROBE-AGENT-KHONG-BIEN-MAT` — **BẢN SỬA ĐỔI 2**

```yaml
packet_id: PROBE-AGENT-KHONG-BIEN-MAT
revision: 2
generation: 1
review_class: sensitive        # sua duong PHONG cua launcher — chot chan truoc moi luot agent
executor: codex
reviewer: claude
assurance_target: cross_approved
```

## 0. Vấn đề — một phép đo, chạy được, hai chiều

`chay_cac_probe` quyết định có chạy probe `claude_trust` hay không bằng **duy nhất phần tử đầu**
của argv:

```python
if Path(str(lenh[0])).name.casefold() in ("claude", "claude.exe"):
    ds["claude_trust"] = _probe_trust_claude(ws)
```

Đo 28-08-2026, gọi thẳng `chay_cac_probe` trên chính kho này (khoá `hasTrustDialogAccepted`
**VẮNG** ⇒ `claude_trust=KHONG_DO_DUOC`; xem §7):

```
phong THANG   claude -p x            -> CHAN ma=15: probe nang luc khong dat: claude_trust=KHONG_DO_DUOC
qua bash -c   'claude -p x'          -> CHO CHAY, probe=['ghi','spawn','workspace']
                                        <- claude_trust BIEN MAT, khong mot dong canh bao
```

**Mọi lượt phóng reviewer claude của phiên 27-08 đều đi qua đường thứ hai** (`bash -c 'cd "$0" &&
claude …'`, vì cần đổi thư mục trước khi gọi). Tức chốt ấy **chưa từng chạy** trong các lượt nó
sinh ra để gác, và không ai biết — trên sổ `run.json` chỉ thấy `probe` có ba mục, không có mục nào
nói "đã bỏ qua một probe".

Đây đúng hình dạng `CLAUDE.md` đã trả giá: **"cổng vắng mặt trông giống cổng xanh"**. Khác các lần
trước ở một điểm làm nó tệ hơn: cổng này **vắng mặt CÓ ĐIỀU KIỆN**, và điều kiện lại là *cách gõ
lệnh* — thứ người dùng đổi vì lý do chẳng liên quan gì tới an ninh (cần `cd`).

### Vì sao KHÔNG chữa bằng cách đọc chuỗi shell

Cám dỗ đầu tiên là dò chữ `claude` trong `lenh[1:]`. **Đừng.** Với `bash -c 'cd "$0" && claude …'`
toàn bộ script là **MỘT** phần tử argv, nên `Path(x).name` của nó không phải `claude`; muốn bắt
được thì phải phân tích cú pháp shell. Kho này đã đặt tên cho lối ấy: *"hiểu nửa vời chính là lỗ
vừa bị đo"*. Một bộ phân tích shell nửa vời sẽ trượt `exec claude`, `$AGENT`, `env X=1 claude`,
`sh -c "$(printf …)"` — và mỗi lần trượt là một lần cổng lại vắng mặt im lặng.

## 1. `write_set`

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

Đúng hai đường. Cần đụng gì khác thì **DỪNG và báo**, đừng tự mở rộng.
Đo 2026-08-28 (`ai-dang-giu`, sau khi so hai nguồn bằng TẬP TÊN 236=236, `comm` hai chiều RỖNG):
cả hai `rc=0`, NGƯỜI_GIỮ 0.

## 2. `ngan_sach_kich_thuoc`

| | |
|---|---|
| tệp tối đa | **2** |
| dòng thêm tối đa | **220** |

Thấp có chủ ý: đây là **một cờ, một bảng, một nhánh fail-close**. Vượt ⇒ DỪNG và NÉN.

## 3. Hợp đồng — KHAI BÁO, không phải ĐOÁN

Đảo bài toán: thay vì đoán lệnh sẽ chạy agent nào, **bắt người gọi KHAI**, và **chặn khi không
khai được**.

### 3.1 Cờ mới `--agent <tên>`

Allow-list, so BẰNG NHAU sau `strip()`:

```
AGENT_CHO_PHEP = ("claude", "codex", "khong")
```

- `--agent claude` ⇒ chạy bộ probe của claude (`claude_trust`) bất kể `lenh[0]` là gì;
- `--agent codex`  ⇒ chạy bộ probe của codex (hiện **rỗng** — khai thẳng là rỗng, đừng bịa probe);
- `--agent khong`  ⇒ khai CÓ CHỦ ĐÍCH rằng lượt này không chạy agent nào; không probe agent;
- giá trị ngoài allow-list ⇒ `Chan(MA_THAM_SO)`. **Không** casefold, **không** đoán gần đúng.

### 3.2 Suy ra khi KHÔNG khai — giữ nguyên hành vi cũ, chỉ ở ca RÕ RÀNG

Không có `--agent`:

- `Path(lenh[0]).name.casefold()` khớp một tên trong `AGENT_CHO_PHEP` ⇒ dùng agent ấy (đây là
  hành vi hôm nay, giữ nguyên để không phá lượt gọi đang chạy);
- `lenh[0]` là **VỎ SHELL** ⇒ xem §3.3;
- còn lại ⇒ coi như `khong`.

### 3.3 VỎ SHELL mà không khai ⇒ CHẶN, và đây là lõi của packet

```
VO_SHELL = ("bash", "sh", "dash", "zsh", "ksh", "cmd", "cmd.exe",
            "powershell", "powershell.exe", "pwsh", "pwsh.exe")
```

`Path(lenh[0]).name.casefold()` nằm trong tập ấy **và** không có `--agent` ⇒
`Chan(MA_THAM_SO)` với thông điệp nói đủ ba điều: (a) vì sao chặn — *lệnh đi qua vỏ shell nên
launcher KHÔNG đọc được nó sẽ chạy agent nào*; (b) cách chữa — thêm `--agent claude|codex`;
(c) cách khai không có agent — `--agent khong`.

Đây là **danh sách CHO PHÉP đảo chiều đúng cách**: `VO_SHELL` không phải danh sách cấm cần đoán
hết mọi vỏ shell trên đời. Nó chỉ là **gợi ý bắt buộc khai** cho các vỏ đã biết; vỏ lạ rơi vào
nhánh "còn lại ⇒ `khong`" y như hôm nay — **không tệ hơn hiện trạng**, và người dùng vỏ lạ vẫn
khai được bằng `--agent`. Nói thẳng giới hạn ấy trong docstring: packet này **không** đóng được
ca "vỏ shell chưa biết tên"; nó đóng ca **đã biết và đang dùng hằng ngày**.

### 3.4 Sổ phải GHI cái đã bỏ qua

`run.json` phải mang, ở mọi lượt:

```
agent_da_khai   : "claude" | "codex" | "khong" | null      (null = suy ra, khong ai khai)
agent_suy_ra    : ket qua sau §3.2/§3.3
probe_da_chay   : [ten...]           (nhu hom nay)
probe_bo_qua    : [ten...]           (MOI — probe cua agent KHAC, khong chay o luot nay)
```

Lý do có `probe_bo_qua`: hôm nay `run.json` chỉ liệt kê probe **đã chạy**, nên một probe biến mất
không để lại dấu nào. Một cổng vắng mặt phải **tự khai là mình vắng**.

## 4. `.claude/dev/launcher_test.py` — phản chứng

Ma trận BIẾT TRƯỚC ĐÁP ÁN, mỗi ô một khẳng định:

| `lenh[0]` | `--agent` | phải ra |
|---|---|---|
| `claude` | (không) | chạy `claude_trust` — **hành vi hôm nay, chống hồi quy** |
| `bash` | (không) | **CHẶN** `MA_THAM_SO`, thông điệp có đủ ba điều §3.3 |
| `bash` | `claude` | chạy `claude_trust` — **đây là ca packet sinh ra để đóng** |
| `bash` | `khong` | không probe agent, `rc` như hôm nay |
| `bash` | `codex` | không `claude_trust`; `probe_bo_qua` có `claude_trust` |
| `pwsh`/`cmd` | (không) | **CHẶN** — vỏ shell không chỉ có `bash` |
| `git` | (không) | không probe agent (nhánh "còn lại") — **chống chặn oan** |
| bất kỳ | `Claude`/`CLAUDE`/`claudex` | `MA_THAM_SO` — allow-list so BẰNG NHAU |

Cộng hai ca sổ: `probe_bo_qua` có mặt và ĐÚNG; `agent_da_khai` phân biệt `null` với `"khong"`.

**ĐỘT BIẾN — mỗi chốt một cái, và runner phải đòi giết ĐÚNG VÀ CHỈ ĐÚNG tập đã khai** (chạy mỗi
đột biến trên TOÀN BỘ ca). Tối thiểu:

| đột biến | phải giết |
|---|---|
| bỏ nhánh `VO_SHELL` (vỏ shell không khai ⇒ cho chạy) | ca `bash` không cờ, ca `pwsh` |
| `--agent` không ghi đè suy luận từ `lenh[0]` | ca `bash` + `--agent claude` |
| allow-list agent nhận cả `Claude` (casefold) | ca chính tả |
| `probe_bo_qua` luôn rỗng | ca sổ |
| `agent_da_khai` gộp `null` và `"khong"` | ca sổ |

Nền có ca ĐỎ ⇒ **TỪ CHỐI công bố điểm đột biến**.

## 5. Cổng phải xanh, và ĐO NỀN TRƯỚC KHI NGHI BẢN VÁ

```
git config core.abbrev 7
python3 .claude/dev/launcher_test.py          # headline phai la N/N va KHONG con ca BO QUA moi
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 .claude/dev/packet_loop.py adr-song --root .
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py workflow-audit  --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 ops/lease_publish_test.py
```

**NỀN ĐO LẠI 28-08-2026 trên `origin/master` `27fb9de` — bản sửa đổi 1 dán SỐ ĐÃ TRÔI, đây là
số đo thật, CẢ HAI NỀN:**

```
launcher_test Linux   : 154/154 ca DA CHAY QUA (tong 155, bo qua 1, hong 0)
                        - KHONG DU: 1 ca BO QUA, chua do gi
                        (ca bo qua la t62, fixture danh cho Windows; ban POSIX la t63)
launcher_test Windows : 140/140 ca DA CHAY QUA (tong 155, bo qua 15, hong 0)
                        (CI `launcher (Windows that)`, run 33139903666, head 73c91cb)
lease_publish         : 116/116 bo qua 0  CHI KHI co actionlint 1.7.7 + shellcheck 0.10.0.
                        Thieu hai cong cu => 115/116, do dung MOT ca (`t33` fail-close
                        "KHONG DO DUOC"). Do la MOI TRUONG, khong phai hoi quy.
```

**Bản sửa đổi 1 ghi `114/114` và `95/114`; cả hai SAI** — đo lại cho `116/116` và `115/116`.
Thiếu công cụ mất **1** ca, không phải 19. `CLAUDE.md` cũng ghi Windows bỏ qua **13** ca (đo
17-08); đo 28-08 là **15** (thêm `t125`/`t126`, nhóm `bridge`). Không con nào là hồi quy — tài
liệu cũ hơn mã. Rút ra: **một con số không ghi ĐIỀU KIỆN ĐO thì sẽ trôi mà không ai biết**, nên
executor phải TỰ ĐO LẠI và khai số của mình chứ đừng chép bảng này.

Cổng nào đỏ ⇒ chạy lại trên `origin/master` sạch, so DELTA; đỏ sẵn thì ghi "đỏ sẵn, delta = 0".

## 6. Điều KHÔNG được làm

- **Không phân tích cú pháp chuỗi shell** để đoán agent — xem §0;
- không đụng đường nào ngoài `write_set`;
- không đổi ý nghĩa mã thoát nào đang có (`MA_PROBE=15`, `MA_WORKTREE`, `124/125`);
- không nới `--bo-qua-probe`: nó đã có và đã đòi lý do khác rỗng — giữ nguyên;
- không tự merge, không tự đẩy `master`;
- nghĩ ra được một hướng hỏng thì **biến ngay thành ca `rXX_`**, đừng để nó nằm trong chú thích.

## 7. Nói thẳng cái packet này KHÔNG chữa

Trên container kiểu này, khoá `hasTrustDialogAccepted` **VẮNG HẲN** — `/root/.claude.json` có
`projects: {}` — nên `_probe_trust_claude` trả **`KHONG_DO_DUOC`**, KHÔNG phải `DO`. (Bản sửa đổi 1
ghi `= False`; sai trạng thái, đúng hậu quả.) Cả hai đều non-`DAT` nên đều chặn `ma=15`, và kho đã
có sẵn ca `r05_trust_thieu_khoa_la_khong_do_duoc` khoá đúng hành vi ấy — **đừng "sửa" cho ra `DO`**.
Đây là doctrine `None ≠ False`, giữ nguyên. Nên khi probe **bắt đầu chạy đúng**, các
lượt phóng qua `bash -c` **sẽ bị CHẶN** — đó là chốt làm đúng việc, không phải hồi quy. Người vận
hành có đúng hai đường, và cả hai phải được nêu trong thông điệp chặn: nhận trust một lần bằng
`claude` tương tác, hoặc truyền `--bo-qua-probe "<lý do>"`. Packet này **không** tự đặt trust hộ
ai — đặt trust là quyết định của người, không phải của một cổng.

## 8. Ràng buộc thi công — đo được 28-08, bản sửa đổi 1 KHÔNG có

### 8.1 `t117` là bẫy riêng của lượt này

`t117` đòi mẫu tìm-thay của **mỗi** đột biến khớp **ĐÚNG MỘT** chỗ trong `launcher.py`, vì
`chay_dot_bien` thay chỗ khớp **ĐẦU TIÊN**. Packet này **thêm mã** vào `launcher.py`. Nếu mã mới
trùng chữ với đoạn một đột biến cũ đang nhắm **và đứng trước nó**, đột biến ấy lặng lẽ nhảy sang
bản sao: **ca đích thôi chết mà bảng vẫn báo "đạt"**. Đã xảy ra thật một lần trong kho này
(khối chuẩn hoá env chép vào `_suc_khoe_mcp_github` trùng khít khối của `_do_github`).

⇒ Chạy `t117` và **đọc kết quả của nó**, đừng chỉ đọc tổng. Triệu chứng là một mutant cũ đột nhiên
`giết 0/1`, không phải một dòng logic sai.

### 8.2 Ca mới KHÔNG được im lặng biến mất trên Windows

Executor chỉ chạy được Linux; Windows do CI đo sau. Mỗi ca thêm vào phải rơi vào ĐÚNG MỘT:

- **chạy được cả hai nền** — không dùng khái niệm riêng POSIX (`SIGTERM`, `setsid`, nhóm tiến
  trình, `SIG_IGN`) trong thân ca; hoặc
- **BỎ QUA CÓ KHAI** trên Windows, đúng nếp 15 ca đang có: in `BO QUA <ten>: <ly do cu the>`.

Packet này sinh ra vì **một chốt biến mất không để lại dấu**. Để bộ test của chính nó lặp lại hình
dạng ấy trên Windows thì hỏng nghĩa. Báo cáo phải phân loại từng ca mới theo hai nhánh trên.

### 8.3 PR phải gắn nhãn `windows` trước khi merge

PR chạm `.claude/dev/**` ⇒ gắn nhãn `windows`. Đo được 28-08: `launcher-windows.yml` **có**
`labeled` trong `types:`, nên nhãn tự nó bắn một lượt chạy — **3 giây** sau khi gắn. (Khác `ci.yml`:
tệp đó khai `pull_request:` mà **thiếu `types:`**, nên nhãn ở đó KHÔNG bắn lượt nào.) Không gắn thì
`push: branches:[master]` biến **lần merge thành lần đo Windows ĐẦU TIÊN** — đúng bài học (c).

### 8.4 THỨ TỰ — packet này xếp SAU #368

Đo `2026-08-28T08:5xZ`, sau khi so hai nguồn (`ls-remote 247 = for-each-ref 247`, `comm` rỗng hai
chiều) và chữa `rc=12` NHÁNH_CỤC_BỘ_TỤT_SAU:

```
ai-dang-giu .claude/dev/launcher.py       -> NGUOI_GIU 1: w1-p1-van-chuyen-prompt-exec-1-codex-20260828
ai-dang-giu .claude/dev/launcher_test.py  -> NGUOI_GIU 1: (y het)
```

Packet **#368 (W1-P1)** giữ ĐỘC QUYỀN cả hai đường, hết hạn `2026-08-29T06:45:00Z`. **KHÔNG được
cấp lease cho packet này trước khi #368 nhả** — cấp chồng là tái tạo đúng sự cố hai-writer đã xảy
ra sáng 28-08 giữa #359 và #363.

Và **quét lại NGAY TRƯỚC lúc đăng lease**, đừng dùng kết quả quét cũ: sự cố ấy sinh ra từ một cửa
sổ **3 phút** giữa lúc quét và lúc đăng, trong đó hai lease cùng khai `NGƯỜI_GIỮ 0` và cùng thành thật.
