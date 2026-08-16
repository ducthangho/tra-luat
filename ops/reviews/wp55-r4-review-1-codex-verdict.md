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
2. **Hai đột biến — đã đo, đạt trong miền khai báo.** Trong `LOP_LACH`, tập chết khớp tuyệt
   đối danh sách khai: 37/37 và 43/43. Hai ca chết thêm khi chạy toàn bộ 185 ca đều là ca
   dương đòi scanner bắt, không phải ca `LOP_BAT_OAN`; xem mục xét lại dưới đây.
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

## Xét lại sau phản chứng

Đã chạy lại cả ba phản chứng từ archive của đúng
`2432e3f64f05739741dfe6f49081e9aaa140799f`, với `GIT_DIR` trỏ kho hiện tại, và bắt `rc`
ngay sau Python (`python_rc=0`). Kết quả:

- Đọc mã và kiểm membership xác nhận `doctrine_scan_bat_qua_ngat_dong` không thuộc
  `LOP_BAT_OAN`; `bang_vai_tro_THAT_van_bi_bat` cũng không thuộc `LOP_BAT_OAN`.
  `case_doctrine_scan_bat_qua_ngat_dong` gom lỗi khi `rc != 6`; ca viết tay
  `case_ac19_bang_vai_tro_THAT_van_bi_bat` gọi `_doi(6, rc, ...)`.
- Tiền tố `ac19_` thật sự có hai nguồn: bảng `CASES` đăng ký ca viết tay
  `ac19_bang_vai_tro_THAT_van_bi_bat`, còn comprehension sinh các ca khác từ
  `LOP_BAT_OAN`. Suy tiền tố thành membership là sai.
- Với mutant `mo_lai_mien_tru_ngat_dong`, miền `LOP_LACH` khớp 37 khai/37 chết. Ca chết
  ngoài miền là `doctrine_scan_bat_qua_ngat_dong`; chứng đường cho thấy cả 6/6 biến thể
  đáng lẽ phải đỏ đều thật sự nhận `rc=0` trên mutant.
- Với mutant `tha_vo_dieu_kien_nhu_generation_4`, miền `LOP_LACH` khớp 43 khai/43 chết.
  Ca chết ngoài miền là ca viết tay `ac19_bang_vai_tro_THAT_van_bi_bat`; lỗi thật là
  “đòi `rc=6`, được `rc=0`”. Đây là ca BẮT đúng bị mutant làm lọt, không phải ca BẮT-OAN.

Vì bàn giao khai rõ danh sách phải-chết được đo trên `LOP_LACH`, hai danh sách không thiếu
hay thừa phần tử trong chính miền ấy. Finding `mutation-kill-set-omits-false-positive-case`
đã dựa trên việc phân loại nhầm ca viết tay `ac19_*` thành `LOP_BAT_OAN`; tôi **rút finding
này**, không hạ mức và không thay bằng finding mới. Sự nhập nhằng tiền tố là một rủi ro đặt
tên, nhưng phép đo hiện tại chưa cho thấy lỗi chức năng hoặc vi phạm đủ để ghi finding riêng.

Kết luận xét lại: vẫn `do_not_land`, nay có đúng **một finding**: P2
`ac19-dead-exemption-mutation-anchors-remain`. Cần xoá hai hằng miễn trừ chết `C3_CU` và
`C3_MOI` trước lượt review kế tiếp.
