# Hướng dẫn dùng dev-tooling (thiết lập 2026-07-02)

> Tham chiếu nhanh cho các gói vừa cài: git, gh, clasp/gas-deploy, ruff, pyright, hypothesis, gas-fakes, ccusage,
> claude-code-log. Chạy từ `D:\Quốc hội\tra-luat\` trừ khi ghi khác.
> Best-practice Claude Code: đọc `./claude-code-best-practice/best-practice/` (kho clone dev-only trên máy canonical, `git pull` cập nhật — KHÔNG có trong bundle) TRƯỚC kiến thức huấn luyện.

---

## 1. Git — lịch sử & diff thay vì so tay với zip

Repo đã init tại `D:\Quốc hội\tra-luat` (5+ commit). Từ nay **mỗi lần sửa xong 1 việc, commit ngay** — thay
thói quen cũ "so file với zip release để phát hiện rogue-edit".

```powershell
cd "D:\Quốc hội\tra-luat"
git status                          # xem file nào đổi
git diff scripts/tl.py              # xem CHÍNH XÁC dòng nào đổi (thay vì đoán)
git add -A
git commit -m "mô tả ngắn"          # LUÔN kiểm `git status` trước — tránh lặp lỗi node_modules
git log --oneline -10                # lịch sử gần đây
```

**Bẫy đã gặp:** `npm install` trong bất kỳ thư mục con nào (vd `gas-project/`) tạo `node_modules/` — PHẢI có dòng
`node_modules/` trong `.gitignore` (đã thêm) TRƯỚC khi `git add -A`, nếu không sẽ track hàng nghìn file rác.

**Revert 1 file về commit trước** (thay thao tác tay copy từ zip cũ):
```powershell
git checkout HEAD~1 -- scripts/tl.py   # hoặc git log để chọn đúng commit
```

---

## 2. `gh` CLI — GitHub (khi cần, repo hiện chưa có remote)

```powershell
gh auth login                       # 1 lần, chọn HTTPS + browser
gh repo create tra-luat --private --source=. --remote=origin   # nếu muốn đẩy lên GitHub riêng tư
git push -u origin master
```
Chưa bắt buộc — repo local đã đủ giá trị (diff/undo). Chỉ cần khi muốn backup ngoài máy hoặc cộng tác.

---

## 3. `clasp` + `gas-deploy.ps1` — Apps Script KHÔNG cần mở browser editor

**Vòng lặp sửa Code.gs:**
```powershell
cd "D:\Quốc hội\tra-luat"
# 1) Sửa code — mở gas-project\Code.gs bằng Claude Code / editor bất kỳ
# 2) Xem trước sẽ đổi gì (KHÔNG động tới production)
.\gas-deploy.ps1 -Message "test" -DryRun

# 3) Deploy thật (push + version + cập nhật deployment production, GIỮ /exec URL)
.\gas-deploy.ps1 -Message "mô tả thay đổi vừa sửa"
```
Sau khi deploy thành công, script **tự đồng bộ ngược** `gas-project/Code.gs` → `references/Code.2.21.2i.gs` — tài
liệu tham chiếu không bao giờ trôi khỏi live nữa (bài học từ vụ `PENDING_EFFECT` viết sẵn nhưng quên deploy).

**Lệnh clasp hữu ích khác:**
```powershell
cd gas-project
clasp pull                # kéo bản LIVE về (nếu ai đó sửa qua browser — hiếm khi cần)
clasp open-script         # mở editor trên browser (chỉ để xem, không nên sửa ở đó nữa)
clasp logs                # xem log Stackdriver của webapp (debug lỗi runtime)
clasp deployments          # liệt kê mọi deployment (đối chiếu deploymentId production)
```

**Test Code.gs OFFLINE trước khi deploy** (dùng `gas-fakes`, tránh lặp bug kiểu "empty string bị webapp nuốt"
mà lẽ ra bắt được không cần chạm production):
```javascript
// gas-project/test-example.mjs (viết khi cần test 1 hàm cụ thể, KHÔNG bắt buộc mỗi lần)
import '@mcpher/gas-fakes/main.js'
// SpreadsheetApp/DriveApp giờ chạy giả lập trên Node — gọi thẳng hàm trong Code.gs để kiểm logic
```
`gas-fakes` đã cài trong `gas-project/node_modules/` (không bị track vào git — đúng thiết kế).

---

## 4. `ruff` — lint nhanh, đã bắt 1 bug thật (v1.29.5)

```powershell
$RUFF = "$env:APPDATA\Python\Python313\Scripts\ruff.exe"
cd "D:\Quốc hội\tra-luat\scripts"
& $RUFF check tl.py --statistics          # tổng quan theo loại lỗi
& $RUFF check tl.py --select F821,F841    # CHỈ bug thật (undefined-name, unused-var) — bỏ qua style E701/E702
& $RUFF check tl.py --select F821,F841 --fix   # tự sửa (an toàn, chỉ 2 loại này)
```
**Đừng chạy `ruff check --fix` không giới hạn `--select`** — codebase cố ý dùng `if x: y; z` (E701/E702) làm
style nén, không phải lỗi. Luôn thu hẹp về `F8xx` (lỗi logic thật: undefined-name, unused-var, import thừa) khi
muốn auto-fix; các rule khác chỉ xem báo cáo, tự quyết định.

**Thêm vào quy trình:** chạy `ruff check --select F821,F841` mỗi khi sửa xong 1 khối lớn trong `tl.py`, TRƯỚC
`--selftest` — rẻ hơn nhiều (mili-giây) và bắt được lớp lỗi selftest không phủ tới (dead code, biến quên dùng).

---

## 5. `pyright` — gõ kiểu dần dần (chưa bắt buộc, dùng khi cần rõ nghĩa 1 hàm)

```powershell
$PYRIGHT = "$env:APPDATA\Python\Python313\Scripts\pyright.exe"
cd "D:\Quốc hội\tra-luat\scripts"
& $PYRIGHT tl.py --outputjson | Select-String '"severity": "error"'   # chỉ lỗi thật, bỏ warning
```
13k dòng không có annotation — KHÔNG kỳ vọng full-typed. Dùng khi debug 1 hàm cụ thể: thêm type hint tạm thời
vào tham số/return của hàm đang sửa, `pyright` báo ngay nếu truyền sai kiểu (vd `dict` vs `list`).

---

## 6. `hypothesis` — property-based test cho hàm PURE

Dùng khi thêm/sửa 1 hàm chuẩn hoá/parse (norm_sohieu, `_key_fam`, dedup...) — thay vì nghĩ tay từng edge-case,
để hypothesis tự sinh + shrink về case nhỏ nhất gây fail. Thêm **cục bộ trong `tl_selftest.py`** (không tách
file riêng — giữ nguyên style embedded hiện có):

```python
from hypothesis import given, strategies as st

@given(st.text(alphabet="0123456789/ABCDEFGHIJKLMNOPQRSTUVWXYZ-", min_size=1, max_size=30))
def _prop_norm_sohieu_idempotent(s):
    assert norm_sohieu(norm_sohieu(s)) == norm_sohieu(s)   # áp norm 2 lần = 1 lần

# gọi trong selftest run():
try:
    _prop_norm_sohieu_idempotent()
    cases.append(("prop_norm_sohieu_idempotent", True))
except Exception as e:
    cases.append(("prop_norm_sohieu_idempotent", False))
```
Ứng viên tốt nhất để thử trước: `norm_sohieu`, `_ingest_dedup_title_key`, `_key_fam` (detector #5) — đều PURE,
đều có invariant rõ (idempotent, hoặc round-trip).

---

## 7. `ccusage` / `claude-code-log` — quan sát phiên làm việc

```powershell
npx ccusage                    # tổng token/chi phí các phiên Claude Code gần đây (đọc local, không upload)
npx ccusage daily              # theo ngày
npx ccusage --json > usage.json   # xuất máy-đọc-được

claude-code-log --help
claude-code-log <path-tới-1-session.jsonl> -o session.html   # session hiện tại thành HTML đọc được
claude-code-log ~/.claude/projects/<project>/ -o all.html    # cả project thành 1 file
```
Dùng `claude-code-log` khi cần **trích session dài thành tài liệu bàn giao** (thay thói quen tự viết
HANDOFF.md thủ công từ đầu — giờ có thể trích + biên tập lại).

---

## 8. Quy trình khuyến nghị mỗi phiên sửa `tl.py`

```
1. Sửa code
2. ruff check tl.py --select F821,F841        (mili-giây — bắt lỗi rẻ trước)
3. python tl.py --selftest                     (đầy đủ — 372+ case)
4. python tl.py verify-integrity
5. git add -A && git commit -m "..."
6. (nếu đụng Code.gs) .\gas-deploy.ps1 -Message "..." -DryRun  →  bỏ -DryRun khi chắc
7. (khi release) .\upload-skill-to-Package.ps1  (xem §9)
```

## 9. Quy trình vận hành đóng gói sẵn (scripts tại `D:\Quốc hội\`, v1.29.7)

Ba script cho các quy trình hay lặp (từ log sự cố NĐ131 — #6/#7/#8/#9):

| Script | Quy trình | Dùng khi |
|---|---|---|
| **`fix-row-kind.ps1`** | Rà + sửa dòng bị gán nhầm `row_kind=overflow` trong 1 profile (bug ingest-local <v1.29.7) | Sau khi phát hiện dòng profile-own mang overflow: `.\fix-row-kind.ps1 -Profile "X"` (DRY) → `-Apply` (mỗi dòng qua `register --row-kind own`, journaled + undo được) |
| **`new-profile.ps1`** | ĐĂNG KÝ profile đã có hạ tầng sẵn (4 ID từ SKILL_OF_RECORD) vào config — hết thêm block JSON tay | Profile như "Pháp lệnh NCC" có notebookId/folder/registry/manifest nhưng thiếu trong config: `.\new-profile.ps1 -Name "..." -NotebookId ... -RootFolderId ... -RegistryDocId ...` — CHẶN registry rỗng/Doc-legacy; ghi journaled + verify bằng profile-info |
| **`preflight-ingest.ps1`** | Nghiệm hạ tầng (`tl up --nlm`) TRƯỚC rồi mới `ingest-local` — không gãy ở bước cuối | Mọi lần nạp văn bản mới: `.\preflight-ingest.ps1 -Profile "X" -File "...docx" --sohieu "..." --cat NN --apply` (args sau -File chuyển thẳng cho ingest-local) |

Lưu ý liên quan (đã vá trong skill v1.29.7 — script là lớp tiện dụng bên ngoài):
- `ingest-local` nay TỰ pre-check NLM trước upload (tắt: `--skip-nlm-preflight`) + read-back/backfill `--sohieu` sau organize.
- `register --row-kind own|overflow|ref` là đường sửa row_kind chính thức.
- `extract` tự dùng cache consolidated của `cache-build` (hết cap 200k); resolver ưu tiên chính văn hơn phụ lục `PL_`.
- `nlm-reconcile` tự refresh manifest khi thấy `unregistered` (nguồn vừa nlm-add hết bị báo oan).

## 10. Build + upload skill lên Package

Script `D:\Quốc hội\upload-skill-to-Package.ps1` (đã có sẵn từ trước, vừa sửa đường dẫn xuất zip):

```powershell
cd "D:\Quốc hội"
.\upload-skill-to-Package.ps1                 # selftest + integrity + zip + push lên Drive/Package
.\upload-skill-to-Package.ps1 -NoPush         # chỉ build + zip, KHÔNG đẩy Drive (test an toàn)
.\upload-skill-to-Package.ps1 -NoTest         # bỏ selftest (nhanh hơn, chỉ khi vừa chạy selftest riêng)
```
**Cần `gws auth login` xong trên máy chạy lệnh này** (quyền GHI Drive) — mới `drive-push` được. Zip xuất ra
`D:\Quốc hội\tra-luat-skill-v<VER>-gws3env.zip`. Verify sau khi push:
```powershell
curl "https://drive.usercontent.google.com/download?id=1H5kAt3SRVP7_xmLMIzcqyFtFc4VSDH0P&export=download&confirm=t" -o pkg.zip
unzip -p pkg.zip "*/VERSION"   # PHẢI khớp VERSION vừa build
```
