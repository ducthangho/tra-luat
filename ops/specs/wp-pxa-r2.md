# WP-PXA r2 — Truyền và kiểm culture cho tiến trình con phản chứng của ProximaActivation.Tests (đặc tả đóng băng)

- **Packet:** #1401 (con của #1319). Revision 2. Review Class `sensitive`.
- **Căn cứ:**
  - Finding **P2** của Codex connector trên PR #1378, head `953ba9d8c32e2e6867956a6f8ed6a90a4137ecb1`: review `5972629197`, comment `4626897634`, `tests/ProximaActivation.Tests.ps1:216`.
  - Nội dung finding: tiến trình con phản chứng không nhận culture của tiến trình cha, nên khi cha chạy `tr-TR` tường minh trên máy có culture mặc định khác, 6 CX được ghi `killed` mà không chứng minh chúng chạy dưới `tr-TR`. Trong khi đó `ops/acceptance/wp-pxa/RESULTS.md` khai "6 CX, tr-TR".
  - Theo ADR-0060 M1, một P2 còn mở chặn merge.
  - Phiên điều phối đã đối chiếu trên mã thật: `ProximaInstall.Tests.ps1` dòng 11–21, 286–287 và 330–332 làm đúng việc này; `ProximaActivation.Tests.ps1` không có tham số `-Culture`, và `Invoke-Counterexample` (dòng 211–216, 251–258) không truyền hay kiểm culture.
- **Ranh giới:**
  - Chỉ sửa `tests/ProximaActivation.Tests.ps1`.
  - Không đổi `scripts/ProximaActivation.psm1`, các test khác, hay bất kỳ ca PA/CX nào: id, nội dung và lý do kỳ vọng giữ nguyên.
  - Không LIVE, không inference, không đụng Proxima đã cài.

## 1. Thay đổi
Làm giống `ProximaInstall.Tests.ps1`:
1. **Tham số `-Culture`** (string, tuỳ chọn).
   - Có giá trị thì trước mọi việc khác đặt `CurrentCulture`, `CurrentUICulture`, `DefaultThreadCurrentCulture` và `DefaultThreadCurrentUICulture` bằng `GetCultureInfo($Culture)`.
2. **Báo cáo:**
   - thêm `ui_culture`, ghi lúc bắt đầu;
   - thêm `culture_at_end`, ghi ngay trước khi ghi report.
   - `culture` giữ nguyên nghĩa: culture lúc bắt đầu.
3. **Tiến trình con phản chứng:**
   - Luôn nhận `-Culture <culture của cha>` khi chuỗi đó khác rỗng.
   - Mỗi bản ghi phản chứng thêm `child_culture`.
   - Trước khi cấp `killed`: nếu `culture` **hoặc** `culture_at_end` của con khác `culture` của cha thì ném lỗi `provenance` (bản ghi thành `not_credited`, ca CX thành `setup_error`, rc 2). Phép kiểm này nằm cạnh phép kiểm băm và edition sẵn có.

## 2. Kiểm
- **Parse:** parser PS 7 và PS 5.1 đều cho 0 lỗi.
- **Chạy trên Desktop** (test Windows tập trung):
  - lấy hai khoá host;
  - cây `.agents/skills/proxima-control` chép từ commit vá, mọi tệp phải khớp băm blob git;
  - `-Culture tr-TR -Counterexamples` trên PS 7 và trên PS 5.1;
  - kỳ vọng mỗi bản **36/36**, `failed`/`skipped`/`setup_error`/`id_errors` rỗng, rc 0;
  - cả 6 bản ghi CX có `verdict=killed` và `child_culture=tr-TR`; `culture` và `culture_at_end` của cha đều là `tr-TR`.
- **Phản chứng của chính bản vá:** trên bản sao tạm của harness, bỏ đối số `-Culture` truyền cho con, rồi chạy `-Culture tr-TR -Counterexamples` trên PS 7.
  - Chỉ ghi được khi culture mặc định của máy **khác** `tr-TR` (phải đo và ghi lại).
  - Kỳ vọng rc 2 và cả 6 CX `not_credited` với lý do lệch culture.
  - Nếu culture mặc định là `tr-TR` thì ghi phản chứng là `not_measured`, không bịa.
- Bằng chứng đóng băng: zip + MANIFEST + quét secret.

## 3. Vai, ngân sách, write set
- **Executor:** phiên điều phối (vá hẹp một tệp test). Reviewer phải độc lập.
- **Review:**
  - Lượt offline đúng head mới (K4 ADR-0060) **chưa được cấp ngân sách**. PR #1378 đã vượt trần lời gọi Codex mặc định (E2, ADR-0067).
  - Lượt này chờ chủ kho cấp, hoặc chủ kho tự audit.
  - Connector Codex sẽ review lại head mới khi được kích hoạt.
- **Native:** Desktop 1 lượt (PS 7 + PS 5.1 + phản chứng), chạy lại 1 lần khi lỗi dựng.
- **Write set** (không glob):
  - `.agents/skills/proxima-control/tests/ProximaActivation.Tests.ps1`
  - `ops/specs/wp-pxa-r2.md`
  - `ops/leases/wp-pxa-r2-g1-executor.yaml`
  - `ops/acceptance/wp-pxa/RESULTS.md`
