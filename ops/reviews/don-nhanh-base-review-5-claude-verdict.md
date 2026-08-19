Selftest `tl.py` chết đúng chữ ký nợ đã khai: `import cryptography` → `pyo3_runtime.PanicException` ở cuối lượt chạy (rc=0 của pipeline là do `tail` nuốt — bằng chứng là chữ ký trong output, không phải mã thoát). Lời khai nợ **đúng nguyên văn**, giữ nguyên. Mọi phép đo đã xong — HEAD không đổi, porcelain chỉ còn `?? nhiem_vu.txt` của harness. Tổng hợp verdict.

---

verdict: changes_requested
reviewed_sha: 12dd16ea6d92a177898a78fb9a547bda1d601dbb
assurance: same_provider_approved

Lượt này **không cấp điều kiện land**: §8 đòi cross-provider cho phạm vi workflow, `codex` hết quota, chủ kho chấp nhận sai lệch có ghi — verdict này chỉ là `same_provider_approved`, không thay được mức assurance bắt buộc.

## Danh sách đóng được của lượt 4

**F1: ĐÓNG. F2: ĐÓNG.** Tự dựng cả bốn đột biến trên bản sao tạm (mỗi con một thư mục riêng, vá khớp-chuỗi-đúng-một-lần, xác nhận khác bản sạch trước khi chạy — chống "đột biến chưa từng được chạy") và chạy trọn suite từng con:

| Đột biến | Người vá khai | Tôi đo | Ca đỏ |
|---|---|---|---|
| M12 `-ge`→`-eq` | 20/21, t19 | **20/21** | t19 ✓ |
| M16 so sánh chuỗi | 19/21, t19+t20 | **19/21** | t19, t20 ✓ |
| M13 mặc định→200 | 20/21, t20 | **20/21** | t20 ✓ |
| M13b mặc định→3 | 20/21, t20 | **20/21** | t20 ✓ |

Khớp từng ca đỏ với lời khai. Đột biến cũ vẫn chết: M10 bỏ chốt ⇒ **18/21** (t17,t19,t21) · M11 `-ge`→`-gt` ⇒ **19/21** (t17,t21) · M14 ⇒ **18/21** (t17,t19,t21) — riêng M14 định nghĩa gốc nằm trong verdict lượt 4 trên comment #55 mà container không đọc được (đường API bị chặn), tôi dựng lại theo gợi ý lượt 4 (`$js.Count`→`$prMo.Count`) và số khớp "M14 18/21"; khai rõ đây là bản dựng lại. Lời khai chú thích t21 cũng đo: nâng mặc định→2000 ⇒ **20/21** đỏ t21 ✓.

Câu 3 (ghim mặc định chặt tới đâu): **chặt tuyệt đối về giá trị so sánh.** Mặc định→1001 ⇒ 20/21 đỏ t21; →999 ⇒ 20/21 đỏ t20. Đại số của cặp: mọi D≤999 làm t20 đỏ (999 -ge D), mọi D≥1001 làm t21 đỏ (1000 < D) — không đột biến đổi-mặc-định nào thoát. Nhưng "chặt" chỉ phủ **ngưỡng so sánh**, không phủ **tham số `--limit` hỏi gh** — đó là finding bên dưới.

## Findings

### [P2] Đột biến sống sót thứ ba là một HỌ BỐN CON: toàn bộ dòng lệnh hỏi `gh` nằm ngoài mọi phép đo

`Dung-Gh-Gia` (don-nhanh_test.ps1) sinh gh giả **mù với argv** — in cùng một JSON bất kể được hỏi gì. Nó mô phỏng trạng thái (đúng doctrine kho) nhưng không mô phỏng **hợp đồng truy vấn**, nên mọi đột biến vào dòng gọi `gh` của script sống trọn. Đo được, cả bốn **21/21 xanh**:

- `--limit $TranPR` → `--limit 200` — với gh thật: trả đúng 200, `200 -ge 1000` không bao giờ nổ ⇒ chốt chạm-trần thành đồ trang trí, danh sách bị cắt im lặng, base ngoài 200 PR đầu không được giữ ⇒ xoá base của PR đang mở. Bất biến chịu lực "limit hỏi gh = ngưỡng so sánh" hiện **không có ca nào canh**.
- **Bỏ hẳn `--limit`** — tệ hơn: mặc định của `gh pr list` là **30**.
- `--state open` → `--state closed` — giữ base của PR đã đóng, bỏ rơi PR đang mở.
- `--json headRefName,baseRefName` → `--json headRefName` — **tái tạo đúng lỗ gốc mà cả PR #150 sinh ra để vá** ("Bản đầu chỉ đọc headRefName"), bằng một token, không ca nào đỏ: t1 vẫn xanh vì gh giả in đủ hai trường bất kể script đã thôi hỏi trường base.

Phân biệt với nợ đã khai `gh-phan-trang-that-chua-ai-do`: nợ ấy nói về **câu trả lời** của gh thật (không đo được vì proxy). Finding này nói về **câu hỏi** của script — đo được ngay trong container, và tôi đã đo.

**Gợi ý vá:**

1. **Vá ở đâu:** don-nhanh_test.ps1 — một dòng trong `Dung-Gh-Gia` (nơi duy nhất sinh gh giả, mọi ca hưởng chung) + chốt trong `t21` (ca duy nhất đi đủ bộ ba tham số với giá trị mặc định — đo "lời hỏi cuối cùng trước khi tin" đúng tại ca chạm trần).
2. **Vá thế nào:** gh giả ghi `"$@"` ra `argv.txt` cạnh nó (một dòng sh trong mảng `$dong`); t21 đọc tệp ấy và đòi đủ ba token `--state open`, `--limit 1000`, `--json headRefName,baseRefName`. Tôi đã chạy thử cơ chế này trên bản sao tạm: bản đúng giữ **21/21**, và **giết cả bốn** đột biến trên (mỗi con 20/21, đỏ t21).
3. **Ca test khoá:** chính t21 sau vá; bốn đột biến argv phải chết 20/21 đỏ t21 (đã đo đủ bốn). Kèm phản chứng cho chính chốt: gỡ ba dòng đòi argv ra thì `--limit 200` phải sống lại — không có phản chứng ấy thì không biết chốt đang đo argv hay đo thứ khác.
4. **Bản vá này có thể đẻ ra gì:** (i) đây là ghim theo **lời gọi** — thêm cờ chính đáng (vd `--repo`) sẽ làm t21 đỏ; đó là chủ ý (đổi câu hỏi gh là đổi hợp đồng, phải có người sửa test và nói lý do), nhưng cần ghi thẳng vào chú thích kẻo lượt sau tưởng đỏ oan; (ii) `-match` là regex — ba token hiện tại vô hại, token tương lai có `[` `(` phải escape; (iii) so **từng token** chứ đừng so nguyên dòng, kẻo chết vì khoảng trắng. Đường đắt hơn: gh giả **mô phỏng `--limit`** (cắt danh sách theo tham số nhận được) — mua thêm hành-vi-thật cho chính cơ chế cắt (t21 tự giết limit-mutants không cần so chuỗi), nhưng không phủ `--state`/`--json`; làm cả hai cũng được, riêng argv-log đã đóng lớp.

## Nợ khai báo

Nợ cũ: đã kiểm chỗ kiểm được, **không mục nào khai sai** — riêng `tl-selftest` nay có bằng chứng dương đầu tiên sau bốn lượt "chưa ai xác nhận": chạy trọn trong container này chết đúng chữ ký đã khai (`import cryptography` → `pyo3_runtime.PanicException`; lưu ý phép đo của tôi nối `tail` sau pipeline nên rc bị nuốt — bằng chứng là chữ ký trong output, không phải mã thoát). Lời khai giữ nguyên. Delta ngoài mã cũng kiểm: lease khớp băm prompt (`3aaa0f61…`, đúng cả bản `sua_lease`); `ops/uy-quyen-150-…` tự vô hiệu đúng luật của nó (neo `05568de`, head đã đổi) — nếu chủ kho muốn đi tiếp sau lượt này thì cần uỷ quyền mới neo SHA mới, và finding P2 ở trên nằm trước quyết định ấy.

Nợ mới khai thêm (đo được, dưới ngưỡng finding theo tiêu chí đóng băng):

- **t20 một mình xanh-vì-lý-do-sai khi danh sách rỗng.** Đột biến helper trả `@()` ⇒ **t20 vẫn xanh** (count 0 < 1000 ⇒ đi tiếp, rac bị xoá, rc=0); cái bắt là t21 (đỏ, suite 19/21). Tức "đọc được thật" hiện là thuộc tính của **cặp**, không của từng ca — t21 là điểm hỏng đơn của cả phép ghim. Gợi ý ngắn: thêm vào t20 một chốt dòng ra `cua 999 PR dang mo` (đã chạy thử: bản đúng 21/21, helper-rỗng làm t20 đỏ thật), hoặc đường hành-vi-thuần đắt hơn một chút: cho một PR trong danh sách trỏ base là nhánh thật rồi đòi nhánh ấy được giữ (cùng khuôn t14, không phụ thuộc câu chữ dòng in).
- **Hằng `999` của t20 không có gì tự canh.** Đột biến 999→998 sống 21/21, và combo (t20@998 + mặc định 999) cũng 21/21 — vế dưới của phép ghim nới đúng một đơn vị mà không ai thấy. Đã đo giới hạn thiệt hại: t20@998 vẫn giết M13 (20/21) ⇒ hồi quy thô vẫn bị chặn. Không đề xuất vá — test không tự canh được hằng của chính nó, chú thích "999 phải QUA, 1000 phải DỪNG" hiện có là đúng chỗ; khai để lượt sau khỏi tốn công đào lại.
- **`Nhieu-PR` có hai bẫy ngoài miền gọi hiện tại** (call site 10/999/1000 đều đúng, đo end-to-end): `Nhieu-PR 0` trả **2 phần tử** (`1..0` chạy xuống: pr/1, pr/0); `Nhieu-PR 1` bị unwrap thành hashtable trần, `.Count` = **2** (đếm KEY) — đúng họ bẫy mảng-đơn mà chính tệp ghi ở t9, hiện được biên `[object[]]` của `Dung-Gh-Gia` trung hoà. Gợi ý một dòng: guard `$So -lt 1` trả `@()` + một câu chú thích về ca 1 phần tử.
- **Chú thích t19 khai sai một vế:** "10/9 là cặp số nhỏ nhất phân biệt số học với chuỗi" — đo phản chứng: `'10' -ge '2'` cũng `False` trong khi `10 -ge 2` `True`, tức (10,2)…(10,8) đều phân biệt. Thứ nhỏ nhất thật là **đếm 10** (buộc 2 chữ số vs 1; mọi cặp một-chữ-số không phân biệt được — đo (9,2) hai kiểu cùng `True`). Gợi ý: sửa câu thành "10 là đếm nhỏ nhất phân biệt được; chọn trần 9 để sát biên". Kho này đo lời khai chú thích — chính người vá vừa đo lời khai t21.
- Đột biến pad-chuỗi (`{0:D9}` hai vế) sống 21/21 — **tương đương hành vi** trong miền với tới (đếm < 10⁹), không giết được bằng phản chứng hành vi và không cần giết. Khai để khỏi ai tính nó là lỗ.

## Phép đo đã chạy

Môi trường: tải PowerShell 7.4.6 linux-x64 (chmod +x đúng cảnh báo tarball thiếu bit exec), `TMPDIR=/dev/shm` — `/dev/shm` đúng là đã bị xoá sạch khi phiên khởi động, kiểm công cụ trước khi đọc số. Neo: HEAD = `12dd16e…` khớp lease; prompt snapshot sha256 khớp `prompt_sha256_required` (cả trên đầu nhánh); hai tệp scripts trong cây review khớp từng byte với `git archive HEAD`.

1. Baseline trên bản sao sạch: **21/21** (~15s).
2. Đột biến script (mỗi con một thư mục, vá có assert): M12 20/21 · M16 19/21 · M13 20/21 · M13b 20/21 · M10 18/21 · M11 19/21 · M14* 18/21 · 1001→20/21(t21) · 999→20/21(t20) · 2000→20/21(t21) · pad 21/21 · **limit-200 21/21 · limit-drop 21/21 · state-closed 21/21 · json-bỏ-base 21/21** (bốn con sống — finding P2).
3. Đột biến bộ test: helper N−1 ⇒ 20/21 (t21 bắt) · `0..$So` ⇒ 20/21 (t20 bắt) · bỏ `-TranPR` khỏi t19 ⇒ 20/21 (t19 tự bắt) · t20 999→998 ⇒ **21/21 sống** · combo 998+mặc-định-999 ⇒ **21/21** · combo 998+M13 ⇒ 20/21 (vẫn giết) · helper-rỗng ⇒ 19/21, **t20 xanh** (bằng chứng câu 4) · helper base→`ops/rac` ⇒ 20/21 (t20 ghim vệ sinh base).
4. Tiền-kiểm hai gợi ý vá trên bản sao tạm: chốt-dòng-999 cho t20 (21/21 đúng; đỏ thật khi helper rỗng) · argv-log + 3 chốt t21 (21/21 đúng; giết cả bốn đột biến argv, mỗi con 20/21 đỏ t21).
5. Probe trực tiếp: bảng số-học/chuỗi các cặp (10,9)(10,2)(9,2)('999','1000'); `Nhieu-PR` với −1/0/1/2/10.
6. Cổng vành đai, khớp hết số người vá: eol `ok=true checked=396 violations=0` · lease_publish **31/31** · golden rc=0 (core.abbrev=7 đã ghim repo-local) · release-verify `--strict` trên `git archive HEAD`: `ok=true, failed=[], file_count 179/179`, hash khớp · non-ASCII trong hunk chỉ là em-dash U+2014 ×6 (đúng văn phong, không đồng tự, không CRLF).
7. Read-only sau khi chạy: HEAD không đổi, `git status --porcelain` chỉ còn `?? nhiem_vu.txt` của harness; mọi đột biến chạy trong `/dev/shm/rv5`, không đụng cây review.

Nguồn có thẩm quyền của lượt này là tệp lease trên đầu nhánh; verdict này là bản trả lời theo đúng hợp đồng ấy.
