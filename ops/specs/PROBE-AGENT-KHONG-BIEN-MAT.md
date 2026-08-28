# ĐẶC TẢ PACKET — `PROBE-AGENT-KHONG-BIEN-MAT`

```yaml
packet_id: PROBE-AGENT-KHONG-BIEN-MAT
revision: 1
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

Đo 28-08-2026, gọi thẳng `chay_cac_probe` trên chính kho này (`hasTrustDialogAccepted = False`):

```
phong THANG   claude -p x            -> CHAN ma=15: probe nang luc khong dat: claude_trust=DO
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

**Nền đo được 28-08-2026 trên `origin/master`, dán vào đây để không ai nghi bản vá của mình:**

```
launcher_test : 154/154 ca DA CHAY QUA (tong 155, bo qua 1, hong 0)
                - KHONG DU: 1 ca BO QUA, chua do gi
                (ca bo qua la t62, fixture danh cho Windows; ban POSIX la t63)
lease_publish : 114/114  CHI KHI co actionlint 1.7.7 + shellcheck 0.10.0 tren PATH.
                Thieu hai cong cu ay => 95/114, va do la MOI TRUONG, khong phai hoi quy.
```

Cổng nào đỏ ⇒ chạy lại trên `origin/master` sạch, so DELTA; đỏ sẵn thì ghi "đỏ sẵn, delta = 0".

## 6. Điều KHÔNG được làm

- **Không phân tích cú pháp chuỗi shell** để đoán agent — xem §0;
- không đụng đường nào ngoài `write_set`;
- không đổi ý nghĩa mã thoát nào đang có (`MA_PROBE=15`, `MA_WORKTREE`, `124/125`);
- không nới `--bo-qua-probe`: nó đã có và đã đòi lý do khác rỗng — giữ nguyên;
- không tự merge, không tự đẩy `master`;
- nghĩ ra được một hướng hỏng thì **biến ngay thành ca `rXX_`**, đừng để nó nằm trong chú thích.

## 7. Nói thẳng cái packet này KHÔNG chữa

`hasTrustDialogAccepted = False` trên kho này (đo 28-08). Nên khi probe **bắt đầu chạy đúng**, các
lượt phóng qua `bash -c` **sẽ bị CHẶN** — đó là chốt làm đúng việc, không phải hồi quy. Người vận
hành có đúng hai đường, và cả hai phải được nêu trong thông điệp chặn: nhận trust một lần bằng
`claude` tương tác, hoặc truyền `--bo-qua-probe "<lý do>"`. Packet này **không** tự đặt trust hộ
ai — đặt trust là quyết định của người, không phải của một cổng.
