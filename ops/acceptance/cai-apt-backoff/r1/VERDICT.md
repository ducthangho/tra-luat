# CAI-APT-BACKOFF r1 — review độc lập Codex offline (2/2 lời gọi): approve

**Căn cứ:** đặc tả `ops/specs/cai-apt-backoff-r1.md` §3–§4, lease `ops/leases/cai-apt-backoff-r1-g1-claude.yaml`
(`review_calls_limit: 2`), Issue #1479, PR #1482.

## Các lượt
| lượt | run (`launcher.py run`) | head review | kết luận | sandbox | model phục vụ |
|---|---|---|---|---|---|
| 1 | `eb85ec11`, 02:52:48Z → 02:57:50Z, `ma_thoat` 0 | `7623e65b1d70e611abd8958cac7c1e71c230785c` | **request_changes**: 1 P2, 1 P3 | `DO_DUOC` | `gpt-6-astra` |
| 2 | `7f6ebe68`, 03:07:21Z → 03:16:50Z, `ma_thoat` 0 | `83c0c950881a37f25b7fcc9f93d9d8be4ebaa030` | **approve**: 0 P0–P2, 0 đột biến sống | `KHONG_DO_DUOC` | `gpt-6-astra` |

Lệnh, cả hai lượt: `python3 .claude/dev/launcher.py run --workspace <clone tại head> --expected-repo ducthangho/tra-luat
--expected-root-commit e13f74bb… --expected-head <head> --prompt-file <p> --expected-prompt-sha256 <sha> -- /opt/node22/bin/codex exec
-m gpt-6-astra --sandbox workspace-write --skip-git-repo-check -C <thư mục review> "…{PROMPT_FILE}…"`.

## Xử lý finding
| finding | xử lý | bằng chứng |
|---|---|---|
| L1 F1479-01 P2: `sleep` hỏng hoặc vắng, dưới `set -e`, làm script thoát ngay với mã của `sleep` (127/23), bỏ lần cài lại và mã của lần cài cuối | `sleep … \|\| echo "… loi (rc=$?) — thu lai ngay"`: chỉ chặn lỗi của riêng lệnh `sleep`; ca `r1479_sleep_hong_van_cai_lai_va_giu_ma_lan_cuoi`; đột biến `wp1479_sleep_hong_lam_chet` | `83c0c95`; lượt 2 tái hiện: thiếu `sleep` thật trong PATH hẹp, và `sleep` trả 23/127 ⇒ đủ 4 lần cài, mã 44; đường `--bat-buoc` với công cụ tuỳ chọn 3/3 đạt |
| L1 F1479-02 P3: chưa ca nào khoá thứ tự sleep → update, cũng chưa khoá tên kênh `kq-thu-lai-<k>` | ca `r1479_thu_tu_sleep_update_va_ten_kenh` (một nhật ký có thứ tự); đột biến `wp1479_update_truoc_sleep`, `wp1479_sai_so_kenh` | `83c0c95`; lượt 2: hai đột biến tự dựng từng sống ở lượt 1 nay bị giết |

## Đo trên head code cuối `83c0c95`
- 9/9 ca `r1404_*` và `r1479_*` đạt.
- 32/32 đột biến wp1404/wp1479 bị giết đúng lý do (`TinHieuChotCa` của ca đích). Cả 80 đột biến nhắm vào `cai_cong_cu.sh` neo khớp đúng một chỗ.
- `.claude/dev/launcher_test.py` đầy đủ trong container của executor: `rc=0`, 452/452 ca chạy qua, 0 hỏng. Hai ca bỏ qua (`t62`, `r484_g4`) chỉ dành cho Windows và đã bỏ qua trên Linux từ trước. Nhật ký `vao=454 ra=454`.
- Delta so `origin/master` `5a152c1` = 0. Executor và lượt 2 đo độc lập, cùng kết quả:
  - `shellcheck` 1 → 1 (SC1090 có sẵn);
  - `bash -n` sạch;
  - ruff F 5 → 5;
  - `doctrine-scan` 12 tệp, 0 vi phạm.
- Ghi nhận môi trường, không phải hồi quy:
  - Một lượt đầy đủ trước đó của executor chạy trùng lúc với Codex lượt 1 và đỏ 11 ca `r484_*` với `Codex home is inside a repository`. Đây là tạo tác `/tmp/.git` của sandbox Codex đang chạy (CLAUDE.md). Chạy lại khi không có Codex: 452/452.
  - Trong sandbox của lượt 2, bộ đầy đủ đỏ 15 ca (`/tmp/.git`, `/var/tmp` chỉ đọc, credential Codex bị từ chối). Reviewer tái hiện cả 15 ca trên `origin/master` với cùng phân loại.
- `ops/cong_cu_test.py` (lượt 2, phần nền): 60/60 ca đo được đạt. Phần bán kính đột biến bị ngắt giữa chừng, nên **chưa** phải lượt đủ; CI của PR chạy đủ 8 mảnh.

## Giới hạn đã nêu, không chặn
- Hook phiên (#1474) cắt mỗi lần cài ở 180 s; lỗi apt kéo dài sẽ bị cắt trước khi hết 3 lần thử lại (đặc tả §2).
- Khi `sleep` hỏng, vòng thử lại ngay không giãn cách, vẫn trong trần N lần.
- Hai hàm `_tl1479_*` còn được định nghĩa trong shell gọi `source`. Đặc tả chỉ cấm lọt BIẾN, và kho đã có tiền lệ `_wp1404_chay_cong_thuc`.
