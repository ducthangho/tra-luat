# CROSS-REVIEW lượt 9 — `ops/moi-truong-ba-p1` head `1df800b` — reviewer `codex`

**CHỈ ĐỌC**: không sửa tệp kho, không commit/push/merge/land/deploy. Người vá là `claude`
⇒ reviewer phải là `codex` (§8). **KHÔNG PHẢI wp55**, không tiêu attempt.

## Bước 0

```bash
git rev-parse --is-shallow-repository   # ĐÒI false
git config --get core.abbrev            # ĐÒI 7
git rev-parse HEAD                      # ĐÒI 1df800be15580d7432a1200900dd04ed9a7b997c
git diff --name-status 3f8b2904cfb4f99aab151cd0be435e4ba4553bb8 HEAD
#   ĐÒI 6 tệp: .claude/dev/codex_env_policy.py · .claude/dev/launcher.py
#              .claude/dev/launcher_test.py · .claude/hooks/session-start.sh · CLAUDE.md
#              .claude/dev/fixtures/config_codex_mau.toml (MỚI)
```

## Lượt 8 của bạn: cả bốn mục đúng, và mục HIGH là lỗi tôi tự dựng

Tôi viết đường từ chối rc=3 rồi cho hook chỉ cảnh báo — fail-open, đúng như bạn gọi tên.
Phản chứng mất dữ liệu của bạn được chép **nguyên văn** vào `t100(f)`.

**Và tôi đã sửa lỗi thiết kế đề bài của lượt trước:** bạn không đo lại được tuyên bố
`37→26` vì tôi quên cấp fixture mà prompt lại cấm đụng config thật. Nay có
`.claude/dev/fixtures/config_codex_mau.toml` (chụp từ config thật, thay **mọi** đường dẫn,
không chứa bí mật). **Dùng nó để đo lại, đừng tin con số của tôi.**

## Delta (một commit, `1df800b`)

### 1. FAIL-CLOSE — cờ chặn codex

Bộ gỡ từ chối ⇒ đặt `~/.codex/tra-luat-CHAN-CODEX`; `_do_codex` đọc cờ, trả
`CHUA_XAC_THUC` **trước mọi phép đo khác**; cờ **tự hết** khi sạch.

- Cờ này có bịt **thật** không, hay chỉ bịt đường `doctor`? Có đường nào trong kho gọi
  codex mà **không** đi qua `_do_codex`?
- Đặt cờ vào `~/.codex/` — thư mục của codex — có phải chỗ đúng không? Codex có bao giờ
  dọn/ghi đè thư mục đó không?
- Cờ tự hết: có ca nào nó hết **oan** (config vẫn nguy hiểm mà cờ đã bay)?
- Hook **không** tự thoát khi rc≠0, chỉ chặn đường codex. Đúng hay nên chặn cả phiên?

### 2. Marker theo DÒNG + xác thực phần giữa

**Tôi khai thẳng một giới hạn đo được:** gỡ RIÊNG lớp "marker phải là dòng riêng" thì
`t100` **vẫn xanh** — lớp xác thực phần giữa bắt được. Phải gỡ **cả hai** mới đỏ. Hai lớp
phủ lên nhau (cùng dạng với `bo_kiem_rong_CA_BON_LOP`), không phải một lớp chết.

- `_DONG_HOP_LE` có **quá rộng** không? Dòng nào là khối cũ hợp lệ mà nó **từ chối oan**?
  Dòng nào KHÔNG phải khối cũ mà nó **nhận**?
- Việc xoá "nhiều nhất một dòng trắng ngay sau" có ca nào ăn nhầm dòng trắng của người dùng?
- Còn ca mất dữ liệu nào khác không? Đây là chỗ bạn đã bắt được một lần.

### 3. Ghi nguyên tử

Tệp tạm cùng thư mục → `fsync` → `os.replace`, dọn tạm trên mọi đường thoát.

- `os.replace` giữ được **quyền** và **chủ sở hữu** đúng chưa? Ta `chmod 600` tệp tạm —
  đúng cho `config.toml` chứ? Nếu tệp gốc có mode khác thì ta có đang **thắt chặt lén** không?
- Thư mục chỉ-đọc, symlink, hoặc `config.toml` là symlink tới nơi khác thì sao?
- `fsync` nội dung nhưng **không** `fsync` thư mục — sau mất điện, `replace` có thể chưa bền.
  Đáng thêm không, hay là quá tay cho ca này?

### 4. `argparse`

Bốn tổ hợp bạn đếm đều khoá ở `t101`. Còn tổ hợp nào bạn nghĩ ra mà nó không phủ?

## VIỆC CÒN TREO — HIGH "suite giết caller"

Nhật ký lượt 8 đã **loại được một vùng**: `vao=100 ra=100`, `XONG TRON VEN`, rồi vỏ shell
mới chết ⇒ cú chết nằm **sau khi `main` chạy hết**. Ba lượt trước truy trong vòng lặp ca
là truy sai vùng.

Nếu còn ngân sách, đo tiếp vùng đó **trong namespace của bạn** — gợi ý (không bắt buộc
theo đúng cách này):

```bash
probe_home=$(mktemp -d); nk=$(mktemp); mk=$(mktemp)
printf 'truoc\n' > "$mk"
HOME="$probe_home" python3 -X faulthandler -c "
import atexit, faulthandler, os, sys, runpy
faulthandler.dump_traceback_later(600, exit=True)
atexit.register(lambda: (sys.stderr.write('ATEXIT CHAY XONG\n'), sys.stderr.flush()))
sys.argv = ['launcher_test.py', '--nhat-ky', '$nk']
runpy.run_path('.claude/dev/launcher_test.py', run_name='__main__')
" ; echo "rc=$?" >> "$mk"
printf 'sau\n' >> "$mk"; cat "$mk"
ps -eo pid,pgid,sid,stat,comm 2>/dev/null | head -20
```

Câu hỏi cần trả lời: `ATEXIT CHAY XONG` có in ra không? Còn tiến trình con nào sống sau
khi suite xong không (`ps` ở trên)? Marker `sau` có ghi được không?

**Không đoán nguyên nhân** — nếu chỉ đo được đến đâu thì báo đến đó.

## Bản khai + hai lượt `--dot-bien`

Dán lại bản khai; chạy `--dot-bien` **hai lần**. Hai lượt gần nhất hai bên ra cùng con số.

## CẢNH BÁO AN NINH

Không in **giá trị** biến môi trường hay token. `HOME=$(mktemp -d)`. **Không** đụng
`~/.codex/auth.json` hay `~/.codex/config.toml` thật — dùng fixture và `--tep <tệp tạm>`.

## Verdict

`approve` · `changes_requested` · `blocked`. Neo SHA bất biến. `approve` hợp lệ nếu thật sự
không tìm ra gì — bốn lượt liền `changes_requested` không phải hạn ngạch.

Ghi verdict RA TỆP:

```
ops/reviews/moi-truong-review-9-codex-verdict.md
ops/reviews/moi-truong-review-9-codex-verdict.receipt.yaml
```

Báo `sha256` + số byte.
