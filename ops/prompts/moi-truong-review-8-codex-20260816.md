# CROSS-REVIEW lượt 8 — `ops/moi-truong-ba-p1` head `3f8b290` — reviewer `codex`

**CHỈ ĐỌC**: không sửa tệp kho, không commit/push/merge/land/deploy. Người vá là `claude`
⇒ reviewer phải là `codex` (§8). **KHÔNG PHẢI wp55**, không tiêu attempt của packet.

## Bước 0

`git fetch`/`git config` không chạy được trong vai này. Điều phối chạy hộ trong chính clone
bạn đứng. Xác minh **bằng đọc**:

```bash
git rev-parse --is-shallow-repository   # ĐÒI false
git config --get core.abbrev            # ĐÒI 7
git rev-parse HEAD                      # ĐÒI 3f8b2904cfb4f99aab151cd0be435e4ba4553bb8
git diff --name-status 69bc3cede6085bf6229ac95a44da4aae9e51ee42 HEAD
#   ĐÒI 5 tệp: .claude/dev/codex_env_policy.py (MỚI) · .claude/dev/launcher_test.py
#              .claude/hooks/session-start.sh · CLAUDE.md · docs/GOI_AGENT_DA_NEN.md
```

## VIỆC SỐ MỘT — định vị cú chết, lần này bằng phép đo SỐNG SÓT ĐƯỢC

Lượt 7 bạn báo suite "dừng ngay sau `t62`". Tôi tin, và đi truy `t63`. **Cả hai chúng ta
đều đọc sai một tạo tác của bộ đệm.**

Bộ test không in gì trong lúc chạy — chỉ dòng BỎ QUA và dòng tổng kết. Nên `BO QUA t62` là
dòng **cuối cùng được IN**, không phải ca **cuối cùng được CHẠY**. Thêm nữa stdout nối vào
ống là bộ đệm KHỐI: mọi thứ chưa xả mất sạch cùng cú giết. Phép đo dùng để định vị cú chết
không sống sót nổi cú chết đó. Ba lượt tìm ở sai chỗ.

Nay có `--nhat-ky`: ghi `>>> vao` / `<<< ra` từng ca, `flush` **+ `fsync`**, kết thúc bằng
`# XONG TRON VEN`.

**Chạy đúng lệnh này, trong namespace của bạn:**

```bash
nk=$(mktemp); probe_home=$(mktemp -d)
HOME="$probe_home" python3 .claude/dev/launcher_test.py --nhat-ky "$nk"; echo "rc=$?"
tail -5 "$nk"
python3 - "$nk" <<'PY'
import sys, re
d = open(sys.argv[1]).read().splitlines()
vao = [re.match(r">>> vao\s+(\d+) (\S+)", x).group(2) for x in d if x.startswith(">>> vao")]
ra  = {re.match(r"<<< ra\s+(\d+) (\S+)", x).group(2) for x in d if x.startswith("<<< ra")}
thieu = [t for t in vao if t not in ra]
print("vao:", len(vao), "| ra:", len(ra), "| CA GIET:", thieu or "khong co")
print("tron ven:", d and d[-1] == "# XONG TRON VEN")
PY
```

**Báo đích danh ca có `vao` mà không có `ra`.** Đó là ca giết tiến trình — lần đầu tiên ta
có con số thay vì suy đoán. Nếu nhật ký `XONG TRON VEN` mà vỏ shell vẫn chết sau đó, thì
cái chết nằm NGOÀI vòng lặp ca (lúc thoát/`atexit`/flush cuối) — cũng là thông tin mới, báo
thẳng. Nếu suite chạy hết bình thường thì nói rõ luôn.

Soi luôn chính bộ đo: `NhatKyCa` + `chay_bo_ca` + `t99`. `t99` có răng thật không? `fsync`
mỗi ca có làm chậm/đổi hành vi đáng kể không? `--nhat-ky` phân tích đối số bằng tay
(`sys.argv.index`) — có ca nào nó nuốt nhầm hoặc chết không?

## Delta lượt này (một commit, `3f8b290`)

### 1. Nhật ký từng ca — xem trên

### 2. THU HỒI `inherit = "all"` (HIGH của bạn)

Lập luận của bạn đúng và tôi nhận: credential đã ra `~/.codex/auth.json` **trước khi** khối
policy chạy, nên policy không mua được gì; và hook không chạy thì policy cũng không có, nên
nó chưa bao giờ là đường cứu hộ độc lập. Hook nay **chỉ gỡ**, không còn đường ghi nào.

- Còn đường nào trong kho ghi lại `inherit = "all"` không?
- Gỡ xong thì codex **còn chạy được** trong các luồng kho vẫn dùng chứ? Tôi cho rằng có
  (device-auth đúc credential tại chỗ) nhưng đó là **lập luận của tôi**, không phải phép đo.
- Tài liệu đã sửa hay còn chỗ nào dạy người sau dựng lại?

### 3. Gỡ mà không làm hỏng config người dùng (MEDIUM của bạn)

`.claude/dev/codex_env_policy.py`: hai kết cục, **gỡ đúng khối có marker** hoặc **TỪ CHỐI
kèm chẩn đoán**. Không prepend, không đoán.

- `go_khoi` có ca nào **xoá quá tay** hoặc **xoá thiếu**? Marker nằm giữa một chuỗi TOML,
  trong comment, hay xuất hiện hai lần lồng nhau thì sao?
- `strip("\n")` cuối có ăn mất phần hợp lệ của người dùng ở ca nào không?
- Từ chối trả rc=3 mà hook chỉ **cảnh báo** rồi đi tiếp — đúng hay nên chặn?
- `t100` phủ đủ chưa? Ca nào bạn nghĩ ra mà nó không có?
- Thử trên bản sao config THẬT của tôi: 37→26 dòng, 9 `[projects]` giữ nguyên, `inherit`=0,
  TOML parse lại được, chạy lần hai no-op. **Đo lại giúp, đừng tin con số của tôi** — lượt
  6 đã cho thấy con số của tôi có thể sai.

## Việc còn treo, nói thẳng

Ba mục này KHÔNG đóng finding HIGH số 1 của bạn (suite giết caller). Chúng làm cho lượt sau
**định vị được** nó. Nếu bạn cho rằng phải đóng HIGH đó trước khi làm gì khác, nói thẳng.

## Bản khai + hai lượt `--dot-bien`

Dán lại bản khai môi trường của bạn; chạy `--dot-bien` **hai lần**. Lượt 7 hai bên lần đầu
ra cùng con số (`56/56`) — giữ chuỗi đó.

## CẢNH BÁO AN NINH

Không in **giá trị** biến môi trường hay token. Phản chứng đụng credential chạy trên
`HOME=$(mktemp -d)`; **không** đụng `~/.codex/auth.json` hay `~/.codex/config.toml` thật —
mọi phép thử policy phải dùng `--tep <tệp tạm>`.

## Verdict

`approve` · `changes_requested` · `blocked`. Bằng chứng **neo SHA bất biến**. `approve` hợp
lệ nếu thật sự không tìm ra gì.

Ghi verdict RA TỆP:

```
ops/reviews/moi-truong-review-8-codex-verdict.md
ops/reviews/moi-truong-review-8-codex-verdict.receipt.yaml
```

Xuất thẳng `stdout` ra tệp, báo `sha256` + số byte.
