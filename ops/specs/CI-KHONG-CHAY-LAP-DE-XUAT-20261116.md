# Đề xuất: không chạy lại bộ test dài cho cùng một nội dung vá (16-11-2026)

Tệp này là **báo cáo kèm đề xuất**, không phải đặc tả packet. Nó trả lời câu hỏi của chủ kho ngày 16-11-2026: bộ test
dài (`tl.py --selftest`, `packet_loop_test.py` và các bộ khác) có bị chạy lại nhiều lần cho cùng một nội dung vá không,
CI có chạy lại không, và nên xử lý thế nào. Đi kèm `ops/specs/CI-TOI-UU-THOI-GIAN-BAO-CAO-20261115.md` (báo cáo thời
lượng từng job) trong cùng PR.

Giờ ghi theo UTC (`Z`); giờ Việt Nam là UTC+7.

## 1. Trả lời ngắn

CI **có** chạy lại. Mỗi lần đẩy lên PR, mỗi lần gọi `workflow_dispatch`, và thêm một lần nữa trên `master` ngay sau
khi merge, `ci.yml` chạy lại toàn bộ: `tl selftest`, `packet-loop selftest`, tám mảnh `gate-cong-cu`, `gate-ops`,
`gate-registry`. CI không nhớ kết quả cũ theo nội dung; lượt nào cũng chạy từ đầu.

Đo trên 147 PR land từ 01 đến 15-11 (79 PR đi làn đầy đủ):

- **278** lượt đầy đủ trên PR và `workflow_dispatch` (trung vị 2 lượt mỗi PR, nhiều nhất 25), cộng **71** lượt đầy đủ
  trên `master` sau merge. Tổng khoảng **82.800 phút runner** trong 15 ngày.
- Phần chạy lại **đúng nội dung đã xanh**: 25 lượt `master` có cây trùng cây PR đã xanh (6.509 phút) và 31 lượt PR chạy
  lại sau khi cùng nội dung đã xanh (7.405 phút). Cộng lại khoảng **13.900 phút, 17 %**.
- Phần lớn còn lại là chạy cho **nội dung mới** (bản vá đổi, hoặc master đã trôi nên cây merge đổi). Không bỏ được bằng
  cách "nhớ kết quả"; chỉ giảm được bằng cách làm mỗi lượt rẻ hơn (song song hoá) hoặc chỉ chạy bộ test mà thay đổi
  chạm tới (bộ chọn theo phụ thuộc).

## 2. Phép đo

### 2.1 Mẫu và cách phân loại

- PR: mọi PR merge có `merged_at` trong `[2026-11-01T00:00Z, 2026-11-16T00:00Z)`, 147 PR. Tải lúc `2026-11-16`, REST qua
  `gh api` (`pulls?state=closed`, `actions/workflows/ci.yml/runs?event=…&branch=…`, `runs/<id>/attempts/<n>/jobs`).
- Gán lượt cho PR: lượt `pull_request` có `created_at` trong `[PR.created_at, merged_at]`; lượt `workflow_dispatch` từ
  2 ngày trước khi mở PR tới lúc merge. Tên nhánh bị **dùng lại** cho nhiều PR (vd. một nhánh `ccr-…` mở 5 PR), nên cửa
  sổ dưới còn bị chặn bởi lúc PR trước trên cùng nhánh merge. Lượt `push` master gán theo `head_sha == merge_commit_sha`.
- Làn đầy đủ: lượt có job `gate-cong-cu (…)` không `skipped`. Phút runner = tổng `completed_at − started_at` của mọi job
  không `skipped`, mọi attempt.
- "Cùng nội dung vá": cùng SHA, hoặc cùng `git patch-id --stable` của `git diff $(merge-base M^1 S) S`, với `M^1` là
  master ngay trước merge. (Bản đầu của phép đo dùng `origin/master` làm gốc và SAI: sau merge mọi commit PR đều là tổ
  tiên của master nên diff rỗng và mọi lượt bị gộp thành "cùng nội dung". Đã sửa trước khi lấy số.)
- "Cây master trùng cây PR": lượt PR xanh cuối có `head_sha` bằng head lúc merge và master lúc lượt ấy chạy bằng
  `M^1`. Kiểm chéo bằng dòng `HEAD is now at … Merge <head> into <base>` trong log checkout của job `gate` cho 8 PR
  (4 trùng, 4 trôi): khớp 8/8.

### 2.2 Kết quả

| nhóm (làn đầy đủ, PR + `workflow_dispatch`) | lượt | phút runner |
|---|---|---|
| xanh | 139 | 37.737 |
| đỏ | 15 | 4.725 |
| bị huỷ giữa chừng (lượt mới hơn thay chỗ, `cancel-in-progress`) | 116 | 19.330 |
| attempt cũ của lượt được chạy lại | 8 | 1.548 |
| **cộng** | **278** | **63.340** |
| `master` sau merge, làn đầy đủ | 71 | 19.470 |

Chạy lại trên nội dung **đã xanh**:

| trường hợp | lượt | phút runner | trong đó `gate-packet-loop` |
|---|---|---|---|
| PR: cùng SHA với một lượt đã xanh (8 xanh, 3 bị huỷ) | 11 | 3.147 | 1.055 |
| PR: SHA khác nhưng cùng patch với lượt đã xanh, vd. cập nhật nhánh theo master (13 xanh, 6 bị huỷ, 1 attempt cũ) | 20 | 4.258 | 1.095 |
| `master` sau merge, cây trùng cây lượt PR xanh cuối | 25 | 6.509 | — |

Lượt `master` sau merge của 79 PR đầy đủ: **25** trùng cây, **44** master đã trôi giữa lượt PR xanh cuối và lúc merge
(9.167 phút), 10 không đo được. Tức là với khoảng **64 %** số merge đo được, cây vào master **chưa từng được test** ở
lượt PR nào; lượt `master` là lần test đầu tiên của cây ấy. Lượt đó không thừa, và không được bỏ.

Số nội dung khác nhau mỗi PR (đếm patch-id): 37 PR một nội dung, 19 PR hai, 10 PR ba, 4 PR bốn, 9 PR từ năm trở lên.

Hiệu quả của luật "review offline, không đẩy giữa các revision" (từ 07-11):

| giai đoạn (theo `merged_at`) | PR đầy đủ | lượt đầy đủ / PR | nội dung / PR | phút runner / PR |
|---|---|---|---|---|
| trước 08-11 | 59 | 3,9 | 2,8 | 849 |
| từ 08-11 | 20 | 2,4 | 2,1 | 662 |

Bộ chọn theo tệp, cận trên: trong 88 PR có lượt đầy đủ (đếm trước khi lọc theo cửa sổ thời gian), **74 PR (84 %)** không
đổi tệp `.claude/dev/packet_loop*`, 61 PR (69 %) không đổi gì dưới `.claude/dev/`. Mọi PR ấy vẫn chạy
`gate-packet-loop` (trung vị 91 phút tường mỗi lượt theo báo cáo 15-11). Đây chỉ là **cận trên**: `packet_loop_test.py`
còn đọc tệp ngoài thư mục ấy (adapter, protocol, bảng ADR), nên tập phụ thuộc thật lớn hơn.

### 2.3 Phía máy cục bộ và review

Không có số đo tự động cho lượt chạy cục bộ. Quan sát trong phiên executor của #1321 và #1322 (15→16-11):

- Reviewer Codex **không** chạy lại toàn bộ bộ test; họ chạy ca đích (`--mot-ca`), lặp đột biến cụ thể, và đọc log chạy
  trọn executor đã nộp (`VERDICT` lượt 1 của #1322). Cách này đúng với §10.1.
- Executor chạy trọn trên CI qua `workflow_dispatch` ở nhánh đo tạm, mỗi revision **ba** lượt vì đặc tả đòi so ba chế độ
  (`N=1`, `N=4`, mặc định). Với `packet_loop_test.py`, `N=1` mất khoảng 130 phút tường; hai lượt kia 35–48 phút.
- Chạy trọn cục bộ trên Windows chậm hơn CI nhiều lần: `packet_loop_test.py` tuần tự 1–2 giờ, và (ghi nhận 09-08, chưa
  đo lại) `tl.py --selftest` trên 10 phút so với khoảng 94 giây trên `ubuntu-latest`, vì các nhịp lùi `[gas-retry]` khi
  chạy không mạng.

## 3. Vì sao chạy lặp

1. **CI không nhớ theo nội dung.** Cơ chế tái dùng duy nhất (`gate_lifecycle.py`, artefact `gate-evidence-<OS>-<attempt>`)
   chỉ phủ `tl selftest`, chỉ sinh ở `push`/`workflow_dispatch`, và chỉ người review đọc nó. Bản thân CI không bao giờ
   bỏ một bước vì đã có kết quả dương cho cùng cây.
2. **Lượt `master` sau merge là bắt buộc cho `landed`** (protocol §10.2: "hậu-merge gate xanh"). §10.1 hàng T4 đã cho
   phép "reuse duy nhất evidence T3 khi toàn bộ exact identity khớp", nhưng chưa có đường nào thực hiện việc đó, và
   identity hiện đòi cả SHA (merge commit luôn có SHA mới dù cây trùng).
3. **Ruleset không đòi nhánh cập nhật theo master trước khi merge**, nên 64 % số merge vào master một cây chưa test. Đó
   là lý do không thể đơn giản bỏ lượt `master`.
4. **Chưa có bộ chọn theo phụ thuộc.** Đổi nội dung là chạy lại mọi bộ, kể cả bộ thay đổi không chạm tới. §10.1 đòi
   shadow 2–4 tuần trước khi bật; đặc tả `CI-REGISTRY-DOT-BIEN-THEO-DIFF-r1` từng bác phương án "bỏ nguyên bộ theo diff"
   vì bảng phụ thuộc gõ tay đã sai ba lần (#245) — bảng phải do máy dựng.
5. **Quy trình.** `CLAUDE.md` §Quy trình sửa code bước 4 ghi "`python scripts/tl.py --selftest` (phải N/N…)" sau mỗi
   lần sửa, lệch với §10.1 (T0 chỉ cần test trực tiếp; full một lần cho mỗi identity). Đặc tả đòi so nhiều chế độ chạy
   ở mọi revision nhân số lượt chạy trọn lên ba.

## 4. Đề xuất, xếp theo thứ tự nên làm

### Đ1 — Quy trình: mỗi revision đóng băng chỉ một lượt chạy trọn (không đổi mã CI)

- **Executor**: sau mỗi lần vá chỉ chạy ca đích, đột biến của nó và đối chứng (`chay_suite(chi_chay=…)`, `--mot-ca`,
  `_mot_dot_bien`). Chạy trọn **một lần** khi đóng băng revision để giao review, và chạy trên CI (nhánh đo tạm +
  `workflow_dispatch`), không chạy trên Windows cục bộ.
- **Reviewer**: không chạy lại toàn bộ; kiểm log chạy trọn của executor hoặc CI theo băm, SHA, cây, lệnh, dấu dương, rồi
  chạy probe đối nghịch và ca đích. Đưa yêu cầu này vào mẫu prompt của `.claude/skills/cross-review/SKILL.md`.
- **Đặc tả** (`soan-spec`): tiêu chí so nhiều chế độ chạy (vd. `N=1` với `N=4`) chỉ đo ở revision cuối; revision giữa
  chỉ chạy chế độ mặc định. Riêng #1321, mỗi revision giảm từ ba lượt (130 + 48 + 35 phút tường) xuống một (35 phút).
- Sửa câu ở `CLAUDE.md` bước 4 cho khớp §10.1.

Tiết kiệm: không đo được bằng số trên CI (phần lớn là lượt cục bộ và lượt đo tạm). Rủi ro thấp: §10.1 đã viết sẵn
nguyên tắc "một full oracle trên mỗi exact identity"; đề xuất này chỉ đưa nó vào chỗ người làm việc đọc.

Cần chủ kho: duyệt nội dung câu sửa. `CLAUDE.md` và `.claude/skills/**` là bề mặt quản trị, sửa qua packet.

### Đ2 — CI tái dùng kết quả theo cây (packet `sensitive`, đổi `ci.yml`, cần E5)

- Mỗi job nặng, khi xanh, tải lên một biên nhận nhỏ: job, OS, **cây đã checkout**, băm blob của `ci.yml`, phiên bản ảnh
  runner, phiên bản Python, lệnh, `rc`, dấu dương, băm đầu ra. Tên artefact chứa cây để tra được.
- Đầu job nặng: tìm biên nhận xanh cùng (job, OS, cây, blob `ci.yml`, Python) từ một lượt **của chính kho** (không phải
  fork; kho công khai nên PR từ fork cũng tải artefact lên được). Có thì bỏ các bước nặng, in `TÁI DÙNG run <id>
  attempt <n>`, vẫn báo xanh kèm dấu dương, và tải lên biên nhận trỏ về lượt gốc. Không đọc được, thiếu, lệch, hay lỗi
  ⇒ chạy đủ (fail-closed).
- Phủ: 25 lượt `master` trùng cây (6.509 phút) và phần lượt PR chạy lại trên nội dung đã xanh (7.405 phút). Lượt PR
  chạy lại chỉ trùng cây khi master không đổi giữa hai lượt; tỷ lệ ấy chưa đo. Tiết kiệm **ít nhất 6.509 phút runner mỗi
  15 ngày (8 %)**, tối đa khoảng 13.900 phút (17 %), và bỏ khoảng 92 phút chờ lượt `master` cho khoảng một phần ba số
  merge (25/79).
- Cần ADR: cho phép bằng chứng hậu-merge của `landed` là biên nhận tái dùng khi **cây** trùng (không đòi SHA trùng), và
  chỉ rõ cách điền bốn mốc §10.2.2 (Run, Checkout, Workflow definition, Gate output) cho lượt tái dùng.
- Rủi ro: (a) biên nhận giả — phải kiểm lượt gốc là của kho này, đúng đường dẫn và blob `ci.yml`, đúng sự kiện; (b) ảnh
  runner đổi giữa hai lượt cùng cây — ghi phiên bản ảnh và chỉ tái dùng khi trùng; (c) test chập chờn — một lần xanh
  được dùng lại thay vì chạy thêm lần nữa, nên lỗi chập chờn lộ ít hơn.

### Đ3 — Đòi nhánh cập nhật theo master trước khi merge: chưa nên làm, đo trước

Nếu bật (ruleset `strict` hoặc merge queue), lượt PR xanh cuối luôn test đúng cây sẽ vào master, nên Đ2 phủ được cả 71
lượt `master` (19.470 phút). Nhưng mỗi lần master đổi, mọi PR đang mở phải cập nhật và chạy lại trọn: với khoảng 10
merge mỗi ngày, số lượt PR có thể tăng nhiều hơn số lượt `master` bỏ được. Merge queue cần kho thuộc organization. Đề xuất
đo trước: đếm số lần master đổi trong lúc mỗi PR đang chờ (dữ liệu §2 đủ để đếm), rồi mới quyết.

### Đ4 — Bộ chọn theo phụ thuộc do máy dựng, chạy shadow trước (theo §10.1)

- Mỗi bộ nặng khai tập đầu vào **do máy dựng** (theo dõi tệp mà bộ thật sự mở/nạp khi chạy), không gõ tay.
- Chạy shadow 2–4 tuần: CI vẫn chạy đủ, nhưng ghi "bộ chọn sẽ bỏ bộ X" kèm kết quả thật của X. Chỉ bật khi không lần nào
  bộ chọn bỏ một bộ mà bộ ấy đỏ.
- Cận trên: `gate-packet-loop` trên PR và `workflow_dispatch` tốn 13.131 phút trong 15 ngày; 84 % PR không đổi tệp
  `packet_loop*`. Số tiết kiệm thật chỉ biết sau shadow.
- Rủi ro: bỏ sót phụ thuộc ngầm (đọc tệp qua đường dẫn ghép, biến môi trường, git log). Đó là lý do phải shadow và phải
  do máy dựng.

### Đ5 — Làm mỗi lượt cần thiết rẻ hơn (đang làm)

#1321 (`packet_loop_test.py` chạy 4 làn) và #1322 (`ci_provenance_test.py` song song). Đo trên `ubuntu-latest` ở nhánh
đo tạm: job chạy `packet_loop_test.py` từ trung vị 91 phút xuống 34,5–39 phút (bản còn lỗi gom làn, xem dưới);
`ci_provenance_test.py` từ 1.307 giây xuống 368 giây. Áp lên mọi lượt còn phải chạy, kể cả lượt `master` sau merge.

Lỗi gom làn của #1321 (run 43693100060): ở chế độ 4 làn và mặc định, báo cáo `WP1174_NATIVE_REPORT_V1` ra
`native_probe: {}` và `TỔNG: 1 lỗi`, trong khi nền 1499/1499 đạt. Ca `wp1174_profile_native_linux` đặt biến toàn cục
`_WP1174_NATIVE_FACTS` mà `_carrier1174` của tiến trình cha đọc; chạy trong làn con thì biến ấy không về tới cha. Bản sửa
cho ca ấy chạy ở cha sau khi các làn xong, kèm ca tự kiểm và ba đột biến; chưa đo lại trên CI.

### Đ6 — `tl.py --selftest` cục bộ trên Windows (đo lại trước)

Nếu số đo 09-08 còn đúng, phần lớn thời gian cục bộ là ngủ chờ trong các nhịp lùi `[gas-retry]` khi chạy không mạng. Khi
`TL_SELFTEST_NO_NET` bật, có thể cho nhịp lùi bằng 0. Việc đầu tiên là đo lại trên `master` hiện tại; chưa đo thì
chưa mở packet.

## 5. Thứ tự đề xuất

1. Đ1 ngay (sửa chữ, không đổi mã).
2. Hoàn tất Đ5 (#1321, #1322 đang review).
3. Đ2: soạn đặc tả và ADR đi kèm; cần chủ kho duyệt (E5).
4. Đ4: soạn đặc tả shadow sau khi Đ2 chạy ổn.
5. Đ3 và Đ6: đo trước, quyết sau.

## Phụ lục A — Lệnh và script

Script (thư mục nháp của phiên, không vào kho): `lap.py` tải dữ liệu, `phan_tich_lap.py` phân loại. Lệnh REST:

```
gh api "repos/ducthangho/tra-luat/pulls?state=closed&per_page=100&sort=updated&direction=desc&page=<n>"
gh api "repos/ducthangho/tra-luat/actions/workflows/ci.yml/runs?event=<pull_request|workflow_dispatch>&branch=<ref>&per_page=100"
gh api "repos/ducthangho/tra-luat/actions/workflows/ci.yml/runs?event=push&head_sha=<merge_commit_sha>&per_page=20"
gh api "repos/ducthangho/tra-luat/actions/runs/<id>/attempts/<n>/jobs?per_page=100"
gh api "repos/ducthangho/tra-luat/actions/jobs/<job_id>/logs"      # kiểm chéo cây cho 8 PR
```

Phân loại nội dung: `git patch-id --stable` trên `git diff $(git merge-base <merge_commit>^1 <sha>) <sha>`. Tám PR kiểm
chéo bằng log checkout: #1114, #1116, #1115, #1130 (trùng cây) và #1055, #1080, #1092, #1091 (master đã trôi).
