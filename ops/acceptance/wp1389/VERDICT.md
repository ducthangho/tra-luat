# WP1389 r1 — review độc lập

## Lượt 1 (Codex CLI, `codex exec -s workspace-write`, 2026-11-18T10:24:39Z → 10:27:51Z, rc 0; chép nguyên văn `scratch/VERDICT.md`)

reviewed_sha: 4aae991093ab4f314c0121b9953ecc772c50b39d  
verdict: request_changes  
reviewer: codex (OpenAI), codex_cli, read-only

## Findings

- **P1 — Bash có thể xoá tệp sai tên.** `.agents/skills/playwright-browser/SKILL.md:331`. Dấu chấm trước `err` là ký tự đại diện trong ERE. Nếu mục duy nhất là tệp thường mang tên `<nonce>Xerr`, Cleanup chép rồi xoá nó và báo thành công. Tệp mang nonce nhưng có thể thuộc chương trình khác. So sánh basename bằng chuỗi đúng `<nonce>.err`, kiểm tra tên hash riêng. Ca: chỉ đặt tệp sai hậu tố trong thư mục hash hợp lệ, yêu cầu STOP, giữ nguyên tệp và chưa tạo bằng chứng 11. Đột biến cho phép dấu chấm đại diện phải làm ca lọt.

- **P1 — Bash có thể báo thành công sau khi quét thiếu.** `.agents/skills/playwright-browser/SKILL.md:329`. `mapfile` nhận phần stdout của `find` và bỏ mã thoát của process substitution. Nếu một thư mục hash truy cập được chứa `.err` hợp lệ và một thư mục hash khác chứa mục cùng nonce nhưng bị từ chối liệt kê, Cleanup có thể xoá mục thấy được và in `CLEANUP OK`. `-print` cùng `mapfile -t` cũng đếm dòng thay cho mục khi tên có newline. Dùng danh sách phân cách NUL và kiểm rc của phép quét trước mọi thao tác ghi/xoá. Ca: giả lập phép quét trả một mục rồi lỗi, xác nhận cả sổ phiên và output 11 giữ nguyên. Thêm ca tên chứa newline để kiểm đếm theo mục.

- **P1 — Đường dẫn qua symlink/junction ở thư mục cha vẫn được chấp nhận.** `.agents/skills/playwright-browser/SKILL.md:190,229,325,332,374–384`. Nếu một thành phần phía trên `daemon` là symlink hoặc junction trỏ sang cây khác, `daemon`, thư mục hash và tệp ở đích đều có thể là đối tượng thường. Kiểm tra hiện tại chấp nhận chúng và thao tác xoá chạy trong cây đích. Tương tự, thay thư mục hash bằng liên kết sau kiểm tra nhưng trước copy/xoá khiến các lệnh tra lại đường dẫn. Kiểm tra mọi thành phần trước Capture và Cleanup, xác lập vị trí và danh tính thư mục, dùng thao tác neo vào thư mục đã mở nếu cần bảo đảm trước việc thay thế đồng thời. Ca: executor dựng liên kết ở thư mục cha và ca hoán đổi thư mục sau khi quét, yêu cầu STOP và xác nhận đích nguyên vẹn. Tôi chỉ phân tích bằng đọc mã, không dựng các đường dẫn này.

- **P1 — Capture có thể quét khác sổ phiên mà CLI mở.** `.agents/skills/playwright-browser/SKILL.md:179–192,207,228–232,323–324,372–374`. Với `XDG_CACHE_HOME` tương đối, Capture Bash quét theo CWD của shell nhưng CLI chạy từ `work`. Nếu sổ CLI đã có `.err` cùng nonce, preflight có thể bỏ qua nó trước khi `startDaemon` mở với chế độ truncate. Cleanup lại từ chối đường dẫn tương đối sau khi đã chạy các lệnh CLI. PowerShell cũng dùng CWD khác CLI nếu `LOCALAPPDATA` là đường dẫn tương đối. Hai Capture còn tính cache mặc định dù hook test được đặt sau Kiểm pin. Kiểm lại môi trường ngay trước open, dùng cùng CWD và quy tắc chuẩn hoá với CLI ở mọi bước hoặc từ chối cache tương đối ngay ở Capture. Ca: đặt cùng nonce trong cache nhìn từ `work`, chạy preflight từ CWD khác với cache tương đối, yêu cầu không gọi open. Thêm ca hook được đặt sau Kiểm pin.

- **P2 — Quy tắc độ sâu và hoa thường của Capture chưa tương đương.** `.agents/skills/playwright-browser/SKILL.md:190,230–231,329,379–384`. Bash chỉ quét độ sâu 2 và so tên phân biệt hoa thường. PowerShell Capture dùng `-Recurse -Depth 1`, có thể nhận tên ở ngay gốc sổ phiên và chặn một lượt sạch ở độ sâu 2. Bộ lọc Windows cũng có thể tính bản viết hoa là mục trùng như N13, trong khi phép so tên tệp đích vẫn yêu cầu chữ thường. Duyệt đúng hai tầng một cách tường minh và ghi rõ quy tắc so tên theo nền tảng. Ca: mục cùng nonce chỉ ở gốc, mục ở độ sâu 2 và biến thể hoa ở thư mục hash khác, chạy trên cả hai shell Windows và Bash. Cache thiếu đã có C3/N12. Cache tồn tại nhưng rỗng riêng biệt chưa có ca. Bash dùng fallback với `XDG_CACHE_HOME` rỗng như CLI, PowerShell Windows bỏ qua biến này như CLI. Fallback Windows cần dùng cùng home thực tế với Node khi `LOCALAPPDATA` thiếu hoặc rỗng.

- **P2 — Gỡ bản cài Windows không bảo đảm giữ thư mục vừa có mục mới.** `.agents/skills/playwright-browser/SKILL.md:406–408`. Sau bước đếm rỗng, một tiến trình khác có thể tạo mục trước khi `Remove-Item` chạy. FileSystem provider có thể hỏi xác nhận xoá cả mục con. Dùng thao tác xoá thư mục nguyên tử ở chế độ không đệ quy, chẳng hạn `[IO.Directory]::Delete(path, $false)`, và ghi biên nhận nếu thư mục còn mục. Xác thực thư mục cha từ biên nhận thuộc đúng hash của bản cài và kiểm liên kết trước khi dùng. Ca: chèn một mục giữa bước đếm và xoá, xác nhận mục giữ nguyên và có biên nhận.

- **P2 — Ma trận chưa đo đầy đủ các chốt và assertions giữ nguyên tệp.** `ops/acceptance/wp1389/residue_matrix.sh:30–41,50–52,61–65,96–130` và `ops/acceptance/wp1389/residue_matrix.ps1:66–70,79,84–87,114–116,129–166`. Bash băm danh sách đường dẫn, kích thước và mtime của mồi, không băm nội dung từng tệp như RESULTS:57–58 mô tả. Hai harness thường chỉ kiểm tệp nonce chính còn tồn tại, không kiểm riêng `.session`/userdata vẫn nguyên trong N3/N4. P2 chỉ đo trạng thái thành công, L1 đo thêm bản sao nhưng không xác nhận tệp gốc đã mất. N13 không kiểm đích viết hoa còn nguyên vì bộ lọc mồi Windows loại tên đó. N8 chỉ dựng `11-daemon.err`, bỏ `11-daemon-path.txt`. Tách assertions theo từng tệp và kiểm bằng hash/nội dung, mtime, tồn tại và output mới vắng mặt khi phải dừng. Ca kiểm ma trận: thay đổi nội dung mồi rồi phục hồi mtime, hoặc xoá mục sót trước khi trả STOP, và xác nhận harness đánh trượt. Thêm ca lỗi copy/so byte/xoá, kiểm thứ tự verify → dọn → hash → thông báo và ca Gỡ có thư mục không rỗng.

- **P3 — Trích đoạn gồm cả hai marker.** `ops/acceptance/wp1389/residue_matrix.sh:12–20` và `ops/acceptance/wp1389/residue_matrix.ps1:13–26`. B6 yêu cầu trích byte giữa marker. Hai harness gồm cả marker, PowerShell còn ghi BOM và chuẩn hoá CRLF. Hành vi fixture hiện tại vẫn chạy được vì marker là comment. Tách byte nội dung và tính SOURCE trên đoạn gốc, dùng file wrapper riêng nếu cần BOM cho PS 5.1. Ca: so hash đoạn trích với khoảng byte độc lập từ SKILL và từ chối marker lệch cặp.

## Đối chiếu nguồn và phạm vi

- HEAD khớp HEAD_SHA.txt, cây sạch trước và sau kiểm. SHA-256 đặc tả khớp `12257fa8d659ff5c013af4bc31de700de4a53b085a99ec8c47cbd403d66610bc`. Ba tarball khớp SRI trong lockfile. Nội dung các tệp giải nén CLI/core khớp tarball.
- `registry.js:119–165` xác nhận hook test, cache Linux/Windows, thêm nhánh macOS ngoài phạm vi SKILL, và 16 hex đầu của SHA-1 trên `workspaceDir || packageRoot`. Với đường dẫn Linux trong RESULTS, SHA-1 bắt đầu `3815e4e10d63867a`. `session.js:73–97,121–126` xác nhận `deleteData` chọn đúng `.session` và tiền tố `ud-`, còn `startDaemon` mở `.err` với `w`. `serverRegistry.js:1786,1847–1848,1927–1928` xác nhận cache `ms-playwright/b`, hook test và thao tác unlink khi đóng. Kiểm mã client, README và session-management của gói ghim, không thấy tuỳ chọn được hỗ trợ để dời sổ phiên. Phương án (b) vẫn có căn cứ.
- B2/B5: thứ tự ở hai khối đầy đủ đặt bước mới sau các kiểm tra 08–10, trước hash và `CLEANUP OK`. Diff giữ nguyên Setup, Kiểm pin và các lệnh CLI 08–10. B4 có đối chiếu bản sao trước xoá ở cả hai shell. B8 liệt kê cả hai output và khai phạm vi tệp/thư mục cũ. Câu cam kết chỉ xoá đúng tệp phiên và ý nghĩa `CLEANUP OK` cần các sửa đổi trên. Limits cũng nên nêu fallback `LOCALAPPDATA` của Windows. Native chỉ đo cache đã tồn tại theo RESULTS:163–165.
- Ca không có đột biến đích riêng trên Bash: P1/P2, N1, N4, N6, N11, N12, C1–C3. Trên PowerShell: P1/P2, N1, N4–N6, N11–N13, L2, C1–C3. L1 có đột biến retry copy làm ca đỏ, chưa có ca hoặc đột biến buộc chạy retry xoá. Hai bản có đột biến cho chốt đúng một mục, lọc nonce, loại daemon liên kết/reparse, output cũ, hình dạng hash và hook. Chỉ Bash đo trực tiếp symlink tệp. Các ca fixture không đo toàn bộ Capture/Cleanup hay Gỡ.

## N1 độc lập

```text
SOURCE 92d1bde3a0c34f5a178b4c87e775555893017ee4b2c4a1dd820329f43f5c34b4 cleanup_frag ee956fa4b3e439ab43a777ef47ba0288e0d9ce9c1c24d9b51bb7837c57b6073c pre_frag c459af715dcd2a39f2f8a8787f317a47ed7e28aa3f2805ff47a5508488f72ca0
TONG: 30 dat / 30
```

## Không đo được và bằng chứng executor

- **N5-err-symlink trên Windows: KHÔNG ĐO ĐƯỢC**, SKIP trên cả PowerShell 5.1 và pwsh 7. Theo lời khai executor, N2 đạt 33/33 ở mỗi shell, rc 0, mỗi lượt có một SKIP. N4 ghi 0 tệp mới và 15 tệp `.err` cũ nguyên vẹn, gồm 13 tệp được chỉ định. Không có lượt Windows độc lập.
- N2–N4 được báo ở commit `783e219db3bf2985eb601b26f546d27d6bd99c1b`. Diff tới H chỉ thêm RESULTS và REVIEW-PROMPT, các byte SKILL và hai harness trùng. Đây là bằng chứng executor trên cùng nội dung thực thi, còn yêu cầu đo native trên chính H chưa được chứng minh. N3/N4 không chạy lại trong review. Cache mới tinh, thời gian nhả handle thực và trạng thái CI/doctrine-scan trên H chưa được xác minh. Các finding từ đọc mã chưa được tái hiện bằng fixture ngoài lượt N1.

## Lệnh đã chạy

- `pwd`, `ls -la`, `cat HEAD_SHA.txt`, `git -C repo rev-parse HEAD`, `git -C repo status --porcelain=v1 --untracked-files=all`, `sha256sum repo/ops/specs/wp1389-r1.md`, `ls pwsrc`, `ls -la scratch` và `cat` đặc tả/lease — rc 0.
- `mkdir scratch/n1 && bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1` — rc 0, chạy đúng một lần.
- `git -C repo diff eca1d125b8..HEAD -- .agents/skills/playwright-browser/SKILL.md` và đọc RESULTS/harness bằng `nl -ba`, `sed`, `head`, `tail` — nhóm lệnh rc 0.
- `rg -n`, `rg -in`, `sed -n` để đọc registry, session, serverRegistry, client program, README và session-management, cùng `printf %s /tmp/claude-0/tlpw-base/install/0.1.0/node_modules/playwright-core | sha1sum` — nhóm đọc nguồn cuối rc 0.
- `cat repo/.agents/skills/playwright-browser/package-lock.json` — rc 0. Hai lượt `python -` đầu kiểm SRI tìm nhầm tên `cli-0.1.23.tgz`, mỗi lượt rc 1. Lượt `python -` đã sửa tên tarball, kiểm SHA-512/base64 và so tệp giải nén — rc 0.
- `git -C repo diff --name-status 783e219db3bf2985eb601b26f546d27d6bd99c1b HEAD`, `sha256sum repo/ops/acceptance/wp1389/residue_matrix.{sh,ps1}`, `git -C repo diff --check eca1d125b8..HEAD`, `git -C repo diff --exit-code 783e219db3bf2985eb601b26f546d27d6bd99c1b HEAD -- .agents/skills/playwright-browser/SKILL.md ops/acceptance/wp1389/residue_matrix.sh ops/acceptance/wp1389/residue_matrix.ps1` và kiểm status lại — rc 0.
