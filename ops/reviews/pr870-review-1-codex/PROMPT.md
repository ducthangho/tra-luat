# Cross-review PR ducthangho/tra-luat#870 — reviewer: codex

Bạn là reviewer CHỈ ĐỌC + ĐO. KHÔNG sửa `cay-kho/`, KHÔNG push, KHÔNG gọi mạng (sandbox không có mạng).
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`.

## Đối tượng
- `reviewed_sha`: `b38fce83d0e97981012072ca2a2023ac726e5b2e` (head PR #870), base `9e9a74b2a396ef458d25c51a5563efafbb45ba0c` (= origin/master).
- Diff: `diff.patch`, `numstat.txt` (chỉ `CLAUDE.md`, +21/-9). Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng reviewed_sha; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`). Thứ định danh tệp là BĂM/SHA, không phải tên nhánh.
- PR sửa bài học "HỎI CHỖ TIỆN TAY…" điểm (c) trong `CLAUDE.md`: thay câu cũ "master chạy CẢ ubuntu LẪN windows" bằng mô tả ma trận `os` hiện tại của `.github/workflows/ci.yml`, kèm ngày đo, run id, đường dẫn readback, và mô tả Windows trên master qua `launcher-windows.yml`.

## Nhiệm vụ chính: ĐO LẠI TỪNG KHẲNG ĐỊNH của đoạn mới (không soát chính tả)
Đoạn mới nằm trong `cay-kho/CLAUDE.md` (tìm `(c) Ma trận`). Mỗi khẳng định có số/SHA/run id/đường dẫn/điều kiện đều phải kiểm bằng lệnh chạy được trong `cay-kho/`. Ví dụ (KHÔNG phải danh sách đủ — mỗi khẳng định bạn tìm ra mà danh sách này bỏ sót được tính là finding):
1. Biểu thức output `os` của job `chuan-bi` trong `ci.yml` tại reviewed_sha: điều kiện nào cho `windows-latest`? push master có vào nhánh đó không?
2. "từ packet #548 … bỏ vế `github.ref == 'refs/heads/master'`": dùng `git log -S`/`git show` tìm commit thật đã bỏ vế ấy khỏi output `os` (gợi ý: `d1258fe`), xác nhận nó đúng là vế master của MA TRẬN, không phải của chỗ khác.
3. Run 39354156843: `ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json` — đếm job, nhãn `labels`, `head_sha`/`run_id` trong tệp có khớp `3a3a3ca` và 39354156843 không; ngày 20-10-2026 có khớp dữ liệu không.
4. Commit `3f6c694` có chứa đúng chuỗi `jobs: '23/23 success (gom windows)'` không.
5. PR #859 / comment `r4323607674` / PR #865: tìm dấu vết trong kho (`git log --all --grep`, `ops/`), nói rõ cái nào ĐO ĐƯỢC trong sandbox và cái nào KHÔNG ĐO ĐƯỢC (không mạng).
6. `launcher-windows.yml`: trigger push master có `paths:` gì; ma trận gồm gì cho push; PR có `types: [..., labeled]` không; `if:` của job.
7. "Các workflow còn lại (`ci-dot-bien-du` `ops-*`) đều `ubuntu-latest`": quét MỌI tệp trong `.github/workflows/` (kể cả `runs-on` biểu thức, matrix, reusable workflow `uses:`).
8. "gate của mã đó KHÔNG BAO GIỜ được đo trên Windows, kể cả sau merge": có workflow/trigger nào khác (schedule, workflow_run, dispatch tự động từ workflow khác…) chạy gate `ci.yml` trên Windows mà đoạn bỏ sót không?
9. Các câu GIỮ NGUYÊN trong đoạn (bẫy `labeled` của `ci.yml`: `pull_request:` không khai `types:`; bước `PR head contains required EOL base` có `if: github.event_name == 'pull_request'`) còn đúng ở reviewed_sha không.
10. Câu chú thích đợt 14-08 ("khi ấy ma trận còn vế master"): kiểm `ci.yml` ở commit ~14-08-2026 (`git log --until`) xem ma trận khi đó thực sự có vế master không.
11. Đoạn mới có tự mâu thuẫn với chỗ KHÁC trong `CLAUDE.md` (ví dụ mục "API CHỈ CÓ TRÊN MỘT NỀN" nói job Windows chỉ chạy khi có nhãn, mục deploy §5 nói lane LAND `if: github.ref == 'refs/heads/master'`) hay với `docs/PROTOCOL_DA_PHIEN.md` / `docs/adr/0049*` không?

Chạy thêm hai cổng tại `cay-kho/` và ghi rc + dòng kết luận:
`python3 .claude/dev/packet_loop.py doctrine-scan --root .` và `python3 scripts/tl.py doc-claims-check --json` (đòi `"ok": true`).

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` NGAY khi bắt đầu (dòng `verdict: dang_lam`), nối thêm sau MỖI hướng thử — lượt có thể bị cắt giữa chừng; phần đã ghi phải còn. Cuối cùng sửa dòng đầu thành `verdict: approve` hoặc `verdict: changes_requested`, kèm `reviewed_sha: b38fce83d0e97981012072ca2a2023ac726e5b2e`.

Cấu trúc:
```
verdict: ...
reviewed_sha: ...

## BẢNG ĐO
| khẳng định | PR khai | đo được (lệnh) | khớp? |

## BẢNG SĂN   (>= 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
HƯỚNG n: <tên>
  giả thuyết : ...
  lệnh       : ...
  output     : ...
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
P1 = khẳng định sai về sự thật đo được (đúng loại lỗi PR này sinh ra để sửa). P2 = khai rộng hơn phép đo / thiếu điều kiện. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" mà không có output là không hợp lệ.
