# Đặc tả packet `LAUNCHER-DUNG-WORKSPACE`

```yaml
packet_id: LAUNCHER-DUNG-WORKSPACE
packet_issue: null                 # CHUA mo Issue — dac ta dong bang truoc, Issue+lease sau
revision: 1
generation: 1
review_class: sensitive
assurance_target: cross_approved
base_sha: efd583b                  # master luc soan; DO LAI truoc khi cap lease
```

> **Đặc tả không phải lease.** Đóng băng xong vẫn phải có Issue + lease còn hiệu lực theo
> `docs/PROTOCOL_DA_PHIEN.md` §3.2 và §4 mới được bắt tay. Phiên nào đọc tệp này rồi tự làm là
> tự cấp việc cho mình.

---

## 1. `nguon_cap_viec`

Không phải một dòng kế hoạch — packet này sinh từ **hai sự cố đo được trong phiên 2026-08-23**,
biên nhận là thân hai PR:

| sự cố | biên nhận | giá phải trả |
|---|---|---|
| workspace là `git worktree` ⇒ Claude Code quy chiếu project về kho chính (`hasTrustDialogAccepted: false`) ⇒ **101** mục `permissions.allow` bị bỏ ⇒ **72** lần `"This command requires approval"` | PR #291 (packet #290 lượt 1) | executor viết đủ 6 tệp / 400 dòng nhưng **chưa bao giờ chạy nổi một lệnh**; toàn bộ `T1..T8` là `KHÔNG_ĐO_ĐƯỢC` |
| `codex` 0.149 tự chọn `sandbox: read-only` cho một workdir, trong khi **cùng câu lệnh** ở thư mục khác cho `workspace-write` | PR #289 (packet #276 vòng 3, lượt 1) | lượt chạy **243 giây**, `rc=0`, `trang_thai=xong`, **0 dòng mã** |

Người giữ kho `ducthangho` yêu cầu trực tiếp trong phiên 2026-08-23, và chốt phạm vi qua vòng
hỏi Q6–Q9 của `/soan-spec`.

## 2. `review_class` — `sensitive`

`docs/PROTOCOL_DA_PHIEN.md:573` liệt kê **`launcher`** đích danh. `:567` — *"Executor không được
hạ lớp."* Trần `ADR-0044` cho `sensitive` chạm authority: **≤ 3 tệp và ≤ 300 dòng thêm**.

Không hạ xuống `systemic` dù đây là tooling: cùng hình dạng sai đã bị đính chính ở `PLAT-M4`
(`ops/DINH_CHINH_REVIEW_CLASS_PLAT_M4.md`) — **phân loại theo VỊ TRÍ thay vì theo HẬU QUẢ**.

## 3. `write_set` — 2 đường dẫn

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

`derived_set` **RỖNG**: `.claude` thuộc `_RELEASE_EXCLUDE_DIRS`, nên không kéo theo tái sinh
`RELEASE_MANIFEST.json`. Đo 18:35Z 23-08-2026 trên `efd583b`: `launcher.py` **3.892 dòng**,
`launcher_test.py` **6.815 dòng**.

**Va chạm đã đo (18:3xZ 23-08-2026):** Issue **#219** (`AG-T0-01B`) khai **đúng hai đường dẫn
này**, đang `open`, nhãn `state:leased`. Nhưng **cả hai lease của nó đã HẾT HẠN**
(`2026-08-22T09:35Z`, `2026-08-23T02:05Z`) và **hiện vật KHÔNG có trên master**
(`git show origin/master:.claude/dev/launcher.py | rg -cw agy` ⇒ **0**) ⇒ write set đang **rỗng
người giữ**. Người giữ kho đã quyết `#219` chạy **sau** packet này, vì Antigravity hết quota nên
`#219` không chứng minh được đầu-cuối lúc này.

**Trước khi cấp lease phải ĐO LẠI cả hai điều đó** — "chưa hết hạn ≠ còn hiệu lực", và nhãn
`state:leased` là thứ trôi.

## 4. `ngoai_pham_vi` — cố ý KHÔNG làm

| thứ | vì sao KHÔNG |
|---|---|
| **Launcher tự DỰNG workspace** (clone, set remote, checkout) | Cần mạng + credential; mỗi thứ là một họ lỗi mới. Chốt **từ chối** bắt được đúng ca đã xảy ra với ~20 dòng. Để packet `P1b`. |
| **Probe chạy lệnh THẬT của agent** (tốn quota) | Ca nó bắt thêm — `trust=False` của claude — bắt được **rẻ hơn** bằng một phép đọc tệp (§6.4). Trả tiền mỗi lần phóng để mua thứ đã có là lỗ. |
| Tạo session, effort theo nền, read/write, cài công cụ | Là P2–P4 của cùng kế hoạch. Gộp vào đây thì vượt trần `sensitive` chắc chắn. |
| Antigravity / `agy` | Issue **#219**, đặc tả riêng `ops/specs/ag-t0-01b-r4.md`. **Không viết bản kê thứ hai** — hai bản sẽ trôi lệch. |
| Sửa `.claude/settings.json` hoặc `~/.claude.json` | Packet này **ĐỌC** trạng thái trust, **không GHI**. Ghi vào tệp cấu hình của người dùng là hình dạng đã ăn **bảy** phát hiện liên tiếp (CLAUDE.md, bộ gỡ `shell_environment_policy`). |

## 5. `muc_tieu` — mỗi mục chiếu vào MỘT đường dẫn của `write_set`

**M1 — Từ chối workspace là `git worktree`.** → `.claude/dev/launcher.py`
`run` kiểm `<workspace>/.git`: là **tệp** (con trỏ worktree) ⇒ thoát mã riêng, in câu chữa nêu
rõ *"dùng bản clone độc lập"*. Là **thư mục** ⇒ đi tiếp.

**M2 — Probe GHI: viết một tệp tạm trong workspace rồi xoá.** → `.claude/dev/launcher.py`
Không ghi được ⇒ chặn. Đây là chốt bắt `sandbox: read-only`.

**M3 — Probe SPAWN: chạy `<chương trình> --version`, đòi rc=0 VÀ đầu ra khác rỗng.** →
`.claude/dev/launcher.py`
Đòi **cả hai**, không đòi mỗi `rc`: `rc=0` kèm đầu ra RỖNG là ca đã xảy ra thật (r244,
`param([string[]]$Args)`).

**M4 — Đọc trust của Claude Code, KHÔNG ghi.** → `.claude/dev/launcher.py`
Đọc `~/.claude.json` → `projects[<đường dẫn giải quyết được>].hasTrustDialogAccepted`. Thiếu
khoá / không đọc được tệp ⇒ `KHÔNG_ĐO_ĐƯỢC`, **không** đọc thành `True`.

**M5 — Fail-close, có đường thoát GHI SỔ.** → `.claude/dev/launcher.py`
Bất kỳ probe nào hỏng ⇒ **chặn**. Cờ `--bo-qua-probe` cho đi tiếp nhưng **bắt buộc** kèm lý do,
và lý do ấy phải vào `run.json`.

**M6 — Ghi kết quả probe vào `run.json`.** → `.claude/dev/launcher.py`
Ba trạng thái mỗi probe: `DAT` · `DO` · `KHONG_DO_DUOC`. Gộp `KHONG_DO_DUOC` vào `DAT` là cấm.

## 6. `nghiem_thu` — mỗi tiêu chí nêu PHÉP ĐO LÀM NÓ ĐỎ

Mọi ca sống ở `.claude/dev/launcher_test.py`, đặt tên `rXX_`. **Mỗi ca đúng MỘT đột biến**, và
**bán kính đo trên TOÀN suite** — nền hiện tại phải đo lại lúc bắt đầu (18:35Z 23-08-2026:
`143/143` đã chạy qua, tổng 144, bỏ qua 1 = fixture Windows).

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| **N1** | workspace là worktree thật (`git worktree add`) ⇒ `run` **chặn** | đột biến `m1_coi_worktree_la_hop_le` (bỏ nhánh kiểm `.git` là tệp) **không** làm ca này đỏ |
| **N2** | workspace là clone thật ⇒ `run` **đi tiếp** (chiều BẮT OAN) | ca này đỏ trên bản **sạch** ⇒ chốt chặn oan việc đúng |
| **N3** | thư mục chỉ-đọc ⇒ probe GHI chặn | đột biến `m2_bo_probe_ghi` không làm đỏ |
| **N4** | chương trình in rỗng nhưng `rc=0` ⇒ probe SPAWN chặn | đột biến `m3_chi_kiem_rc` (bỏ điều kiện đầu ra khác rỗng) không làm đỏ |
| **N5** | `~/.claude.json` thiếu khoá ⇒ `KHONG_DO_DUOC`, **không** `DAT` | đột biến `m4_thieu_khoa_coi_la_tin_cay` không làm đỏ |
| **N6** | probe hỏng + **không** có `--bo-qua-probe` ⇒ mã thoát khác 0 | đột biến `m5_canh_bao_thay_vi_chan` không làm đỏ |
| **N7** | `--bo-qua-probe` **không** kèm lý do ⇒ từ chối | đột biến `m5b_cho_bo_qua_khong-can-ly-do` không làm đỏ |
| **N8** | `--bo-qua-probe` có lý do ⇒ đi tiếp **và** lý do có mặt trong `run.json` | đột biến `m6_khong_ghi_so` không làm đỏ |
| **N9** | ba trạng thái probe có mặt trong `run.json`, `KHONG_DO_DUOC` không bị gộp vào `DAT` | đột biến `m6b_gop_khong_do_duoc_vao_dat` không làm đỏ |

**Chốt chung, áp cho mọi ca trên:**

- Đột biến chạy trên **bản sao tạm**, tên tệp **riêng từng đột biến**, xoá `.pyc` + tắt ghi
  bytecode. Lý do: CPython coi `.pyc` hợp lệ theo **(mtime tính bằng GIÂY, kích thước)** — hai
  đột biến cùng kích thước ghi trong cùng một giây thì bản sau **chạy mã của bản trước**. Kho
  mất ba lượt review vì đúng chuyện này.
- **Đột biến không BIÊN DỊCH ĐƯỢC là đột biến không chạy** ⇒ phải báo ĐỎ tại chỗ, không được
  làm sập cả lượt và che các đột biến sau.
- **Đột biến giết thêm ca ngoài họ ⇒ sửa ĐỘT BIẾN, đừng sửa chốt.** Hai lần trong
  `codex_cred_test.py` (23-08) mắc đúng lỗi này: đột biến đo **hai** tính chất cùng lúc.
- **Windows là bắt buộc** trên exact SHA. Gắn nhãn `windows` **KHÔNG đủ**: `ci.yml` khai
  `pull_request:` không kèm `types:` nên `labeled` không sinh lượt chạy nào. Đường chắc chắn là
  `workflow_dispatch` tay. Đo được 23-08 trên PR #289: `gate (windows-latest)` 61 bước chạy
  thật, `launcher (windows-latest)` 4 probe Windows-only đều xanh.

**Ngân sách:** ước lượng **~115 dòng** ở `launcher.py` + **~150** ở `launcher_test.py` =
**~265/300**, 2/3 tệp. Vượt ⇒ **NÉN, không nới**; thứ cắt đầu tiên là **M3** (probe spawn), vì
`doctor` đã đo công cụ rồi.

## 7. `hinh_dang_ke_thua`

Không phải packet khắc phục của một packet hỏng, nhưng L4 vẫn áp — vì packet này **chính là**
bản vá cho một hình dạng lỗi đã đếm được:

```
hinh_dang: 'dem SU CO MAT cua mot duong thay vi KHA NANG cua no'
so_lan_da_ghi_nhan: 6
```

Bốn lần đã ghi trong `CLAUDE.md` (`shutil.which("gh")` tính là đường mở · `rest-chung` mở nhưng
không đọc nổi PR nào · `gh auth status` xanh trong khi mọi thao tác kho trả 403 · `doctor` mục
`hook-phien` so **băm tệp** tức đo *"tệp có mới không"* chứ không đo *"hook đã chạy chưa"*), cộng
**hai** lần đo được trong phiên 23-08 (worktree: phiên điều phối đọc **số lời gọi công cụ** thành
tiến độ thay vì đo lời gọi có **thành công** không · codex: câu lệnh có mặt nhưng năng lực ghi
vắng).

Doctrine nói *"cùng một hình dạng lặp ba lần trở lên thì câu hỏi đúng là **có nên làm việc này
không**, không phải **vá thế nào**"*. Ở đây câu trả lời **không** phải bỏ việc: sáu lần đều là
*suy* năng lực từ sự có mặt, và packet này thay `suy` bằng **ĐO**. Nếu một lượt thi công thấy
mình đang thêm một phép **suy** nữa thay vì một phép **đo**, đó là điều kiện dừng.

## 8. `chua_do_duoc` — khai thẳng

- **Ranh giới trust của Claude Code là quan sát, không phải hợp đồng.** Kết luận *"worktree ⇒
  project quy chiếu về kho chính"* rút từ **một** thông điệp lỗi quan sát được 23-08. Chưa đọc
  mã Claude Code, chưa có tài liệu. Hành vi này đổi được ở bản sau mà không ai báo ⇒ ca `N1`
  đo **triệu chứng** (`.git` là tệp), không đo **nguyên nhân**.
- **`~/.claude.json` không phải giao diện công khai.** Đường dẫn và tên khoá
  `hasTrustDialogAccepted` là quan sát 23-08. Đổi tên khoá ⇒ `M4` trả `KHONG_DO_DUOC` — đúng
  fail-close, nhưng mất tín hiệu mà không ai biết. Chưa có cách canh việc đó.
- **Chưa đo trên macOS.** Hai nền có bằng chứng là Linux (phiên này) và Windows (CI). macOS
  không có trong ma trận `ci.yml`.
- **Chưa biết `codex` chọn `sandbox` theo luật nào.** Đo được *hiện tượng* (cùng câu lệnh, hai
  thư mục, hai kết quả) nhưng **không** biết nguyên nhân. `M2` vì thế đo **năng lực ghi thật**
  chứ không đoán chế độ sandbox — cố ý.
- **Trần 300 dòng chưa được kiểm bằng bản dựng thật.** Con số `~265` là **ƯỚC LƯỢNG** của phiên
  soạn, không phải phép đo. Nó có thể sai, và nếu sai thì `§6` đã nói trước: nén, không nới.
