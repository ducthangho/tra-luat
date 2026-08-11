# Handoff bền — không để trong Temp máy cá nhân

## Vì sao có thư mục này

Ngày 11-08-2026, một phiên Reconciler được giao:

> Đọc toàn bộ handoff: `C:\Users\admin\AppData\Local\Temp\tra-luat-wp86-cloud-handoff.md`

Phiên đó chạy trên **cloud Linux runner**, không phải máy ASUS, nên đường dẫn Windows kia **không
tồn tại**. Handoff không đọc được. Phiên phải dựng lại toàn bộ ngữ cảnh từ Issue #76/#77/#86 —
may là đủ, nhưng đó là may chứ không phải thiết kế.

Cùng lớp sự cố xảy ra khi chủ kho mở phiên từ **điện thoại**: mọi tệp nằm trên ổ `D:` hoặc trong
`%TEMP%` của máy tính đều vô hình.

**Quy tắc rút ra: handoff phải nằm ở nơi MỌI tác nhân đọc được — repo hoặc GitHub Issue — chứ không
nằm trong thư mục tạm của một máy.**

## Nguồn sự thật: chia hai lớp, đừng trộn

| Loại nội dung | Nơi đặt | Lý do |
|---|---|---|
| **Trạng thái sống** — state, lease, verdict, budget ledger, authorization | **Comment trên GitHub Issue** | Có `reconcile_key`, có thứ tự thời gian, có identity bền, không cần clone repo. Đây là event journal (§3.3). |
| **Nội dung DÀI** — prompt handoff, ma trận bằng chứng, inventory, báo cáo probe | **Thư mục này** | Comment quá dài thì khó đọc và khó diff; tệp trong git có SHA, có history, diff được. |
| **Mẫu prompt tái dùng** | `docs/prompts/` | Đã có `CODEX_EXECUTOR_D0.md`, `CLAUDE_REVIEWER_D0.md`, `MANUAL_SUCCESSOR_HANDOFF_D0.md`. |

Khi hai lớp nói khác nhau thì **Issue thắng** — tệp trong repo là ảnh chụp, Issue là trạng thái.
Vì vậy tệp ở đây phải luôn **trỏ ngược** về Issue/comment URL sinh ra nó.

## Đặt tên

```
.github/coordination/handoffs/YYYY-MM-DD-<slug>.md
```

Ví dụ: `2026-08-11-wp86-cloud-linux-migration.md`. Ngày là ngày tạo, không phải ngày sửa.

## Ràng buộc bắt buộc

- **KHÔNG secret.** Không token, cookie, credential, đường dẫn có chứa bí mật. Repo đang `private`
  nhưng đó không phải lý do để nới — bộ quét `scripts/pkg_secret_scan.py` và hook vẫn áp dụng.
- **LF.** Mọi tệp mới phải LF; `python .githooks/eol_policy.py --all --json` phải cho `violations=0`.
- **Trỏ về Issue.** Mỗi tệp mở đầu bằng khối YAML nêu `mission_issue`, `packet_issue`, `spec_hash`
  (nếu có) và URL comment nguồn.

## Vì sao đặt dưới `.github/` chứ không phải `docs/`

`.github` nằm trong `_RELEASE_EXCLUDE_DIRS` (`scripts/tl_core/release.py:394`), nên tệp ở đây:

- **ngoài gói phát hành** — runtime Cowork không cần đọc handoff điều phối;
- **không ăn vào trần 200 tệp** — quỹ import đang rất chật;
- **không kéo** `RELEASE_MANIFEST.json` hay golden vào diff;
- **không đụng** ratchet `r291_docs_ngoai_goi` (ratchet đó đếm Markdown dưới `docs/`).

Vẫn **giữ trong git** đầy đủ — cùng khuôn với `rasoat/` và `changelog_archive/`.

## Với tệp đang kẹt trên máy tính

Nếu handoff/bằng chứng đang nằm trên ASUS mà phiên cloud hoặc điện thoại cần đọc, có hai đường:

1. **Bridge session** — mở phiên trên environment bridge của chính máy đó
   (`ASUS-LAPTOP:D:\Quốc hội\tra-luat`), copy tệp vào thư mục này rồi commit/push. Đường này giữ
   provenance và diff được.
2. **Dán thẳng vào comment Issue** — hợp cho nội dung ngắn. Dài quá thì dùng đường 1.

Trước khi copy bất cứ thứ gì từ `%TEMP%`: **đọc qua một lượt**. Thư mục tạm hay lẫn tệp không liên
quan và đôi khi có dữ liệu nhạy cảm; đừng copy cả mớ.
