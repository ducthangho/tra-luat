# Đặc tả packet `LAUNCHER-DUNG-WORKSPACE` — **revision 2**

```yaml
packet_id: LAUNCHER-DUNG-WORKSPACE
packet_issue: 292
revision: 2
generation: 1
review_class: sensitive
assurance_target: cross_approved
base_sha: f33c12d                  # master luc soan r2; DO LAI truoc khi cap lease
```

> **`r1` KHÔNG bị sửa đè.** `ops/specs/LAUNCHER-DUNG-WORKSPACE.md`
> (`94351fd0e6e0d788ddf4a13ac03b0c9a7cd82e65a44905df77a9106dff171957`) giữ nguyên và **đang có
> hiệu lực cho lượt thi công hiện hành**. Sửa đè một đặc tả đã băm là làm băm trong lease trỏ vào
> thứ không còn tồn tại.
>
> **`r2` CHỈ THÊM `M7`.** Không đổi `M1`–`M6`, không đổi `N1`–`N9`, không đổi `write_set`.

---

## 0. Delta so `revision 1` — thêm đúng một mục tiêu

`r1` làm launcher **PHÁT HIỆN** năng lực (probe ghi, probe spawn, đọc trust). `r2` thêm nửa còn
lại: launcher **CẤP** năng lực, để phiên con thực thi được **mà không phải hỏi**, trừ trường hợp
bắt buộc phải hỏi.

Hai nửa của một việc. Tách thành hai packet thì chúng vẫn phải nối đuôi nhau (cùng `write_set`),
mà lại mất mạch.

## 1. Vì sao `M7` tồn tại — luật ĐÃ CÓ và ĐÃ TRÔI

Cơ chế không mới. Nó được ghi ở `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md:378`:

```
-- claude -p --model opus --effort max --permission-mode acceptEdits --output-format json
```

kèm luật ngay dưới: *"Không dùng `--dangerously-skip-permissions`."*

**Nhưng không cổng nào đọc dòng đó, và `launcher.py` không biết gì về quyền** — bốn chỗ khớp
`permission` trong tệp đều là `PermissionError` của Python, không liên quan. Người gọi phải tự nhớ.

Đo được **phiên 2026-08-23**: phiên điều phối phóng **6 lượt `claude`**, cả sáu `so_doi_so = 4`
(`-p` · `--effort` · `max` · prompt). **KHÔNG lượt nào** truyền `--permission-mode`. Bốn chỗ
`grep` thấy chuỗi ấy trong nhật ký hoá ra là **các phiên codex đang ĐỌC tệp kế hoạch** rồi in lại.

Hệ quả đo được: packet #290 lượt 1 ăn **72** lần `"This command requires approval"` và executor
**viết đủ 400 dòng mà chưa bao giờ chạy nổi một lệnh**. Hai nguyên nhân **độc lập, cùng hướng**:
workspace là `worktree` (⇒ mất `settings.json`, đã là `M1`) **và** không cấp allowlist theo lượt
(⇒ `M7`). Vá một nửa thì nửa kia vẫn giết.

Đây là hình dạng *"một luật sống trong tài liệu mà không cổng nào cưỡng chế"* — cùng họ với
*"nghĩ ra được phép thử mà không chạy nó thì phép thử ấy không tồn tại"*, chỉ khác là nạn nhân
ở đây là một **luật vận hành**, không phải một ca test.

## 2. Ba sự thật đã trả giá — mã hoá, đừng để trong tài liệu

Biên nhận: `ops/reviews/README.md:39` và
`ops/reviews/lease-dang-review-1-claude-verdict.receipt.yaml:92`.

| # | sự thật | bằng chứng |
|---|---|---|
| **S1** | `--permission-mode bypassPermissions` **giải ra** `--dangerously-skip-permissions`, thứ `claude` **TỪ CHỐI chạy dưới quyền root** | lượt review chết sau **1,1 giây**, `stdout` **0 byte** |
| **S2** | `--allowedTools` là cờ **NHẬN NHIỀU GIÁ TRỊ** ⇒ đặt ngay trước prompt thì nó **NUỐT LUÔN prompt** | `claude` báo *"Input must be provided either through stdin or as a prompt argument"* — **một thông báo về stdin cho một lỗi về THỨ TỰ ĐỐI SỐ** |
| **S3** | `codex` mặc định **`sandbox: read-only`** ở một số workdir, cùng câu lệnh ở thư mục khác lại cho `workspace-write` | đo 23-08: lượt chạy **243 giây**, `rc=0`, **0 dòng mã** |

`S2` là cái nguy nhất: thông báo lỗi **chỉ sai hướng hoàn toàn**, nên người gặp sẽ đi tìm stdin
trong khi lỗi nằm ở thứ tự đối số.

## 3. `write_set` — KHÔNG ĐỔI so `r1`

```
.claude/dev/launcher.py
.claude/dev/launcher_test.py
```

## 4. `ngoai_pham_vi` — thêm so `r1`

| thứ | vì sao KHÔNG |
|---|---|
| `--dangerously-skip-permissions` và mọi đường tương đương | `S1`: `claude` từ chối dưới root; và kho đã cấm tường minh. Đây là **CẤM**, không phải "không ưu tiên". |
| Tự sửa `.claude/settings.json` để nới quyền | `r1` §4 đã cấm GHI tệp cấu hình người dùng. `M7` cấp quyền **theo lượt**, không sửa cấu hình vĩnh viễn. |
| Suy diễn chế độ quyền cho một nền **chưa đo** | Bảng ở `M7` chỉ chứa nền **đã có bằng chứng chạy**. `agy`/Antigravity ⇒ Issue #219. |

## 5. `muc_tieu` — THÊM `M7` (M1–M6 giữ nguyên từ `r1`)

**M7 — Launcher TỰ cấp chế độ thực thi theo nền, và TỪ CHỐI phóng khi không rõ.**
→ `.claude/dev/launcher.py`

Bảng **CHO PHÉP** (không phải danh sách cấm — danh sách cấm không bao giờ đủ):

```
claude : --permission-mode acceptEdits          # mac dinh
codex  : --sandbox workspace-write              # S3: mac dinh la read-only, PHAI khai tuong minh
```

Ba chốt:

1. **Fail-close**: người gọi không khai chế độ, và nền không có trong bảng ⇒ **TỪ CHỐI phóng**.
   Không đoán. Không "để mặc định của công cụ" — `S3` chứng minh mặc định ấy đổi theo thư mục.
2. **Chặn `bypassPermissions`** và mọi bí danh giải ra `--dangerously-skip-permissions` (`S1`).
3. **Chặn thứ tự đối số nguy hiểm**: nếu lệnh có cờ nhận-nhiều-giá-trị (`--allowedTools`) đứng
   **ngay trước** chuỗi prompt ⇒ từ chối, nêu rõ *thứ tự đối số*, không nêu stdin (`S2`).

## 6. `nghiem_thu` — THÊM `N10`–`N13` (N1–N9 giữ nguyên)

Mọi ca ở `.claude/dev/launcher_test.py`, **mỗi ca đúng MỘT đột biến**, bán kính đo trên TOÀN suite.

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| **N10** | lệnh `claude` không có cờ chế độ ⇒ launcher **thêm** `--permission-mode acceptEdits`; lệnh `codex` ⇒ thêm `--sandbox workspace-write` | đột biến `m7_khong_cap_che_do` (bỏ bước thêm cờ) không làm ca này đỏ |
| **N11** | nền **không có trong bảng** ⇒ **TỪ CHỐI phóng**, mã thoát khác 0 | đột biến `m7_nen_la_thi_cho_qua` (thay từ chối bằng đi tiếp) không làm đỏ |
| **N12** | lệnh chứa `bypassPermissions` hoặc `--dangerously-skip-permissions` ⇒ **TỪ CHỐI** | đột biến `m7_cho_bypass` không làm đỏ |
| **N13** | cờ nhận-nhiều-giá-trị đứng ngay trước prompt ⇒ từ chối, **thông điệp nêu THỨ TỰ ĐỐI SỐ** | đột biến `m7_bo_kiem_thu_tu` không làm đỏ · **và** ca phải kiểm NỘI DUNG thông điệp, vì `S2` đúng là ca thông điệp chỉ sai hướng |

**Chiều BẮT OAN, bắt buộc:** một lệnh **đã có sẵn** cờ chế độ hợp lệ do người gọi truyền ⇒ launcher
**KHÔNG được thêm lần hai**, và **không được từ chối**. Ca này đỏ trên bản sạch nghĩa là `M7` đang
chặn oan chính đường dùng đúng.

**Không có ca nào được đo bằng cách đọc mã.** `N10` phải kiểm **đối số thực sự truyền cho tiến
trình con**, không kiểm một biến trung gian — nếu không nó lại là *"đo vật thay thế cho cửa thật"*,
đúng hình dạng đã giết `N11` của packet #262 **ba lần**.

## 7. Ngân sách

`r1` khai **≤ 2 tệp · ≤ 300 dòng thêm** (trần `ADR-0044` cho `sensitive`). `M7` + 4 ca + 4 đột
biến **không** vừa phần còn lại của trần ấy.

**⚠️ Con số cho `r2` CHƯA XÁC ĐỊNH ĐƯỢC tại thời điểm soạn**, vì lượt thi công `r1` **đang chạy**
và chưa biết nó tiêu bao nhiêu. Ước lượng thô: `M7` ~45 dòng ở `launcher.py`, ~90 ở
`launcher_test.py` ⇒ **~135 dòng THÊM** so với head sau khi `r1` land.

Trần `r2` phải được chốt **sau khi `r1` land và đo được số thật**. Vượt trần `ADR-0044` ⇒ cần
ngoại lệ người giữ kho; **đừng tự nới** — và đừng ép `M7` vào cho vừa bằng cách cắt phản chứng.

## 8. `hinh_dang_ke_thua`

Kế thừa nguyên bộ đếm của `r1`:

```
hinh_dang: 'dem SU CO MAT cua mot duong thay vi KHA NANG cua no'
so_lan_da_ghi_nhan: 6
```

`r2` thêm một hình dạng **thứ hai**, đếm riêng:

```
hinh_dang_2: 'luat song trong TAI LIEU ma khong cong nao cuong che'
so_lan_da_ghi_nhan: 1        # chinh M7 nay
ghi_chu: >-
  Cung ho voi "nghi ra duoc phep thu ma khong chay no thi phep thu ay khong ton tai",
  chi khac nan nhan la mot LUAT VAN HANH. Neu trong luot thi cong M7 co ai de nghi
  "ghi them vao tai liệu cho ro" THAY VI viet mot ca test, do la lan thu hai — va la
  dieu kien dung.
```

## 9. `chua_do_duoc`

- **Bảng chỉ có hai nền.** `agy`/Antigravity chưa có bằng chứng chạy về chế độ quyền ⇒ **không**
  đưa vào bảng. Issue #219 phụ trách.
- **`--permission-mode auto` chưa đo.** `ops/handoff/don-nhanh-150-handoff.md:73` dùng nó, nhưng
  phiên soạn `r2` **không** chạy lại để xác nhận. Bảng chọn `acceptEdits` vì nó có bản gọi chính
  tắc trong kế hoạch; `auto` để ngỏ.
- **Không biết `claude` sẽ đổi tên/ngữ nghĩa cờ ở bản sau.** `N10` đo **đối số truyền cho tiến
  trình con**, nên nó phát hiện được việc launcher ngừng cấp cờ — nhưng **không** phát hiện được
  việc cờ ấy đổi ý nghĩa phía `claude`. Chưa có cách canh việc đó.
- **Chưa đo macOS**; ma trận CI chỉ có ubuntu + windows.
- **Ngân sách `r2` chưa đo được** — xem §7.
