# Packet nháp: CI-FULL-AUDIT-PIN-SHA r1

**Trạng thái:** draft ngoài repository, chưa có Issue ID, `spec_hash`, lease hoặc quyền ghi. Người soạn không được dùng tài liệu này để sửa source. Mốc khảo sát `master` `75feff232a5182aa2436e08228c5d864d866f0ec` (03-11-2026); base thi công phải đo lại khi cấp lease.

## 1. Mục tiêu và lựa chọn ưu tiên

Đây là lát thi công đầu tiên có hiệu lực trên toàn dự án sau khi land: mọi lượt `full_mutant_audit` hằng tuần hoặc dispatch đều chạy trên một source SHA duy nhất và không bị một lượt mới thay chỗ chỉ vì trùng concurrency group. Nó tăng độ tin cậy của bằng chứng đang dùng tại K7 mà **chưa nới M9**. Lịch Chủ nhật 02:17 giờ Việt Nam đã tồn tại; giữ nguyên.

Việc của #1143/PR #1155 (đường nhanh cho hồ sơ thụ động) đã landed, không làm lại. #1160 tối ưu lease refs, không giao với write set này. #1124 đang có lease r4 đến 04-11-2026 01:24:54Z cho `packet_loop.py`, `packet_loop_test.py` và tài liệu ADR/Protocol; Packet này không sửa các đường đó.

## 2. Contract dự kiến

| Trường | Giá trị dự kiến |
|---|---|
| Review class | `sensitive`, vì sửa `.github/workflows/**` và nguồn bằng chứng merge/release |
| Executor / reviewer | Định tuyến khi có authority; reviewer độc lập exact H, không kiêm executor |
| Write set | `.github/workflows/ci-dot-bien-du.yml`; `.claude/dev/ci_dang_ky_test.py`; đặc tả Packet này khi được đưa vào `ops/specs/` |
| Giới hạn | Dự kiến tối đa 3 tệp và 300 dòng thêm; nếu không đủ, tách successor thay vì cắt test |
| Phụ thuộc | Chủ kho duyệt WP/Packet Spec; kiểm lease/holder trên **đủ refs** cho write set; base đã chứa các Packet tác động tới workflow/registry; review kế hoạch P1/P2/P3 được đóng |
| Không đổi | M9/K7, required checks, danh sách mutant/ca, `fail-fast: false`, timeout, cron, nhánh và workflow bảo vệ master |

## 3. Thay đổi thiết kế

1. Mỗi run đặt `AUDIT_SHA` từ `github.sha` của **sự kiện**, kiểm mẫu OID 40 ký tự và ghi vào output một job prepare. Với schedule, nó là snapshot master lúc sự kiện được tạo. Với dispatch, người gọi phải chọn ref mà `github.sha` đúng ứng viên H. Không lấy `git rev-parse HEAD` sau khi master đã dịch rồi gọi đó là snapshot cũ.
2. Mỗi job audit checkout `ref: AUDIT_SHA` và in `git rev-parse HEAD`, tree, workflow definition OID (`github.workflow_sha` khi có), run ID/attempt. Nếu checkout hoặc đối chiếu OID hỏng, job đỏ. Job gom kiểm artifact `head`, manifest inventory và toàn bộ 8 mảnh đều khớp `AUDIT_SHA`, cùng mode full. K7 hiện kiểm run `head_sha`; nguồn H của artifact phải cùng H ấy.
3. Thêm concurrency group riêng `full-mutant-audit-<run_id>` (hoặc scheme duy nhất có kiểm chứng với actionlint và canary), `cancel-in-progress: false`. Không dùng chung group với `ci.yml`; không chỉ dùng SHA nếu nhiều run cùng SHA có thể làm pending bị thay chỗ. Không tăng số shard hay timeout trong Packet này.
4. Chốt cấu trúc workflow trong `ci_dang_ky_test.py`: cron, mode full, `fail-fast: false`, 8 shard, `needs`, checkout SHA, concurrency, và không có `continue-on-error` ở job/bước liên quan. Ghi test âm cho việc bỏ `ref`, dùng `github.ref` động, đổi group về ref/SHA, bật cancel, thiếu một shard hoặc lẫn mode targeted.
5. Lưu receipt máy đọc được gồm sự kiện, scheduled slot nếu là cron, event SHA, checkout SHA/tree, workflow definition SHA, run ID/attempt, status từng job, artifact ID/hash và outcome. Nếu GitHub không cung cấp `workflow_sha` tin cậy qua context trên runner, ghi `not_measured` và lấy workflow definition identity từ REST/GraphQL ở successor; **không** tự xem checkout SHA là chứng minh definition SHA.

## 4. Acceptance và phản chứng

| ID | Phép đo đạt | Phép đo đỏ |
|---|---|---|
| A1 | `actionlint` workflow, registry selftest, test workflow mới, syntax YAML đều đạt trên H; baseline tests/IDs không giảm. | Cửa nào `skipped`/`not_run`, ca mới xanh trên workflow cũ khi nó cần bắt lỗi. |
| A2 | Lượt `workflow_dispatch` trên nhánh ứng viên H: run `head_sha=H`, checkout của mọi job và `head` của mỗi artifact bằng H; 10/10 job hoàn tất `success`; K7 trên H vẫn ra rc 0. | Một job/mảnh sai SHA, thiếu attempt hoặc artifact, `cancelled`/`timed_out`/`failure`/`not_run` mà K7 hoặc receipt kết luận xanh. |
| A3 | Canary cô lập: hai dispatch khác run ID cùng SHA, rồi một push master mới khi audit đầu còn chạy; không run nào bị hủy/thay chỗ do concurrency group. Ghi run IDs, queue/start/end và số job chạy thật. | Chỉ có run `pending`/`cancelled`, hoặc ba trigger mà ít hơn ba receipt kết thúc; `cancel-in-progress: false` không được coi là đủ bằng chứng. |
| A4 | Đọc lại definition OID riêng với source OID và ghi provenance; mọi lần kiểm lại sau khi H đổi đều dùng receipt mới. | Dùng một run `success` của H cho H+1, hoặc definition identity không đo được mà báo đã khớp. |
| A5 | Windows theo M3/spec trên `tra-luat-win` nếu required, exact H; M9 full audit trên H; CI PR và `kiem-merge` K0–K7 đạt trước khi bỏ draft. | Tự miễn Windows/full audit, dùng run khác H, hoặc `fail-fast`/skip làm mất fail IDs. |
| A6 | Review độc lập P0/P1/P2/P3 = 0 hoặc finding P3 được đóng/miễn đúng ADR-0060; duyệt và land theo protocol. Hậu merge CI master và readback receipt đạt. | Chỉ dựa vào self-review hoặc run PR để claim đã áp dụng toàn dự án. |

## 5. Rollback và phần kế tiếp

Nếu audit mới làm mất lượt chạy, tạo artifact sai H hoặc gây queue starvation rõ rệt, không dùng receipt ấy cho K7/release; quay workflow về definition đã được duyệt bằng Packet/authority hợp lệ, giữ đầy đủ run đỏ, rồi đo lại exact SHA bị ảnh hưởng. Không xóa lịch sử. Successor riêng sẽ làm watchdog độc lập phát hiện lịch vắng, outcome schema, targeted selector và đối chứng fast/full; chỉ sau đó mới xét nới M9 toàn dự án.

## 6. Việc còn phải hoàn tất trước code

- Reviewer độc lập đã xác nhận kế hoạch r2 đóng 1 P1, 4 P2, 1 P3 ở cấp kế hoạch; điều này **không** thay review exact H cho Packet này. Trước khi đóng băng spec, đối chiếu lại phạm vi PR0 trong kế hoạch r2 và các lease mới.
- Đo holder đủ refs cho 3 đường write set, xác định Issue ID/`spec_hash`/base SHA và cấp lease generation đúng provider/surface. Hiện **chưa có** các mục ấy.
- Chốt với chủ kho mức concurrency tối đa vì mỗi run có thể có 8 shard song song; unique group bảo vệ pending nhưng không tự kiểm soát tài nguyên. Kiểm thực tế runner quota/queue từ baseline.
