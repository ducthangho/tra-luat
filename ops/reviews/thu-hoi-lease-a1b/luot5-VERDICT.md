<!-- Verdict codex lượt 5 (gpt-6-astra, reasoning effort xhigh — xác nhận ở header log runtime), codex_cli tại chỗ, trên ops/specs/THU-HOI-LEASE-A1b.md bản nháp 13 @ b124b64, base 5c79fa2. Chép nguyên văn từ tệp -o của codex exec; chỉ bỏ khoảng trắng cuối dòng theo tiền lệ. -->
Có **2 finding P2**. Review này là `advisory_review`, `openai_codex / codex_cli / machine`; model/effort chưa được chứng thực bằng header runtime.

```text
reviewed_sha:  b124b64be5fdc3ae1dbe77acbfd7a9742ec7745c
reviewed_tree: 6dfdf1b506da3899cce3d15a38d3bc33c1fc32fd
base:          5c79fa2c94b328ae3bbbef52a4cfa820fc40bc4a
spec_sha256:   c2640ba3750ec45d4b3ce9517af627b4d88bbfd5ec5deaebec384137147acaf6
```

Đã đọc lại [quyết định nâng trần](https://github.com/ducthangho/tra-luat/pull/657#issuecomment-5853920122); API xác nhận PR vẫn ở đúng SHA trên.

**[P2] ops/specs/THU-HOI-LEASE-A1b.md:131 — A5 đòi đầu vào sinh `11→0` trên một trục không thể trả `11`.**

M5(b) xếp `11→0` vào **eligibility**; A5 dòng 142 bắt mỗi loại có đầu vào sinh đúng delta qua seam WIRING, thiếu thì chưa đo. Nhưng eligibility được A6 giao cho `check`; luật cũ của `check` không trả `11`. Q14 lại bắt WIRING giữ nguyên hành vi khi cờ `False`. Vì vậy không thể dựng vế trước bằng `11` qua các đầu vào map/clock/discovery đã khai. `11` thuộc `ai-dang-giu`.

Bằng chứng:

```bash
python3 -B - <<'PY'
import ast
from pathlib import Path
t = ast.parse(Path('ops/lease_publish.py').read_text())
fs = {n.name:n for n in t.body if isinstance(n, ast.FunctionDef)}
q, seen = ['lenh_check'], set()
while q:
    n = q.pop()
    if n in seen or n not in fs:
        continue
    seen.add(n)
    q += [x.func.id for x in ast.walk(fs[n])
          if isinstance(x, ast.Call) and isinstance(x.func, ast.Name)]
codes = sorted({ast.unparse(x.args[0])
    for n in seen for x in ast.walk(fs[n])
    if isinstance(x, ast.Call) and isinstance(x.func, ast.Name)
    and x.func.id == 'Chan' and x.args})
print('check_Chan_codes:', codes)
print('rc11_consumers:', [n for n,f in fs.items()
    if any(isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load)
           and x.id == 'RC_DANG_GIU' for x in ast.walk(f))])
PY
```

Output, **rc=0**:

```text
check_Chan_codes: ['RC_KHONG_XAC_DINH', 'RC_LOP', 'RC_NEO', 'RC_NOI_DUNG', 'RC_THAM_SO', 'RC_TU_CAP']
rc11_consumers: ['lenh_ai_dang_giu']
```

**Câu sửa đề xuất:** “Phản chứng production được khai riêng theo hợp đồng từng đường; `11` thuộc trục holder. Phản chứng bộ phân loại delta được tiêm cặp kết quả tại seam của bộ phân loại, không bắt đầu vào discovery sinh một mã ngoài hợp đồng.”

Khóa bằng ca bộ phân loại từ chối cặp kết quả cấm và mutant bỏ chốt ấy làm ca đỏ. Không thêm hành vi trả `11` vào `check` chỉ để đạt nghiệm thu.

**[P2] ops/specs/THU-HOI-LEASE-A1b.md:84 — T6/A6 bỏ sót hai consumer mà r9 bắt dùng chung trạng thái.**

T6 và ma trận A6 chỉ nghiệm thu `check`, `ai-dang-giu`, `kiem-thu-hoi-github`. r9 Q4.6 còn yêu cầu **`body` và `kiem-github`** dùng chung hàm trạng thái. Hai đường này đang gọi bộ kiểm cũ trực tiếp; WIRING chỉ nối ba entry point đã liệt kê vẫn có thể đạt toàn bộ ma trận A6 mà bỏ chúng lại.

Đây là thiếu phạm vi nghiệm thu; guard `packet_loop` thuộc slice B nên không nằm trong finding này.

Bằng chứng:

```bash
sed -n '355,356p' ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md
python3 -B - <<'PY'
from pathlib import Path
s = Path('ops/specs/THU-HOI-LEASE-A1b.md').read_text().splitlines()
names = {'check','ai-dang-giu','body','kiem-github','kiem-thu-hoi-github'}
for line in (84,143):
    print(line, 'missing:',
          sorted(n for n in names if '`'+n+'`' not in s[line-1]))
PY
```

Output, **rc=0**:

```text
6. Nạp sổ một lần; áp theo `lease_id` cho **MỌI** cặp; ... Mọi lệnh
   (`check`, `ai-dang-giu`, `body`, `kiem-github`, `kiem-thu-hoi-github`, guard packet_loop) dùng chung hàm trạng thái.
84 missing: ['body', 'kiem-github']
143 missing: ['body', 'kiem-github']
```

**Câu sửa đề xuất:** “T6/A6 phải nghiệm thu thêm `body` và `kiem-github`, với oracle theo hợp đồng riêng và phản chứng bỏ kiểm trạng thái/discovery tại từng đường.” Ghi phần mở rộng vào bảng diễn giải Q14 chờ xác nhận; giữ nguyên ô quyết định gốc. Thiếu seam thì trả về packet WIRING, không chuyển thi công sang A1b.

Khóa bằng mutant bỏ kiểm ở riêng từng đường; giữ nguyên hành vi cờ `False` và các chốt GitHub hiện có.

Đối chiếu Claude lượt 7:

| Finding | Kết quả trên nháp 13 |
|---|---|
| F1 | **Đã vá thật:** cả 18 ô Q khớp byte các commit nguồn; diễn giải tách riêng. |
| F2 | Đã bổ sung các lượt tái diễn được finding chỉ ra và checkpoint. |
| F3, F4 | **Chưa vá**, khai đúng thành nợ §8.8–9; không lặp finding. |
| F5 | Đã hạ lời khai A4; phần thiết kế còn mở ở §8.10. |
| F6 | **Đã vá thật:** phân biệt r9 Q2 và chặn R8(b) khi sổ/hằng rỗng. |
| F7 | Đã thêm tiền đề binding/verifier T7; chưa chứng nhận hiện vật triển khai. |
| F8–F12 | Các sửa cơ học khớp phép đo băm, lịch sử, write set và dẫn dòng. |
| F13 | Khai đúng giới hạn runtime ở §8.11; chưa đóng nợ. |

Các phép đo bổ sung:

```bash
git diff --numstat 0721811^1 0721811
```

**rc=0**, kiểm từng số hạng:

```text
141     0   .github/workflows/ops-thu-hoi-admission.yml
919     0   ops/lease_publish.py
1327    1   ops/lease_publish_test.py
```

Tổng **2.387 dòng thêm / 3 tệp**. Hai phép `git rev-list --first-parent --count` từ A0 tới `67802bf` và `f5bef3a` lần lượt trả **76**, **77**, đều rc=0.

```bash
python3 -B ops/reviews/thu-hoi-lease-a1a-r2/do_q6_hk.py \
  . 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z
```

**rc=0**; bản in khớp byte JSON đã ghim:

```text
lease_hop_le=89
cap_hai_chieu=11
vi_pham=[]
BIA_MO_LICH_SU_theo_b=[]
digest=8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48
stdout_sha256=1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61
```

M1–M6 đều chiếu vào write set §3. Các băm lịch sử, băm script và dẫn dòng Git đã kiểm khớp; descriptor đọc lại có **1.379 byte**, băm `f974b6db…`, không newline cuối. Log đã ghim có đúng **35/35**, **27 dòng `DUNG `**, một `DUNG LECH`; **không khai là đã chạy lại hai suite đó**.

Các số lịch sử **100/89 run, 441/441 ref và annotation Ubuntu** chưa tái lập độc lập. CI/canary/implementation: **not_run**. `git diff --check` passed, rc=0; HEAD/tree và tracked/index không đổi. Không sửa tệp, không commit.

VERDICT: REQUEST_CHANGES
