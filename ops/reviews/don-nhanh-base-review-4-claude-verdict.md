Mọi phép đo đã xong. Tổng hợp verdict theo đúng định dạng yêu cầu.

---

```
verdict: changes_requested
reviewed_sha: 05568de6ad054a5f0c9991ecac7e38805d1227c3
assurance: same_provider_approved
```

Lượt này là **phản biện bổ sung cùng nhà cung cấp** — theo §8 và theo lease (`khong_cap_dieu_kien_land: true`), kết luận dưới đây **không cấp điều kiện land** cho #150, bất kể verdict.

## Danh sách đóng được của lượt trước

**Nợ `--limit`: ĐÓNG về hành vi của SCRIPT** — với phép thử đã chạy (pwsh 7.4.6 tải từ GitHub release, TMPDIR=/dev/shm, kiểm `PowerShell 7.4.6` in ra TRƯỚC khi đọc số):

- Bộ 18 ca trên HEAD `05568de`: **18/18 đạt** — khớp số người vá.
- Bản `bfeedfc` + bộ test HEAD: **16/18, đỏ đúng t17+t18** — cặp ca mới có bằng chứng dương.
- M10 bỏ chốt: **17/18 đỏ t17** · M11 `-ge`→`-gt`: **17/18 đỏ t17** — cả ba con số đột biến của người vá tái lập khớp từng số.
- Biên đo đủ **bốn phía**: `=trần` từ chối (t17), `trần−1` vẫn xoá đúng (t18), `trần+1` từ chối + remote không đổi (ca tự dựng p19: 3 PR, `-TranPR 2` → rc=13), `10 vs trần 9` từ chối (p28 — ghim so sánh SỐ học, không phải chuỗi). Không chặn oan: 0 PR + `-TranPR 1` → rc=0 và xoá rác đúng (p23).
- Trả lời câu 4: `$js.Count` = số phần tử mảng JSON `gh` in ra = **số PR** — đúng đại lượng `--limit` giới hạn. Đo ba dạng trên pwsh 7.4.6: `'[]'` → AutomationNull → `@()` đếm **0** (không dính bẫy `@($null)`=1); 1 phần tử → PSCustomObject bọc lại = **1**; 2 PR chung base → `js.Count=2` ≠ `prMo.Count=3`. t18 là bằng chứng hành vi chốt so đúng đại lượng (nếu so `$prMo.Count`=5 ≥ 4 thì t18 phải rc=13, thực đo rc=0); M14 đo chiều ngược lại.
- Trả lời câu 2: **không giá trị `-TranPR` nào làm cổng lỏng hơn** — `0`/`1`(có PR)/`-5` → rc=13, không xoá gì (kể cả khi 0 PR: `0 -ge 0`, `0 -ge -5` đều từ chối); `2147483647` → hành xử y mặc định (giữ base, xoá rác); `2147483648`/`abc` → lỗi binding rc=1, script chưa chạy, remote không đổi. Không có P1. Dry-run chạm trần: rc=0 + in `cham tran` + `CANH BAO … CHUA loai base` (p29) — nhất quán hành vi dry-run sẵn có khi không đọc được PR, không phải hồi quy.

Lập luận "nâng số chỉ DỜI biên, chốt mới ĐÓNG lớp" đứng vững qua mọi phép đo — nhưng chốt hiện chỉ được test ghim từ MỘT phía biên (xem Findings).

## Findings

**F1 — P2, đột biến SỐNG SÓT (`scripts/don-nhanh_test.ps1`): cặp t17/t18 pin biên chỉ từ phía dưới; hai đột biến làm chốt fail-open sống sót 18/18.**
- **M12** `-ge`→`-eq`: **18/18 đạt** (t17: 3 -eq 3 vẫn ném; t18: 3 -eq 4 vẫn qua). Không phải khác biệt "chỉ xảy ra khi gh trả quá limit": dưới M12, đường fail-open kích hoạt được **bằng chính tham số công khai** — đo được `-Xoa -TranPR 0` với 1 PR mở: rc=0 và **xoá thật** (p20 đỏ: "rc=0, doi 13"), trong khi HEAD từ chối. Suite probe giết M12 ở 6 ca (24/30: p19 p20 p22 p24 p24b p28).
- **M16** `($js.Count -ge $TranPR)`→`("$($js.Count)" -ge "$TranPR")` (ép kiểu chuỗi — gợi ý số 3 của prompt): **18/18 đạt**, chỉ chết ở p28 (29/30): đếm 10 vs trần 9, so chuỗi cho `"10" < "9"` → rc=0 dù vượt trần.
- Cách đóng, rẻ: thêm **một** ca kiểu p28 (10 PR giả, `-TranPR 9` ⇒ rc=13 + remote không đổi) — giết cả M12 lẫn M16 trong một ca; p19 (3 PR, trần 2) là bản tối thiểu chỉ giết M12. Ca này thuộc đúng kỷ luật của kho: nghĩ ra mà không nằm trong `don-nhanh_test.ps1` thì nó không tồn tại.

**F2 — P3, đột biến SỐNG SÓT: mặc định `TranPR = 1000` không được ghim.**
- **M13** default 1000→**200** (hồi quy đúng trần cũ): **18/18 đạt**. **M13b** →**3**: cũng **18/18**. Mọi ca đa-PR đều truyền `-TranPR` tường minh nên nửa "nâng trần 200→1000" của bản vá không có bằng chứng dương nào trong bộ test (chỉ default→1 mới bị t1 bắt). Mức P3 vì chiều sai này là fail-close-hơn, không mở lỗ; nhưng nó nghĩa là tiêu đề của bản vá có thể bị lùi âm thầm.

Hai đột biến người vá muốn thử đã bị bắt (đối chứng rằng suite không mù toàn phần): **M14** `$js.Count`→`$prMo.Count` tại chỗ → 17/18 đỏ t17 (`$prMo` còn `@()` ở điểm chốt — chốt chết hẳn); **M15** dời chốt xuống SAU `$doDuocPR = $true` → 17/18 đỏ t17 (throw bị catch nhưng `$doDuocPR` đã true → xoá tiếp) — đồng thời chứng minh **vị trí** chốt hiện tại (trước `$prMo`/`$doDuocPR`) là bắt buộc, không phải tình cờ.

Không tìm thấy hồi quy (16 ca cũ xanh nguyên trạng ở mọi lần chạy HEAD; dry-run/`-BoQuaLopPR` không đổi hành vi) và không lỗ an ninh MỚI trong mã HEAD.

## Nợ khai báo

- Delta `bfeedfc..05568de` ngoài hai tệp `scripts/`: `ops/reviews/**` (4 verdict + biên nhận + README), cùng lease/prompt của chính lượt này trên đầu nhánh — không phải mã, không xét theo phạm vi đóng băng.
- Hành vi `gh` THẬT với `--limit 0`/âm/`2147483647` chưa ai đo (proxy chặn `gh` — xác nhận nợ "gh phân trang thật" đã khai; phần giá trị lạ này là mở rộng nhỏ của cùng nợ). Phía script đã đo đủ.
- `tl selftest`: lượt này THỬ đo — chết ngay khi import `cryptography` (`pyo3_runtime.PanicException`) trong container này, không có dòng N/N ⇒ lời khai "chưa ai đo" vẫn ĐÚNG. Ghi thêm: lần đo đầu của tôi in "rc=0" — đó là rc của `tail` sau pipeline (đúng bẫy `$?` CLAUDE.md đã ghi), không phải bằng chứng.
- 12 ca probe (p19–p29) và 4 đột biến mới (M12/M13/M14–M16) nằm trong scratchpad phiên review, KHÔNG trong cây — là bằng chứng của lượt này, muốn thành chốt phải được người vá đưa vào suite.
- Môi trường: tarball PowerShell 7.4.6 giải nén ra `pwsh` **thiếu bit exec** (rc=126) — phải `chmod +x`; không phải `/dev/shm` noexec (mount chỉ `rw,relatime`). Ghi lại kẻo lượt sau chẩn đoán sai.
- Trong worktree phiên review, `release-verify --strict` đỏ (rc=2) vì `extra_files: ["nhiem_vu.txt"]` — tệp nhiệm vụ do harness đặt vào, untracked; trên cây sạch `git archive HEAD` thì xanh (delta so nền = 0, xem Phép đo).

## Phép đo đã chạy

Công cụ kiểm TRƯỚC khi đọc số: `pwsh 7.4.6` (tải release linux-x64, chmod +x, chạy in `PowerShell 7.4.6`), git 2.43.0 tại `/usr/bin/git` (PATH thu hẹp của harness thấy được), TMPDIR trong `/dev/shm`.

| Phép đo | Kết quả | Đối chiếu số người vá |
|---|---|---|
| Neo `git rev-parse HEAD` | `05568de…` khớp lease | ✔ |
| SHA-256 prompt snapshot vs `ops/prompts/…review-4…md` trên đầu nhánh | `1906eabd…` khớp | ✔ |
| `git diff bfeedfc..HEAD -- scripts/` | đúng 2 tệp, +27/−2 và +43 | ✔ |
| Bộ 18 ca trên HEAD | **18/18 đạt**, rc=0 | ✔ 18/18 |
| `bfeedfc` + test HEAD (bản sao tạm) | **16/18**, đỏ t17+t18 | ✔ |
| M10 bỏ chốt | **17/18**, đỏ t17 | ✔ |
| M11 `-ge`→`-gt` | **17/18**, đỏ t17 | ✔ |
| M12 `-ge`→`-eq` | **18/18 — SỐNG SÓT**; probe 24/30 (đỏ p19 p20 p22 p24 p24b p28) | phát hiện mới |
| M13 default→200 · M13b default→3 | **18/18 — SỐNG SÓT** (cả hai) | phát hiện mới |
| M14 `$js.Count`→`$prMo.Count` | 17/18 đỏ t17 — bị bắt | phát hiện phụ: chốt chết vì `$prMo=@()` |
| M15 chốt sau `$doDuocPR=$true` | 17/18 đỏ t17 — bị bắt | vị trí chốt là bắt buộc |
| M16 so sánh chuỗi | **18/18 — SỐNG SÓT**; probe 29/30 (đỏ p28) | phát hiện mới |
| Probe 30 ca trên HEAD (18 cũ + p19–p29) | **30/30 đạt**; QUAN_SAT: p21 rc=13 · p23 rc=0 xoá rác · p26 rc=1 · p27 rc=1 · p29 rc=0 | Q1/Q2 đóng |
| Micro-probe `ConvertFrom-Json` (pwsh 7.4.6) | `[]`→0 · 1 phần tử→1 · 2 PR chung base: js=2 vs prMo=3 | Q4 đóng |
| `.githooks/eol_policy.py --all --json` | ok=true, **checked=393**, violations=[] | ✔ |
| `ops/lease_publish_test.py` | **31/31 đạt**, rc=0 | ✔ |
| `scripts/tl.py golden-test --json` (`core.abbrev=7` sẵn) | rc=0, ok=true | ✔ |
| `release-verify --strict` trên cây sạch HEAD (git archive → scratchpad) | **ok=true, 179/179, failed=[]**, rc=0; trong worktree review: rc=2 chỉ vì `nhiem_vu.txt` của harness | ✔ ok=true · failed=0 · file_count 179 |
| `tl.py --selftest` | chết import `cryptography` (pyo3 panic) — **KHÔNG ĐO ĐƯỢC** | nợ khai đúng |

Nguồn có thẩm quyền của lượt này là tệp lease trên đầu nhánh `ops/don-nhanh-giu-base-pr` (đã đọc bằng `git show`, các trường khớp: `reviewed_sha_required`, phạm vi 2 tệp, `assurance_target: same_provider_approved`).
