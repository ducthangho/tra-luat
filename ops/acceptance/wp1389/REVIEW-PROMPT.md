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

## Lượt 2 (delta) — dùng thêm phần này khi đã có `VERDICT.md` lượt 1

- Lượt 1 ở `4aae991` ra `request_changes`: 4 P1, 3 P2, 1 P3. Nguyên văn ở `repo/ops/acceptance/wp1389/VERDICT.md`.
- Executor sửa ở `5c01f39` và `6896f16`. Từng sửa đổi và lỗi mới do local Windows bắt (W3, W4) ghi trong
  `repo/ops/acceptance/wp1389/RESULTS.md` §6.
- Việc lượt 2:
  1. Với TỪNG finding lượt 1, xác minh trên mã ở H: đã sửa, sửa một phần, hay chưa. Phải có căn cứ là dòng mã, không
     dựa vào lời khai trong `RESULTS.md`.
     - Riêng P1 thứ ba (liên kết ở thư mục cha, tráo thư mục): executor KHÔNG sửa bằng mã, chỉ khai trong Limits.
       Đánh giá lựa chọn đó: chấp nhận được hay vẫn là chặn merge, và vì sao.
  2. Chạy lại đúng một lần lệnh N1 vào `scratch/n1` rỗng. Báo dòng `SOURCE` và dòng `TONG`.
  3. Tìm lỗi MỚI do các bản sửa đưa vào. Chú ý:
     - `mapfile -d ''` + `wait "$!"` (bash ≥ 4.4);
     - so `${f##*/}`;
     - kiểm `${h%/*} = $D` khi `XDG_CACHE_HOME` có `/` ở cuối;
     - quét bằng `[IO.Directory]` của PowerShell: thư mục là junction, mẫu `*nonce*` khớp tên 8.3, đường dẫn UNC;
     - thứ tự chép → so → ghi `11-daemon-path.txt` → xoá.
  4. Ghi verdict theo đúng khuôn đầu ra ở trên vào `scratch/VERDICT.md`.

## Lượt 3 (delta, lời gọi Codex cuối theo lease) — sau thiết kế lại

- Lượt 2 ở `f2654b2`: `request_changes` (3 P1, 4 P2, 1 P3), nguyên văn trong `VERDICT.md`.
- Chủ kho chọn thiết kế lại "hỏi chính CLI", ghi ở `RESULTS.md`. Sổ phiên giờ lấy từ `baseDaemonDir()` và
  `createClientInfo().daemonProfilesDir` của `playwright-core/lib/tools/cli-client/registry.js` trong bản ghim, chạy bằng
  `node -e` từ `work`.
  - Capture ghi kết quả vào `00-sophien.txt`.
  - Cleanup hỏi lại TRƯỚC `close` và đòi kết quả trùng tệp đó.
  - Bước dọn đòi mục duy nhất phải là `<dòng 2>/<nonce>.err`.
  - Gỡ bản cài hỏi lại trước khi xoá `install`.
- Việc lượt 3:
  1. Với TỪNG finding lượt 2, xác minh trên mã ở H: đã sửa, sửa một phần, hay chưa. Căn cứ phải là dòng mã.
  2. Đánh giá chính thiết kế mới:
     - phụ thuộc vào mô-đun nội bộ của bản ghim;
     - `node -e` có cùng CWD và môi trường với CLI không (`chay_ghi`/`Invoke-PwGhi`);
     - `00-sophien.txt` có thật sự neo được từ Capture tới Cleanup không;
     - hành vi khi Capture dừng trước `open`;
     - cách truyền đối số `node -e` trong PowerShell 5.1/7 (chuỗi JS không có dấu nháy).
  3. Chạy N1 đúng một lần:
     `bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1 "$(command -v node)"`,
     tạo `scratch/n1` rỗng trước. Báo dòng `SOURCE` và dòng `TONG`.
  4. Ghi verdict theo khuôn đầu ra ở trên vào `scratch/VERDICT.md`. Trong verdict, tách riêng finding nào chặn merge và
     finding nào chỉ là giới hạn đã khai.

## Lượt 4 (delta, lời gọi Codex thứ 4 do chủ kho nâng trần trong lease)

- Lượt 3 ở `86879e1`: `request_changes`. Chặn merge gồm 2 P1 và 2 P2; P3 là giới hạn đã khai. Nguyên văn trong
  `VERDICT.md`.
- Sửa ở `429fb5b`, chi tiết trong `RESULTS.md`:
  - `00-sophien.txt` thêm dòng nonce; Cleanup đòi trùng cả ba dòng TRƯỚC `close`.
  - Trước `close`, sổ phiên và thư mục hash phải là thư mục thường, không có hook; bash ≥ 4.4.
  - `node -e` in base64 của UTF-8; cả hai shell giải mã tường minh.
  - Gỡ bản cài kiểm loại thư mục.
  - Ma trận thêm phần TOÀN LUỒNG E1–E4: chạy chính khối Capture và Cleanup của SKILL với một CLI giả có nhật ký và
    trạng thái, kèm đột biến đưa chốt đầu Cleanup ra sau `10-verify`.
- Việc lượt 4:
  1. Với TỪNG finding chặn merge của lượt 3, xác minh trên mã ở H: đã sửa, sửa một phần, hay chưa. Căn cứ phải là dòng mã.
  2. Tìm lỗi MỚI do bản sửa đưa vào. Chú ý:
     - `base64 -d` và `FromBase64String`;
     - dòng thứ ba nonce;
     - thứ tự kiểm trước `close`;
     - phần toàn luồng của harness: CLI giả có mô phỏng đúng hợp đồng phản hồi mà Cleanup so byte không?
  3. Chạy N1 đúng một lần, như lượt 3. Báo dòng `SOURCE` và dòng `TONG`.
  4. Ghi verdict vào `scratch/VERDICT.md`. Tách riêng finding chặn merge và giới hạn đã khai.

## Lượt 5 (delta; CHỈ chạy khi chủ kho đã nâng trần hoặc chọn đường review khác — lease đang `used: 4, limit: 4`)

- Lượt 4 ở `999f5fc`: `request_changes`. Chặn merge gồm 1 P1 và 4 P2. Nguyên văn trong `VERDICT.md`.
- Sửa ở `ff34b2c` và `d7960ee`, chi tiết trong `RESULTS.md` §8:
  - Không thành phần nào của đường dẫn tới thư mục hash được là liên kết: bash so `realpath`, PowerShell dò từng thư mục
    tổ tiên tìm ReparsePoint. Áp ở trước `open`, trước `close`, bước dọn và Gỡ. Các chốt `-L`/reparse riêng lẻ cũ đã gộp
    vào phép này.
  - `00-sophien.txt`: PowerShell kiểm thuộc tính reparse trước khi đọc; cả hai shell tạo tệp ở chế độ không ghi đè.
  - Gỡ có khối mã (1)/(2) cho cả hai shell: thư mục lấy từ `11-daemon-path.txt` (B7), đối chiếu `00-sophien.txt` và câu
    trả lời CLI, rồi xoá không đệ quy.
  - Harness: CLI giả trả `deleted` theo descriptor có tồn tại (như `session.js`); E1/E6 so `SHA256SUMS` với 4 tệp; E2/E3
    so nhật ký chính xác và byte phiên kia; thêm E5/E7/E8, N20–N24, D9/D10, C14/C15, L4, W1, G1–G7 và các đột biến.
- Việc lượt 5:
  1. Với TỪNG finding chặn merge của lượt 4, xác minh trên mã ở H: đã sửa, sửa một phần, hay chưa. Căn cứ là dòng mã.
  2. Tìm lỗi MỚI do bản sửa đưa vào. Chú ý:
     - `realpath -m` khi thư mục chưa tồn tại;
     - dò tổ tiên bằng `Split-Path -Parent` với đường dẫn UNC;
     - `set -C` trong subshell lồng;
     - khối Gỡ: `GO_DH=$(…) || …` và chuỗi `-and` trong ngoặc của PowerShell;
     - CLI giả có còn mô phỏng đúng hợp đồng `close`/`delete-data` của bản ghim không.
  3. Chạy N1 đúng một lần, như lượt 3. Báo dòng `SOURCE` và dòng `TONG`.
  4. Ghi verdict vào `scratch/VERDICT.md`. Tách riêng finding chặn merge và giới hạn đã khai.

## Lượt 6 (delta; chủ kho nâng trần Codex 5 → 6, ghi ở lease `budget_nang_tran_3`)

- Lượt 5 ở `376e9c2`: `request_changes` (1 P1 + 2 P2 chặn merge), nguyên văn trong `VERDICT.md`.
- Sửa ở `1d7b9f4` (và commit vá harness sau nó nếu có, xem `RESULTS.md` §9):
  - P1: mọi phép so `realpath` của bash giữ byte cuối: `[ "$(realpath … -- "$DH"; echo .)" = "$DH"$'\n.' ]`.
  - P2 Gỡ: `00-sophien.txt` và `11-daemon-path.txt` phải là tệp thường, không liên kết, TRƯỚC khi đọc; cấm hook; `00`
    trùng NGUYÊN câu trả lời CLI + nonce (bash so cả tệp kèm LF cuối; PS so từng dòng và dòng rỗng cuối).
  - P2 Capture: từ chối mọi mục có sẵn ở `00-sophien.txt` (gồm FIFO, symlink treo) trước khi tạo với `set -C`.
- Việc lượt 6:
  1. Với TỪNG finding chặn merge của lượt 5, xác minh trên mã ở H: đã sửa, sửa một phần, hay chưa. Căn cứ là dòng mã.
  2. Tìm lỗi MỚI do bản sửa đưa vào, đặc biệt ở các phép so `"$(…; echo .)"` và khối Gỡ PowerShell.
  3. Chạy N1 đúng một lần, như lượt 3. Báo dòng `SOURCE` và dòng `TONG`.
  4. Ghi verdict vào `scratch/VERDICT.md`. Tách riêng finding chặn merge và giới hạn đã khai.

## Lượt 7 (delta; chủ kho nâng trần Codex 6 → 7, ghi ở lease `budget_nang_tran_4`)

- Lượt 6 ở `d0d4879`: `request_changes` (1 P1 + 2 P2 chặn merge), nguyên văn trong `VERDICT.md`.
- Sửa ở `8be8070`, chi tiết trong `RESULTS.md` §10:
  - P1: PowerShell so đường dẫn đích và thư mục hash bằng `[string]::Equals(…, [StringComparison]::Ordinal)`, không dùng `-ceq`.
  - P2: đầu Cleanup và Gỡ so TỪNG BYTE `00-sophien.txt`/`11-daemon-path.txt` với nội dung mà Capture/Cleanup tạo: bash
    `printf … | cmp -s -- - <tệp>`, PowerShell `ReadAllBytes` → base64 → so ordinal.
  - P3 (gợi ý): sentinel `realpath` chỉ in khi lệnh thành công (`&& echo .`).
  - Ca mới: N26 (tên có U+00AD), D12/G13/G14 (byte NUL ở bash, BOM ở PS), kèm đột biến trở về so chuỗi. Đột biến PS
    `ceq-path` ĐO hành vi runtime: lọt ⇒ P1 tái hiện trên shell đó; không lọt ⇒ ghi SKIP "KHÔNG TÁI HIỆN".
- Việc lượt 7:
  1. Với TỪNG finding chặn merge của lượt 6, xác minh trên mã ở H: đã sửa, sửa một phần, hay chưa. Căn cứ là dòng mã.
  2. Tìm lỗi MỚI do bản sửa đưa vào: pipeline `printf | cmp` trong chuỗi `&&`/`||` (không có `pipefail`), cách PowerShell
    mở dòng tiếp sau dấu phẩy có chú thích, mã hoá UTF-8 không BOM ở cả hai phía phép so.
  3. Chạy N1 đúng một lần, như lượt 3. Báo dòng `SOURCE` và dòng `TONG`.
  4. Ghi verdict vào `scratch/VERDICT.md`. Tách riêng finding chặn merge và giới hạn đã khai.
