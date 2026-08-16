# Prompt EXECUTOR — wp55 revision 4, lượt 1/3

**Neo bất biến.** Đọc bằng SHA, không bằng tên nhánh. Tên nhánh dời được; SHA thì không.

| | |
|---|---|
| spec | `ops/specs/wp55-r4-spec.md` trên `ops/wp55-r4-spec-draft` |
| `spec_hash` | `86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd` |
| `base_sha` | `18da1da6a07ab2c86d716cef1d74ff2cd0e3218a` (tip master, sau PR #129) |
| `start_from_sha` | `b0e3e3b6a4c630ba0652b8fc939025d9c4031c67` (head nhánh packet r3) |
| reviewer | `codex` — §8 cross-provider, executor là `claude` |

Trước khi đọc tiếp, xác minh spec chưa bị đổi dưới chân:

```bash
git fetch origin ops/wp55-r4-spec-draft
git show origin/ops/wp55-r4-spec-draft:ops/specs/wp55-r4-spec.md | sha256sum
# ĐÒI: 86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd
```

Lệch ⇒ **DỪNG**. Một spec khác với spec được duyệt không phải spec được duyệt.

---

## Việc, gọn trong ba câu

1. **Xoá hẳn** cơ chế miễn trừ AC 19 khỏi `packet_loop.py` — xoá, không vô hiệu.
2. Chuyển hai ca chiều-tha sang ma trận LỌT, giữ nguyên mọi ca bắt-oan khác.
3. Đo lại trọn bộ, kể cả trên **cây đã merge** theo công thức AC 20 đã sửa.

Chi tiết ở spec. Prompt này chỉ nói những chỗ prompt biết mà spec không tiện nói.

---

## BƯỚC 0 — bốn phép đo phải chạy TRƯỚC khi sửa một dòng nào

Cả bốn đều đã sập ít nhất một lần trong revision 3. Đây không phải thủ tục.

### 0.1 · Không bỏ mất bản vá P1 an ninh

```bash
git merge-base --is-ancestor 4085bbf2 <head-ban-dang-dung>; echo "rc=$?"   # ĐÒI rc=0
```

`4085bbf2` vá chỗ `SKILL.md` nối `${VAR:+…}` với `${VAR:-…}` — ở nhánh "đã đặt" nó bung ra
**chính giá trị** của biến bí mật, trong một lệnh hướng dẫn agent chạy với refresh token
thật. `SKILL.md` nằm trong `write_set`, nên xuất phát sai chỗ sẽ **mở lại lỗ ấy trong im
lặng**. Bản thảo spec đầu tiên ghi `start_from_sha: 1a4525a` và đã bị sửa đúng vì lý do này.

### 0.2 · Merge master 18da1da TRƯỚC khi đo AC 19

Không tuỳ chọn. `b0e3e3b6` merge master ở mức `d5b7bcc`, và `CLAUDE.md` của `d5b7bcc` vẫn
còn cụm cấm ở dòng 82. Đo trên chính `b0e3e3b6`:

```
r3g5 (còn miễn trừ)  ->  rc=0
r4   (bỏ miễn trừ)   ->  rc=6   CLAUDE.md:82 'người có thẩm quyền'
```

Không merge master thì sẽ đuổi theo một finding mà **bản vá đã nằm sẵn trên master**.

### 0.3 · AC 26 — không commit nào không có lease

```bash
git fetch origin 'refs/heads/ops/*:refs/remotes/origin/ops/*'
# 1. lease EXECUTOR còn sống, neo đúng head xuất phát, chưa hết hạn?  Không ⇒ DỪNG.
# 2. lease REVIEWER còn sống neo một SHA trên nhánh này?              Có   ⇒ DỪNG, hỏi.
```

Revision 3 có **bốn** commit không lease; hai trong số đó đẩy khi một lease reviewer đang
neo SHA cũ, làm hỏng lượt review 8 và phải cấp lại. Handoff §7 phải khai `lease_id` mà mỗi
commit chạy dưới.

### 0.4 · Tái lập ba lỗi lượt 10, đừng nhận theo lời kể

Spec khẳng định cả ba `rc=6` trên bản không miễn trừ — **tự đo lại**. Ma trận đầy đủ ở
`ops/reviews/wp55-r3-review-10-codex-verdict.md`, nhánh `ops/wp55-r3-review-10-verdict`.

---

## Cạm bẫy đã trả giá — đọc trước khi gõ

**Đọc `rc` qua ống là đọc `rc` của lệnh cuối.** `cmd | head -1` cho `rc` của `head`. Bắt
`rc` ngay sau lệnh, hoặc dùng `PIPESTATUS`. Lỗi này đã lọt một lần và làm một cổng đỏ báo
xanh.

**Phép đo rỗng còn tệ hơn không đo.** Một lượt trước dò một hàm bằng tên đoán, `hasattr`
trả `False`, và cả bốn ca cùng ra `rc=0` — trông như "sạch". Mọi phép mô phỏng phải có
**chứng đường**: một ca BIẾT PHẢI ĐỎ. Nó không đỏ ⇒ phép đo hỏng, không phải cây sạch.

**Backtick trong `git commit -m` bị shell nuốt.** Dùng `-F` với tệp. Đã mất ba lần.

**In phản hồi thô trước, phân tích sau.** Một lời gọi API đã thành công nhưng trình phân
tích nuốt kết quả và in `PR #None`; lượt gọi lại trả `422 already exists`.

**Không in nội dung biến bí mật.** Kiểm bằng `-n` và `${#VAR}`, không bao giờ bằng
expansion nối chuỗi. Đây chính là lỗ `4085bbf2` vá.

---

## Điều kiện nghiệm thu — chép từ spec, không diễn giải lại

**AC 19 mới**, bốn mục:

1. Không tệp nào trong `write_set` chứa cụm cấm ở **bất kỳ hình dạng nào** — đo cả trên
   nhánh LẪN trên cây đã merge.
2. Mọi hàm và hằng số phục vụ miễn trừ bị **XOÁ**, không phải bị vô hiệu. Danh sách spec
   nêu: `_duoc_tha_vi_ngat_dong`, `_dong_khoi_ma`, `_dong_bang_html`, `_go_dau_dong_tho`,
   cộng 8 hằng/regex. **Đo lại số dòng thật, đừng chép `~241` từ spec** — spec cũng chỉ
   ước lượng.
3. Suite giữ chiều bắt oan: văn bản KHÔNG chứa cụm cấm phải `rc=0`, kể cả khi có bảng,
   khối mã, tag, comment, dấu đầu dòng.
4. Hai ca chiều-tha chuyển sang ma trận LỌT, **kèm lý do ghi tại chỗ**.

**AC 20** — công thức đã sửa, `GIT_DIR` là phần bắt buộc:

```bash
MASTER=18da1da6a07ab2c86d716cef1d74ff2cd0e3218a     # sha40 bất biến, KHÔNG dùng origin/master
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary <base>..<head> | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

**AC 25** — suite tự in khối `SỐ LIỆU (đếm bằng máy)`; mọi con số vào handoff/commit/lease
**chép từ đó**, không gõ lại. Executor một lượt trước khai `39 đột biến` trong khi thật là
`38`.

**AC 18** giữ nguyên: danh sách ĐÓNG các lớp né **trước** khi vá, mỗi lớp một phản chứng và
một đột biến giết đúng ca đó. Qua bốn lượt, danh sách đóng luôn tìm ra nhiều hơn reviewer
nêu (18 so với 2, 18 so với 4, 18 so với 9).

---

## Cái giá phải khai thẳng, không giấu trong handoff

Bỏ miễn trừ nghĩa là **văn xuôi thật kể lại một phép đo, có cụm cấm ngắt dòng, nay sẽ ĐỎ**.
Hai ca đang có trong suite sẽ chuyển ma trận. **Đó là hợp đồng mới, không phải hồi quy** —
nhưng phải nói ra bằng đúng chữ ấy, ở cả commit lẫn handoff. Reviewer có quyền tính việc
im lặng về chuyện này là finding.

Nếu trong lúc đo phát hiện thêm ca nào khác đổi chiều ngoài hai ca spec nêu: **báo, đừng tự
quyết**. Spec nói thẳng "có thể còn ca khác" và giao việc đo cho executor, không giao việc
chọn.

## Trần lượt

`attempts_limit: 3`, đếm lại từ 0 cho revision 4. Cạn trần ⇒ §12, dừng và bàn giao, không
tự gia hạn.
