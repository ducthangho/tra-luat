from pathlib import Path
p=Path('VERDICT.md'); s=p.read_text()
summary='''Hoàn tất cross-review PR #1058 lượt 1: **request_changes — 0 P0, 0 P1, 1 P2, 1 P3**. Các cổng đều qua, không có delta lỗi so base; byte/hashes, trường định lượng của ba biên nhận và hàng README khớp nguồn. Hai finding nằm ở lời khai của hồ sơ land. Lệnh và output ở các mục đo bên dưới và `evidence/`; script tái hiện đều nằm ngoài `cay-kho/`. Không cấp quyền merge/land.

Finding (hai lớp, hai biểu hiện):

- [P2] uy-quyen-land-suy-tu-merge: `ops/land/pr1047-wp1045-land-evidence.yaml:34` — `PYTHONDONTWRITEBYTECODE=1 python3 finding_checks.py authorization` — output `authorization_claim="uy quyen land la hanh dong merge cua chu kho."`, trong khi chính điều kiện (5) của tệp là `uy quyen land neo SHA: CHUA DAT` và yêu cầu mở lại là `chu kho ghi duyet ben neo 2014602`. Readback PR chỉ có `merged=true`, `merged_by=ducthangho`, head `2014602…`; comment 6529094452 ghi hộ nâng trần và điều kiện merge. Danh tính người bấm/duyệt land exact-SHA: **KHÔNG ĐO ĐƯỢC** từ hai nguồn này (dòng 35 cũng tự giới hạn như vậy). Câu cuối dòng 34 biến bằng chứng thao tác thành bằng chứng ủy quyền ngay trong trường authorization, trái mục đích tách hai vai của protocol §7 và điều kiện cuối hồ sơ. — Hướng vá: bỏ hoặc đính chính câu này thành “readback chỉ chứng minh thao tác merge; chưa có nguồn duyệt land bền neo exact SHA”, đồng bộ với điều kiện (5); giữ `landed: false`, không sửa readback. Kiểm đóng bằng cùng lệnh: lời giải thích authorization và điều kiện mở lại phải cùng ghi thiếu bằng chứng duyệt; việc sửa văn xuôi không được đổi kết luận merged hay tạo quyền land.

- [P3] nhan-windows-ke-ca-job-skipped: `ops/land/pr1047-wp1045-land-evidence.yaml:42` — `PYTHONDONTWRITEBYTECODE=1 python3 finding_checks.py labels` — output phản ví dụ duy nhất: `id=124215501550`, `name=gate-cong-cu-gop`, `conclusion=skipped`, `labels=[]`, `runner_id=null`; `executed_gate_jobs=14`, tổng `15 success / 1 skipped`. Vì vậy câu **measured** “moi job gate* nhan windows-latest” rộng hơn nguồn, dù số skipped ở cùng dòng đã được ghi đúng. — Hướng vá: ghi “14 job gate* đã chạy có nhãn windows-latest; gate-cong-cu-gop skipped, không có runner/nhãn”; giữ `chuan-bi` Ubuntu và tổng 15/1. Kiểm đóng: đối chiếu tất cả gate* đã chạy với nhãn, tách job skipped; không sửa JSON hay nâng skipped thành Windows execution/pass (protocol §10.2.3).
'''
s=s.replace('Đang đo; verdict tạm thời, chưa kết luận finding. Bản cuối sẽ thay đoạn này khi hoàn tất. Không cấp quyền merge/land.',summary)
s=s.replace('Cập nhật 1 — cổng đã chạy xong; chưa chốt verdict:', 'Cập nhật 1 — kết quả cổng:')
a=s.index('Finding xác nhận bước đầu:'); b=s.index('Cập nhật 3 —',a)
s=s[:a]+'Phản ví dụ nhãn job đã được ghi tăng dần ở bước này; kết luận và hướng vá nằm trong finding `nhan-windows-ke-ca-job-skipped` ở đầu tệp.\n\n'+s[b:]
s+='''
Cập nhật cuối — trạng thái, giới hạn và toàn vẹn:

- `PYTHONDONTWRITEBYTECODE=1 python3 provenance_audit.py` → `land_status` có `landed=false`, `assurance_81=CHUA_DAT`; `python3 audit.py receipts` → cả ba `sandbox_state=KHONG_DO_DUOC`. Giữ hai trạng thái này phù hợp bằng chứng thiếu sandbox và thiếu Checkout / Workflow definition / Gate output. Hai snapshot in_progress rồi success mô tả hai thời điểm, không mâu thuẫn. Review `approve`/`cross_approved` ở receipt và README không được dùng để suy §8.1 đã ĐẠT; cả receipt lượt 3 và hồ sơ đều ghi rõ giới hạn ấy. Câu suy ủy quyền từ merge vẫn phải sửa như finding P2.
- `git diff --name-only afc82f6 HEAD` → 51 tệp, ngoài `ops/reviews/**`/`ops/land/**` = `[]`; đối chiếu byte `git diff afc82f6 HEAD` với `DIFF.patch` → `True`, SHA-256 `a8e3d2e479804d07751849d0dc4f74a2ae4c7d5613473833a8a3a9470a1ed8da` (`evidence/final-state.json`).
- Kiểm cuối `git rev-parse HEAD HEAD^{tree}` → head `5dd347c67da680099e292acf02da7e363a0559bd`, tree `7176a9306859b0b772d49d6ddf9d5ddca0cf8167`. `git status --porcelain=v1 --untracked-files=all --ignored`, `git diff --exit-code`, `git diff --cached --exit-code` → cả ba rc0, stdout/stderr rỗng. Không có thay đổi nội dung checkout quan sát được ở mốc cuối; chỉ cấu hình `core.abbrev=7` theo yêu cầu.

**KHÔNG ĐO ĐƯỢC** trong review này:

| Phần | Lệnh/nguồn đã đối chiếu và giới hạn |
|---|---|
| Trạng thái GitHub thật, tính xác thực/đầy đủ của REST readback, giờ thực hiện GET 23:40/04:05 và lỗi GraphQL 403 | `python3 provenance_audit.py` chỉ đọc tệp được cung cấp; các `created_at`/`updated_at` là trường trong JSON, không chứng minh thời điểm tải. Không có phép gọi mạng. |
| Người thật bấm merge, phiên dùng credential, approval exact SHA | `python3 finding_checks.py authorization` chỉ thu được actor tài khoản và comment ghi hộ; không suy thêm danh tính/quyền. |
| Checkout CI, exact workflow-definition OID/blob/hash của run và output/rc/marker từng gate | `python3 provenance_audit.py` đo run/jobs/steps JSON; không có bộ provenance đủ bốn mốc §10.2.2. `head_sha` và nhãn runner không thay ba mốc còn thiếu. |
| Số ca CI 312/312, 255/255, đột biến 502/502, 410/410; log publish lease rc9 | `rg -n 'Thuat_lai|thuat_lai|khong luu' cay-kho/ops/land/pr1047-wp1045-land-evidence.yaml` → các dòng 43, 84–85 đã đánh dấu thuật lại/không lưu log. Không tái chứng nhận các số này từ jobs JSON. |
| Đầy đủ ref và người giữ lease tại 00:23 lịch sử | `python3 provenance_audit.py` đối chiếu snapshot 713/713, NGƯỜI_GIỮ 0 ×3; `git for-each-ref --format='%(refname)' refs/remotes/origin` hiện có 717 nhánh khi loại `/HEAD` (`evidence/final-state.json`). Không dùng tập ref hiện tại để xác nhận tập remote lịch sử hoặc tuyên bố ai đang giữ ở hiện tại. |
| Thực thi lại phép đo trong các VERDICT gốc, toàn bộ lịch sử sandbox/context độc lập và argv CLI nguyên văn | `python3 audit.py bytes receipts` xác minh bản sao, run JSON, hash và những trường có thể đo. `git ls-tree -r` của ba thư mục handoff chỉ có 6 tệp/lượt; không có `evidence/`. Receipt/README đã nêu thiếu script, checkout không cưỡng chế read-only và sandbox `KHONG_DO_DUOC`. Các kết quả bên trong verdict gốc chỉ được đối chiếu là lời của nguồn, không tự nhận đã tái chạy. |

Ngưỡng yêu cầu là không còn P0/P1/P2/P3; hai finding trên khiến PR chưa đạt ngưỡng. Kết luận chỉ áp dụng commit đã ghi ở dòng 2.
'''
p.write_text(s)
