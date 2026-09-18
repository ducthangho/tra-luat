# WP541 — chỉ thị thi công, executor `antigravity`, lượt 1 / generation 1

> Soạn 00:5xZ 18-09-2026 bởi phiên điều phối (claude). **Đây là bản chiếu.** Nguồn có thẩm quyền là
> tệp lease và tệp spec trong kho, cả hai có băm. Lệch nhau thì **tệp đúng**, không phải văn bản này.

## 1. Neo — TỰ XÁC MINH, đừng nhận bảng giá trị này

```
git fetch origin ops/cap-lease-541 claude/spec-541-r2-20260917
git show origin/ops/cap-lease-541:ops/leases/wp541-path-r1-g1-antigravity.yaml   # lease
git show origin/claude/spec-541-r2-20260917:ops/specs/wp541-path-toi-thieu-theo-nen-r2.md \
  | sha256sum        # phải ra fc6e814d2bfacf74a00537a57bd33aca712d50eca5302b23780bfbeef1162075
```

| | |
|---|---|
| Packet Issue | **#541** `WINDOWS-LEASE-PUBLISH` |
| `lease_id` | `wp541-path-r1-g1-antigravity`, hết hạn **`2026-09-19T00:00:00Z`** |
| `spec_hash` | `fc6e814d2bfacf74a00537a57bd33aca712d50eca5302b23780bfbeef1162075` (22 812 byte) |
| nhánh của bạn | `agy/wp541-path-r1-g1` — độc quyền |
| `start_from_sha` | `d705623162b75b7340ee7cca54ac2d2abbddbb6f` (`origin/master` lúc cấp) |
| lớp | `sensitive` · `assurance_target: human_audited` |

Băm không khớp, hoặc lease đã hết hạn lúc bạn đọc ⇒ **DỪNG**, báo chủ kho. Đừng tự suy.

## 2. ĐỌC TRƯỚC KHI GÕ LỆNH NÀO

```
sed -n '1,140p' .claude/dev/launcher.py
python3 .claude/dev/launcher.py doctor        # rc=12 = thiếu công cụ bắt buộc
python3 .claude/dev/launcher.py chuan-bi      # khôi phục xác thực khi hook không chạy
git config core.abbrev 7
git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'
```

Dòng `remote.origin.fetch` **không phải nghi lễ**. Đo 17-09: clone `--depth 1` siết refspec thành
một-nhánh, khiến `git rev-parse '<nhánh>@{upstream}'` **thất bại** dù `refs/remotes/origin/<nhánh>`
có thật và đúng SHA; `ai-dang-giu` đọc `%(upstream)` qua `for-each-ref` nên thấy rỗng rồi fail-close
`rc=12` cho **mọi** đường. Sai refspec thì mọi phép quét lease của bạn đều vô nghĩa.

Rồi đọc `CLAUDE.md` và `docs/PROTOCOL_DA_PHIEN.md`.

## 3. RÀNG BUỘC CỨNG NHẤT — đọc kỹ, nó là thứ dễ phá nhất

Write set có **hai** đường, nhưng **chúng KHÔNG mở cùng lúc**:

```
ops/lease_publish.py        → MỞ NGAY.  ai-dang-giu rc=11, NGƯỜI_GIỮ 1 = chính bạn.
ops/lease_publish_test.py   → CHƯA MỞ.  ai-dang-giu rc=11, NGƯỜI_GIỮ 2 =
                              bạn + ci-windows-r2-g2-antigravity (#548).
```

Đây là **chồng lấn có thật, đã khai** trong lease (`CHONG_LAN_DA_BIET`). Lease #548 hết hạn
`2026-09-18T17:00:00Z`.

**Luật:** bắt tay ngay trên `ops/lease_publish.py`. **KHÔNG chạm `ops/lease_publish_test.py`** cho
tới khi bạn **tự đo** được `ai-dang-giu ops/lease_publish_test.py` trả `rc=0` / `NGƯỜI_GIỮ 0`.

**Đừng suy từ mốc `17:00:00Z`.** *"Hết hạn" KHÔNG phải "đã nhả"* — lease gia hạn được, và phải đọc
`da_bi_thay_the`. Kho đã trả giá một lần: `#227`, cửa sổ hai writer ~23,75 giờ.

Và nói thẳng: chốt này là **KỶ LUẬT, không có máy nào cưỡng chế**. Không cổng nào chặn bạn sửa tệp
test sớm. Nếu bạn phá nó, không ai biết cho tới khi hai bản vá đè nhau.

## 4. Việc phải làm — hai mục, đúng như spec r2

**M1 — `ops/lease_publish.py`** (mở ngay)

Thay hằng số ở `:1106` bằng phép giải **THEO NỀN**. Thêm
`_git_windows(path=None, system_root=None, program_files=None, cwd=None)` **trong chính tệp này**,
theo khuôn `_bash_windows` của `ops/cong_cu.py` (đọc nó trước — danh sách ứng viên có thứ tự, loại
trừ theo VỊ TRÍ, tham số tiêm để test lái được). `_git_exe_toi_thieu(*, nen=None, **tiem)` nhận tham
số tiêm. Giữ nguyên `Chan(RC_KHONG_XAC_DINH)` khi trượt hết, và giữ hợp đồng *"trả đường TUYỆT ĐỐI
đã resolve"* — `_env_rong` lấy `Path(git_exe).parent` làm **toàn bộ PATH của tiến trình con**.

Thứ tự ứng viên trên Windows: `CONG_CU_GIT` → thư mục cài Git phân giải từ `%ProgramFiles%` →
`shutil.which("git")` **ở chót**. Mọi bước: loại ứng viên trong **cwd**, loại ứng viên dưới
**`%SystemRoot%`**. POSIX **giữ nguyên** `/usr/bin:/bin`.

Bước `%ProgramFiles%` không phân giải được ⇒ ghi `KHÔNG_ĐO_ĐƯỢC` vào chẩn đoán **rồi mới** thử bước
chót; không im lặng rơi xuống.

**M2 — `ops/lease_publish_test.py`** (chỉ sau khi đo được `rc=0`)

Thêm **≥4** ca `rXX_` mới, chạy được trên `ubuntu-latest`, mỗi ca kèm đột biến đổi màu riêng.

## 5. Nghiệm thu — mỗi tiêu chí nêu thứ làm nó ĐỎ

| | tiêu chí | đột biến phải làm nó ĐỎ |
|---|---|---|
| **N1** | nền Windows giả: không ứng viên hợp lệ ⇒ `Chan(RC_KHONG_XAC_DINH)`; có `%ProgramFiles%\Git\cmd\git.exe` ⇒ trả đúng đường ấy, tuyệt đối | quay bước giải Windows về hằng số `"/usr/bin:/bin"` |
| **N2** | nền Windows giả, `cwd` có `git.bat` **và** `git.py` ⇒ kết quả **KHÔNG** trỏ vào cwd | gỡ phép loại-trừ-cwd |
| **N3a** | ứng viên dưới `%SystemRoot%` bị loại | gỡ phép loại `%SystemRoot%` |
| **N3b** | `%ProgramFiles%` không phân giải ⇒ ghi `KHÔNG_ĐO_ĐƯỢC`, không im lặng rơi xuống | đổi thành rơi thẳng xuống bước chót, không ghi gì |
| **N4** | POSIX không hồi quy: `ubuntu-latest` vẫn trả `/usr/bin/git` | đổi nhánh POSIX sang hằng số khác |
| **N5** | *(chỉ báo, KHÔNG phải tiêu chí)* delta ca đỏ so `d705623` = 0 | — |
| **N6** | `git diff --numstat` so `d705623`: ≤ **2** tệp, ≤ **300** dòng thêm | vượt ⇒ DỪNG, handoff |

**N1 là MỘT chốt cho BA nguyên nhân** (dấu phân cách `;` · `/usr/bin` không tồn tại · PATHEXT). Trên
Windows chúng nổ cùng lúc nên **không phân biệt được bằng đầu vào** ⇒ là một bộ TƯƠNG ĐƯƠNG. Đừng
đếm thành ba chốt rồi khai độ phủ rộng hơn thực tế.

**N2 đo chế độ hỏng THỨ HAI**, khác hẳn N1: nhánh `win32` của `shutil.which` tự
`path.insert(0, os.curdir)`, nên PATH "tối thiểu" **tự nhận cwd** — đúng cái nó sinh ra để chặn.
Phân biệt được với N1 bằng đầu vào (cwd sạch ⇔ cwd có `git.*`).

## 6. Vì sao KHÔNG neo nghiệm thu vào `gate (windows-latest)` — hai lý do, cả hai đo được

1. **`t150` sẽ vẫn ĐỎ.** Nó ngoài phạm vi và hỏng vì nguyên nhân KHÁC — đo từ log job
   `105238582317`: **14 ca PATH · 1 ca `t150` KHÁC**; hai dòng chẩn đoán của `t150` **không chứa**
   `PATH tối thiểu`, **không chứa** `/usr/bin`. Nó thuộc packet riêng **#552**. Nên cổng Windows
   **không thể xanh** sau WP541 dù bạn làm đúng hoàn toàn.
2. **Cổng ấy đã THÔI CHẠY.** Từ `#548` (`d705623`), `ci.yml` bỏ điều kiện
   `github.ref == 'refs/heads/master'`; push master giờ chỉ chạy `ubuntu-latest`. ADR-0049 ghi thẳng:
   *"Cổng Windows đang đỏ biến mất khỏi CI không phải vì được chữa."*

⇒ N1–N4 chạy trên `ubuntu-latest` bằng **tham số tiêm** là đường đo duy nhất còn lại. Nó không tiêu
`manual_ci_budget`. Một lượt trên máy Windows của chủ kho là **xác nhận cuối**, không phải phép đo
nghiệm thu.

## 7. CẤM

- `self_review` · `self_approve` · `merge` · `land` · `deploy` · LIVE · ruleset · admin bypass
- **`workflow_dispatch`, gọi CI Windows bằng tay** — `manual_ci_budget: 0`
- **chạm `ops/lease_publish_test.py` trước khi đo được `rc=0`** (mục 3)
- **vá `t150`** — nó thuộc #552, nguyên nhân khác; gộp vào là cấp **tín dụng giả**
- **đặt `_git_windows` vào `ops/cong_cu.py`** — Issue #541 khai write set `only` hai tệp
- **thay phép giải cố định bằng PATH thừa kế KHÔNG giới hạn** (nguyên văn Issue #541)
- nới write set quá hai đường · vượt 300 dòng thêm mà chưa xin ngoại lệ ADR-0044 **trước khi đẩy**
- viết dấu bỏ-qua-CI nguyên văn trong thông điệp commit, **kể cả khi trích dẫn**
- đọc `rc` qua pipe (`| tail` rồi `$?` là `rc` của `tail`)

## 8. DỪNG khi

- `ai-dang-giu ops/lease_publish_test.py` còn `rc=11` mà bạn cần sửa tệp ấy ⇒ **chờ**, báo chủ kho.
- Cần chạm tệp thứ ba ⇒ DỪNG, xin ngoại lệ **trước** khi đẩy.
- Không dùng được tham số tiêm để chạy N1–N4 trên `ubuntu-latest` ⇒ DỪNG và báo: đó là đường đo
  **duy nhất** còn lại.
- Một hình dạng lỗi lặp lần thứ **BA** ⇒ dừng, hỏi *"có nên làm việc này không"*, đừng hỏi *"vá thế nào"*.

## 9. Báo về cái gì

Handoff phải có: `numstat` thật so `d705623` · kết quả từng ca N1–N4 **kèm đột biến đã chạy và màu
nó đổi** · `rc` đọc trực tiếp của mỗi lệnh · và **khai thẳng thứ không đo được**, đừng giấu sau chữ
*"có thể"*.

Hai điều kho này sẽ soi kỹ, vì đã trả giá:

- **Đột biến bị giết ≠ bị giết ĐÚNG LÝ DO.** `t139` đang tự báo *"mutant chết vì lỗi VÔ CAN (tín
  dụng giả)"* ngay trong log CI hiện tại. Tín hiệu "assertion của ca đích" phải là thứ mã triển khai
  **không giả được** — một lớp ngoại lệ riêng, neo cả **tên ca** — chứ không phải chuỗi
  `AssertionError` mà bất kỳ `except` nào cũng viết ra được.
- **Vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba.** `_git_exe_toi_thieu` có **3** nơi gọi
  (`:1156` `:1218` `:1298`) và phép giải có **3** bước ứng viên. Tự liệt kê HẾT đường **trước**, cho
  mỗi đường một chốt, và khai thẳng chỗ nào là bộ TƯƠNG ĐƯƠNG thay vì đếm to lên.
