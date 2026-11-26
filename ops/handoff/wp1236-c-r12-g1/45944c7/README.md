# Handoff wp1236 đợt C — lượt 6, ứng viên `45944c7` (revision 12, generation 1)

Nguồn có thẩm quyền của thư mục này là `handoff.yaml`; tệp này chỉ giải thích những chỗ một bảng YAML không nói hết.
Trả lời review mã lượt 5/6 trên `8aab9da` (`ops/reviews/wp1236-c-r12-ma-5-codex/` trên `ops/wp1236-bc-lease`, `changes_requested`: C05 P2)
theo quyết định của chủ kho ở #1236 issuecomment-7182681531 ("Vá (a)+(b), gọi Codex 6/6"). Ứng viên CHƯA push, CHƯA có PR (ADR-0060 M5/M12):
lấy bằng bundle. Executor không tự review và không tự gán nhãn đóng lớp. Lượt Codex kế tiếp là lượt CUỐI (6/6).

```bash
git fetch ops/handoff/wp1236-c-r12-g1/45944c7/wp1236-c-45944c7.bundle claude/wp1236-c-r12-g1:claude/wp1236-c-r12-g1   # cần base f602325
git rev-parse claude/wp1236-c-r12-g1            # 45944c7c3f4c75beaa87f36138b2bba9fb9198a3
git rev-parse 'claude/wp1236-c-r12-g1^{tree}'   # 66a0f315c1cf27eaac67beae06ee20cd1789f23a
git diff 8aab9da 45944c7 --stat                 # phần đổi của lượt 6: packet_loop.py +6 −5 · packet_loop_test.py +18 −10
```

**Thư mục này được đẩy làm hai bước**, như lượt 4 và 5. Bước 1: bundle và tệp này, để điều phối chạy M3 Windows tập trung song song với phép đo
A/B của executor. Bước 2 (commit kế tiếp, cùng nhánh): `handoff.yaml` và toàn bộ log. Chưa có `handoff.yaml` thì chưa có lời khai nào về A/B, luật 9
hay bộ cổng trên `45944c7`.

## 1. Vì sao lượt 5 hở (C05)

Lượt 5 so đường dẫn đích sau chuẩn hoá với danh mục cây, từng byte. Luật của chủ kho còn một mệnh đề riêng: "đích chứa `\`" thì chặn. Trên POSIX
`\` là một byte hợp lệ của tên tệp, nên khi cây có đúng một tệp mang tên ấy và symlink trỏ tới nó, phép so byte ĐẠT và cổng đóng WP với rc 0.
Reviewer đo native trên Python 3.13.18 và 3.12.3 (`paths-*.json`, `modes.json`). Phép so byte không thực thi mệnh đề ấy; nó cần một điều cấm riêng.

## 2. Thay đổi: ba điều kiện, kiểm theo thứ tự trên từng symlink

Nhánh `passed`, sau ba luật của lượt 3, trước khi gọi `kiem_tep`. Với mỗi mục 120000 `t` của danh mục cây con thư mục provenance, `d = readlink(t)`,
`j = posixpath.join(dirname(t), d)`:

- **(a)** `j` không mang `\`. Kiểm TRƯỚC `normpath`, nên gồm cả đích thô lẫn thư mục chứa link. Không thay `\` bằng `/`, không casefold, không NFC.
- **(b)** `posixpath.normpath(d) == d`: đích thô đã ở dạng chuẩn tắc.
- **(c)** `posixpath.normpath(j)` trùng từng byte đường dẫn một mục kiểu tệp của danh mục (như lượt 5).

Sai một điều ở một symlink bất kỳ thì trả `kiem_tep:not_measured:symlink` (rc 12) mà không gọi module.

Vì sao có (b), dù reviewer không nêu thành finding: mệnh đề "đích hỏng hoặc không tồn tại" chưa được thực thi cho dạng `a/../x` khi `a` vắng. Phép
`normpath` xoá `a` mà không biết nó có tồn tại không, nên đích hỏng ấy chuẩn hoá ra đúng một tệp thường. `paths-*.json` của reviewer, chế độ
`retained_safe_link_text`, cho rc 0 ở `missing_parent`, `file_parent`, `chain_parent` (link có `exists=False`). Reviewer coi đó là mô hình vì hai
bản Python họ đo đều viết lại `linkname` trong `data_filter` (native ra rc 8). Bản vá ấy của `tarfile` không có trong mọi bản Python đang dùng: xem
mục 5. Với (b), một đích qua danh sách chỉ còn dạng `(../)*tên/tên/…`, các `..` chỉ đứng đầu và đi lên qua thư mục thật của danh mục, phần còn lại
là đường dẫn của một tệp thường có trong danh mục. Trên POSIX nó phân giải đúng tới tệp ấy, không cần lập luận chuỗi lồng của lượt 5.

Hệ quả có chủ đích của (b), chủ kho đã duyệt: `./x`, `a//b`, `sub/../x` cũng bị chặn, chặt hơn chữ "chuẩn hoá trên văn bản" của luật trước.

## 3. Bảng đối chiếu từng mệnh đề của luật với mã

Luật: issuecomment-7180063460, bổ sung ở issuecomment-7182681531. Cột "mã" là điều kiện nào ở mục 2 thực thi mệnh đề; cột "đột biến" là đột biến
khai báo mà gỡ đúng điều kiện ấy thì ca đích đỏ.

| mệnh đề của luật | mã | biến thể của `cong_d2b_c4_symlink` | đột biến `d2b_k2_*` |
|---|---|---|---|
| đích là thư mục | (c): mục kiểu thư mục không thuộc tập tệp | `lk4`, `lk7` (thật và mô hình `tep`) | `cho_thu_muc` |
| gốc bản bung | (c): `.` hay đường đi lên không thuộc tập tệp | `lk6` | `cho_goc` |
| bí danh khác hoa/thường | (c): so byte | `lk8` (thư mục), `lk9` (tệp) | `cho_hoa_thuong`, `cho_ten_lk8`, `cho_ten_lk9` |
| bí danh khác NFC | (c): so byte | `lke` | `cho_nfc`, `cho_ten_lke` |
| đích chứa `\` | (a) | `lka` (không có tệp nào tên ấy) · `lkf` (tệp 100644) · `lkg` (tệp 100755) · `lkh` (thành phần thư mục) · `lki` (link lồng) · `lkj` (link nằm trong thư mục `\`, đích thô sạch) | `bo_cam_cheo`, `cam_cheo_chi_dich_tho` (chỉ `lkj` bắt), `cho_cheo_nguoc` (chỉ `lka` bắt) |
| đích hỏng hoặc không tồn tại | (c) cho tên vắng; (b) cho dạng không chuẩn tắc | `lkb`; `nen_giu_nguyen_dich[lkl]` (mô hình `nguyen`) | `cho_ten_lkb`, `cho_ngoai_danh_muc`; `bo_chuan_tac` (chỉ `lkl` bắt) |
| đích ngoài cây | (c): tập tệp lấy từ danh mục cây con thư mục provenance | `lkc` | `cho_ten_lkc`, `cho_ngoai_danh_muc` |
| đích là một symlink khác | (c): mục kiểu symlink không thuộc tập tệp | `lkd` | `cho_symlink`, `cho_ten_lkd` |
| chỉ tệp thường 100644 / 100755 | KHÔNG có mã riêng: "kiểu tệp" là mọi mode khác 040000 và 120000. Gitlink (160000) không tới được chốt, luật danh mục ra rc 8 trước (`modes.json` của reviewer, kịch bản `gitlink`). Chủ kho duyệt không thêm mã (điểm c của quyết định) | không có | không có |
| symlink `*.yaml` vẫn do module bắt | không đổi: link `*.yaml` trỏ tệp thường qua danh sách rồi module trả `symlink` | `yaml_chi_la_symlink` (`lk2`), `yaml_thuong_kem_yaml_symlink` (`lk3`) | `d2b_loc_mat_symlink` |
| symlink tệp không phải `*.yaml` trỏ đúng tệp thường thì qua | cả ba điều kiện đúng | `symlink_ngoai_pham_vi_k2` (`lk5`, rc 0); `lk5` dưới mô hình `tep` và `nguyen` | `moi_symlink`, `dich_tho` |

Đột biến `tin_dia` bỏ cả chốt. `cho_ten_lka` của lượt 5 bị bỏ: `lka` nay bị (a) chặn, nới tập tệp cho tên ấy không đổi kết quả.

## 4. Fixture và mô hình

- `_D2B_TB` (năm thư mục `lkf`…`lkj`): cây CÓ THẬT một tên mang `\`. **Chỉ dựng trên POSIX.** Trên Windows bảng rỗng và năm biến thể vắng mặt, vì
  Git for Windows từ chối đường dẫn index mang `\`. Điều này executor suy từ mã `verify_path` của git, CHƯA đo trên Windows. Ở Windows chỉ còn
  `lka` đo điều cấm (đích có `\`, không có tệp tên ấy).
- Tệp 100755 của `lkg` đi thẳng vào index (giá trị `bytearray` trong bảng mục index), không qua `chmod` trên cây làm việc.
- `lkl` (`c → khong/../ci.yaml`) có trên mọi nền. Biến thể `nen_giu_nguyen_dich[lkl]` chạy trong tiến trình với mô hình `git_loi="nguyen"`: bộ lọc
  của `extractall` gọi `tarfile.data_filter` rồi trả lại `linkname` gốc. Đó là mô hình của một bộ bung không viết lại đích, không phải một bản Python
  cũ thật. `nen_giu_nguyen_dich[lk5]` là đối chứng dương của chính mô hình (rc 0).
- Ba fixture thư mục/gốc (`lk4`, `lk6`, `lk7`) vẫn cần mô hình `git_loi="tep"` trên Linux như lượt 4.

## 5. Hai điều về Python và Windows (executor không đo; phần đã đo là của điều phối)

- **Bản vá `tarfile` viết lại đích.** Trên Python 3.13.18 ở đây, `tarfile._get_filtered_attrs` gọi `os.path.normpath(member.linkname)` và ghi lại
  `linkname` (executor đọc mã). Điều phối đo riêng hàm `tarfile.data_filter` trên DESKTOP-T9R33P2 (báo 05:02Z 26-11): Python 3.12.10 GIỮ NGUYÊN
  `khong/../ci.yaml`; CPython 3.13.17 viết lại thành `ci.yaml`. Vậy trên 3.12.10 đích hỏng ấy tới được chốt của `8aab9da` và qua danh sách. Bản Python đầu
  tiên có bản vá (executor nhớ là 3.12.11 / 3.13.4) chưa được đo, và chưa ai chạy cả cổng D2b với đích ấy trên 3.12.10.
- **Nợ: Windows với Python có bản vá ấy.** `os.path.normpath` trên Windows là `ntpath.normpath`, đổi `/` thành `\`. Điều phối đo ở mức hàm trên
  CPython 3.13.17 (cùng máy): `../../..`, `sub/danh-gia-gate-output-3.txt`, `../lk5-provenance/ci.yaml` đều bị đổi mọi `/` thành `\`, không ném ngoại
  lệ. Hệ quả dự đoán: đích của `lk6`, `lk7`, `lkc` bị viết lại lúc bung, luật nội dung của lượt 3 ra rc 8, trong khi biến thể đòi rc 12, nên ca
  `cong_d2b_c4_symlink` ĐỎ trên interpreter ấy. Vẫn fail-closed. Tồn tại từ lượt 4; chủ kho quyết ghi nợ (issuecomment-7182681531), không vá ở lượt
  này. Kết quả ở mức ca, nếu có, nằm trong `handoff.yaml`.

## 6. Tệp trong thư mục

Bước 1: `README.md` · `wp1236-c-45944c7.bundle`. Bước 2 thêm: `handoff.yaml` · `ab/` · `gate/` · `luat9/` · `cong_cu/`.
