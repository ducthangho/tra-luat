# Kế hoạch điều chỉnh — ưu tiên đa thiết bị / đa nền tảng

> **Trạng thái:** kế hoạch thi công. Không cấp authority — authority là Packet Spec,
> GitHub facts và receipt đã verify.
>
> **Nguyên tắc xếp thứ tự:** hoàn thiện năng lực **chạy được trên nhiều thiết bị và
> nhiều nền** TRƯỚC, rồi mới tới cưỡng chế quy trình. Lý do ở §1.

Nền đo: `origin/master` `47847b1`. Mọi con số dưới đây đo được, kèm cách tái lập.

---

## 1. Phát hiện quyết định thứ tự: mã đa nền tảng đã viết nhưng CHƯA TỪNG ĐƯỢC ĐO

```
grep 'Darwin' .claude/dev/launcher.py      -> >=8 nhánh mã cho macOS
grep -r 'macos' .github/workflows/         -> 0 kết quả
```

`launcher.py` sinh ra chính vì mục tiêu này — chú thích đầu tệp nói thẳng: *điện thoại và
phiên remote không có shell cục bộ, macOS/Linux không có PowerShell mặc định*. Nó có
đường riêng cho Darwin ở `_chup_cay`, `_khoa_danh_tinh`, `_thanh_vien_nhom`, và bảng gợi ý
cài đặt. **Không dòng nào trong số đó từng chạy trên một máy macOS thật.**

Đây đúng lớp bệnh kho này đã đặt tên hai lần: *đo sự CÓ MẶT thay vì đo KHẢ NĂNG*. Mã có
mặt không phải bằng chứng mã chạy.

Ba lỗ đo được nữa, cùng họ:

| lỗ | phép đo | hệ quả |
|---|---|---|
| `launcher_test.py` không chạy ở PR thường | chỉ có trong `launcher-windows.yml`, kích hoạt khi push master · gọi tay · nhãn `windows` | nền tảng đa nền là thứ **ít được gác nhất** |
| `t53_doctor_bao_du_khi_du` ĐỎ trên master | `126/128 · bỏ qua 1 · hỏng 1 · rc=1`, trên máy **đủ** công cụ | cổng công cụ tự nó không tin được |
| phiên headless không chạm được GitHub | `claude mcp get github` → `Pending approval`; nhưng POST thẳng endpoint bằng `GITHUB_PAT` → **HTTP 200, 44 công cụ** | phiên web/điện thoại tưởng bị chặn trong khi đường vẫn mở |

---

## 2. Ma trận mô hình — chọn theo VIỆC, và dùng `effort` làm cần gạt chính

Giá thật (Claude API, $/1M token):

| mô hình | input | output | ngữ cảnh | ghi chú |
|---|---|---|---|---|
| Claude Fable 5 | 10 | 50 | 1M | mạnh nhất; thinking luôn bật; **gấp đôi Opus 5** |
| Claude Opus 5 | 5 | 25 | 1M | thinking bật mặc định; có fast mode |
| Claude Sonnet 5 | 3 (2 tới 31-08-2026) | 15 (10) | 1M | |
| Claude Haiku 4.5 | 1 | 5 | 200K | |

**Kết luận chi phí quan trọng nhất: `effort` rẻ hơn nhiều so với nhảy hạng mô hình.**
`effort` nhận `low · medium · high · xhigh · max`; `xhigh` là mức tốt nhất cho hầu hết việc
lập trình và agentic, và là mặc định của Claude Code. Một lượt **Opus 5 ở `xhigh` tốn
khoảng một nửa Fable 5 ở `high`**. Nên quy tắc là: *nâng `effort` trước, đổi mô hình sau*.

### Bảng khuyến nghị theo loại việc

| loại việc | mô hình | effort | vì sao |
|---|---|---|---|
| Executor mặc định cho packet | **Opus 5** | `xhigh` | mặc định của Claude Code; đủ mạnh cho gần hết packet của kho này |
| Việc cơ học: tái sinh manifest/golden, đổi tên, đồng bộ doc | **Sonnet 5** hoặc **Haiku 4.5** | `low`–`medium` | không có quyết định thiết kế nào; trả tiền hạng cao là lãng phí |
| Việc CỰC khó: flake, đồng thời, khác biệt nền, thiết kế hai trần | **Fable 5** | `xhigh` | chỉ dùng **sau khi** Opus 5 đã thử và trượt, hoặc packet khai sẵn là lớp này |
| Reviewer chính (cross-provider) | **Codex** | cao | khác nền với executor ⇒ đạt `cross_approved` |
| Reviewer khi codex hết quota — `routine` | **Antigravity / Gemini Flash** | — | rẻ, đủ cho `routine`; là **advisory**, không tự xoá nợ |
| Reviewer khi codex hết quota — `sensitive` | **Fable 5** | `max` | đã chứng minh: một lượt `max` tự nghĩ 13 đột biến, **12/13 sống sót** qua suite 205 ca. Nhưng chỉ đạt `same_provider_approved` ⇒ **sinh nợ re-audit** |
| Đọc/tra cứu, tóm tắt log, quét kho | **Haiku 4.5** | `low` | ngữ cảnh 200K đủ; rẻ nhất |

**Quy tắc assurance (không đổi):** ưu tiên cross-review. `same_provider_approved` chỉ dùng
khi hết quota **hoặc** người giữ cho phép, và **luôn sinh một nợ re-audit** ghi vào sổ.

### Năm cách tiết kiệm token đã đo được trong kho này

1. **Trần review 2 vòng** đã chốt — chặn thẳng cái tốn nhất: vòng review thứ 3, 4.
2. **Review bundle đóng băng** (`ops/chatgpt_review/build_bundle.py`) — reviewer đọc diff
   đã cắt sẵn, không quét cả kho. Hạ tầng đã có, chưa dùng hết.
3. **Giao đúng `effort` theo packet**, khai trong Packet Spec, thay vì để mặc định `high`
   cho mọi việc.
4. **Packet nhỏ, không gộp** — ràng buộc sẵn có. Packet nhỏ ⇒ diff nhỏ ⇒ review rẻ.
5. **Đừng để reviewer tự quét kho.** Mỗi finding nay bắt buộc kèm gợi ý vá bốn phần, nên
   một lượt review đắt hơn nhưng **thay được một lượt điều tra riêng** của executor.

---

## 3. Nhóm A — ĐA NỀN TẢNG (làm trước)

### A1 · macOS chưa từng được đo — `PLAT-M1`

> **⛔ TẠM HOÃN — người giữ kho quyết định 20-08-2026: tạm thời bỏ macOS.**
> Mục này giữ nguyên làm hồ sơ, **không nhận việc từ nó**. Hai lỗi đo được trong lượt
> soạn nháp cũng ngủ theo (cả hai chỉ cắn khi macOS quay lại), chép ra đây để lần sau
> không phải tìm lại: `if:` gác **cả matrix** chứ không gác từng phần tử ⇒ nhãn
> `windows` sẽ kéo theo runner macOS và không gọi riêng macOS được; và bước cài
> `ripgrep` chạy `apt-get` ở nhánh `else` ⇒ trên macOS `doctor` thoát **12**, nhánh
> macOS đỏ vì lý do không liên quan gì tới macOS. Chi tiết:
> `ops/specs/plat-m1-packet-issue-nhap.md`.

- **Write set:** `.github/workflows/launcher-windows.yml` (đổi tên thành `launcher-nen.yml`)
- **Việc:** thêm `macos-latest` vào matrix; khai **số ca bỏ qua trên TỪNG nền** thành đầu
  ra dương, không để ẩn. Nếu macOS lộ ca hỏng thật thì **DỪNG** và mở packet riêng — sửa
  `launcher.py` nằm ngoài write set này.
- **Độ phức tạp:** trung bình. Rủi ro: macOS runner đắt gấp ~10 lần Linux ⇒ chỉ chạy khi
  push master, gọi tay, hoặc gắn nhãn `macos`.
- **Mô hình:** Executor **Opus 5 @ `high`** · Reviewer **Codex**
- **Review class:** `systemic`

### A2 · Nền tảng đa nền là thứ ít được gác nhất — `PLAT-M2`

- **Write set:** `.github/workflows/ci.yml`
- **Việc:** đưa **lượt Linux** của `launcher_test.py` vào `ci.yml` cho **mọi PR**. Windows
  và macOS vẫn theo nhãn (đắt). Cùng lớp với lỗ vừa vá ở `AG-T0-03`: bộ test tồn tại mà
  CI không gọi.
- **Độ phức tạp:** thấp. Một bước YAML.
- **Mô hình:** Executor **Sonnet 5 @ `medium`** · Reviewer **Antigravity/Gemini Flash**
  (đủ cho `routine`)
- **Review class:** `routine`
- **Phụ thuộc:** làm **sau** A3, nếu không CI sẽ đỏ ngay vì `t53`.

### A3 · `t53_doctor_bao_du_khi_du` đỏ trên máy đủ công cụ — `PLAT-M3`

- **Write set:** `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`
- **Việc:** `doctor` thoát 12 rồi ngay sau đó thoát 0 — cùng lệnh, cùng máy, cách nhau hai
  phút. Nợ đã ghi ở `ops/NO_KY_THUAT.md`. Phải tìm **nguồn chớp** rồi làm nó tất định.
  Cảnh báo chữ ký trùng đã ghi sẵn: trên host **không có** `codex`, `t53` đỏ **tất định**
  vì lý do khác hẳn — kiểm `command -v codex` TRƯỚC khi kết luận đã tái hiện.
- **Độ phức tạp:** **CAO**. Flake, khó tái hiện, đã hụt hai lần vì stdout bị bộ chạy nuốt.
- **Mô hình:** Executor **Fable 5 @ `xhigh`** — đây đúng lớp việc xứng đáng mô hình mạnh
  nhất · Reviewer **Codex @ cao**
- **Review class:** `sensitive`

### A4 · Đường GitHub cho phiên headless / di động — `PLAT-M4`

- **Write set:** `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`
- **Việc:** tách trường `mcp` của `doctor` làm hai, y hệt cách `_do_github` đã tách cho
  `rest`:
  - `mcp-cli` — `claude mcp get`, đo **dây nối** (hiện trả `Pending approval`)
  - `mcp-endpoint` — một lượt `initialize` **thật** tới URL khai trong `.mcp.json`, đo
    **đầu kia của dây**
  Áp đúng tiêu chí sẵn có: 4xx **có** header `x-github-*` là *tới nơi, thiếu quyền*;
  **không có** header là *proxy tự sinh*.
- **Vì sao quan trọng nhất cho mục tiêu đa thiết bị:** một phiên web/điện thoại đọc
  `mcp=khong` sẽ kết luận GitHub bị chặn và dừng — **đã xảy ra thật, mất trọn một lượt** —
  trong khi endpoint vẫn thông. Đo được: POST tới `api.githubcopilot.com/mcp/` bằng
  `GITHUB_PAT` trả HTTP 200, header GitHub đầy đủ, 44 công cụ.
- **Độ phức tạp:** trung bình–cao (phải có fixture cho cả hai trạng thái).
- **Mô hình:** Executor **Opus 5 @ `xhigh`** · Reviewer **Codex**
- **Review class:** `sensitive`

### A5 · Script chỉ chạy một nền — `PLAT-M5` (ưu tiên thấp hơn)

- `don-nhanh.ps1` · `deploy-guard.ps1` · `deploy-package.ps1` · `tl-setup.ps1` (+ `.cmd`)
- **Việc:** khai rõ nền cho từng script, và chuyển sang Python **thứ nào thật sự cần chạy
  đa nền**. Không chuyển hết — `tl-setup` là đường cài trên máy người dùng Windows, hợp lý
  khi giữ PowerShell.
- **Độ phức tạp:** cao nhưng **tách được** thành nhiều packet nhỏ.
- **Mô hình:** Executor **Opus 5 @ `high`** · Reviewer **Codex**
- **Xếp sau A1–A4:** hiện đã dùng được trên Windows, và `pwsh` chạy được trên Linux.

---

## 4. Nhóm B — nợ chặn, chạy song song được

| # | việc | mô hình | ghi chú |
|---|---|---|---|
| B1 | Cross-review codex cho `W0-R1` | **Codex** | quota mở `2026-08-20 06:23`. Mở khoá `#177` |
| B2 | Re-audit `AG-T0-04` (#163) và `AG-T0-02` (#164) | **Codex** @ cao | `reviewed_sha` rút gọn + stale |
| B3 | `#177` W0-R1B | Executor **Fable 5 @ `xhigh`** · Reviewer **Codex** | thiết kế hai trần — lớp khó nhất. Sau `W0-R1 integrated` |
| B4 | `#178` W0-RC | Executor **Opus 5 @ `xhigh`** · Reviewer **Codex** | 9 phản chứng, write set **chỉ tệp test** ⇒ rủi ro thấp hơn |

`#177` và `#178` dùng chung `packet_loop_test.py` ⇒ **không chạy song song**.

---

## 5. Nhóm C — hoãn hoặc bỏ

| việc | quyết |
|---|---|
| `A1` · `PLAT-M1` macOS vào matrix | **hoãn** — người giữ quyết định 20-08-2026. §3 và §7 (kể cả bản đính chính ở PR #187) vẫn vẽ A1 trong luồng đa nền; **dòng này thắng** |
| `AG-T0-05` registry ratchet | **hoãn** — phụ thuộc `AG-T0-03`, không chặn đa nền tảng |
| `AG-T0-01B` Antigravity `agy` discovery | **hoãn** — `planned_experimental` |
| `W0-R2` review receipt · `W0-R3` | **hoãn** sau nhóm A |
| `W1-P1` schema `review_verdict.v1` | **hoãn** — thư mục schema đang rỗng |
| `W1-S1` | **hoãn** |
| `W0-C1` · `W1-C2a` · `W1-C2b` · toàn bộ `M3`/`W2-*` | **BỎ** (đã quyết) |

---

## 6. Issue và PR sẵn có cần sửa

| đối tượng | vấn đề đo được | sửa thế nào |
|---|---|---|
| `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md` §2 | **3/7 dòng sai**: `AG-T0-01A`, `01C`, `03` đã land nhưng bảng ghi `ready_for_branch`/`planned` | **Bỏ hẳn cột trạng thái**, trỏ sang GitHub facts. Sửa tay sẽ lại lệch — đúng thứ kế hoạch đa provider §12 cấm |
| bảng packet §6 kế hoạch cũ | còn liệt kê packet đã BỎ | đánh dấu BỎ ngay trong bảng, kèm lý do |
| `#177` | phạm vi đã đổi vì chốt trần 2 vòng | **đã sửa** — nối mục 8, đọc ngược khớp byte |
| `#178` | không đổi | giữ nguyên |
| PR #182 · #183 | chờ review | không đổi |
| nhánh `agent/ag-t0-03-parser-coverage` | nhánh mồ côi ở `83cd05a` | chạy `ops-don-ref.yml` bằng `workflow_dispatch` — **kho đã có sẵn đường này**, không phải làm tay |

---

## 7. Thứ tự thi công đề nghị

```
NGAY (không cần review):
  dọn nhánh mồ côi qua ops-don-ref.yml
  merge PR #182, #183

SONG SONG 1 — đa nền tảng          SONG SONG 2 — nợ
  A3  t53 flake      Fable 5 xhigh   B1  cross-review codex   (từ 20-08 06:23)
   │                                  │
  A2  launcher vào CI  Sonnet 5       B2  re-audit #163/#164
   │                                  │
  A1  macOS vào matrix Opus 5         B3  #177   Fable 5 xhigh
   │                                  │
  A4  mcp-endpoint     Opus 5 xhigh   B4  #178   Opus 5 xhigh

SAU:
  A5 script một nền · nhóm C
```

`A3` đứng trước `A2` vì đưa một bộ test đang đỏ vào cổng PR sẽ chặn mọi PR.

---

## 8. Ràng buộc áp cho mọi packet trong kế hoạch này

- Trần review **2 vòng**, đếm theo vòng.
- Mỗi finding kèm **gợi ý vá bốn phần**.
- Master drift sau khi gate xanh ⇒ **merge thẳng**, kèm sáu kích hoạt bắt buộc chạy lại.
- Đặt `core.abbrev` bằng 7 trước mọi cổng, nếu không hai ca doc-claims **đỏ oan**.
- Đọc ngược mọi thứ đã đăng lên GitHub. `git fetch` qua proxy **nói dối** — dùng
  `git ls-remote`.
- Packet Spec phải khai **`effort`** cùng với mô hình. Không khai thì mặc định `high`, và
  đó thường là lãng phí hoặc thiếu.
