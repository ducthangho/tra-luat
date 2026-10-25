verdict: approve
reviewed_sha: 7574c39d98459c9caf1365a7dd092747335ae4e8

Review hoàn tất trên exact SHA trên: **không có finding P0–P3 của diff; N1–N4 đạt theo tiêu chí delta của spec**, gồm phản chứng 8999. N5/N6 thuộc phép đo của phiên điều phối, không tự nhận đã đạt.

- Packet: wp923 r1 / Issue #923 / PR #924; review class: sensitive.
- Base: `1a269f51120fd9b93bbf6a96a68d2840b7ac2b0e`.
- Head tree: `43853cd8bbcd1d25a982d8ba26e4c4e28533d633`.
- Reviewer: Codex, model family OpenAI; session `fd021cb7`; công cụ shell cục bộ qua API, transport machine. Không có biên nhận runtime trong bundle để tự chứng nhận model/effort hoặc assurance của hệ thống điều phối.
- Phạm vi: read-only đối với `cay-kho/`; phép thử/đột biến ở bản sao ngoài repository. Không commit/push/đăng GitHub.

## Đã đo

- `sha256sum SPEC.md` ⇒ `65db5e381ce9c7539f5bf9fb3b7d116ba3822a4914f3725e7a9ba98a484e4513`, đúng đặc tả đóng băng.
- `git -C cay-kho rev-parse HEAD` ⇒ exact SHA trên; `git status --short` rỗng.
- `git -C cay-kho diff --numstat 1a269f5 7574c39` ⇒ đúng 2 tệp, tổng 8 dòng thêm; `.ps1` chỉ đổi mặc định HanGiay và chú thích liền kề, giữ `ValidateRange(1, 86400)`. `diff.patch` trùng byte với diff tự dựng.
- N1: `python3 review-evidence/check_static.py` (PyYAML 6.0.3), `yaml.safe_load(git show base:.github/workflows/ci.yml) == yaml.safe_load(git show head:.github/workflows/ci.yml)` ⇒ **True**. Gọi chính `bam_gate_nhanh` / `bam_gate_registry` của module head: cả hai khớp hằng `BAM_GATE_NHANH` / `BAM_GATE_REGISTRY`. Bằng chứng chi tiết: `review-evidence/static.txt`.
- N2: lấy `git diff base head -- .github/workflows/ci.yml`, bỏ header `---/+++`, kiểm `line[1:].lstrip().startswith('#')` trên mọi dòng `-/+` ⇒ **True**, 5 dòng (2 bỏ, 3 thêm).
- N3: tìm được binary ngoài PATH tại `/root/.local/bin/actionlint`; `--version` ⇒ **1.7.7**. Xuất `ci.yml` base/head bằng `git show` vào `review-evidence/ci-{base,head}.yml`; chạy `/root/.local/bin/actionlint -color <tệp>` với cwd `cay-kho` ⇒ **base rc=0, head rc=0**, stdout/stderr rỗng. `shellcheck` **vắng** trên PATH. Chi tiết: `review-evidence/n3-results.json`.
- `./pwsh/pwsh -NoProfile -Command '$PSVersionTable.PSVersion.ToString()'` ⇒ **7.4.6**.

### N4 — chạy trọn ba lượt độc lập

Lệnh đã chạy từ thư mục rv: `python3 -u review-evidence/run_n4.py > review-evidence/n4-runner.log 2>&1`. Script tạo clone bằng `git clone --no-hardlinks --no-checkout`, checkout detached exact SHA, đòi `git status --porcelain=v1 --untracked-files=all` rỗng, rồi gọi **`<rv>/pwsh/pwsh -NoProfile -File .claude/dev/chay-cong-windows_test.ps1`** với cwd của từng clone và TMPDIR riêng. Script không lọc/bỏ ca nào. Muốn chạy lại script, cần các thư mục clone/tmp do lượt trước tạo chưa tồn tại.

| Cây | Mặc định | rc | Dòng tổng | t9 | Ca harness ghi `DO` | Thời gian |
|---|---:|---:|---|---|---|---:|
| Base `1a269f5` | 6300 | 1 | `chay-cong-windows: 32/36 dat` | ĐỎ | t9, t15, t30, t32 | 120,233 s |
| Head `7574c39` | 9000 | 1 | `chay-cong-windows: 33/36 dat` | ĐẠT | t15, t30, t32 | 121,637 s |
| Head đột biến | 8999 | 1 | `chay-cong-windows: 32/36 dat` | ĐỎ | t9, t15, t30, t32 | 121,213 s |

Output t9 nguyên văn:

```text
base: DO   t9 han mac dinh >= timeout-minutes cua job CI — HanGiay mac dinh 6300 s < 9000 s cua job CI
head: DAT  t9 han mac dinh >= timeout-minutes cua job CI
8999: DO   t9 han mac dinh >= timeout-minutes cua job CI — HanGiay mac dinh 8999 s < 9000 s cua job CI
```

**N4 ĐẠT:** `head_failed == base_failed - {'t9'}` ⇒ **True**; `mut8999_failed == head_failed | {'t9'}` ⇒ **True**. Thông báo ba ca còn lại trùng nguyên văn ở cả ba lượt. Bộ test không xanh toàn bộ: t15 không dựng được điều kiện trên nền này, t30/t32 đỏ có sẵn trên base (Q5).

Base/head sạch trước và sau test; bản đột biến xuất phát từ clone sạch head và chỉ thay `[int]$HanGiay = 9000,` thành `[int]$HanGiay = 8999,`, duy nhất một hunk. Tệp test không đổi giữa base/head/đột biến; sha256 `fbaa3a63ed9818f4768b5a1acb506145928b3ed3c348985d0092a72915599740`.

Bằng chứng tự đo: [base](review-evidence/n4-base.log), [head](review-evidence/n4-head.log), [8999](review-evidence/n4-mut8999.log), [kết quả lệnh/rc](review-evidence/n4-results.json), [so sánh delta](review-evidence/n4-comparison.json), [diff đột biến](review-evidence/mut8999.diff.patch). Không dùng ba log `n4-*.log` có sẵn ở gốc rv làm bằng chứng tự đo.

## Rà ngữ nghĩa chú thích

- Đã đọc các khối chú thích và quét `rg -ni 'timeout|trần|tran|phút|phut|hạn giờ|han gio' .github/workflows/ci.yml` trên head; đối chiếu các câu nói về trần cấp job với đối tượng YAML. Các job `gate`, `gate-cong-cu`, `gate-ops`, `gate-nhanh-manh`, `gate-registry`, `gate-packet-loop` đều 150; hai job gom là 10. Không thấy câu còn khẳng định sai trần HIỆN TẠI.
- `.github/workflows/ci.yml:734`: `git show 89591e1:.github/workflows/ci.yml` xác nhận lúc chú thích “Đo 16-08: 3,4 giây” được đưa vào (16-08-2026), job chứa bước này là `gate`, trần 25. Câu mới gọi đó là trần “lúc đo”, đúng; không nói `gate-ops` đã tồn tại khi ấy. `git show 6e09f4b -- .github/workflows/ci.yml` xác nhận `gate-ops` 60 → 150 ở #910 pha A.
- `.github/workflows/ci.yml:952–955`: giữ nguyên mốc #705 và câu 105 của mốc ấy, nối mốc #910 pha B 105 → 150. `git show a7da463 -- .github/workflows/ci.yml` xác nhận chuyển đổi này. `git show 6e09f4b -- .github/workflows/ci.yml` xác nhận trước pha A, `gate` là 60, `gate-packet-loop` là 120; do đó câu lịch sử mới sửa đúng cả chi tiết executor cũ đã gộp nhầm “vẫn 60”. Hiện tại cả ba là 150. Không viết lại các số đo/mốc #593/#705.
  Dòng 953 mà spec nêu vẫn còn nguyên văn, nhưng giờ nằm trong diễn tiến rõ #705 → #910: 105 là giá trị của mốc #705, không phải giá trị hiện tại. Cách nối câu có mốc chính là cách spec cho phép để cập nhật hiện tại mà giữ sự thật lịch sử.
- `.claude/dev/chay-cong-windows.ps1:66–71`: mô tả mới đúng: 9000 = 150 × 60, max động của mọi job `gate*` trên `1a269f5` là 150; `3818bd4` (#849) đưa `gate-cong-cu` 45 → 150; `6e09f4b` và `a7da463` đưa năm job được liệt kê còn lại lên 150. `t9` đã đo đỏ trên base và đạt trên head, đúng mô tả.

### Hai nhóm executor đề nghị giữ nguyên

- **Đồng ý giữ `.github/workflows/ci.yml:118–119`**: hai câu thuộc khối r391, ngày 29-08-2026, A5/đặc tả r3. `git show 7657bfd -- .github/workflows/ci.yml` cho thấy chính commit ấy thêm nguyên văn “Nâng tiếp 45 → 60 … Trần 60 … lần ĐO SAU” đồng thời đổi YAML 45 → 60. Đây là mô tả quyết định tại mốc lịch sử, không phải tuyên bố trần của head còn 60; sửa thành 150 sẽ bóp méo lịch sử mà spec yêu cầu bảo toàn.
- **Đồng ý giữ `.github/workflows/ci.yml:1029–1030` trên head** (1028–1029 trên base): `git show 9fcd49c -- .github/workflows/ci.yml` xác nhận mốc WP856/PR #866 60 → 120 và số đo run đi kèm. `6e09f4b` nâng 120 → 150 về sau mà không đổi mốc WP856. Không có câu #910 riêng ngay tại job này không biến câu có mốc cũ thành câu hiện tại; spec không bắt thêm lịch sử cho mọi job.

Lệnh lịch sử và diff đã lưu tại `review-evidence/timeout-history.txt` và `review-evidence/timeout-commits.txt`.

## KHÔNG ĐO ĐƯỢC

- **N5/N6**: theo prompt, phiên điều phối đo; lượt này không xác nhận check-run GitHub hay `ci_dang_ky_test.py` nguyên bộ. Không có evidence N5/N6 độc lập trong kết luận hiện tại.
- **t15 trên cả ba cây**: harness ghi `KHONG DO DUOC: khong dung duoc tep khong xoa duoc tren nen nay`. Không coi ca này đạt.

Handoff Q5 cho người điều phối #923: t30 thiếu các khóa `CI_DANG_KY_GOP_KQ`, `CONG_CU_TEST_GOP_CHE_DO`, `NHANH_DON_DUOC_DICH`, `NHANH_DON_DUOC_DICH_DU`, `NHANH_DON_DUOC_DICH_RA`; t32 lệch lệnh/gương/dấu vân CI. Hai ca đều đỏ với cùng thông báo ở base/head/8999; là nợ sẵn có, không vá trong wp923 r1. Chi tiết từng lỗi nằm trong ba log N4 liên kết ở trên.

## Findings

Không có finding P0/P1/P2/P3 của diff. Đồng ý cách phân loại và giữ nguyên hai nhóm lịch sử executor nêu, với lý do và bằng chứng Git ở trên. Nợ t15/t30/t32 được handoff theo Q5; không phát sinh ca đỏ mới ngoài write set do thay đổi này. Kiểm cuối: `git -C cay-kho rev-parse HEAD` vẫn là exact reviewed SHA; `git -C cay-kho status --porcelain=v1 --untracked-files=all` rỗng.
