# ĐẶC TẢ ĐÓNG BĂNG — CAI-CONG-CU-SIGPIPE revision 1

Packet Issue: #675 · chỉ thị: https://github.com/ducthangho/tra-luat/issues/675#issuecomment-5883033056
Immutable acceptance baseline: `cd23c7dbc7833d64a8e87e8ffd94f194c18e0060` (origin/master lúc soạn).

## 1. Objective

Không còn pipeline nào kiểu "người đọc thoát sớm" (`| head …`) chạy dưới `set -e` + `pipefail`
trong các script `ops/*.sh` do CI gọi hoặc do quy trình review gọi. Việc trích dòng đầu phải dùng
khai triển tham số của bash, không dùng pipeline. Kèm theo một phép đo phản chứng chạy được,
cho kết quả ĐỎ trên bản cũ và XANH trên bản vá.

## 2. Bằng chứng nền (phiên điều phối, 29-09-2026, bash 5.2.21, Linux 4 lõi)

- Cơ chế (strace): builtin `printf '%s\n' "$X"` gọi **một `write()` cho mỗi dòng**, nên đầu vào
  từ hai dòng trở lên đã có cửa sổ đua với `head`. Khi `head` thoát trước lần ghi sau thì `printf`
  ăn SIGPIPE, pipefail đẩy 141 lên, và `set -e` giết script mà không in gì.
- Đo ngẫu nhiên với đầu vào thật (`cong_cu.py cai-lenh actionlint` in 2 dòng), 3000 lần, có tải
  CPU nền: dạng `cai_cong_cu.sh:64` hiện tại hỏng **2/3000**. `${DAU_RA%%$'\n'*}` hỏng **0/3000**.
- Đo tất định với đầu vào 20.000 dòng: dạng hiện tại **10/10 rc=141**, khai triển tham số **0/10**.

## 3. Liệt kê (đã đo; executor PHẢI đo lại, không nhận lời)

| script:dòng | dạng | `set -e`+pipefail | kết luận |
|---|---|---|---|
| `ops/cai_cong_cu.sh:64` | `printf … \| head -1` | có | VÁ |
| `ops/cai_actionlint.sh:188` | `printf … \| head -1 \| tr -d '\r'` | có | VÁ |
| `ops/dung_goi_review.sh:163` | `printf '%s' … \| head -1 \| tr -d '\r'` | có | VÁ |
| `ops/dung_goi_review.sh:179` | `… \| tr \| grep -m1 … \|\| true` | có | `\|\| true` cứu, giá trị đúng. Executor chọn giữ hoặc đổi, và ghi lý do |
| `ops/cai_cong_cu.sh:67,71` | `\| tail …` | có | `tail` đọc hết đầu vào, không dính. Giữ nguyên |
| `ops/kiem_trang_quyet_dinh_test.sh:34,37` | `grep \| head -1` | KHÔNG `set -e` | không thoát, giá trị đúng. Ngoài write set |
| `ops/don_ref_chot_test.sh:327,333` | `printf \| grep -q` trong `if !` | KHÔNG `set -e` | 141 cũng ra nhánh "đã thấy", tức đúng ngữ nghĩa. Ngoài write set |

Executor phải tự quét lại **mọi** `ops/*.sh`. Quét không chỉ tìm `head` mà mọi lệnh có thể thoát
trước khi đọc hết đầu vào: `head`, `grep -q`, `grep -m`, `sed …q`, `awk …exit`, `read`. Nếu thấy
một điểm DÍNH nằm ngoài W1–W3 thì DỪNG và báo (S1). Không được tự mở write set.

## 4. Write set (exact)

- W1 `ops/cai_cong_cu.sh`
- W2 `ops/cai_actionlint.sh`
- W3 `ops/dung_goi_review.sh`
- W4 `ops/do_sigpipe.sh` (mới)

NGOÀI write set, tuyệt đối không chạm (lease #668 đang giữ): `ops/cong_cu_test.py`,
`.github/workflows/ci.yml`, `.claude/dev/ci_dang_ky_test.py`. Việc nối W4 vào CI là
**packet kế nhiệm**, mở sau khi #668 land.

## 5. Ràng buộc bản vá

- Mỗi điểm vá dùng khai triển tham số, ví dụ `X="${Y%%$'\n'*}"`, rồi bỏ CR bằng `"${X//$'\r'/}"`
  hoặc `"${X%$'\r'}"`. Hai cách bỏ CR phải cho CÙNG kết quả với bản cũ trên mọi đầu vào ở §6 (a).
- Giữ idiom chú thích của từng tệp: chú thích ASCII không dấu, ngắn, nêu bằng chứng
  (`r<số>`/phép đo) và lý do.
- Không đổi hành vi nào khác. `git diff` của W1–W3 chỉ được chạm đúng các dòng ở §3 và chú thích đi kèm.

## 6. W4 `ops/do_sigpipe.sh` — hợp đồng

- Chạy được bằng `bash ops/do_sigpipe.sh [--lan N]` trên Linux. Tự đặt `set -euo pipefail` ở
  vỏ ngoài nhưng đo từng phép trong tiến trình con.
- **Trích dòng đang đo TỪ CHÍNH script W1–W3** (theo mẫu/số hiệu biến), KHÔNG chép lại. Trích
  không thấy thì ĐỎ (`KHÔNG ĐO ĐƯỢC`, mã khác 0), không được bỏ qua êm.
- Có ba loại phép đo:
  (a) **tương đương**: dòng đã trích và dạng pipeline cũ (dựng ngay trong W4 làm đối chứng) cho CÙNG
      giá trị trên một tập đầu vào: 1 dòng · nhiều dòng · có CR/CRLF · rỗng · dòng đầu rỗng · không
      có LF cuối.
  (b) **tất định**: đầu vào ≥ 20.000 dòng, chạy trong `bash -c 'set -euo pipefail; …'`. Dạng cũ
      phải cho rc=141 ở **mọi** lần, dạng trích từ script phải cho rc=0 ở **mọi** lần.
  (c) **tự kiểm có răng**: nếu một đột biến đưa dòng W1 về lại dạng pipeline (trên BẢN SAO TẠM,
      không bao giờ trên tệp thật) thì (b) phải ĐỎ.
- In một dòng tổng kết có bằng chứng dương dạng `N/N` (hai số BẰNG NHAU), và in rõ điều kiện đo
  (phiên bản bash, số lõi, số lần).

## 7. Nghiệm thu

- A1: `bash ops/do_sigpipe.sh` trả rc=0 trên bản vá, với tổng kết `N/N`. Trên baseline (W1–W3 cũ,
  W4 mới) phải có ít nhất một phép (b) ĐỎ cho mỗi điểm W1–W3, tức mỗi điểm có răng riêng.
- A2: `python ops/cong_cu_test.py` N/N (chế độ mặc định; ghi số và thời gian). `t5` chạy lặp
  ≥ 200 lần bằng cách gọi thẳng `cai_cong_cu.sh actionlint` với môi trường giống t5, cho 0 lần rc=141.
- A3: `python ops/bash_nen.py quet --root .` rc=0 · `actionlint` trên `.github/workflows/*.yml`
  không phát sinh delta so baseline · `shellcheck` (nếu có) trên W1–W4 không phát sinh delta so
  baseline · `python -m ruff check --select F` không đổi (packet không sửa `.py`).
- A4: `python .claude/dev/ci_dang_ky_test.py` (chế độ mặc định) không đỏ vì packet này, tức delta
  so baseline = 0.
- A5: cross-review Codex độc lập, lặp tới khi 0 P1 / 0 P2 / 0 P3. Verdict đăng lên #675.

## 8. Điều kiện dừng

- S1: cần chạm đường ngoài W1–W4 thì DỪNG, handoff.
- S2: lease hết hạn thì ngừng ghi, handoff §7.
- S3: cùng một hình dạng finding lặp ≥ 3 lần thì hỏi chủ kho.
- S4: không tự merge/land/approve, không force-push, không deploy.
- S5: diff > 150 dòng thêm thì DỪNG, hỏi chủ kho.
