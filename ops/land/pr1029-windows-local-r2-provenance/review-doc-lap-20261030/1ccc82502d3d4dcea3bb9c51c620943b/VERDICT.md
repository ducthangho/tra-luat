verdict: approved
reviewed_sha: 9aa725c72b6b38263de366ce34a80fb384a522a0
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Review độc lập hai trục **Spec** và **Standards/Security**. Áp ngưỡng của assignment/spec: chỉ approved khi 0 P0–P3, với `effective_review_class: sensitive`. Không có finding có bằng chứng trên diff được giao.

## Neo và phạm vi

- HEAD đầu/cuối kiểm tra: `9aa725c72b6b38263de366ce34a80fb384a522a0`; tree: `a5820b68a689c8a07bc4c53ccb3ba927e56f6033`.
- Base là parent trực tiếp: `5f3855eaf47e024b6c63f8923f64d8f80c5de707`. Checkout detached; clone không shallow; `core.abbrev=7`; origin là `https://github.com/ducthangho/tra-luat.git`.
- SHA-256 đặc tả đầu/cuối: `4c92ecbf38fb7f5f97ddea64ed4a43f1cbc9e7a826e87fd8c234dc7e25677c2b`; bytes đặc tả tại base và HEAD giống nhau.
- `lease.yaml`: packet `WINDOWS-LOCAL-MAY-CHU-KHO`, r2/g1, mission #748, executor `anthropic_claude`, reviewer `openai_codex`, effective class `sensitive`. Diff chỉ chạm đúng hai path trong write set; 68 dòng thêm, 2 dòng xoá, dưới trần 120 dòng thêm.
- Diff tự lấy từ Git khớp byte `diff.patch`: 10.069 byte; SHA-256 `0b149d9024ebd6bc1ff549a2aa3f2ac09f47a2a5188beeaf632541e2bd8062a4` ([bản đối chiếu](evidence/actual.diff.patch)).

## Spec

| Yêu cầu đặc tả | Vị trí đối chiếu trên HEAD | Kết quả |
|---|---|---|
| §2.1: thêm ADR Accepted; sửa đúng Phạm vi/Khoá, giữ phần khác; tiền lệ ADR-0056/ADR-0017 | `docs/adr/0058-windows-local-han-khoa-va-pham-vi-may.md:3–8`; ADR-0056:11–24; ADR-0057:31–49 | Đạt. Các số §1/§3 trỏ đúng các mục quyết định có tên Phạm vi/Khoá. Blob ADR-0057 không đổi: `f13b364c6834f016387c3c96fca6aacb21f9a5b5`. |
| Phạm vi theo `list_devices`, `Online`, cấm tự đi đường khác vào máy ngoài danh sách | ADR-0058:22–25 | Đạt. VM chỉ vào phạm vi khi xuất hiện trong danh sách và đáp ứng điều kiện Online của câu đầu. |
| Khoá/sổ đo riêng từng máy, gốc D hoặc C khi không có D; diễn giải lại các đường dẫn; `ghi_chu` có `may=…` | ADR-0058:26–28 | Đạt; bao phủ cả đường dẫn cô lập và sổ đo được giữ từ ADR-0057. |
| Dòng khoá bốn trường; hạn ≤2 giờ; gia hạn | ADR-0058:29–32 | Đạt; không thêm trần hoặc điều kiện ngoài đặc tả. |
| Hết hiệu lực (a) quá hạn, (b) dòng cũ quá 2 giờ, (c) chủ khoá tuyên bố bỏ; bằng chứng riêng cho (c) | ADR-0058:33–37 | Đạt; (c) đòi tin nhắn chính phiên hoặc comment trên PR của nó. |
| Thứ tự tiếp nhận: kiểm tải → ghi sổ khoá cũ/session/UTC/lý do → thay dòng khoá; cấm dừng tiến trình khác | ADR-0058:38–40, 50; ADR-0057:38–39 | Đạt; con trỏ kiểm tải đúng mục §4. |
| Chép D7–D9 và khai không có cổng cưỡng chế | ADR-0058:14–18, 52–57; đặc tả:18–22, 33 | Đạt. Cả ba ô số đo, mọi token số và định danh backtick khớp; D7 chỉ bỏ một dấu phẩy không đổi nghĩa. |
| §20 đúng một dòng ADR-0058, cột cổng chính xác; chỉ sửa ô mô tả ADR-0057 | `docs/PROTOCOL_DA_PHIEN.md:1537–1538` | Đạt. Cột cổng là `không cổng — kỷ luật executor`; ba ô khác của dòng ADR-0057 giữ nguyên byte. |
| §10.2 nhắc cả hai ADR, con trỏ trung tính | protocol:1015 | Đạt: “Quy ước sử dụng máy Windows local của chủ kho nằm tại `ADR-0057` và `ADR-0058`.” Câu chỉ định vị quy ước, không tạo nghĩa vụ mới. |
| Không chép thêm doctrine vào protocol; giữ đúng phạm vi sửa | Toàn diff protocol so với base | Đạt. So byte chứng minh chỉ có câu con trỏ, ô mô tả ADR-0057 và một dòng mới ADR-0058. |

Đã đọc toàn bộ 65 dòng ADR-0058, 73 dòng ADR-0057, ADR-0056 và các phần protocol liên quan. Không phát hiện quy tắc của ADR-0058 mạnh hơn/rộng hơn đặc tả, hoặc mâu thuẫn ở các phần ADR-0057 được giữ lại. Việc thêm `may=…` dùng cột `ghi_chu` hiện có nên không đổi schema cột sổ đo. Khoá vẫn không nguyên tử; ADR-0058:48–49 nêu rõ rủi ro hai phiên cùng tiếp nhận, phù hợp ngoài phạm vi §5 của đặc tả.

## Standards/Security và lời khai

Đã quét các lớp sau trên toàn bộ hai tệp thay đổi và tài liệu nguồn tương ứng; không có lớp lỗi mở (0 lớp, 0 biểu hiện):

| Lớp đối chiếu | Bằng chứng và kết quả |
|---|---|
| Nới phạm vi/quyền truy cập hoặc quyền dừng tiến trình | ADR-0058:22–28, 38–40, 50, 57, 63–65 khớp spec:26–32, 53–55. Không cấp credential, thêm đường vào VM hoặc quyền dừng tiến trình. |
| Thiếu điều kiện/thứ tự thao tác khoá; khẳng định nguyên tử sai | ADR-0058:29–40, 48–49 so với spec:28–32, 53 và ADR-0057:36–39, 63–65: đủ hạn/gia hạn/(a)/(b)/(c)/bằng chứng/thứ tự; không hứa khoá nguyên tử. |
| Lời khai “KHÔNG đổi” làm mất điều kiện cũ | ADR-0058:42–50 so với ADR-0057:33–57 và protocol §8/§10.2: giữ điều kiện lỗi do diff, khai lỗi nền kèm SHA, offline/không đo local, CI/branch protection/review class, cô lập, môi trường, tiến độ, sổ đo, bằng chứng và mốc xem xét lại. |
| Sai số liệu, session, SHA, PR/issue, tên tệp hoặc dẫn mục | D7–D9 so trực tiếp từng ô số đo với spec; Git resolve cả ba SHA; `git ls-files` xác nhận các ADR/spec. Các PR/issue và comment authority được đọc qua GitHub GET, chi tiết bên dưới. |
| Khai cổng cưỡng chế vượt bằng chứng; con trỏ biến thành luật | Đọc `cmd_adr_song` tại `.claude/dev/packet_loop.py:1916–2007`: kiểm cấu trúc/định tuyến/trạng thái, không thực thi luật máy Windows. Quét code/config dưới `.claude/dev`, `scripts`, `.github` không tìm thấy các token vận hành khoá/sổ đo/thiết bị. Diff chỉ có Markdown. Câu protocol:1015 trung tính; cột cổng khớp spec. Giới hạn quét nằm trong [enforcement-scan.json](evidence/enforcement-scan.json). |
| Câu tự mâu thuẫn hoặc có hai nghĩa làm đổi hành vi executor | Đọc chéo quyết định, “KHÔNG đổi”, “Không cổng” và các phương án bị loại; không tìm được biểu hiện có hậu quả ngoài nội dung đặc tả đóng băng. |

Các tham chiếu lịch sử đã kiểm:

- [Comment 6514073214, PR #1025](https://github.com/ducthangho/tra-luat/pull/1025#issuecomment-6514073214): tác giả `ducthangho`, association `OWNER`, tạo `2026-10-30T03:15:32Z`; mục 1 duyệt đúng đường dẫn đặc tả, full hash và cấp lease r2/g1. Khớp ADR-0058:3–5; lưu [JSON nguồn](evidence/authority-comment-6514073214.json).
- [PR #1025](https://github.com/ducthangho/tra-luat/pull/1025) có head `6c1436af07704b20df2506bc05f3c726ef04e1e3`, merge `5f3855eaf47e024b6c63f8923f64d8f80c5de707`, khớp base/authority. [Issue #748](https://github.com/ducthangho/tra-luat/issues/748) tồn tại.
- D9: `9666771` resolve thành `96667715996d41bc45e70a64fbaa8996de20f6a0`; `10446ff` thành `10446ffa400725b23189ad9c4902932d5eb969bc`; `f4d15ed` thành `f4d15edcb5d0a9742182273e5950f76165060667`.
- [PR #1022](https://github.com/ducthangho/tra-luat/pull/1022) có đúng head `f4d15ed…`, base `9666771…`, merge `d31df1e…`. [PR #1007](https://github.com/ducthangho/tra-luat/pull/1007) về sau có head `76b6593…`; `10446ff…` là tổ tiên của head đó. Commit thay head có timestamp `2026-10-29T11:43:59Z`, sau khoảng đo D9 `11:39:56Z–11:40:20Z`; head cuối PR khác head lúc đo không tạo mâu thuẫn. [Metadata đã lọc](evidence/github-reference-metadata.json) chỉ chứa thông tin PR/issue, không chứa nội dung review.
- Hai session ID ở D7 khớp nguyên văn đặc tả. Số đo trên máy Windows và tin nhắn phiên ngày 29-10 là dữ liệu nguồn đóng băng; lượt này kiểm tính chép đúng và các object/quan hệ Git, không tái đo thiết bị hay xác thực lại log phiên gốc không được cấp.

## Độc lập và assurance §8.1/§8.2

- Reviewer `openai_codex`, context mới theo assignment; tự đọc spec/diff và tự chạy các phép kiểm. Không đọc verdict lượt 1 của r2 hoặc verdict review cũ khác để suy kết luận.
- Ghi trong sandbox: `VERDICT.md` và `evidence/`. Không sửa `cay-kho/`, cấu hình Git, branch, index hoặc refs. Shell thực chạy là Bash trên Linux, Python `3.13.16`, Git `2.43.0`; transport công cụ là machine. Sandbox được khai trong phiên là `workspace-write`, approval `never`; vì checkout nằm trong writable root nên đây không phải bằng chứng filesystem cưỡng chế read-only riêng cho checkout.
- Ba gate dùng `PYTHONDONTWRITEBYTECODE=1`, `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, `GIT_OPTIONAL_LOCKS=0`; `TMPDIR` và `TL_CACHE_DIR` trỏ vào `evidence/tmp` và `evidence/cache`, ngoài checkout. Lệnh đo và stdout/stderr thô nằm trong [commands.json](evidence/commands.json).
- Trước/sau các gate: HEAD/tree không đổi; `status --ignored`, diff worktree, diff index đều rỗng. Cuối lượt danh sách untracked và ignored đều rỗng ([final-commands.json](evidence/final-commands.json)). Các kiểm Git này bổ sung cho snapshot nội dung đầy đủ do phiên điều phối chụp ngoài sandbox theo assignment; tôi chưa đọc các snapshot bên ngoài đó và không thay chúng bằng lời khai status sạch.
- Snapshot hai mốc chỉ chứng minh không có delta quan sát được giữa hai mốc, không chứng minh toàn lịch sử không từng ghi rồi hoàn nguyên. Repo nguồn ngoài sandbox không nằm trong phạm vi quan sát của reviewer.
- Model/effort phục vụ từng request, session/run ID của launcher, rc cuối launcher/tiến trình reviewer và hash output sau khi run kết thúc: `not_measured` từ trong lượt đang chạy; phiên điều phối nối evidence thực của run theo §8.1. `approved` ở đây là verdict nội dung exact SHA; việc nhận nhãn assurance từ receipt phải đối chiếu các evidence ấy và snapshot ngoài sandbox.
- Ruff pin/probe contract và bare Ruff lint: `not_run`; không thuộc ba tiêu chí được giao cho diff hai tệp Markdown này, không khai “Ruff passed”. Windows local: `not_run` trong lượt Linux này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Theo chỉ thị trực tiếp của lượt review độc lập này, không xem verdict lượt 1. Không gán trạng thái vá cho finding của lượt ấy. Đã kiểm lại toàn bộ acceptance từ spec/protocol trên đúng HEAD; kết luận và bảng lớp ở trên không dựa vào verdict trước. Câu con trỏ trung tính được đối chiếu độc lập với spec:37 và protocol:1015.

## Đã chạy

Ba lệnh bắt buộc dưới đây chạy với cwd tuyệt đối là thư mục `cay-kho/` của sandbox này; mã thoát lấy từ từng subprocess, không suy từ lệnh cuối chuỗi shell.

1. `python3 .claude/dev/packet_loop.py adr-song --root .` — **rc=0**, passed. Stdout thật:
   ```text
   adr-song: sạch — 57 ADR trên đĩa, 57 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])
   ```
   [stdout](evidence/11.stdout), [stderr rỗng](evidence/11.stderr).
2. `python3 .claude/dev/packet_loop.py doctrine-scan --root .` — **rc=0**, passed. Stdout thật:
   ```text
   doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
   ```
   [stdout](evidence/12.stdout), [stderr rỗng](evidence/12.stderr).
3. `python3 scripts/tl.py doc-claims-check --json` — **rc=0**, passed. Trường kết quả thật: `"ok": true`, `"files_scanned": 117`, `"advisory_count": 381`, `"layers_skipped": {}`, `"strict": false`; `flags=[]`, cả 10 lớp trong `by_layer` đều 0. Không có advisory thuộc ADR-0058/protocol. [JSON stdout đầy đủ](evidence/13.stdout), [stderr rỗng](evidence/13.stderr). Không gọi đây là strict pass.
4. `git diff --numstat 5f3855eaf47e024b6c63f8923f64d8f80c5de707 HEAD` — **rc=0**:
   ```text
   3	2	docs/PROTOCOL_DA_PHIEN.md
   65	0	docs/adr/0058-windows-local-han-khoa-va-pham-vi-may.md
   ```
   Tổng **2 tệp, 68 dòng thêm, 2 dòng xoá**; đúng write set.
5. `git diff --check 5f3855eaf47e024b6c63f8923f64d8f80c5de707 HEAD` — **rc=0**, stdout/stderr rỗng.
6. `git diff 5f3855eaf47e024b6c63f8923f64d8f80c5de707 HEAD -- 'docs/adr/0057-*'` — **rc=0**, stdout/stderr rỗng; không sửa ADR-0057.
7. Từ sandbox: `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python3 evidence/audit_spec.py` — **rc=0**; dòng cuối thật: `audit_spec: 28 passed, 0 failed`. Kiểm cơ học hash/base/diff/write set/kích thước, các ô D7–D9, thay đổi đúng ba vị trí protocol và object SHA. [Script](evidence/audit_spec.py), [kết quả](evidence/audit_spec.json). Phần đọc nghĩa được đánh giá riêng ở trên.
8. `git rev-parse HEAD 'HEAD^{tree}'` — **rc=0**, cả đầu/cuối: `9aa725c72b6b38263de366ce34a80fb384a522a0` / `a5820b68a689c8a07bc4c53ccb3ba927e56f6033`.
9. `sha256sum ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r2.md` — **rc=0**: `4c92ecbf38fb7f5f97ddea64ed4a43f1cbc9e7a826e87fd8c234dc7e25677c2b`.
10. `git rev-parse --is-shallow-repository` — **rc=0**, `false`; `git config --show-origin --get core.abbrev` — **rc=0**, `file:.git/config` / `7`; `git remote get-url origin` — **rc=0**, endpoint thật nêu ở phần neo.
11. `git status --porcelain=v1 --untracked-files=all --ignored=matching`; `git diff --binary`; `git diff --cached --binary` — **từng lệnh rc=0**, stdout/stderr rỗng ở các mốc đã ghi.
12. `git ls-files --others --exclude-standard`; `git ls-files --others --ignored --exclude-standard` — **từng lệnh rc=0**, stdout/stderr rỗng ở cuối lượt.
13. `git rev-parse --verify '9666771^{commit}'`; tương tự với `10446ff`, `f4d15ed` — **từng lệnh rc=0**, full OID như phần tham chiếu. `git ls-files 'docs/adr/0017-*' 'docs/adr/0056-*' 'docs/adr/0057-*' 'docs/adr/0058-*' ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r1.md ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r2.md` — **rc=0**, đủ sáu tệp; [output/argv](evidence/reference-commands.json).
14. `git merge-base --is-ancestor 10446ffa400725b23189ad9c4902932d5eb969bc 76b65936e9e83ad2711e20a158e552449b4c6d86` — **rc=0**. `git show -s '--format=%H %aI %s' 10446ff 76b6593 f4d15ed 9666771` — **rc=0**; quan hệ/thời điểm như phần tham chiếu.
15. `rg -n --glob '*.py' --glob '*.yaml' --glob '*.yml' --glob '*.json' --glob '*.ps1' --glob '*.sh' --glob '!**/golden/**' --glob '!**/fixtures/**' --glob '!**/parser_surface.json' 'KHOA[.]txt|do-luong[.]csv|list_devices|UTC hạn' .claude/dev scripts .github` — **rc=1**, stdout/stderr rỗng: không khớp token trong phạm vi quét; đây là kết quả tìm kiếm âm, không phải gate thất bại. [Bằng chứng](evidence/enforcement-scan.json).
16. GitHub plugin GET `issues/comments/6514073214`, `issues/748`, `pulls/1007`, `pulls/1022`, `pulls/1025` của `ducthangho/tra-luat` — thành công, `isError=false`; **rc không áp dụng** cho connector. Chỉ đọc comment authority và metadata PR/issue; không gọi endpoint reviews hay đọc verdict trước.
