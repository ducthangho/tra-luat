## Findings

### 1. `t34` ràng theo tệp, không ràng installer với selftest trong cùng job — P2

**Bằng chứng đo được**

Trên bản sao tạm, tôi đổi installer trong job `gate` thành:

```yaml
run: echo ops/cai_actionlint.sh
```

và thêm job khác:

```yaml
installer-o-runner-khac:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - env:
        AL_VER: 1.7.7
      run: bash ops/cai_actionlint.sh
```

Sau đó chạy trực tiếp:

```text
python3 ops/lease_publish_test.py
actionlint .github/workflows/ci.yml
```

Kết quả nguyên văn:

```text
lease_publish: 38/38 đạt
JOB_SPLIT_RC=0 ACTIONLINT_RC=0
```

Job chạy selftest không nhận `actionlint`; installer ở job khác không truyền filesystem hay `PATH` sang runner của nó. Phản chứng `echo` cũ khi áp cả hai workflow đã được đóng:

```text
lease_publish: 37/38 đạt
ECHO_RC=1
```

**Invariant bị cắt**

Mỗi job chạy `lease_publish_test.py` phải được cấp `actionlint` trên chính runner của job đó. Sự hiện diện của installer ở một job khác trong cùng tệp không đáp ứng nghĩa vụ này và mở lại regression `32351892214`.

**Gợi ý vá**

Trong `t34`, duyệt từng `(workflow, job)`:

- Nếu các step của job nhắc `lease_publish_test.py`, chính danh sách step của job đó phải có installer canonical.
- Nên yêu cầu installer đứng trước selftest theo thứ tự step.
- Thêm mutation job A/job B ở trên.

---

### 2. Tên gói không có dấu chấm làm phép dựng tên cục bộ chứa cả đường dẫn — P2

**Bằng chứng đo được**

Tôi tạo một tar hợp lệ chứa binary in `1.7.7`, sao chép thành tệp `nodot`, tính đúng SHA-256 rồi chạy:

```text
AL_VER=1.7.7 \
AL_GOI=/tmp/platx4-review.WB7uAg/nodot \
AL_DICH=/tmp/platx4-review.WB7uAg/d-nodot \
AL_NEN=Linux \
AL_SHA256=<băm đúng> \
bash ops/cai_actionlint.sh
```

Kết quả nguyên văn:

```text
nodot rc=5 out=cp: cannot create regular file '/tmp/platx4-review.WB7uAg/d-nodot/goi_giai_nen.WB7uAg/nodot': No such file or directory cai_actionlint: khong chep duoc goi vao '/tmp/platx4-review.WB7uAg/d-nodot'
```

Nguyên nhân:

```bash
DUOI_GOI="${TEN_GOI##*.}"
```

Nếu toàn bộ đường dẫn không có `.`, phép mở rộng trả lại toàn bộ `TEN_GOI`, gồm các dấu `/`. Trong bản trước, gói này đi nhánh tar mặc định và không cần phần mở rộng.

**Invariant bị cắt**

`AL_GOI` được mô tả là đường dẫn tới một gói có sẵn, không yêu cầu tên phải có phần mở rộng. Một tar hợp lệ không được thất bại chỉ vì tên tệp.

**Gợi ý vá**

Chọn tên cục bộ từ loại archive thay vì lấy suffix tùy ý từ đường dẫn:

```bash
case "$TEN_GOI" in
  *.zip) GOI_CUC_BO="goi_giai_nen.zip" ;;
  *)     GOI_CUC_BO="goi_giai_nen.tar.gz" ;;
esac
```

Thêm ca dương với `AL_GOI=<đường>/nodot`.

## Xác minh ba finding lượt 1

Cả ba finding cũ đã được đóng trong những ca ban đầu:

- Mutation hai workflow sang `echo`: `37/38`, rc `1`.
- `AL_VER=1x.2y.3z`: rc `2`.
- Giá trị chứa newline: rc `2`.
- Bản chưa có băm ghim, với URL cố ý không dùng được:

```text
nopin rc=8 out=cai_actionlint: khong co bam de doi chieu goi 'actionlint_9.9.9_linux_amd64.tar.gz'...
```

Không xuất hiện lỗi tải, xác nhận dừng trước tải.

- Thiếu cả hai công cụ băm:

```text
nohash rc=8 out=cai_actionlint: KHONG DO DUOC bam: thieu ca `sha256sum` lan `shasum`...
```

- Băm sai:

```text
mismatch rc=9 out=cai_actionlint: bam goi KHONG KHOP...
```

- Băm đúng:

```text
match rc=0 out=/tmp/platx4-review.WB7uAg/d-ok
```

## Các hướng §3 không thành finding

- `GOI_CANON` cố ý chặt: `set -e; bash ...` hoặc `bash -lc ...` bị từ chối; `env:` và `shell:` ở YAML không làm đổi thân `run` nên vẫn được nhận. Đây là chính sách chuẩn hóa có thể chấp nhận. Cách giả `bash` qua `PATH` đòi một step/action trước đó đã có khả năng chạy mã; không làm rộng đáng kể mô hình đe dọa.
- `AL_SHA256` là override thật, nhưng workflow không ánh xạ input hay `vars.*` vào nó. Người sửa được workflow/script đã có thể bỏ hẳn cổng; action trước đó bị chiếm quyền cũng đã chạy mã. Vì vậy override chủ yếu mở giao diện offline/test, không phải finding mới trong mô hình hiện tại.
- Gói hỏng truyền đúng rc:

```text
badtar rc=5
gzip: stdin: not in gzip format
...
cai_actionlint: giai nen tar that bai
```

Subshell không nuốt mã thoát.

- `AL_DICH=/sys` cho lỗi `cp` đúng rc `5`; symlink tới gói ngoài cho rc `0`; `AL_GOI` đúng bằng `$AL_DICH/goi_giai_nen.gz` cho rc `0`. `mkdir -p` thất bại trước `cp` trả rc `1`; đây là hành vi đã có trước phần vá `cp`, không phải regression mới. Không thể tạo đĩa đầy thật trong sandbox nên hướng đó vẫn là giả thuyết chưa đo.
- Trên POSIX hiện tại, cả `t36` và `t38` thật sự chạy nhánh POSIX và suite đạt. Tuy nhiên còn các `return` sớm có thể xanh rỗng: đáng chú ý `t19` bỏ qua nếu không tạo được symlink, `t23` bỏ qua khi thiếu thư mục lease, và `t32` trả sớm nếu không lấy được thân bước. Chúng có trước diff lượt này và không làm sai kết quả trên môi trường đã đo.
- `t37` phủ băm đúng, sai, gói lạ không override và bản chưa ghim; nó chưa tự dựng môi trường thiếu công cụ băm. Tôi đã đo độc lập trạng thái thiếu công cụ và nhận đúng rc `8`, nên đây là thiếu ca regression chứ không phải lỗi hành vi hiện tại.
- Lời khai về nguồn băm đúng: các hằng SHA-256 nằm trực tiếp trong script, không có chữ ký hay trust root độc lập. Nó chống drift/thay thế sau thời điểm ghim, không chứng minh artefact gốc sạch. Đây là giới hạn đã khai, không phải finding mới.

## Bằng chứng nền

```text
lease_publish: 38/38 đạt
SUITE_RC=0 ACTIONLINT_RC=0
```

Diff đúng bốn tệp write set. `doc-claims-check --strict` trả rc `2` trên cả head và archive của base:

```text
HEAD_DOC_RC=2 BASE_DOC_RC=2
```

Không có đường đọc `N/N` Windows trong sandbox; tôi không khai đã đọc nó. Bằng chứng packet chỉ hỗ trợ kết luận bước selftest chuyển `failure → skipped → success`, trong đó bản vá tar chỉ có bằng chứng Windows từ `2348710b`.

Lưu ý mỏ neo: `909d3e…` là tổ tiên trực tiếp của HEAD và là base tôi dùng. Ref `master` cục bộ trong bản sao cho merge-base `50d8d12e…`, không khớp mô tả packet; tôi không dùng ref stale đó để thay base được chỉ định.

Chốt cuối:

```text
git status --short
# rỗng

git rev-parse HEAD
1d37861ec419d1c3a25cfbdb1b07689bbf42504c
```

VERDICT: changes_requested  
Reviewed commit: 1d37861ec419d1c3a25cfbdb1b07689bbf42504c
