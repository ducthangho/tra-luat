verdict: changes_requested
reviewed_sha: 2ef85c9defe1bfc41564180a486b5462d50b8f74
reviewed_tree: c89e66b2e6476bbb75fc03390153d569d9d8c90e
provider: openai_codex
execution_surface: codex_service
transport: machine
executor: claude
reviewer: codex
round: 1

# Cross-review vong 1 — `MANG-SANDBOX-CODEX` (#334)

## 0. Kha nang chay ma va preflight

- `python3 --version` → `Python 3.11.15`, rc=0.
- `python3 -c 'print("PROBE_OK")'` → `PROBE_OK`, rc=0. Reviewer chạy được mã.
- Local HEAD detached khớp `2ef85c9defe1bfc41564180a486b5462d50b8f74`; tree
  `c89e66b2e6476bbb75fc03390153d569d9d8c90e`; base tồn tại đúng
  `ac82ddc583f688d54bdc60e06922ec09bdab9f16`.
- `python3 .claude/dev/probe_mang.py` trong chính vỏ Reviewer → rc=0 và:

  ```text
  bind_loopback=1
  urlopen=1
  git_ls_remote=1
  ```

  Đây là điểm dữ liệu thật cho sandbox Codex hiện tại và khớp ba giá trị của hàng "sandbox mặc
  định". Nó không tái lập hàng "NGOÀI codex".
- `codex sandbox` lồng không chạy được. Cả bốn tổ hợp trả rc=101 trước khi probe khởi động:

  ```text
  failed to open synthetic bubblewrap mount registry lock
  /tmp/codex-bwrap-synthetic-mount-targets-0/lock: Read-only file system (os error 30)
  ```

- Điều kiện đo thực tế khớp tài liệu: `Linux 6.18.44-fc-v21 x86_64`, Python 3.11.15,
  `codex-cli 0.150.0`, outer sandbox `workspace-write`.
- Clone không chứa Packet Issue/lease nên không thể readback độc lập `revision`, `generation`,
  `spec_hash` hay current GitHub head. Review này dùng exact SHA/base/write set do chỉ thị điều
  phối cung cấp và ghi phần thiếu vào `CHỖ KHÔNG ĐO ĐƯỢC`; không tự suy các giá trị đó.

## 1. Phán quyết việc 1 — probe có đo đúng thứ nó khai không

**Không.** Probe đo được một phép gộp "thành công hay có bất kỳ lỗi nào", nhưng in và tài liệu
diễn giải mọi lỗi thành "bị chặn". Không có ca nào phân biệt lỗi chính sách sandbox với lỗi đầu
vào, DNS, timeout, thiếu executable, repo không tồn tại hay lỗi xác thực.

Phép đo độc lập trên exact head:

| tình huống | kết quả của hàm |
|---|---:|
| `kenh_urlopen("khong-phai-url")` | 1 |
| `urlopen` ném `socket.gaierror` giả lập | 1 |
| `urlopen` ném `TimeoutError` giả lập | 1 |
| `PATH=''`, gọi thật `kenh_git_ls_remote()` | 1 |
| `subprocess.run` trả rc=128 với stderr repo không tồn tại | 1 |
| `subprocess.run` trả rc=128 với stderr xác thực hỏng | 1 |
| gọi thật `kenh_git_ls_remote('.claude/dev/KHO_KHONG_TON_TAI')` | 1 |

Các ca `t1`–`t3` tại `.claude/dev/probe_mang_test.py:46-73` không bắt nhầm lẫn này; chúng
khóa nó lại: `ValueError`/`TypeError` không liên quan chính sách cũng bắt buộc phải ra 1. Ba mutant
thu hẹp `except Exception` bị giết chính vì lỗi bug không còn bị nuốt.

Kênh mang tên `bind_loopback` cũng chưa chắc đã chạm `bind`. Chạy primitive không qua probe trong
sandbox hiện tại cho:

```text
raw_socket_create=PermissionError:[Errno 1] Operation not permitted
```

Lỗi xảy ra tại `socket.socket(...)` ở `.claude/dev/probe_mang.py:24`, trước `bind` ở dòng 26.
Do đó điểm `bind_loopback=1` hiện tại là phép đo socket creation bị từ chối, không phải phép đo
riêng thao tác bind loopback.

Về phạm vi cờ: tài liệu có nói `bind_loopback` là đối chứng nội bộ và không ra mạng
(`docs/MANG_SANDBOX_CODEX.md:8-9`). Nhưng nếu bảng bốn tổ hợp đúng, `network_access` đảo cả socket
nội bộ này; vậy cờ gate rộng hơn egress. Kết luận "cờ gây mở mạng" ở dòng 42-43 chưa gọi đúng phạm
vi. Reviewer không tái lập được phép đảo cờ vì nested sandbox rc=101.

`git ls-remote` ở `.claude/dev/probe_mang.py:45-54` chỉ đọc return code. Một rc=128 do repo/auth
hỏng và một rc=128 do đường mạng bị chặn cùng thành `MA_CHAN`; không có ca tách chúng.

## 2. Phán quyết việc 2 — bộ phản chứng có răng không

Baseline tự khai:

```text
python3 .claude/dev/probe_mang_test.py
nền: 5/5 đạt
đột biến: 5, tự khai giết 5/5
TỔNG: ĐẠT
rc=0
```

Bốn mutant sản phẩm theo số dòng đều bị giết. Tuy nhiên cổng đột biến tự giảm được số mutant,
mất guard hoặc mất đường fail-close mà vẫn xanh. Hai phản chứng ghép chứng minh đây không chỉ là
"dòng chưa đi qua ở nền xanh": xóa guard làm anchor trùng lọt rc=0; xóa fail-close làm nền đỏ
được báo `TỔNG: ĐẠT`, rc=0.

### BẢNG ĐỘT BIẾN CỦA REVIEWER

Mọi số dòng là 1-based trên exact reviewed SHA; mọi sửa/xóa chạy trên bản sao tạm ngoài repo.

| mutant theo dòng | phép thay | kết quả | ca đỏ / bằng chứng |
|---|---|---|---|
| P17-18 | đảo `MA_LOT=1`, `MA_CHAN=0` | **BỊ GIẾT** | `t1,t2,t3,t5` |
| P36-42 | cho `kenh_urlopen` luôn trả `MA_LOT` | **BỊ GIẾT** | `t2` |
| P61 | bỏ `git_ls_remote` khỏi `main` | **BỊ GIẾT** | `t4` |
| P46-54 | cho `kenh_git_ls_remote` luôn trả `MA_LOT` | **BỊ GIẾT** | `t3` |
| T109-110 | xóa entry mutant m1 | **SỐNG SÓT** | rc=0, `đột biến 4`, `TỔNG: ĐẠT` |
| T111-112 | xóa entry mutant m2 | **SỐNG SÓT** | rc=0, `đột biến 4`, `TỔNG: ĐẠT` |
| T113-114 | xóa entry mutant m3 | **SỐNG SÓT** | rc=0, `đột biến 4`, `TỔNG: ĐẠT` |
| T115-116 | xóa entry mutant m4 | **SỐNG SÓT** | rc=0, `đột biến 4`, `TỔNG: ĐẠT` |
| T117-118 | xóa entry mutant m5 | **SỐNG SÓT** | rc=0, `đột biến 4`, `TỔNG: ĐẠT` |
| T155-158 | xóa guard duy-nhất `goc.count(cu) != 1` cùng thân phụ thuộc | **SỐNG SÓT** | rc=0, `đột biến 5`, `TỔNG: ĐẠT` |
| T148-150 | xóa fail-close nền đỏ | **SỐNG SÓT** | rc=0, `đột biến 5`, `TỔNG: ĐẠT` |
| T172-173 | xóa ghi nhận mutant sống | **SỐNG SÓT** | rc=0, `TỔNG: ĐẠT` |
| T176-180 | xóa nhánh kết luận `xau` | **SỐNG SÓT** | rc=0, `TỔNG: ĐẠT` |
| P18 + T148-150 | làm nền đỏ bằng `MA_CHAN=0`, rồi xóa fail-close | **SỐNG SÓT** | nền có ca đỏ nhưng runner vẫn đếm mutant, in `TỔNG: ĐẠT`, rc=0 |
| thêm anchor trùng sau P17 + T155-158 | tạo lần xuất hiện thứ hai rồi xóa guard duy-nhất | **SỐNG SÓT** | guard còn: rc=1; guard mất: rc=0 |
| mutant m1 no-op theo T109 + xóa T172-173 | tạo mutant sống rồi xóa ghi nhận | **SỐNG SÓT** | guard còn: rc=1; guard mất: rc=0 |
| mutant m1 no-op theo T109 + xóa T176-180 | tạo mutant sống rồi xóa kết luận | **SỐNG SÓT** | guard còn: rc=1; guard mất: rc=0 |

`phai_chet` có che lỗi chéo. Mutant đảo quy ước P17-18 làm toàn suite đỏ ở bốn ca
`t1,t2,t3,t5`; bán kính ở `.claude/dev/probe_mang_test.py:167-170` chỉ chạy ca đích và sẽ chỉ
báo 1/1. Với mutant m5 tích hợp, cùng kiểu coupling bị giấu. Cách đếm hiện tại chứng minh ca đích
có đỏ, nhưng không chứng minh mutant chỉ bị ca đích giết và không hiện toàn bộ tác động.

## 3. Phán quyết việc 3 — hạng bằng chứng và tính tái lập của tài liệu

- Doctrine ở `docs/MANG_SANDBOX_CODEX.md:3-6` giữ đúng mệnh đề bắt buộc: mạng đóng là mặc định cấu
  hình, không phải bất biến an ninh. Phần này đạt.
- Dòng 48-49 có giới hạn rõ rằng cơ chế kernel chưa đo; điều kiện OS/Python/Codex/sandbox_mode ở
  dòng 14-15 hiện khớp môi trường. Phần này đạt ở mức khai báo điều kiện chung.
- Ba lệnh bảng ba cột ở dòng 19-21 đủ đối số về mặt văn bản. Lệnh thứ nhất chạy được nhưng trong
  vỏ hiện tại nó đo **trong** Codex và cho 1/1/1, nên không tái lập hàng ngoài Codex. Hai lệnh nested
  parse được nhưng chết rc=101 trước probe.
- Bốn tổ hợp ở dòng 30-39 **không có bốn lệnh nguyên văn**. Template còn token `[CỜ]`; các cột chỉ
  ghi `network_access=true` và `writable_roots=[...]`, thiếu `-c` cùng dotted key
  `sandbox_workspace_write.` cần theo `codex sandbox --help`. Tổ hợp (d) không chỉ rõ cách ghép hai
  override. `DUONG_DAN_GOC` có được định nghĩa ở dòng 32, nhưng không có một assignment/lệnh shell
  copy-paste để biến chữ `DUONG_DAN_GOC` trong TOML thành đường dẫn thật.
- Mục `KHÔNG_ĐO_ĐƯỢC` chưa đủ: nó không khai việc probe không phân biệt lỗi chính sách với lỗi
  endpoint/DNS/timeout/tool/auth; không khai kênh bind có thể dừng ở socket creation; và không khai
  phạm vi egress mới chỉ dùng HTTPS tới hai host GitHub, chưa đo giao thức/đích khác.
- Vì hai P1 ở logic phân loại và cổng mutant, câu "Cơ chế mạng ĐÃ XÁC MINH" tại dòng 42-43 hiện
  rộng hơn bằng chứng. Bảng có thể là quan sát thật của Executor, nhưng sản phẩm chưa cho Reviewer
  tái lập hoặc loại các nguyên nhân cạnh tranh.

## 4. Phán quyết việc 4 — ngân sách và phạm vi

Lệnh đúng yêu cầu:

```text
git diff --numstat ac82ddc583f688d54bdc60e06922ec09bdab9f16 -- .claude/dev/probe_mang.py .claude/dev/probe_mang_test.py docs/MANG_SANDBOX_CODEX.md
69      0       .claude/dev/probe_mang.py
186     0       .claude/dev/probe_mang_test.py
52      0       docs/MANG_SANDBOX_CODEX.md
```

Tổng = **307**, đúng lời khai và không vượt trần 320.

`git diff --name-only ac82ddc583f688d54bdc60e06922ec09bdab9f16` chỉ in đúng:

```text
.claude/dev/probe_mang.py
.claude/dev/probe_mang_test.py
docs/MANG_SANDBOX_CODEX.md
```

`git diff --name-only ac82ddc583f688d54bdc60e06922ec09bdab9f16 -- docs/GOI_AGENT_DA_NEN.md`
không in gì: tệp packet #318 không bị chạm. `git diff --check BASE..HEAD` rc=0.

## 5. Findings

### `ma-chan-gom-moi-loi-khong-phan-loai` — P1

**Tệp/dòng:** `.claude/dev/probe_mang.py:2-10,21-54`;
`.claude/dev/probe_mang_test.py:46-73`; `docs/MANG_SANDBOX_CODEX.md:8-10`.

**Vấn đề:** contract `1=bị chặn` rộng hơn phép đo. Mọi exception/child rc khác 0 thành cùng một mã;
bộ test chủ động bắt lỗi bug và bắt nó phải mang nhãn chặn. Các phép đo URL sai, PATH rỗng, repo
không tồn tại, DNS/timeout/auth giả lập đều cho 1.

**Gợi ý vá:** (1) Vá ở ba hàm kênh và schema output, vì đây là nơi mất nguyên nhân; tài liệu chỉ
được diễn giải sau khi dữ liệu còn phân loại. (2) Tách ít nhất `LOT`, `POLICY_DENIED`,
`ENDPOINT_ERROR`, `TIMEOUT`, `TOOL_ERROR`, `UNKNOWN`; lỗi không nhận dạng phải fail thành
`KHÔNG_ĐO_ĐƯỢC`, không tự nâng thành sandbox chặn. Với git, giữ rc và loại stderr đã chuẩn hóa; với
socket, ghi stage create/bind/listen. (3) Ca khóa: URL sai cú pháp, DNS lỗi, timeout, PATH rỗng,
repo không tồn tại, auth lỗi và policy-denied phải ra các lớp khác nhau; mutant gom hai lớp bất kỳ
về `MA_CHAN` phải chết. (4) Rủi ro: nhận diện lỗi theo chuỗi/errno có thể trôi theo OS/client; nếu
không chắc, chọn `UNKNOWN` và lưu dữ liệu thô đã khử nhạy cảm thay vì đoán.

### `cong-dot-bien-tu-giam-van-xanh` — P1

**Tệp/dòng:** `.claude/dev/probe_mang_test.py:107-119,138-181`.

**Vấn đề:** xóa bất kỳ một trong năm entry làm cổng xanh với bốn mutant; xóa guard duy-nhất,
fail-close, ghi nhận mutant sống hoặc nhánh kết luận cũng xanh. Phản chứng ghép còn biến anchor
trùng, nền đỏ và mutant sống thành rc=0. Vì vậy lời khai "5 đột biến, 0 sống sót" không được chính
cổng bảo vệ.

**Gợi ý vá:** (1) Vá trong meta-test độc lập cho runner, không nhét oracle tự bảo vệ vào cùng khối
nó đang đo. (2) Ghim manifest ID/count mong đợi, bơm fixture anchor trùng, nền đỏ và mutant sống rồi
đòi rc/output chính xác. (3) Ca khóa phải xóa theo số dòng từng entry và từng guard nêu trong bảng
trên; mọi mutant đó phải đỏ. (4) Rủi ro: meta-test phụ thuộc số dòng dễ vỡ khi format; nên neo theo
AST/ID ở mã kiểm chính thức nhưng runner review vẫn phải báo exact line đã thay để tránh thay nhầm
chuỗi dữ liệu.

### `bon-to-hop-chua-co-lenh-nguyen-van` — P1

**Tệp/dòng:** `docs/MANG_SANDBOX_CODEX.md:25-39`.

**Vấn đề:** đây là bằng chứng trung tâm để cô lập hai cờ, nhưng tài liệu chỉ có một template và
shorthand trong bảng, không có bốn lệnh copy-paste. Theo `codex sandbox --help`, mỗi override phải
đi qua `-c key=value`; các shorthand hiện tại không đáp ứng hợp đồng "tái lập nguyên văn".

**Gợi ý vá:** (1) Vá ngay mục Việc 4 vì thiếu nằm ở recipe, không ở bảng kết quả. (2) In đủ bốn
lệnh với dotted key và quoting thật, kèm assignment `DUONG_DAN_GOC`; lưu stdout/stderr/rc từng lệnh.
(3) Ca khóa chạy parser/smoke cho cả bốn lệnh và đòi probe thật sự khởi động; mutant bỏ một `-c`,
bỏ dotted prefix hoặc để nguyên token thay thế phải chết. (4) Rủi ro: quoting khác giữa Bash và
PowerShell; chỉ cam kết Bash/Linux đã đo, còn Windows để `KHÔNG_ĐO_ĐƯỢC` tới khi có recipe riêng.

### `network-access-gate-rong-hon-egress` — P2

**Tệp/dòng:** `.claude/dev/probe_mang.py:21-31`; `docs/MANG_SANDBOX_CODEX.md:8-9,41-43`.

**Vấn đề:** loopback không phải egress; trong sandbox hiện tại probe dừng ngay ở socket creation.
Nếu flag đảo cột này như bảng khai, flag đang gate capability socket rộng hơn "mạng ra ngoài".
Tài liệu nêu dữ kiện nhưng kết luận lại gọi nó đơn thuần là cờ mở mạng.

**Gợi ý vá:** (1) Vá tên kênh/kết luận ở probe và tài liệu. (2) Tách stage socket-create,
loopback-bind và egress-connect; gọi kết quả là phạm vi capability của config flag. (3) Ca khóa
bơm lỗi riêng tại create/bind/listen và đòi stage đúng; mutant đổi stage phải chết. (4) Rủi ro:
tăng số cột làm bảng dài hơn nhưng tránh đọc một syscall gate thành chính sách egress.

### `ban-kinh-phai-chet-che-tac-dong-cheo` — P2

**Tệp/dòng:** `.claude/dev/probe_mang_test.py:152,167-170`.

**Vấn đề:** mỗi mutant chỉ chạy `phai_chet`; mutant đảo hằng số thực tế làm bốn ca đỏ nhưng báo cáo
chỉ cho thấy ca đích. Disclosure "CHỈ" là trung thực, nhưng phép đếm che coupling và không thể phát
hiện một mutant được giết đồng thời bởi ca ngoài ý muốn.

**Gợi ý vá:** (1) Vá runner tại chỗ gọi `chay_suite`. (2) Chạy toàn bộ `CA` cho mỗi mutant, báo full
kill set; tiêu chí tối thiểu là ca đích có mặt, còn exclusivity chỉ ép khi spec thật sự đòi. (3) Ca
khóa dùng mutant P17-18 và đòi báo đủ `t1,t2,t3,t5`. (4) Rủi ro: coupling hợp lệ sẽ làm output ồn;
đừng tự coi ca đỏ phụ là lỗi, chỉ đừng giấu nó.

## 6. CHỖ KHÔNG ĐO ĐƯỢC

| ô / khẳng định | lệnh đã thử | lỗi hoặc lý do |
|---|---|---|
| Hàng đối chứng NGOÀI Codex 0/0/0 | `python3 .claude/dev/probe_mang.py` | vỏ này nằm trong Codex; lệnh cho 1/1/1, nên không phải đối chứng ngoài |
| Hàng nested mặc định | `codex sandbox -c sandbox_mode=workspace-write -- python3 .claude/dev/probe_mang.py` | rc=101, bubblewrap mount registry lock read-only |
| Hàng nested bật network | `codex sandbox -c sandbox_mode=workspace-write -c sandbox_workspace_write.network_access=true -- python3 .claude/dev/probe_mang.py` | rc=101, cùng lỗi lock trước probe |
| Tổ hợp (a) | lệnh nested không override | rc=101, không có giá trị bind/url/git |
| Tổ hợp (b) | nested với `network_access=true` | rc=101, không có giá trị bind/url/git |
| Tổ hợp (c) | nested với `writable_roots` là `.git` và `/tmp` | rc=101, không có giá trị bind/url/git |
| Tổ hợp (d) | nested với cả hai override | rc=101, không có giá trị bind/url/git |
| Current GitHub remote/head | `git ls-remote https://github.com/ducthangho/tra-luat.git HEAD` | rc=128; không kết nối được proxy loopback, nên chỉ exact local SHA được xác minh |
| Packet revision/generation/spec hash | tìm toàn repo bằng `rg` cho packet #334/slug/SHA | không có Packet Spec/lease/handoff tương ứng trong clone |
| OS khác, Codex khác, sandbox mode khác | không có execution surface tương ứng | đúng như tài liệu đã khai `KHÔNG_ĐO_ĐƯỢC` |

## 7. Kết luận

`changes_requested`. Còn ba finding P1:
`ma-chan-gom-moi-loi-khong-phan-loai`, `cong-dot-bien-tu-giam-van-xanh`, và
`bon-to-hop-chua-co-lenh-nguyen-van`. Theo luật dừng của kho, **không land exact SHA này khi các P1
còn mở**. Hai P2 phải thành nợ có tên nếu không sửa trong packet này; chúng không phải lý do riêng
để giữ packet mở sau khi mọi P1 đã đóng.
