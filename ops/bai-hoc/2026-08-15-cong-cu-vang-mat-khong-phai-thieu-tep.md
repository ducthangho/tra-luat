# Bài học: "không có công cụ" là một KẾT LUẬN, không phải một quan sát

**Ngày đo:** 2026-08-15 · **Phiên:** wp55 r3 g5/g6 · **Người ghi:** executor `claude`

Phiên này đã kết luận sai rằng **không gọi được `codex`**, rồi báo với người dùng rằng
cross-review không chạy được. Kết luận ấy sai. Người dùng đính chính, và khi kiểm lại thì
`codex` cài được, đăng nhập được, chạy được — lượt review 7 sau đó tìm ra một P1 thật.

Ghi lại để không lặp: cả **vì sao công cụ vắng mặt**, cả **vì sao tôi kết luận sai**, và
**lệnh khôi phục đã đo được**.

---

## 1. Vì sao `codex` vắng mặt — ba nguyên nhân độc lập, tất cả đo được

Câu hỏi khởi điểm của người dùng là "tại sao `launcher.py` lại chưa có". Đo ra thì
`launcher.py` **không mất**; nó chưa bao giờ có mặt trên nhánh này.

```
nhánh packet 2cccf1e — .claude/dev/launcher.py        : KHÔNG
nhánh packet 2cccf1e — .claude/hooks/session-start.sh : KHÔNG
base fbe5ab9e        — .claude/dev/launcher.py        : KHÔNG
master               — .claude/dev/launcher.py        : CÓ

launcher.py vào master : 13935ec  2026-08-12
hook vào master        : 63627cb  2026-08-12
base fbe5ab9e ngày     : 2026-08-11
base là tổ tiên master : CÓ · master đi trước 86 commit
```

**(a) Nhánh packet ghim `base_sha` CŨ HƠN công cụ.** `base_sha` của wp55 là `fbe5ab9e`
(11-08), còn `launcher.py` và hook vào master ngày 12-08. Cây làm việc của packet vì thế
không mang công cụ nào của kho — đúng theo thiết kế, không phải hỏng hóc. Cây ĐÃ MERGE thì
có đủ (đo: 80628 byte, `doctor` báo `DU CONG CU BAT BUOC`).

**(b) `.claude/settings.json` trên nhánh packet KHÔNG đăng ký `SessionStart`.** Bản trên
nhánh chỉ có `PreToolUse`; bản master mới có `SessionStart`. Nên kể cả khi hook tồn tại,
nó cũng không được gọi.

**(c) Kho được gắn GIỮA phiên.** Thư mục làm việc lúc phiên khởi động là `/home/user`
(rỗng); kho về `/workspace/tra-luat` sau đó bằng `add_repo`. Lúc `SessionStart` chạy thì
chưa có kho nào để đọc `settings.json`. Nguyên nhân này áp cho MỌI nhánh, kể cả master.

Ba nguyên nhân chồng lên nhau, và mỗi cái một mình đã đủ. Không cái nào là "thiếu tệp".

## 2. Vì sao tôi kết luận sai — chỗ này quan trọng hơn chỗ trên

Tôi suy từ **tài liệu** (`docs/GOI_AGENT_DA_NEN.md` ghi "container đã đo 12-08: không có
codex") và từ **`ListAgents`** (không liệt kê codex), rồi kết luận "môi trường chặn".
Tôi **chưa từng chạy `command -v codex`** trước khi báo là không gọi được.

Quan sát thật chỉ có thể là một trong hai:

```bash
command -v codex        # rỗng hay không?
codex login status      # "Logged in using ChatGPT" hay "Not logged in"?
```

Từ một quan sát rỗng, có **ba** kết luận khả dĩ, và chúng đòi ba hành động khác hẳn nhau:

| quan sát | kết luận SAI hay gặp | ba khả năng thật |
|---|---|---|
| `command -v codex` rỗng | "môi trường này không có codex" | (a) môi trường thật sự không có · (b) hook chưa chạy · (c) nhánh đang checkout không mang hook |

**Chốt:** không được báo "không gọi được X" khi chưa phân biệt xong ba khả năng đó. Tài
liệu mô tả một lần đo trong quá khứ, trên một cây khác, ở một ngày khác — nó không phải
quan sát về phiên đang chạy.

## 3. Lệnh khôi phục — đã chạy thật, không phải đề xuất

Chạy được từ **bất kỳ nhánh nào**, kể cả nhánh packet không mang công cụ:

```bash
D="$(mktemp -d)"
git show origin/master:.claude/hooks/session-start.sh > "$D/session-start.sh"
git show origin/master:.claude/dev/launcher.py        > "$D/launcher.py"
python3 "$D/launcher.py" doctor          # BẰNG CHỨNG DƯƠNG, lấy từ master
```

Đo được trên nhánh packet `2cccf1e`:

```
co    git      git version 2.43.0        co    codex    codex-cli 0.147.0
co    python   Python 3.11.15            co    rg       ripgrep 14.1.0
co    claude   2.1.233                   co    npm/node 10.9.7 / v22.22.2
KET LUAN  : DU CONG CU BAT BUOC          rc=0
```

Nếu thiếu thật thì dựng tay, đúng thứ tự hook làm:

```bash
npm install -g @openai/codex          # đo: 0.147.0
codex login status </dev/null         # CODEX_AUTH_JSON đã được hook khôi phục?
codex login --device-auth             # nếu chưa: link + mã 15 phút
```

## 4. Bốn cái bẫy đã trả giá trong lượt này

**4.1 — Chạy hook bằng tay LÀM HỎNG môi trường đang tốt.** Hook chạy
`pip install -r requirements.txt`; lần chạy tay đó nâng `cffi` lên 2.1.1 và làm
`cryptography` 41.0.7 (bản Debian) panic:

```
pyo3_runtime.PanicException: Python API call failed
tl.py --selftest  rc=1     (trước đó 1696/1696)
```

Hậu quả lan sang reviewer: codex cũng vấp đúng panic ấy và **không xác nhận được**
`1696/1696`, phải ghi `not_confirmed` trong verdict. Sửa được, nhưng đáng lẽ không nên xảy
ra. **Đừng chạy cả hook chỉ để lấy một công cụ** — lấy đúng thứ cần
(`git show origin/master:...`), đừng chạy phần `pip`.

**4.2 — Hook báo sai nguyên nhân.** Chạy hook (lấy từ master) trên cây packet thì:

```
[session-start] codex auth: Logged in using ChatGPT
python3: can't open file '.../.claude/dev/launcher.py': No such file or directory
[session-start] THIEU CONG CU BAT BUOC — xem bang tren     rc=1
```

Đủ công cụ, nhưng thông điệp nói **thiếu công cụ bắt buộc**. Đây là âm tính giả trỏ người
đọc đúng vào kết luận sai. Bản vá đề xuất ở §5.

**4.3 — In biến bí mật ra transcript.** Lệnh chẩn đoán của tôi in nguyên
`CODEX_AUTH_JSON` (5648 ký tự base64) — chứa `refresh_token`, `access_token`, `id_token`
còn sống. Chốt số 1 trong chính hook ghi *"KHÔNG in giá trị, và KHÔNG truyền qua đối số
dòng lệnh"*, và tôi vi phạm đúng chốt ấy khi đi tìm hiểu vì sao hook không chạy.
**Kiểm sự TỒN TẠI, đừng in NỘI DUNG:**

```bash
echo "CODEX_AUTH_JSON: ${CODEX_AUTH_JSON:+có, ${#CODEX_AUTH_JSON} ký tự}${CODEX_AUTH_JSON:-chưa đặt}"
```

Sai chỗ này thì phải **thu hồi và cấp lại**, không có cách vá nào khác.

**4.4 — `codex exec` cần đúng sandbox và tránh vài lệnh.** `-s read-only` chặn ghi tệp
tạm nên reviewer không chạy nổi bộ test; dùng worktree riêng + `-s workspace-write`.
Sandbox cũng **từ chối `rm -rf`** (`rejected: rm -f style commands are not permitted`) —
prompt cho reviewer nên dùng thư mục có hậu tố SHA thay vì dọn bằng `rm -rf`. Và `codex`
đọc stdin, nên luôn `</dev/null`.

## 5. Bản vá đề xuất cho hook — `docs/GOI_AGENT_DA_NEN.md` và hook nằm NGOÀI write_set

`write_set` của wp55 gồm đúng 6 tệp; `.claude/hooks/session-start.sh` và
`docs/GOI_AGENT_DA_NEN.md` không nằm trong đó, và ranh giới packet ghi rõ *"phát hiện
ngoài spec ⇒ xuất successor rồi dừng; không tự mở write set"*. Nên phần dưới là **đề
xuất đã soạn sẵn**, chưa áp.

Sửa để hook không còn báo sai nguyên nhân — lùi về bản master khi cây hiện tại không có
`launcher.py`:

```diff
 echo "[session-start] kiem cong cu:"
-"$PY" .claude/dev/launcher.py doctor || {
-  echo "[session-start] THIEU CONG CU BAT BUOC — xem bang tren"
-  exit 1
-}
+# Nhanh packet ghim base CU HON launcher.py thi cay lam viec khong co no. Do khong
+# phai "thieu cong cu" — do la "nhanh nay chua co cong cu do". Bao dung nguyen nhan,
+# va van do duoc bang ban tren master.
+DOCTOR=.claude/dev/launcher.py
+if [ ! -f "$DOCTOR" ]; then
+  DOCTOR="$(mktemp)"
+  if git show origin/master:.claude/dev/launcher.py > "$DOCTOR" 2>/dev/null; then
+    echo "[session-start] nhanh nay khong co launcher.py — dung ban tren origin/master"
+  else
+    echo "[session-start] CANH BAO: khong co launcher.py o ca nhanh lan master — bo qua doctor"
+    DOCTOR=""
+  fi
+fi
+if [ -n "$DOCTOR" ]; then
+  "$PY" "$DOCTOR" doctor || {
+    echo "[session-start] THIEU CONG CU BAT BUOC — xem bang tren"
+    exit 1
+  }
+fi
```

Và thêm vào `docs/GOI_AGENT_DA_NEN.md`, ngay sau mục *"Trước tiên: đủ công cụ chưa"*,
mục §2 và §3 của tệp này.

## 6. Điều duy nhất cần nhớ nếu quên hết phần trên

> Trước khi nói với người dùng rằng một công cụ **không gọi được**, phải chạy
> `command -v <tool>` và `<tool> login status` trong CHÍNH phiên này, và phải loại trừ
> xong khả năng **hook chưa chạy** và khả năng **nhánh đang checkout không mang hook**.
> Tài liệu và `ListAgents` không phải quan sát.
