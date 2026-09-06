```yaml
verdict: changes_requested
reviewed_sha: 867dd8585770a6d9e63bfe6feb870bca92d2aecb
base_sha: 1b3caa11df3e339bcfdb52be903884b5b99b9f77
reviewer: codex
executor: claude
P1: 1
P2: 1
```

## Findings

### P1-01 — Marker mới vẫn có một giá trị `sys.platform` làm nó đúng

Điều kiện bước 1 của `SPEC.md` là marker phải sai trên mọi nền. Chuỗi mới ở
`.claude/dev/launcher_test.py:6443` chỉ so sánh bằng với một sentinel; nó sai trên
Windows/Linux hiện tại nhưng không sai với mọi giá trị của biến marker.

Lệnh tái lập đã chạy trong `C:/tl458b/cay-kho`:

```powershell
python -c 'from pip._vendor.packaging.requirements import Requirement; r=Requirement("khong_he_ton_tai_r345; sys_platform == ''khong_he_co''"); print(r.marker.evaluate()); print(r.marker.evaluate({"sys_platform":"khong_he_co"}))'
```

Số đo:

```text
False
True
```

Vì vậy, nếu môi trường marker có `sys_platform="khong_he_co"`, hàng này được áp
dụng. Trong venv Windows do `_r345_venv` dựng, distribution
`khong_he_ton_tai_r345` được đo là `ABSENT`; khi cho hàng đi qua, tiến trình con
trả `rc=1` với đúng stdout:

```text
[session-start] requirements.txt CHUA THOA: khong_he_ton_tai_r345: VANG MAT (khong co metadata)
```

Khi đó kỳ vọng `0` lại phụ thuộc nền, đúng lớp lỗi packet phải loại bỏ. Việc gói
sentinel vắng mặt cũng mới được đo độc lập trên venv Windows này; bằng chứng
executor cho thấy nó vắng trên Linux đã thử, nhưng mã không có tiền điều kiện bảo
đảm tên distribution ấy vắng trong mọi venv trên mọi Python/platform.

Gợi ý vá bắt buộc đủ bốn phần:

- **Vá ở đâu:** hàng `marker khong khop` và chú thích tương ứng trong
  `.claude/dev/launcher_test.py`; thu hẹp cùng lời khai tại `CHANGELOG.md:30` và
  `commit-message.txt:18` nếu chưa dùng marker bất khả thỏa thật sự.
- **Vá thế nào:** dùng một mệnh đề mâu thuẫn theo cùng một biến, chẳng hạn
  `sys_platform == "win32" and sys_platform != "win32"`, thay vì một giá trị
  sentinel có thể được gán cho biến; đồng thời kiểm rõ tiền điều kiện gói đối
  chứng vắng mặt trong venv.
- **Ca test khóa:** đánh giá marker với cả giá trị xuất hiện trong biểu thức và
  một tập giá trị nền khác, tất cả phải `False`; sau đó giữ phép đột biến bỏ lọc
  marker và đòi hàng đích đỏ trên Windows lẫn Linux.
- **Rủi ro bản vá:** biểu thức marker phức hợp phải được parser vendored của các
  phiên bản pip/Python được hỗ trợ hiểu giống nhau; tiền điều kiện gói vắng mặt
  không được biến một môi trường không đo được thành pass.

### P2-01 — Hash “sau” của phép A/B Linux không neo vào file tại `reviewed_sha`

`EVIDENCE.md:42` ghi file sau sửa có SHA-256 bắt đầu bằng
`123529a62160ece1`. Đo trực tiếp byte Git của hai revision cho thấy hash nền được
ghi đúng, nhưng hash sau không phải file tại exact head đang review.

Lệnh tái lập đã chạy trong `C:/tl458b/cay-kho`:

```powershell
@'
import hashlib, subprocess
for label, rev in [
    ("base", "1b3caa11df3e339bcfdb52be903884b5b99b9f77"),
    ("head", "867dd8585770a6d9e63bfe6feb870bca92d2aecb"),
]:
    data = subprocess.run(
        ["git", "-c", "safe.directory=C:/tl458b/cay-kho", "show",
         f"{rev}:.claude/dev/launcher_test.py"],
        capture_output=True, check=True,
    ).stdout
    print(label, len(data), hashlib.sha256(data).hexdigest())
'@ | python -
```

Số đo:

```text
base 429027 009f8e6a1cbc640033c48c79bdd400ab214934382d9078bda8f7e8f5627bdc25
head 431295 b899cb29c0d3295c0213693672fb50473f1ef4033f325773afd66e14656c0ec0
```

Như vậy `009f8e6a…` được xác nhận, còn `123529a6…` là một bản dựng trung gian
hoặc một artefact chưa được cung cấp, không phải byte của exact head. Bảng CI ở
`EVIDENCE.md:9-10` vẫn khai kết quả exact-head riêng, nên finding này không bác
các tổng CI; nó bác phạm vi của lời khai A/B cục bộ tại dòng 40-50.

Gợi ý vá bắt buộc đủ bốn phần:

- **Vá ở đâu:** `EVIDENCE.md:40-50` và mọi câu trong commit/CHANGELOG đang dựa
  vào phép A/B cục bộ đó.
- **Vá thế nào:** chạy lại phép A/B Linux với file lấy trực tiếp từ
  `867dd858…`, ghi đầy đủ SHA-256 mới; hoặc khai rõ `123529a6…` là bản trung gian
  và không dùng nó làm bằng chứng exact-head.
- **Ca test khóa:** trước khi nhận evidence, tính SHA-256 trên byte từ
  `git show <reviewed_sha>:.claude/dev/launcher_test.py` và đòi bằng đúng trường
  `after_sha256` đã ghi.
- **Rủi ro bản vá:** phải quy định hash byte Git hay byte checkout; CRLF có thể
  tạo hash khác. Nên hash Git blob và ghi rõ thuật toán/nguồn byte.

## Phán định tám hướng

### 1. Tính độc lập nền của hàng mới

**Không đạt.** Trên Windows/Python 3.13.1 hiện tại, marker mặc định đo được
`False`, nhưng với environment `{"sys_platform": "khong_he_co"}` đo được
`True`. Do đó không thể gọi biểu thức hiện tại là sai trên mọi nền. Distribution
sentinel đo được `ABSENT` trong venv Windows hiện tại; Linux chỉ có bằng chứng do
executor cung cấp, không phải phép đo độc lập của reviewer. Không có chốt trong
`_r345_venv` bảo đảm sự vắng mặt trên mọi Python/platform. Xem P1-01.

### 2. Răng của đột biến thứ ba và tín dụng giả

**Đạt trên exact head ở Windows.** Các số đo độc lập:

- `python .claude/dev/launcher_test.py --lap-ca r345_cac_phep_do_cuc_bo_van_dung --lan 1`
  → `1/1 qua`, `0 bo qua`, `0 hong`, rc=0.
- `python .claude/dev/launcher_test.py --lap-ca r345_dot_bien_ba_phep_do_cuc_bo_lam_ca_dich_DO --lan 1`
  → `1/1 qua`, `0 bo qua`, `0 hong`, rc=0.
- Đột biến sống trong bộ nhớ: `anchor_count=1`; ca đích ném
  `TinHieuChotCa`; thông điệp là
  `phep do cuc bo sai: marker khong khop: duoc 1, mong 0`.
- Chạy riêng tiến trình con của đúng mutant: `child_rc=1`, stderr rỗng, stdout
  chỉ báo `khong_he_ton_tai_r345: VANG MAT (khong co metadata)`.

Vì thay đổi duy nhất là bỏ đúng câu lọc marker, và tiến trình con chết bởi đúng
distribution của hàng đích, không thấy tín dụng giả trong phép đo này.

### 3. Rà đủ 10 hàng

Mười hàng đều đã được chạy riêng trong cùng một venv thật do `_r345_venv` dựng:

| Hàng | Đo Windows `actual/expected` | Liên hệ `sys_platform`/`os_name` |
|---|---:|---|
| `ban thoa` | `0/0` | Không có marker; độc lập theo hai biến này được suy từ chính chuỗi fixture. |
| `lech ban` | `1/1` | Không có marker; suy từ chuỗi fixture. |
| `marker khong khop` | `0/0` | Có `sys_platform`; đo marker mặc định `False`, giá trị sentinel `True`. Kỳ vọng vẫn phụ thuộc biến này. |
| `marker chua dau thang` | `0/0` | Có `os_name`; đo mặc định `False`, ép `os_name="posix#x"` cho `True`. Vì `pypdf` có mặt nên kỳ vọng `0` ở nhánh đúng được suy từ phép kiểm downstream; chưa ép environment end-to-end. |
| `chu thich sau khoang trang` | `0/0` | Không có marker; suy từ chuỗi fixture. |
| `URL tran toi host chet` | `0/0` | Không có marker; suy từ chuỗi fixture. |
| `VCS git+http` | `0/0` | Không có marker; suy từ chuỗi fixture. |
| `goi VANG MAT + direct ref` | `1/1` | Không có marker; suy từ chuỗi fixture. |
| `goi CO MAT + direct ref` | `0/0` | Không có marker; suy từ chuỗi fixture. |
| `goi thieu han` | `1/1` | Không có marker; suy từ chuỗi fixture. |

Vì vậy lời khai “không hàng nào khác có **kỳ vọng** phụ thuộc
`sys_platform`/`os_name`” phù hợp với 9 hàng còn lại trong phạm vi đã rà, với
caveat nêu rõ cho `marker chua dau thang`. Hàng mới chính là ngoại lệ chưa được
loại bỏ hoàn toàn.

### 4. Hai hàng dùng chung gói vắng mặt

**Không thừa và không ghi công chéo trong thiết kế hiện tại.** Hàng
`goi thieu han` đo `1/1`; hàng có marker đo `0/0`. Khi bỏ lọc marker, thông điệp
ngoài chỉ liệt kê `marker khong khop`, còn `goi thieu han` vẫn khớp kỳ vọng `1`.
Quan trọng hơn, ca đột biến thứ ba gọi `_r345_chay` với đúng một dòng
requirements của hàng marker, nên hàng `goi thieu han` không có mặt để vô tình
giết mutant. Việc dùng chung package giúp giữ package là biến kiểm soát; khác biệt
được đo là marker.

### 5. Độ chặt của neo đột biến

**Đủ chặt cho thân hook hiện tại.** `than.count(neo_marker)` đo được đúng `1`;
tìm toàn cây cho thấy câu thực thi nằm tại
`.claude/hooks/session-start.sh:369`, còn các lần khác là định nghĩa/kiểm neo trong
test. Thay đúng neo đó làm đúng hàng marker đỏ và tiến trình con báo đúng gói vắng
mặt. Neo lexical không chứng minh mọi refactor tương lai, nhưng chốt hành vi và
nhãn hàng hiện tại ngăn một vị trí khác được ghi công trong bản đang review.

### 6. Phạm vi lời khai và từng con số

| Lời khai | Kết quả kiểm |
|---|---|
| `164/165` | **Đo được:** bản sao exact head chỉ đổi fixture về dạng cũ cho `164/165`, `hong 1`, rc=1. |
| `165/165` | **Đo được:** exact head cho `165/165`, `hong 0`, rc=0. |
| `tong 182, bo qua 17` | **Đo được:** cả hai lượt full Windows cho đúng tổng/bỏ qua; import module cũng cho `len(CA)=182`. |
| `181/181` | **KHÔNG ĐO ĐƯỢC độc lập trong phiên Windows này.** `EVIDENCE.md` khai CI Ubuntu exact-head `181/181`, bỏ qua 1, hỏng 0. |
| `160/160` | **Đo được:** `--dot-bien` exact head cho `160/160`, 11 không đo được, rc=0. |
| `170/170` | **KHÔNG ĐO ĐƯỢC độc lập trong phiên Windows này.** `EVIDENCE.md` khai CI Ubuntu `170/170`, 1 không đo được. |
| `009f8e6a` | **Đo được, đúng:** SHA-256 Git blob base bắt đầu `009f8e6a1cbc6400`. |
| `123529a6` | **Đo được, sai với exact head:** head bắt đầu `b899cb29c0d3295c`, không phải `123529a62160ece1`; xem P2-01. |

Các số Windows trong commit/CHANGELOG không rộng hơn phép đo reviewer. Các số
Linux chỉ được đối chiếu với `EVIDENCE.md`, không được reviewer chạy lại do phiên
này là Windows. Phép A/B Linux cục bộ được mô tả rộng hơn artefact có thể xác
minh vì hash “sau” không khớp reviewed head.

### 7. Lời khai nợ `marker chua dau thang`

**Đo lại và đúng.** Trong bộ nhớ, thay đúng một lần
`_CHU_THICH = re.compile(r"(^|\s)#.*$")` bằng
`_CHU_THICH = re.compile(r"#.*$")`, rồi chạy ca đích với cùng venv: kết quả
`RAW_COMMENT_TARGET=GREEN result=None`. Không ném ngoại lệ. Do đó hàng này vẫn
không có răng với luật comment thô như lời khai.

### 8. Hồi quy trong bộ phản chứng

Không thấy hồi quy trong phần đo được trên Windows:

- Full candidate: `165/165 ca DA CHAY QUA (tong 182, bo qua 17, hong 0)`, rc=0.
- Full bản sao fixture cũ: `164/165`, đúng một lỗi ở
  `r345_cac_phep_do_cuc_bo_van_dung`, tổng 182, bỏ qua 17, rc=1.
- Tự đột biến candidate: `160/160 dat (11 khong do duoc tren nen nay)`, rc=0.
- `git diff --check base head`: rc=0.
- `doc-claims-check --strict`: `ok=true`, 106 tệp, 366 claim được xem xét,
  không có flag cứng, rc=0. Cổng này không bắt được P1-01 hoặc hash ngoài repo ở
  P2-01.
- Mirror được review vẫn sạch, detached tại `867dd858…`; tree
  `823a9091ca45c434a95862e0a86170f4b8e5fc01`.

Bộ full và mutation trên Linux **KHÔNG ĐO ĐƯỢC độc lập trong phiên này**; chỉ có
bằng chứng executor/CI trong `EVIDENCE.md`. Vì P1-01 vi phạm trực tiếp yêu cầu
marker sai trên mọi nền, verdict là `changes_requested` dù toàn bộ phép đo Windows
hiện tại đều xanh.
