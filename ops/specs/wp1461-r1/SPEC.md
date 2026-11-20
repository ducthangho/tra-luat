# wp1461 r1 — B3 của kế hoạch nguồn r4: cổng phát hành đúng candidate + quy trình audit đỏ (CONG-PHAT-HANH-B3)
packet_id: wp1461
revision: 1
mission_issue: 1172
risk: sensitive
review_class: sensitive
executor: claude
environment: cloud (Linux) + chạy Windows-local trên máy chủ kho (desktop trước, rồi VM)
immutable_acceptance_baseline: `0f9aa2a2cc697129e1f5be72feddf60986286865` (`origin/master`, bằng `base_sha` của Mission r85)

Trạng thái: bản đầu, CHƯA review, CHƯA được chủ kho duyệt băm. Đặc tả Packet #1461, vai **B3** của Mission #1172 theo **kế hoạch nguồn r4 bản sửa 9** (`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md` trên nhánh `ops/wp1172-plan-r4`, sha256 `0f287ce4369fbeb7b1939daa8de5db7c27c2a4efdc1a21f2fccdd37dc9d83fbe`, cài ở Mission r83). Quyết định Q7 của chủ kho ghi ở Mission r84 (`owner_decisions.Q7`); thẩm quyền mở làn và trần ở Mission r85 (`envelope`, `r85_constraints`). Mọi "§" dưới đây là mục của kế hoạch r4; nơi đặc tả này và kế hoạch khác nhau thì **đặc tả này thắng** cho packet này, và mỗi chỗ khác được nêu ở mục "Chỗ lệch có chủ đích". Số dòng trích dẫn đo tại baseline; executor đo lại trước khi sửa.

"Release" = đẩy Package: `scripts/deploy-package.sh --push` và `scripts/deploy-package.ps1 -Push` (kể cả qua `scripts/deploy-package.cmd`). H = commit đang checkout lúc script bắt đầu.

## Mục tiêu
Sau packet này, một lần đẩy Package chỉ xảy ra khi (1) gói được ràng buộc byte với đúng H trên `master`, và (2) có bằng chứng máy đọc được rằng full audit (biên nhận B1 `bien_nhan_audit.v1`) cùng lượt push `ci.yml` đã xanh trên đúng H — hoặc chủ kho tự tay dùng đường khẩn cấp có xác nhận TTY. Không có ngoại lệ nào do máy cấp. Packet land ở chế độ `warning_only`; chế độ chặn bật bằng một thay đổi mã riêng sau khi đủ điều kiện của Q7 (mục 8).

## Hợp đồng

### 1. Bất biến (cưỡng chế bằng ca test, mục Nghiệm thu)
- **I1 — Chỉ siết.** Không chốt hiện có nào của hai script bị nới: gate 8 bước, same-SHA ×2, verify nội dung gói, quét bí mật, chốt chống thụt lùi (rc 3), byte-match sau đẩy giữ nguyên quyết định trên cùng đầu vào. `scripts/deploy-guard.ps1` dự kiến diff = 0; sửa nó phải kèm A/B chứng minh quyết định không đổi.
- **I2 — Build-only không đổi quyết định.** Không `--push`/`-Push`: mã thoát và việc có/không sinh zip giữ nguyên so với baseline; B3 chỉ được IN thêm dòng (H, tree, cảnh báo cây bẩn "gói này KHÔNG được phép đẩy"). Lệch có sẵn giữa hai nền ở build-only (ps1 chặn khi tụt sau `origin/master`, dòng 157–175; sh không kiểm) KHÔNG thuộc packet này.
- **I3 — Không ngoại lệ do máy cấp.** Không cờ, biến môi trường, tệp cấu hình ngoài kho, comment, nhãn hay bản ghi nào làm cổng nới, ngoài đúng hai thứ: tệp chế độ đọc từ đầu `origin/master` (mục 8) và cờ khẩn cấp có xác nhận TTY (mục 7). `--force-older`/`-ForceOlder` vẫn chỉ là ghi đè phiên bản, không miễn bất kỳ phép kiểm nào của B3. `--no-test`/`-NoTest` không miễn phép kiểm nào của B3.
- **I4 — Ba trạng thái.** Mọi phép đọc cho ra `dat` · `khong_dat` · `khong_do_duoc`. `khong_do_duoc` không bao giờ thành `dat`. Ở chế độ chặn, chỉ `dat` được đẩy.
- **I5 — Một nguồn cho logic dùng chung.** Phép đọc REST, kiểm biên nhận, ràng buộc byte và ghi nhật ký nằm ở MỘT tệp Python dùng chung cho cả hai nền (`ops/cong_phat_hanh.py`, tiền lệ `scripts/pkg_secret_scan.py`); hai script chỉ gọi nó và xử lý mã thoát. Không chép logic ấy vào sh/ps1.
- **I6 — Không seam mới đổi quyết định.** Không thêm biến môi trường hay tham số nào đổi địa chỉ API, kho, workflow, chế độ, hay bỏ bước. Test tiêm transport bằng tham số hàm Python, và tiêm ở mức script bằng seam interpreter đã có (`TL_PYTHON`, `-Python`).
- **I7 — Bí mật.** Token không lên argv, không vào nhật ký, không in ra; không gửi `Authorization` tới host chuyển hướng của artifact.

### 2. Điểm chèn (đo tại baseline)
| Bước | `deploy-package.sh` | `deploy-package.ps1` | Việc của B3 |
|---|---|---|---|
| A. Ghi H | sau khối `core.abbrev` (dòng 91–100), trước bước 1 (dòng 109) | sau khối "không tụt sau" (dòng 157–175, tức sau `-Pull`), trước bước 1 (dòng 177) | `ghi-h`: H (40 hex), tree, trạng thái cây; push + cây bẩn ⇒ rc 7 trước khi build |
| B. Ràng buộc byte | sau bước 3 (dòng 258–259), trước nhánh build-only (dòng 262) | sau khối `finally` của bước 3 (dòng 324–326), trước dòng 329 | `rang-buoc`: gói ↔ H; in digest gói |
| C. Cổng audit | sau chốt chống thụt lùi (dòng 280–294), trước `drive-push` (dòng 302) | sau lời gọi `deploy-guard.ps1` (dòng 338–340), trước `drive-push` (dòng 342) | `kiem`: bằng chứng trên H; nếu có cờ khẩn cấp thì hỏi TTY tại đây |
| D. Kiểm lại | ngay trước `drive-push`, sau C, không lệnh nào khác chen giữa | như bên | `kiem-lai`: H, tree, cây sạch, digest zip, H còn trên `master` |
| E. Ghi kết cục | sau bước 5 và ở mọi lối thoát kể từ C | như bên | `ghi-ket-cuc`: một dòng nhật ký cho lần thử |

Thứ tự C → D → `drive-push` là bất biến; có ca và đột biến riêng cho "đổi thứ tự" và "bỏ D".

### 3. Ràng buộc byte gói ↔ H
- **Cây sạch (bước A và D):** `git status --porcelain=v1 -z --untracked-files=all` rỗng (không dùng `-uno`). Tệp bị ignore được phép tồn tại. Lệnh lỗi ⇒ `khong_do_duoc`.
- **H trên `master`:** `git fetch origin +refs/heads/master:refs/remotes/origin/master` phải thành công; kho shallow ⇒ `khong_do_duoc`. Ở A (chỉ push): H phải BẰNG đầu `origin/master` vừa fetch (giữ luật mục 2 §Quy ước deploy của `CLAUDE.md` và đưa sh về ngang ps1). Ở D: fetch lại; `git merge-base --is-ancestor H origin/master` rc 0 ⇒ còn trên master (master đi tới thì IN số commit chênh và đi tiếp), rc 1 ⇒ `khong_dat`, rc khác ⇒ `khong_do_duoc`.
- **Ảnh chụp H:** `git archive H` giải vào thư mục tạm ngoài kho (áp đúng chuyển đổi checkout theo `.gitattributes`, không phụ thuộc cây làm việc). Phương án của §B3 được chọn là "so tập tệp + byte phát hành với blob tại H"; KHÔNG build từ ảnh chụp (build trong cây không có `.git` đổi nhánh hành vi của `tl.py`).
- **Phép so, cả hai phải đạt:** (a) mọi tệp trong zip (bỏ thư mục đỉnh) có mặt trong ảnh chụp H và trùng byte; tệp trong zip mà không có ở H ⇒ `khong_dat` (bắt tệp ignore/chưa theo dõi bị bộ duyệt thư mục của `release-bundle` gom vào); (b) tập đường dẫn trong zip BẰNG tập đường dẫn của `RELEASE_MANIFEST.json` tại H (cộng chính tệp manifest nếu đo thấy nó không tự liệt kê); thừa hoặc thiếu ⇒ `khong_dat`. In ba số: tệp trong zip, tệp đã so, tệp trong manifest; ba số này vào bảng parity.
- **Digest gói:** sha256 của zip (đã có: `S1`). `kiem-lai` tính lại sha256 từ tệp trên đĩa ngay trước `drive-push`; lệch ⇒ rc 7. Bước 5 hiện có (tải về, so `S3 = S1`) giữ nguyên; digest ghi vào nhật ký.
- Lỗi ràng buộc ở chế độ `warning_only` VẪN chặn: ràng buộc byte là tính đúng của gói, không phải bằng chứng audit, nên không có chế độ cảnh báo cho nó.

### 4. Bằng chứng trên H (lệnh `kiem`)
Kho cố định trong mã: `ducthangho/tra-luat`; kiểm thêm `repository.id` trong phản hồi.

**4.1 Lượt push `ci.yml` trên H.** Liệt kê lượt của `.github/workflows/ci.yml` với `head_sha=H`, `event=push`, `head_branch=master`. Lấy lượt mới nhất và attempt mới nhất của nó: `status=completed`, `conclusion=success`; mọi job của attempt ấy có kết luận `success` hoặc `skipped`, số job ≥ 1. Thêm tập tên `CHECK_BAT_BUOC` (hằng trong mã, lấy từ phép đo bảo vệ `master` của chủ kho ở mục 8; tập rỗng chỉ hợp lệ khi hồ sơ đo ghi rõ master không đòi check nào): mỗi tên phải có check run trên H do app `github-actions` tạo, thuộc đúng lượt ấy, kết luận `success` (`skipped` không được nhận cho tên bắt buộc). Không có lượt, lượt `cancelled`/đỏ, check vắng ⇒ `khong_dat`.

**4.2 Biên nhận B1 (bên tiêu dùng).** Phụ thuộc: đặc tả B1 ĐÓNG BĂNG (băm đã duyệt), không cần B1 đã land. Lúc viết bản này đặc tả B1 chưa đóng băng, nên B3 khai các trường LOGIC nó cần; B1 phải cung cấp đủ, và executor B3 điền bảng ánh xạ `ANH_XA_V1` (trường logic → đường dẫn JSON của v1) từ đặc tả B1 đã đóng băng, ghi băm đặc tả B1 vào PR. B1 thiếu một trường hoặc khác ngữ nghĩa ⇒ DỪNG, `blocked`, revision mới; không tự suy.

| # | Trường logic B3 cần | Phép kiểm của B3 |
|---|---|---|
| L1 | tên/phiên bản hợp đồng | bằng đúng `bien_nhan_audit.v1`; phiên bản lạ ⇒ `khong_do_duoc` |
| L2 | kho (tên + id) | bằng kho cố định |
| L3 | đường dẫn workflow | bằng `.github/workflows/ci-dot-bien-du.yml` |
| L4 | sự kiện (+ khung cron nếu `schedule`) | thuộc {`schedule`, `workflow_dispatch`} |
| L5 | SHA sự kiện và SHA/tree checkout TỪNG job | tất cả bằng H và tree của H |
| L6 | run_id, attempt của lượt, attempt của từng bên sản xuất mảnh | khớp REST; dòng attempt hợp lệ theo luật B1 |
| L7 | danh sách job/mục KỲ VỌNG và tập thực có | kỳ vọng ⊆ thực có; mỗi mục kỳ vọng đối chiếu được với job REST |
| L8 | kết luận cuối từng job | mọi mục kỳ vọng `success` |
| L9 | định danh definition: `workflow_sha` + sha256 tệp workflow tại OID ấy, hoặc `not_measured` | xem 4.3 |
| L10 | artifact id + digest của từng artifact thành phần | khớp REST và khớp byte tải về |
| L11 | kết cục theo A+3 | bằng `xanh` |
| L12 | dấu hiệu dương | có mặt, đúng dạng B1 định |
| L13 | tên artifact và tên tệp chứa biên nhận (để tìm) | dùng để định vị; không đoán theo mẫu |

Đối chiếu ĐỘC LẬP với REST (không tin riêng biên nhận): lượt có `path` = L3, `head_sha` = H, `conclusion=success`, `event` ∈ L4; job của đúng attempt đọc qua REST khớp L7/L8; digest artifact do API trả khớp sha256 của byte tải về. Bất kỳ trường bắt buộc nào vắng, lạ kiểu, không đọc được ⇒ không `dat` (`khong_dat` khi phép đọc trọn vẹn và giá trị sai; `khong_do_duoc` khi không đọc trọn). Nhiều lượt audit trên H: chỉ cần MỘT lượt thoả toàn bộ; lượt đỏ khác trên cùng H được IN ra và ghi vào nhật ký, không tự chặn (quy trình audit đỏ ở mục 9 xử lý).

**4.3 Definition đo được.** L9 đo được ⇒ sha256 tệp workflow tại `workflow_sha` phải bằng sha256 của `git show H:.github/workflows/ci-dot-bien-du.yml` tính tại chỗ, và `workflow_sha` phải là H hoặc tổ tiên của `origin/master`. L9 = `not_measured` ⇒ B3 chỉ ĐỌC artifact A4 của `ops-do-workflow-definition.yml` cho đúng run ấy (tên artifact và trường do đặc tả B1 chốt); artifact vắng, cũ hơn lượt, giá trị null hoặc hết giờ ⇒ không `dat`. B3 không dispatch gì.

**4.4 Nhịp tim B2.** Đọc comment của Issue theo dõi B2 (số Issue và dạng dấu thời gian do đặc tả B2 chốt). Cũ hơn 24 giờ, không đọc được, hoặc B2 chưa tồn tại ⇒ CHỈ in cảnh báo và ghi `nhip_tim` vào nhật ký; không bao giờ chặn, không bao giờ tính vào quyết định, ở cả hai chế độ.

### 5. Bảng năng lực endpoint
B3 chỉ gọi GET các endpoint sau; không gọi GraphQL, không POST/PATCH/PUT/DELETE, không đọc bảo vệ nhánh, biến hay secret.

| # | Endpoint (dưới `/repos/{kho}`) | Quyền | Dùng cho | Lỗi ở chế độ chặn |
|---|---|---|---|---|
| E1 | `/actions/workflows/{tệp}/runs?head_sha=…` | Actions: read | 4.1, 4.2 | chặn |
| E2 | `/actions/runs/{id}` và `/actions/runs/{id}/attempts/{n}/jobs` | Actions: read | 4.1, 4.2 | chặn |
| E3 | `/actions/runs/{id}/artifacts` | Actions: read | 4.2, 4.3 | chặn |
| E4 | `/actions/artifacts/{id}/zip` (302 sang host lưu trữ) | Actions: read | 4.2, 4.3 | chặn |
| E5 | `/commits/{H}/check-runs` | Checks: read | 4.1 | chặn |
| E6 | `/commits/{H}` | Contents: read | xác nhận H và tree phía máy chủ | chặn |
| E7 | `/issues/{n}/comments` | Issues: read | 4.4 | chỉ cảnh báo |

- **Luật đọc chung:** nhận 2xx chỉ khi phản hồi mang dấu GitHub thật (`X-GitHub-Request-Id`) và JSON đúng kiểu; 2xx không dấu, 3xx ngoài E4, 401/403/404/5xx, JSON hỏng, hết giờ ⇒ `khong_do_duoc` kèm mã lý do phân biệt "GitHub trả" với "không có dấu GitHub" (bài học proxy). Phân trang có giới hạn (hằng số trang tối đa × 100); còn `rel="next"` sau giới hạn, hoặc số mục gom được khác `total_count` ⇒ `khong_do_duoc`. Mỗi lời gọi có hạn giờ; thử lại có trần cho lỗi mạng/5xx/429; tổng thời gian có trần.
- **Nguồn token:** thứ tự là hằng trong mã, do executor ĐO trên từng máy rồi chốt (ứng viên: `gh auth token`, `GITHUB_PAT`, `GH_TOKEN`, `GITHUB_TOKEN`, không token). Chỉ ghi TÊN nguồn đã dùng. Biến giữ chỗ cho 401 thì thử nguồn kế tiếp; hết nguồn ⇒ `khong_do_duoc`.
- **Lệnh `do-nang-luc`:** gọi từng endpoint E1–E7 một lần trên một run tham chiếu, ghi `do/NANG_LUC_<máy>.json` (mỗi endpoint: mã trạng thái, có dấu GitHub, số trang, `total_count`, host chuyển hướng của E4, nguồn token theo tên, giờ đo, phiên bản OS/Python). Hồ sơ này là điều kiện bật chế độ chặn (mục 8), không phải bằng chứng audit.

### 6. Quyết định, mã thoát, nhật ký G8
| Kết quả `kiem` | Chế độ `warning_only` | Chế độ `chan` |
|---|---|---|
| `dat` | đẩy; lớp `audit_passed` | đẩy; lớp `audit_passed` |
| `khong_dat` | đẩy; lớp `warning_only`; in cảnh báo nổi bật | rc 5, không đẩy |
| `khong_do_duoc` | đẩy; lớp `warning_only`; in cảnh báo nổi bật | rc 6, không đẩy |
| không `dat` + cờ khẩn cấp được xác nhận (mục 7) | đẩy; lớp `owner_emergency` | đẩy; lớp `owner_emergency` |

- Mã thoát mới, GIỐNG NHAU ở hai nền: 5 = cổng audit chặn (đo được, không đạt) · 6 = không đo được ở chế độ chặn · 7 = ràng buộc byte/H/cây vi phạm · 8 = đường khẩn cấp bị từ chối. Mã 0–3 (và 4 của `deploy-guard.ps1`) giữ nghĩa cũ. Cập nhật dòng `rc:` ở đầu ba tệp script/cmd nếu tệp ấy thuộc write set; `deploy-package.cmd` không thuộc write set nên dòng chú thích của nó được ghi là nợ tài liệu.
- **Nhật ký:** `scripts/.tl_state/deploy/nhat-ky-day.jsonl` (đã bị ignore), chỉ nối thêm, mỗi lần thử tới bước C một dòng JSON, `flush` + `fsync`: giờ UTC, máy, nền (`sh`/`ps1`), H, tree, digest gói, VERSION, chế độ và nguồn chế độ, kết quả `kiem` + mã lý do, run_id/attempt của lượt `ci.yml` và lượt audit đã dùng, `nhip_tim`, lớp G8 (`audit_passed` · `owner_emergency` · `warning_only` · `bi_chan`), lý do khẩn cấp (nếu có), kết cục đẩy (`da_day_khop_byte` · `day_hong` · `khong_day`). Dòng lớp/ý định được ghi TRƯỚC `drive-push`; kết cục được ghi bằng dòng thứ hai cùng `id`. G8 đếm theo dòng kết cục `da_day_khop_byte`; `bi_chan` không phải lần đẩy. Nhật ký là tệp cục bộ từng máy: gom hai máy để báo G8 là việc của runbook (mục 9), packet này không công bố nó lên kho.

### 7. Đường khẩn cấp của chủ kho
- **Tên cờ (đóng băng):** sh `--khan-cap-chu-kho` · ps1 `-KhanCapChuKho` (switch). Chỉ có nghĩa cùng `--push`/`-Push`; thiếu ⇒ rc 2.
- **Lớp 1 — trong script, máy cưỡng chế, không chứng minh danh tính.** Có cờ ⇒ ngay ở bước phân tích đối số kiểm stdin VÀ stdout là TTY tương tác (sh: `[ -t 0 ] && [ -t 1 ]`; ps1: `[Console]::IsInputRedirected` và `IsOutputRedirected` đều false, phiên không `-NonInteractive`); không đạt ⇒ rc 8 trước mọi việc khác. Tại bước C, nếu `kiem` không `dat`: kiểm TTY lần nữa, in H + digest gói + kết quả `kiem`, hỏi một dòng lý do (khác rỗng, ≤ 200 ký tự), rồi đòi gõ lại ĐÚNG 40 ký tự hex thường của H (chỉ bỏ ký tự xuống dòng cuối; không cắt khoảng trắng, không nhận tiền tố, không nhận chữ hoa). Sai hoặc EOF ⇒ rc 8, không đẩy, ghi `bi_chan`. Đúng ⇒ ghi `owner_emergency` rồi đi tiếp tới D. `kiem` đã `dat` ⇒ không hỏi, lớp `audit_passed`, ghi chú `khan_cap_khong_can`. Cờ khẩn cấp KHÔNG miễn: mục 3 (ràng buộc byte, cây sạch, H trên master), bước D, chốt chống thụt lùi, quét bí mật, byte-match sau đẩy.
- **Lớp 2 — hook PreToolUse, chỉ HỎI LẠI.** Thêm vào bảng `RISKY` của `.claude/hooks/pretooluse_guard.py` (dòng 13–54) hai luật, cùng trả `permissionDecision=ask`: (a) chuỗi `--khan-cap-chu-kho` ở bất kỳ đâu trong lệnh; (b) trong lệnh có nhắc `deploy-package.ps1` hoặc `deploy-package.cmd` (không phân biệt hoa thường): một token bắt đầu bằng `-` theo sau là TIỀN TỐ KHÁC RỖNG bất kỳ của `KhanCapChuKho`, không phân biệt hoa thường, có hoặc không có `:<giá trị>` (PowerShell nhận viết tắt theo tiền tố: `-K`, `-kh`, `-KHANCAP`, `-KhanCapChuKho:$true`). Executor ĐO trên PowerShell 5.1 và 7 thật rằng mọi tiền tố ấy đều gắn vào tham số (không tiền tố nào trùng tham số khác) và ghi kết quả. B3 không khai gì về cách từng chế độ quyền hay phiên không tương tác xử lý `ask` (CHƯA ĐO, không nghiệm thu nào dựa vào nó). Lớp này KHÔNG phủ: Codex và nền agent khác; lệnh nằm trong tệp script, ghép qua biến hoặc splatting; phiên không nạp hook; terminal của người. Nhánh `deny` của agent chỉ-đọc không đổi.
- **Lớp 3 — cấm theo quy trình, không do máy cưỡng chế.** "Phiên AI không dùng cờ khẩn cấp, kể cả khi được hỏi lại và được đồng ý": ghi ở runbook (mục 9) và một dòng ở §Cấm của `CLAUDE.md`.
- Cờ và luật hook land trong CÙNG PR.

### 8. Chế độ và điều kiện bật chặn
- **Nguồn chế độ:** tệp một dòng `ops/cong_phat_hanh.che_do`, đọc bằng `git show <đầu origin/master vừa fetch>:ops/cong_phat_hanh.che_do` — không đọc từ cây làm việc, không từ biến môi trường. Chỉ đúng chuỗi `warning_only` (cho phép một ký tự xuống dòng cuối) mới cho chế độ cảnh báo; `chan`, rỗng, vắng, lạ, không đọc được ⇒ chế độ `chan`. Vì đọc từ đầu master, checkout một H cũ không hạ được chế độ.
- **Packet này land với `warning_only`.** Đổi sang `chan` là MỘT thay đổi mã riêng (ngoài packet này, cần thẩm quyền riêng), chỉ sau khi đủ: (a) `do/NANG_LUC_<máy>.json` của CẢ HAI máy deploy — container Linux chạy sh và desktop Windows của chủ kho chạy ps1 — mọi endpoint E1–E6 đọc được trọn vẹn; (b) hồ sơ đo bảo vệ `master` bằng quyền quản trị của chủ kho (cấm force-push/xoá, ai vượt được, danh sách check bắt buộc → `CHECK_BAT_BUOC`), lưu `do/BAO_VE_MASTER_<ngày>.json`, đo lại hằng tháng theo runbook; (c) B1 đã land và có ít nhất một biên nhận thật `dat` qua `kiem` trên cả hai máy. B3 KHÔNG đọc bảo vệ nhánh lúc deploy; trôi cấu hình giữa hai lần đo là rủi ro tồn dư chủ kho đã nhận ở Q7(b).
- **Rủi ro tồn dư khai thẳng:** script chạy từ cây của H, nên một H có trước B3 không có cổng nào (chỉ còn chốt chống thụt lùi và quy trình); người ngồi máy sửa được script; TTY không chứng minh ai gõ; `TL_PYTHON`/`-Python` là seam có sẵn. Mục tiêu là chặn tay trượt và phiên tự động, không chặn kẻ gian có quyền ghi máy.

### 9. Tài liệu quy trình (dev-side, không vào gói)
`docs/QUY_TRINH_PHAT_HANH_B3.md` (tệp mới) gồm: quy trình audit đỏ đúng §B3 (owner = chủ kho; xác nhận ≤ 2 giờ làm việc; ≤ 1 ngày làm việc có Issue nêu H, ID đỏ, phân loại code/test/hạ tầng, tái hiện tối thiểu hoặc lý do chưa tái hiện; tối đa 1 lần chạy lại hạ tầng, giữ attempt đỏ; bisect chỉ trên commit dựng được, không dựng được ghi `not_testable`; khi công tắc A+1 đã tồn tại thì đóng nó theo runbook công tắc và không merge thay đổi cùng vùng; release bị chặn tới khi có audit xanh đúng candidate hoặc chủ kho dùng đường khẩn cấp); ba lớp quanh cờ khẩn cấp, mỗi lớp nói đúng mức của nó; danh sách kiểm bật chế độ chặn (mục 8); runbook đo bảo vệ `master` hằng tháng; cách gom nhật ký hai máy để báo G8 ba dòng TÁCH. `CLAUDE.md`: thêm tối đa 15 dòng ở §Quy ước deploy (con trỏ tới tài liệu trên, tên cờ, mã thoát 5–8) và §Cấm (lớp 3); không sửa chỗ khác.

### Chỗ lệch có chủ đích so với kế hoạch r4
1. §B3 viết lớp 1 "trong chính script": giữ đúng (TTY và gõ lại H nằm trong sh/ps1); phần còn lại gom vào helper dùng chung (I5) để hai nền không trôi.
2. Lỗi ràng buộc byte chặn cả ở `warning_only` (mục 3) — chặt hơn kế hoạch.
3. Chế độ đọc từ đầu `origin/master`, mặc định đóng (mục 8) — kế hoạch chỉ nói "chưa đo ⇒ `warning_only`, ghi rõ".
4. Write set rộng hơn danh sách của Mission r85 (xem Write set, có lý do từng tệp) — cần chủ kho duyệt cùng băm này.

## Nghiệm thu
1. **Hai chiều + ba trạng thái cho từng phép kiểm.** Mỗi phép kiểm của mục 3, 4, 5 có ít nhất: một ca `dat`, một ca `khong_dat`, một ca `khong_do_duoc`, và ca "đạt" không được đạt vì lý do khác (đòi mã lý do đúng, không chỉ mã thoát).
2. **Cây và H:** tệp theo dõi bị sửa; tệp theo dõi bị xoá; tệp chưa theo dõi ngoài tập phát hành; tệp chưa theo dõi nằm trong thư mục phát hành; tệp bị ignore nằm trong thư mục phát hành và bị gom vào zip (⇒ chặn ở phép so (a)); tệp ignore trong `scripts/.tl_state/` (⇒ không chặn, không vào gói); HEAD đổi giữa A và D; tệp theo dõi bị sửa giữa build và D; zip bị thay giữa B và D (digest lệch); zip thừa/thiếu một tệp so với manifest tại H; H không phải đầu master ở A; master bị ép lùi khiến H hết là tổ tiên ở D; master đi tới bình thường giữa A và D (⇒ đi tiếp, có in); kho shallow; fetch lỗi.
3. **Biên nhận:** không có lượt audit trên H; có lượt nhưng không có artifact biên nhận; biên nhận sai SHA (một job checkout khác H); sai tree; sai kho; sai workflow; lượt đỏ; kết cục khác `xanh`; thiếu một job kỳ vọng; một job kỳ vọng `skipped`/`cancelled`; thiếu từng trường L1–L13 (mỗi trường một ca); trường sai kiểu; phiên bản hợp đồng lạ; digest artifact lệch; attempt không khớp REST; definition lệch byte với H; `not_measured` + A4 hợp lệ (⇒ `dat`); `not_measured` + A4 vắng / cũ / null / hết giờ; hai lượt trên H một đỏ một xanh (⇒ `dat`, có in lượt đỏ); biên nhận nói xanh nhưng REST nói job đỏ (⇒ không `dat`).
4. **CI bắt buộc:** không có lượt push trên H; lượt `cancelled`; lượt xanh nhưng một tên trong `CHECK_BAT_BUOC` vắng; tên bắt buộc `skipped`; check cùng tên do app khác tạo; lượt `pull_request` xanh trên cùng H không được tính thay lượt push; audit xanh nhưng CI đỏ (⇒ chặn).
5. **API:** 403 có dấu GitHub; 403 không dấu; 404; 401 rồi nguồn token kế tiếp đạt; 5xx hết lượt thử; hết giờ; JSON hỏng; 200 không dấu GitHub; phân trang 2 trang đủ; phân trang vượt giới hạn; `total_count` lệch số gom được; E4 chuyển hướng (không gửi `Authorization` sang host mới); E4 chuyển hướng tới host không tới được; E7 lỗi (⇒ chỉ cảnh báo, quyết định không đổi).
6. **Chế độ:** bảng mục 6 đủ mọi ô; tệp chế độ = `warning_only` / `chan` / rỗng / vắng / `Warning_Only` / có khoảng trắng thừa / `git show` lỗi; tệp chế độ trong cây làm việc khác bản trên master (⇒ dùng bản master); biến môi trường lạ (liệt kê trong ca: `GITHUB_API_URL`, `GH_HOST`, `GH_REPO`, và mọi tên `TL_B3_*` thử được) KHÔNG đổi quyết định; `--force-older`/`-ForceOlder` và `--no-test`/`-NoTest` KHÔNG đổi quyết định của B3.
7. **Khẩn cấp:** cờ + không TTY ⇒ rc 8, không build; cờ không kèm push ⇒ rc 2; TTY + H sai (thiếu một ký tự, chữ hoa, 7 ký tự đầu, có khoảng trắng) ⇒ rc 8, không đẩy; TTY + lý do rỗng ⇒ rc 8; TTY + H đúng ⇒ đẩy (đồ giả), nhật ký `owner_emergency` có lý do và digest; `kiem` đã `dat` ⇒ không hỏi; cờ + cây bẩn ⇒ vẫn rc 7; cờ + thụt lùi ⇒ vẫn rc 3. Linux: dựng pty bằng module `pty`. Windows: chạy trên console thật theo kịch bản tay trong runbook, kết quả ghi vào hồ sơ parity.
8. **Hook:** hai cách viết cờ và các tiền tố PowerShell (`-K`, `-kh`, `-KHANCAP`, tên đủ, dạng `:$true`, qua `.cmd`, qua `pwsh -File`) ⇒ `ask`; lệnh deploy thường (`--push`, `-Push`, `--force-older`, `-ForceOlder`, `-Pull -Push`, `--no-test`, `--out`, `-Out`, `-Python`, `-Repo`) ⇒ quyết định BẰNG quyết định của blob hook tại baseline `0f9aa2a…` (so bằng cơ chế blob-base như ca `t4`); lệnh không liên quan có `-k` (`sort -k2`, `curl -k`, `ssh -K`) không nhắc deploy-package ⇒ quyết định không đổi; agent chỉ-đọc vẫn `deny` như trước. Ca mới phải có mặt trong `CA` (ca `t36` canh).
9. **Đột biến riêng cho từng chốt,** chạy trên BẢN SAO trong thư mục tạm (tên tệp riêng từng đột biến, `-B`), phân hạng bằng LỚP NGOẠI LỆ RIÊNG của ca đích neo cả TÊN CA (kiểu `TinHieuChotCa`), kèm ca tự kiểm bộ phân hạng (đột biến chết vì `AttributeError`/assertion của ca khác phải rơi vào TÍN DỤNG GIẢ, kể cả khi trên đường có `except` đổi kiểu). Tối thiểu, mỗi dòng một đột biến có ca đích riêng: bỏ kiểm cây sạch · dùng `-uno` · bỏ phép so (a) · bỏ phép so (b) · so với cây làm việc thay vì ảnh chụp H · bỏ bước D · đổi thứ tự D trước C · bỏ so digest ở D · bỏ kiểm tổ tiên ở D · coi rc khác 0/1 của `merge-base` là "không phải tổ tiên" · bỏ so `head_sha = H` · bỏ so SHA checkout từng job · nhận `skipped` cho job kỳ vọng · bỏ đối chiếu REST (tin riêng biên nhận) · bỏ kiểm digest artifact · nhận `not_measured` không cần A4 · nhận lượt `pull_request` thay push · bỏ `CHECK_BAT_BUOC` · bỏ kiểm app nguồn của check · `khong_do_duoc` thành `dat` · `khong_do_duoc` thành `khong_dat` · phân trang cụt được coi là đủ · bỏ so `total_count` · 2xx không dấu GitHub được nhận · gửi `Authorization` sang host chuyển hướng · nhịp tim lỗi làm chặn · chế độ lạ thành `warning_only` · đọc chế độ từ cây làm việc · đọc chế độ từ biến môi trường · bỏ kiểm TTY stdin · bỏ kiểm TTY stdout · nhận tiền tố của H · nhận H chữ hoa · khẩn cấp miễn ràng buộc byte · `--force-older` miễn cổng audit · ghi `audit_passed` cho lần `warning_only` · không ghi nhật ký trước khi đẩy · gỡ luật hook (a) · gỡ luật hook (b) · luật hook (b) chỉ khớp tên đủ · luật hook (b) không đòi nhắc deploy-package. Đột biến ở tệp sh/ps1 là đột biến văn bản trên bản sao script trong kho tạm.
10. **Đồ giả giữ TRẠNG THÁI:** `gws` giả và interpreter bọc ghi nhật ký từng lời gọi; mỗi ca chặn phải đòi ĐÚNG 0 lời gọi `drive-push` trong nhật ký, mỗi ca đẩy đòi đúng 1, đúng tệp zip, đúng thứ tự sau `kiem-lai`. Ít nhất hai ca đầu-cuối dùng `release-bundle` THẬT (một đạt, một lệch byte); các ca còn lại được dùng bundle giả tất định.
11. **Parity hai nền trên CÙNG đầu vào.** Một bộ kịch bản đóng băng `do/KICH_BAN.json` (mọi ca mức script của mục 2, 3, 6, 7) chạy bằng sh trên Linux (container) và bằng ps1 trên **Windows thật: desktop của chủ kho trước, rồi VM** (máy Asus offline, không tính). Mỗi lượt xuất `do/PARITY_<máy>_<nền>.json`: với từng kịch bản — mã thoát, lớp G8, mã lý do, số và thứ tự lời gọi phá trong nhật ký đồ giả; cộng các SỐ ĐẾM: số kịch bản chạy / bỏ qua, số tệp trong zip, số tệp đã so với H, số tệp trong manifest. Hai bảng phải BẰNG nhau từng ô và từng số đếm; kịch bản bỏ qua phải bằng 0 hoặc trùng tên ở cả hai bên kèm lý do. Chạy cho cả base lẫn candidate ở các kịch bản không dùng tính năng mới (chứng minh I1/I2), hai vế dựng trong MỘT lệnh. Chạy ps1 trên cả Windows PowerShell 5.1 và PowerShell 7 nếu desktop có cả hai. `pwsh` trên Linux chỉ là bằng chứng PHỤ, ghi riêng, không thay Windows thật. Tránh ba bẫy PowerShell của `CLAUDE.md` (`$Args`, `Get-Content -Raw` trên tệp rỗng/BOM, thiếu `-Force`) và có ca cho tệp nhật ký/chế độ rỗng và chỉ-BOM.
12. **Đo năng lực:** `do/NANG_LUC_<máy>.json` cho container Linux và desktop Windows (VM nếu chủ kho định dùng nó để deploy). Thiếu hồ sơ của một máy KHÔNG chặn merge packet (packet land ở `warning_only`), nhưng PR phải ghi rõ máy nào `chua_do`.
13. **Cổng kho:** `python ops/cong_phat_hanh_test.py` và `python .claude/hooks/pretooluse_guard_test.py` (chế độ đủ) N/N với hai số bằng nhau và dòng dấu hiệu dương; `python .claude/dev/ci_dang_ky_test.py` đạt; `python .claude/dev/packet_loop.py doctrine-scan --root .` và `adr-song --root .` rc 0; `python scripts/tl.py --selftest` N/N (các ca đang đọc văn bản ba script deploy — `r251_*`, các ca r244/r330 — phải còn xanh); Ruff `--select F` DELTA = 0 so baseline trên mọi tệp `.py` đổi hoặc thêm; `actionlint` không áp (không đổi workflow).
14. **Gói phát hành không đổi:** `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` cho `ok=true`, `expected == checked`, và `file_count` của `release-bundle` BẰNG baseline (A/B một lệnh). Write set dự kiến không chứa tệp nào trong manifest (`ops/`, `docs/`, `.claude/`, `CLAUDE.md` và bốn script deploy đều bị loại khỏi gói); nếu đo thấy một tệp trong manifest phải đổi ⇒ DỪNG (ngoài write set: tái sinh `RELEASE_MANIFEST.json`, golden và bump VERSION cần revision mới).
15. **CI:** CI PR Ubuntu xanh trên H; PR báo delta thời gian theo job/bước của bộ test mới và ghi nhận `pretooluse_guard_test` chạy chế độ đủ (§13: trung vị 1009 s thay vì 26 s mỗi lượt). K7 (một lượt `ci-dot-bien-du.yml` `success` trên đúng H) nếu effective write set chạm vùng M9 theo dispatcher.

## Write set
Theo Mission r85:
- `scripts/deploy-package.sh`
- `scripts/deploy-package.ps1`
- `scripts/deploy-guard.ps1` (dự kiến diff = 0, xem I1)
- `.claude/hooks/pretooluse_guard.py`
- `.claude/hooks/pretooluse_guard_test.py`
- `ops/specs/wp1461-r1/` (SPEC, lease, `do/`: kịch bản, hồ sơ parity, hồ sơ năng lực, hồ sơ bảo vệ master; nhánh `ops/wp1461-r1`)

Thêm, có lý do (cần chủ kho duyệt cùng băm):
- `ops/cong_phat_hanh.py` (MỚI) — I5: một nguồn logic cho hai nền; `ops/` không vào gói nên không đụng manifest và trần 200 tệp.
- `ops/cong_phat_hanh_test.py` (MỚI) — bộ test dev-side; các ca deploy hành vi không hợp với `scripts/tl_selftest.py` (tệp trong manifest ⇒ kéo theo manifest + VERSION + CHANGELOG, và selftest chạy cả trong gói cài không có script deploy).
- `ops/cong_phat_hanh.che_do` (MỚI) — mục 8.
- `.claude/dev/ci_dang_ky_test.py` — CHỈ thêm mục đăng ký cho bộ test mới (bộ quét `rglob("*_test.py")` đòi mọi test trong `ops/` phải có trong sổ). Tệp này đang bị lease `wp1236-a-r9-g1-claude-20261120` giữ tới 2026-11-22T15:35Z và B1/B2/PR2 cùng dùng: lease B3 chỉ cấp sau khi lease ấy hết và phải xếp NỐI TIẾP với B1 trên tệp này (`ai-dang-giu` trên mọi ref trước khi cấp).
- `docs/QUY_TRINH_PHAT_HANH_B3.md` (MỚI) — mục 9.
- `CLAUDE.md` — tối đa 15 dòng ở hai chỗ nêu tại mục 9; lớp 3 chỉ có tác dụng khi nằm ở nơi phiên AI đọc đầu tiên.

Không thuộc write set: `scripts/deploy-package.cmd`, `scripts/tl.py`, `scripts/tl_core/**`, `scripts/tl_selftest.py`, `RELEASE_MANIFEST.json`, `VERSION`, `.github/**`, `.claude/settings.json`, `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`.

## Quy trình và quyền
- **Điều kiện cấp lease:** (1) chủ kho duyệt băm đặc tả này; (2) đặc tả B1 đã đóng băng và có băm được duyệt, đủ L1–L13; (3) lease `wp1236-…` trên `.claude/dev/ci_dang_ky_test.py` đã hết và không lease sống nào chồng write set (`ai-dang-giu` trên mọi ref, so tập ref cục bộ với `ls-remote`); (4) Mission revision riêng cho packet (r85: "Own frozen spec approved by the owner (hash) and its own Mission revision before any lease").
- **Vai:** Executor Claude Code (Fable 5.2). Reviewer Codex service gpt-6-astra, mức xhigh, phiên độc lập, chỉ đọc; reviewer CHẠY ca và đột biến có sẵn trong cây, hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời cho điều phối.
- **Trần (r85 `per_new_packet`):** executor attempts 3 · review mã Codex 3 · CI PR Ubuntu 3 · `ci-dot-bien-du.yml` (K7) 1 nếu chạm vùng M9 · connector 2 · CI rerun 1 · Windows CI 0. Review đặc tả: tác giả 3, Codex 4. Đếm số lời gọi Codex đã dùng TRƯỚC mỗi lời gọi.
- **Windows:** không dispatch Windows CI. Chạy Windows-local trên desktop của chủ kho trước, rồi VM; chủ kho chạy và gửi lại các tệp `do/PARITY_*`, `do/NANG_LUC_*`. Chưa có hồ sơ Windows thật ⇒ nghiệm thu 11 CHƯA đạt; chỉ chủ kho miễn được, bằng văn bản nêu rủi ro tồn dư.
- **Trong lúc thi công và test:** KHÔNG đẩy Package thật, KHÔNG gọi `drive-push` thật, KHÔNG dùng cờ khẩn cấp ngoài đồ giả, KHÔNG dispatch workflow, KHÔNG đổi biến/secret/bảo vệ nhánh, KHÔNG LIVE.
- Chủ kho tự audit exact-H trước lần đẩy đầu của H; merge do chủ kho bấm. Trước khi đẩy H: cập nhật nhánh lên master mới nhất và đo lại làn.
- **Ngoài phạm vi:** bật chế độ `chan`; B1 (bên sản xuất biên nhận, canary A3/A4); B2 (watchdog, Issue theo dõi); B4 và công tắc A+1; đổi `ci.yml` hay bất kỳ workflow nào; sửa `release-bundle`/manifest/VERSION; công bố nhật ký G8 lên kho; sửa lệch build-only có sẵn giữa sh và ps1; đo cách các chế độ quyền xử lý `ask`; làn A, làn C.
