# Review độc lập packet #1389 r1 (PLAYWRIGHT-DAEMON-DU-LUONG)

Bạn là reviewer độc lập, chỉ đọc, chạy ở context mới. Bạn không sửa nhánh executor, không commit, không push. Tệp này
là prompt, KHÔNG phải lease. Thứ định danh mã là **băm commit**, không phải tên nhánh.

## Đầu vào
- Thư mục làm việc là bản clone của `ducthangho/tra-luat` tại exact head `H` (xem `HEAD_SHA.txt` cạnh `repo/`).
  Coi `repo/` là chỉ đọc. Base: `eca1d125b82783a6a736c7023751ba53cc9a49c8`.
- Đặc tả đóng băng: `repo/ops/specs/wp1389-r1.md`, sha256 phải là
  `12257fa8d659ff5c013af4bc31de700de4a53b085a99ec8c47cbd403d66610bc`. Lease: `repo/ops/leases/wp1389-r1-g1-claude.yaml`.
- Diff cần review: `git -C repo diff eca1d125b8..HEAD -- .agents/skills/playwright-browser/SKILL.md`, cộng hai harness
  `repo/ops/acceptance/wp1389/residue_matrix.sh` và `.ps1`, cộng `repo/ops/acceptance/wp1389/RESULTS.md`.
- Nguồn CLI đã ghim, giải nén sẵn, chỉ đọc: `pwsrc/x_playwright-cli-0.1.23/`, `pwsrc/x_playwright-core-1.65.0-alpha-2026-10-30/`.
  Tarball gốc nằm trong `pwsrc/*.tgz`. Tự kiểm SRI sha512 so với `integrity` trong `repo/.agents/skills/playwright-browser/package-lock.json`.
- `scratch/` là thư mục rỗng: chỗ duy nhất bạn được ghi.

## Việc phải làm
1. Kiểm `git -C repo rev-parse HEAD` bằng `HEAD_SHA.txt`, và cây sạch.
2. Kiểm lời khai nguồn trong spec §1 bằng chính mã ghim:
   - `computeBaseDaemonDir`;
   - cách tính hash thư mục con;
   - `startDaemon` tạo `.err`;
   - `deleteData` không xoá `.err`;
   - không có tuỳ chọn dời được hỗ trợ.
   Nếu tìm được một tuỳ chọn được hỗ trợ để dời sổ phiên, đó là finding: phương án (a) của spec sẽ khả dụng.
3. Chạy đúng một lần: `bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1`
   (tạo `scratch/n1` rỗng trước). Báo dòng `SOURCE` và dòng `TONG`. Harness chỉ dùng fixture tệp, không gọi CLI, không mạng.
4. Review theo spec §3 (B1–B8), trên cả bash lẫn PowerShell:
   - Có đường nào khiến bước dọn xoá một tệp KHÔNG mang nonce của Capture hiện tại? Có đường nào xoá tệp của phiên
     khác, đi theo symlink/junction ra ngoài, hoặc in `CLEANUP OK` mà dư lượng vẫn còn?
   - Hai bản bash/PS có tương đương không: phân biệt hoa thường, reparse point, thư mục cache rỗng/thiếu,
     `XDG_CACHE_HOME` rỗng?
   - Có hồi quy nào ở Capture/Cleanup hiện có không?
   - Limits/Uninstall có khai đúng phạm vi không, có hứa quá phép đo không?
5. Đánh giá độ đủ của ma trận: chốt nào không có đột biến? Ca nào chỉ CÓ MẶT mà không ĐO? Đọc bằng chứng Windows trong
   `RESULTS.md` như lời khai của executor: bạn không chạy được Windows.
   Ca `N5-err-symlink` trên Windows là KHÔNG ĐO ĐƯỢC.
6. Khi muốn thử một hướng tấn công cần dựng đường dẫn thoát khỏi cây, hãy MÔ TẢ nó bằng lời trong finding. Đừng tự
   soạn nội dung ấy; executor sẽ dựng nó thành ca.

## Đầu ra (ghi vào `scratch/VERDICT.md`, cùng in ra stdout)
- `reviewed_sha: <40 hex>`, `verdict: approve | request_changes`, `reviewer: codex (OpenAI), codex_cli, read-only`.
- Findings P0–P3. Mỗi finding gồm: tệp:dòng, kịch bản hỏng cụ thể, đề xuất sửa, và ca test sẽ bắt được nó.
- Các lệnh đã chạy kèm mã thoát thật. Phần KHÔNG đo được.
