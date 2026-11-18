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

## Lượt 2 (Codex CLI, 2026-11-18T10:52:06Z → 10:56:11Z, rc 0; chép nguyên văn `scratch/VERDICT.md`)

# WP1389 r1 — review độc lập lượt 2

reviewed_sha: f2654b2f6b8d7445db93b60b4a2fb41aca9364ac
verdict: request_changes
reviewer: codex (OpenAI), codex_cli, read-only

## Findings P0–P3

- **P1 — Capture dừng trước open nhưng vẫn chỉ dẫn chạy Cleanup trên nonce đã có chủ.** `.agents/skills/playwright-browser/SKILL.md:172,184,192,241,292,309–320,357–378`. Khi preflight phát hiện trùng nonce với một phiên đang chạy của cùng bản cài, Bash in “chạy Cleanup” và phần Capture chỉ dẫn Cleanup khi lỗi. Cleanup chỉ kiểm cú pháp nonce rồi gọi `08-close` và `09-delete-data`. CLI tra phiên theo nonce và dừng phiên tìm thấy (`program.js:115–122,162–166`). Hai phản hồi vẫn có thể khớp mẫu, sau đó bước mới có thể xoá chính `.err` của phiên đó. Sửa bằng cách ghi trạng thái preflight và launch attempt gắn với run, yêu cầu trạng thái này trước cả `08-close`, và đổi chỉ dẫn khi dừng trước open. Giữ đường Cleanup cho lần open đã được thử sau preflight thành công nhưng thất bại giữa chừng. Ca: nonce trùng với một phiên fixture đang mở, preflight STOP, rồi thử đi qua entry point Cleanup với CLI giả. Kiểm không có lệnh 01 hoặc 08–10, không có output 11 và phiên cũ nguyên vẹn. Thêm đối chứng open đã được thử nhưng trả lỗi.

- **P1 — Preflight bỏ qua thư mục mà CLI vẫn dùng.** `.agents/skills/playwright-browser/SKILL.md:189–194,231–243,337–345,388–400`. Bash `find` không đi qua symlink tại gốc daemon hoặc thư mục hash. PowerShell đi qua junction ở gốc daemon nhưng bỏ qua junction hash. CLI dùng `stat` và đọc theo đường dẫn đó (`registry.js:92–103`), còn `startDaemon` mở `.err` bằng `w`. Nếu thư mục daemon thực của bản cài nằm sau liên kết bị preflight bỏ qua, Capture có thể chạm phiên có sẵn hoặc truncate `.err` trước khi chốt Cleanup chạy. Cleanup cũng có thể đếm một mục thường, bỏ qua mục cùng nonce ở nhánh hash liên kết rồi báo thành công trong khi cây CLI đọc vẫn còn mục. Kiểm daemon và hash đích của bản cài trước open, dừng khi chúng là liên kết/reparse point. Với các hash khác, giữ quy tắc không đi xuyên B3 và ghi rõ giới hạn của phép đếm. Ca executor: đặt mục trùng nonce sau liên kết ở daemon hoặc hash đích, yêu cầu STOP trước open và dữ liệu đích nguyên vẹn. Thêm đối chứng có một `.err` thường và dư lượng sau liên kết hash thực của phiên. Các tình huống liên kết ở đây chỉ được mô tả bằng lời.

- **P1 — Sổ phiên và đường dẫn đích chưa được ràng buộc xuyên suốt run.** `.agents/skills/playwright-browser/SKILL.md:179–180,190–192,210–211,233–239,334–349,384–411,437–440`. Bash đọc cả `XDG_CACHE_HOME` chỉ là biến shell, trong khi Node chỉ thấy giá trị đã export. Một giá trị cache thay đổi giữa Capture và Cleanup cũng khiến phiên được preflight ở một sổ nhưng các lệnh đóng/xoá chạy ở sổ khác. Phép nối chuỗi Bash giữ thành phần đường dẫn mà `path.join` của CLI chuẩn hoá, nên khi đường dẫn có liên kết ở phần cha, việc phân giải có thể khác ngay với cấu hình tĩnh. Kiểm tra trước open và trước bất kỳ lệnh Cleanup nào bằng cache tuyệt đối tính từ môi trường thực của Node và chuẩn hoá đúng như CLI. Ràng buộc sổ phiên, hash dự kiến và định danh run. Từ chối sai lệch. Chấp nhận cấu hình cha là liên kết tĩnh chỉ khi đã xác định và kiểm cùng đích suốt run. Việc không chống tiến trình cùng người dùng chủ động tráo thư mục có thể là giới hạn nếu nêu rõ giả định cache tin cậy, ổn định. Chỉ ghi Limits như hiện tại vẫn chặn merge vì không xử lý sai lệch tĩnh hoặc đổi môi trường giữa các bước, và tên nonce không xác nhận cây đích. Ca: biến cache chỉ đặt trong Bash, đổi cache giữa hai bước, và executor dựng liên kết ở phần cha với đường dẫn có bước chuẩn hoá. Kiểm phép quét và CLI cùng thấy một sổ hoặc STOP trước mọi thao tác trên phiên, và cây kia nguyên vẹn. Đường dẫn thoát cây chỉ được phân tích bằng lời.

- **P2 — Harness tính hash nonce sau khi chạy đoạn cần kiểm.** `ops/acceptance/wp1389/residue_matrix.sh:54–57,69–102`, `ops/acceptance/wp1389/residue_matrix.ps1:79–84,108–141`. N3/N4 và nhiều ca âm khác dựng dữ liệu đúng, nhưng `sha`/`Sha` của tệp phải giữ được đánh giá khi gọi assertion sau `run_frag`/`Run-Frag`. Nếu đoạn dọn sửa `.session` hoặc `Prefs` và trả STOP, giá trị kỳ vọng đã là hash sau sửa. Tệp mất có thể làm ca hỏng, nhưng nội dung nguyên vẹn chưa được đo. Cả hai N8 cũng không buộc output 11 còn lại phải vắng. PS N15 không kiểm tệp nonce bị che sau khi gỡ ACL. Chụp tồn tại, loại, SHA-256 và mtime trước khi chạy, rồi kiểm lại sau khi khôi phục ACL cho N15. Ca tự kiểm: sửa một byte trong tệp nonce rồi trả STOP, hoặc tạo output 11 còn lại trong N8. Harness phải báo FAIL ở đúng ca.

- **P2 — Chốt đường dẫn Windows chưa tương đương cách CLI nhận cache tuyệt đối.** `.agents/skills/playwright-browser/SKILL.md:233–239,385–395`. Regex chỉ nhận dấu gạch ngược. Node `path.win32` coi `C:/Cache` và UNC dạng gạch xuôi là tuyệt đối rồi chuẩn hoá chúng, còn hai đoạn PS dừng. UNC chuẩn với dấu gạch ngược qua regex, nhưng regex một mình cũng nhận tiền tố UNC thiếu cấu trúc và đường dẫn namespace thiết bị. Chuẩn hoá theo cách CLI dùng rồi kiểm drive-absolute/UNC hợp lệ, với phạm vi namespace được công bố. Ca: ổ đĩa dùng cả hai dấu phân cách, UNC chuẩn và UNC gạch xuôi, đường dẫn UNC không hợp lệ, cache rỗng/thiếu và UNC không truy cập được. Yêu cầu đường dẫn hợp lệ cùng kết quả với CLI, lỗi liệt kê phải STOP. Chỉ kiểm logic Node và đọc mã, chưa chạy PS/UNC.

- **P2 — Bằng chứng Gỡ Windows chưa đo lệnh giao cho operator.** `.agents/skills/playwright-browser/SKILL.md:421–424`, `ops/acceptance/wp1389/RESULTS.md:145–155,182–183`. Lệnh không đệ quy mới giải quyết cửa sổ thư mục có mục mới trong finding cũ. N4 vẫn dùng đếm rồi `Remove-Item`. Văn xuôi chỉ xác thực dạng hash và vị trí dưới sổ phiên, thiếu đối chiếu với hash thực của bản cài và loại thư mục. Nếu biên nhận nhầm sang hash rỗng của bản cài khác thì có thể xoá thư mục đó. Đối chiếu hash với đường dẫn package root thực của bản cài và xác thực danh tính/loại thư mục trước khi dùng biên nhận. Chạy N4 bằng chính lệnh mới. Ca: đối chứng hash rỗng hợp lệ, một hash rỗng của bản cài khác, và thư mục đúng có mục được thêm ngay trước khi xoá. Giữ nguyên hai ca sau và ghi biên nhận.

- **P2 — Bash thêm phụ thuộc phiên bản ở sau bước thay đổi trạng thái phiên.** `.agents/skills/playwright-browser/SKILL.md:316–341,427–429`. `mapfile -d ''` cần Bash ≥4.4 theo chính chú thích, nhưng không có kiểm phiên bản trước Capture hoặc trước 08–10. Trên Bash cũ, người dùng có thể tạo phiên rồi chỉ phát hiện không dọn được dư lượng sau khi phiên đã đóng. Mã thoát của `mapfile` cũng bị bỏ qua dưới `set -u`. Khai báo/kiểm điều kiện phiên bản sớm hoặc dùng phép quét tương thích, và yêu cầu cả mã đọc lẫn mã quét thành công. Ca: Bash tối thiểu được hỗ trợ chạy danh sách NUL và quét trả dữ liệu rồi lỗi; shell thấp hơn dừng trước 01 và 08; lỗi đọc danh sách giữ nguyên tệp và output.

- **P3 — Thứ tự hiện tại khác câu chữ B4 và chưa có ca lỗi đối chiếu.** `.agents/skills/playwright-browser/SKILL.md:304–305,347–349,404–412`, `ops/specs/wp1389-r1.md` §3 B4. Cả hai thực thi chép → so → ghi đường dẫn → xoá. Điều này giữ nguyên tệp gốc nếu không ghi được đường dẫn và phù hợp văn xuôi SKILL. B4 liệt kê ghi đường dẫn trước chép. Khi copy hay so thất bại, hiện trạng có thể để lại bản sao dở mà thiếu đường dẫn gốc. Chốt thứ tự với chủ spec hoặc tuân theo B4 theo nghĩa thứ tự, tiếp tục yêu cầu đủ bằng chứng trước xoá. Ca: copy lỗi, byte lệch và ghi đường dẫn lỗi, kiểm tệp gốc nguyên, trạng thái từng output theo thứ tự đã chốt, không hash thành công và không `CLEANUP OK`.

## Từng finding lượt 1 tại H

| Finding lượt 1 | Trạng thái và căn cứ mã |
|---|---|
| P1 tên sai hậu tố | **Đã sửa.** Bash so basename bằng chuỗi ở SKILL:343–345. PS dùng `-ceq` ở 399. N14 và hai mutant đích kiểm chốt này. |
| P1 quét thiếu, tên newline | **Đã sửa đối với rc của scanner.** Bash dùng NUL và `wait "$!"` ở 341–342. PS dùng .NET trong `try/catch` ở 237–240,393–397, thay nhánh bỏ sót W3. Còn chốt mã đọc `mapfile` và tương thích phiên bản ở finding trên. |
| P1 liên kết cha, tráo thư mục | **Chưa sửa bằng mã.** Các chốt 337,345,390,394,400 chỉ xét daemon/hash/tệp; 347–349 và 404–412 tra lại đường dẫn. Limits 438–440 nói rõ. Chấp nhận giả định không có tiến trình cùng người dùng chủ động tráo thư mục nếu cache tin cậy và ổn định. Liên kết cha tĩnh vẫn cần cùng đích đã xác nhận, nên ghi Limits đơn thuần chưa đủ để merge. |
| P1 cache tương đối và hook sau Kiểm pin | **Sửa một phần.** 190–192,232–235,334–336,384–387 thêm kiểm hook và đường dẫn tương đối thông thường. Vẫn ghép đường dẫn ngoài môi trường CLI và không ràng buộc sổ qua các bước. Cleanup kiểm hook sau 08–10 đúng vị trí B2 cho bước mới, nhưng cần chốt provenance trước 08 để bảo vệ lệnh CLI vốn có. |
| P2 độ sâu, hoa thường, cache trống | **Sửa một phần.** 237–239 và 393–396 duyệt hai tầng trực tiếp, tương ứng độ sâu 2 ở 192,341. Bash phân biệt hoa thường. PS Windows có đếm biến thể hoa theo N13 executor, rồi yêu cầu basename và hash thường ở 399–400. Bash XDG rỗng dùng fallback, PS Windows bỏ qua XDG và LOCALAPPDATA rỗng dùng USERPROFILE. Hai Capture cho qua sổ thường rỗng/thiếu, hai Cleanup dừng (rỗng là zero match, thiếu là lỗi loại sổ). Chưa có fixture riêng cho sổ tồn tại nhưng thật sự rỗng hoặc fallback Node khi biến home thiếu/lệch. |
| P2 Gỡ Windows race đếm rồi xoá | **Sửa một phần.** SKILL:421–424 dùng xoá thư mục không đệ quy. Xác thực biên nhận/đúng hash chưa đủ và N4 chưa đo lệnh mới. |
| P2 assertions và độ phủ | **Sửa một phần.** Bash:37–38 và PS:57–60 băm mồi. Bash:63–66 và PS:85–88,103–106,143–145 kiểm nguồn mất và bản sao. N8 đã có cả hai tên. PS:131–133 đã bao gồm tệp hoa trong snapshot, W4 có kiểm cỡ fixture. Hash nonce sau thao tác, lỗi copy/compare và Gỡ không rỗng còn thiếu như trên. |
| P3 byte giữa marker | **Đã sửa trên H.** Bash:14–24 và PS:14–31 bỏ marker, kiểm cặp, hash đúng nội dung LF tại H. BOM dành cho tệp chạy PS. Tôi đối chiếu byte độc lập cho cả hai cặp của mỗi shell, hash Bash khớp tệp trích, hash PS khớp tiền tố trong RESULTS. |

## Nguồn ghim, B1–B8 và các kiểm tra delta

- HEAD khớp `HEAD_SHA.txt`, cây sạch trước và sau. SHA-256 đặc tả khớp `12257fa8d659ff5c013af4bc31de700de4a53b085a99ec8c47cbd403d66610bc`. Ba tarball đều khớp SRI. So từng tệp thường trong hai tarball có cây giải nén, CLI 16 tệp và core 116 tệp, đều trùng.
- Core ghim `registry.js:119–165` xác nhận hook test có giá trị, Linux `XDG_CACHE_HOME || os.homedir()/.cache`, Windows `LOCALAPPDATA || os.homedir()/AppData/Local`, thêm macOS ngoài phạm vi SKILL, nối `ms-playwright/daemon` và lấy 16 hex đầu SHA-1 của `workspaceDir || packageRoot`. Đường dẫn package root mẫu cho `3815e4e10d63867a`. `session.js:73–97,121–126` xác nhận `deleteData` chọn đúng `.session`/tiền tố `ud-` theo phiên, còn `.err` mở với chế độ `w`. `serverRegistry.js:1816–1819,1847–1848,1918–1928` xác nhận cache `ms-playwright/b`, hook test và unlink descriptor có nuốt lỗi. README, session-management, help và client không có tuỳ chọn được hỗ trợ để dời sổ phiên. Phương án (a) vẫn không khả dụng.
- B1–B4 có các lỗ hổng ở Findings. B2/B5 đặt bước dọn ở sau verify và trước hash/thông báo ở SKILL:328–353,381–417. Diff giữ nguyên Setup, Kiểm pin và khối 08–10. Chốt cũ yêu cầu close thực sự trả `closed`. CLI trả `not-open` nếu chưa mở, nên vẫn giữ hành vi STOP khi thực sự không có phiên. Chỉ dẫn Cleanup sau khi preflight dừng là hồi quy mới khi có phiên khác trùng nonce.
- Bash 5.2.21: probe `mapfile` đọc được một mục NUL, trả 0, `wait "$!"` trả đúng 7 từ process substitution. `${f##*/}` là đối chiếu tên nguyên văn. Dấu `/` cuối XDG làm đường dẫn có hai slash ở giữa, GNU find trên máy này giữ nguyên tiền tố, nên `${h%/*} = $D` vẫn đúng. Probe dùng fixture thường bên trong scratch, không chạy lại ma trận.
- PowerShell: chốt Attributes chặn reparse point tại daemon trong Cleanup và lọc thư mục con trước khi liệt kê ở cả hai đoạn. Capture thiếu chốt root như finding. Mẫu `*nonce*` có thể chịu ngữ nghĩa wildcard theo nền tảng, nhưng nonce hiện tại dài 18 ký tự, vượt toàn bộ tên ngắn 8.3 kể cả dấu chấm, nên chính bí danh 8.3 không thể chứa nguyên nonce. Chưa đo case-sensitive directory trên Windows. UNC thường được phân tích ở finding đường dẫn.
- B6 đạt trên byte hiện tại. B7 cần sửa/đo như finding Gỡ. B8 có cả hai output và khai đúng ba loại thư mục còn lại, `.err` cũ và lý do không chọn (a). Câu “chỉ xoá tệp của mình” quá rộng khi thiếu provenance. Câu descriptor trong `b` được xoá khi close cần nói đây là thao tác CLI cố thực hiện, vì mã ghim bỏ lỗi unlink. Ca giới hạn: giả lập unlink descriptor lỗi, xác nhận tài liệu và biên nhận phân biệt sổ trình duyệt với phép dọn `.err`.

## N1 độc lập

```text
SOURCE c3b07090ba6352e65792eeaaa93bd2f408acc0f37f3407b28db4f4975bcdef34 cleanup_frag 04aec5e00ca2cd17ebbdd5f8163c55a776433135dc436c4a6fa4b89dbba6a955 pre_frag 25375d548f85ce9a7b9270758a60e31fec47675ffdcff620df6f2725dcafa12a
TONG: 39 dat / 39
```

- Bash không có đột biến đích riêng cho P1/P2, N1, N4, N6, nhánh N8-path, N11–N12, N16 và C1–C3/C6. N16 đo có nhiều mục chứa nonce nhưng cũng có thể qua với một scanner đếm dòng. Chưa khoá được yêu cầu NUL. N7 mutant bỏ guard đồng thời bật follow, nên không cô lập guard. N15 có đột biến trực tiếp cho rc quét. C4 baseline có mục trùng trong cwd của runner, nhưng mutant bỏ tệp nonce, và cả hai dùng một cwd thay vì mô phỏng cwd riêng của CLI. C4 chứng minh guard tương đối, chưa tái hiện lệch CWD qua entry point.
- PS không có đột biến đích riêng cho P1/P2, N1, N4–N6, nhánh N8-path, N11–N13, L2, C1–C3/C6. N5 SKIP. N6 đặt junction làm nhánh nonce duy nhất, N7 đo từ chối root trong Cleanup. Cả hai không đo root/hash liên kết trước open. W4 được khoá bằng kiểm cỡ fixture. L1/L3 kiểm retry đọc/xoá dưới khoá mô phỏng và có mutant. L2 kiểm timeout đọc, chưa kiểm timeout xoá. Các ca STOP có tên đúng nhưng phần hash nonce, output N8 đối ứng và N15 bị che có giới hạn như finding. Các harness trích đoạn nên không đo thứ tự thực của toàn khối, kể cả việc Cleanup chỉ chạy sau Capture đã thử open, các chốt 08–10, hash cuối, thông báo cuối và Gỡ.
- Thiếu ca với thư mục daemon rỗng thật sự, XDG rỗng, LOCALAPPDATA rỗng hoặc thiếu, UNC, lỗi ghi output/copy/so byte, và Uninstall còn mục. C1 là sổ có mồi, C3 là sổ thiếu, N1 là sổ có mục nhưng không có tên trùng. Các trạng thái này khác thư mục daemon rỗng.

## KHÔNG đo được

- **N5-err-symlink trên Windows: KHÔNG ĐO ĐƯỢC.** Theo lời khai executor, cả PS 5.1 và pwsh 7 ở `6896f164db73a16c6c4f92d02cd556dad1c1b3c4` đạt 44/44 rc 0, mỗi shell một SKIP. N4 báo 0 tệp mới và 15 `.err` cũ nguyên vẹn, gồm 13 tệp được chỉ định. N3 báo snapshot trước/sau trùng byte. N2–N4 là lời khai executor, không có lượt Windows hoặc native độc lập tại đây.
- So diff xác nhận SKILL và hai harness ở commit đo giống H. N2–N4 chưa được chứng minh chạy trên chính H theo yêu cầu exact head, và N4 chạy cách Gỡ cũ. Cache mới tinh, thời gian daemon nhả handle thật sau verify, PowerShell với UNC/case-sensitive directory, Bash 4.4, và CI/doctrine-scan ở H chưa được xác minh. Tôi không dựng fixture thoát cây hay chạy CLI ghim.

## Lệnh đã chạy và mã thoát

- `ls -la`, `ls -la scratch pwsrc`, `cat HEAD_SHA.txt`, `git -C repo rev-parse HEAD`, `git -C repo status --porcelain` và `--porcelain=v1 --untracked-files=all`, `sha256sum repo/ops/specs/wp1389-r1.md`, và `cat` spec/lease/VERDICT lượt 1/package-lock — rc 0.
- `mkdir scratch/n1 && bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1` — rc 0, đúng một lần.
- `git -C repo diff eca1d125b8..HEAD -- .agents/skills/playwright-browser/SKILL.md`, `git -C repo log -8 --oneline`, `git -C repo rev-parse 6896f16`, `git -C repo diff --name-status 6896f16 HEAD` và `eca1d125b8..HEAD`, `git -C repo diff --exit-code 6896f16 HEAD -- .agents/skills/playwright-browser/SKILL.md ops/acceptance/wp1389/residue_matrix.sh ops/acceptance/wp1389/residue_matrix.ps1` — rc 0.
- `git -C repo diff --check eca1d125b8..HEAD` — rc 2, hai khoảng trắng cuối dòng Markdown trong VERDICT lượt 1. Cùng lệnh giới hạn SKILL, hai harness và RESULTS — rc 0.
- Các lệnh đọc `rg`, `nl -ba`, `sed -n`, `tail`, `head`, `cut` trên SKILL, harness, RESULTS, registry/session/program/output/serverRegistry, help và tài liệu ghim — các nhóm đọc rc 0.
- Hai lệnh `python -` kiểm SRI và so tệp giải nén, rồi đối chiếu byte giữa marker — rc 0. `printf %s /tmp/claude-0/tlpw-base/install/0.1.0/node_modules/playwright-core | sha1sum` — rc 0.
- `bash --version | head -1`, probe GNU `find` trên fixture sẵn có với slash kép và `test` so thư mục cha — rc 0. Probe `bash -c` cho `mapfile`/process substitution — rc wrapper 0, `mapfile` 0, `wait` 7. `node -p process.version` và `node -e` kiểm `path.win32.isAbsolute/join` — rc 0. `command -v pwsh` — rc 1.

## Lượt 3 (Codex CLI, 2026-11-18T11:50:52Z → 11:55:26Z, rc 0; chép nguyên văn `scratch/VERDICT.md`)

# WP1389 r1 — review độc lập lượt 3

reviewed_sha: 86879e1a77b0c89d68b5a0695eab5de1969c6f90  
verdict: request_changes  
reviewer: codex (OpenAI), codex_cli, read-only

## Findings chặn merge

- **P1 — Bản ghi sổ phiên dùng được với nonce của run khác.** `.agents/skills/playwright-browser/SKILL.md:177–178,195–204,209–211,242–259,325–341,380–408`. Hai Capture chỉ lưu hai đường dẫn dùng chung cho mọi run của cùng bản cài. Nếu Cleanup giữ `TL_PW_RUN` của A nhưng lấy `TL_PW_SESSION` của B đang mở trên cùng bản cài, bản ghi của A vẫn khớp. Cả hai wrapper truyền B cho CLI. `registry.js:51–54` tìm theo tên và `program.js:115–122,162–166` thực thi trên phiên đó. Nếu B đóng thành công và chỉ còn đúng `.err`, Cleanup xoá tệp của B, ghi bằng chứng vào A và có thể in `CLEANUP OK`. Tôi xác nhận riêng chốt Bash ở đầu Cleanup chấp nhận nonce mồi trên fixture D4, rc 0, chưa gọi CLI. Gắn nonce với bản ghi của run, kiểm trước 08 và ghi trạng thái đã bắt đầu lần gọi native open sát điểm launch, sau các kiểm tra và chuẩn bị output. Từ chối marker cũ hoặc liên kết. Ca: toàn khối với CLI giả, hai nonce hợp lệ cùng install, ghép run A/nonce B, yêu cầu không gọi 08–10 và cả hai cây nguyên vẹn. Thêm hai đối chứng preflight qua nhưng launcher dừng trước gọi native, và launch đã thử nhưng trả lỗi giữa chừng.

- **P1 — Kiểm loại sổ phiên sau thao tác CLI là quá muộn.** `.agents/skills/playwright-browser/SKILL.md:328–341,359–362,384–408,417–421,449–455`. Sau Capture, nếu daemon hoặc hash đích được đổi thành symlink/junction rồi giữ nguyên trước khi bắt đầu Cleanup, hai dòng trả về vẫn giống biên nhận. CLI đi qua liên kết khi tải phiên (`registry.js:92–107`); 08 có thể đóng phiên ở đích và 09 có thể xoá dữ liệu trước khi chốt B2/B3 từ chối. Kịch bản này xảy ra giữa hai lần gọi độc lập, không cần tráo thư mục đúng lúc đang quét hay xoá. Gỡ cũng đối chiếu chuỗi rồi gọi xoá thư mục, thiếu kiểm loại ở vị trí được phép gỡ. Thêm kiểm hook, loại daemon/hash và vị trí đích thực trước 08, kiểm lại ở bước B2/B3, và kiểm loại/vị trí trước Gỡ. Nếu cho phép liên kết cha tĩnh, lưu và đối chiếu đích vật lý lúc Capture và lúc Cleanup/Gỡ. Ca do executor dựng: thay daemon hoặc hash bằng liên kết trước khi bắt đầu Cleanup, yêu cầu STOP trước 08 và giữ nguyên đích, rồi kiểm Gỡ giữ nguyên liên kết và ghi biên nhận. Tôi chỉ mô tả tình huống liên kết ngoài cây bằng lời.

- **P2 — Kênh stdout PowerShell có thể giải mã sai đường dẫn cache Unicode.** `.agents/skills/playwright-browser/SKILL.md:242–256,384–390`. JS không có dấu nháy nhúng và đường dẫn module không có dấu gạch cuối, nên cách truyền argv dùng được theo ngữ nghĩa dự kiến của native binding 5.1/7, kể cả khoảng trắng. Vấn đề ở đầu ra: Node ghi chuỗi UTF-8 vào pipe, trong khi PowerShell đọc stdout native theo encoding của console. Trên Windows PowerShell 5.1 với code page OEM, cache hợp lệ chứa ký tự ngoài ASCII có thể bị đổi tên khi đọc. Khi đường dẫn đã đổi tên không tồn tại, preflight bỏ quét, ghi biên nhận đường dẫn sai và open vẫn dùng sổ thật. Cleanup lại giải mã giống vậy, qua chốt đầu, rồi dừng sau 08–10 vì không tìm thấy sổ để dọn. Nếu sổ thật đã chứa nonce, preflight còn có thể bỏ lọt mục trùng trước khi CLI mở stderr bằng chế độ truncate. Dùng giao thức ASCII (chẳng hạn base64 của UTF-8, giải mã tường minh ở PS) hoặc lấy byte stdout thô và giải mã UTF-8 tường minh, áp dụng cả Gỡ. Ca trên 5.1 và 7: work và LOCALAPPDATA chứa khoảng trắng và Unicode dưới console không phải UTF-8, đặt mục trùng ở cache thật và kiểm STOP trước open; đối chứng sạch phải ghi đúng đường dẫn và dọn được. Đây là kết luận đọc mã, chưa chạy trên Windows.

- **P2 — Chưa đủ bằng chứng nghiệm thu theo điều kiện exact H và phạm vi chốt.** `ops/acceptance/wp1389/RESULTS.md:84–115,123–133`, `ops/acceptance/wp1389/residue_matrix.sh:58–67,115–140,178–193`, `ops/acceptance/wp1389/residue_matrix.ps1:40–44,173–194,241–263`. N2/N4 được khai ở `07efca6`, N3 mới ở `4d8e9a7`. Tôi xác nhận byte SKILL/harness có liên quan trùng như mô tả bên dưới. Spec §5 yêu cầu exact commit. Fragment D1–D4 cũng dừng trước 08 theo cấu tạo runner, nên có thể xanh dù khối giao cho operator gọi 08 trước chốt hoặc chấp nhận ghép run/nonce. Sau khi xử lý các finding trên, ghi bằng chứng gắn đúng SHA ứng viên theo spec và đo toàn luồng với CLI giả có nhật ký cho 01/08–10, lỗi ghi đường dẫn/copy/so byte/xoá, thứ tự verify → dọn → hash → thông báo, và Gỡ với biên nhận sai. Một mutant chuyển chốt D1 sau 08 phải làm ca toàn khối đỏ.

## Từng finding lượt 2 tại H

| Finding lượt 2 | Trạng thái tại H và căn cứ |
|---|---|
| P1 dừng trước open nhưng Cleanup đụng phiên cũ | **Sửa một phần.** SKILL:192–204,241–259 ghi marker sau preflight, có hướng dẫn STOP đúng cho nhánh đó. SKILL:325–341,380–408 từ chối thiếu marker trước 08. Marker chưa gắn nonce hoặc launch attempt. Bash:187–191 còn trap khuyên Cleanup nếu pin, URL hoặc ghi config lỗi trước khi vào preflight; chốt đầu sẽ từ chối run mới thiếu marker. Sửa cả thông báo ở các nhánh này. |
| P1 daemon/hash liên kết bị preflight bỏ qua | **Sửa một phần.** Bash:199,361 và PS:249–254,420–427 chặn liên kết ở gốc/hash của chính bản cài tại preflight và đoạn dọn. Vẫn thiếu kiểm trước 08 sau khi quay lại Cleanup. PS kiểm loại ở preflight sau `Test-Path`; thêm ca liên kết gãy và lỗi truy cập để xác nhận provider cho kết quả dừng. |
| P1 neo sổ phiên xuyên run | **Sửa một phần.** SKILL:195–201,242–256,328–333,384–390 dùng Node từ work, rồi so base và hash trước 08. SKILL:369,430 buộc đúng đường dẫn của bản cài. Biến Bash chưa export và phép ghép đường dẫn riêng đã được xử lý; danh tính run/nonce và đích vật lý vẫn thiếu. |
| P2 expected hash được tính sau thao tác | **Đã sửa các lỗi chính.** Bash harness:51–75,89–98 và PS:73–97,128–144 chụp trước khi chạy, kiểm N8 cả output đối ứng. PS:155–158 kiểm hash mục bị ACL che sau khi gỡ ACL, còn thiếu snapshot đầy đủ loại/mtime cho riêng mục đó. |
| P2 cache tuyệt đối Windows | **Sửa một phần.** SKILL:245–248 lấy đầu ra đã chuẩn hoá của Node, xử lý cấu hình drive/UNC dùng dấu gạch xuôi theo quy tắc Node. Còn namespace đặc biệt không được quy định tường minh, UNC chuẩn/chia sẻ lỗi và Unicode chưa được chứng minh trên 5.1/7. UNC có thể được provider hoặc .NET biểu diễn khác chuỗi dùng trong phép so tuyệt đối ở :430. |
| P2 Gỡ Windows chưa đo lệnh giao cho operator | **Sửa một phần.** SKILL:449–455 hỏi lại trước xoá install, so đúng hash bản cài và dùng thao tác không đệ quy. RESULTS:126,132–133 khai đã dùng chính thao tác mới và phản chứng thư mục không rỗng ở commit đo. Thiếu kiểm loại ở Gỡ và ca biên nhận/hash sai trên khối hoàn chỉnh. |
| P2 Bash tối thiểu và rc của mapfile | **Đã sửa đường vận hành từ Capture.** SKILL:193–194 chặn Bash dưới 4.4 trước open, :366–367 kiểm cả rc đọc và rc scanner, :469 khai điều kiện. Cleanup chạy riêng dưới Bash cũ với run đã mở từ Bash mới vẫn thiếu guard trước 08. Đưa kiểm phiên bản lên đầu Cleanup và đo cả hai entry point. |
| P3 thứ tự B4 và lỗi đối chiếu | **Đã sửa thứ tự; đo một phần.** SKILL:371–373,432–442 thực hiện ghi đường dẫn → chép → so → xoá. PS harness:170–171 đo đường dẫn có trước khi copy vì bị khoá; chưa có ca lỗi compare hoặc ghi đường dẫn buộc giữ nguồn và thiếu thông báo thành công. |

## Đối chiếu nguồn và B1–B8

- HEAD khớp `HEAD_SHA.txt`. Cây sạch. SHA-256 spec khớp `12257fa8d659ff5c013af4bc31de700de4a53b085a99ec8c47cbd403d66610bc`. Cả ba tarball khớp SRI trong lockfile; đối chiếu thêm 16 tệp CLI và 116 tệp core đã giải nén với tarball.
- `registry.js:119–165` xác nhận hook test có giá trị, fallback Linux và Windows, nhánh macOS ngoài phạm vi, và 16 hex đầu SHA-1 của `workspaceDir || packageRoot`. `package.js:38` đặt package root tại gốc gói core. Entry point `playwright-cli.js` gọi `cli-client/program.js`, và `program.js:61` dùng chính `createClientInfo()`. Đọc README, help, session-management và client ghim, không thấy tuỳ chọn được hỗ trợ để dời sổ phiên. `--profile` chọn user-data, `--global` của install chọn nơi cài skill. Phương án (a) vẫn không khả dụng.
- `session.js:73–97,121–126` xác nhận delete-data chỉ chọn đúng `.session` và tiền tố userdata của phiên, startDaemon mở `.err` bằng `w`. `serverRegistry.js:1816–1819,1847–1848,1927–1928` xác nhận `ms-playwright/b`, hook test và xoá descriptor có bỏ lỗi unlink. Limits tại SKILL:461–472 khai đúng hành vi cố xoá descriptor và dư lượng thư mục/`.err` cũ; nên ghi thêm fallback Windows khi LOCALAPPDATA thiếu/rỗng. Evidence tại :294–297 liệt kê cả hai output.
- B1/B2: Bash dùng cùng Node, CWD work và môi trường export trong `chay_ghi` và probe; PS dùng cùng môi trường tiến trình, `Push-Location` cho native probe và `-WorkingDirectory` cho CLI. Chốt workspace ngăn đổi sang cách tính hash theo workspace. Bash thử nguồn thật cho XDG rỗng và slash cuối: fallback và chuẩn hoá của CLI đúng, bỏ rủi ro so prefix chứa slash kép. Cache thiếu/rỗng đi qua preflight khi đọc được; Cleanup từ chối thiếu sổ hoặc zero match. PS có thêm rủi ro decoding ở finding trên.
- B3/B4: cả hai chỉ dọn đúng đường dẫn dòng 2 cộng nonce; bỏ qua symlink/junction ở các thư mục hash khác khi quét. Bash tìm phân biệt hoa thường. Windows dùng đối sánh wildcard của .NET/filesystem, mặc định có thể đếm biến thể hoa (N13), rồi buộc FullName đúng hoa thường bằng `-ceq`. Tên ngắn 8.3 không thể chứa nguyên nonce 18 ký tự. Windows case-sensitive directory và UNC chưa được chạy ở đây. Chuỗi thao tác đúng B4 trên cả hai shell. B5/B6: đoạn dọn sau 08–10 và trước hash/thông báo; harness trích giữa marker và băm byte đoạn gốc. Setup, pin và lệnh/kiểm phản hồi 08–10 giữ nguyên. B7 có thao tác không đệ quy, với thiếu sót về kiểm loại ở finding trên. B8 đạt về danh mục bằng chứng và dư lượng; lời bảo đảm chỉ xoá của chính run còn phụ thuộc việc ràng buộc nonce.

## Giới hạn đã khai, không tự chặn merge

- **P3 — Mô-đun nội bộ và cache ổn định.** SKILL:464–472. Mô-đun có thật trong gói ghim và chính CLI dùng nó. Nâng pin cần đo lại lời gọi và dữ liệu trả về. Liên kết cha tĩnh trong cache tin cậy có thể chấp nhận khi đã xác nhận cùng đích vật lý ở các entry point. Sau khi kiểm trước thao tác, cửa sổ tráo thư mục đồng thời bởi tiến trình cùng người dùng có thể tiếp tục được khai là giới hạn. Ca executor nếu muốn đo giới hạn: so đối chứng liên kết cha ổn định với liên kết đổi đích giữa hai bước. Không có fixture ngoài cây do reviewer dựng.

## Độ phủ ma trận

- Chưa có mutant đích riêng trên cả hai nền cho P1/P2, N1/N2/N4/N6/N9/N11/N12/N19, nhánh N8-path, D3/D4, C1–C3/C6/C8/C10/C12/C13. N3 có mutant đếm và lọc tên; N2/N4 chia sẻ các chốt đó. Bash N16 đo nhiều mục nhưng không khoá yêu cầu NUL. PS còn N13 và L2 chưa có mutant đích riêng, N5 SKIP và thiếu mutant chốt reparse riêng cho tệp. N7 Bash thay hai thứ cùng lúc, C9 bỏ chung chốt daemon/hash, C10/N19 không cô lập được từng chốt.
- D2 thay đầu ra module giả; đo so chuỗi, chưa đo thay môi trường thật. C4/N17 đo từ chối đầu ra tương đối, chưa đo CWD của CLI; fixture C1–C13 dùng module giả bỏ qua CWD. N15 PS kiểm hash mục bị che; C7 PS chỉ kiểm STOP/marker, không snapshot mục bị che. Fixture không đo Gỡ, không chứng minh toàn luồng 01/08–10 hoặc lỗi/đột biến sau phần trích, và không thay thế các ca cache rỗng, cache env rỗng/thiếu, Unicode, UNC. L1/L3 có mutant retry, L2 đo timeout đọc và thứ tự biên nhận, chưa đo timeout xoá.

## N1 độc lập

```text
SOURCE d7954c30772a954da44a5fa50c08713ebc8cd3a001faeb9618c17e1094a0a0be pre_frag 78ffaccac4168eb0db9a251ce01a36e875c1efd73801298e8ded24dfb1c1161e dau_frag c7c7579a285723d56f4edef2f738d480d733e67fde897fa08f51f6ab5566da26 cleanup_frag 52328848e4da336eef8c35aa539a728ed6118cc41b943c0ef46e0e79b666fdbd node v22.23.5
TONG: 55 dat / 55
```

## KHÔNG đo được

- **N5-err-symlink trên Windows: KHÔNG ĐO ĐƯỢC.** Theo executor, PS 5.1 và pwsh 7 mỗi bản 65/65, rc 0, mỗi lượt một SKIP. N4 báo snapshot trùng byte với 15 `.err` cũ giữ nguyên (gồm 13 tệp được chỉ định), xoá thư mục hash rỗng sau khi đối chiếu probe. N3 báo snapshot trùng byte sau Gỡ. Đây là lời khai executor. N3 có SKILL trùng byte H; N2/N4 có SKILL và hai harness trùng byte H. Không tự chạy Windows, N3/N4, cache mới tinh, Windows UNC/Unicode hoặc thời gian nhả handle thực. Bash cục bộ 5.2.21, chưa đo 4.4 hoặc shell cũ. CI/doctrine-scan exact H chưa được xác minh.

## Lệnh đã chạy và mã thoát

- `ls -la`, `ls -la scratch`, `cat HEAD_SHA.txt`, `git -C repo rev-parse HEAD`, `git -C repo status --porcelain=v1 --untracked-files=all` trước và sau review, `sha256sum repo/ops/specs/wp1389-r1.md`, `cat` spec/lease/VERDICT — rc 0.
- `mkdir scratch/n1 && bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1 "$(command -v node)"` — rc 0, đúng một lượt.
- `git -C repo diff eca1d125b8..HEAD -- .agents/skills/playwright-browser/SKILL.md` lưu trong scratch, `git log -7 --oneline`, `git diff --name-status 07efca6 HEAD`, `git diff --name-only eca1d125b8..HEAD`, `git diff --check` giới hạn SKILL/hai harness/RESULTS, và hai `git diff --exit-code` so SKILL tại `4d8e9a7`, SKILL/hai harness tại `07efca6` với H — rc 0.
- `ls pwsrc`, các nhóm đọc `rg`, `find`, `nl -ba`, `sed`, `head`, `tail`, `cat` trên lockfile, SKILL, harness, RESULTS và nguồn/tài liệu ghim — rc 0. `python -` kiểm SRI và byte giải nén — rc 0.
- `mkdir scratch/work-probe` và hai probe `node -e` đọc registry ghim với XDG có slash cuối và XDG rỗng — nhóm rc 0, không gọi CLI. `bash --version | head -1` — rc 0. `command -v pwsh` — rc 1.
- `bash -c` nạp duy nhất fragment đầu Cleanup từ `scratch/n1/frag_dau.sh` với bản ghi fixture D4 và nonce mồi của cùng bản cài — rc 0, chốt chấp nhận nonce sai; không gọi 08–10.

## Lượt 4 (Codex CLI, 2026-11-18T12:08:26Z → 12:11:58Z, rc 0; chép nguyên văn `scratch/VERDICT.md`)

# WP1389 r1 — review độc lập lượt 4

reviewed_sha: 999f5fcb1a8d4bad3d280d87aa3bfcf3ba9897da
verdict: request_changes
reviewer: codex (OpenAI), codex_cli, read-only

## Findings chặn merge

- **P1 — Bản ghi neo đường dẫn dạng chuỗi, chưa neo đích qua thư mục cha.** `.agents/skills/playwright-browser/SKILL.md:196–203,247–259,332–340,393–402,464–468,483–485`. Nếu một liên kết cha được đổi đích hoàn toàn giữa hai bước, lần hỏi CLI trả cùng hai chuỗi. Hai thư mục cuối ở đích mới đều có thể là thư mục thường. Chốt đầu chấp nhận, rồi 08/09 đi vào cây mới trước phép đếm; nếu cây đích có phiên cùng nonce, Cleanup có thể đóng phiên đó và xoá stderr của nó. Gỡ cũng chỉ đối chiếu chuỗi và loại ở thư mục cuối. Chấp nhận liên kết cha tĩnh và chấp nhận cửa sổ tráo đồng thời đã khai, nhưng cần phân biệt chúng với thay đổi đích đã xảy ra trước lần gọi Cleanup/Gỡ. Lưu và so đích vật lý trước các thao tác, hoặc từ chối thành phần cha là liên kết. Ca executor dựng bằng lời: liên kết cha ổn định qua hai bước là đối chứng; đổi đích giữa hai bước phải STOP trước 08 và Gỡ giữ nguyên thư mục ở đích mới. Reviewer không dựng đường dẫn thoát cây.

- **P2 — PowerShell chấp nhận bản ghi của run khác qua reparse point.** `.agents/skills/playwright-browser/SKILL.md:336–337,396–401`. Bash loại symlink của `00-sophien.txt`; PS chỉ yêu cầu leaf, rồi đọc qua đường dẫn. Nếu bản ghi của A được thay bằng liên kết tới bản ghi của B đang mở trên cùng bản cài, và biến session bị ghép với B, phép so ba dòng thành công. Cleanup có thể đóng B và ghi chứng cứ vào A. Kiểm thuộc tính bản ghi trước khi đọc, từ chối reparse point và ghi bản ghi với chế độ tạo mới. Ca executor: chạy E2 với bản ghi A chuyển hướng sang bản ghi B, yêu cầu STOP trước 08 và so snapshot B. Reviewer chỉ mô tả tình huống liên kết.

- **P2 — Gỡ dùng bản ghi Capture thay cho chứng cứ Cleanup theo B7.** `.agents/skills/playwright-browser/SKILL.md:461–468`, `ops/specs/wp1389-r1.md:54–55`. Bản ghi Capture có thể tồn tại dù launcher lỗi và chưa có `11-daemon-path.txt`. Hướng dẫn hiện tại vẫn cho dùng nó để chọn một thư mục hash rỗng để xoá. B7 yêu cầu lấy thư mục cha từ biên nhận 11. Dùng biên nhận đó và đối chiếu thêm với probe/bản ghi 00, hoặc ghi phê duyệt thay đổi B7. Ca Gỡ chỉ có 00, có 11 sai cha, và 11 hợp lệ nhưng thư mục còn mục; cả ba giữ thư mục và ghi biên nhận.

- **P2 — Ma trận toàn luồng chưa chứng minh hết các chốt nó báo đạt.** `ops/acceptance/wp1389/residue_matrix.sh:166–173,189–215`, `ops/acceptance/wp1389/residue_matrix.ps1:233–240,270–286`. CLI giả có byte JSON/LF đúng cho close, verify và nhánh `deleted:false`. Tuy nhiên nó xoá descriptor còn tồn tại rồi vẫn báo false. CLI thật trả `deleted:result.existed` (output.js:259–260, session.js:73–97). Biến thể chỉ chấp nhận false vẫn qua E1. PS E1 cũng không đọc bảng hash; Bash chỉ kiểm bảng có tên 00 và 11-daemon.err, thiếu kiểm 11-daemon-path và thứ tự dọn trước hash. E2/E3 chỉ cấm `close` và kiểm một số tệp còn tồn tại, nên không đo độc lập việc cấm 09/10 hoặc bảo toàn byte. Để fixture phân biệt close dọn descriptor và descriptor còn sót, chạy cả true/false, thêm phản chứng byte/rc/stderr sai và lỗi ghi/copy/so/xoá. So bảng hash với ba tệp thật, kiểm nhật ký theo nonce và snapshot phiên bên kia. Các mutant bỏ nhánh true, chuyển hash lên sớm và gọi delete-data trước chốt phải làm ca đích đỏ.

- **P2 — N2–N4 vẫn chưa có chứng cứ trên exact H.** `ops/acceptance/wp1389/RESULTS.md:6–9,87–125`, `ops/specs/wp1389-r1.md:71–90`. Executor đo ở `429fb5b0d43b5298734142c8eafafb9a0804c40e`. Tôi xác nhận ba tệp thực thi trùng byte H, và diff chỉ có RESULTS, REVIEW-PROMPT và lease. Điều đó xác nhận nội dung phép đo, còn đặc tả yêu cầu commit H. Gắn bằng chứng N2–N4 và các gate với exact H, hoặc chủ kho ghi quyết định chấp nhận phép đo trên nội dung thực thi trùng byte. Ca kiểm nghiệm thu đối chiếu SHA của các receipt với SHA ứng viên khi chuẩn bị merge.

## Đối chiếu từng lỗi chặn lượt 3

| Finding lượt 3 | Trạng thái tại H |
|---|---|
| P1 ghép run A/nonce B | **Sửa một phần.** SKILL:203,259 ghi nonce; :336–338 và :396–398 so trước 08. E2 và mutant xác nhận thứ tự trên Bash. PS vẫn nhận bản ghi chuyển hướng. Cả hai ghi 00 trước phần ghi nhật ký và khởi chạy trong wrapper (:180–186,206,214–235,262). Lỗi ở ghi nhật ký, redirect hoặc start có thể để lại 00 dù chưa gọi native. E4 chỉ đo dừng ở preflight. Cần ca launcher không chạy và ca native đã thử nhưng lỗi, để phân biệt bằng dấu mốc launch. |
| P1 loại daemon/hash chỉ kiểm sau CLI | **Sửa một phần.** SKILL:339–340 và :399–402 chặn link/reparse ở đúng daemon/hash trước 08; :368–369 và :432–433 kiểm lại trước dọn. :464–468 thêm kiểm loại trước Gỡ. Trường hợp cha đổi đích vẫn qua phép so chuỗi như finding P1 trên. |
| P2 stdout PowerShell làm sai Unicode | **Đã sửa cơ chế.** SKILL:244–248 và :391–395 truyền base64 ASCII rồi giải mã UTF-8; Bash :196–200 và :332–335 giải mã bằng `base64 -d`. Chuỗi JS truyền bằng một argv, không có dấu nháy kép nội bộ; đường dẫn mô-đun là argv riêng và không kết thúc bằng dấu phân cách. Theo executor, U1 đạt trên 5.1/7; mutant đổi UTF-8 sang ASCII làm ca đỏ. U1-Cleanup dùng đoạn trích và không đo lại kênh probe đầu Cleanup trong toàn luồng Unicode. |
| P2 exact H và độ phủ toàn luồng | **Sửa một phần.** Harness Bash:155–215 và PS:225–286 chạy khối vận hành và có mutant đặt chốt đầu sau verify. Nhật ký mutant Bash thực sự có close, delete-data và tab-list của B. Còn thiếu các khẳng định độc lập, nhánh lỗi và chứng cứ exact H như hai finding P2 trên. |

## B1–B8 và đối chiếu nguồn

- HEAD khớp HEAD_SHA.txt, cây sạch. SHA-256 đặc tả khớp `12257fa8d659ff5c013af4bc31de700de4a53b085a99ec8c47cbd403d66610bc`. Base có blob SKILL `678ba2f0209690c535d9827ae8badbe7fff85748`. Ba tarball khớp SRI SHA-512 trong lockfile; 16 tệp CLI và 116 tệp core trong cây giải nén trùng tarball.
- registry.js:119–165 dùng hook test, Linux `XDG_CACHE_HOME || ~/.cache`, Windows `LOCALAPPDATA || ~/AppData/Local`, và macOS ngoài phạm vi skill. Hash là 16 hex đầu SHA-1 của `workspaceDir || packageRoot`; đường dẫn Linux trong spec cho `3815e4e10d63867a`. session.js:73–97,121–126 xác nhận mở .err với `w` và delete-data chỉ chọn descriptor/userdata. serverRegistry.js khai hook test và thao tác unlink descriptor có bỏ lỗi. README, session-management và client ghim không có tuỳ chọn được hỗ trợ để dời sổ phiên. `--profile` chọn dữ liệu trình duyệt; phương án (a) vẫn không khả dụng.
- B1/B2: Bash probe và wrapper cùng Node, subshell `cd work` và môi trường export. PS dùng `Push-Location` cho native probe và `-WorkingDirectory` cho CLI với cùng môi trường tiến trình trong điều kiện FileSystem của Setup. Cả hai từ chối workspace mode. Node chuẩn hoá dấu slash cuối và tự dùng fallback khi biến cache rỗng. Cache thiếu hoặc rỗng cho qua preflight nếu không có mục trùng; Cleanup từ chối thiếu thư mục hoặc zero match. Guard Bash 4.4 hiện có trước open và 08; N1 chạy trên 5.2.21.
- B3/B4: đường dẫn xoá phải đúng `DH/<nonce>.err`, so literal và phân biệt hoa thường ở đích. Quét Bash phân biệt hoa thường, dùng NUL và kiểm rc scanner. PS bỏ thư mục con reparse, đối sánh wildcard theo .NET/filesystem có thể đếm thêm biến thể hoa rồi từ chối. Tên ngắn 8.3 không chứa được nonce 18 ký tự. UNC thông thường qua điều kiện hình dạng, chưa có phép đo provider trả cùng chuỗi FullName. Hai shell ghi đường dẫn → chép → so → xoá → kiểm mất. Trong cache ổn định và với bản ghi run thường, không thấy đường xoá basename thiếu nonce. Phạm vi phép đếm là độ sâu 2 và không đi xuyên các hash liên kết khác theo B3.
- B5/B6/B8: mã đặt dọn sau 08–10, trước hash và CLEANUP OK; lệnh và mẫu byte 08–10 giữ nguyên. Harness băm byte giữa marker. Evidence liệt kê cả hai output 11; Limits khai thư mục dùng chung, descriptor trình duyệt được cố gắng xoá, .err cũ giữ nguyên. Nên ghi fallback Windows còn thiếu trong Limits. B7 dùng thao tác xoá thư mục không đệ quy, với sai khác nguồn biên nhận đã nêu.

## Giới hạn đã khai, không tự chặn merge

- **P3 — Phụ thuộc mô-đun nội bộ và giả định cache ổn định.** SKILL:474–485. Bản ghim thực tế dùng cùng `createClientInfo()` tại program.js:61. Đổi pin cần kiểm lại API và hợp đồng stdout. Cửa sổ giữa lần kiểm cuối và thao tác qua đường dẫn vẫn phụ thuộc cache tin cậy. Ca phân biệt giới hạn này với finding P1: đích cha ổn định qua các entry point, và đối chứng do executor dựng đổi thư mục sau chốt cuối. N1 không đo bảo đảm trước thao tác đồng thời.

## Độ phủ ma trận và phần KHÔNG đo được

- Ca chưa có mutant đích riêng trên cả hai shell gồm P1/P2, N1/N2/N4/N6/N9/N11/N12/N19, nhánh N8-path, D3/D4/D6/D8, C1–C3/C6/C8/C10/C12/C13 và E1/E3/E4. PS còn N13 và L2; U1 có mutant ở đoạn dọn nhưng không cô lập hai probe. N3 có mutant đếm/lọc; C9/D5 gộp guard daemon/hash; E2 có mutant thứ tự; D7 có mutant nonce. Các chốt B4 về lỗi ghi/so và hash/thông báo cuối chưa có mutant riêng. L1/L3 PS đo retry; L2 đo biên nhận có trước copy và timeout đọc.
- D2 đổi đầu ra module giả, chưa đo đổi môi trường thật hoặc CWD của probe so với CLI vì fake registry không dùng CWD. C3 đo cache thiếu, chưa đo cache tồn tại nhưng rỗng thật sự. E4 đo workspace mode trước open, chưa đo launcher lỗi sau khi ghi 00. E2/E3 có dữ liệu phiên nhưng chỉ kiểm tồn tại một số mục. E1 có ghi hash trên PS theo mã, harness không kiểm nội dung đó. Gỡ không nằm trong E1–E4.
- **N5-err-symlink trên Windows: KHÔNG ĐO ĐƯỢC.** Executor báo SKIP trên cả PS 5.1 và pwsh 7, mỗi shell 80/80 các phép đo tính điểm, rc 0. N4 khai snapshot trước/sau trùng byte, 15 .err cũ giữ nguyên gồm 13 tệp chỉ định; N3 khai snapshot trùng và hash-dir của bản cài đã gỡ. Đây là lời khai executor tại `429fb5b`. Không tự chạy Windows hoặc native N3/N4. Chưa đo độc lập UNC, Windows Unicode dưới OEM console, Bash 4.4, cache mới tinh, cache env rỗng/thiếu trên Windows, thời gian nhả handle thật hoặc CI/doctrine-scan trên H.

## N1 độc lập

```text
SOURCE 2dcbb5d4fa8362df603999b299c481ba099a6b3e6e47763cb925d7f48c84e0e5 pre_frag 4b8bb645114af21f66422222cab295c1773fda0a25820c3790648f2f99dac488 dau_frag 6b163824fd0e886d4ae1fe921a7a2e65a2912d257c0fd0ab358b9e105d4f5640 cleanup_frag 52328848e4da336eef8c35aa539a728ed6118cc41b943c0ef46e0e79b666fdbd node v22.23.5
TONG: 66 dat / 66
```

## Lệnh và mã thoát

- `ls -la`, `ls -la scratch`, `cat HEAD_SHA.txt`, `git -C repo rev-parse HEAD`, `git -C repo status --porcelain` và `--porcelain=v1 --untracked-files=all`, `sha256sum repo/ops/specs/wp1389-r1.md`, `ls pwsrc`, tìm AGENTS bằng `rg --files` — rc 0.
- `mkdir scratch/n1 && bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1 "$(command -v node)"` — rc 0, đúng một lần, stdout/stderr lưu tại `scratch/n1.log`.
- `git -C repo diff eca1d125b8..HEAD -- .agents/skills/playwright-browser/SKILL.md`, `git -C repo log -8 --oneline`, `git -C repo diff --name-status 429fb5b..HEAD`, `git -C repo diff --exit-code 429fb5b..HEAD --` SKILL và hai harness, `git -C repo diff --check eca1d125b8..HEAD --` SKILL, hai harness và RESULTS, `git -C repo rev-parse eca1d125b8:.agents/skills/playwright-browser/SKILL.md` — rc 0.
- Các nhóm `cat`, `nl -ba`, `sed`, `rg`, `head`, `cut` đọc chỉ dẫn kho, lease, spec, verdict cũ, lockfile, SKILL, hai harness, RESULTS, nguồn ghim và nhật ký fixture — rc nhóm 0. `bash --version | head -1` và `printf %s /tmp/claude-0/tlpw-base/install/0.1.0/node_modules/playwright-core | sha1sum` — rc 0. `command -v pwsh` — rc 1.
- `python -` kiểm SRI lần đầu tìm nhầm tên tarball CLI — rc 1. Lần sửa tên tarball, kiểm cả ba SRI và byte hai cây nguồn giải nén — rc 0.

## Lượt 5 (Codex CLI, 2026-11-18T14:04:44Z → 14:10:25Z, rc 0; chép nguyên văn `scratch/VERDICT.md`)

# WP1389 r1 — review độc lập lượt 5

reviewed_sha: 376e9c2661e15f8ac28155783366c53caf0c09e7
verdict: request_changes
reviewer: codex (OpenAI), codex_cli, read-only

Tree: `282371516959796d6a4756c58f38163b90c12f5f`. HEAD khớp `HEAD_SHA.txt`, cây sạch. Lease g1 ghi quyền gọi lượt 5 và quyết định dùng phép đo trên nội dung thực thi trùng byte.

## Findings chặn merge

- **P1 — Chốt đường dẫn vật lý Bash mất byte cuối và có thể chấp nhận symlink tĩnh** (`daemon-path-binding`). `.agents/skills/playwright-browser/SKILL.md:202,344,373,489`. Bash bỏ **mọi** LF cuối stdout trong `$(…)`. Nếu thư mục hash là symlink tĩnh tới một thư mục cùng đường dẫn cơ sở và tên chỉ khác ở LF cuối, `realpath` trả đường dẫn vật lý khác nhưng phép so coi chúng bằng nhau. Capture bỏ qua nội dung đích vì `find` không đi theo symlink rồi có thể để `startDaemon` mở và truncate tệp nonce có sẵn. Nếu liên kết xuất hiện giữa Capture và Cleanup, chốt đầu có thể cho CLI chạy `close` và `delete-data` qua liên kết. Registry thật dùng `stat`, đọc descriptor qua đường dẫn và tra theo hash của tên thư mục logic (`registry.js:51–54,78–114`). Bước dọn sau 10 có thể dừng vì `find` không thấy mục, nhưng các lệnh CLI đã chạy. Gỡ qua symlink ở chính thư mục hash còn được `rmdir` chặn. Sửa cả bốn phép so bằng cách giữ nguyên byte kết quả và kiểm rc (ví dụ `realpath -z`, đọc NUL và thu rc), hoặc kiểm loại từng thành phần. Ca executor: liên kết tĩnh với đích khác đúng LF cuối, đối chứng thư mục thường, kiểm Capture không gọi open và không đổi byte đã có, Cleanup không gọi 08–10 và giữ snapshot. N16 đo tên mục trong bước quét, còn C10/D6/E3 đo liên kết với đích thông thường. Tôi kiểm độc lập quy tắc cắt LF bằng chuỗi thường và chỉ mô tả bố trí đường dẫn.
- **P2 — Gỡ vẫn có thể nhận biên nhận chuyển hướng** (`uninstall-receipt-binding`). `.agents/skills/playwright-browser/SKILL.md:486–494,505–517`. Bash `-f` theo symlink của 11 rồi `cat`/ `sed` đọc theo đường dẫn. PS đọc cả hai tệp bằng `ReadAllText` trước khi kiểm loại của chúng. Một run chưa từng hoàn thành Cleanup có thể có 00/11 là liên kết tới cặp bản ghi từ run khác cùng bản cài. Khi hash dir rỗng và probe khớp, Gỡ cho phép xoá dù thiếu biên nhận của run được chọn. Phạm vi xoá ở đây là thư mục rỗng. Yêu cầu cả hai tệp là tệp thường, từ chối symlink/reparse trước đọc, kiểm nguyên bản ghi và hook cấm trước probe. Ca Gỡ thay lần lượt 00 và 11 bằng liên kết tới bản ghi hợp lệ rồi kiểm thông báo GIỮ và thư mục còn; đối chứng G1. G2 hiện chỉ xoá 11, G5 chỉ liên kết ở đường dẫn cache.
- **P2 — C15 chưa chứng minh tạo mới với mục đặc biệt trên Bash** (`capture-record-creation`). `.agents/skills/playwright-browser/SKILL.md:204,261–263`, `ops/acceptance/wp1389/residue_matrix.sh:370`. Bash noclobber từ chối tệp thường có sẵn, nhưng cho mở FIFO đã tồn tại. Bản ghi tại FIFO có thể làm Capture treo trước open, hoặc nhận byte rồi cho open chạy trong khi không tạo được bản ghi thường để Cleanup đối chiếu. PS `CreateNew` từ chối mục có sẵn. Từ chối mọi mục đã có (kể cả symlink dangling) trước khi tạo và giữ chốt tạo độc quyền cho file thường, hoặc dùng primitive tạo mới độc quyền ngay từ đầu. Ca đặt FIFO trong run fixture, giới hạn thời gian, xác nhận STOP, không gọi open và FIFO nguyên vẹn. C15 hiện dùng tệp thường. Probe Bash tối giản với FIFO trong scratch bị timeout (rc 124), FIFO còn nguyên. Probe không chạy Capture.

## Đối chiếu từng finding chặn merge của lượt 4 (999f5fc)

| Finding | Trạng thái ở H và căn cứ |
|---|---|
| P1 liên kết cha đổi đích giữa hai bước | **Sửa một phần.** Bash kiểm đường dẫn vật lý ở :202,344,373,489. PowerShell dò tổ tiên ở :253–255,407–408,440–441,509–510. Các trường hợp tĩnh thông thường đã có chốt trước open/close/Gỡ. Ngoại lệ Bash mới ở trên. Thay đổi đồng thời sau phép kiểm thuộc giới hạn đã khai. |
| P2 PS nhận 00 qua reparse point | **Đã sửa trong Capture/Cleanup.** :261–263 tạo bằng CreateNew và :401–404 kiểm leaf/reparse trước đọc. D10 và mutant trên Windows chưa đo được. Bash giữ chốt `! -L` tại :340, nhưng chốt tạo mới có ngoại lệ FIFO nêu trên. |
| P2 Gỡ lấy 00 thay 11 | **Sửa một phần.** :486–489,505–511 bắt buộc nội dung 11 khớp đường dẫn chính xác dựng từ probe và nonce; :494,517 xoá không đệ quy. Thiếu 11 thật sự hoặc 11 sai cha đều bị chặn. Còn đường nhận biên nhận chuyển hướng. |
| P2 bằng chứng toàn luồng | **Sửa một phần.** Bash harness :217–221,235–269 và PS harness :284–288,320–345 đã đo hai kết quả deleted, băm bốn tệp, đối chiếu nhật ký và byte phiên khác. Mutant only-false, hash-early và chốt đầu đặt muộn có mục tiêu cụ thể. Chưa có lỗi riêng cho rc/stdout/stderr của từng lệnh 08–10 và PS chưa có phản chứng độc lập cho hash bản sao lệch. |
| P2 exact H | **Đã đóng theo quyết định trong lease.** Diff executable từ `d7960ee` tới H rc 0. SKILL từ `ff34b2c` (phép đo N3) tới H cũng trùng byte. N1 độc lập chạy trên H. N2/N4 là lời khai của executor tại `d7960ee`, N3 tại `ff34b2c`, theo ngoại lệ chủ kho ghi. CI bắt buộc trên H chưa xác minh, doctrine-scan tại H đạt. |

## Đối chiếu nguồn ghim và B1–B8

- Cả ba tarball khớp SRI SHA-512 trong lockfile, 16 tệp CLI và 116 tệp core giải nén trùng byte tarball. Spec SHA-256 khớp `12257fa8d659ff5c013af4bc31de700de4a53b085a99ec8c47cbd403d66610bc`. Blob base SKILL khớp `678ba2f0209690c535d9827ae8badbe7fff85748`.
- `registry.js:119–165` xác nhận hook test, fallback Linux/Windows, và nhánh macOS ngoài phạm vi. Hash lấy 16 hex đầu SHA-1 của `workspaceDir || packageRoot`; đường dẫn đo trong spec cho `3815e4e10d63867a`. `session.js:73–97,121–126` xác nhận tạo .err bằng `w` và delete-data chỉ nhắm descriptor/userdata. `serverRegistry.js:1818,1848` xác nhận cơ chế bỏ lỗi unlink và hook test. README, session-management và help ghim không có tuỳ chọn hỗ trợ dời sổ phiên. `--profile` thuộc dữ liệu trình duyệt. Phương án (a) vẫn không khả dụng.
- **B1/B2.** Probe dùng đúng mô-đun mà CLI dùng (`program.js:61`). Bash dùng cùng Node và CWD `work` trong subshell. PS dùng `Push-Location` cho native probe và `-WorkingDirectory` cho CLI, cùng môi trường tiến trình trong điều kiện FileSystem của Setup. Kênh base64 mang ASCII, JS là một đối số và không có dấu nháy kép bên trong. Node chuẩn hoá slash cuối và áp fallback khi biến cache rỗng, kể cả fallback Windows khi LOCALAPPDATA rỗng hoặc thiếu. Cache chưa tạo được cho qua preflight, Cleanup yêu cầu có thư mục. GNU `realpath -m` xử lý thành phần chưa tồn tại, chốt Bash còn có lỗi mất LF nêu trên. Vết 00 được ghi sau preflight và trước wrapper open, nên chứng minh preflight đã qua chứ chưa chứng minh tiến trình đã khởi động. E7 đo CLI giả đã được gọi nhưng chưa tạo thư mục hash, E8 đã tạo .err nhưng close chưa chứng minh được phiên đóng. Nếu launcher lỗi khi hash dir đã tồn tại, Cleanup vẫn có thể thử close cho nonce đã neo rồi dừng khi trả not-open.
- **B3/B4.** Phép dọn dùng đúng đường dẫn tuyệt đối, so literal phân biệt hoa thường, và kiểm loại tệp. Bash `mapfile -d ''` với `wait "$!"` kiểm phép quét NUL trên Bash 5.2.21, chốt phiên bản yêu cầu 4.4. PS bỏ hash reparse trước liệt kê, dùng .NET để lỗi liệt kê dừng. Wildcard Windows có thể đếm thêm biến thể hoa thường trên volume mặc định, còn `-ceq` buộc đúng đích trước khi xoá. Tên ngắn 8.3 không chứa đủ nonce 18 ký tự. UNC được chấp nhận theo regex Capture, chưa đo vòng Split-Path/Get-Item tại gốc share hoặc cách FullName được trả trên UNC. Thứ tự đúng spec là ghi 11-path → chép → so → xoá → kiểm mất. Với đường dẫn thường ổn định và bản ghi nguyên vẹn, không thấy đường từ bước dọn xoá basename thiếu nonce hay in OK khi mục phù hợp vẫn còn.
- **B5/B6/B8.** Dọn ở giữa marker sau 08–10, trước hash và CLEANUP OK. Ba hợp đồng CLI cũ giữ nguyên. Fixture khớp byte JSON/LF và rc ở các nhánh được dùng. CLI thật lấy `wasOpen` từ socket và `deleted` từ mục khớp của entry, kể cả userdata khi còn entry (`program.js:115–123,162–166`, `session.js:67–97`, `output.js:236–238,259–260,276–277`). Fixture chỉ mô phỏng descriptor và trạng thái mở, đủ kiểm nhánh E1/E6 và E8 đã dựng. Evidence có hai tệp 11. Limits khai các thư mục dùng chung, .err cũ và việc CLI có thể bỏ qua lỗi xoá descriptor trình duyệt. Nên ghi rõ fallback Windows trong Limits để mô tả đủ quy tắc mà mã thực hiện.
- **B7.** Cả hai Gỡ xác minh probe trước khi xoá bản cài, rồi dùng thao tác chỉ xoá thư mục rỗng. Chuỗi `GO_DH=$(…) || …` Bash đặt lại biến khi kiểm thất bại, và chuỗi `-and` trong ngoặc PS short-circuit. Biên nhận chuyển hướng vẫn lọt. Giữa hai pha Gỡ, đường dẫn kiểm lần cuối ở pha (1) nên pha (2) phụ thuộc cây ổn định.

## Độ phủ và phần KHÔNG đo được

- Những ca thiếu mutant đích riêng trên cả hai shell gồm P1/P2 dương, N1/N2/N4/N6/N9/N11/N12/N19/N20R/N21, nhánh N8-path, D3/D4/D6/D8, C1–C3/C6/C8/C10/C12/C13, G1/G4/G7, E3–E5/E7/E8. Bash còn N16. PS còn N13, N22, W1 và L2. Bash N24 có mutant ghi biên nhận, PS W1 có phản chứng cấm ghi. Có mutant cho kết quả cuối của retry xoá, thiếu mutant cho hậu kiểm khi lệnh xoá trả thành công mà mục vẫn còn. E1 là đích của hash-early, E2 của chốt đặt muộn, E6 của only-false. Chưa có phản chứng tách lỗi bảng hash cuối với việc phát CLEANUP OK.
- D2 đo probe giả trả khác, chưa đo đổi CWD/môi trường dựa vào registry thật. C3 đo cache thiếu, E1/E6 bắt đầu với hash khác có dữ liệu, chưa đo cache thật tồn tại nhưng rỗng. U1 dùng biến đầu ra của module giả và đoạn trích, không đo mọi probe trên console OEM. E7/E8 đo theo log fake CLI, chưa đo wrapper không thể khởi động tiến trình hoặc loại lỗi khác của từng phản hồi 08–10. Các ca STOP chung có thể xanh do dừng sai chốt, dù các ca có mutant đích giảm được nguy cơ này.
- **Windows N5-err-symlink, D10 và mutant record-reparse: KHÔNG ĐO ĐƯỢC.** Executor báo SKIP ba phép đo, PS 5.1 và 7 mỗi shell 110/110 phép tính điểm, rc 0. Executor báo N3/N4 snapshot giữ nguyên và hash dir đã gỡ, N4 giữ cả 15 .err cũ gồm 13 tệp chỉ định. Tôi không chạy Windows hay CLI thật. UNC, thời gian daemon thật nhả handle, Bash 4.4, cache hoàn toàn mới và CI bắt buộc tại H chưa được xác minh.

## Giới hạn đã khai, không tự chặn merge

- **P3 — Phụ thuộc nội bộ bản ghim và cây cache ổn định.** SKILL:529–538. Đổi pin có thể đổi API và byte phản hồi; tiến trình cùng người dùng thay đối tượng sau lần kiểm cuối vẫn có thể đổi đích. Giữ giới hạn cho thiết kế này, kiểm lại hợp đồng khi đổi ghim và đo tách trường hợp đổi đồng thời khỏi các liên kết đã tồn tại trước khi chạy. Finding P1 ở trên xảy ra với cây tĩnh.

## N1 độc lập

```text
SOURCE 75e9be5ff358476de7405008955bf898f9186a02d34e1616c50e079f6826c94c pre_frag 972cff1823a754c92a63887429e71a90ae5233a6867c8eefbdb9fd4de31f1ffc dau_frag 385efe408f5d9c3eae8f7ffef8194b0c620d171229d749a5b2940694b618f938 cleanup_frag 29d8183b49ff76fca502885c7578299c531a26cfe87954f0cff16f0ce057bae8 go_frag 418a97a2aa1b0fc28fc30b372a7e7cd27166f4bbff2a9c5791b65699b5e51416 node v22.23.5
TONG: 99 dat / 99
```

## Lệnh và mã thoát

- `ls -la`, `ls -la scratch`, `cat HEAD_SHA.txt`, `git -C repo rev-parse HEAD HEAD^{tree}`, `git -C repo status --porcelain=v1 --untracked-files=all` và kiểm lại với `--no-optional-locks`/ `--ignored`, `sha256sum repo/ops/specs/wp1389-r1.md` — rc 0.
- `mkdir scratch/n1 && bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1 "$(command -v node)"` — rc 0, đúng một lần. Nhật ký ở `scratch/n1.log`.
- `git -C repo diff eca1d125b8..HEAD -- .agents/skills/playwright-browser/SKILL.md`, `git -C repo diff --stat eca1d125b8..HEAD`, `git -C repo rev-parse eca1d125b8:.agents/skills/playwright-browser/SKILL.md`, `git -C repo diff --exit-code d7960ee HEAD -- .agents ops/acceptance/wp1389/residue_matrix.sh ops/acceptance/wp1389/residue_matrix.ps1`, và phép diff riêng SKILL từ `ff34b2c` — rc 0.
- `git -C repo diff --check eca1d125b8..HEAD` — rc 2 vì bốn dòng kết thúc bằng hai dấu cách trong VERDICT lịch sử. Giới hạn cùng phép kiểm vào SKILL, hai harness và RESULTS — rc 0.
- `python -` kiểm SRI và byte cây nguồn — lần đầu rc 1 do tên file tarball npm scoped, chạy lại với tên đúng rc 0. `printf %s /tmp/claude-0/tlpw-base/install/0.1.0/node_modules/playwright-core | sha1sum`, `bash --version | head -1` và phép `v=$(printf 'hash\n\n'); printf '%s' "$v" | od -An -tx1` — rc 0. `command -v pwsh` — rc 1.
- `mkdir scratch/noclobber-check && mkfifo scratch/noclobber-check/record` — rc 0. `timeout 1s bash -c'…'` với `set -C` và redirect vào FIFO — rc 124; kiểm FIFO còn nguyên — rc 0.
- `python -B repo/.claude/dev/packet_loop.py doctrine-scan --root repo` — rc 0, quét 12 tệp, 0 chỗ chép doctrine.
- Các nhóm đọc `cat`, `nl -ba`, `sed`, `rg`, `ls`, `head`, `tail`, `cut` trên chỉ dẫn kho, spec, lease, verdict trước, SKILL, harness, RESULTS, nguồn ghim và log fixture — rc nhóm 0, ngoài các probe đã ghi riêng.

## Lượt 6 (Codex CLI, 2026-11-18T14:28:07Z → 14:33:04Z, rc 0; chép nguyên văn `scratch/VERDICT.md`)

# WP1389 r1 — review độc lập lượt 6

reviewed_sha: d0d4879c743c124b43c43e0713427d5be99cf1d9  
verdict: request_changes  
reviewer: codex (OpenAI), codex_cli, read-only

Tree `db8b7fd1deb021d10f17eac3af415197bd547fe5`. HEAD khớp `HEAD_SHA.txt`, cây sạch trước và sau review. Base là tổ tiên của HEAD, blob SKILL tại base khớp spec, diff nằm trong write set. SHA-256 spec khớp `12257fa8d659ff5c013af4bc31de700de4a53b085a99ec8c47cbd403d66610bc`. Lease g1 ghi `budget_nang_tran_3` và dành lượt gọi thứ sáu.

## Findings chặn merge

- **P1 — PowerShell có thể xoá tệp sai tên và báo CLEANUP OK.** `.agents/skills/playwright-browser/SKILL.md:445–463`. Phép so `-ceq` phân biệt hoa thường theo InvariantCulture. .NET có thể bỏ qua U+00AD khi so theo văn hoá. Nếu sau verify mục duy nhất là tệp thường có nonce đúng nhưng tên chứa thêm U+00AD giữa nonce và hậu tố, bộ lọc vẫn thấy nonce liền mạch. Phép so đường dẫn có thể chấp nhận mục này, rồi copy và xoá chính `$f.FullName`. Hậu kiểm xác nhận tệp sai đã mất và luồng có thể báo OK. Lỗi đã có trước bản vá lượt 6, phát hiện ở lượt này bằng đọc mã và hợp đồng .NET. Dùng `[string]::Equals(..., [StringComparison]::Ordinal)` cho ràng buộc đường dẫn và thao tác trên đường dẫn đích đã xác minh. Ca hồi quy trên PS 5.1 và 7 dùng mục sai tên duy nhất trong đúng thư mục hash, yêu cầu STOP, giữ nguyên byte và chưa ghi output 11. Đột biến trở lại `-ceq` phải làm ca lọt. [PowerShell 5.1](https://learn.microsoft.com/en-us/PowerShell/module/microsoft.PowerShell.core/about/about_comparison_operators?view=powershell-5.1) · [PowerShell 7](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_comparison_operators?view=powershell-7.3) · [.NET CompareInfo](https://learn.microsoft.com/en-us/dotnet/fundamentals/runtime-libraries/system-globalization-compareinfo)
- **P2 — Gỡ mới vẫn nhận biên nhận khác nội dung đã ghi.** `.agents/skills/playwright-browser/SKILL.md:342,405,489–492,512–518`. Bash giữ được LF cuối trong Gỡ nhưng command substitution bỏ byte NUL. Một tệp 00 hoặc 11 thường có byte NUL thừa vẫn có thể mở chốt xoá thư mục hash rỗng. Probe độc lập trên chuỗi vô hại cho phép so shell rc 0 và `cmp` rc 1. PowerShell `ReadAllText` nhận và bỏ BOM, còn `-ceq` có thể bỏ qua ký tự Unicode khi so theo văn hoá. Chốt đầu Cleanup cũng có cùng loại sai lệch khi đối chiếu 00. Sửa bằng so byte trực tiếp với nội dung UTF-8/LF mà Capture và Cleanup tạo, dùng `cmp` trên Bash và `ReadAllBytes` trên PowerShell. Ca hồi quy lần lượt sửa byte của 00 và 11 trong fixture Gỡ, giữ nguyên đường dẫn hợp lệ, yêu cầu GIỮ và thư mục còn nguyên. Thêm đối chứng đầu Cleanup với 00 sai byte, kiểm nhật ký chưa ghi 08. [PowerShell về phép so chuỗi](https://learn.microsoft.com/en-us/PowerShell/module/microsoft.PowerShell.core/about/about_comparison_operators?view=powershell-5.1) · [.NET về ký tự bị bỏ qua](https://learn.microsoft.com/en-us/dotnet/fundamentals/runtime-libraries/system-globalization-compareinfo)

## Đối chiếu từng finding lượt 5

| Finding | Trạng thái ở HEAD |
|---|---|
| P1 Bash bỏ LF cuối khi so đường dẫn vật lý | **Đã sửa cho trường hợp đã báo.** SKILL:202,345,374,492 đặt dấu kết thúc sau stdout của `realpath`. LF của tên đích nằm trước LF phân cách và vẫn được so. C18 và D11 có đột biến hoàn tác phép so. N25 và G8 có ca dừng, nhưng chưa cô lập được phép so ở hai pha đó. |
| P2 Gỡ đọc 00/11 qua liên kết | **Sửa một phần.** SKILL:484–488 và :504–510 kiểm loại cả hai tệp và cấm hook trước khi đọc/probe. Bash kiểm LF cuối tại :490–491, PS kiểm đủ dòng tại :512–515. Liên kết tại chính tệp biên nhận bị chặn. Phép so toàn nội dung vẫn nhận nội dung khác như finding P2. |
| P2 Capture Bash có thể mở FIFO | **Đã sửa với mục có sẵn.** SKILL:204 kiểm cả `-e` và `-L` trước redirect noclobber tại :205. PS giữ `CreateNew` tại :262. C16 dừng rc 1 với FIFO nguyên, mutant pre-fifo timeout rc 124. C17 kiểm symlink treo. Việc thay mục đồng thời sau chốt thuộc giới hạn đã khai. |

## Đối chiếu nguồn ghim và B1–B8

- Ba tarball khớp SRI SHA-512 trong lockfile. Đối chiếu byte của toàn bộ 16 tệp CLI và 116 tệp core đã giải nén với tarball. `registry.js:119–165` xác nhận hook test, fallback cache Linux/Windows và thêm nhánh macOS ngoài phạm vi. Hash là 16 hex đầu của SHA-1 trên `workspaceDir || packageRoot`. `session.js:73–97,121–126` xác nhận mở `.err` bằng `w` và delete-data chỉ chọn `.session` và `ud-<nonce>-*`. `coreBundle.js` xác nhận cache trình duyệt riêng `ms-playwright/b` và hook test riêng. README, help và session-management của bản ghim không có tuỳ chọn hỗ trợ dời sổ phiên. `--profile` đổi profile trình duyệt. Phương án (b) vẫn có căn cứ.
- **B1/B2.** Probe và CLI dùng cùng Node, cùng `work` và môi trường kế thừa tại các entry point Setup thông thường. Bash dùng `cd`, PS dùng `Push-Location` cho native probe và `-WorkingDirectory` cho CLI. JS được truyền thành một đối số với nội dung ASCII, không có dấu nháy kép bên trong. Base64 bảo toàn Unicode qua kênh console. `XDG_CACHE_HOME` rỗng dùng fallback Linux, slash cuối do Node chuẩn hoá. Windows dùng `LOCALAPPDATA` hoặc home của Node, bỏ qua XDG. Cache thiếu cho qua preflight, cache rỗng cho kết quả quét 0, Cleanup yêu cầu thư mục đã có. `00` được tạo sau preflight và trước wrapper open. Dừng trước khi ghi 00 thì đầu Cleanup từ chối. Dừng sau khi ghi 00 chưa chứng minh CLI đã khởi động, nên vẫn phải qua hợp đồng close. E7/E8 đo hai dạng lỗi này ở mức fixture. Bảng ghim, Setup, Kiểm pin và các lệnh 08–10 giữ nguyên.
- **B3/B4.** Bash quét NUL bằng `mapfile -d ''`, chờ rc bằng `wait "$!"`, và so nguyên đường dẫn. Guard yêu cầu Bash ≥ 4.4, phép chạy độc lập là 5.2. PS bỏ qua thư mục con reparse trong phép quét và các guard kiểm tổ tiên của đường dẫn cần thao tác. Wildcard có thể thu thêm bản viết hoa trên Windows. Tên ngắn 8.3 không chứa nonce 18 ký tự. Chốt đích PowerShell có lỗi so Unicode nêu trên. Cả hai ghi 11-path → chép → so → xoá → kiểm mất. Không dựng đường dẫn thoát cây trong review.
- **B5/B6.** Bước dọn nằm sau 08–10, trước bảng hash và CLEANUP OK. Harness trích phần giữa marker, PS tính hash trên nội dung UTF-8/LF rồi thêm BOM riêng khi dựng script thực thi. CLI thật lấy `wasOpen` từ phiên và `deleted` từ mục dữ liệu thực sự tồn tại. Fake CLI mô phỏng trạng thái mở và descriptor, khớp byte JSON/LF và rc của các nhánh E1/E6/E8 mà harness chạy. Fake không mô phỏng toàn bộ xử lý userdata và I/O launcher của CLI thật. Các ca N3/N4 trong ma trận dựng riêng dư lượng descriptor/userdata để kiểm chốt quét.
- **B7/B8.** Gỡ xác minh trước khi xoá install, sau đó dùng `rmdir` hoặc `Directory.Delete(..., false)`. Biên nhận không còn đơn thuần là dòng 2 của 00. Phép so biên nhận còn lỗi nêu trên. Evidence liệt kê hai output 11. Limits khai mô-đun nội bộ, thư mục còn lại, `.err` cũ và lỗi xoá descriptor trình duyệt có thể bị CLI bỏ qua. Nên ghi thêm fallback của `LOCALAPPDATA` rỗng/thiếu để khớp hành vi. B5 chỉ có bằng chứng qua các fixture và native được báo, với ngoại lệ hành vi PowerShell ở P1.

## Giới hạn đã khai, không tự chặn merge

- **P3 — Cache phải ổn định và mô-đun nội bộ phải đúng pin.** SKILL:533–545. Đổi pin có thể đổi giao diện registry hoặc hợp đồng stdout. Thao tác qua đường dẫn sau lần kiểm cuối phụ thuộc cache và cây run ổn định. `echo .` giữ LF nhưng che rc lệnh trước. Với GNU `realpath` một toán hạng, lỗi không có dòng kết quả phù hợp thì phép so vẫn dừng. Có thể phát sentinel chỉ sau khi lệnh thành công để biểu đạt rõ điều kiện. Ca kiểm giới hạn dùng probe đơn lẻ báo lỗi và đối chứng riêng do executor dựng cho thay đổi đồng thời sau lần kiểm cuối. Không chạy các ca đó trong review.

## Độ phủ ma trận

- Bash, ca không có mutant đích riêng theo log: P1/P2, C1/C2/C3/C6/C8/C10/C12/C13/C17, D3/D4/D6/D8, E3/E4/E5/E7/E8, G1/G4/G7/G8, N1/N2/N4/N6/N9/N11/N12/N16/N19/N20R/N21/N25. Nhánh N8-path chưa có mutant đích tách riêng. Các ca mới C16/C18/D11 và G9–G12 có mutant đích.
- PS, theo mã harness: P1/P2, C1/C2/C3/C6/C8/C10/C12/C13, D3/D4/D6/D8, E3/E4/E5/E7/E8, G1/G4/G7/G9, L2, N1/N2/N4/N5/N6/N9/N11/N12/N13/N19/N20R, W1 thiếu mutant đích riêng. G10 có mutant nhưng executor báo SKIP. Chưa có phản chứng PS tách riêng lỗi so nội dung bản sao và chưa có ca đích cho so đường dẫn ordinal.
- **Có ca nhưng chưa đo được chốt riêng.** G8 chỉ kiểm GIỮ và snapshot. `rmdir` tự từ chối symlink ở chính thư mục hash, nên G8 vẫn có thể xanh khi chốt pha (1) đã lọt. Kiểm thêm giá trị GO_DH rỗng hoặc phân biệt biên nhận từ hai pha và hoàn tác phép so riêng. N25 chạy cả đầu Cleanup, nên đầu Cleanup có thể dừng trước khi tới chốt sau verify. Dùng đoạn residue-only, kiểm lý do hoặc dùng mutant sao cho kết quả phân biệt được chốt đó. D2 thay đầu ra registry giả, chưa đo drift CWD/môi trường thật. N2 Windows bao gồm fixture Windows, không phải ca kiểm chuẩn Unicode theo P1. Các ca Gỡ PS kiểm kết quả giữ thư mục, chưa bắt buộc kiểm biên nhận cảnh báo.

## N1 độc lập

```text
SOURCE a435d08248f38e609ad953149ff2f832305a1b71610fae39ca1a34b8190ccadf pre_frag 5dd274675365ee20d5e72bccb4e5b22b7329cbad9e61587c9571c27720c11eee dau_frag 7c01d3164e433c5348ba93b6882a5341bf030a04f1131e6a8319bfb70314aa85 cleanup_frag b717d4c157c23f5fa12896b075f76553843d2693225979c9d60867ddc0135431 go_frag 63d36e12a4fc71bd9aec0bc03c9e537ca013109793ee7877904a557edde2ad2a node v22.23.5
TONG: 116 dat / 116
```

## Không đo được và bằng chứng executor

- **N5-err-symlink trên Windows: KHÔNG ĐO ĐƯỢC.** RESULTS §9 cũng báo SKIP D10, G9, G10 và mutant record-reparse/go-record-reparse. N2 là lời khai executor trên `1d7b9f4`, 114/114 phép tính điểm ở mỗi shell, 6 SKIP mỗi shell. Tôi không chạy Windows, nên nhánh P1 là suy luận từ mã và hợp đồng runtime.
- Executor báo N3/N4 native trên `1d7b9f4` có snapshot trước/sau trùng byte, hash dir bị gỡ và 15 `.err` cũ trên Windows giữ nguyên, gồm 13 tệp chỉ định. Tôi xác nhận SKILL và cả hai harness trùng byte giữa commit đo và HEAD. Lease ghi quyết định dùng bằng chứng trên mã trùng byte, với tiền lệ ghi cụ thể ở `d7960ee`. Native N3/N4 không được chạy độc lập trên HEAD.
- Chưa đo UNC và cách PowerShell duyệt gốc share, Bash 4.4, host cache mới tinh hoặc thời gian nhả handle thật. Chưa xác minh CI bắt buộc của PR tại HEAD. Doctrine-scan local đạt.

## Lệnh và mã thoát

- `cat HEAD_SHA.txt`, `git -C repo rev-parse HEAD`, kiểm tree và blob base bằng `rev-parse`, kiểm base bằng `merge-base --is-ancestor`, `git --no-optional-locks -C repo status --porcelain=v1 --untracked-files=all`, `sha256sum repo/ops/specs/wp1389-r1.md`, `ls` kiểm scratch/nguồn — rc 0.
- `mkdir scratch/n1 && bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1 "$(command -v node)"` — rc 0, đúng một lần. Nhật ký `scratch/n1.log`.
- `git -C repo diff eca1d125b8..HEAD -- .agents/skills/playwright-browser/SKILL.md`, diff lượt 5 tới HEAD, `diff --name-only`, `log -8 --oneline`, `diff --check` trên SKILL/hai harness/RESULTS, `git -C repo diff --exit-code 1d7b9f4 HEAD -- .agents ops/acceptance/wp1389/residue_matrix.sh ops/acceptance/wp1389/residue_matrix.ps1` — rc 0.
- `python -B -` kiểm SRI và byte tarball — rc 0. `python -B -` đối chiếu ID các ca với mutant — rc 0. Probe Bash trên `scratch/receipt-byte-probe`: ghi bằng `printf` rc 0, phép so command substitution rc 0 và có cảnh báo bỏ NUL, `cmp -s` rc 1.
- Các nhóm đọc bằng `cat`, `nl`, `sed`, `rg`, `head`, `tail`, `wc` cho chỉ dẫn, spec, lease, verdict cũ, mã, nguồn, harness, RESULTS và log — rc nhóm 0, trừ nhóm kết thúc bằng `command -v pwsh` rc 1. `bash --version | head -1` rc 0. Tra tài liệu Microsoft và mã nguồn PowerShell qua web trả kết quả, không có mã thoát shell.
- `python -B repo/.claude/dev/packet_loop.py doctrine-scan --root repo` — rc 0, quét 12 tệp, 0 chỗ chép doctrine. Kiểm lại trạng thái checkout — rc 0, cây sạch.

## Lượt 7 (Codex CLI, 2026-11-18T14:48:37Z → 14:51:53Z, rc 0; chép nguyên văn `scratch/VERDICT.md`)

# WP1389 r1 — review độc lập lượt 7

reviewed_sha: 3c524fce69931fc38a23ba9056b1b24cb71f4049
verdict: request_changes
reviewer: codex (OpenAI), codex_cli, read-only

HEAD khớp HEAD_SHA.txt, tree cb3d08340819dbe4876844d830849d78f9cc7308, checkout sạch trước và sau review. Base là tổ tiên của HEAD, blob SKILL tại base khớp spec. SHA-256 spec là 12257fa8d659ff5c013af4bc31de700de4a53b085a99ec8c47cbd403d66610bc. Lease ghi budget_nang_tran_4, used 6, reserved 1, limit 7.

## Finding chặn merge

- **P1 — Capture Bash có thể cho CLI cắt rỗng tệp .err đã có trên cache Linux không phân biệt hoa thường.** `.agents/skills/playwright-browser/SKILL.md:195–208`, đặc biệt dòng 203, và nguồn ghim `cli-client/session.js:121–126`. Trên một thư mục cache Linux có tra cứu tên không phân biệt hoa thường, chẳng hạn thư mục ext4 bật casefold, giả sử thư mục hash đã chứa tệp .err với các chữ hex trong nonce được viết hoa. `find -name` so tên phân biệt hoa thường nên preflight có thể thấy 0 mục. Tuy nhiên tra cứu đúng pathname chữ thường của Node có thể mở chính tệp đã có với cờ `w`, làm mất byte trước khi Cleanup chạy. Limits hiện bao gồm Linux x64 và giả định cache tin cậy, nhưng tình huống này không cần liên kết, can thiệp đồng thời hay cache không tin cậy. Đây là lỗi có sẵn trong thiết kế preflight, phát hiện khi đối chiếu hai shell ở lượt 7. Thêm chốt tra cứu pathname chính xác mà Node sẽ mở, từ chối khi mục đã tồn tại, kể cả symlink treo, và dừng nếu lỗi tra cứu khác trường hợp vắng mặt. Giữ phép quét B1 cho các mục cùng nonce ở các thư mục khác. Ca test do executor dựng trên cache Linux casefold, chỉ đặt biến thể hoa tại hash hiện hành, ép nonce fixture có chữ hex, rồi yêu cầu không chạy open, byte và mtime của tệp giữ nguyên. Gỡ chốt tra cứu trực tiếp phải làm ca lọt. Ca này là suy luận từ mã, chưa được chạy trong review.

## Đối chiếu từng chốt chặn của lượt 6

| Chốt | Trạng thái ở HEAD |
|---|---|
| P1 PowerShell có thể xoá sai tên do phép so theo văn hoá | **Đã sửa.** SKILL:253 và :452 dùng Equals Ordinal cho ràng buộc hash và đường dẫn đích. :452–464 chỉ chép/xoá mục đã qua chốt. N26 PS có mutant riêng. Executor báo mutant tái hiện trên cả 5.1 và 7. |
| P2 đầu Cleanup nhận 00 khác byte | **Đã sửa.** SKILL:341–346 và :402–411 bắt tệp thường, so dữ liệu thô với ba dòng và LF cuối trước :354/:429. D12 và mutant record-bytes đo byte NUL trên Bash và BOM trên PS theo mã harness. |
| P2 Gỡ nhận 00 hoặc 11 khác byte | **Đã sửa.** SKILL:485–493 và :505–520 kiểm loại tệp, trích nonce rồi so byte của cả hai biên nhận. Việc đọc dòng nonce bằng sed hoặc ReadAllText không quyết định một mình, vì cả tệp vẫn phải qua cmp hoặc ReadAllBytes. G13/G14 và mutant tương ứng tách hai chốt. |

Bản verdict lượt 6 gộp hai hàng P2 trên vào một bullet. P3 về sentinel cũng đã sửa tại SKILL:202,345,374,493. Sentinel được in sau khi realpath thành công, đồng thời giữ LF cuối đường dẫn trong phép so.

## B1–B8 và kiểm tra delta

- **Nguồn ghim.** SRI SHA-512 của cả ba tarball khớp lockfile. 16 tệp CLI và 116 tệp core trong cây giải nén trùng byte với tarball. `registry.js:119–165` xác nhận hook test, cache Linux/Windows, nhánh macOS ngoài phạm vi, hash SHA-1 cắt 16 hex trên workspaceDir hoặc packageRoot. `session.js:73–97,121–126` xác nhận chỉ delete-data chọn .session và ud- cùng phiên, .err mở bằng w. Nguồn registry trình duyệt trong coreBundle dùng cache ms-playwright/b riêng. README, session-management và chương trình ghim không cung cấp tuỳ chọn chuyển sổ phiên được hỗ trợ. --profile và --config phục vụ cấu hình trình duyệt. Phương án (a) vẫn không khả dụng theo định nghĩa spec.
- **B1/B2.** Probe và CLI dùng cùng Node, CWD work và môi trường kế thừa qua các wrapper thông thường (SKILL:180–184,194–205,216–225,246–263). JS ASCII được truyền thành một đối số, không có dấu nháy kép nhúng. Base64 giữ Unicode qua stdout. Node xử lý XDG_CACHE_HOME rỗng và slash cuối, Windows lấy LOCALAPPDATA hoặc home của Node. Cache thiếu cho qua preflight, cache rỗng trả 0 mục, Cleanup cần cả hai thư mục hiện hữu. Bản ghi tạo mới trước open, thiếu hoặc khác thì đầu Cleanup dừng. Có bản ghi chưa chứng minh open thành công. E4/E7/E8 phân biệt các thời điểm dừng ở mức fixture. Bảng ghim, Setup, Kiểm pin và lệnh 08–10 giữ nguyên.
- **B3/B4.** Bash dùng mapfile -d với NUL, wait PID quét, rồi so đường dẫn chính xác và loại tệp. PS bỏ qua thư mục con reparse khi liệt kê, kiểm tổ tiên của đích và dùng ordinal cho mục duy nhất. Tên ngắn 8.3 không chứa trọn nonce dài 18 ký tự. Đường dẫn UNC chưa được đo. Hai shell ghi 11-path, chép, so, xoá, kiểm mất, theo thứ tự đó. Ngoài lỗi preflight nêu trên và giới hạn dưới đây, không thấy đường mới xoá nhầm đích hoặc báo OK khi bước dọn chưa đạt.
- **Pipeline và UTF-8.** Pipe có ưu tiên cao hơn danh sách &&/||. Không bật pipefail ở Cleanup/Gỡ nghĩa là status cmp quyết định. Một luồng bị cắt ngắn so với biên nhận hợp lệ bị cmp từ chối. Probe cục bộ cho thấy luồng đủ byte vẫn khớp dù producer báo lỗi, còn luồng ngắn trả 1. Với printf format cố định và stdout là pipe, không tìm thấy đường mà lỗi producer thực tế làm biên nhận sai khớp. PowerShell tiếp dòng sau dấu phẩy bên trong đối số phương thức, dấu chú thích không làm mất dấu phẩy. GetBytes không chèn preamble, Capture ghi UTF-8 no BOM và LF, WriteAllText hai đối số mặc định ghi UTF-8 no BOM, ReadAllBytes giữ nguyên BOM nếu bị thêm. Executor báo cả PS 5.1 và 7 đã chạy các khối có cú pháp này.
- **B5/B6.** Marker vẫn bao đúng phần dọn. Dọn xong mới băm và in CLEANUP OK. CLI giả của E1/E6/E8 mô phỏng JSON/LF, rc, trạng thái mở và nhánh deleted theo descriptor cho các tình huống harness dùng. Fixture không mô phỏng đầy đủ launcher hay userdata. N3/N4 của ma trận dựng riêng dư lượng descriptor/userdata. Giới hạn bỏ qua lỗi xoá registry trình duyệt trong close vẫn cần đọc cùng kết quả CLEANUP OK.
- **B7/B8.** Gỡ kiểm 00/11 và hỏi CLI trước khi xoá install, sau đó chỉ rmdir hoặc Directory.Delete với false. Evidence khai cả hai output 11. Limits nêu phạm vi file, thư mục, .err cũ, cache dùng chung, mô-đun nội bộ và Bash tối thiểu 4.4. Nên bổ sung fallback Windows của LOCALAPPDATA vào Limits.

## Findings không chặn merge và giới hạn đã khai

- **P3 — N26 có thể quy nhầm lỗi fixture thành runtime không tái hiện.** `ops/acceptance/wp1389/residue_matrix.ps1:478–482`. Nếu mutant dừng vì parse, IO hay chốt khác, nhánh else vẫn ghi SKIP với lý do -ceq không bỏ qua U+00AD. Sửa bằng probe so sánh độc lập trên hai tên và kiểm riêng lý do thất bại của mutant. Ca test cho mutant gặp lỗi trước chốt tên và yêu cầu FAIL thay vì SKIP. Executor báo mutant đạt đường lọt trên cả hai runtime đã đo nên nhược điểm này chưa làm mất bằng chứng của lượt đó.
- **P3 — Cache và cây run cần ổn định.** SKILL:202,374–386,442–464,493–526,544–547. Sau lần kiểm cuối, các thao tác dựa trên pathname. Một tiến trình đồng quyền có thể tráo thư mục hoặc biên nhận giữa kiểm và dùng. Limits đã khai giả định cache tin cậy. Nếu mở rộng mục tiêu sang thay đổi đồng thời, cần thao tác neo vào thư mục đã mở và kiểm danh tính đối tượng. Ca xác nhận do executor dựng sẽ thay thư mục sau chốt và kiểm mục ở đích giữ nguyên. Review không dựng fixture đường dẫn thoát cây.
- `git diff --check d0d4879..HEAD` báo trailing whitespace tại harness Bash :399,400,437,446 và hai dòng xuống hàng Markdown trong verdict lưu :326–327. Lỗi trình bày, không ảnh hưởng phép đo.

## Độ phủ ma trận

- Bash không có mutant đích riêng theo log hoặc có mutant nhắm ca khác: P1/P2, C1/C2/C3/C6/C8/C10/C12/C13/C17, D3/D4/D6/D8, E3/E4/E5/E7/E8, G1/G4/G7/G8, N1/N2/N4/N6/N9/N11/N12/N16/N19/N20R/N21/N25/N26 và biến thể N8-path. D12/G13/G14 có mutant đích mới, đều lọt.
- PS không có mutant đích riêng theo mã: P1/P2, C1/C2/C3/C6/C8/C10/C12/C13, D3/D4/D6/D8, E3/E4/E5/E7/E8, G1/G4/G7/G9, N1/N2/N4/N5/N6/N9/N11/N12/N13/N19/N20R, L2 và W1. Chưa có mutant riêng cho so nội dung bản sao PS hoặc phép ordinal ở pre-open. D10/G10 có mutant nhưng executor báo SKIP.
- **Có mặt mà chưa cô lập được phép đo.** N25 chạy qua đầu Cleanup, có thể dừng trước chốt residue. G8 chỉ kiểm giữ cây, rmdir tự từ chối symlink nên kết quả chưa chứng minh pha (1) từ chối biên nhận. N20R chạy riêng residue nhưng mutant dùng N20. D2 đổi đầu ra registry giả, chưa đo thay đổi CWD/môi trường của registry thật. Các ca Gỡ PS kiểm cây cuối nhưng chưa bắt buộc có cảnh báo GIỮ. N26 Bash kiểm yêu cầu đích đúng, không đo khác biệt giữa ordinal và so theo văn hoá. N13 Windows không đo cache casefold của Linux. Các ca dừng thường cho phép thông báo STOP chung.

## N1 độc lập

```text
SOURCE 01b08e953c5f012fdb7ab2f2c0c62a913d670536da47360d30c6469e66f1a776 pre_frag 79d485ba6e16310e512e886b76d4d8e1328eb2a45e00c35975368512589c89b6 dau_frag 84a893f5600389fae3bf2ba8c27a4650eeaf1bbeda8d7ec858a73006e84eadda cleanup_frag 2198f91d554fcbe0c17a5ab6ac6238281501ace9d0c01debbb82a4845a425f2e go_frag b63d3f537755e5c97f92c996dab3a5acd032f66923482dca855c336de54bcf2c node v22.23.5
TONG: 123 dat / 123
```

## Không đo được và bằng chứng executor

- **Windows N5-err-symlink: KHÔNG ĐO ĐƯỢC.** Executor báo D10, G9, G10 và mutant record-reparse/go-record-reparse cũng không dựng được. N2 theo lời khai trên 8be8070 là 122/122 và 6 SKIP ở mỗi shell. Review không tự chạy Windows.
- RESULTS §10 báo N3/N4 native trên 8be8070 khớp snapshot trước/sau, gỡ được hash directory và giữ nguyên 15 .err cũ trên Windows, gồm 13 tệp chỉ định. Tôi xác minh SKILL và hai harness trùng byte giữa commit đo và H. Tôi không tự chạy native.
- Chưa đo cache Linux casefold, UNC, Bash 4.4, host có cache hoàn toàn mới hoặc thời gian daemon thật nhả handle. N1 dùng Node v22.23.5 có sẵn, khác Node ghim của lượt native. CI bắt buộc trên H chưa được xác minh. Doctrine-scan local đạt.

## Lệnh và mã thoát

- cat HEAD_SHA.txt, git -C repo rev-parse HEAD, rev-parse HEAD^{tree} và blob base, merge-base --is-ancestor, git --no-optional-locks -C repo status --porcelain=v1 --untracked-files=all trước/sau, sha256sum spec, các nhóm đọc cat/nl/sed/rg/ls và diff đọc SKILL/harness/RESULTS — rc 0. command -v pwsh — rc 1, không có pwsh.
- mkdir scratch/n1 rồi bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1 "$(command -v node)" — rc 0, đúng một lần. Log scratch/n1.log.
- python -B - kiểm SHA-512 và byte từng file tarball — rc 0. git -C repo diff --exit-code 8be8070 HEAD -- .agents/skills/playwright-browser/SKILL.md ops/acceptance/wp1389/residue_matrix.sh ops/acceptance/wp1389/residue_matrix.ps1 — rc 0.
- git -C repo diff --check d0d4879..HEAD — rc 2 theo mã báo lỗi whitespace của git diff --check. Bash probe pipe cmp — luồng đầy đủ rc 0, luồng bị cắt rc 1. python -B repo/.claude/dev/packet_loop.py doctrine-scan --root repo — rc 0 (12 tệp, 0 vi phạm).

## Lượt 8 (Codex CLI, 2026-11-18T15:07:48Z → 15:11:14Z, rc 0; chép nguyên văn `scratch/VERDICT.md`)

# WP1389 r1 — review độc lập lượt 8

reviewed_sha: 277db46263883c05d6d3e839d0c4661d7b95597f
verdict: approve
reviewer: codex (OpenAI), codex_cli, read-only

## Findings chặn merge

Không có P0–P2 mới trong delta lượt 8. **P1 lượt 7 đã sửa.** Bash vẫn quét toàn sổ phiên ở độ sâu 2 tại `.agents/skills/playwright-browser/SKILL.md:203`, sau đó kiểm trực tiếp cả hai tên ở :204–205 bằng `-e` và `-L`. Trên cache casefold, pathname chữ thường được tra theo cùng quy tắc filesystem mà Node dùng. Tệp đã có, kể cả symlink treo, chặn bước tạo bản ghi :207 và `01-open` :210. Điều này đóng đường cắt rỗng tệp cũ bằng `openSync(..., "w")` ở nguồn ghim `session.js:121–126`. PowerShell giữ phép quét :259–263 và bổ sung `Test-Path -LiteralPath` :264–265 trước CreateNew :266 và open :271. C19/C20 và hai mutant xác nhận từng chốt Bash qua mô phỏng. Bằng chứng trên cache casefold thật vẫn còn thiếu.

## Findings không chặn merge

- **P3 — C20 đo việc dừng, còn bảo toàn descriptor chưa được đo.** `ops/acceptance/wp1389/residue_matrix.sh:174–176,198–201`, `ops/acceptance/wp1389/RESULTS.md:249–251`. C20 sẽ vẫn báo PASS nếu preflight sửa hoặc xoá descriptor rồi trả STOP mà chưa ghi 00. C19 có snapshot trước/sau. Thêm snapshot tồn tại, loại, byte và mtime cho C20 và giới hạn câu công bố theo assertion hiện có. Ca tự kiểm nên thay một byte hoặc xoá descriptor trước STOP và yêu cầu harness báo FAIL.

## Đối chiếu đặc tả và nguồn

- HEAD khớp HEAD_SHA.txt, tree `81a11067e53ccc31a7d6c46ffb0044ab6bbb7217`, worktree sạch trước và sau. Base là tổ tiên của H, blob base đúng `678ba2f0209690c535d9827ae8badbe7fff85748`. SHA-256 đặc tả đúng `12257fa8d659ff5c013af4bc31de700de4a53b085a99ec8c47cbd403d66610bc`. Diff nằm trong write set. Lease dành một lượt review cuối trong trần 8.
- Ba tarball khớp SRI SHA-512 trong lockfile. Đối chiếu byte 16 tệp CLI và 116 tệp core giải nén với tarball. `registry.js:119–165` xác nhận hook test, fallback cache Linux/Windows, nhánh macOS ngoài phạm vi, và 16 hex đầu SHA-1 của `workspaceDir || packageRoot`. `session.js:73–97,121–126` xác nhận phạm vi `deleteData` và cách mở `.err`. `coreBundle.js:54240–54242,54361–54362` xác nhận cache `ms-playwright/b` và hook riêng. README, session-management và mã client ghim không cho thấy tuỳ chọn CLI được hỗ trợ để dời sổ phiên. `--profile` và `--config` cấu hình trình duyệt. Phương án (b) vẫn có căn cứ.
- **B1/B2.** Probe và CLI dùng cùng Node, CWD `work` và môi trường kế thừa qua wrapper. Node xử lý `XDG_CACHE_HOME` rỗng hoặc có slash cuối và fallback Windows. Cache thiếu và cache rỗng có thể đi qua Capture. Cleanup cần sổ phiên và hash tồn tại, kiểm byte của 00 gồm nonce cùng loại và đường dẫn thư mục trước close (SKILL:337–358,397–433). Capture dừng tại chốt mới thì chưa tạo 00. Các phản hồi 08–10, Setup, Kiểm pin và bảng ghim giữ nguyên so với base. Bash dùng quét phân biệt hoa thường, Windows dùng wildcard theo filesystem .NET. Tra đúng tên bảo vệ hai pathname CLI dùng trong thư mục hash hiện hành, phép quét ở các hash khác vẫn theo quy tắc cũ.
- **B3–B6.** Bash đếm mục phân cách NUL và kiểm rc quét qua `wait`. PowerShell duyệt hai tầng, bỏ qua thư mục con reparse và so đích ordinal. Cả hai yêu cầu đúng một tệp thường ở hash đã neo, ghi 11-path, chép và so trước xoá, kiểm đã mất rồi mới băm và in OK (SKILL:375–394,441–473). Tên 8.3 không đủ dài chứa nguyên nonce. Trong cây cache ổn định theo Limits, tôi không thấy đường mới xoá tệp sai đích hoặc in OK sau khi bước dọn thất bại. Các đoạn làm sạch và hợp đồng CLI giả không đổi trong delta. Fixture toàn luồng đo thứ tự và phản hồi cố định, còn fixture residue đo riêng tệp sót. Marker giữ nguyên.
- **B7/B8.** Gỡ đối chiếu nguyên byte hai biên nhận với câu trả lời CLI trước khi xoá install, chỉ xoá thư mục hash đã kiểm bằng thao tác không đệ quy (SKILL:475–530). Evidence khai hai output 11. Limits khai phạm vi thư mục còn lại, `.err` cũ, mô-đun nội bộ, cache dùng chung và giới hạn đo casefold (SKILL:536–553). Dòng mô tả cache Windows có thể bổ sung fallback khi LOCALAPPDATA thiếu/rỗng để khớp nguồn ghim.

## Độ phủ và giới hạn đã khai

- C19/C20 có mutant bỏ từng chốt, cả hai lọt đúng mục tiêu. Chưa cô lập mutant cho riêng `-L` trên hai tệp đích Capture hoặc cho lớp tra tên bổ sung trên Windows. Ca dương Windows do executor báo chỉ đo lớp bổ sung cho qua khi vắng mục.
- Các ca thiếu mutant đích riêng đã ghi ở lượt 7 và không đổi ngoài C19/C20. Bash gồm nhóm P1/P2, C1/C2/C3/C6/C8/C10/C12/C13/C17, D3/D4/D6/D8, E3/E4/E5/E7/E8, G1/G4/G7/G8, N1/N2/N4/N6/N9/N11/N12/N16/N19/N20R/N21/N25/N26 và biến thể N8-path. PS gồm P1/P2, C1/C2/C3/C6/C8/C10/C12/C13, D3/D4/D6/D8, E3/E4/E5/E7/E8, G1/G4/G7/G9, N1/N2/N4/N5/N6/N9/N11/N12/N13/N19/N20R, L2 và W1. D10/G10 PS có mutant nhưng executor báo SKIP. Phép so bản sao PS và ordinal ở pre-open chưa có mutant riêng.
- Những ca chưa cô lập phép đo vẫn gồm N25 (có thể dừng ở đầu Cleanup), G8 (rmdir tự từ chối symlink), N20R (mutant nhắm N20) và D2 (sổ phiên giả). Các ca Gỡ PS chủ yếu xác nhận trạng thái cuối, chưa buộc có biên nhận GIỮ. N26 PS vẫn có thể gán lỗi khác của mutant cho runtime không tái hiện nếu chưa kiểm riêng nguyên nhân.
- Kiểm tra thư mục rồi thao tác theo pathname giả định cache ổn định và tin cậy. Tiến trình đồng quyền có thể thay thế thư mục hoặc biên nhận trong cửa sổ giữa kiểm và dùng, như Limits đã khai. Không dựng ca đường dẫn thoát cây trong review.

## N1 độc lập

```text
SOURCE 5b965c597b07e2357fed072018edc8b8a5e7b608303405be81a1a8c649945879 pre_frag 4095df8f66bf807f9984b17508166f95cafd6ca7b847a8a0733225f3ae064d44 dau_frag 84a893f5600389fae3bf2ba8c27a4650eeaf1bbeda8d7ec858a73006e84eadda cleanup_frag 2198f91d554fcbe0c17a5ab6ac6238281501ace9d0c01debbb82a4845a425f2e go_frag b63d3f537755e5c97f92c996dab3a5acd032f66923482dca855c336de54bcf2c node v22.23.5
TONG: 127 dat / 127
```

## Không đo được và bằng chứng executor

- **Windows N5-err-symlink: KHÔNG ĐO ĐƯỢC.** Executor ghi N2 trên `511cf5f` đạt 122/122 và 6 SKIP ở mỗi shell. Các lượt trước ghi thêm D10, G9, G10 và hai mutant reparse là SKIP vì thiếu quyền tạo symlink tệp. Không có lượt Windows độc lập.
- RESULTS §11 ghi N3/N4 native trên `511cf5f` có snapshot trước/sau trùng byte, đã gỡ thư mục hash và giữ 15 tệp `.err` cũ trên Windows, gồm 13 tệp chỉ định. Đã xác minh SKILL và hai harness trùng byte giữa commit đo và H theo quy tắc nhận bằng chứng của lease. Đây là lời khai executor về N2–N4. Review chỉ tự chạy N1, dùng Bash 5.2.21 và Node v22.23.5.
- ext4 casefold thật, UNC, Bash 4.4, cache mới hoàn toàn và thời gian daemon thật nhả handle chưa được đo độc lập. CI bắt buộc trên H chưa được xác minh. Doctrine-scan local đạt 12 tệp, 0 vi phạm. Verdict này đánh giá mã và bằng chứng review, còn trạng thái CI cần được xác nhận ở cổng merge.

## Lệnh và mã thoát

- `cat HEAD_SHA.txt`, `git -C repo rev-parse HEAD`, `git -C repo rev-parse 'HEAD^{tree}' 'eca1d125b8:.agents/skills/playwright-browser/SKILL.md'`, `git -C repo merge-base --is-ancestor eca1d125b82783a6a736c7023751ba53cc9a49c8 HEAD`, `git --no-optional-locks -C repo status --porcelain=v1 --untracked-files=all` trước/sau, `sha256sum repo/ops/specs/wp1389-r1.md` — rc 0.
- `mkdir scratch/n1 && bash repo/ops/acceptance/wp1389/residue_matrix.sh repo/.agents/skills/playwright-browser/SKILL.md scratch/n1 "$(command -v node)"` — rc 0, chạy đúng một lần, redirect vào `scratch/n1.log`.
- `git -C repo diff eca1d125b8..HEAD -- .agents/skills/playwright-browser/SKILL.md`, diff delta và write set, `git -C repo diff --exit-code 511cf5f HEAD -- .agents/skills/playwright-browser/SKILL.md ops/acceptance/wp1389/residue_matrix.sh ops/acceptance/wp1389/residue_matrix.ps1`, `git -C repo diff --check 3c524fc..HEAD` — rc 0.
- `python -B -` kiểm SRI và byte tệp giải nén — rc 0. `python -B repo/.claude/dev/packet_loop.py doctrine-scan --root repo` — rc 0. Các nhóm đọc `ls`, `cat`, `nl`, `sed`, `rg`, `tail`, `find` và kiểm phiên bản Bash — rc 0 ở cấp nhóm. Lệnh dò đầu dùng sai vị trí session-management và báo lỗi IO, đã tìm được đúng tệp dưới `package/skills/playwright-cli/references/` và đọc lại. `command -v pwsh` — rc 1.
