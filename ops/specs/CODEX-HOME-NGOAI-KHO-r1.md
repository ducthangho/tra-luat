tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# Đặc tả packet — `CODEX-HOME-NGOAI-KHO` (revision 1)

| trường | giá trị |
|---|---|
| `packet_id` | `CODEX-HOME-NGOAI-KHO` |
| `packet_issue` | #1334 |
| `revision` | 1 |
| `nguon_cap_viec` | #433 (finding "keep ephemeral credential destinations outside the repository"). Vòng hỏi `soan-spec` của phiên điều phối #1206 ngày 16-11-2026 đã chốt Q1 (đây là P-D), Q5 (hành vi), Q6 (executor, reviewer); chủ kho trả lời "Đồng ý theo khuyến nghị". |
| `review_class` | `sensitive` (đường ghi credential) |
| `base` | nhánh mặc định lúc cấp lease; số đo dưới đây lấy trên `a97a1ca` |

## 0. Vấn đề (đo 16-11-2026 ~04:4xZ, cây `a97a1ca`, dữ liệu GIẢ)

Cách dựng ca đo:
- Tạo một kho git tạm, đặt `CODEX_HOME=<kho>/codexhome`.
- Thay `tl_gws._public_curl_bytes` bằng hàm trả bytes giả, và `gws_cred_store.decrypt` bằng hàm trả payload
  `{"schema":1,"rev":9,"codex_auth":{"tokens":{…GIẢ…},"last_refresh":"2099-…"}}`.
- Gán `tl_gws._imp = importlib.import_module`.

Kết quả:

```
_bootstrap_agent_creds('x'*40) -> ('ĐÃ NẠP', 'rev=9; codex auth.json → …/kho/codexhome/auth.json (0600)')
git -C <kho> status --porcelain --untracked-files=all -> ?? codexhome/auth.json
```

Credential bị ghi vào trong cây kho. Chỉ cần một lần `git add -A` là nó vào commit.

Có hai chỗ ghi, cả hai không kiểm đích:
- `scripts/tl_gws.py`: `_codex_auth_path()` cùng nhánh ghi trong `_bootstrap_agent_creds()`, hàm gọi
  `_ghi_nguyen_tu_0600(dst, …)`.
- `ops/cloud_agent_creds.py`: `_codex_dir()` cùng `_ghi_dau()`, ghi tệp dấu `.tra-luat-agent-creds-dau.json`.
  Tệp dấu không chứa token nhưng nằm cùng thư mục.

Đường phóng Codex của launcher đã có chốt này: `.claude/dev/launcher.py`, lớp `_KhoCodex`, thông điệp
`Codex home is inside a repository`. Chốt kiểm từng tổ tiên của đường dẫn, kể cả chính thư mục đích, và
coi là "trong kho" khi tổ tiên ấy có mục `.git` (lstat, không theo symlink). Đường agent_creds không đi qua
chốt này.

## 1. `write_set`

```
scripts/tl_gws.py
ops/cloud_agent_creds.py
ops/cloud_agent_creds_test.py
RELEASE_MANIFEST.json
changelog.d/wp-1334.md
```

`RELEASE_MANIFEST.json` có mặt vì `scripts/tl_gws.py` nằm trong manifest, đo 16-11 thấy 185 tệp có
`scripts/tl_gws.py`. Đổi nội dung tệp ấy thì phải tái sinh manifest (CLAUDE.md, mục *Quy ước deploy* số 5),
nếu không lane LAND trên master sẽ đỏ. `changelog.d/wp-1334.md` là fragment theo tiền lệ `wp-1009`/`wp-1038`.
`CHANGELOG.md` ở trong manifest, nên packet này **không** sửa nó, và **không** bump `VERSION`.

## 2. `ngoai_pham_vi`

- Không đổi `_KhoCodex` trong `launcher.py`: tệp này không thuộc write set, và P-B đang sửa nó.
- Không đổi định dạng, nguồn hay luật so `last_refresh` của credential.
- Không chạm `.claude/hooks/session-start.sh`. Nếu hook cần in thêm lý do, kết luận `KHÔNG ĐO ĐƯỢC` hiện có
  đã đi qua kênh in sẵn có.
- Không chạy bootstrap với bundle thật. Mọi phép đo dùng tệp giả.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| M1 | `scripts/tl_gws.py` có MỘT hàm `_trong_kho_git(path) -> str \| None`. Hàm trả đường dẫn tổ tiên có `.git` nếu đích hoặc bất kỳ tổ tiên nào của nó có mục `.git` (lstat, không theo symlink, đi từ chính đích lên tới gốc), ngược lại trả `None`. Thư mục đích chưa tồn tại thì xét từ tổ tiên gần nhất đang tồn tại. Luật khớp với `_KhoCodex`. | `scripts/tl_gws.py` |
| M2 | `_bootstrap_agent_creds`: nếu `_trong_kho_git(thư mục của auth.json)` khác `None` thì trả `("KHÔNG ĐO ĐƯỢC", "CODEX_HOME nằm trong kho git (<tổ tiên>) — không ghi auth.json")` và **không ghi tệp nào**, kể cả không tạo thư mục, không tạo tệp tạm. Chuỗi trả về không mang giá trị credential. | `scripts/tl_gws.py` |
| M3 | `cmd_agent_creds_set --codex` (đường ĐỌC auth.json để upload) không bị chặn. Chỉ đọc thì không rò ra cây kho. Ghi thẳng điều này vào docstring để người sau không "sửa" nhầm. | `scripts/tl_gws.py` |
| M4 | `ops/cloud_agent_creds.py`: `_ghi_dau` cũng không ghi khi `tl_gws._trong_kho_git(_codex_dir())` khác `None`. Phải gọi qua `tl_gws`, không định nghĩa lại (luật `p3a12_khong_dinh_nghia_lai_ten_tl_gws` trong test). | `ops/cloud_agent_creds.py` |
| M5 | Ca test, đặt trong `ops/cloud_agent_creds_test.py`, dùng đồ giả như mục 0: (a) `CODEX_HOME` trong kho ⇒ `KHÔNG ĐO ĐƯỢC`, không có `auth.json`, và `git status --porcelain --untracked-files=all` của kho tạm RỖNG; (b) `CODEX_HOME` ngoài kho ⇒ `ĐÃ NẠP`, có `auth.json` 0600 (vế dương, giữ hành vi cũ); (c) `.git` là TỆP (worktree/submodule) ở tổ tiên ⇒ vẫn bị chặn; (d) `.git` là symlink ⇒ vẫn bị chặn; (e) thư mục đích chưa tồn tại, tổ tiên trong kho ⇒ bị chặn và không tạo thư mục; (f) `_ghi_dau` trong kho ⇒ không ghi tệp dấu. | `ops/cloud_agent_creds_test.py` |
| M6 | Đăng ký đột biến cho từng chốt vào khung đột biến sẵn có của `ops/cloud_agent_creds_test.py`, theo dạng các hàng `P3…`. Đường ra của bộ test vẫn khớp regex đăng ký ở `.claude/dev/ci_dang_ky_test.py:59` (`CA: N/N dat`, `DOT BIEN: M/M bi giet dung ly do`, `TU KIEM PHAN HANG: DAT`, `TONG: DAT`). | `ops/cloud_agent_creds_test.py` |
| M7 | Tái sinh `RELEASE_MANIFEST.json`; thêm fragment `changelog.d/wp-1334.md`. | `RELEASE_MANIFEST.json`, `changelog.d/wp-1334.md` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Ca M5(a) xanh trên head, và **đỏ trên base** `a97a1ca` (vế âm: chính phép đo ở mục 0). | Đột biến: bỏ lời gọi `_trong_kho_git` trong `_bootstrap_agent_creds` ⇒ M5(a) đỏ ở khẳng định "không có auth.json", không đỏ vì lỗi vô can. |
| N2 | M5(b) xanh. | Đột biến: `_trong_kho_git` luôn trả một đường dẫn ⇒ M5(b) đỏ, vì chặn oan bản đúng. |
| N3 | M5(c), M5(d) xanh. | Đột biến: kiểm `.git` bằng `is_dir()` ⇒ (c) đỏ. Đột biến: theo symlink (`exists()` thay cho lstat) ⇒ (d) đỏ, hoặc chỉ ra vì sao không đổi màu và giữ đột biến khác chứng minh răng. |
| N4 | M5(e) xanh. | Đột biến: tạo thư mục (`makedirs`) trước khi kiểm ⇒ (e) đỏ ở khẳng định "không tạo thư mục". |
| N5 | M5(f) xanh. | Đột biến: bỏ chốt trong `_ghi_dau` ⇒ (f) đỏ. |
| N6 | Toàn bộ `python3 -B ops/cloud_agent_creds_test.py` ra `CA: N/N dat`, đột biến `M/M bi giet dung ly do`, `TONG: DAT` (hai số bằng nhau). N lấy số ca nền đo lúc cấp lease cộng ca mới. | Bất kỳ ca nào đỏ, hoặc số lệch. |
| N7 | `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ra `ok=true` và `expected == checked` (lệnh của lane LAND, CLAUDE.md mục 5). `python scripts/tl.py --selftest` ra N/N. | Quên tái sinh manifest ⇒ `ok=false`. |
| N8 | Ruff `--select F` delta 0 trên `scripts/tl_gws.py`, `ops/cloud_agent_creds.py`, `ops/cloud_agent_creds_test.py`. `doctrine-scan` và `adr-song` rc 0. | Delta lớn hơn 0 hoặc rc khác 0. |
| N9 | CI Ubuntu xanh trên head; gate hậu merge đủ bốn mốc §10.2.2. | Đọc nhãn job và log. |

Windows: **không bắt buộc**. Luật kiểm `.git` dùng `os.lstat` và `pathlib`, không gọi API riêng của nền nào.
Ca (d) dùng symlink: trên Windows thiếu quyền tạo symlink thì bộ test sẵn có trả mã 5 (bỏ qua) theo quy ước
của tệp, và khai rõ. Nếu reviewer chỉ ra một hành vi riêng của Windows mà ca không phủ, việc đó thành
finding, không tự thêm lượt Windows.

## 5. Kích thước và trần

Dự kiến 5 tệp, khoảng 30 dòng mã cộng 120–200 dòng test, cộng manifest (khoảng 2–4 dòng đổi băm) và
fragment. Trần `ADR-0053`: ≤ 6 tệp, ≤ 450 dòng thêm. Lời gọi Codex theo trần mà `ADR-0055` chọn.

## 6. `luat_dung`

- Vượt trần `ADR-0053` ⇒ dừng và nén. Muốn nâng trần thì xin chủ kho (E2), mang theo `numstat`.
- Chạm trần lời gọi Codex ⇒ theo `ADR-0055` (E2).
- Không được chạy bootstrap với bundle thật hay đọc tệp bí mật nào (CLAUDE.md, mục *Cấm*). Một phép đo
  cần dữ liệu thật thì ghi vào `chua_do_duoc`, không xin ngoại lệ.

## 7. `pham_vi_e`

Không chạm E4, không chạm E5. Packet thêm một chốt từ chối ghi, không đổi thẩm quyền hay nguồn credential.

## 8. `hinh_dang_ke_thua`

Kế thừa từ #433, nơi PR #432 và #447 đóng mà không merge vì thiết kế chuyển sang `agent_creds`. Hình dạng:
**một chốt an ninh có ở một đường (`_KhoCodex`) nhưng không có ở đường song song mới dựng sau**. Cùng họ
"PHẠM VI TUYÊN BỐ phải bằng phạm vi ĐO ĐƯỢC" (CLAUDE.md): kho từng có chốt "không ghi credential vào kho",
nhưng chỉ một trong hai cửa ghi đọc chốt ấy. Đếm hình dạng: lần thứ 1 được ghi cho cửa `agent_creds`.

## 9. `chua_do_duoc`

- Hành vi với bundle thật: không đo, vì bị cấm đọc bí mật. Ca test thay bằng đồ giả ở cùng ranh giới
  (`_public_curl_bytes`, `decrypt`).
- Biến `CODEX_HOME` trên các máy chủ kho thật đang trỏ về đâu: chưa đo. Container phiên này **không** đặt
  `CODEX_HOME` (đo 16-11), nên đích mặc định là `~/.codex`.
- Ca `/tmp/.git` rỗng do sandbox Codex để lại (CLAUDE.md, bài học 22-10): luật mới cũng coi đó là kho, và
  fail-closed như `_KhoCodex`. Nếu `CODEX_HOME` mặc định (`~/.codex`) không nằm dưới `/tmp` thì không ảnh
  hưởng. Chưa đo trên máy có `HOME` dưới một kho.
