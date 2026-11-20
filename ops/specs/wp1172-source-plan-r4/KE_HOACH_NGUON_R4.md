# KẾ HOẠCH NGUỒN r4 — hợp nhất r2 gốc, r3, nháp PR0 và phản biện Proxima (Mission #1172) — bản sửa 6

## 1. Trạng thái và nguồn

- **Trạng thái: `proposed`.** Chưa duyệt, chưa cài. Băm do phiên điều phối ghi khi đóng băng; chỉ có hiệu lực khi chủ
  kho duyệt băm và một Mission revision cài nó. Cho tới lúc ấy **r3 vẫn là kế hoạch hiện hành** (Mission r81/r82).
- **r4 không xoá r3 và không hồi sinh r2.** r4 = r3 (giữ nguyên tám packet, bất biến I1–I6, chín phương án loại, số nền,
  G1–G6) **cộng** các chốt siết A+1…A+5 cho packet làn A CHƯA mở, **cộng** làn bảo đảm B, **cộng** làn chính sách C có
  điều kiện. Câu nào của r3 không được nhắc ở đây là giữ nguyên.
- **Không hồi tố.** PR1 (#1448, spec `5014de59…`, lease `wp1448-r2-g1-claude`) chạy đúng hợp đồng đóng băng của nó; mọi
  bổ sung của r4 áp từ packet KẾ TIẾP. Không bổ sung nào được nhét vào PR1.
- **Bản sửa 2** xử lý 13 finding của review Codex `wp1172-plan-r4-review-1` (2 P1, 11 P2) trên bản sửa 1 (`76b836fa…`,
  `d5bc154`). **Bản sửa 3** xử lý 6 P2 + 1 P3 của `wp1172-plan-r4-review-2` trên bản sửa 2 (`5a34f1e9…`, `3f3f4ab`);
  **Bản sửa 4** xử lý 1 P1 + 1 P2 của `wp1172-plan-r4-review-3` trên bản sửa 3 (`1082c645…`, `a6f7195`); bản sửa 4
  đã qua review lượt 4 (`wp1172-plan-r4-review-4`, còn 1 P1 R4-19). Bản sửa 5 qua review lượt 5 (2 P1 + 3 P2, cùng một
  lớp: uỷ quyền chủ kho do máy kiểm). **Bản sửa 6 BỎ lớp ấy** thay vì vá tiếp (xem §11) và CHƯA được review lại.
- **Nguồn (lưu nguyên byte tại `ops/specs/wp1172-source-plan-r4/nguon/`, `.gitattributes` `-text`):**

| Nguồn | sha256 | Vai trò |
|---|---|---|
| r2 gốc `KE_HOACH_TOI_UU_MUTATION_TESTING_r2_2026-11-03.md` (31 028 byte) | `f4611b0f0c79f33d56b293f5fcb854eeeae2fcbb6acbdfd59d6134dcbfbdcb8f` | Khớp `source_plan_status.r2_sha256` của Mission; chủ kho tìm lại và nộp 2026-11-20 |
| Nháp PR0 `PACKET_DRAFT_CI_FULL_AUDIT_PIN_SHA_2026-11-03.md` | `621026692cda1be04d8f1df1a47828d19d01c087dcb484f7c3b2fbf58a900e8e` | Tiêu chí A1–A6 của PR0 |
| Phản biện Proxima `proxima-mutation-policy-review-20261103.txt` | `122fadcab2dbf34303edafc3cd6e93ae08aeba7f3593ce715eeba7ef1d05cec8` | Tư vấn chính sách tổng quát, KHÔNG phải audit kho |
| r3 `ops/specs/wp1172-source-plan-r3/KE_HOACH_NGUON_R3.md` (nhánh `ops/wp1172-plan-r3`@`c032656`) | `2e9fb13f1ab3f299c2d2dc1e5a6e407ff0aadb8aee1f6ffd00d88fc02b146f89` | Xương sống; cài ở r81 (kèm đính chính làm tròn 3,4–5,6 triệu s của r82) |
| BASELINE #1434 `ops/specs/wp1434-r3/do/BASELINE.json` @ `5e5d2cc` | `6100c8e18907f59b1abbdc44195861cc2310c654ce8dcfa2e74ca4ffa155f54c` | Nền số |

## 2. Kế thừa — việc đã làm và nơi nó được dùng tiếp

| Việc | Trạng thái đo được | Dùng tiếp ở r4 |
|---|---|---|
| PR0 #1166 → PR #1412 | accepted rev12 H3 `b79cbf5`; merged `f8b9cdd`; M8 `landed: false` | Nền của làn B. Đối chiếu từng tiêu chí của nháp ở bảng §8.2 — KHÔNG coi là "nháp đã đạt" |
| `ops-do-workflow-definition.yml` (#1094) | trên master | B1/B3 dùng để đo định danh workflow definition, không dựng đường mới |
| Đo nền #1434 | merged `5e5d2cc`; ảnh chụp thô thu lại 2026-11-20 cùng T0/T1 | Nền G1–G6; đầu vào nghiệm thu PR1 mục 5 |
| r3 (4 vòng review Codex) | installed r81 | Làn A |
| PR1 #1448 | leased, đang thực thi lượt 1/3 | Giữ nguyên; bóng 14 ngày của nó là đầu vào PR3/PR4 và phép đo overhead A+5 |
| #1308, #1370, #1393, #1422 | accepted/merged | Sửa vòng đời, admission, biên nhận công bố. KHÔNG tính là tiết kiệm thời gian |
| #1143/#1155, wp892, wp1343/wp1353, WP748 | landed | Tiền lệ và cơ chế mà r3 PR3/PR6 mở rộng; không làm lại |

## 3. Phản biện ba nguồn

**r2.** Đúng: bằng chứng full audit ghim SHA và không bị thay chỗ; tách `cancelled`/`timed_out`/`infrastructure_error`/
`not_run` khỏi đạt; tự kiểm harness bằng lỗi cài cố ý; watchdog ĐỘC LẬP; release kiểm đúng candidate; rollback tức
thời, không chờ PR. Sai theo số đo về sau: r2 coi khoản lớn là full audit và nhắm cắt M9; full audit chỉ 700 504 s = 4,7 %
`[r3 DX-5]`, còn bước G5 trên lượt `ci.yml` là 52,8 % `[B: M2.theo_buoc…G5]`. Mục tiêu "preflight p50 ≤ 2 phút" của r2
không có phép đo nền và là mục tiêu cho MỘT làn mới chưa tồn tại.

**r3.** Đúng: dựng trên số đo; nhắm khoản lớn; giữ M9 (I1); fail-closed ba trạng thái; bóng ≥ 14 ngày trước khi bật.
Thiếu (soạn khi r2 bị coi là mất): watchdog/freshness cho full audit mà I1/I5 dựa vào; cổng release; quy trình audit đỏ;
rollback của PR3/PR6 cần một PR; điều kiện bật PR3 không có lỗi cài cố ý; kết cục không có tầng thực thi tường minh;
không đo RSS và overhead.

**Proxima.** Chỉ dùng làm danh mục kiểm. Bốn điểm chưa có trong r3: audit dở không bao giờ xanh + cảnh báo quá hạn; tự
kiểm harness; release gate; đo cả lỗi BỎ SÓT bằng holdout/seeded. Proxima cũng nói "audit tuần không thay được kiểm chứng
tại thời điểm merge" — ủng hộ I1 của r3.

**Xung đột duy nhất:** r2 PR8 (M9 theo rủi ro) ↔ r3 §6 phương án loại 3. Giải: giữ I1 mặc định; phần của r2 thành làn C
hai cửa (Q8a cho NGHIÊN CỨU, Q8b cho ĐỔI M9 chỉ sau kết quả C1).

## 4. Làn A — giảm chi phí (r3) + năm chốt siết

PR1 → PR2 → PR3 → PR4 → PR5 → PR6 → PR7 → PR8 đúng r3 §5. Năm chốt áp vào đặc tả packet tương ứng khi tới lượt.

**Không có kho uỷ quyền do máy kiểm.** Ba lượt review (R4-08 → R4-19 → R4-20…R4-24) cho thấy mọi cách để máy chứng minh
"chủ kho đã cấp quyền" (biến, comment, tệp git do chủ kho merge) đều mở thêm lỗ, vì quy tắc thường trực "chủ kho bấm mọi
merge" làm `merged_by` mất nghĩa cấp quyền. r4 vì vậy chỉ dựa vào hai thứ có thẩm quyền rõ ràng: (1) **quyền quản lý biến
Actions** của kho (đo tập chủ thể ghi được); (2) **mã đã merge qua review** như mọi thay đổi cổng khác. Không cơ chế nào ở
r4 cho phép NỚI một cổng bằng một bản ghi ngoài mã.

- **A+1 (PR3, PR6, C2) — công tắc bảo thủ có thẩm quyền đo được.**
  - **Công tắc CHỈ SIẾT.** Một Actions repository variable (tên đóng băng trong đặc tả B4) với đúng một giá trị có hiệu
    lực: `FULL` ⇒ mọi lượt PR chạy G5 đủ, bất kể bộ phân loại nói gì. Mọi giá trị khác hoặc biến vắng ⇒ hành vi của MÃ ĐÃ
    MERGE (tức PR3/PR6 sau khi đã qua review và chủ kho merge). Công tắc không bao giờ nới được gì ngoài mã.
  - **Ai lật được.** Đo tập chủ thể ghi được biến của kho (giả thuyết cần đo: kho cá nhân thì chỉ chủ kho, cộng GitHub App
    có quyền Variables:write). Chủ kho xác nhận tập ấy ở Q9. Nếu tập ấy CHỈ là chủ kho thì "bỏ `FULL`" (nới lại về hành vi
    mã) chỉ chủ kho làm được — đúng yêu cầu r2 "bật lại theo quyết định mới của chủ kho" — mà không cần bản ghi nào. Nếu tập
    ấy rộng hơn và không thu hẹp được, công tắc vẫn dùng được để SIẾT nhưng chủ kho phải chấp nhận ở Q9 rằng người ghi khác
    cũng bỏ được `FULL`; không chấp nhận ⇒ PR3/PR6 chỉ hoàn tác bằng revert (r3 gốc).
  - **Điều phối không cần quyền ghi biến để siết:** `kiem-merge` LUÔN được phép đòi G5 đủ cho một PR (siết là việc ai cũng
    được làm); điều phối dưới uỷ quyền dùng đường ấy khi có sự cố, rồi báo chủ kho đặt `FULL`.
  - Không đọc được biến ⇒ hành vi mã đã merge (vì công tắc chỉ siết, mất đọc không thể nới); ghi rõ trong log lượt.
  - Nghiệm thu B4: `FULL` ⇒ đủ ở cả job PR lẫn `kiem-merge`; PR sửa job tiêu dùng để bỏ qua `FULL` ⇒ `kiem-merge` vẫn
    đòi đủ; đặt `FULL` sau khi lượt bỏ qua đã xanh ⇒ `kiem-merge` đỏ; mọi giá trị khác ⇒ không đổi hành vi; đột biến "giá trị
    lạ ⇒ bỏ" phải đỏ. Trước khi đóng băng spec B4: đo tập người ghi và quyền đọc biến từ máy chạy `kiem-merge`.
  - Tiêu dùng có thẩm quyền KHÔNG phải job trong cây PR (trên `pull_request`, PR có thể sửa chính `ci.yml` hay bộ phân
    loại). Thẩm quyền nằm ở cổng merge chạy từ cây TIN CẬY: `kiem-merge` (từ master, không từ head PR) đọc lại công tắc
    tại thời điểm xét merge và TÍNH LẠI yêu cầu từ diff bằng bao đóng của mã trên master: diff chạm bao đóng, hoặc công tắc
    = `FULL` ⇒ đòi G5 đủ `success` trên đúng H, bất kể job PR nói gì. Job `chuan-bi` đọc công tắc chỉ để tiết kiệm; output
    của nó là gợi ý. Không dùng `pull_request_target` chạy mã PR.
  - Mã tiêu dùng tin cậy (`kiem-merge`: `.claude/dev/packet_loop.py` + test) KHÔNG nằm trong write set r3 của PR3/PR6,
    nên thuộc một packet riêng **B4 — công tắc chỉ siết và tiêu dùng tin cậy** (sensitive), land TRƯỚC khi PR3 bật.
- **A+2 (điều kiện bật PR3 thứ sáu) — lỗi cài cố ý.** Tập lỗi KHÓA TRƯỚC bởi oracle độc lập (không do bộ phân loại sinh),
  mỗi lỗi ở một thành phần bao đóng (`ops/` thường, `.claude/dev/`, `scripts/*.py`, `.github/`, cấu hình gốc, tệp đọc qua
  object git) ⇒ bóng phải `chay` cho 100 %. Cộng các PR lịch sử trong cohort có G5 đỏ không do hạ tầng (ghi đúng số tìm
  được; tìm được 0 thì ghi 0, không bịa) ⇒ bóng `chay`.
- **A+3 (PR2, PR5, B1) — kết cục theo tầng, không gộp.** Bốn trường tách biệt:
  `trang_thai_thuc_thi` ∈ {`hoan_tat`, `timed_out`, `infrastructure_error`, `cancelled`, `not_run`} ·
  `quan_sat_ca` (mỗi ca: `passed`/`failed`) · `phan_hang_dot_bien` ∈ {`giet`, `song`, `tin_dung_gia`,
  `equivalent_reviewed` (bắt buộc `ly_do` + `nguoi_xac_nhan`; không bao giờ đếm là giết)} · `ket_luan_tong` ∈ {`xanh`,
  `do`, `khong_ket_luan`}. Luật: `ket_luan_tong = xanh` chỉ khi mọi mục `hoan_tat`, ca nền `passed`, và mọi đột biến
  được phân hạng theo đúng bộ phân hạng hiện có (I2, không đổi); ca KHÔNG phải đích sống sót là bình thường, không làm
  đỏ. Fixture bắt buộc: nền khoẻ · ca không đích sống · giết đúng đích · tín dụng giả · tương đương có xét duyệt ·
  timeout/hạ tầng. Kiểm hai chiều: bên đọc cũ vẫn đọc được; số giết không đổi trên cùng SHA.
- **A+4 (PR7b) — bộ nhớ.** RSS đỉnh theo TỪNG tiến trình con bằng `os.wait4` (rusage riêng của con vừa thu, đơn vị KiB
  trên Linux, gồm cháu đã được con thu); nhu cầu ĐỒNG THỜI đo riêng qua cgroup (`memory.peak`) khi có. Không có ⇒
  `khong_do_duoc`. Không dùng `RUSAGE_CHILDREN` (giữ mức cao nhất qua các con đã thu). Ca: con tuần tự khác cỡ, con
  chồng nhau.
- **A+5 (điều kiện bật PR3 thứ bảy) — overhead của phần đo PR1.** Đo GHÉP CẶP bật/tắt trên CÙNG ảnh chụp bất biến (sản
  phẩm, test, đột biến, môi trường), chạy xen kẽ lặp lại (≥ 5 cặp trên một mảnh), ước lượng = trung vị hiệu ghép cặp; cần
  một công tắc môi trường tắt phần đo — thêm trong write set của PR3 (`ops/cong_cu_test.py`), không sửa PR1. Ca kiểm có
  overhead nhân tạo biết trước. **Phủ:** cả 8 mảnh, mỗi mảnh ≥ 3 cặp xen kẽ; ước lượng toàn cục = tổng trung vị hiệu ghép
  cặp của 8 mảnh / tổng trung vị thời gian bản tắt của 8 mảnh (có trọng số theo thời gian từng mảnh); kèm ca kiểm "mảnh
  không đồng nhất" (overhead tập trung ở một mảnh). Đo trong môi trường đo cố định (container), không dùng lượt CI thêm;
  ước ~48 lượt mảnh ≈ 10 giờ máy, tính vào ngân sách của PR3. Đo không đủ 8 mảnh thì chỉ báo mảnh đã đo và ngưỡng toàn
  cục là `khong_do_duoc` ⇒ điều kiện bật thứ bảy CHƯA đạt. Overhead ≤ 5 % ⇒ giữ; > 5 % ⇒ chuyển phần đo sang lấy mẫu ngoài cổng, không xoá tín hiệu
  (r2 §5.1). So sánh trước/sau theo cohort 14 ngày chỉ là giám sát vận hành, KHÔNG phải phép đo overhead.

## 5. Làn B — bảo đảm bằng chứng (không đổi quyết định cổng `ci.yml`, không nới M9)

### B1 — Hợp đồng biên nhận full audit (bên sản xuất) + canary A3 + A4

- **Hợp đồng `bien_nhan_audit.v1` (đóng băng TRƯỚC B2/B3).** Trường: kho; đường dẫn workflow; định danh definition
  (`github.workflow_sha` + blob/sha256 của tệp tại OID ấy, hoặc `not_measured`); sự kiện; khung cron (nếu `schedule`);
  SHA sự kiện; SHA/tree checkout từng job; run_id, attempt của lượt và attempt của TỪNG bên sản xuất mảnh (giữ dòng
  chạy-lại-mảnh đang được phép từ PR0, không cấm cũng không tin mù); danh sách job/mục KỲ VỌNG lập độc lập từ mã tại
  SHA ấy và tập thực có; kết luận cuối từng job; artifact id + digest; Python/OS/digest phụ thuộc (`requirements*.txt`,
  phiên bản công cụ); kết cục theo A+3; giây và bộ nhớ từng mảnh; dấu hiệu dương.
- **A3 — canary concurrency.** Hai `workflow_dispatch` khác run_id trên CÙNG SHA, chồng thời gian ⇒ HAI biên nhận audit
  hoàn tất, không lượt nào `cancelled` vì concurrency; cộng một quan sát RIÊNG: một lượt push `ci.yml` chạy trong lúc ấy
  (ghi run_id, queue/start/end, số job chạy thật) không huỷ lượt audit nào. Push không kích hoạt `ci-dot-bien-du.yml`;
  không thêm trigger push. (Muốn ba lượt audit thì phải là dispatch thứ ba, tính vào ngân sách.)
- **A4.** Gọi `ops-do-workflow-definition.yml` cho mỗi lượt canary; hợp đồng cho phép `not_measured` ở bên sản xuất, nhưng
  bên tiêu dùng B3 thì không (xem B3).
- Write set: `.github/workflows/ci-dot-bien-du.yml`, `.claude/dev/ci_dang_ky_test.py`, đặc tả mới. Trước PR5 (cùng write set).

### B2 — Watchdog freshness (bên tiêu dùng đọc báo cáo)

- Workflow MỚI, lịch riêng **mỗi 6 giờ** + `workflow_dispatch`; quyền: đọc Actions, ghi Issue. Đọc REST (phân trang có
  giới hạn) các lượt `ci-dot-bien-du.yml`, kiểm biên nhận B1 theo hợp đồng v1.
- Ba trạng thái như r2 §4: `fresh` · `due_in_progress` · `stale_or_missing`. Tuổi tính từ khung/snapshot gốc; chạy lại
  cùng SHA cũ KHÔNG làm mới. Đọc API lỗi ⇒ `khong_do_duoc` (không bao giờ thành `fresh`).
- `stale_or_missing` hoặc `khong_do_duoc` ⇒ mở/cập nhật MỘT Issue theo dõi rồi ĐỌC LẠI Issue; ghi Issue lỗi ⇒ job đỏ.
  Job đỏ KHÔNG đồng nghĩa chủ kho đã nhận tin (định tuyến thông báo phụ thuộc người kích hoạt lịch và cài đặt). Điều kiện
  bật B2: chủ kho theo dõi (subscribe) Issue theo dõi và một lần thử giao tin thật được xác nhận; chưa xác nhận ⇒ kênh
  giao tin ghi `chua_do`.
- Nhịp tim: mỗi lượt watchdog ghi dấu thời gian lên Issue theo dõi; lượt kế tiếp và B3 đọc dấu ấy và báo khi cũ hơn 24
  giờ; phiên điều phối kiểm nó bằng TAY ở đầu mỗi phiên theo một runbook dev-side (không sửa `doctor`). Đây là giám sát
  chéo, không phải SLA cứng (cùng chịu rủi ro lịch GitHub).
- Báo cáo hiện cả SHA đầu `master` hiện tại, SHA đã audit và khoảng cách giữa hai bên; không bao giờ ghi "master hiện tại
  đã đủ" khi hai SHA khác nhau (r2 §4).
- **G7 phát biểu đúng phạm vi:** cảnh báo trong ≤ khung + 36 h + 6 h (chu kỳ) + độ trễ lịch đã khai; là best-effort có
  giám sát chéo, chủ kho chấp nhận ở Q6.
- **Thứ tự:** SAU B1 (cần hợp đồng v1). Ban đầu chỉ báo cáo, không chặn merge.
- Write set: workflow mới, script `ops/` mới + test, VÀ `.claude/dev/ci_dang_ky_test.py` (đăng ký bộ test mới vào
  registry theo đường thông thường) — nên xếp nối tiếp với B1/PR2. Ca: biên thời gian, khung vắng, chạy lại SHA cũ, API
  bị từ chối, ghi Issue lỗi, lượt watchdog vắng.

### B3 — Cổng release đúng candidate + quy trình audit đỏ

- **"Release"** = đẩy Package (`scripts/deploy-package.sh --push`, `scripts/deploy-package.ps1 -Push`).
- **Ràng buộc byte:** trước khi build, ghi H và tree; đòi cây sạch (không tệp theo dõi bị sửa, không tệp chưa theo dõi
  lọt vào tập phát hành; tệp trạng thái deploy bị ignore được phép nhưng không vào gói); build từ ảnh chụp đã kiểm của H
  (ví dụ `git archive H`) HOẶC so tập tệp + byte phát hành với blob tại H; tính digest gói và GẮN vào bằng chứng; ngay
  trước `drive-push` kiểm lại H, tree, digest.
- **Ref phát hành và CI bắt buộc:** ref phát hành = `master`. Trạng thái bảo vệ của `master` (cấm force-push/xoá, ai
  vượt được) là ĐIỀU KIỆN TIÊN QUYẾT đo một lần lúc bật B3 bằng quyền quản trị của chủ kho, ghi hồ sơ, đo lại theo
  runbook hằng tháng; B3 KHÔNG đọc nó lúc deploy (token chỉ đọc không đủ quyền), và rủi ro trôi cấu hình giữa hai lần đo
  là rủi ro tồn dư chủ kho chấp nhận ở Q7. H phải là commit trên `master` (bằng đầu nhánh hoặc tổ tiên của nó, đo bằng git trên bản
  sao đủ lịch sử); mọi check bắt buộc của lượt push `ci.yml` trên đúng H phải `success` (đọc REST, nguồn gốc khớp). "Không
  tụt sau master" KHÔNG đồng nghĩa "được phép phát hành". Ca: H sạch, đi trước master, audit xanh nhưng một check bắt
  buộc đỏ/vắng ⇒ chặn; ref di chuyển giữa lúc kiểm và lúc đẩy ⇒ chặn.
- **Kiểm biên nhận (bên tiêu dùng B1 v1):** đúng kho, đúng workflow, definition ĐO ĐƯỢC (khi biên nhận ghi `not_measured`:
  một người vận hành được uỷ quyền chạy A4 TRƯỚC cho đúng lượt ấy; B3 chỉ ĐỌC artifact A4 bằng quyền chỉ đọc; artifact vắng,
  cũ, GraphQL null hoặc hết giờ ⇒ chặn, không hạ xuống cảnh báo sau khi chế độ chặn đã bật), SHA = H, mọi job kỳ vọng có mặt và `success`, kết cục `xanh`, artifact digest khớp, dòng
  attempt hợp lệ. Bất kỳ trường bắt buộc nào vắng/lạ/không đọc được ⇒ chặn.
- **Xác thực trên máy deploy — bảng năng lực:** B3 chỉ gọi: danh sách lượt + job + artifact của workflow (Actions:
  read), check run của commit (Checks: read), nội dung/so sánh commit (Contents: read). Không cần quyền PR metadata, bảo
  vệ nhánh, biến hay dispatch. Đo TỪNG endpoint từ CẢ HAI máy deploy (403/404, phân trang thiếu, chuyển hướng artifact)
  trước khi bật chế độ chặn; chưa đo ⇒ `warning_only`, ghi rõ; sau khi bật chặn, mọi lỗi đọc ⇒ chặn.
- **Không có ngoại lệ do máy cấp.** Thiếu biên nhận audit trên H ⇒ đường bình thường là chạy full audit trên H (dispatch
  bởi người có quyền) rồi deploy. Trường hợp khẩn cấp: CHỈ chủ kho, tự tay chạy deploy trên máy của mình với cờ khẩn cấp
  đòi gõ lại đúng H trên TTY tương tác; script ghi biên bản (H, digest gói, lý do) vào log deploy và in cảnh báo; G8 đếm
  lần ấy là `owner_emergency`. Phiên AI KHÔNG BAO GIỜ dùng cờ này (thêm vào danh sách cấm của hook PreToolUse như
  `--apply`). Đây là quy trình có người, không phải bằng chứng máy — nói thẳng ra ở Q7.
- **Hai nền:** chạy thật `sh` trên Linux và `ps1` trên **Windows thật** (máy Windows của chủ kho), đối chiếu parity cùng đầu
  vào, base và candidate (bài học r244). `pwsh` trong container Linux chỉ là bằng chứng phụ. Không dùng Windows CI (quy
  tắc thường trực); hoặc chủ kho miễn Windows-local cho B3 bằng văn bản, nêu rủi ro tồn dư.
- **Quy trình audit đỏ** (tài liệu dev-side): owner = chủ kho; xác nhận ≤ 2 giờ làm việc; ≤ 1 ngày làm việc có Issue nêu
  H, ID đỏ, phân loại code/test/hạ tầng, tái hiện tối thiểu hoặc lý do chưa tái hiện; tối đa 1 lần chạy lại hạ tầng, giữ
  attempt đỏ; bisect chỉ trên commit dựng được, không dựng được ghi `not_testable`; trong lúc chưa khoanh được vùng, lật
  công tắc A+1 về chạy đủ (khi A+1 đã có) và không merge thay đổi cùng vùng; release bị chặn tới khi có audit xanh đúng
  candidate hoặc ngoại lệ hợp lệ.
- Phụ thuộc B1. Write set: hai script deploy + test của chúng, tài liệu quy trình.

## 6. Làn C — chính sách M9 (r2 PR7/PR8), mặc định ĐÓNG, hai cửa

- **Cửa Q8a — được NGHIÊN CỨU** (chỉ khi làn A PR8 đo xong 30 ngày và B1–B3 đã land). C1: shadow cặp đủ/đích trên CÙNG
  snapshot (sản phẩm, đầu vào, kiểm kê, môi trường); lỗi lịch sử, lỗi cài cố ý và holdout KHÓA TRƯỚC khi chỉnh bộ chọn;
  vòng 1 = 6 replay lịch sử + 4 PR mã live (10 cặp), trần 50 runner giờ, mốc sau 5 cặp; vòng 2 cần quyết định mới, tối
  đa 30 cặp / 150 runner giờ hoặc 2 tuần; đơn vị đếm = cụm nguyên nhân gốc/PR; báo bỏ sót tương đối so với đủ theo tầng
  rủi ro; tiêu chí: **0 P0/P1 lịch sử/seeded bị bỏ sót**; khoảng tin cậy chỉ khi giả định lấy mẫu đạt (r2 §5.2–§5.3).
- **Cửa Q8b — được ĐỔI M9** chỉ sau kết quả C1 và quyết định văn bản của chủ kho. C2 sửa ADR-0060/K7 theo rủi ro, dùng
  A+1 làm công tắc, mất đọc = full M9, kiểm âm trước merge khi PR rollback chưa land (r2 PR8).
- Mục tiêu preflight p50 ≤ 2 phút / p95 ≤ 5 phút chỉ thuộc làn C.

## 7. Thứ tự và phụ thuộc (một executor tại một thời điểm)

1. **PR1** (đang chạy) → land; bóng 14 ngày bắt đầu.
2. **B1** (hợp đồng v1 + canary A3/A4).
3. **B2** (sau B1).
4. **PR2** (Q3 quyết trước).
5. **B4** (công tắc A+1 + tiêu dùng tin cậy trong `kiem-merge`; sau Q9).
6. **PR3** (sau ≥ 14 ngày bóng, Q1, B4 đã land, A+2, A+5).
7. **B3** (sau B1; Q7).
8. **PR4** → **PR5** (sau B1) → **PR6** → **PR7** → **PR8**.
9. **Làn C** chỉ khi Q8a/Q8b mở.

Ba packet chung tệp `.claude/dev/ci_dang_ky_test.py` (B1, B2, PR2) xếp nối tiếp; B4 đụng `.claude/dev/packet_loop.py`
(tệp nóng, sensitive) nên kiểm lease toàn kho trước khi cấp; effective write set đo lại trước mỗi
lease. B1/B2/PR2 lấp khoảng chờ bóng 14 ngày. Chủ kho từ chối làn B ⇒ làn A chạy đúng r3, chỉ giữ A+2…A+5 nếu Q6 cho phép.

## 8. Truy vết đầy đủ

### 8.1 r2 → r4 (từng yêu cầu chuẩn tắc)

| Mục r2 | Yêu cầu | Đích r4 | Trạng thái |
|---|---|---|---|
| §3 PR0 | ghim SHA, group theo run, không huỷ, chốt cấu trúc | PR0 (mã) + bảng §8.2 + B1 | mã có; đo còn nợ |
| §3 PR1 | đo theo ca/mutant/tiến trình con, wall/CPU | PR1 (chỉ G5) | đang thực thi |
| §3 PR1 | RSS đỉnh | A+4 | đích |
| §3 PR1 | runner OS/Python/digest phụ thuộc | trường của B1 v1 | đích |
| §3 PR1 | overhead ≤ 5 % hoặc tách khỏi cổng | A+5 (ghép cặp bật/tắt, cùng ảnh chụp) | đích |
| §3 PR1 | 1 full + 3 targeted cùng SHA, khớp ID/kết cục | PR1 nghiệm thu 1 (A/B 8 mảnh hai vế, toàn bộ định danh) cho G5; phần targeted thuộc C1 | thu hẹp, có lý do: chưa có làn targeted |
| §3 PR1 | phủ `packet_loop_test`, `nhanh_don_duoc_test` | Không đưa vào làn A/B: hai bộ đã có làn riêng (wp1353 hằng đêm; WP748 đích/đủ) và ngoài khoản lớn; C1 có thể gồm | loại khỏi A/B — chủ kho xác nhận ở Q6 |
| §3 PR1/§4 | tách kết cục; tương đương có xét duyệt | A+3 | đích |
| §3 PR2 | fixture âm cho runner/parser/selector/aggregator | PR1 fixture G4b · PR5 ca âm · A+2 · A+3 fixture · B1/B3 ca âm | đích, phân tán theo packet |
| §3 PR3 | cache | r3 §6 mục 7 | loại, giữ |
| §3 PR3 | fixture bất biến, giảm startup, cô lập state | Q4 (r3 khuyến nghị không) | chờ quyết |
| §3 PR3 | cân mảnh theo runtime, ràng buộc RSS | PR7b + A+4 | đích |
| §3 PR3/§4 | reference đóng băng, cold/warm, hai runner, oracle seeded | Chỉ cần khi tối ưu harness (Q4); A+2 dùng oracle khóa trước | phụ thuộc Q4 |
| §3 PR4 | selector theo phụ thuộc/rủi ro; không biết ⇒ rộng; manifest quyết định | r3 PR3 (bao đóng bảo thủ, dòng bóng có lý do) + PR4 + PR6 | đích; manifest ID chọn chỉ ở PR6 |
| §3 PR4 | PR sửa chính bộ chọn không tự xếp làn nhẹ | bao đóng bảo thủ gồm `ops/`, `.github/` + A+1 ở `kiem-merge` | đích |
| §3 PR5/§4 | freshness 36 h/8 ngày, watchdog độc lập, retry hạ tầng ≤ 1 | B2 + B3 quy trình | đích (G7 best-effort, Q6) |
| §3 PR5 | release đúng candidate, definition OID | B3 + B1 (A4 do người vận hành chạy trước, B3 chỉ đọc) | đích |
| §4 release | ref phát hành được bảo vệ + check bắt buộc trên H | B3 (ref = `master`, đo bảo vệ, check push `ci.yml` trên H) | đích |
| §4 thời gian | bảng điều khiển hiện SHA master hiện tại so với SHA đã audit | B2 báo cáo | đích |
| §3 PR6 | trigger rộng theo rủi ro | mặc định làn A: chạm bao đóng ⇒ đủ | đích |
| §3 PR6/§5 | audit đỏ: owner, 2 giờ, 1 ngày, tái hiện, bisect, chặn cả candidate | B3 quy trình | đích |
| §3 PR7/§5.2–5.3 | shadow cặp, holdout, seeded, bỏ sót tương đối, trần 10 cặp/50 h, 30/150 | C1 (Q8a) + A+2 | có điều kiện |
| §3 PR8/§5.4–5.5 | M9 theo rủi ro, công tắc bảo thủ, cutover cho Packet mới, không hồi tố | A+1/B4 + C2 (Q8b) | công tắc: đích; M9: có điều kiện |
| §4 release | ngoại lệ thành phần cần manifest + audit thành phần hoặc waiver cụ thể | B3 ngoại lệ do chủ kho; ngoại lệ thành phần: không áp (gói là một khối) | đích |
| §6 | ngưỡng p95 ≤ 5 phút, 0 P0/P1 lọt | làn C | có điều kiện |
| §6 mục 3 | ai được tắt ngay targeted, ai được waiver | Q7, Q9 | chờ quyết |

### 8.2 Nháp PR0 → r4 (từng tiêu chí; không suy "đạt" từ accept của spec hẹp hơn)

| ID | Điều kiện của nháp | Hiện trạng | Đích |
|---|---|---|---|
| A1 | actionlint, registry, test workflow đạt trên H | mã và chốt tĩnh (`loi_ghim_sha_du`, `chon_bien_nhan_du`, `loi_bien_nhan_du`) có trên master; kết quả trên H3 nằm trong hồ sơ accept rev12, r4 CHƯA đối chiếu từng mục | B1 ghi lại |
| A2 | dispatch trên H: mọi checkout/artifact = H, 10/10 job, K7 rc 0 | CHƯA XÁC MINH trong r4 (cần đọc hồ sơ accept rev12 và #1412) | B1 canary tạo bằng chứng mới |
| A3 | hai dispatch cùng SHA + một push, không lượt nào bị thay chỗ | `not_run` | B1 (thiết kế đã sửa) |
| A4 | definition OID tách khỏi source OID | `not_measured` | B1/B3 |
| A5 | Windows exact H, full audit, CI PR, `kiem-merge` | Windows: MIỄN theo quy tắc thường trực (r67); phần còn lại CHƯA XÁC MINH trong r4 | ghi lại trong hồ sơ B1 |
| A6 | review độc lập, land, hậu merge readback | merged; M8 `landed: false` (§10.2.2 không đo được) | nợ đo, B1 ghi lại |
| §3.5 | biên nhận máy đọc | chưa có | B1 v1 |

### 8.3 Proxima → r4

Concurrency riêng không huỷ (PR0, B1 A3) · tách kết cục (A+3) · audit dở không xanh + cảnh báo quá hạn (B2) · tự kiểm
harness (A+2, A+3, PR5) · nhóm rủi ro buộc rộng (bao đóng bảo thủ) · release gate (B3) · audit đỏ mở Issue có owner, tạm
dừng merge cùng vùng (B3) · paired full/targeted + holdout + seeded + bỏ sót (A+2, C1) · ba giai đoạn (bóng → bật có kiểm
chứng → làn C có điều kiện).

## 9. Chỉ số

G1–G6 giữ nguyên r3 §3. Thêm:

| # | Chỉ số | Nền | Mục tiêu |
|---|---|---|---|
| G7 | Khung cron vắng/đỏ được cảnh báo trong ≤ khung + 36 h + 6 h + độ trễ lịch | CHƯA ĐO | 100 % sau B2, best-effort có giám sát chéo (Q6) |
| G8 | Lần đẩy Package, báo TÁCH ba dòng: `audit_passed` · `owner_emergency` · `warning_only` | CHƯA ĐO | sau B3 chế độ chặn: `warning_only` = 0; `audit_passed` + `owner_emergency` = 100 %; mỗi `owner_emergency` có biên bản |
| G9 | Đầu-cuối p50/p95 (CHỈ BÁO CÁO) | quần thể: `pull_request`, luật cũ `day_du`, `success`, một attempt, đầu-cuối suy từ job, sau 17-11: trung vị 1775 s, p25 1590 `[r3 DX-4]` | không mục tiêu ở A/B; báo riêng `cancelled`/`failure` và thời gian xếp hàng; quần thể rộng hơn cần nền riêng |

## 10. Câu hỏi chủ kho

Q1–Q5 giữ nguyên r3 §7. Thêm:
- **Q6.** Chấp nhận làn B và A+2…A+5; chấp nhận G7 là best-effort có giám sát chéo; chấp nhận loại `packet_loop_test`/
  `nhanh_don_duoc_test` khỏi A/B? Khuyến nghị: CÓ.
- **Q7.** B3: chặn hay cảnh báo 30 ngày đầu; chấp nhận (a) KHÔNG có ngoại lệ do máy, khẩn cấp chỉ là chủ kho tự chạy với
  cờ có xác nhận TTY, và (b) bảo vệ `master` đo lúc bật + hằng tháng (trôi giữa hai lần là rủi ro tồn dư)? Khuyến nghị: chặn
  khi đã đo xong năng lực đọc trên cả hai máy deploy; chấp nhận (a) và (b).
- **Q8a / Q8b.** Cho nghiên cứu C1 sau PR8 (Q8a)? Đổi M9 chỉ sau C1 (Q8b)? Khuyến nghị: quyết Q8a sau PR8, Q8b sau C1.
- **Q9.** Xác nhận tập chủ thể ghi được biến công tắc (đo được; giả thuyết: chỉ chủ kho + App có Variables:write) và cơ
  chế A+1 CHỈ SIẾT (`FULL` ⇒ đủ; còn lại ⇒ hành vi mã). Khuyến nghị: thu hẹp tập ấy về chỉ chủ kho; khi ấy bỏ `FULL` là
  quyết định của chủ kho theo cấu trúc. Điều phối siết bằng `kiem-merge`, không cần quyền ghi biến.

## 11. Xử lý review `wp1172-plan-r4-review-1`

| Finding | Mức | Xử lý |
|---|---|---|
| R4-01 khai quá về A2/A5/A6 | P2 | §2, bảng §8.2 từng tiêu chí: delivered/not_run/not_measured/miễn/chưa xác minh |
| R4-02 truy vết mất mát | P2 | §8.1 tách từng yêu cầu; overhead ⇒ A+5; digest ⇒ B1; SLA 2 giờ/1 ngày, tái hiện tối thiểu, dừng merge cùng vùng ⇒ B3; C1 giữ trần và tiêu chí 0 P0/P1; Q8 tách a/b |
| R4-03 kết cục gộp tầng | P2 | A+3 bốn trường, giữ `equivalent_reviewed`, fixture và kiểm tương thích |
| R4-04 RSS không theo từng con | P2 | A+4 dùng `os.wait4` + cgroup; bỏ `RUSAGE_CHILDREN` |
| R4-05 canary ba biên nhận bất khả | P2 | B1 A3: hai biên nhận audit + một quan sát push riêng |
| R4-06 B2 trước B1, thiếu đăng ký test | P2 | B2 sau B1; write set gồm `ci_dang_ky_test.py`; xếp nối tiếp |
| R4-07 SLA watchdog | P2 | chu kỳ 6 h, đọc lại Issue, ghi lỗi ⇒ đỏ, nhịp tim chéo; G7 best-effort |
| R4-08 thẩm quyền công tắc | P2 | A+1: đo người ghi, tiêu dùng có thẩm quyền ở `kiem-merge` từ cây tin cậy, vô hiệu bằng chứng cũ khi tắt |
| R4-09 biên nhận release thiếu provenance | P1 | B1 hợp đồng v1 đóng băng trước B2/B3; B3 từ chối mọi trường bắt buộc vắng; A4 cho chính lượt; token đo trước khi chặn |
| R4-10 HEAD không ràng buộc byte gói | P1 | B3 ràng buộc byte: cây sạch, build từ ảnh chụp H, digest gói, kiểm lại trước push |
| R4-11 cờ ghi đè không phải waiver | P2 | B3 ngoại lệ chỉ do chủ kho, kiểm REST; G8 ba dòng |
| R4-12 pwsh Linux không phải Windows | P2 | B3 parity trên Windows thật hoặc miễn văn bản |
| R4-13 quần thể G9 | P2 | G9 nêu đủ bộ lọc, báo riêng huỷ/đỏ/xếp hàng |

Review lượt 2 (`wp1172-plan-r4-review-2`, trên `3f3f4ab`): 9 finding lượt 1 đóng, 4 đóng một phần; thêm 4 finding mới.

| Finding | Mức | Xử lý ở bản sửa 3 |
|---|---|---|
| R4-02 (phần còn lại) ref phát hành, CI bắt buộc, hiển thị master so snapshot | P2 | B3 "Ref phát hành và CI bắt buộc"; B2 báo cáo hai SHA; hai dòng mới ở §8.1 |
| R4-07 (phần còn lại) job đỏ ≠ đã báo chủ kho | P2 | B2: điều kiện bật = chủ kho subscribe + thử giao tin thật; chưa xác nhận ⇒ `chua_do` |
| R4-08 (phần còn lại) App ghi được biến; bật lại không do chủ kho | P2 | A+1: biến chỉ tắt; bật = bản ghi thế hệ của OWNER; Q9 gồm App; không đo được ⇒ đủ |
| R4-14 overhead bị nhiễu | P2 | A+5 ghép cặp bật/tắt cùng ảnh chụp, xen kẽ lặp, ca overhead nhân tạo; cohort chỉ giám sát |
| R4-15 B3 thiếu quyền gọi A4 | P2 | A4 do người vận hành chạy trước; B3 chỉ đọc; thiếu ⇒ chặn |
| R4-16 bên tiêu dùng chưa có write set | P2 | Packet B4 (`packet_loop.py` + test) trước PR3; nhịp tim ở phiên điều phối là runbook thủ công, không sửa `doctor` |
| R4-17 chi phí canary chỉ là mảnh | P3 | §13 ghi rõ là tổng phụ 8 mảnh, phần còn lại ước sau |

Review lượt 3 (`wp1172-plan-r4-review-3`, trên `a6f7195`): 16 finding trước đóng; R4-08 đóng một phần; thêm R4-18.

| Finding | Mức | Xử lý ở bản sửa 4 |
|---|---|---|
| R4-08 (phần còn lại) bản ghi kích hoạt bị phát lại sau tắt/bật | P1 | A+1: vị từ bật đòi `updated_at` của biến (do máy chủ đặt) sớm hơn `created_at` của bản ghi OWNER; mọi lần ghi biến tiêu thụ thế hệ; không trạng thái nên sống qua khởi động lại; ca phát lại bắt buộc ở B4; đo trước rằng REST trả `updated_at` |
| R4-18 overhead chỉ đo một mảnh | P2 | A+5 phủ cả 8 mảnh × ≥ 3 cặp, ước lượng có trọng số, ca mảnh không đồng nhất, ngân sách ~10 giờ máy trong PR3; thiếu phủ ⇒ `khong_do_duoc` |

Review lượt 4 (`wp1172-plan-r4-review-4`, trên `b764ed6`): R4-08 và R4-18 đóng; mọi finding trước giữ đóng; thêm R4-19.

| Finding | Mức | Xử lý ở bản sửa 5 |
|---|---|---|
| R4-19 comment của OWNER sửa được, không phải uỷ quyền | P1 | Bản ghi uỷ quyền chuyển thành tệp git bất biến trong `ops/uy_quyen/` trên `master`, `merged_by` = OWNER, mốc `merged_at`; điều kiện tin = `master` cấm force-push/xoá (đo); thế hệ lớn nhất thắng, xoá không làm sống lại bản cũ; áp cho cả A+1 và B3; B4 đo thêm thứ tự đồng hồ, ghi không đổi giá trị và cấu hình bảo vệ trước khi đóng băng |

Review lượt 5 (`wp1172-plan-r4-review-5`, trên `c7cf78d`): R4-19 "vá sinh lỗi mới"; thêm R4-20…R4-24, cả năm cùng lớp
"uỷ quyền chủ kho do máy kiểm" — lớp ấy đã sinh finding qua R4-08, R4-11, R4-19, R4-20…R4-24. Theo bài học kho "cùng một
hình dạng lặp ba lần trở lên thì câu hỏi đúng là có nên làm việc này không", bản sửa 6 BỎ cả lớp thay vì vá:

| Finding | Mức | Xử lý ở bản sửa 6 |
|---|---|---|
| R4-20 merge thường của chủ kho không phải cấp quyền | P1 | Không còn kho uỷ quyền; A+1 chỉ SIẾT (`FULL`), nới chỉ bằng mã đã merge qua review |
| R4-21 REST không chứng minh người đẩy | P2 | Bỏ đường commit trực tiếp cùng cả kho uỷ quyền |
| R4-22 xoá bản mới làm sống bản cũ | P1 | Không còn thế hệ/bản ghi để sống lại |
| R4-23 bản miễn trên master làm H tụt | P2 | B3 không có ngoại lệ do máy; khẩn cấp = chủ kho tự chạy, có xác nhận TTY, không ghi master |
| R4-24 token đọc không đủ cho phép kiểm mới | P2 | B3 bảng năng lực chỉ Actions/Checks/Contents read; bảo vệ nhánh là điều kiện tiên quyết đo lúc bật + hằng tháng (Q7) |
| R4-08, R4-11, R4-19 (lớp uỷ quyền) | — | Đóng theo kiến trúc: không cơ chế nào nới cổng ngoài mã; bật lại sau `FULL` là quyền quản lý biến (Q9) |


## 12. Phương án loại

Giữ chín phương án của r3 §6. Thêm: (10) khôi phục nguyên r2 — nhắm khoản 4,7 % và đổi lấy M9; (11) sửa spec PR1 đang
chạy — hồi tố; (12) watchdog là một bước trong full audit — lượt vắng không chạy được bước của nó; (13) thêm trigger push
cho full audit chỉ để đủ canary — đổi tần suất và chi phí; (14) `pull_request_target` chạy mã PR để đọc công tắc — mở
quyền cho mã chưa duyệt; (15) kho uỷ quyền chủ kho do máy kiểm (biến có thế hệ, comment, tệp git do chủ kho merge) — ba
lượt review cho thấy lớp này tự sinh lỗ vì chủ kho bấm mọi merge.

## 13. Ngân sách và rủi ro

Làn B ước bốn packet nhỏ (B1–B4); mỗi packet 1–3 lượt thực thi, 1–3 review Codex, 1–3 CI PR Ubuntu, K7 khi chạm vùng M9, 0
Windows CI; B3 thêm một lần chạy Windows-local trên máy chủ kho (hoặc miễn). Canary A3 = 2 lượt full audit thêm; riêng 8 job mảnh ≈ 2 ×
13 282 = 26 564 s giây job (trung vị 8 mảnh `[B: M1.luot_du_8_manh_success.tong_giay_8_job_manh_moi_luot]`, CHƯA gồm job
registry, job gom, A4 và quan sát push — ước lại từ cùng tập lượt sau B1, không chạy thêm audit chỉ để ước). Chi phí thường xuyên: B1 vài giây mỗi lượt audit; B2 4 job nhỏ/ngày;
B3 vài lời gọi REST mỗi lần deploy. Rủi ro: B1 đụng workflow M9 (sensitive, chỉ siết); B3 có thể chặn deploy khi chưa có
audit trên H — chủ đích, có ngoại lệ của chủ kho. Không bổ sung nào tăng giây CI của `ci.yml`.
