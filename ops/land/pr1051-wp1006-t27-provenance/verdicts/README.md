# Bàn giao hiện vật PR #1051 (land-81-ha-cap r2 / vá P2 kiểm toán #1007)

Nhánh tạm theo luật bàn giao 02-11-2026. Đây không phải nhánh PR, và không mở PR từ nhánh này.

- PR #1051 đã merge: head `c00561c9e9f581242e6d05ac3421e992d4b98f42`, merge commit `68fa6a1c6a629d0a623661ae1032532280598e58`.
- Nhánh này rẽ từ `68fa6a1`. Thứ duy nhất được thêm là thư mục này.

## reviews/
Mỗi thư mục con `cr-1051-rN` giữ những tệp có sẵn trong bốn tệp: `PROMPT.md`, `VERDICT.md`, `run.json`, `launcher-out.json`.
Cả 14 lượt đều chạy Codex qua `.claude/dev/launcher.py run`.

| Lượt | Thư mục | Kết quả |
|---|---|---|
| 1–13 | `r1`…`r13` | changes_requested, mỗi lượt 1 P2 cùng lớp `wp1006-case-insensitive-listing-case-sensitive-consumer` |
| 14 | `cr-1051-r14` | approve, P0–P3 = 0, run `a2aead211630`, trên `de55985` |

Các thư mục hậu tố `b`/`c` là lượt chạy lại: lần đầu chết vì bộ lọc nội dung hoặc tự dừng. Chi tiết ở PR #1051 issuecomment-6538759559.

`sha256(reviews/cr-1051-r14/VERDICT.md) = fe37b7eb8c4797a3aa83b51154198db292bd9fe0d772f218d3ea3f669968cecd`.

Tổng lời gọi Codex: 17, trần 10 (ADR-0055). Chủ kho chọn (a) ở #1051 issuecomment-6569227267: chấp nhận lượt 14 cho head `c00561c`, vì diff của PR ở hai head trùng từng dòng.

## mutation/
- `mut1051n.py`: bộ đột biến 39 mutant cộng 1 đối chứng. Một mutant chỉ tính là giết khi dòng kết quả có `rc=1` và `ĐỎ t27_phan_chung…`.
- `mut1051n.out`: kết quả trên Linux, 39/39.
- Windows `tra-luat-win` trên `c00561c` (tệp `C:\work\tl-1007\mut1051n-c005.out`, không chép về đây vì console mã hoá sai): 40 dòng. Đối chứng `rc=0` 1/1; 39 dòng `rc=1`, dòng nào cũng có `ĐỎ t27_phan_chung_ten_bien_nhan_sai…` ⇒ 39/39.

## CI trên c00561c
- Run PR `41374084633`: 23/23 success, nhãn `ubuntu-latest`.
- Run Windows `workflow_dispatch` `41374085718`:
  - 15 success, 1 skipped (`gate-cong-cu-gop`, job này không chạy Windows theo thiết kế);
  - `lease_publish` 256/256, bỏ qua 13. Cả 13 ca thuộc `ops-publish-lease.yml`, workflow chỉ chạy Ubuntu.

Quét bí mật: `scripts/pkg_secret_scan.py ops/handoff` cho rc=0. Đối chứng dương: bơm một chuỗi `GOCSPX-…` giả thì công cụ trả rc=1.
