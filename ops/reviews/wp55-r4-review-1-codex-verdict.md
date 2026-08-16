# Verdict wp55 revision 4 generation 1 — review 1 (codex)

```yaml
reviewed_sha: 2432e3f64f05739741dfe6f49081e9aaa140799f
spec_sha256: 86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd
reviewer_provider: codex
executor_provider: claude
verdict: do_not_land
```

Đã đo trên SHA bất biến nêu trên. `origin/claude/wp55-r4g1-f3-03` vẫn trỏ đúng SHA ấy ở lần
đọc lại cuối. Vá an ninh `4085bbf2` là tổ tiên (`rc=0`). Spec có đúng hash đã duyệt.

## Findings

### `mutation-kill-set-omits-false-positive-case`

`finding_id: mutation-kill-set-omits-false-positive-case`

Mức: P1 / chặn land.

Hai danh sách `phải-chết` không bằng tập chết thực tế khi chạy đột biến qua **toàn bộ** 185 ca:

- `mo_lai_mien_tru_ngat_dong`: khai 37, thực tế 38; thừa
  `doctrine_scan_bat_qua_ngat_dong`.
- `tha_vo_dieu_kien_nhu_generation_4`: khai 43, thực tế 44; thừa
  `ac19_bang_vai_tro_THAT_van_bi_bat`.

Ca thừa thứ hai là ca `ac19_*` (chiều BẮT-OAN), đúng điều kiện prompt quy định là finding.
Suite hiện chỉ chạy `phải-chết` cộng ba đối chứng khác họ, nên tự in 37/43 xanh mà không phát
hiện hai ca chết ngoài danh sách.

Tái lập (chạy từ cây archive của reviewed SHA; `GIT_DIR` trỏ vào kho hiện tại):

```bash
TREE=$(mktemp -d)
git archive 2432e3f64f05739741dfe6f49081e9aaa140799f | tar -x -C "$TREE"
GIT_DIR="$PWD/.git" TREE="$TREE" python3 -B - <<'PY'
import importlib.util, os, tempfile
from pathlib import Path
p = Path(os.environ["TREE"]) / ".claude/dev/packet_loop_test.py"
s = importlib.util.spec_from_file_location("packet_test", p)
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
goc = m.CANONICAL.read_text(encoding="utf-8")
for name in ("mo_lai_mien_tru_ngat_dong", "tha_vo_dieu_kien_nhu_generation_4"):
    tim, thay, khai = m.MUTANTS[name]
    than = goc
    for a, b in m._cap_thay_the(tim, thay):
        than = than.replace(a, b, 1)
    with tempfile.TemporaryDirectory() as td:
        script = Path(td) / "packet_loop.py"
        script.write_text(than, encoding="utf-8")
        ket = m.chay_suite(script, Path(td) / "cases")
    chet = {ten for ten, loi in ket.items() if loi is not None}
    print(name, "khai", len(khai), "thực", len(chet), "thừa", sorted(chet-set(khai)))
PY
echo "rc=$?"
```

Kết quả thật:

```text
mo_lai_mien_tru_ngat_dong khai 37 thực 38 thừa ['doctrine_scan_bat_qua_ngat_dong']
tha_vo_dieu_kien_nhu_generation_4 khai 43 thực 44 thừa ['ac19_bang_vai_tro_THAT_van_bi_bat']
rc=0
```

`rc=0` là rc của chính script đo; output là bất biến bị vi phạm. Phép đo có chứng đường dương:
cả hai tập chết đều chứa đủ toàn bộ danh sách khai (không thiếu ca), đồng thời phơi đúng ca
ngoài danh sách.

### `ac19-dead-exemption-mutation-anchors-remain`

`finding_id: ac19-dead-exemption-mutation-anchors-remain`

Mức: P2 / phải sửa trước khi land.

`packet_loop_test.py` vẫn định nghĩa `C3_CU` và `C3_MOI`; không chỗ nào dùng chúng. `C3_CU`
chứa nguyên mỏ neo `_DAU_HIEU_PHEP_DO` của chốt miễn trừ cũ, còn `C3_MOI` chứa thân vô hiệu
`if False`. Đây là mã chết phục vụ miễn trừ, không phải khối chú thích lịch sử, trái AC 19
mục 2 (phải **xoá**, không chỉ vô hiệu/để chết) và trái lời khai “không còn tham chiếu ngoài
chú thích”.

Tái lập:

```bash
git grep -n -E '\bC3_CU\b|\bC3_MOI\b' \
  2432e3f64f05739741dfe6f49081e9aaa140799f -- \
  .claude/dev/packet_loop_test.py
echo "rc=$?"
```

Kết quả thật: chỉ hai dòng định nghĩa ở dòng 1928–1929, `rc=0`; không có consumer nào.

## Bốn mục kiểm trọng tâm

1. **Cặp cùng hình dạng — đã đo.** Cả 12 `_tha_cu` có đối chứng nội dung riêng giữ cùng số
   dòng, rào, thụt lề, tag mở/đóng và vị trí ngắt dòng; chỉ cụm chữ vai trò được viết lại.
   Hai ca HTML đáng ngờ ánh xạ riêng: `...sau_bang_html_tha_cu` →
   `oan_van_xuoi_sau_bang_html`, còn `...chua_dong_tha_cu` →
   `oan_van_xuoi_sau_bang_html_chua_dong`. Cặp `claude_md_master` đều giữ bốn dòng và mức
   thụt hai dấu cách ở ba dòng nối.
2. **Hai đột biến — đã đo, không đạt.** Tập chết thật là 38/44 chứ không phải 37/43; đột
   biến thứ hai giết một ca `LOP_BAT_OAN`. Bỏ `tha_vo_dieu_kien_nhu_generation_4` để hở đúng
   sáu lớp một dòng: `cum_don_heading`, `dong_tran`, `gach_dau_dong`, `in_dam`,
   `dinh_nghia`, `cau_van_xuoi_mot_dong`.
3. **Số liệu — đã đo.** Suite với `GIT_DIR` trả `rc=0` và tự in nguyên văn
   `185 / 34 / 78 / 35 / 0`. `packet_loop.py` ở `start_from_sha` có 1503 dòng, ở head có
   1223: giảm 280; `280 / 1503 = 18,629...%`, làm tròn 18,6%. `_RE_BANG_HTML` không tồn tại
   ở `start_from_sha` (`git grep` trả `rc=1`). Phân hoạch đổi ma trận là đúng 12 ca chứa cụm
   cấm và 23 ca không chứa cụm vẫn xanh.
4. **Mã miễn trừ — đã đo, không đạt.** Các hàm/hằng executor liệt kê đã biến mất khỏi mã
   scanner; `_go_dau_dong` được `_khuc_chuan` gọi, `_RE_DAU_DONG` được `_go_dau_dong` dùng,
   `_dong_tai` được scanner gọi. Tuy nhiên hai hằng chết `C3_CU`/`C3_MOI` còn trong suite
   như finding trên. Khối lịch sử trong scanner chỉ là chú thích.

## Các phép đo còn lại

- Phạm vi diff `18da1da..2432e3f6`: đúng sáu tệp trong `write_set`, không có tệp thứ bảy.
- Cây merge dựng bằng archive base + apply binary diff: doctrine-scan `rc=0`; suite với
  `GIT_DIR="$PWD/.git"` `rc=0`. Cùng cây đó bỏ `GIT_DIR`: suite `rc=1`, nền 184/185 và
  `legacy_state_khong_co_lease_bi_chan` báo `fatal: not a git repository`; chứng đường AC 20
  có tác dụng.
- `origin/master` sau fetch vẫn là
  `18da1da6a07ab2c86d716cef1d74ff2cd0e3218a`; không cần đo lại trên tip mới.
- Sổ lượt: first-parent từ `start_from_sha` đến head có đúng hai commit của lượt
  (`179d5f37`, `2432e3f6`), và handoff gắn cả hai với
  `wp55-r4-exec-1-claude-20260816`. Lưu ý lệnh literal `git log 18da1da..2432e3f6` liệt kê
  19 commit vì nó còn đi theo phía lịch sử packet của merge; dùng nó để đòi tổng bằng 2 là
  sai hình học DAG. Không có commit thứ ba trên first-parent của lượt.
- Suite nền trên cây head với `GIT_DIR` đạt 185/185, `rc=0`. Không chạy ruff/release gate
  đầy đủ; đây là thiếu sót đã khai và ngoài điều kiện chặn của verdict này.

Kết luận: không land SHA này. Cần làm cho hai danh sách đột biến bằng đúng tập chết thực tế
(đặc biệt không được giết `LOP_BAT_OAN`), bổ sung chốt suite đo hai chiều trên phạm vi phù hợp,
và xoá hai hằng miễn trừ chết trước lượt review kế tiếp.
