## Findings

### 1. `t34` vẫn xác nhận token, không xác nhận workflow thật sự gọi installer — P2

**Bằng chứng đo được**

Tôi thay cả hai lời gọi:

```yaml
run: bash ops/cai_actionlint.sh
```

bằng:

```yaml
run: echo ops/cai_actionlint.sh
```

rồi chạy:

```text
python3 ops/lease_publish_test.py
```

Kết quả nguyên văn:

```text
lease_publish: 35/35 đạt
ECHO_INSTALLER_MUTATION_RC=0
MUTATED_RUN_LINES:
.github/workflows/ci.yml:155:        run: echo ops/cai_actionlint.sh
.github/workflows/ops-publish-lease.yml:137:        run: echo ops/cai_actionlint.sh
```

`t34` đã bắt được sáu dạng caller khi bỏ token installer (`&&`, pipe, biến, `$()`, `xargs`, `bash -c`), tất cả cho:

```text
rc=1
lease_publish: 34/35 đạt
```

Nhưng nó vẫn dùng:

```python
if not any(TOKEN in x for x in dong_lenh):
```

Do đó P2-1 chỉ được chuyển từ khớp chuỗi caller sang khớp chuỗi installer; phản chứng `echo` vẫn lọt.

**Invariant bị cắt**

Mọi workflow dùng bộ test phải **thực thi** installer giữ tầng. Sự hiện diện của tên script không chứng minh hành vi đó.

**Gợi ý vá**

Tránh tự phân tích shell bằng substring. Chuẩn hóa workflow thành một cấu trúc máy kiểm được, chẳng hạn installer là một step riêng có `run` chính xác sau khi parse YAML:

```yaml
run: bash ops/cai_actionlint.sh
```

Chỉ cho phép các biến thể cú pháp đã parse/chuẩn hóa rõ ràng; thêm mutation bắt buộc `echo`, comment, assignment và chuỗi nằm trong đối số đều phải đỏ.

### 2. Kiểm tra `AL_VER` chấp nhận giá trị không phải `X.Y.Z` — P2

**Bằng chứng đo được**

Tôi dựng gói có binary khai đúng chuỗi bất hợp lệ rồi chạy:

```text
AL_VER=1x.2y.3z AL_GOI=<weird.tar.gz> AL_DICH=<tmp>/d8 AL_NEN=Linux \
  bash kho/ops/cai_actionlint.sh
```

Kết quả:

```text
malformed_accepted rc=0 out=/tmp/.../d8
```

Nguyên nhân là shell pattern:

```bash
[0-9]*.[0-9]*.[0-9]*
```

Trong `case`, `*` khớp cả ký tự không phải số và dấu `.` không được dùng như regex.

**Invariant bị cắt**

`AL_VER` phải là phiên bản ghim exact dạng số `X.Y.Z`; input ngoài schema phải fail-close bằng rc=2.

**Gợi ý vá**

Dùng regex Bash đầy đủ:

```bash
[[ "$AL_VER" =~ ^[0-9]+\.[0-9]+\.[0-9]+$ ]] ||
  loi 2 "..."
```

Bổ sung ca âm như `1x.2y.3z`, `1.2.3/abc`, `1.2.3-rc1`, khoảng trắng và newline. `t35` hiện chỉ thử `""`, `latest`, `1.7`, nên bỏ sót lỗi này.

### 3. Gói thực thi tải từ mạng không được kiểm checksum — P2

**Bằng chứng đo được**

```text
rg -n 'sha256|sha512|checksum|shasum|cosign' ops/cai_actionlint.sh
HASH_CHECK_SEARCH_RC=1
```

Trong khi đường tải và giải nén là:

```text
55:  curl -fsSL --retry 2 -o "$AL_DICH/goi.${GOI##*.}" ...
65:      unzip -q -o "$TEN_GOI" -d "$AL_DICH" ...
69:  *) tar -xzf "$TEN_GOI" -C "$AL_DICH" ...
```

Đối chiếu `actionlint --version` không thay thế kiểm tính toàn vẹn: binary bị thay thế có thể tự in `1.7.7`.

**Invariant bị cắt**

Mã thực thi cấp cho cổng có `contents: write` và `issues: write` phải được xác thực độc lập với chính binary vừa tải.

**Gợi ý vá**

Ghim SHA-256 theo từng asset/platform trong repo hoặc tải checksum release rồi xác thực bằng một trust root độc lập trước khi giải nén/chạy. Áp dụng cùng kiểm tra cho `AL_GOI`, hoặc ghi rõ biến này chỉ dành cho test và không được nhận từ input không tin cậy.

Mức rủi ro là P2: cần compromise release asset/CDN/mirror hoặc nguồn `AL_GOI`, nhưng khi xảy ra sẽ dẫn tới thực thi mã trong job có quyền ghi.

## Các phép đo còn lại

- HEAD đo được khớp bảng: `d0acd79f8bf22acf12d226283f176f2e7cc81508`.
- Diff đúng bốn tệp thuộc write set; merge-base đúng `909d3e171d7b37a734c1100b3fdc3c48e1b66d19`.
- Suite sạch: `lease_publish: 35/35 đạt`, `rc=0`.
- `actionlint .github/workflows/*.yml`: `rc=0` trên cả năm workflow.
- Thiếu `actionlint`: `34/35`, `NO_ACTIONLINT_RC=1`; `t33` fail-close.
- `t35` có đường thuận và thực sự chạy script với các gói giả theo trạng thái. Phần đo installer đúng/sai bản là hành vi; phần giữ tầng và kiểm `AL_VER` trong workflow vẫn dựa trên khớp chuỗi/regex.
- Inline installer trở lại: `33/35`, `INLINE_INSTALL_MUTATION_RC=1`; chốt giữ tầng có răng.
- Mã lỗi đo được phân biệt đúng: thiếu version `2`, nền lạ `3`, thiếu gói `4`, archive hỏng `5`, binary hỏng `6`, sai version `7`.
- Không có nhánh thoát sớm theo `PATH`; script luôn xử lý gói rồi gọi binary vừa giải nén.
- Tar chứa `../ESCAPED`: `TRAVERSAL_RC=5`, `ESCAPED_EXISTS=no`; GNU tar trong môi trường đo đã chặn traversal. Đây không chứng minh mọi implementation `tar` trên mọi runner đều tương đương.
- `doc-claims-check --strict` tại base: `BASE_DOC_CLAIMS_RC=2`, xác nhận đỏ sẵn.
- Mọi mutation nằm trong bản sao dưới thư mục tạm, không ghi vào tracked tree.
- Chốt cuối: `git -C kho status --short` rỗng; HEAD vẫn là `d0acd79f8bf22acf12d226283f176f2e7cc81508`.

VERDICT: changes_requested  
Reviewed commit: d0acd79f8bf22acf12d226283f176f2e7cc81508
