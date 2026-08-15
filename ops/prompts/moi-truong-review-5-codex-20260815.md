# CROSS-REVIEW lượt 5 — `ops/moi-truong-env-first` head `ad60b6f3402f1f8cca80f716667464734ea44395` — reviewer `codex`

**CHỈ ĐỌC**: không sửa tệp kho, không commit/push/merge/land/deploy. Người vá là
`claude` ⇒ reviewer phải là `codex` (§8). **KHÔNG PHẢI wp55**, không tiêu attempt.

## Bước 0

`git fetch`/`git config` không chạy được trong vai này (sandbox codex đặt `.git/` chỉ
đọc). Điều phối chạy hộ trong chính clone bạn đứng. Xác minh bằng đọc:

```bash
git rev-parse --is-shallow-repository        # ĐÒI false
git config --get core.abbrev                 # ĐÒI 7
git rev-parse HEAD                           # ĐÒI ad60b6f3402f1f8cca80f716667464734ea44395
git diff --name-status fe895a068368754bd11b25ca59c504f973e9f086 ad60b6f3402f1f8cca80f716667464734ea44395
#   ĐÒI 2 tệp: .claude/dev/launcher.py · .claude/dev/launcher_test.py
```

## Delta: HAI commit, gộp một lượt theo yêu cầu chủ kho

### 1. `d9029c6` — bộ test TỰ KHAI môi trường

Ba lượt liền hai bên đo cùng một cổng ra hai kết quả, mỗi bên tự nhất quán. Commit này
không sửa cổng; nó bắt cổng khai nó đang chạy ở đâu, để hai phép đo SO ĐƯỢC với nhau.
`--moi-truong` in JSON; dòng gọn luôn in ở đầu mọi lượt chạy kể cả `--dot-bien`.

**Nó đã đổi hướng chẩn đoán ngay:**

```
                     điều phối              sandbox codex
pid/pgid/sid         20239/20237/19879      3/1/1
chung_nhom_voi_cha   TRUE                   TRUE      <- GIONG NHAU
ns_pid               pid:[4026531836]       pid:[4026532315]
```

`chung_nhom_voi_cha` TRUE ở **cả hai** ⇒ "chung nhóm với vỏ shell" KHÔNG phân biệt được
hai môi trường, tức giả thuyết dùng để vá `setsid` ở `fe895a0` **giải thích không đủ** —
đúng như bạn đã chỉ ra.

Khối này cũng **tự phơi ra một lỗi của chính nó**: cờ `trong_pid_namespace` bản đầu so ns
của mình với ns của `/proc/1`, mà trong namespace thì hai cái luôn bằng nhau nên cờ luôn
`false`. Đã bỏ cờ, chỉ giữ số thô.

### 2. `ad60b6f3402f1f8cca80f716667464734ea44395` — chốt TRƯỞNG NHÓM trước `killpg` (truy từ manh mối của bạn)

Bạn chỉ `launcher.py:720` và `:739`. Truy ra lỗ THẬT:

`os.killpg` nhận **process group id**, `_giet_cay` cầm **pid**. Hai số chỉ bằng nhau khi
tiến trình là trưởng nhóm — giả định `start_new_session` tạo ra nhưng **không ai kiểm tại
chỗ giết**. Đo được: con sinh không kèm `start_new_session` có pid=26072 pgid=26071, mà
`_giet_cay` vẫn gọi `killpg(26072)` — nhắm vào nhóm **không phải** của mục tiêu.

Máy thường pid lớn nên nhóm đó hầu như không tồn tại (lỗi tan thành `ProcessLookupError`),
nên lỗ sống lâu. Trong PID namespace pid chạy từ 1 ⇒ dễ trúng nhóm CÓ THẬT, kể cả nhóm 1
của vỏ shell.

Vá: `getpgid(pid) != pid` ⇒ từ chối, không gọi `killpg`. Không đo được thì đi tiếp.

## Việc của lượt này

1. **Chốt trưởng nhóm có đúng và có đủ không?** Còn đường nào tới `killpg` mà không qua
   chốt? `_giet_windows` và `_giet_rieng` thì sao? Có ca hợp lệ nào bị **từ chối oan**
   (tiến trình vừa chết, pid tái dùng giữa lúc đo, race giữa `getpgid` và `killpg`)?
2. **Nó có làm chốt giết thôi hoạt động không** — tức mua sự an toàn bằng cách không giết
   được gì nữa? Các ca giết-cây có còn đo đúng thứ chúng khai không?
3. **Bản khai môi trường**: còn khoá nào cần mà thiếu? Có khoá nào **rò thông tin nhạy
   cảm** không (đường dẫn, tên máy, biến)? `_do_an_toan` nuốt `BaseException` — có nuốt
   nhầm `KeyboardInterrupt`/`SystemExit` theo cách gây hại không?
4. **Giờ hai bên đã so được**: chạy `--dot-bien` **hai lần** và **dán bản khai môi trường
   của bạn** vào verdict. Nếu số vẫn lệch, bản khai sẽ nói vì sao — đó là mục đích của nó.
5. `setsid` ở `fe895a0` **giữ nguyên** trong lượt này (gỡ một chốt lúc chưa ai review chốt
   kia là đổi hai biến một lúc). Nếu bạn cho rằng chốt trưởng nhóm khiến `setsid` thành
   thừa — hoặc thành có hại — **nói thẳng**, đó là finding có giá trị.

## CẢNH BÁO AN NINH

Không in **giá trị** biến môi trường. Phản chứng đụng credential chạy trên
`HOME=$(mktemp -d)`; không đụng `~/.codex/auth.json` thật.

## Verdict

`approve` · `changes_requested` · `blocked`. Bằng chứng **neo SHA bất biến**. Nói thẳng
chỗ không chạy được. `approve` hợp lệ nếu thật sự không tìm ra gì.

Ghi verdict RA TỆP:

```
ops/reviews/moi-truong-review-5-codex-verdict.md
ops/reviews/moi-truong-review-5-codex-verdict.receipt.yaml
```

Xuất thẳng `stdout` ra tệp, báo `sha256` + số byte.
