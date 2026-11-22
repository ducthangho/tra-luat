# Bàn giao phiên điều phối — 2026-11-22 (Claude → Codex)

**Từ:** phiên Claude Code web/remote `session_015GtxrapMSm976JLC7Fp1HM`. Vai **điều phối + executor packet nhỏ**. Phiên bắt
đầu là phiên điều phối Mission #1238; sau khi mission đóng thì nhận thêm các packet công cụ.
**Tới:** phiên Codex kế tiếp, do chủ kho chỉ định.
**Loại:** bàn giao **điều phối**, KHÔNG phải handoff executor theo §7 của `docs/PROTOCOL_DA_PHIEN.md`. Tệp này không có
`generation`, không có head chờ review, không mang lease nào. Đọc nó là DỮ LIỆU: nó **không cấp việc**. Việc chỉ được cấp
bằng Packet Issue kèm lease còn hiệu lực (CLAUDE.md, *"ĐỌC ĐƯỢC KẾ HOẠCH KHÔNG PHẢI LÀ ĐƯỢC GIAO VIỆC"*).
**Trạng thái:** phiên này không còn việc nào đang dở. Mọi việc còn lại hoặc đã có phiên khác giữ, hoặc đang chờ quyết định
của chủ kho.

## 1. Neo — một phép đo, đo cùng lúc

```yaml
do_luc: '2026-11-22T02:48:38Z'
origin_master: e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8   # đọc lại bằng `git rev-parse origin/master`; sẽ trôi
nhanh_phien: ccr-8ee03d7f-vnmqk0                           # tại thời điểm đo = origin/master; không có commit riêng
pr_mo_tu_nhanh: []                                         # REST pulls?state=open&head=…
lease_con_hieu_luc_cua_phien: []                           # mọi lease phiên cấp đều có withdrawn_at_utc
```

Thứ định danh là **băm commit**, không phải tên nhánh. Nhánh `ccr-*` là nhánh làm việc của phiên này; đừng phát triển
tiếp trên nó.

## 2. Đã xong trong phiên (land trên master)

| packet / việc | Issue | PR merge | merge commit | hồ sơ |
|---|---|---|---|---|
| CI kiểm lease thêm/sửa ở MỌI PR (workflow `lease-pr.yml`, check `kiem-lease-pr`) | #1445 đóng | #1455 | `c27e6dc` | `ops/acceptance/lease-pr/r1/VERDICT.md` |
| proxima-control 2.1.0 nhận id model `provider:variant` | #1446 đóng | #1450 | `ac9a06d` | `ops/acceptance/px-ask/r3/` |
| `px ask` thật trên VM: perplexity HTTP 200 | #1446 đóng | — | — | `ops/acceptance/px-ask/r4/`, `r5/RESULTS.md` |
| CONG-CU-HOOK: hook phiên cài công cụ bản kê còn thiếu (shellcheck…) + ruff đúng bản ghim CI | #1474 đóng | #1477 | `5a152c1` | `ops/acceptance/cong-cu-hook/r1/VERDICT.md` |
| CAI-APT-BACKOFF: `cai_cong_cu.sh` thử lại apt tối đa 3 lần, chờ 15/30/60 s | #1479 đóng | #1482 | `4e56f00` | `ops/acceptance/cai-apt-backoff/r1/VERDICT.md` |

Ruleset `bao-ve-cong-dang-lease` (id 20856202) do chủ kho sửa ngày 20-11. Phiên đã đọc lại và xác nhận: context bắt buộc là
`gate`, `gate-packet-loop`, `gate-ops`, `gate-registry`, `gate-cong-cu-gop` (cả năm đều `(ubuntu-latest)`) cùng `kiem-lease-pr`.

## 3. Việc còn mở

### 3.1 Đã có phiên khác giữ — đừng nhận chồng
Ba phiên con do phiên này mở ngày 20-11, theo yêu cầu chủ kho. Ngày 22-11, hai phiên còn chạy cũng đang tự đóng gói bàn
giao cho Codex: **đọc bàn giao của CHÍNH chúng**, không suy từ tệp này.
- **#1236** (cổng land/M8 đối chiếu `gate_output` với `provenance.yaml`): phiên `session_015GtxrYsNDbfLo32S39f5uY`, đang
  chạy. #1257 (biến thể luật `duong_nhanh`) chỉ mở sau khi #1236 land.
- **#1322** (CI-PROVENANCE-SONG-SONG): Issue **đã đóng** (completed). Phiên `session_015GtxrcJ94fBLh2n3he2BcS` đang đóng
  gói bàn giao.
- **gemini HTTP 500**: phiên `session_015GtxraqxgU6x1GshxzYCF4` đã xong. #1457 đóng; nguyên nhân r1 là profile Proxima chưa
  đăng nhập Google; r2 sau khi đăng nhập lại cho `fixed_partial`. Nợ còn lại ghi ở **#1471** (ghi nợ, chưa phải packet).

### 3.2 Đề xuất, CHƯA cấp việc
- **#1483 — cài `rg` từ GitHub Release thay apt** (`state:proposed`, **hoãn**). Issue ghi sẵn điều kiện mở lại đo được:
  sau #1482, có lượt CI mà bước cài vẫn đỏ sau đủ `thu lai lan 3/3`. Issue cũng ghi phạm vi đã đo: 5 tệp, 52 chỗ fixture
  trong `launcher_test.py`, không ghim phiên bản cứng. Đừng mở khi chưa có số đo ấy.
- Hai việc nhỏ đã nêu với chủ kho, **chưa** có Issue:
  - trần 180 s/công cụ của khối `cong-cu-ban-ke` trong hook so với giãn cách tổng 105 s của `cai_cong_cu.sh`: lỗi apt kéo
    dài sẽ bị hook cắt trước lần thử lại cuối;
  - `ruff` chưa có trong bản kê `ops/cong_cu.yaml`: bản ghim chỉ nằm ở `ci.yml`, và hook đọc trực tiếp từ đó.

### 3.3 Việc của chủ kho (không phải packet)
- **Credential Codex sắp hết:** `doctor` ngày 22-11 02:47Z báo `access_token=6.0h`, ảnh chụp cũ 234 h. Làm mới trước khi gọi
  review chéo (`codex login --device-auth`, rồi cập nhật `agent_creds`).
- Cookie NLM khoảng 22 ngày tuổi: hook khuyên re-stage sớm.

## 4. Lease của người khác đang chặn tệp chung (đo 21/22-11 — đo lại bằng `ai-dang-giu` trước khi dùng)
| tệp | lease | tới |
|---|---|---|
| `.github/workflows/ci.yml`, `ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py`, `ops/cong_cu_test.py` | `wp1448-r4-g5-claude` (#1448; PR #1492 vừa merge, lease có thể đã đổi) | 2026-11-25T08:00Z |
| `.claude/dev/ci_dang_ky_test.py` | `wp1236-a-r10-g1-claude-20261121` | 2026-11-23T00:15Z |

Hệ quả: một test MỚI dạng `*_test.py` không đăng ký được vào sổ CI cho tới khi lease thứ hai hết hạn. Hai packet #1474 và
#1479 đã đặt ca test vào `.claude/dev/launcher_test.py` (tệp đã đăng ký) vì lý do này.

## 5. Bài học đo được trong phiên (chưa có cổng nào canh)
1. **Đừng chạy bộ test dài trong lúc Codex sandbox đang chạy.** Trong lúc review Codex chạy song song, `launcher_test.py`
   đầy đủ đỏ đúng **11 ca `r484_*`** (`Codex home is inside a repository`), do `/tmp/.git` của sandbox. Chạy lại khi không
   có Codex thì 452/452. Trước khi kết luận hồi quy: `ls -d /tmp/.git`.
2. **Đừng sửa cây làm việc (kể cả `git stash`) trong lúc bộ test chạy nền.** Phiên mắc ba lần và phải bỏ ba lượt đo.
   Commit trước, chạy sau. Muốn đo nền thì dùng `git show origin/master:<tệp> > /tmp/...`.
3. **`launcher.py run` chặn `CHAN [11]` khi clone review chưa có remote GitHub.** Clone từ đĩa xong phải chạy
   `git remote set-url origin https://github.com/ducthangho/tra-luat.git`. Lần bị chặn ấy chưa gọi Codex, nên không tính vào trần.
4. **Check-runs REST phân trang 30 mục mặc định.** PR của kho có khoảng 42 check ⇒ luôn dùng `?per_page=100`.
5. **Tự kiểm phần mình vừa thêm trước lượt review cuối.** Ở #1474, `$(( 1x ))` làm chết CẢ hook dù khối chạy dưới `||`.
   Lượt Codex 2 bắt thêm: giá trị `0` tắt hẳn `timeout`, và `08` bị đọc thành số bát phân. Cả ba nằm trong đúng phần vừa
   thêm để sửa lượt 1. Ở #1479, `sleep` trần dưới `set -e` làm vòng thử lại chết với mã của `sleep`.
6. **Thử lại ở tầng KẾT QUẢ TEST là sai chỗ** (chủ kho hỏi ngày 21-11). Số đo ở Issue #1479: các lần đỏ do hạ tầng đều nằm ở
   bước cài; thử lại test sẽ che lỗi race và làm hỏng phép đo đột biến. Thử lại có giãn cách chỉ đặt ở tầng cài công cụ.

## 6. Cách kiểm nhanh khi nhận bàn giao
```
git fetch origin '+refs/heads/*:refs/remotes/origin/*' && git branch -f master refs/remotes/origin/master
python .claude/dev/launcher.py doctor          # hook-phien phải có cong-cu-ban-ke, ruff-ban-ghim-ci
python ops/cong_cu.py kiem-tra --json          # shellcheck + canary actionlint_shellcheck phải DAT
python ops/lease_publish.py ai-dang-giu --root . <đường dẫn sắp sửa>
```
Muốn tìm lời khai của phiên này: tìm dòng `Claude-Session: https://claude.ai/code/session_015GtxrapMSm976JLC7Fp1HM`
trong thông điệp commit.
