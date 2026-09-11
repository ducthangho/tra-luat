# Tóm tắt đo GitHub Actions — `ducthangho/tra-luat`, workflow `ci.yml`, job `gate`

- Thời điểm đo (UTC): **2026-09-07T03:54:32Z** (lời gọi `get_workflow_run` + `list_workflow_jobs` qua MCP github, filter=all, perPage=100).
- Đơn vị: **phút** (2 chữ số lẻ, = giây/60, KHÔNG làm tròn lên từng phút như GitHub tính tiền) trừ khi ghi `giây`. Mọi mốc thời gian là UTC.
- `phut` của job = `completed_at − started_at` của JOB (theo API jobs). `run_dau_cuoi_phut` = `updated_at − created_at` của RUN.
- Phạm vi: 13 run, 26 job (13 ubuntu + 13 windows), 1140 bước liệt kê. Run có 2 hình dạng: 44 mục (41 bước + 3 hậu xử lý) ở 11 run; 43 mục ở 2 run (`34048685345`, `34045664423` — chưa có bước `bien-nhan v2 selftest`).
- Run không đọc được: **0** (xem `khong_do_duoc.txt`). Run duy nhất KHÔNG success: `34048229370` (workflow_dispatch, head 4cd80c5) — job windows `cancelled` ở bước 16 `test registry` sau 45 ph 18 s (17:34:14 → 18:19:32), job ubuntu success.

## 1. Thống kê `phut` theo job — chỉ conclusion=success VÀ head_branch=master

- `gate (windows-latest)`, master, success: n=5 · min=40.20 · max=48.00 · biên độ=7.80 · trung vị=45.58 · trung bình=44.65
- `gate (ubuntu-latest)`,  master, success: n=5 · min=23.80 · max=27.68 · biên độ=3.88 · trung vị=26.52 · trung bình=25.91

Tham khảo (KHÔNG thuộc yêu cầu, chỉ để so): mọi job success bất kể nhánh —
- windows: n=12 · min=40.20 · max=50.48 · biên độ=10.28 · trung vị=45.80 · trung bình=45.62
- ubuntu:  n=13 · min=20.93 · max=27.68 · biên độ=6.75 · trung vị=26.52 · trung bình=25.87

## 2. Bảng theo run (sắp theo `created_at`)

`phút tính tiền` = ubuntu×1 + windows×2 trên số phút THÔ (chưa làm tròn lên từng phút, chưa loại job cancelled); job `cancelled` vẫn tính phút chạy thật.

| run_id | head7 | branch / event | ubuntu (ph) | windows (ph) | tính tiền (ph) | run_dau_cuoi (ph) | ghi chú |
|---|---|---|---:|---:|---:|---:|---|
| 34045664423 | 426bfc0 | claude/cap-nhat-trang-thai-pr-taxzax / workflow_dispatch | 24.25 | 43.20 | 110.65 | 43.28 |  |
| 34048229370 | 4cd80c5 | claude/tra-luat-process-review-o4d7kb / workflow_dispatch | 26.42 | 60.17 | 146.75 | 60.52 | windows=cancelled |
| 34048685345 | 1b3caa1 | master / push | 26.52 | 42.28 | 111.08 | 42.33 |  |
| 34049592719 | b912e5f | claude/tra-luat-process-review-o4d7kb / pull_request | 26.65 | 46.02 | 118.68 | 46.35 |  |
| 34052910676 | c0f18ac | claude/tra-luat-process-review-o4d7kb / pull_request | 27.37 | 43.83 | 115.03 | 43.90 |  |
| 34055467808 | cacaba3 | master / push | 23.80 | 47.18 | 118.17 | 47.23 |  |
| 34058508426 | 82e01a4 | claude/priceless-volhard-329577 / pull_request | 27.33 | 41.65 | 110.63 | 41.72 |  |
| 34060879398 | 28cb898 | master / push | 27.68 | 45.58 | 118.85 | 45.63 |  |
| 34062997697 | 62a6385 | claude/tra-luat-process-review-o4d7kb / workflow_dispatch | 20.93 | 49.37 | 119.67 | 49.48 |  |
| 34065779670 | 771c6ed | claude/tra-luat-process-review-o4d7kb / workflow_dispatch | 27.47 | 49.62 | 126.70 | 49.70 |  |
| 34068433781 | 8ce02fd | master / push | 23.93 | 40.20 | 104.33 | 40.27 |  |
| 34070122978 | 0c3405f | claude/tra-luat-process-review-o4d7kb / workflow_dispatch | 26.30 | 50.48 | 127.27 | 50.57 |  |
| 34074288203 | d28c4b1 | master / push | 27.62 | 48.00 | 123.62 | 48.03 |  |
| **Tổng 13 run** | | | 336.27 | 607.58 | **1551.43** | | |

## 3. Hai bước nặng + tổng 9 bước thiết lập (bước 2–10) theo run và nền — đơn vị phút

`thiết lập 2–10` = tổng 9 bước có tên từ `Force LF checkout (hash parity với manifest)` tới `cài Ruff 0.15.15 và in probe dương` (số thứ tự API 2..10; `Set up job` #1 KHÔNG tính). Hai bước nặng: `test registry (phạm vi + các bộ chưa được nối)` và `packet-loop selftest`.

| run_id | head7 | ubuntu: test registry | ubuntu: packet-loop | ubuntu: thiết lập 2–10 | windows: test registry | windows: packet-loop | windows: thiết lập 2–10 | ghi chú |
|---|---|---:|---:|---:|---:|---:|---:|---|
| 34045664423 | 426bfc0 | 13.13 | 3.65 | 1.17 | 17.70 | 9.70 | 3.32 |  |
| 34048229370 | 4cd80c5 | 14.25 | 3.98 | 1.27 | 45.30 (cancelled) | 9.32 | 3.33 | windows test registry cancelled — KHÔNG đưa vào thống kê |
| 34048685345 | 1b3caa1 | 14.33 | 3.98 | 1.45 | 17.13 | 9.37 | 3.10 |  |
| 34049592719 | b912e5f | 14.45 | 3.93 | 1.23 | 18.55 | 9.78 | 3.27 |  |
| 34052910676 | c0f18ac | 14.48 | 3.97 | 1.27 | 17.07 | 7.73 | 3.20 |  |
| 34055467808 | cacaba3 | 12.37 | 3.52 | 1.17 | 16.48 | 9.77 | 3.17 |  |
| 34058508426 | 82e01a4 | 14.48 | 4.08 | 1.28 | 16.13 | 7.67 | 2.83 |  |
| 34060879398 | 28cb898 | 14.72 | 4.05 | 1.32 | 15.72 | 9.63 | 3.20 |  |
| 34062997697 | 62a6385 | 10.58 | 2.98 | 1.00 | 18.07 | 8.63 | 3.07 |  |
| 34065779670 | 771c6ed | 14.35 | 4.00 | 1.30 | 17.40 | 9.18 | 3.12 |  |
| 34068433781 | 8ce02fd | 12.48 | 3.45 | 1.13 | 15.45 | 7.52 | 2.90 |  |
| 34070122978 | 0c3405f | 13.72 | 3.83 | 1.22 | 17.85 | 9.43 | 3.33 |  |
| 34074288203 | d28c4b1 | 14.53 | 4.02 | 1.27 | 16.25 | 9.52 | 3.15 |  |

Thống kê theo nền, chỉ bước success (đơn vị phút):

- ubuntu · test registry: n=13 · min=10.58 · max=14.72 · biên độ=4.13 · trung vị=14.33 · trung bình=13.68
- ubuntu · packet-loop selftest: n=13 · min=2.98 · max=4.08 · biên độ=1.10 · trung vị=3.97 · trung bình=3.80
- ubuntu · thiết lập 2–10: n=13 · min=1.00 · max=1.45 · biên độ=0.45 · trung vị=1.27 · trung bình=1.24
- windows · test registry: n=12 · min=15.45 · max=18.55 · biên độ=3.10 · trung vị=17.10 · trung bình=16.98
- windows · packet-loop selftest: n=13 · min=7.52 · max=9.78 · biên độ=2.27 · trung vị=9.37 · trung bình=9.02
- windows · thiết lập 2–10: n=13 · min=2.83 · max=3.33 · biên độ=0.50 · trung vị=3.17 · trung bình=3.15

## 4. Bước `skipped` theo nền

- ubuntu (12 job, loại run cancelled): `gate lifecycle selftest (nen khong co cgroup)`×12; `PR head contains required EOL base`×9; `tl selftest (luot PR — khong sinh bang chung)`×9; `release-verify strict (lane LAND — manifest committed)`×7; `release-verify strict (lane WORKER — manifest TẠM ngoài repo)`×5; `tl selftest (co bang chung exact-identity)`×3
- windows (12 job, loại run cancelled): `don-nhanh selftest (chốt xoá nhánh)`×12; `bo ca gate chay TRONG cgroup duoc uy quyen (Linux)`×12; `ci-phamvi selftest (phan chung — cong co rang)`×12; `PR head contains required EOL base`×9; `tl selftest (luot PR — khong sinh bang chung)`×9; `release-verify strict (lane LAND — manifest committed)`×7; `release-verify strict (lane WORKER — manifest TẠM ngoài repo)`×5; `tl selftest (co bang chung exact-identity)`×3

Ghi chú đọc: `PR head contains required EOL base` skipped ở mọi lượt KHÔNG phải pull_request (push/workflow_dispatch); `tl selftest (luot PR)` ↔ `tl selftest (exact-identity)` và `release-verify LAND` ↔ `WORKER` là cặp loại trừ theo lane; `don-nhanh`, `cgroup (Linux)`, `ci-phamvi selftest` chỉ chạy ubuntu; `gate lifecycle (nen khong co cgroup)` chỉ chạy windows.

## 5. Nguồn

- `job.tsv` (26 dòng), `buoc.tsv` (1140 dòng), `khong_do_duoc.txt`, dữ liệu thô đã chép: `raw/runs.json`, `raw/jobs.txt`; script: `tinh.py`.
- Dữ liệu bước được chép tay từ phản hồi MCP vào `raw/jobs.txt` rồi kiểm hình dạng bằng máy (số mục đúng layout, thời gian đơn điệu, nằm trong khung job). Số job/bước khớp 26 / 1140.
