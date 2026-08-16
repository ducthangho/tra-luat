# Verdict wp55 revision 4 generation 2 — review 2 (codex)

```yaml
reviewed_sha: 817598e2a3101c1e550dcba59bd7caea093264f6
spec_sha256: 86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd
reviewer_provider: codex
executor_provider: claude
verdict: approve
land_recommendation: land 817598e2a3101c1e550dcba59bd7caea093264f6
```

Đã đo trên SHA bất biến nêu trên. Sau lần fetch và lần đọc cuối,
`origin/claude/wp55-r4g1-f3-03` vẫn trỏ đúng SHA ấy. `origin/master` vẫn là
`18da1da6a07ab2c86d716cef1d74ff2cd0e3218a`; spec tại nhánh neo có đúng SHA-256 đã duyệt.

## Trạng thái finding lượt 1

`ac19-dead-exemption-mutation-anchors-remain`: **đã đóng**.

Tái lập:

```bash
git grep -n -E '\bC3_CU\b|\bC3_MOI\b' \
  817598e2a3101c1e550dcba59bd7caea093264f6 -- .claude/
echo "rc=$?"
```

Kết quả thật: không có output, `rc=1`. Hai hằng chết đã bị xoá.

```bash
git grep -n '_DAU_HIEU_PHEP_DO' \
  817598e2a3101c1e550dcba59bd7caea093264f6 -- .claude/
echo "rc=$?"
```

Kết quả thật: đúng một dòng ở `packet_loop_test.py:1973`, `rc=0`; dòng bắt đầu bằng `#` và
nằm trong khối chú thích lịch sử kể lại mười hai đột biến đã xoá, không phải mã. Quét rộng
các tên/hình dạng miễn trừ trong `packet_loop.py` và `packet_loop_test.py` không tìm thấy
hằng hay hàm khác chỉ phục vụ miễn trừ mà bị vô hiệu thay vì bị xoá. Khối lịch sử chủ ý giữ
vẫn nằm trong `packet_loop.py`.

Không có finding mới. Finding `mutation-kill-set-omits-false-positive-case` đã được rút ở
lượt 1 và không có phép đo mới nào đảo ngược kết luận đó, nên không được nêu lại.

## Bốn mục kiểm hẹp

1. **Finding đã đóng — đã đo, đạt.** Hai tên không còn; tham chiếu lịch sử duy nhất là chú
   thích; quét rộng không thấy mã miễn trừ chết cùng loại còn sót.
2. **Bảy dòng xoá — đã đo, đạt.** `git show 817598e2` cho thấy chỉ xoá hai hằng và khối chú
   thích bốn dòng cộng một dòng trống. Khối bốn dòng chỉ mô tả “chốt (3)” của
   `_duoc_tha_vi_ngat_dong` và cách dùng hai hằng ngay dưới; hàm/chốt đã bị xoá ở generation
   1. Nó không mang hợp đồng còn sống và không phải khối lịch sử được handoff giữ trong
   `packet_loop.py`, nên phần mở rộng xoá này là chính đáng.
3. **Năm số — đã đo, đạt.** Trên cây merged, suite tự in đúng: `ca: 185`, `đột biến: 34`,
   `lớp lách: 78`, `ca bắt-oan: 35`, `ngoại lệ AC 18: 0`; `rc=0`. Phạm vi suite không đổi.
4. **Phần finding đã rút — đã đo, đạt.** Lệnh dưới không có output, `rc=1`; generation 2
   không đụng `MUTANTS`, `LOP_LACH`, `LOP_BAT_OAN`, hay các vùng `ac18_`/`ac19_`:

```bash
git diff 2432e3f64f05739741dfe6f49081e9aaa140799f..817598e2a3101c1e550dcba59bd7caea093264f6 \
  -- .claude/dev/packet_loop_test.py | grep -E '^[+-]' | \
  grep -iE 'MUTANTS|LOP_LACH|LOP_BAT_OAN|ac18_|ac19_'
echo "rc=${PIPESTATUS[2]}"
```

## Phạm vi, cây merged và sổ commit

- Phạm vi tự đo khớp khai báo: `git diff --stat 2432e3f6..817598e2` cho đúng một tệp,
  7 dòng xoá, 0 dòng thêm; `git rev-list --count` cho `1`; commit chứa đúng
  `lease_id: wp55-r4-exec-2-claude-20260816`.
- Dựng cây bằng archive `18da1da6` rồi apply binary diff đến `817598e2`: apply `rc=0`.
  `python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"` quét 4 tệp,
  0 vi phạm, `rc=0`.
- Trên cùng cây, `GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"`
  đạt `185/185`, tự chứng minh đủ 34 đột biến, in năm số nêu trên và kết thúc `rc=0`.
- Chứng đường bắt buộc: bỏ `GIT_DIR` làm đúng ca
  `legacy_state_khong_co_lease_bi_chan` đỏ với `fatal: not a git repository`, nền
  `184/185`, `TỔNG: 1 lỗi`, `rc=1`. Điều kiện AC 20 có tác dụng, không phải phép đo rỗng.
- Hình học DAG của lượt này được đo bằng `2432e3f6..817598e2`: đúng một commit. Không dùng
  tổng commit từ base vì nhánh mang lịch sử packet qua merge như đã ghi ở lượt 1.

Kết luận: thay đổi hẹp đóng finding P2 duy nhất, không làm đổi phạm vi kiểm thử và không tạo
finding mới. Có thể land đúng SHA đã review.
