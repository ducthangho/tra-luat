# Prompt REVIEWER — wp55 revision 4, generation 2, lượt review 2

**Vai:** `codex`. §8 bắt reviewer khác provider; executor vẫn là `claude`.
**Quyền:** `read-only`. `write_set: []`, `branch_ownership: none`. KHÔNG commit, KHÔNG push lên
`claude/wp55-r4g1-f3-03`, KHÔNG sửa spec.

**Neo bất biến.** Đọc bằng SHA, không bằng tên nhánh.

| | |
|---|---|
| head để review | `817598e2a3101c1e550dcba59bd7caea093264f6` |
| head lượt trước | `2432e3f64f05739741dfe6f49081e9aaa140799f` (bạn đã review, verdict `do_not_land`) |
| `base_sha` | `18da1da6a07ab2c86d716cef1d74ff2cd0e3218a` (tip master, KHÔNG đổi từ g1) |
| nhánh | `claude/wp55-r4g1-f3-03` |
| spec | `ops/specs/wp55-r4-spec.md` trên `ops/wp55-r4-spec-draft` |
| `spec_hash` | `86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd` |
| verdict lượt 1 | `ops/reviews/wp55-r4-review-1-codex-verdict.md` trên `ops/wp55-r4-review-1-codex-verdict` |

Không có pull request. Review neo thẳng vào SHA.

---

## Đây là lượt review HẸP — nói rõ để bạn không đo lại cả packet

Generation 2 chỉ làm một việc: đóng finding P2 duy nhất còn lại của verdict lượt 1. Diff so với
head bạn đã review là **7 dòng xoá, 1 tệp**. Mọi thứ khác bạn đã đo ở lượt 1 trên `2432e3f6`.

Nhưng **"executor bảo diff nhỏ" không phải phép đo**. Việc đầu tiên là tự xác minh phạm vi:

```bash
git fetch origin claude/wp55-r4g1-f3-03
git rev-parse origin/claude/wp55-r4g1-f3-03      # ĐÒI 817598e2a3101c1e550dcba59bd7caea093264f6
git diff --stat 2432e3f6..817598e2               # ĐÒI đúng 1 tệp, 7 dòng xoá, 0 dòng thêm
git rev-list --count 2432e3f6..817598e2          # ĐÒI đúng 1
git log -1 --format=%B 817598e2 | grep lease_id  # ĐÒI wp55-r4-exec-2-claude-20260816
```

Bất kỳ dòng nào lệch ⇒ phạm vi lớn hơn khai báo, và **toàn bộ phần "đã đo ở lượt 1" mất hiệu
lực** — khi ấy phải review lại như một head mới. Lệch thì nói ra, đừng thu hẹp cho vừa prompt.

---

## Bốn mục kiểm

### 1 · Finding đã đóng THẬT chưa

```bash
git grep -n -E '\bC3_CU\b|\bC3_MOI\b' 817598e2 -- .claude/     # ĐÒI: rỗng
git grep -n '_DAU_HIEU_PHEP_DO' 817598e2 -- .claude/
```

Lệnh thứ hai còn **đúng một** dòng — kiểm nó là **chú thích** (dòng bắt đầu bằng `#`, kể lại 12
đột biến đã xoá) chứ không phải mã. Nếu nó là mã thì finding chưa đóng.

Quét rộng hơn tên: còn hằng/hàm nào khác chỉ phục vụ miễn trừ mà bị **vô hiệu** chứ không bị
**xoá** không? AC 19 mục 2 đòi xoá. Lượt 1 bạn tìm ra `C3_CU`/`C3_MOI` bằng cách này; lần này
quét lại xem còn anh em nào.

### 2 · Executor xoá 7 dòng, không phải 2 — phần thừa có chính đáng không

Finding của bạn chỉ nêu hai hằng. Executor xoá thêm **khối chú thích 4 dòng** ngay trên chúng,
lý do khai trong commit: khối ấy mô tả *"chốt (3) của `_duoc_tha_vi_ngat_dong`"*, mà hàm đó đã bị
xoá ở generation 1, nên giữ lại là để một chú thích trỏ vào hư không.

Đây là **mở rộng phạm vi so với finding**. Xét:

- Khối ấy có thật sự chỉ nói về hai hằng vừa xoá không, hay nó còn mang thông tin cho thứ khác?
- Nó có phải **khối chú thích lịch sử** mà handoff g1 cố ý giữ không? (Executor khai là KHÔNG —
  khối lịch sử nằm trong `packet_loop.py`, không phải `packet_loop_test.py`.) Tự kiểm.
- Nếu bạn thấy khối ấy đáng giữ thì việc xoá nó là finding. Nếu đồng ý thì nói rõ đã xét.

Đọc `git show 817598e2` để thấy đúng 7 dòng bị bỏ.

### 3 · Năm con số phải KHÔNG ĐỔI

Hai hằng bị xoá không ai dùng, nên phạm vi suite phải giữ nguyên. Nền g1:

```
ca               : 185
đột biến         : 34
lớp lách         : 78
ca bắt-oan       : 35
ngoại lệ AC 18   : 0
```

Chạy suite trên `817598e2`, đọc khối `SỐ LIỆU (đếm bằng máy)` mà AC 25 bắt nó tự in, đòi **y hệt
năm số trên**. Một số đổi nghĩa là đã xoá nhầm thứ đang được dùng.

Chốt này mạnh hơn "suite xanh": suite xanh chỉ nói không ca nào đỏ; năm số bằng nhau nói phạm vi
không đổi.

### 4 · Thứ bạn đã RÚT có bị "sửa" không

Ở lượt 1 bạn tự rút `mutation-kill-set-omits-false-positive-case` sau khi đo lại. Lease g2 đã
cảnh báo executor **không được** đụng `MUTANTS`, hai danh sách phải-chết, hay hai ma trận. Xác
minh executor tuân thủ:

```bash
git diff 2432e3f6..817598e2 -- .claude/dev/packet_loop_test.py | grep -E '^[+-]' | grep -iE 'MUTANTS|LOP_LACH|LOP_BAT_OAN|ac18_|ac19_'
# ĐÒI: rỗng
```

Không rỗng ⇒ executor đã đi sửa một thứ đang đúng vì tin một finding đã rút. Đó là finding.

Và: **đừng nêu lại finding bạn đã rút** trừ khi có phép đo MỚI cho thấy việc rút là sai. Rút rồi
nêu lại mà không có số mới thì lượt review sau không tin được lượt nào.

---

## Phải đo trên CÂY ĐÃ MERGE (AC 20)

```bash
MASTER=18da1da6a07ab2c86d716cef1d74ff2cd0e3218a
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary 18da1da..817598e2 | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

Executor báo `rc=0` cả hai. **Chứng đường bắt buộc:** chạy lại dòng cuối mà BỎ `GIT_DIR` — nó
PHẢI đỏ. Executor đo được `rc=1`, ca đỏ là `legacy_state_khong_co_lease_bi_chan` với
`fatal: not a git repository`. Tái lập. Nó xanh ⇒ điều kiện spec vừa thêm là thừa và cả AC 20
chỉ là nghi lễ — finding lớn.

`18da1da` vẫn là tip master lúc cấp lease này (đã đo). Kiểm lại: master tiến thêm thì phải đo lại
AC 20 trên tip mới, vì AC 20 nói *cây đã merge*, không nói *cây tại base_sha*.

---

## AC 26 — sổ commit

Đúng **một** commit từ `2432e3f6`, khai `lease_id: wp55-r4-exec-2-claude-20260816`.

Lưu ý hình học DAG mà chính bạn đã ghi ở verdict lượt 1: `git log 18da1da..817598e2` liệt kê
nhiều commit vì nó đi cả nhánh lịch sử packet của merge. Dùng `2432e3f6..817598e2` cho lượt này.

---

## Điều phải biết về thẩm quyền ở lượt này

Phiên `claude` vừa rồi **vừa thực thi generation 2, vừa soạn lease review này**. Đó là hai vai
khác nhau nhưng cùng một phiên, và nó không tự cấp quyền cho mình: `granted_by` là `ducthangho`,
người đã duyệt trực tiếp, và cổng `ops/lease_publish.py` chặn cứng mọi tên provider ở trường đó.

Nói ra để bạn biết mà soi kỹ hơn, không phải để trấn an. Cụ thể: **đừng tin phần khai trong
commit và trong lease** — cả hai do chính phiên thực thi viết. Đo lại từ cây.

---

## Verdict — dạng và chỗ đặt

Ghi `ops/reviews/wp55-r4-review-2-codex-verdict.md`. **KHÔNG commit, KHÔNG push, KHÔNG tạo
nhánh** — môi trường chặn `403` ở `git push`, lượt trước đã mất thì giờ ở đó. Chỉ ghi tệp; phiên
gọi sẽ đăng hộ nguyên văn và đọc ngược về đối chiếu byte.

Verdict phải mang:

- `reviewed_sha: 817598e2a3101c1e550dcba59bd7caea093264f6` — đúng SHA bạn đã đo.
- `spec_sha256` bạn đã xác minh.
- `verdict`: `approve` | `approve_with_findings` | `do_not_land`.
- `land_recommendation` nếu `approve`.
- Trạng thái finding lượt 1: `ac19-dead-exemption-mutation-anchors-remain` đã đóng hay chưa.
- Mỗi finding mới một `finding_id` kebab, kèm **lệnh tái lập và `rc` thật**.
- Bốn mục kiểm trên: nói rõ từng mục **đã đo** hay **chưa đo**. "Không kiểm được" khác "đạt".

Nếu head dời khỏi `817598e2` giữa chừng: **DỪNG**, báo chủ kho.

## Cạm bẫy

**Đọc `rc` qua ống là đọc `rc` của lệnh cuối.** Bắt `rc` ngay sau lệnh hoặc dùng `PIPESTATUS`.

**Phép đo rỗng còn tệ hơn không đo.** Mọi phép mô phỏng phải có chứng đường: một ca BIẾT PHẢI ĐỎ.
Nó không đỏ ⇒ phép đo hỏng, không phải cây sạch.

## Trần lượt

`attempts_limit: 3`, `attempts_used: 2`. Còn đúng MỘT attempt nội dung. Nếu lượt này ra
`do_not_land`, executor chỉ còn một lượt sửa trước khi §12 buộc dừng và bàn giao — cân nhắc điều
đó khi phân mức finding, nhưng **đừng hạ chuẩn vì sắp cạn trần**: một finding thật vẫn phải nêu.
