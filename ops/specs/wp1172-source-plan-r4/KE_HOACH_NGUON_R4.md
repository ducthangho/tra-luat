# KẾ HOẠCH NGUỒN r4 — hợp nhất r2 gốc, r3, nháp PR0 và phản biện Proxima (Mission #1172) — bản sửa 1

## 1. Trạng thái và nguồn

- **Trạng thái: `proposed`.** Chưa duyệt, chưa cài. Băm do phiên điều phối ghi khi đóng băng; chỉ có hiệu lực khi chủ
  kho duyệt băm và một Mission revision cài nó. Cho tới lúc ấy **r3 vẫn là kế hoạch hiện hành** (Mission r81/r82).
- **r4 không xoá r3 và không hồi sinh r2.** r4 = r3 (giữ nguyên tám packet, bất biến, số nền, mục tiêu G1–G6) **cộng**
  một làn bảo đảm mới (làn B) lấy từ r2/nháp/Proxima, **cộng** một làn chính sách có điều kiện (làn C) chỉ mở khi chủ
  kho quyết. Mọi câu của r3 không được nhắc ở đây là giữ nguyên.
- **Nguồn (lưu nguyên byte tại `ops/specs/wp1172-source-plan-r4/nguon/`):**

| Nguồn | sha256 | Vai trò |
|---|---|---|
| r2 gốc `KE_HOACH_TOI_UU_MUTATION_TESTING_r2_2026-11-03.md` (31 028 byte) | `f4611b0f0c79f33d56b293f5fcb854eeeae2fcbb6acbdfd59d6134dcbfbdcb8f` | Khớp `source_plan_status.r2_sha256` của Mission; chủ kho tìm lại và nộp ngày 2026-11-20 |
| Nháp PR0 `PACKET_DRAFT_CI_FULL_AUDIT_PIN_SHA_2026-11-03.md` | `621026692cda1be04d8f1df1a47828d19d01c087dcb484f7c3b2fbf58a900e8e` | Tiêu chí A1–A6 của PR0 |
| Phản biện Proxima `proxima-mutation-policy-review-20261103.txt` | `122fadcab2dbf34303edafc3cd6e93ae08aeba7f3593ce715eeba7ef1d05cec8` | Tư vấn chính sách tổng quát, KHÔNG phải audit kho |
| r3 `ops/specs/wp1172-source-plan-r3/KE_HOACH_NGUON_R3.md` (nhánh `ops/wp1172-plan-r3`@`c032656`) | `2e9fb13f1ab3f299c2d2dc1e5a6e407ff0aadb8aee1f6ffd00d88fc02b146f89` | Xương sống; cài ở r81 |
| BASELINE #1434 `ops/specs/wp1434-r3/do/BASELINE.json` @ `5e5d2cc` | `6100c8e18907f59b1abbdc44195861cc2310c654ce8dcfa2e74ca4ffa155f54c` | Nền số |

## 2. Kế thừa — việc đã làm và nơi nó được dùng tiếp (không bỏ công nào)

| Việc đã xong / đang chạy | Trạng thái đo được | Dùng tiếp ở r4 |
|---|---|---|
| PR0 #1166 (ghim SHA, group theo `run_id`, `cancel-in-progress: false`, chọn biên nhận mảnh) | accepted rev12 H3 `b79cbf5`; merged `f8b9cdd` (PR #1412); M8 `landed: false` | Là nền của làn B. Đóng r2-PR0 mục 1–4 và nháp A1, A2, A5, A6 ở mức mã. **A3** (canary hai dispatch cùng SHA + một push) và **A4** (đọc định danh workflow definition) CHƯA có hồ sơ đo ⇒ chuyển vào B1 |
| `ops-do-workflow-definition.yml` (#1094, CI-PROVENANCE-WD) | trên master | B1 dùng nó cho A4 thay vì dựng đường mới |
| Đo nền #1434 | merged `5e5d2cc`; ảnh chụp thô thu lại 2026-11-20 tại cùng T0/T1 | Nền số của r3 và mục tiêu G1–G6; ảnh chụp dùng cho nghiệm thu PR1 mục 5 |
| r3 (4 vòng review Codex, cài r81) | installed | Làn A giữ nguyên |
| PR1 #1448 (spec r2 `5014de59…`, lease `wp1448-r2-g1-claude`) | đang thực thi lượt 1/3 | **Không đổi spec, không đổi lease.** Làn A tiếp tục; dữ liệu bóng 14 ngày của nó là đầu vào cho PR3/PR4 |
| Canary #1308, #1370, #1393, #1422 | accepted/merged | Sửa vòng đời, admission, biên nhận công bố. KHÔNG tính là tiết kiệm thời gian; chỉ là hạ tầng để chạy packet |
| #1143/PR #1155 (đường nhanh hồ sơ), wp892, wp1343/wp1353 (packet-loop 16 mảnh + hằng đêm), WP748 (`nhanh_don_duoc` đích/đủ) | landed | Tiền lệ và cơ chế mà r3 PR3/PR6 mở rộng; không làm lại |

## 3. Phản biện ba nguồn

**r2 đúng ở đâu, sai ở đâu.** Đúng: bằng chứng full audit phải ghim SHA và không bị thay chỗ; phân loại kết cục phải tách
`cancelled`/`timed_out`/`infrastructure_error`/`not_run` khỏi `passed`; harness phải được tự kiểm bằng lỗi cài cố ý;
cần watchdog ĐỘC LẬP cho lịch vắng; release phải kiểm đúng candidate; rollback phải tức thời, không chờ PR. Sai (đo ra
sau): r2 coi chi phí lớn là full audit và nhắm cắt M9. BASELINE cho thấy full audit chỉ 700 504 s = 4,7 % `[r3 DX-5]`,
còn bước G5 trên từng lượt `ci.yml` là 52,8 % `[B: M2.theo_buoc…G5]`. Cắt M9 đánh vào khoản nhỏ và đánh đổi bảo đảm lớn.
Mục tiêu "preflight p50 ≤ 2 phút" của r2 không có phép đo nền; trung vị đầu-cuối lượt PR `day_du` hiện là 1775 s `[r3
DX-4]`, chủ yếu do G5, nên 120 s là mục tiêu cho MỘT làn mới chưa tồn tại, không phải cho CI hiện hành.

**r3 đúng ở đâu, thiếu ở đâu.** Đúng: dựng trên số đo; nhắm đúng khoản lớn (G5 theo diff, registry); giữ M9 (I1); fail-closed
ba trạng thái; bóng ≥ 14 ngày trước khi bật. Thiếu (vì soạn khi r2 bị coi là mất): (a) không có watchdog/freshness cho
full audit, trong khi I1 dựa vào chính lượt audit ấy làm lớp bù; (b) không có cổng release đúng candidate; (c) không có
quy trình audit đỏ (owner, SLA); (d) hoàn tác của PR3/PR6 là "công tắc một dòng" trong MÃ, tức cần một PR — đúng cái r2
§5.5 cảnh báo; (e) điều kiện bật PR3 không có lỗi cài cố ý (seeded fault) để chứng minh bao đóng bắt được lỗi thật; (f) kết
cục mutant chỉ phân giết/sống/tín dụng giả, không có `timed_out`/`infrastructure_error` tường minh; (g) không đo RSS.

**Proxima.** Tổng quát, không đọc kho, nên chỉ dùng làm danh mục kiểm. Bốn điểm có giá trị và chưa nằm trong r3: (1)
"audit bị huỷ hoặc chưa hoàn tất tuyệt đối không được tính là xanh" kèm cảnh báo quá hạn; (2) kiểm thử chính hệ thống kiểm
thử bằng lỗi cài cố ý; (3) release gate; (4) đo cả lỗi bị BỎ SÓT bằng holdout/seeded, không chỉ điểm mutant. Proxima cũng
nói "audit tuần không thay được kiểm chứng tại thời điểm merge" — điều này ỦNG HỘ r3 (giữ M9), không ủng hộ phần cắt M9 của r2.

**Xung đột và cách giải.** Một xung đột thật: r2 PR8 (M9 theo rủi ro) ↔ r3 §6 phương án loại 3. r4 giải: **giữ I1 của r3
mặc định**; phần cắt M9 của r2 thành làn C, chỉ mở khi có số đo của làn A (PR8) và quyết định văn bản của chủ kho (Q8).
Không có xung đột nào khác: các yêu cầu bảo đảm của r2 chỉ THÊM, không làm yếu bất biến nào của r3.

## 4. Thiết kế hợp nhất: ba làn

### Làn A — giảm chi phí (r3, giữ nguyên, ghép bốn bổ sung)

PR1 → PR2 → PR3 → PR4 → PR5 → PR6 → PR7 → PR8 đúng như r3 §5, bất biến I1–I6 và năm phép chứng minh của r3 §4. Bốn bổ
sung chỉ SIẾT, áp vào đặc tả của packet khi tới lượt (không áp hồi tố cho PR1 đang chạy):

- **A+1 (PR3, PR6) — công tắc bảo thủ ngoài cây PR.** Ngoài hoàn tác bằng revert, `chuan-bi` đọc một biến kho (Actions
  repository variable, ví dụ `MISSION1172_CONG_TAC`) do chủ kho giữ. Chỉ đúng chuỗi cho phép mới mở bỏ/giảm G5; vắng,
  rỗng, lạ, đọc lỗi ⇒ chạy đủ (I3). Lật công tắc có hiệu lực ở lượt kế tiếp, không cần PR. Nghiệm thu: ca hai chiều + đột
  biến "công tắc vắng ⇒ bỏ" phải đỏ; một lượt CI thật với công tắc tắt in dấu hiệu dương "chạy đủ vì công tắc".
- **A+2 (điều kiện bật PR3 thứ sáu) — lỗi cài cố ý.** Trước commit bật: một tập lỗi cài cố ý KHÓA TRƯỚC (oracle độc lập,
  không do bộ phân loại sinh), mỗi lỗi nằm ở một thành phần của bao đóng (`ops/` thường, `.claude/dev/`, `scripts/*.py`,
  `.github/`, cấu hình gốc, tệp đọc qua object git) ⇒ bóng phải ra `chay` cho 100 %; cộng ít nhất 5 PR lịch sử ĐÃ có G5 đỏ
  vì lý do không phải hạ tầng (nếu tìm được trong cohort) ⇒ bóng `chay`. Thiếu PR lịch sử thì ghi số tìm được, không bịa.
- **A+3 (PR2, PR5) — kết cục tường minh.** Bản ghi mảnh/biên nhận mang `ket_cuc` ∈ {`giet`, `song`, `tin_dung_gia`,
  `timed_out`, `infrastructure_error`, `cancelled`, `not_run`}; chỉ `giet` được cộng vào số bị giết; mọi giá trị khác hoặc
  vắng ⇒ không xanh. Không đổi phân hạng hiện có (I2), chỉ thêm trường và phép kiểm.
- **A+4 (PR7b) — RSS.** Khi cân mảnh, đo thêm RSS đỉnh mỗi tiến trình con (`resource.getrusage(RUSAGE_CHILDREN)` trên
  Linux; `khong_do_duoc` nơi khác), dùng làm ràng buộc song song.

### Làn B — bảo đảm bằng chứng (mới, từ r2 PR0/PR5/PR6, nháp A3/A4, Proxima)

Làn B không đổi quyết định cổng nào của `ci.yml` và không nới M9. Nó làm cho lớp bù mà I1/I5 dựa vào trở nên KIỂM ĐƯỢC.

- **B1 — Biên nhận full audit + đóng A3/A4 của PR0.** Job cuối của `ci-dot-bien-du.yml` ghi một biên nhận JSON (artifact):
  sự kiện, khung cron (nếu `schedule`), SHA sự kiện, SHA/tree checkout của mọi job, `github.workflow_sha` nếu có (vắng ⇒
  `not_measured`, không suy từ checkout), run_id/attempt, kết luận từng job, kết cục theo A+3, giây và RSS từng mảnh.
  Đo A3 bằng canary: hai `workflow_dispatch` khác run_id trên CÙNG SHA + một push master trong lúc lượt đầu chạy ⇒ ba
  biên nhận kết thúc, không lượt nào `cancelled` vì concurrency. Đo A4 bằng `ops-do-workflow-definition.yml` trên một
  lượt. Write set: `.github/workflows/ci-dot-bien-du.yml`, `.claude/dev/ci_dang_ky_test.py`, thư mục đặc tả mới.
  Phải land TRƯỚC PR5 (cùng write set; PR5 mở rộng đúng biên nhận này).
- **B2 — Watchdog freshness độc lập.** Workflow MỚI chạy theo lịch riêng (không phải bước trong full audit) + `workflow_dispatch`,
  quyền chỉ đọc Actions và ghi Issue. Đọc REST các lượt `ci-dot-bien-du.yml`, phân ba trạng thái theo r2 §4: `fresh` (lượt
  cron gần nhất `success` đủ biên nhận B1, tuổi snapshot ≤ 8 ngày, không khung nào quá 36 giờ chưa đóng) · `due_in_progress`
  · `stale_or_missing` (khung vắng, quá 36 giờ chưa `success`, > 8 ngày, hoặc kết cục `failure`/`cancelled`/`timed_out`
  /`infrastructure_error` chưa được thay bằng biên nhận hợp lệ). Tuổi tính từ khung/snapshot gốc; chạy lại cùng SHA cũ
  KHÔNG làm mới. `stale_or_missing` ⇒ mở hoặc cập nhật MỘT Issue theo dõi, gắn nhãn, nêu SHA, run, kết cục. Ba trạng thái
  ĐO: lỗi đọc API ⇒ `khong_do_duoc`, cũng mở Issue, không im lặng. Ban đầu CHỈ BÁO CÁO, không chặn merge. Write set: tệp
  workflow mới, một script `ops/` mới + test (tệp mới, không giao write set làn A). Có thể chạy song song thời gian với
  14 ngày bóng của PR1.
- **B3 — Cổng release đúng candidate + quy trình audit đỏ.** "Release" của dự án là đẩy Package (`scripts/deploy-package.sh`
  `--push`, `scripts/deploy-package.ps1 -Push`). Thêm bước trước `drive-push`: đòi một biên nhận B1 `success` cho đúng
  HEAD đang đóng gói (khớp 40 ký tự), đọc qua REST; vắng, sai SHA, đỏ, không đọc được ⇒ dừng với mã riêng. Ghi đè chỉ bằng
  cờ tường minh kèm lý do (giống `--force-older`), in ra log. Parity hai nền theo bài học r244 (chạy thật cả `sh` và `ps1`,
  so cùng đầu vào). Quy trình audit đỏ (tài liệu `ops/` hoặc `docs/`): owner = chủ kho; nhận trong 1 ngày; Issue nêu SHA,
  ID đỏ, phân loại code/test/hạ tầng; tối đa 1 lần chạy lại hạ tầng, giữ cả attempt đỏ; bisect chỉ trên commit dựng được,
  không dựng được ghi `not_testable`. Phụ thuộc B1. Write set: hai script deploy + test của chúng, tài liệu quy trình.

### Làn C — chính sách M9 (từ r2 PR7/PR8), CÓ ĐIỀU KIỆN, mặc định ĐÓNG

Chỉ mở khi: làn A PR8 đã đo xong 30 ngày, B1–B3 đã land, và chủ kho quyết Q8 bằng văn bản. Khi mở: C1 shadow cặp đủ/đích
trên CÙNG snapshot với lỗi lịch sử, lỗi cài cố ý và holdout khoá trước; báo bỏ sót tương đối theo cụm PR/nguyên nhân gốc
(r2 §5.3), không công bố khoảng tin cậy khi giả định lấy mẫu không đạt. C2 sửa ADR-0060/K7 theo rủi ro, kèm công tắc bảo
thủ A+1 và rollback không cần PR. Mục tiêu preflight p50 ≤ 2 phút / p95 ≤ 5 phút của r2 thuộc làn C và chỉ là mục tiêu
cho một làn mới; trước đó nó là chỉ số CHỈ BÁO CÁO (G9).

## 5. Thứ tự và phụ thuộc (một executor tại một thời điểm, theo envelope)

1. **PR1** (đang chạy) → land.
2. **B2** (write set độc lập; lấp khoảng chờ 14 ngày bóng).
3. **PR2** (Q3 quyết trước).
4. **B1** (sau PR0; trước PR5).
5. **PR3** (sau ≥ 14 ngày bóng của PR1, Q1, A+1, A+2).
6. **B3** (sau B1).
7. **PR4** → **PR5** (sau B1) → **PR6** → **PR7** → **PR8**.
8. **Làn C** chỉ khi Q8 = mở.

Lý do đặt B2/B1 sớm: (i) chúng không giao write set với PR2/PR3 trừ `ci_dang_ky_test.py` của B1, nên xếp nối tiếp; (ii)
PR3 chuyển một phần bảo đảm sang lượt push và full audit — lớp bù ấy phải KIỂM ĐƯỢC trước khi bật PR3; (iii) thời gian
chờ bóng 14 ngày vốn rảnh. Nếu chủ kho từ chối làn B, làn A chạy đúng như r3 và kế hoạch quay về r3 nguyên vẹn.

## 6. Chỉ số

G1–G6 giữ nguyên r3 §3 (định nghĩa, mẫu số, phép quy G4b). Thêm:

| # | Chỉ số | Nền | Mục tiêu |
|---|---|---|---|
| G7 | Khung cron full audit bị vắng/đỏ mà watchdog không mở Issue trong 36 giờ | CHƯA ĐO (không có watchdog) | 0 sau B2; kiểm bằng fixture lịch vắng và một lần đọc lại thật |
| G8 | Tỷ lệ lần đẩy Package có biên nhận full audit `success` đúng HEAD hoặc ghi đè có lý do | CHƯA ĐO | 100 % sau B3 |
| G9 | Đầu-cuối p50/p95 lượt PR mã (CHỈ BÁO CÁO) | mốc sau 17-11: trung vị 1775 s `[r3 DX-4]` | Không đặt mục tiêu ở làn A/B; mục tiêu 120 s / 300 s chỉ thuộc làn C |

## 7. Câu hỏi chủ kho

Q1–Q5 giữ nguyên r3 §7. Thêm:
- **Q6.** Chấp nhận làn B (B1, B2, B3) như phần của Mission #1172? Khuyến nghị: CÓ — chi phí nhỏ, không đổi cổng `ci.yml`,
  và là điều kiện để lớp bù của PR3/PR6 kiểm được.
- **Q7.** B3: cổng release CHẶN (mặc định) hay chỉ CẢNH BÁO trong 30 ngày đầu? Khuyến nghị: CHẶN, có cờ ghi đè kèm lý do.
- **Q8.** Làn C (nới M9 theo rủi ro) mở sau PR8 hay đóng hẳn? Khuyến nghị: quyết SAU PR8 trên số đo; tới lúc ấy giữ I1.
- **Q9.** Ai được lật công tắc A+1 (chỉ chủ kho, hay cả điều phối dưới uỷ quyền)? Khuyến nghị: tắt (về chạy đủ) — cả hai;
  bật lại — chỉ chủ kho.

## 8. Truy vết đầy đủ

**r2 → r4** (mọi yêu cầu có đích):

| Yêu cầu r2 | Đích r4 | Trạng thái |
|---|---|---|
| PR0 ghim SHA, group riêng, không huỷ | PR0 #1166 (xong) + B1 (A3 canary, A4 definition) | mã xong; đo A3/A4 còn nợ |
| PR1 đo theo ca/mutant/tiến trình con, wall/CPU | Làn A PR1 (đang chạy, chỉ G5) | đang thực thi |
| PR1 RSS, digest OS/Python/deps, overhead ≤ 5 % | A+4 (RSS); digest vào biên nhận B1; overhead: PR1 báo "thêm vài giây mỗi mảnh" (r3) | thu hẹp, có đích |
| PR1 phạm vi `packet_loop_test`, `nhanh_don_duoc_test` | Không đưa vào: hai bộ đã có làn riêng (wp1353 hằng đêm, WP748 đích/đủ) và nằm ngoài khoản lớn | loại, cần Q6 xác nhận ngầm |
| PR1/§4 schema kết cục tám trạng thái | A+3 (PR2, PR5) + B1 | có đích |
| PR2 harness tự kiểm, lỗi cài cố ý, thiếu mảnh, sai SHA | PR1 fixture G4b + PR5 ca âm + A+2 + B1 | có đích |
| PR3 cache | Loại (r3 §6 mục 7) | loại, giữ |
| PR3 fixture bất biến, giảm startup, cân mảnh theo runtime, cô lập state | PR7b (cân mảnh) + A+4; phần còn lại thuộc Q4 (khuyến nghị không) | thu hẹp |
| PR4 selector phụ thuộc/rủi ro, không biết ⇒ đủ | Làn A PR3 (bao đóng bảo thủ) + PR4 + PR6 | có đích |
| PR5 freshness ba trạng thái, watchdog độc lập | B2 | có đích |
| PR5 release đúng candidate, workflow definition OID | B3 + B1 (A4) | có đích |
| PR6 trigger rộng theo rủi ro | Mặc định của làn A: mọi diff chạm bao đóng ⇒ đủ | có đích |
| PR6 audit đỏ, owner, SLA, bisect | B3 (quy trình) | có đích |
| PR7 shadow cặp, seeded, holdout, relative miss | A+2 (cho PR3) + làn C1 | một phần, phần còn lại có điều kiện |
| PR8 M9 theo rủi ro, công tắc bảo thủ, cutover toàn dự án | A+1 (công tắc) + làn C2 | có điều kiện (Q8) |
| §5 cutover cho Packet đủ điều kiện, không hồi tố | Giữ: mọi bổ sung áp từ packet kế tiếp; PR1 không đổi | giữ |
| Mục tiêu p50 ≤ 2 phút / p95 ≤ 5 phút | G9 (chỉ báo cáo) → làn C | hạ thành chỉ báo, cần Q8 |

**Nháp PR0 → r4:** A1, A2, A5, A6 đóng bởi #1166/#1412 (theo hồ sơ accept và merge; M8 `landed: false`); A3, A4 ⇒ B1.
§3.5 biên nhận máy đọc ⇒ B1.

**Proxima → r4:** concurrency riêng, không huỷ (PR0); tách kết cục (A+3); audit dở không xanh + cảnh báo quá hạn (B2);
tự kiểm harness (A+2, PR5 ca âm); nhóm rủi ro buộc audit rộng (bao đóng bảo thủ PR3, mặc định đủ); release gate (B3); audit
đỏ mở Issue có owner (B3); paired full/targeted + holdout + seeded + bỏ sót (A+2, làn C1); triển khai ba giai đoạn (làn A
bóng → bật có kiểm chứng → làn C có điều kiện).

## 9. Phương án loại

Giữ chín phương án loại của r3 §6. Thêm: (10) **khôi phục nguyên r2** — loại: nhắm khoản 4,7 % và đổi lấy M9; (11) **sửa
spec PR1 đang chạy để nhét yêu cầu r2** — loại: hồi tố một packet đã đóng băng/lease; yêu cầu ấy có đích ở A+3/A+4/B1;
(12) **watchdog là một bước trong chính full audit** — loại (r2 §4): lượt vắng không chạy được bước của nó.

## 10. Ngân sách và rủi ro

Làn B ước ba packet nhỏ, mỗi packet: 1–2 lượt thực thi, 1–2 review Codex, 1–2 CI PR Ubuntu, 0 Windows (theo quy tắc
thường trực, trừ B3 cần kiểm `ps1` — chạy `pwsh` trong container như r244, không cần Windows CI), K7 khi chạm vùng M9.
Chi phí chạy thêm: B1 vài giây mỗi lượt audit; B2 một job nhỏ mỗi ngày; B3 một lời gọi REST mỗi lần đẩy Package. Rủi ro
chính: B1 đụng workflow M9 (sensitive, chỉ siết); B3 có thể chặn deploy khi full audit chưa chạy trên HEAD — đó là chủ
đích, có cờ ghi đè. Không bổ sung nào làm tăng giây CI của `ci.yml`.
