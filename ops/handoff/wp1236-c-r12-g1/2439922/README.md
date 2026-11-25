# Handoff wp1236 đợt C — lượt 2, ứng viên `2439922` (revision 12, generation 1)

Nguồn có thẩm quyền của thư mục này là `handoff.yaml`; tệp này chỉ giải thích những chỗ một bảng YAML không nói hết.
Trả lời review mã lượt 1 (`ops/reviews/wp1236-c-r12-ma-1-codex/` trên `ops/wp1236-bc-lease` @ `8ccc146`, `changes_requested`: C01 P1, C02 P2).
Ứng viên CHƯA push, CHƯA có PR (ADR-0060 M5/M12): lấy bằng bundle. Executor không tự review và không tự gán nhãn đóng lớp.

```bash
git fetch ops/handoff/wp1236-c-r12-g1/2439922/wp1236-c-2439922.bundle claude/wp1236-c-r12-g1:claude/wp1236-c-r12-g1   # cần base f602325
git rev-parse claude/wp1236-c-r12-g1            # 2439922c67a091c53e277c9e0b13d8fc04089453
git rev-parse 'claude/wp1236-c-r12-g1^{tree}'   # b2ba746fdbe08bff82d66467c0e9b0306fad38cd
git diff ac523ae 2439922 --stat                 # phần đổi của lượt 2: packet_loop.py +30 −18 · packet_loop_test.py +91 −43
```

## 1. Hai lớp của verdict, và những biểu hiện executor tự tìm thêm

Bảng đầy đủ ở `handoff.yaml` (`bang_doi_chieu_lop`). Tóm tắt cơ chế:

**`archive-loc-mat-du-lieu-kiem` (C01).** Validator của đợt A đọc một bản bung trên đĩa. Bản bung khác cây của `oid` ở đâu thì nó kết luận trên dữ
liệu không phải của `oid` ở đó. Reviewer chỉ ra một đường (bộ lọc tar bỏ symlink). Cùng cơ chế còn bốn đường nữa, đều đo được trên kho tạm:
`.gitattributes` của chính `oid` có `export-ignore` (tệp biến mất khỏi `git archive`), `eol=crlf` (byte bị đổi), nền không tạo được symlink
(`tarfile` chép đích của liên kết thành tệp thường), và hai tên chỉ khác hoa/thường trên hệ tệp không phân biệt.

Vá chung bằng một bất biến: **bản bung phải đúng là cây của `oid`**. Bung cả symlink, rồi đối chiếu từng mục của `git ls-tree -r -z` với đĩa
(symlink vẫn là symlink, tệp khớp băm blob, tập tên không trùng sau NFC + casefold). Lệch ⇒ rc 8, vì thứ hỏng là dụng cụ đo chứ không phải biên bản.
Symlink nào là vi phạm vẫn do module đợt A quyết theo K2; D2b không chép lại phạm vi ấy. Hai đối chứng giữ cho bản vá không siết oan:
`symlink_ngoai_pham_vi_k2` (symlink không phải `*.yaml`) và `mien_readback_kem_symlink` vẫn ĐẠT.

Hướng này khác gợi ý của VERDICT ("kiểm entry/mode trước giải nén"). Lý do và giá phải trả ghi ở `khac_huong_reviewer_goi_y`.

**`hop-dong-dau-ra-duong-dan-tu-do` (C02).** Theo quyết định E3 của chủ kho (#1236 issuecomment-7134458601): mỗi thành phần đường dẫn chỉ nhận ASCII
0x21–0x7E trừ `/`. Lớp ký tự `[!-.0-~]+` đặt ở cả bốn vị trí của hai regex, kiểm trên chuỗi thô trước mọi lệnh git và mọi dòng in. Tự tìm thêm cửa
thứ tư: dòng rc 8 chèn `str(ngoại lệ)`, nay dùng `repr`.

## 2. Thứ tự chốt đổi so với lượt 1 (đo trên hai clone, cùng script)

Biên bản vừa sai đường dẫn vừa có OID không trên remote (`gate/hai_loi.log`):

| ứng viên | stderr |
|---|---|
| `ac523ae` | `THIẾU  D2b oid_khong_tren_remote` |
| `2439922` | `THIẾU  D2b duong_dan_sai` |

Cả hai đều in đúng một dòng lý do, ở cả nhánh `passed` lẫn nhánh miễn. Lý do đổi: mọi chốt thuần chuỗi chạy trước mọi phép đo trên kho, nên lý do
của một biên bản sai cú pháp không còn phụ thuộc kho đã fetch hay chưa. Ở `ac523ae` cũng không lệnh git nào nhận đường dẫn trước khi regex chạy;
thứ thay đổi là thứ tự. Ca khoá: `cong_d2b_c9_oid/hai_loi_khoa_thu_tu`; đột biến khoá: `d2b_duong_dan_sau_git`.

## 3. Phép đo không hồi quy base ↔ head

Thư mục `ab/`. Hai clone đầy đủ dựng trong một lệnh (`ab/cong_cu/ab_dung.sh`), chạy xen kẽ trong một lệnh (`ab/cong_cu/ab_du.sh`), mỗi vế đủ 16
mảnh nền (`--manh i/16`), job gom, và 16 mảnh đột biến (`--dot-bien j/16`, mảnh 0 chạy hai ca `CA_DAI`). Bảng số từng mảnh và ba kết luận
(i)(ii)(iii) ở `ab/bang_so.md`, dựng bằng `ab/cong_cu/ab_so.py` từ `ab/ab.tong` và log từng mảnh.

Cách đọc hai bảng: cột "ok" đếm số DÒNG `ok … → giết` trong log của mảnh, gồm cả phần tự chứng minh suite không rỗng ở đầu log; con số trong
dòng `MẢNH:` ("lượt đột biến") đếm riêng. Kết luận (ii) tính theo TÊN đột biến, không theo số dòng.

Một đột biến đỏ ở cả hai vế: `r1187_spec_packet_type` (ca đích chỉ chết vì CLI sập, bộ phân hạng xếp tín dụng giả). Đỏ sẵn, delta 0; đo ở Python
3.13.18, chưa đo ở 3.12 của CI. Vì nó, mảnh đột biến 9 của base và mảnh 3 của head thoát rc 1.

## 4. Luật 9

Cách áp như lượt 1 (reviewer đã chấp nhận): bộ quét ghim `ops/reviews/wp1236-r10-soan/quet_dot_bien.py` (sha256 `1b3e4a9e…`, không sửa) chạy trên
khối D2b cắt nguyên văn, qua bộ nối `luat9/d2b_noi.py`. Tái lập từ gốc kho đang ở `2439922`, cây sạch:

```bash
D=ops/handoff/wp1236-c-r12-g1/2439922/luat9      # hoặc bản chép của thư mục này
python3 $D/d2b_noi.py trich .claude/dev/packet_loop.py /tmp/d2b_trich.py && sha256sum /tmp/d2b_trich.py
WP1236C_GOC="$PWD" python3 ops/reviews/wp1236-r10-soan/quet_dot_bien.py do /tmp/d2b_trich.py $D/d2b_noi.py $D/kho_rong.jsonl --thu-muc-ra /tmp/D --song-song 4
python3 $D/ledger.py /tmp/D /tmp/d2b_trich.py /tmp/ledger_A.tsv
```

Sổ từng ID ở `luat9/ledger_A.tsv`. Đột biến sống đều có chứng minh tương đương, neo theo dòng đột biến (`luat9/ledger.py`, bảng `TUONG_DUONG`).

## 5. Tệp trong thư mục

`handoff.yaml` · `wp1236-c-2439922.bundle` · `ab/` (bảng số, `ab.tong`, log 16 + 16 mảnh và `gom.log` của mỗi vế, bản ghi `manh-*.json`, script
dựng và chạy) · `gate/` (`gate2.tong`, `dot_bien_khai_bao.log`, đuôi log selftest và `ci_dang_ky_test`, `ruff_head.log`, `hai_loi.log`,
`autocrlf.log`, `archive_that.log`, `bundle_verify.log`) · `luat9/` (bộ nối, khối cắt, kho rỗng, `do.log`, `ledger.py`, `ledger_A.tsv`, thư mục `D`)
· `cong_cu/` (script nháp của executor đã dùng để đo; không phải cổng).
