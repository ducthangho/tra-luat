## Findings

### 1. `t34` vẫn fail-open với các dạng gọi ngoài `_CHAY_BO_TEST` — P2

**Bằng chứng đo được**

Trên bản sao tạm, tôi bỏ installer khỏi job `ci.yml:gate` và đổi lệnh thành dạng hợp lệ:

```yaml
run: python -m ops.lease_publish_test
```

Chạy trực tiếp:

```text
python3 ops/lease_publish_test.py
actionlint .github/workflows/*.yml
```

Kết quả nguyên văn:

```text
lease_publish: 38/38 đạt
PYTHON_MODULE_NO_INSTALLER_RC=0
PYTHON_MODULE_ACTIONLINT_RC=0
```

Ca thứ hai: chuyển installer xuống sau selftest và gọi selftest qua shell:

```yaml
run: bash -c "python ops/lease_publish_test.py"
```

Kết quả:

```text
lease_publish: 38/38 đạt
BASH_C_INSTALL_AFTER_RC=0
BASH_C_ACTIONLINT_RC=0
```

`python -m ...` không chứa chuỗi `lease_publish_test.py`, nên cả `i_nhac` lẫn `i_chay` đều `None`: nghĩa vụ installer biến mất. `bash -c ...` có `i_nhac`, nhưng không khớp `_CHAY_BO_TEST.fullmatch`; do đó installer đặt sau vẫn không bị `sai_thu_tu`.

**Invariant bị cắt**

Mọi job thực sự chạy bộ kiểm phải có installer trên cùng runner và installer phải hoàn thành trước lần chạy, bất kể cú pháp shell dùng để gọi Python.

**Gợi ý vá**

Không duy trì danh sách regex dương cho các shell invocation. Có thể:

- Chuẩn hóa một wrapper duy nhất, chẳng hạn `bash ops/chay_lease_publish_test.sh`, rồi bắt workflow dùng đúng wrapper; wrapper tự cài/kiểm `actionlint`.
- Hoặc tách thành composite action chứa cả installer và selftest.
- Nếu vẫn dùng phân tích YAML, nghĩa vụ và thứ tự phải bấu vào cùng một invocation canonical, đồng thời từ chối mọi dạng không nhận diện được thay vì bỏ qua.

Thêm mutation tối thiểu cho `python -m ...`, `bash -c ...`, `exec python ...`, `uv run ...` và lệnh sau `&&`/`;`.

---

### 2. Installer `if: false` vẫn được tính là đã cấp công cụ — P2

**Bằng chứng đo được**

Tôi thêm vào installer của `ci.yml`:

```yaml
if: false
```

Selftest vẫn đứng sau như cũ. Kết quả:

```text
lease_publish: 38/38 đạt
IF_FALSE_RC=0
IF_FALSE_ACTIONLINT_RC=0
```

GitHub chắc chắn bỏ qua bước này, nhưng `t34` chỉ đọc thân `run`, nên vẫn đặt `i_cai` và tuyên job đã có installer.

**Invariant bị cắt**

Installer phải thực sự có khả năng chạy trên mọi đường thực thi dẫn tới selftest; sự hiện diện cấu trúc của một bước bị skip không cấp bất kỳ binary nào.

**Gợi ý vá**

Fail-closed khi installer có `if:` trừ khi điều kiện được chứng minh tương đương với điều kiện của selftest. Phương án ít mong manh hơn vẫn là đóng gói installer và selftest trong cùng wrapper/composite action, không cho hai bước có điều kiện độc lập.

---

### 3. Suy loại archive từ suffix vẫn từ chối zip hợp lệ không đuôi hoặc `.ZIP` — P2

**Bằng chứng đo được**

Tôi dựng tar và zip hợp lệ, đều chứa executable `actionlint` in `1.7.7`, truyền đúng SHA-256 và đọc rc trực tiếp:

```text
nodot rc=0 out=/tmp/platx4-archive.fe5rmj/d-nodot
archive.tgz rc=0 out=/tmp/platx4-archive.fe5rmj/d-archive.tgz
zipnodot rc=5 out=cai_actionlint: giai nen xong ma khong thay `actionlint` trong '/tmp/platx4-archive.fe5rmj/d-zipnodot'
archive.ZIP rc=5 out=cai_actionlint: giai nen xong ma khong thay `actionlint` trong '/tmp/platx4-archive.fe5rmj/d-archive.ZIP'
archive.zip rc=0 out=/tmp/platx4-archive.fe5rmj/d-archive.zip
```

Vá hiện tại đóng đúng phản chứng tar tên `nodot`, nhưng mọi tên không khớp chính xác `*.zip` đều bị ép sang `tar -xzf`. Với zip, `tar` có thể giải nén mà không báo lỗi nhưng không tạo nội dung mong đợi, cuối cùng rc=5.

So với rev2, tar không đuôi đã tốt hơn; việc xác định loại archive vẫn chưa đáp ứng giao diện `AL_GOI` chỉ mô tả là đường dẫn gói có sẵn. `.tgz` hoạt động do rơi vào nhánh tar, không phải do nhận diện riêng.

**Invariant bị cắt**

Loại archive không được suy sai chỉ từ cách viết hoa hoặc việc tên tệp có suffix, đặc biệt khi hợp đồng không bắt buộc quy ước tên.

**Gợi ý vá**

Ưu tiên một trong hai hợp đồng rõ ràng:

- Nhận diện nội dung bằng magic bytes/khả năng giải nén an toàn; hoặc
- Thêm `AL_LOAI_GOI=zip|tar.gz` bắt buộc cho tên mơ hồ, xử lý suffix không phân biệt hoa/thường và từ chối rõ ràng loại không xác định.

Không nên mặc định “không phải `*.zip` thì chắc chắn là tar”.

## Hai finding lượt 2

Cả hai đã đóng trong đúng phản chứng cũ:

```text
lease_publish: 37/38 đạt
JOB_SPLIT_RC=1
```

Job chạy selftest chỉ còn `echo`, installer canonical ở job khác: `t34` nay đỏ.

Tar hợp lệ tên không dấu chấm:

```text
nodot rc=0 out=/tmp/platx4-archive.fe5rmj/d-nodot
```

## Các hướng đã đo thêm

Mutation riêng của các ca mới cho thấy chúng có răng:

```text
t35_MUTATION_RC=1
lease_publish: 37/38 đạt
t36_MUTATION_RC=1
lease_publish: 37/38 đạt
t37_MUTATION_RC=1
lease_publish: 37/38 đạt
t38_MUTATION_RC=1
lease_publish: 37/38 đạt
```

Cụ thể:

- `t35`: khôi phục `${TEN_GOI##*.}` làm chính `t35` đỏ.
- `t36`: khôi phục giải nén trực tiếp từ đường dẫn có `C:` làm `t36` đỏ, rc=5.
- `t37`: bỏ cưỡng chế mismatch băm làm `t37` đỏ.
- `t38`: truyền tên tệp cho `sha256sum` thay vì stdin làm `t38` đỏ, rc=9.

Over-approximate ở trục nghĩa vụ có báo nhầm thật. Một job chỉ chạy:

```yaml
run: echo lease_publish_test.py
```

bị buộc installer:

```text
ĐỎ  t34_MOI_workflow_goi_bo_test_deu_phai_duoc_cap_actionlint: job ['ci.yml:chi-nhac-tai-lieu'] ...
lease_publish: 37/38 đạt
MENTION_ONLY_RC=1
```

Đây là chi phí fail-closed đã được chủ ý chấp nhận, nhưng nó củng cố lý do không nên dùng nhận diện chuỗi để mô hình hóa hành vi shell.

Job chỉ có `uses:` và reusable workflow ngoài tệp quét không được `t34` truy vết. Tôi chưa dựng được phản chứng external reusable hoàn chỉnh trong sandbox, nên phần này vẫn là giả thuyết; reusable workflow cục bộ nằm dưới `.github/workflows/*.yml` sẽ được quét như một tệp độc lập.

## Bằng chứng nền

```text
lease_publish: 38/38 đạt
SUITE_RC=0 ACTIONLINT_RC=0
```

Write set:

```text
.github/workflows/ci.yml
.github/workflows/ops-publish-lease.yml
ops/cai_actionlint.sh
ops/lease_publish_test.py
WRITE_SET_COUNT=4
```

Tôi không khai đã đọc `N/N` Windows; chỉ dùng bằng chứng success được packet cung cấp.

Chốt cây:

```text
git -C kho status --short
# rỗng
HEAD=a09aae627533f59e6b2e817858a6db50b999d41c
TREE=08b291e4a5ac0eae65df8989d9871ba2ffe49086
```

VERDICT: changes_requested  
Reviewed commit: a09aae627533f59e6b2e817858a6db50b999d41c
