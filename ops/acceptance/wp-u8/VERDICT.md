# WP-U8 r1 — Review độc lập (1/1)

- **Reviewer:** Codex CLI 0.169.0, `-m gpt-6-astra`, chạy trong container điều phối, chỉ đọc. Model tự khai **`KHONG_do_duoc`**. Thời gian 05:22:35Z–05:24:14Z ngày 19/11, rc 0. Verdict gốc có sha256 `41c446fb…`.
- **Đối tượng:** bộ con bằng chứng zip `70708004…`; 15/15 tệp khớp MANIFEST-a `e1a1246d…` và MANIFEST-b `69763498…`. **Không** chuyển: hai driver chính `U8-A.ps1` và `U8-B.ps1`, hai manifest profile lớn, và zip đầy đủ. Reviewer ghi rõ giới hạn này.
- **Reviewer tự khai một vi phạm phạm vi:** đã ghi tạm một bản sao ngữ cảnh ra ngoài thư mục được phép rồi xoá. Không có ghi nào vào kho.

## Verdict: `approve_with_fixes` (không có P0)
| Điểm | Kết luận |
|---|---|
| Toàn vẹn | Đạt |
| A0/A1/A2, khoá | Đạt theo bằng chứng có. Độ rộng tiền kiểm không kiểm được, vì thiếu `U8-A.ps1` |
| L1/L2 | Đủ cho câu "mở lại và đóng êm trên profile đã restore". **Không** đủ cho trạng thái REST sẵn sàng hay "dùng được khi đã đăng nhập". Cả hai lượt tự ghi `passed=false` |
| B0–B4 | Đạt: B1 = B2 = B4 (`9201616d…`), robocopy rc 1 |
| B7 | Đạt: đúng hai thư mục, có kiểm reparse point |
| Credential, yêu cầu | Không thấy nội dung credential hay cookie; không thấy lời gọi provider hay inference nào do operator khởi phát. `U8-L.ps1` có đọc toàn bộ `settings.json` vào bộ nhớ, nhưng chỉ chiếu ra các boolean |

**P1 (đã sửa):** RESULTS và MATRIX ghi PASS rộng hơn phần thực đo. `totalRequests=0` là **chưa đo**, không phải được miễn. Lệnh của chủ kho cho phép operator mở và đóng app, không cho phép thay tiêu chí. Đã sửa câu chữ; PASS nay chỉ là "sao chép, khôi phục, mở lại được" trên Desktop.

**P2 (đã sửa ở công cụ, chưa từng chạy):** nhánh dự phòng của `U8-L.ps1` diệt mọi tiến trình `Proxima*`. Nay chỉ diệt hậu duệ của tiến trình do chính driver mở. Cả hai lượt thật đều đóng êm, nên nhánh này chưa bao giờ chạy.

<details><summary>Nguyên văn verdict của reviewer (sha256 41c446fb…)</summary>

```text
VERDICT: approve_with_fixes

Independent offline evidence review; no Windows execution. Model: KHONG_do_duoc (exact model ID unavailable). Provider: OpenAI; surface: API agent with container tools; transport: local files.

Reviewed SHA: `0ded21c7e01a9641c76742b406195aa77d3c9753`; tree: `8a5628dea72a655404c381a9bd78c4eca69bd3bb`; branch: `ccr-8ee03d7f-vnmqk0`. Reviewed repository files match HEAD. Spec SHA matches lease `$.spec_hash`. References below: A/B = EV/evidence-a/b; S = ops/specs/wp-u8-r1.md; R = ops/acceptance/wp-u8/RESULTS.md; M = ops/acceptance/wp1319/MATRIX.md.

| Check | Assessment and evidence |
|---|---|
| Integrity | PASS: subset SHA256 `70708004d2ad6d0154e475328d9cb8c50132bb0c8684550fce7d6599e9810261`; extracted bytes match ZIP. All 15 relayed evidence files match MANIFEST `$.files[*].size/sha256`; no extras. Manifest hashes match supplied prefixes: A `e1a1246df8ed3edbbad0e288bccea868e5d9b8452f0fb44d0faf88b34a6c96f4`, B `697634982108683613362a81828c966a38fc4c1c12e8f6ca6f7d38597adc24ec`. |
| A0/A1 | A/U8-A-result.json `$.steps.A0` records empty keys/directories/shortcuts/processes, absent default profile/backup and machine load. A1 records rc=0, hkcu_only=true, installer `959c14c1…`, updater size 161754969, exe `6990dce4…`, 105 polls with no app observed. Exact hive/search breadth, install invocation/helper waiting cannot be audited without U8-A.ps1. Sampling cannot exclude a short-lived process. |
| A2/locks | One failed shortcut creation, one successful ASCII-name rerun; empty profile, correct arguments, no app/default profile (A/U8-A-progress.log:4–13). Both locks released after failure/success. A/U8-A2.ps1:14–17,32 checks empty locks and releases only matching ownership text. |
| L1/L2 | Explicit test-profile launch (B/U8-L.ps1:32). Both JSONs: `$.ready=false`, `$.passed=false`, `$.stats=[]`, 120 seconds, six WM_CLOSE posts, graceful_exit=true, exit_code=0. L1 creates 21 top-level entries; L2 retains 21. Sufficient for “reopened and closed on restored profile,” not REST readiness or authenticated usability. |
| B0–B4 | B/U8-B-result.json `$.steps`: no processes; 12404 files/180730298 bytes; B1=B2=B4 digest `9201616d…`, both equal_B1=true, robocopy rc=1<8. Robocopy logs confirm required options and zero failures. B3 records rename and profile_gone=true. |
| B7 | B/U8-B7.ps1:10–21 restricts selection to backup plus exactly one damaged directory, checks workdir prefix, root/descendant reparse points. B/U8-B-progress.log:39–44 records precisely those two deletions, retained profile/install, released locks. |
| Credentials/requests | No exposed credential/cookie content or operator inference/provider calls in relayed evidence. U8-L.ps1:12 parses settings.json then projects only enabled/loggedIn; it does read the whole JSON into memory. No cookie-store inspection shown. REST branch was not entered. Secret scans `$.rc=0` cover listed evidence files, not every frozen-ZIP member. |

Findings:

- **P0:** None evidenced.
- **P1 — qualify acceptance:** R:36,62 and M:232 overstate full measurement against S:68–69. REST-disabled operation makes stats unavailable, not automatically waived; totalRequests=0 remains unmeasured. Owner’s R:33 instruction supports operator launch/close, not silently replacing acceptance criteria. Record both launch `passed=false` results explicitly and label PASS as the narrower Desktop copy/restore/reopen result. Otherwise downstream readers could treat unmeasured inference/readiness criteria as passed.
- **P2 — unsafe fallback, unexercised:** B/U8-L.ps1:11,49–53 kills all matching Proxima processes after timeout, despite claiming “own tree.” A concurrently started unrelated app could be killed. Restrict future use to owned descendants; both observed runs exited gracefully.

Limits to record: login leg **not_measured**, correctly disclosed (R:37,63; M:233); booleans cannot prove session validity. R:15,39–44 honestly records shortcut, launch, REST and build deviations. B log:9–30 supports failed attempt, DryRun, single mutating rerun; “before any changes” means profile changes, since locks/evidence were written. Missing main drivers, both large profile manifests, freezer, original Windows state and full frozen ZIPs prevent independent algorithm/digest recomputation and complete credential audit; attempt-1 driver revision is unavailable. No network used or repository writes. Reviewer housekeeping briefly wrote a context copy outside cwd, then removed it; this breached the requested scratch boundary.
```
</details>

