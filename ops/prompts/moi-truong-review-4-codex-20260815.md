# CROSS-REVIEW lượt 4 — `ops/moi-truong-env-first` head `fe895a0` — reviewer `codex`

**CHỈ ĐỌC**: không sửa tệp kho, không commit/push/merge/land/deploy. Đầu ra là **verdict**
+ **evidence §7**. Người vá là `claude` ⇒ reviewer phải là `codex` (§8).

**KHÔNG PHẢI wp55.** `la_viec_cua_packet: false` — không tiêu attempt của packet.

## Bước 0 — hai lệnh khác prompt, đã xử lý sẵn

`git fetch`/`git config` không chạy được trong vai này (sandbox `workspace-write` của
codex đặt `.git/` chỉ đọc). Điều phối chạy hộ trong chính clone bạn đứng. Xác minh bằng đọc:

```bash
git rev-parse --is-shallow-repository       # ĐÒI false
git config --get core.abbrev                # ĐÒI 7
git rev-parse HEAD                          # ĐÒI fe895a0...
git diff --name-status c89ca5929c2d5da6c182f7858e652c51df147cd5 <HEAD>
#   ĐÒI ĐÚNG 1 tệp: .claude/dev/launcher_test.py
```

Không tin thì **nêu thành finding và VẪN LÀM TIẾP** — mỏ neo là SHA bất biến.

## Delta: đáp lại finding lượt 3 của chính bạn

Bạn báo suite không in tổng kết, và lệnh shell sau python cũng không chạy. Điều phối tái
lập được và tìm ra cơ chế:

```
trong sandbox:  python3 launcher_test.py        -> VO SHELL CHET, log 1 dong
                setsid python3 launcher_test.py -> rc=0, day du, shell SONG
                vo shell: pid=2 pgid=1
```

`launcher.py` giết theo **nhóm** (`killpg`). Máy thường có job control nên python là
trưởng nhóm riêng; trong PID namespace nó **thừa kế nhóm 1 của shell**, nên `killpg` cuốn
theo cả shell.

**Vá:** `_tu_tach_nhom_neu_can()` chạy trước mọi thứ trong `main()` — không phải trưởng
nhóm thì `setsid()`. Máy thường ta LÀ trưởng nhóm nên chốt không làm gì.

Điều phối đo **trong sandbox, không có `setsid` bọc ngoài**: `da tach sang session moi
(pgid=3)` · `90/90` · rc=0 · **vỏ shell sống** (trước khi vá: tệp chứng KHÔNG được tạo).

## Việc của lượt này

1. **Tự chạy trong môi trường của bạn.** Đây là finding của bạn; bạn là người duy nhất đã
   thấy nó hỏng. Chạy suite và `--dot-bien` **ít nhất hai lần**, và kiểm xem vỏ shell có
   sống không (đặt một lệnh `echo` SAU python và xem nó có chạy không).
2. **`setsid()` có tác dụng phụ nào không?** Nó bỏ terminal điều khiển. Có ca nào cần
   terminal, cần job control, hay cần nhận tín hiệu từ nhóm cũ không? `--dot-bien` có bị
   ảnh hưởng không?
3. **Chốt có tự bắn vào chân không?** Nếu `setsid()` thành công, các ca giết-cây có còn đo
   đúng thứ chúng khai không, hay nay chúng chạy trong ngữ cảnh khác và trở nên vô hại
   (tức là xanh GIẢ)? Đây là câu hỏi nặng nhất của lượt này.
4. **`t90` có răng không?** Đột biến từng nhánh trên **bản sao** và xem nó có đỏ không.
5. Điều phối tự khai **chưa chỉ được đích danh ca nào** phát `killpg`, và bản vá chặn HẬU
   QUẢ chứ chưa chỉ ra thủ phạm. Bạn tìm được thì đó là finding có giá trị.

Phần delta trước đã duyệt (cô lập toàn cục, `t89`, oracle, `hook-nang-luc`) **đừng soi
lại** trừ khi đo được điều khác.

## CẢNH BÁO AN NINH

Không in **giá trị** biến môi trường nào. Mọi phản chứng đụng credential chạy trên
`HOME=$(mktemp -d)`; **không** ghi/xoá/đổi `~/.codex/auth.json` thật.

## Verdict

`approve` · `changes_requested` · `blocked`. Mỗi finding: `finding_id`, `severity`,
`disposition`, bằng chứng chạy được **neo SHA bất biến**. Nói thẳng chỗ không chạy được.
`approve` hợp lệ nếu thật sự không tìm ra gì.

Ghi verdict RA TỆP (REST bị proxy 403, `gh` không cài):

```
ops/reviews/moi-truong-review-4-codex-verdict.md
ops/reviews/moi-truong-review-4-codex-verdict.receipt.yaml
```

Xuất thẳng `stdout` ra tệp, báo `sha256` + số byte.
