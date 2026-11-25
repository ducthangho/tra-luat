# Handoff wp1236 đợt C — lượt 4, ứng viên `d5a7d85` (revision 12, generation 1)

Nguồn có thẩm quyền của thư mục này là `handoff.yaml`; tệp này chỉ giải thích những chỗ một bảng YAML không nói hết.
Trả lời biên nhận M3 Windows local ĐỎ trên `dbe650d` (#1236 issuecomment-7170894289) theo quyết định của chủ kho ở issuecomment-7170968907
(vá trong write set, trần Codex 4 → 6). Review mã lượt 3 đã approve `dbe650d`; SHA mới cần review lại. Ứng viên CHƯA push, CHƯA có PR
(ADR-0060 M5/M12): lấy bằng bundle. Executor không tự review và không tự gán nhãn đóng lớp.

```bash
git fetch ops/handoff/wp1236-c-r12-g1/d5a7d85/wp1236-c-d5a7d85.bundle claude/wp1236-c-r12-g1:claude/wp1236-c-r12-g1   # cần base f602325
git rev-parse claude/wp1236-c-r12-g1            # d5a7d8510af03e0d08545f677ad5de687e0264f4
git rev-parse 'claude/wp1236-c-r12-g1^{tree}'   # 241bd084f5979b02a1221d7d645e113227feee59
git diff dbe650d d5a7d85 --stat                 # phần đổi của lượt 4: packet_loop.py +6 −1 · packet_loop_test.py +14 −6
```

**Thư mục này được đẩy làm hai bước.** Bước 1 (commit đầu của nhánh handoff): bundle và tệp này, để điều phối chạy M3 Windows tập trung song song
với phép đo A/B của executor. Bước 2 (commit kế tiếp, cùng nhánh): `handoff.yaml` và toàn bộ log. Chưa có `handoff.yaml` thì chưa có lời khai nào
về A/B, luật 9 hay bộ cổng trên `d5a7d85`.

## 1. Cái gì đã lệch trên Windows

Ba luật của lượt 3 so bản bung với cây của `oid` ở tên, loại (tệp · thư mục · symlink) và nội dung. Trên Windows, symlink còn mang một thuộc tính
mà cây git KHÔNG có: LOẠI của nó (symlink tệp hay symlink thư mục), gắn lúc tạo. Hai đường đo được trên DESKTOP-T9R33P2 (Python 3.12.10):

- `git archive` xếp `d` (→ `sub`) trước `sub`; `tarfile` tạo `d` khi đích chưa có, nên `d` là symlink TỆP. `os.walk` của module đợt A xếp `d` vào
  danh sách tệp; K2 chỉ xét symlink trong danh sách thư mục và tệp `*.yaml` trong danh sách tệp, nên bỏ sót. D2b trả rc 0 thay vì rc 12 (M3 đỏ).
- symlink có đích chứa `/` không phân giải được trên Windows (`isdir` False dù đích là thư mục có thật), bất kể thứ tự bung (điều phối đo 18:41Z 25-11).

Cả ba luật lượt 3 đều đạt ở hai ca này: tên không trùng, danh mục khớp (`dia` hỏi `is_symlink()` trước `is_dir()`), đích `readlink` khớp blob.

## 2. Bản vá: K2 hỏi CÂY, không hỏi đĩa

Nhánh `passed`, sau ba luật và trước khi gọi `kiem_tep`: với mỗi mục 120000 của `git ls-tree -r -t`, đích được tính trên danh mục cây,
`posixpath.normpath(join(dirname(mục), readlink))`. Đích là một mục 040000 của cây, hoặc là gốc bản bung, thì D2b trả
`kiem_tep:not_measured:symlink` và không gọi module. Chuỗi `readlink` đã được luật nội dung ghim bằng băm blob ngay trước đó, nên phép tính chỉ
dùng dữ liệu của cây. Không lệnh nào hỏi đĩa về LOẠI của symlink.

Phạm vi K2 giữ nguyên (chủ kho chọn "Giữ phạm vi K2", điều phối chuyển 18:45Z 25-11): symlink tệp không phải `*.yaml` vẫn không bị xét
(`symlink_ngoai_pham_vi_k2` vẫn rc 0); symlink `*.yaml` vẫn do module bắt (nó hỏi `is_symlink()` trên từng tệp `*.yaml`, không phụ thuộc loại).

Chuỗi symlink không cần mã riêng: nếu một symlink phân giải tới thư mục qua symlink khác thì symlink trong cùng của chuỗi trỏ THẲNG tới thư mục
và tự nó bị bắt; phép kiểm là "có symlink NÀO trỏ thư mục". Vì không có dòng mã riêng nên không có đột biến riêng; fixture `lk7` có chuỗi `c` → `e`.

Phép chuẩn hoá là văn bản (`normpath`), nên với đích có `..` đứng SAU một thành phần là symlink hoặc không tồn tại, nó có thể coi là thư mục thứ
mà nền coi là treo. Hướng lệch ấy là chặn thừa (rc 12), không bỏ sót: symlink trong cùng của mọi chuỗi phân giải được luôn có đích tính đúng.

**Đổi hành vi trên mọi nền:** cây có symlink trỏ thư mục thì D2b báo `symlink` trước cả lỗi K1 của tệp đánh giá (trước đây module báo lý do K1
trước). Vẫn rc 12 `not_measured` ở cả hai.

## 3. Đối chiếu với mẫu có sẵn trong kho (chủ kho yêu cầu)

`_chup_workspace` (`.claude/dev/launcher.py`) có hai ý. (i) Nhận diện symlink bằng `islink`/`lstat` trên MỌI mục của cả hai danh sách của
`os.walk`, không tin cách `os.walk` xếp: D2b đã làm vậy từ lượt 3 (`dia` duyệt `ds + fs`, hỏi `is_symlink()` trước) và so hai chiều với mode của
cây, nên tập symlink trên đĩa = tập mục 120000; chốt mới chạy trên đúng tập ấy. (ii) Coi mọi symlink như nhau (`L`): D2b không theo nguyên dạng,
vì K2 phân biệt symlink trỏ thư mục với symlink tệp ngoài `*.yaml`; muốn giữ phân biệt ấy mà không hỏi nền thì chỉ còn cây.

Mục "Ca symlink Windows native" của `.claude/skills/work-packet/SKILL.md` (fixture dựng symlink thật phải khai `target_is_directory`, đích dùng `\`
trên Windows) áp cho fixture TỰ tạo symlink trên đĩa. Fixture `lk2`…`lk7` không làm thế: symlink được ghi thẳng vào index (mode 120000), đi qua
`git archive`, và symlink trên đĩa do chính `tarfile` của nền tạo trong mã sản phẩm — tức phần ấy đo hành vi của nền. Chỉ `_D2B_NEN` tự tạo symlink
trên đĩa (`gop` tới thư mục, nay có `target_is_directory=True`; `dich` tới tệp), cả hai đích không chứa `/`.

## 4. Ca Linux tái hiện Windows là MÔ HÌNH

`git_loi="tep"` thay `os.walk` trong tiến trình để xếp symlink trỏ thư mục vào danh sách tệp (đúng `thu=['sub'] tep=['d']` điều phối đo). Dưới
đột biến `d2b_k2_tin_dia` (bỏ chốt mới, tức hành vi của `dbe650d`) ba biến thể mô phỏng ra rc 0: tái hiện ca đỏ M3 trên Linux. Đó là mô hình của
executor về Windows, không phải Windows. Răng thật chỉ đo được bằng M3; ba biến thể KHÔNG mô phỏng đo Windows thật là
`yaml_thuong_kem_thu_muc_symlink` (`lk4`, symlink tạo trước đích), `symlink_tro_thu_muc[lk6]` (đích `../../..`, gốc bản bung) và
`symlink_tro_thu_muc[lk7]` (đích chứa `/` tới thư mục con, kèm chuỗi).

## 5. Tệp trong thư mục

Bước 1: `README.md` · `wp1236-c-d5a7d85.bundle`. Bước 2 thêm: `handoff.yaml` · `ab/` · `gate/` · `luat9/` · `cong_cu/`.
