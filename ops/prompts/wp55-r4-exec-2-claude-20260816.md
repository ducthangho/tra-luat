# Prompt EXECUTOR — wp55 revision 4, generation 2, lượt 2/3

**Vai:** `claude`. **Việc:** đóng ĐÚNG MỘT finding của cross-review lượt 1. Không hơn.

**Neo bất biến.** Đọc bằng SHA, không bằng tên nhánh. Tên nhánh dời được; SHA thì không.

| | |
|---|---|
| `start_from_sha` | `2432e3f64f05739741dfe6f49081e9aaa140799f` (head g1, đã review) |
| `base_sha` | `18da1da6a07ab2c86d716cef1d74ff2cd0e3218a` (tip master sau PR "#129") |
| nhánh | `claude/wp55-r4g1-f3-03` |
| spec | `ops/specs/wp55-r4-spec.md` trên `ops/wp55-r4-spec-draft` |
| `spec_hash` | `86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd` |
| verdict phải đóng | `ops/reviews/wp55-r4-review-1-codex-verdict.md` trên `ops/wp55-r4-review-1-codex-verdict` |
| reviewer lượt sau | `codex` — §8, executor là `claude` |

Trước khi sửa một dòng nào:

```bash
git show origin/ops/wp55-r4-spec-draft:ops/specs/wp55-r4-spec.md | sha256sum
# ĐÒI: 86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd
git rev-parse origin/claude/wp55-r4g1-f3-03
# ĐÒI: 2432e3f64f05739741dfe6f49081e9aaa140799f
```

Lệch ⇒ **DỪNG, hỏi chủ kho.** Head đã dời nghĩa là verdict lượt 1 nói về vật khác.

---

## Việc — một câu

Xoá hai hằng chết `C3_CU` và `C3_MOI` khỏi `.claude/dev/packet_loop_test.py`.

Đó là toàn bộ. Không sửa gì khác.

### Finding đang đóng, nguyên văn của reviewer

> `ac19-dead-exemption-mutation-anchors-remain` — Mức: P2 / phải sửa trước khi land.
>
> `packet_loop_test.py` vẫn định nghĩa `C3_CU` và `C3_MOI`; không chỗ nào dùng chúng.
> `C3_CU` chứa nguyên mỏ neo `_DAU_HIEU_PHEP_DO` của chốt miễn trừ cũ, còn `C3_MOI` chứa thân
> vô hiệu `if False`. Đây là mã chết phục vụ miễn trừ, không phải khối chú thích lịch sử, trái
> AC 19 mục 2 (phải **xoá**, không chỉ vô hiệu/để chết) và trái lời khai "không còn tham chiếu
> ngoài chú thích".

Đã tái lập độc lập trước khi cấp lease này — dòng `1928–1929`, đúng **2** lần xuất hiện trên
toàn `.claude/dev/`, **không consumer nào**:

```bash
git grep -n -E '\bC3_CU\b|\bC3_MOI\b' 2432e3f6 -- .claude/dev/packet_loop_test.py
git grep -c -E '\bC3_CU\b|\bC3_MOI\b' 2432e3f6 -- .claude/dev/   # ĐÒI: đúng 2
```

Finding này đứng vững, không tranh cãi. Đừng mở lại nó.

### Finding kia ĐÃ RÚT — đừng "sửa" nó

Reviewer đã **tự rút** `mutation-kill-set-omits-false-positive-case` sau khi đo lại: hai ca
`doctrine_scan_bat_qua_ngat_dong` và `ac19_bang_vai_tro_THAT_van_bi_bat` là ca VIẾT TAY đòi
`rc=6`, không thuộc `LOP_BAT_OAN`; trong đúng miền `LOP_LACH` mà danh sách tự khai thì
`37 khai/37 chết` và `43 khai/43 chết`, khớp tuyệt đối.

**KHÔNG sửa hai danh sách phải-chết. KHÔNG đổi `MUTANTS`. KHÔNG đổi hai ma trận.** Sửa chúng là
làm hỏng một thứ đang đúng vì tin một finding đã rút.

---

## Cách xoá — và chỗ dễ làm hỏng

`C3_CU` chứa nguyên văn một dòng mã của cơ chế miễn trừ cũ, `C3_MOI` chứa `if False:`. Chúng nằm
gần bảng `MUTANTS`. Đọc quanh chúng TRƯỚC khi cắt: nếu có một mục `MUTANTS` nào tham chiếu tới
chúng thì việc này không còn là "xoá hai dòng chết" nữa — **dừng và báo**, đừng tự quyết.

Đo trước, sửa sau:

```bash
grep -n -E '\bC3_CU\b|\bC3_MOI\b' .claude/dev/packet_loop_test.py
sed -n '1915,1935p' .claude/dev/packet_loop_test.py
```

Xoá cả dòng, không để lại biến rỗng, không thay bằng `None`, không comment chúng ra —
**mã bị comment ra vẫn là mã chết**, và đó chính là hạng lỗi finding này nói tới.

Chú thích lịch sử quanh đó (danh sách ba lớp lỗi sẽ quay lại nếu revision sau mở lại miễn trừ)
được phép GIỮ. Nó là chú thích, không phải mã.

---

## Nghiệm thu — số phải KHÔNG ĐỔI, và đó là chốt

Hai hằng ấy không ai dùng, nên xoá chúng **không được** làm đổi bất kỳ con số nào. Nền của g1:

```
ca               : 185
đột biến         : 34
lớp lách         : 78
ca bắt-oan       : 35
ngoại lệ AC 18   : 0
```

Chạy suite, đọc khối `SỐ LIỆU (đếm bằng máy)` mà AC 25 bắt nó tự in, và **đòi y hệt năm số
trên**. Một con số đổi ⇒ bạn vừa xoá nhầm thứ đang được dùng ⇒ **DỪNG**, đừng "sửa cho khớp".

Đây là chốt mạnh hơn "suite xanh": suite xanh chỉ nói không ca nào đỏ, còn năm con số bằng nhau
nói phạm vi không đổi.

Bốn phép đo, bắt `rc` NGAY SAU từng lệnh:

```bash
python3 -B .claude/dev/packet_loop.py doctrine-scan --root .          # ĐÒI 0
python3 -B .claude/dev/packet_loop_test.py                            # ĐÒI 0, và 185/185

MASTER=18da1da6a07ab2c86d716cef1d74ff2cd0e3218a
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary 18da1da..<head-moi> | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"        # ĐÒI 0
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"            # ĐÒI 0
```

**Chứng đường AC 20, bắt buộc:** chạy lại dòng cuối mà **BỎ** `GIT_DIR`. Nó PHẢI đỏ
(`fatal: not a git repository`). Nó xanh ⇒ điều kiện spec vừa thêm là thừa và cả AC 20 chỉ là
nghi lễ — đó là finding, và bạn phải khai.

Kiểm phạm vi: `git diff --stat 2432e3f6..<head-moi>` phải là **đúng 1 tệp**,
`.claude/dev/packet_loop_test.py`. Tệp thứ hai xuất hiện là ra ngoài phạm vi lượt này.

---

## AC 26 — sổ commit

**Đúng MỘT commit.** Thông điệp phải khai `lease_id: wp55-r4-exec-2-claude-20260816`.

Revision 3 hỏng đúng ở chỗ này — bốn commit chạy không lease — và hai trong số đó đẩy khi một
lease reviewer đang neo SHA cũ, làm hỏng lượt review 8. Commit không khai được lease là commit
ngoài sổ, và reviewer được quyền tính đó là finding.

**Backtick trong `git commit -m` bị shell nuốt.** Dùng `-F` với tệp. Đã mất ba lần.

---

## Sau khi xong

Head đổi ⇒ verdict lượt 1 hết hiệu lực (nó neo `2432e3f6`). Phải cấp **lease review 2** cho
`codex` neo head MỚI. Đừng đẩy thêm gì sau khi lease ấy được cấp — đó đúng là cách lượt review 8
của revision 3 bị hỏng.

Bàn giao §7 phải mang khối `SỐ LIỆU` **nguyên văn** do suite tự in (AC 25), và khai `lease_id`
mà commit chạy dưới (AC 26).

---

## Cạm bẫy đã trả giá

**Đọc `rc` qua ống là đọc `rc` của lệnh cuối.** `cmd | tail -3` rồi `$?` cho `rc` của `tail`.
Bắt `rc` ngay sau lệnh, hoặc dùng `PIPESTATUS`. Lỗi này đã lọt trong phiên cấp lease này.

**Phép đo rỗng còn tệ hơn không đo.** Mọi phép mô phỏng phải có chứng đường: một ca BIẾT PHẢI
ĐỎ. Nó không đỏ ⇒ phép đo hỏng, không phải cây sạch.

**`git push` trong phiên remote trả `403`** (proxy không tiêm credential cho kho này). Đường ghi
duy nhất là GitHub MCP `https://api.githubcopilot.com/mcp/`. Toolset `actions` nằm ở
`https://api.githubcopilot.com/mcp/x/actions`, không có ở endpoint mặc định.

**Không in nội dung biến bí mật.** Kiểm bằng `-n` và `${#VAR}`. Phiên cấp lease này đã vi phạm
một lần bằng `env | grep`, và giá trị vào thẳng transcript.

## Trần lượt

`attempts_limit: 3`, `attempts_used: 1` trước lượt này. Cạn trần ⇒ §12, dừng và bàn giao, không
tự gia hạn.
