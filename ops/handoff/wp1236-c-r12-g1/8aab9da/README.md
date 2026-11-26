# Handoff wp1236 đợt C — lượt 5, ứng viên `8aab9da` (revision 12, generation 1)

Nguồn có thẩm quyền của thư mục này là `handoff.yaml`; tệp này chỉ giải thích những chỗ một bảng YAML không nói hết.
Trả lời review mã lượt 4/6 trên `d5a7d85` (`ops/reviews/wp1236-c-r12-ma-4-codex/` trên `ops/wp1236-bc-lease`, `changes_requested`: C03 P1, C04 P2)
theo quyết định của chủ kho ở #1236 issuecomment-7180063460: chốt symlink của D2b đổi sang DANH SÁCH CHO PHÉP. Ứng viên CHƯA push, CHƯA có PR
(ADR-0060 M5/M12): lấy bằng bundle. Executor không tự review và không tự gán nhãn đóng lớp.

```bash
git fetch ops/handoff/wp1236-c-r12-g1/8aab9da/wp1236-c-8aab9da.bundle claude/wp1236-c-r12-g1:claude/wp1236-c-r12-g1   # cần base f602325
git rev-parse claude/wp1236-c-r12-g1            # 8aab9dabb6f3f150e4ab1872e37757c2620912c3
git rev-parse 'claude/wp1236-c-r12-g1^{tree}'   # 5474259bbb71e3be6e3f7d3eaf4661142906ca0d
git diff d5a7d85 8aab9da --stat                 # phần đổi của lượt 5: packet_loop.py +5 −4 · packet_loop_test.py +14 −6
```

**Thư mục này được đẩy làm hai bước**, như lượt 4. Bước 1: bundle và tệp này, để điều phối chạy M3 Windows tập trung song song với phép đo A/B của
executor. Bước 2 (commit kế tiếp, cùng nhánh): `handoff.yaml` và toàn bộ log. Chưa có `handoff.yaml` thì chưa có lời khai nào về A/B, luật 9 hay
bộ cổng trên `8aab9da`.

## 1. Vì sao lượt 4 hở

Lượt 4 hỏi "đích của symlink có phải một THƯ MỤC của danh mục cây không" và chặn nếu có. Đó là danh sách CẤM: nó phải đoán trước mọi cách viết tên
một thư mục. Reviewer chỉ ra ba cách viết nó không đoán được (khác hoa/thường, dấu `\`, dạng NFD của tên NFC): chuỗi đích không trùng mục nào của
danh mục, nên chốt cho qua; nền nào phân giải bí danh ấy thành thư mục và xếp symlink vào danh sách tệp thì K2 của module đợt A bỏ sót (C03). Cùng
lúc, phép chuẩn hoá văn bản xoá thành phần đứng trước `..` mà không biết nó có tồn tại không, nên một symlink hỏng bị coi là trỏ thư mục (C04).

## 2. Luật mới: danh sách cho phép

Nhánh `passed`, sau ba luật của lượt 3 và trước khi gọi `kiem_tep`: mỗi mục 120000 của `git ls-tree -r -t <oid> -- <thư mục provenance>` chỉ được
qua khi `posixpath.normpath(join(dirname(mục), readlink))` trùng TỪNG BYTE đường dẫn một mục kiểu tệp của CHÍNH danh mục ấy. Mọi trường hợp khác trả
`kiem_tep:not_measured:symlink` mà không gọi module: thư mục, gốc bản bung, bí danh, đích hỏng, đích ngoài thư mục provenance, symlink khác.

Một bí danh không bao giờ trùng từng byte, nên chốt không còn phải đoán cách viết. Ba dòng chốt của lượt 4 được THAY, không cộng thêm.

## 3. Ba chỗ executor đã chọn cách đọc, cần reviewer soi

- **"Cây" là danh mục cây con của thư mục provenance** (thứ được bung ra đĩa), không phải cả cây của `oid`. Đích `../lk5-provenance/ci.yaml` là một
  tệp thường có thật trong cây của `oid` nhưng không có trong bản bung: bị CHẶN. Đây là đọc chặt hơn chữ "cây git của oid" trong quyết định; điều
  phối đã đồng ý (02:05Z 26-11).
- **Chuẩn hoá là văn bản, đúng chữ quyết định.** Đích không chuẩn tắc mà chuẩn hoá ra tệp thường (`./ci.yaml`, `absent/../ci.yaml`) được QUA, kể cả
  khi nền coi nó là hỏng. Lập luận rằng nó không thể thành thư mục: nếu MỌI symlink của danh mục đều qua danh sách thì mỗi symlink hoặc hỏng hoặc
  phân giải tới đúng tệp thường ấy; không symlink nào phân giải tới thư mục, nên không symlink nào đi XUYÊN được một symlink khác như một thành phần
  thư mục, và phép `..` chỉ còn chạy trên thư mục thật (ở đó chuẩn hoá văn bản trùng phép phân giải của nền) hoặc trên thành phần hỏng (ở đó nền
  thất bại). Không có ca dương cho dạng này trên Python 3.13: bộ lọc `data` viết lại đích không chuẩn tắc, luật nội dung của lượt 3 ra rc 8 trước.
- **"Mục kiểu tệp" là mọi mode khác 040000 và 120000.** Gitlink (160000) rơi vào kiểu này về mặt mã, nhưng luật danh mục của lượt 3 đã ra rc 8 cho
  cây có gitlink trước khi tới đây (reviewer lượt 3 đo).

## 4. Siết K2 so với đặc tả r12 (chủ kho đã duyệt)

Symlink tệp không phải `*.yaml` mà hỏng, là bí danh, trỏ ngoài thư mục provenance hay trỏ symlink khác: r12 để module bỏ qua (rc 0), nay rc 12.
Phần K2 được giữ: symlink tệp không phải `*.yaml` trỏ đúng một tệp thường của danh mục vẫn qua (`symlink_ngoai_pham_vi_k2`, rc 0). Symlink `*.yaml`
vẫn do module bắt. Thứ tự báo như lượt 4: lý do `symlink` của D2b đứng trước lỗi K1 của tệp đánh giá.

## 5. Fixture và mô hình

`_D2B_TC`: bảy thư mục, mỗi thư mục một lớp tên ngoài danh sách (`lk8` bí danh THƯ MỤC khác hoa/thường · `lk9` bí danh TỆP khác hoa/thường · `lka`
dấu `\` · `lkb` hỏng · `lkc` ngoài thư mục provenance · `lkd` trỏ symlink khác · `lke` dạng NFD của tên NFC). Trên Linux module bỏ qua cả bảy (đều là
symlink tệp không phải `*.yaml`), nên thiếu chốt thì cổng trả rc 0: bảy biến thể này KHÔNG cần mô hình `os.walk` và đo được như nhau trên mọi nền.
Thư mục và gốc bản bung (`lk4`, `lk6`, `lk7`) vẫn cần mô hình `git_loi="tep"` trên Linux như lượt 4; đó là mô hình, không phải Windows.

Như lượt 4, symlink của fixture được ghi thẳng vào index (mode 120000) rồi do `tarfile` của nền tạo trong mã sản phẩm. `lke` là fixture đầu tiên có
tên ngoài ASCII trên đĩa; điều phối đã đo trước trên Windows rằng tên ấy đi qua `ls-tree`, `archive`, `tarfile`, `os.walk` nguyên byte.

## 6. Tệp trong thư mục

Bước 1: `README.md` · `wp1236-c-8aab9da.bundle`. Bước 2 thêm: `handoff.yaml` · `ab/` · `gate/` · `luat9/` · `cong_cu/`.
