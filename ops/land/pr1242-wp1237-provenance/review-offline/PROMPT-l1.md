# Cross-review wp1237 r1 (CAI-ACTIONLINT-RETRY) — lượt 1, reviewer openai_codex, read-only với kho

Bạn là reviewer ĐỘC LẬP. Bạn KHÔNG sửa kho nguồn. Bạn được ghi trong thư mục sandbox hiện tại.

## Hiện vật (thư mục hiện tại)
- `SPEC.md` — đặc tả đóng băng, sha256 b0e12304e0c591db6e2130454ed6a72c1458d4541b1312037935b0ccbb210666.
- `LEASE.yaml` — lease (write_set, base_sha, review_class sensitive).
- `cay-kho/` — clone đầy đủ, HEAD detached ở reviewed_sha `43258fbe43d2b1508cdb0a00dc1ba436f28968c5`,
  base `fe84620f897913c7f6c2ce5a0c7316a49655e82f`. `git -C cay-kho diff fe84620f HEAD` là diff.
- `diff.patch`, `numstat.txt` — cùng diff.
- `mutation_runner_executor.py` — bảng đột biến executor đã chạy (REPO trỏ kho của executor; sửa REPO
  thành `cay-kho` tuyệt đối nếu muốn chạy lại). Executor khai: 5/5 giết, mỗi cái đúng vế đích
  (retry_ve_2→D1, bo_retry_all_errors→D2, bo_kiem_regex→D4, bo_doi_chieu_bam→D5, doi_bam_sau_giai_nen→D5).

## Việc
1. Đối chiếu diff với SPEC M1–M5 và bảng nghiệm thu D1–D6, từng mục. Nói rõ mục nào khớp/lệch.
2. CHẠY: `cd cay-kho && python3 ops/lease_publish_test.py --chi-ca=t237` (cần đọc `lease_publish: 1/1 đạt`),
   và `--chi-ca=t35`, `--chi-ca=t37`, `--chi-ca=t38`. `shellcheck ops/cai_actionlint.sh` nếu có.
   Trong môi trường có proxy, ca tự đặt NO_PROXY; nếu sandbox chặn loopback thì ghi KHÔNG ĐO ĐƯỢC.
3. Đo răng: chạy lại bảng đột biến trên BẢN SAO TẠM (không sửa `cay-kho`), và nghĩ thêm ít nhất 3 đột
   biến KHÁC của `ops/cai_actionlint.sh` mà t237 nên giết (ví dụ: bỏ kiểm khoảng MAX_TIME, bỏ
   `--retry-max-time`, đổi mã 13 thành 4, bỏ `--retry-delay`, thông điệp loi 4 mất số lần thử). Ghi đột biến
   SỐNG riêng. Đột biến chết vì lỗi KHÁC (cú pháp shell, ngoại lệ Python ngoài `bang`) là tín dụng giả.
4. Săn lỗi độc lập (≥ 6 hướng, mỗi hướng có LỆNH + OUTPUT THẬT): ví dụ bash tràn số / số 0 đứng đầu
   (`08`, `0099`), `set -u` với `${!nut}`, giá trị rỗng tường minh, curl cũ không có `--retry-all-errors`
   (Git Bash Windows), tệp ra một phần còn lại sau retry có lọt qua cổng băm không, `--retry-max-time` ngắt
   giữa lần tải đang chạy, hành vi đường `AL_GOI` (không tải) có đổi không, stdout của đường ăn được (M5),
   độ chập chờn của ca (chạy t237 3 lần), máy chủ test có thật sự giữ trạng thái không.
5. Kiểm phạm vi: chỉ 2 tệp trong write_set, ≤ 250 dòng thêm, `ops/lease_publish_test.py` chỉ THÊM
   (không sửa ca có sẵn), không đụng workflow.

## Đầu ra
Ghi `VERDICT.md` trong thư mục hiện tại, GHI SỚM và cập nhật dần (đừng đợi cuối mới ghi). Dạng:

```
verdict: approve | changes_requested | blocked
reviewed_sha: 43258fbe43d2b1508cdb0a00dc1ba436f28968c5

## BẢNG ĐỐI CHIẾU SPEC (M1–M5, D1–D6)
## BẢNG ĐỘT BIẾN (của executor + của bạn; GIẾT/SỐNG/TÍN DỤNG GIẢ, vế đỏ)
## BẢNG SĂN
HƯỚNG n: ...
  giả thuyết / lệnh / output / kết luận: LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC
## FINDINGS
### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG / VẤN ĐỀ / ĐÃ THỬ NGHIỆM / ĐỘ TIN / gợi ý vá (HINT, không bắt buộc)
```
`changes_requested` chỉ khi có finding P0–P2 có bằng chứng chạy được. P3 không chặn.
