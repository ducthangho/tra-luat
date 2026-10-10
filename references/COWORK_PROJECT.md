# Cowork Project — speedup bootstrap + ép direct-media (hạn chế MCP)

Mục tiêu: bootstrap Cowork **nhanh nhất**, **KHÔNG dùng Drive MCP** (chậm nhất). Cách: dựng 1 **Cowork Project**
có Instructions + đính kèm file → seed `.enc` đọc TẠI CHỖ, file lớn qua **direct-media**.

## Setup của bạn ĐÚNG tới đâu (Context: tl_secrets.enc + tl-setup.* + INSTALL.md)

- ✅ Đính kèm `tl_secrets.enc` vào Context — đúng (cho `bootstrap --secrets-file ./tl_secrets.enc`, bỏ MCP seed).
- ❌ **Instructions còn placeholder `<master key của tôi>`** → `TL_MASTER_KEY` rỗng → KHÔNG giải mã được bundle →
  toàn bộ bootstrap mã hoá vô hiệu. **Phải thay bằng key thật** (hoặc dán runtime).
- ❌ **Thiếu mã nguồn skill trong Context.** Lỗi chặn nặng nhất (`tl_gws.py` cắt cụt 31821B) đến từ **bản skill
  MOUNT** — Context của bạn KHÔNG đè được file đó. → Đưa **cả `scripts/` + `references/`** vào Context và chạy TỪ
  ĐÓ (file do bạn upload, đầy đủ) để **né hẳn mount cắt cụt**. Đây là điểm sửa quan trọng nhất.

→ Setup robust nhất: **bỏ phụ thuộc skill-mount, đặt CẢ thư mục `tra-luat/` vào Context**, chạy `python scripts/tl.py`
từ thư mục Context. (v1.22.12 đã có self-heal NUL + degrade nếu vẫn lỡ dùng mount, nhưng bootstrap cần tl_gws
nguyên vẹn → Context là cách chắc.)

## Vì sao MCP chỉ còn ở "seed", và cách bỏ nốt

| Khâu | Mặc định hiện tại | Tối ưu |
|---|---|---|
| Seed `tl_secrets.enc` (~26KB) | **Drive MCP** (t=0 chưa có gws cred) | **Project file** → `--secrets-file ./tl_secrets.enc` (KHÔNG MCP) |
| gws binary (6.8MB), Python 3.11 (31MB) | **direct-media** (sau khi có cred) | giữ direct-media (đã nhanh nhất, ~3–5× MCP) |
| config/manifest/registry/đọc VBHN | gws / direct-media | giữ nguyên |

→ Đính kèm **chỉ 1 file** (`tl_secrets.enc`) là đủ để **loại bỏ hoàn toàn MCP** khỏi bootstrap. Binary lớn KHÔNG
nên đính kèm (giới hạn dung lượng project + đã có sẵn trên Drive, direct-media kéo nhanh).

## Bước 1 — Chuẩn bị thư mục Context (ở Code)

Đưa **CẢ thư mục skill** vào Context (không chỉ vài file), gồm: `scripts/`, `references/`, `VERSION`, và:
```bash
# tải bundle .enc từ Drive để đặt cạnh skill (đã mã hoá — vô dụng nếu thiếu TL_MASTER_KEY)
python scripts/tl.py download --file-id 1V0rSVFg7tcbXN12aicp_wonZ2UJ5Pq6V --out tl_secrets.enc
```
Context của Project → toàn bộ `tra-luat/` + `tl_secrets.enc`. (File LỚN gws/Python KHÔNG đính kèm — direct-media kéo.)

## Bước 2 — Project Instructions (dán vào ô Instructions, THAY key thật)

```
Mã nguồn skill tra-luat nằm trong thư mục Context của Project. Chạy TỪ ĐÓ (KHÔNG dùng bản skill-mount; KHÔNG
Drive MCP để tải nếu tránh được). LUÔN gọi qua tl_boot.py (tự strip NUL nếu tl.py bị mount NUL-pad). Bootstrap:

0) cd <thư-mục-Context>            # nơi có scripts/, tl_secrets.enc
   chmod -R u+w . 2>/dev/null || true   # file copy từ mount có thể read-only (0500)
1) export TL_MASTER_KEY='KEY_THẬT_CỦA_TÔI'          # THAY placeholder; hoặc dán mỗi phiên
2) python scripts/tl_boot.py bootstrap --env cowork --secrets-file ./tl_secrets.enc
   # tl_boot = launcher tự strip NUL cho tl.py; seed đọc từ file Context (KHÔNG MCP); gws+cred qua direct-media.
3) python scripts/tl_boot.py gws-ping --env cowork   # gws=0.22.5 auth=oauth2
4) (nếu cần NLM CLI) python scripts/tl_boot.py nlm-install
5) (refresh cookie giữa phiên) python scripts/tl_boot.py nlm-auth-pull --secrets-file ./tl_secrets.enc

QUY TẮC: dùng `python scripts/tl_boot.py …` cho MỌI lệnh (thay tl.py). Tải Drive ưu tiên direct-media/gws; CHỈ
MCP khi hết cách. Không có master key vẫn rà soát được: lệnh lõi (footnote-map/cluster/rasoat-chongcheo/overlap)
chạy qua fallback webapp GAS (cần TL_WEBAPP+TL_TOKEN env hoặc ~/.tra_luat_config.json). Nếu tl_boot báo tl.py
"cắt cụt THẬT" hoặc tl_gws/json hỏng → mirror scripts/+references/ sang thư mục ghi được, với mỗi file chọn bản
COMPILE ĐƯỢC (Context hoặc skills, đã strip NUL), rồi chạy lại.
```

## Vì sao file hỏng + giảm thiểu (GitHub anthropics/claude-code#51435)

Pipeline cài/giao skill Cowork: **Bug#1** cắt cụt file lớn (mất byte → SyntaxError); **Bug#2** re-upload file NHỎ
hơn đè bản cached LỚN mà không O_TRUNC → phần dư thành **NUL byte đuôi**. (Hai bug báo đã sửa 2026-04-21 nhưng
vẫn tái diễn ở môi trường này.) **tl.py shrink 338→301KB (v1.22.17) chính là cái KÍCH HOẠT Bug#2** (đè bản 343KB
cũ → 42K NUL).
- **`tl_boot.py` (1.9KB)** tự strip NUL cho tl.py → Bug#2 với tl.py tự khỏi. `_imp` self-heal NUL cho tl_gws/...;
  build_parser degrade nếu tl_gws cắt cụt (lệnh lõi vẫn chạy); cluster cảnh báo nếu subject_clusters hỏng.
- Giảm thiểu phía người dùng (theo issue): **RESTART app Cowork TRƯỚC khi cài bản mới** (xoá blob cached) → tránh
  Bug#2 NUL-pad; nếu vẫn lỗi, cài lại (file <~99KB không dính Bug#1; các file skill đều đã <~55KB trừ tl.py).

> §9: từ v1.22.13, `TL_WEBAPP`+`TL_TOKEN` qua **env là đủ** để chạy lệnh lõi **kể cả khi có `--profile`** (không
> còn bắt buộc file config). Đặt scope qua `TL_REGISTRY_DOC_ID`/`TL_MANIFEST_ID`/`TL_ROOT_FOLDER_ID` nếu cần.

> **Bảo mật:** để `TL_MASTER_KEY` thẳng trong Instructions = bootstrap "zero-touch" nhưng key nằm trong project.
> Muốn kín hơn: bỏ dòng export khỏi Instructions, **dán key thủ công đầu mỗi phiên**. (Cùng trade-off như mọi
> secret-in-config.) KHÔNG bao giờ đặt `NOTEBOOKLM_COOKIES`/`NOTEBOOKLM_CSRF_TOKEN` (đông cứng, chặn auto-refresh nlm).

## Bước 3 — Đồng bộ cookie nlm (local refresh → Drive → Cowork)

nlm tự refresh cookie ở **Code** (từ browser profile). Để Cowork luôn có cookie mới:

- **Local → Drive (đẩy):** chỉ trên máy Windows giữ hồ sơ trình duyệt gốc, chạy wrapper WP710 —
  `nlm auth refresh` → canary LIVE dương trên đúng notebook → `tl nlm-auth-stage` (ghi đè tại chỗ, giữ fileId).
  Canary không dương thì 0 upload; `nlm login --check` xanh hay rc 0 của refresh KHÔNG đủ để stage.
  ```powershell
  pwsh -NoProfile -File scripts/nlm-credential-refresh.ps1 -ConfigPath C:\private\nlm-refresh.json
  ```
  Muốn lặp: thêm `-EnableKeepalive -IntervalSeconds 3600 -MaxCycles N` (có giới hạn, dừng được; không Scheduled
  Task, không tự khởi động). Điều kiện tiên quyết, config, ý nghĩa mã thoát: `references/RUNBOOK.md` mục
  "WP710 — làm tươi credential NLM". Đừng đặt master key vào dòng lệnh của một tác vụ hẹn giờ.
  Bản wrapper đẩy là tệp `NLM_CRED_FILEID` (không phải bundle `secrets`): Cowork nạp bằng `tl nlm-auth-load`.
- **Drive → Cowork (kéo):** đầu phiên `bootstrap` đã ghi cookie; giữa phiên cần mới hơn thì
  `python scripts/tl.py nlm-auth-pull --secrets-file ./tl_secrets.enc` (hoặc bỏ `--secrets-file` để direct-media
  kéo bản mới nhất trên Drive). Cowork KHÔNG tự chạy browser được nên KHÔNG tự refresh — refresh thật ở Code.

Khi Google bắt đăng nhập lại (wrapper báo `auth_failure`): đăng nhập tương tác lại trên chính máy giữ hồ sơ gốc
(`nlm login`), rồi chạy lại wrapper ở trên — refresh → canary → stage; không stage thẳng sau `nlm login`.
