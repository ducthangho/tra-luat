# CROSS-REVIEW lượt 6 — `ops/moi-truong-env-first` head `c775c0a` — reviewer `codex`

**CHỈ ĐỌC**: không sửa tệp kho, không commit/push/merge/land/deploy. Người vá là `claude`
⇒ reviewer phải là `codex` (§8). **KHÔNG PHẢI wp55**, không tiêu attempt của packet.

## Bước 0

`git fetch`/`git config` không chạy được trong vai này (sandbox codex đặt `.git/` chỉ đọc).
Điều phối chạy hộ trong chính clone bạn đứng. Xác minh **bằng đọc**:

```bash
git rev-parse --is-shallow-repository   # ĐÒI false
git config --get core.abbrev            # ĐÒI 7
git rev-parse HEAD                      # ĐÒI c775c0a5b0bf0816e913ba0b300d898fec3c58b0
git diff --name-status fe895a068368754bd11b25ca59c504f973e9f086 c775c0a5b0bf0816e913ba0b300d898fec3c58b0
#   ĐÒI 2 tệp: .claude/dev/launcher.py · .claude/dev/launcher_test.py
```

Không tin thì **nêu thành finding và VẪN LÀM TIẾP** — mỏ neo là SHA bất biến.

## Delta: BA commit, gộp một lượt

```
d9029c6  bộ test TỰ KHAI môi trường
ad60b6f  chốt TRƯỞNG NHÓM trước killpg — lỗ giết nhầm THẬT trong launcher.py
c775c0a  _do_codex thôi nâng nhãn vượt quá bằng chứng
```

Lượt 5 đã cấp lease cho `ad60b6f` nhưng **KHÔNG chạy được**: credential codex bị thu hồi
giữa chừng (`refresh_token_invalidated`). Nên `d9029c6` và `ad60b6f` **chưa ai soi**, gộp
vào lượt này.

### 1. `d9029c6` — tự khai môi trường

Ba lượt liền hai bên đo cùng một cổng ra hai kết quả, mỗi bên tự nhất quán. Commit này
không sửa cổng; nó bắt cổng khai nó đang chạy ở đâu. Đã đổi hướng chẩn đoán ngay:
`chung_nhom_voi_cha` **TRUE ở cả hai** môi trường ⇒ giả thuyết dùng để vá `setsid`
(`fe895a0`) **giải thích không đủ** — đúng như bạn chỉ ra ở lượt 4.

Khối này cũng tự phơi ra một lỗi của chính nó: cờ `trong_pid_namespace` bản đầu luôn
`false` vì trong namespace thì `/proc/1` cũng thuộc namespace ấy. Đã bỏ cờ, giữ số thô.

### 2. `ad60b6f` — chốt TRƯỞNG NHÓM (truy từ manh mối `launcher.py:720/739` của bạn)

`os.killpg` nhận **process group id**, `_giet_cay` cầm **pid**. Chỉ bằng nhau khi tiến
trình là trưởng nhóm — giả định `start_new_session` tạo ra nhưng **không ai kiểm tại chỗ
giết**. Đo được: con không kèm `start_new_session` có pid=26072 pgid=26071, mà `_giet_cay`
vẫn gọi `killpg(26072)` — nhắm vào nhóm **không phải** của mục tiêu. Máy thường pid lớn nên
nhóm đó hầu như không tồn tại; trong PID namespace pid chạy từ 1 nên dễ trúng nhóm có thật.

Vá: `getpgid(pid) != pid` ⇒ từ chối, không gọi `killpg`. Không đo được ⇒ đi tiếp.

### 3. `c775c0a` — `_do_codex` thôi nâng nhãn vượt quá bằng chứng

Lần **thứ hai** cùng lớp lỗi trong đúng hàm này trong đúng một ngày. `codex login status`
trả rc=0 "Logged in" trong khi mọi lời gọi thật trả 401 `refresh_token_invalidated`.

Ba nhãn cho ba mức bằng chứng: `CO_CREDENTIAL` (có tệp, đọc được, chưa hết hạn — **chưa**
chứng minh dùng được) · `CHUA_XAC_THUC` (đo được là hỏng) · `DUNG_DUOC` (**chỉ** khi
`--kiem-song` gọi thật và thành công).

Phần offline một mình đã bắt được sự cố: `id_token` hết hạn 39h trước, `last_refresh` quá
40h — bản trước báo `DUNG_DUOC`.

## Việc của lượt này

1. **Chốt trưởng nhóm**: còn đường nào tới `killpg` không qua chốt (`_giet_windows`,
   `_giet_rieng`)? Có **từ chối oan** không (tiến trình vừa chết, pid tái dùng, race giữa
   `getpgid` và `killpg`)? Có mua an toàn bằng cách **không giết được gì nữa** không?
2. **Ba nhãn**: `CO_CREDENTIAL` có bị đối xử như `DUNG_DUOC` ở đâu trong dòng chảy không?
   `_han_token_codex` đọc JWT **không xác thực chữ ký** — có chỗ nào lời khai đó bị dùng
   như bằng chứng mạnh hơn thực tế không? Có **rò giá trị token** qua `exp`/thông điệp không?
   `_do_codex_song` chạy `codex exec` thật — có tác dụng phụ nào (ghi tệp, đổi auth.json,
   tốn quota ngoài dự kiến)?
3. **Bản khai môi trường**: còn khoá nào cần mà thiếu? Có **rò thông tin nhạy cảm** không?
   `_do_an_toan` nuốt `BaseException` — có nuốt nhầm `KeyboardInterrupt`/`SystemExit`?
4. **`t85` đã ĐỔI KỲ VỌNG** (từ `DUNG_DUOC` sang `CO_CREDENTIAL`) và được ghim
   `_han_token_codex` để thôi đọc `~/.codex/auth.json` thật. Đổi kỳ vọng của một ca sẵn có
   là việc cần soi kỹ: nó **đúng theo hợp đồng mới**, hay là **nới ca cho vừa bản vá**?
5. **Dán BẢN KHAI MÔI TRƯỜNG của bạn** vào verdict, và chạy `--dot-bien` **hai lần**. Sau
   ba lượt tranh cãi con số, đây là lượt đầu hai bên có thứ để so.
6. `setsid` ở `fe895a0` **giữ nguyên**. Nếu bạn cho rằng chốt trưởng nhóm khiến nó thành
   **thừa** hoặc **có hại**, nói thẳng — đó là finding có giá trị.

## CẢNH BÁO AN NINH

Không in **giá trị** biến môi trường hay token. Phản chứng đụng credential chạy trên
`HOME=$(mktemp -d)`; **không** đụng `~/.codex/auth.json` thật — credential vừa được cấp lại,
làm hỏng nó là chặn mọi lượt sau.

## Verdict

`approve` · `changes_requested` · `blocked`. Bằng chứng **neo SHA bất biến**. Nói thẳng chỗ
không chạy được. `approve` hợp lệ nếu thật sự không tìm ra gì.

Ghi verdict RA TỆP:

```
ops/reviews/moi-truong-review-6-codex-verdict.md
ops/reviews/moi-truong-review-6-codex-verdict.receipt.yaml
```

Xuất thẳng `stdout` ra tệp, báo `sha256` + số byte.
