# Handoff wp868 — executor claude, lease `wp868-r1-g1-claude`

Bản TẠM (đang thi công) — sẽ cập nhật ở head cuối. Nguồn sự thật: spec `ops/specs/wp868.md`
(sha256 `0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69`), lease `ops/leases/wp868-r1-g1-claude.yaml`.

```yaml
schema_version: 1
packet_id: wp868
generation: 1
spec_hash: 0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_01WgcSwsdNhpznNmmkxeLBuA
base_sha: 9e9a74b2a396ef458d25c51a5563efafbb45ba0c
head_sha: null          # cập nhật ở head cuối (PR #873)
status: in_progress
```

## Q4 — ca/đột biến cũ đã đổi, vì sao (hợp đồng đổi CÓ CHỦ ĐÍCH)

| Thứ đổi | Trước | Sau | Lý do |
|---|---|---|---|
| `r831` F01 (`_wp831_cai_rg_chon_ban_chay_duoc`) | eval công thức `rg` TRỰC TIẾP, đòi dòng in cuối = thư mục bản tốt đầu PATH | chạy qua `cai_cong_cu.sh`, đòi DAT và `$GITHUB_PATH` KHÔNG nhận thư mục ứng viên | `rg` nay dùng bộ chọn chung: tên trần đã DAT ⇒ `GIU_PATH`, không in thư mục nào. Ý đồ giữ nguyên: ứng viên không thực thi không bị chọn. Nhánh `truc_tiep` của helper wp831 bị bỏ (không còn ai gọi). |
| harness `truc_tiep` của `_wp858_chay_cai` | `eval "$LENH"` rồi đọc dòng in cuối stdout | cấp `KENH_KQ` tạm, chạy `( set +e; eval ) > out`, in như reader (kênh có nội dung ⇒ kênh, rỗng ⇒ stdout) | Bộ chọn không còn in ra stdout; không cấp kênh thì nó `return 1` và các ca `rc != 0` xanh VÔ NGHĨA. Đọc như reader giữ mutant `wp858_yaml_python_linux_ve_dirname` chết bằng hành vi. |
| `r858_hinh_dang_cong_thuc_cai` | 12 công thức; chốt `printf '\n%s\n' /dev/null` / `"$dich"` | 15 công thức (thêm `rg`); chốt `GIU_PATH`/`DICH` trên kênh + vòng duyệt có `break` | N4 + Q3. |
| đột biến `wp858_sh_bo_dong_canh_giu_path` · `dong_canh_la_ten_thu_muc` · `dong_canh_khong_tach_dong` | neo dòng canh `/dev/null` | neo dòng ghi `GIU_PATH` · payload `DICH` sai · nhánh `GIU_PATH` đọc stdout | dòng canh bị thay bằng kênh (Q3); giữ ý đồ "tên trần đã DAT thì không đổi PATH". |
| đột biến `wp802_yaml_bo_ung_vien_winget_links` · `wp831_yaml_{linux_bo_ung_vien_usrbin,macos_bo_ung_vien_brew}` | neo vòng `RG_D` riêng | neo đối số ứng viên của `chon_thu_muc_chay_duoc rg`; thêm `r858_hinh_dang_cong_thuc_cai` để đo được trên Windows | N4. |
| BỎ 5 đột biến YAML: `wp802_yaml_chon_ung_vien_chi_theo_ma_thoat`, `wp802_yaml_khong_ghi_github_path`, `wp831_yaml_linux_chi_theo_ma_thoat`, `wp831_yaml_macos_bo_kiem_thuc_thi`, `wp831_yaml_linux_ghi_github_path_vo_dieu_kien` | logic chọn/ghi PATH nằm trong YAML `rg` | logic ấy nay ở hàm chung, đã có `wp858_sh_chon_theo_ma_thoat` · `wp858_sh_nuot_loi_ghi_github_path` · `wp858_sh_bo_kiem_ten_tran` canh | neo không còn tồn tại; không xoá ca test nào. |

## Đo môi trường (Q9, packet khác — không vá)
- Sau khi một lượt Codex KẾT THÚC, `/tmp/.git` RỖNG (không còn mount) còn sót ⇒ 11 ca `r484_*` đỏ
  ("Codex home is inside a repository"). `rmdir /tmp/.git` (chỉ thư mục rỗng do chính lượt Codex của phiên này tạo) ⇒ cả
  11 ca xanh. Mở rộng nợ `r484_*`/`/tmp/.git` của #858: không chỉ KHI Codex đang chạy mà cả SAU khi nó thoát.
- `ci.yml` run 39746531917 (`ac4a6cb`): `chuan-bi` đỏ hai lần, ~5 s, `runner_id: 0`, log 404 — chưa cấp runner.
  Comment PR #873 issuecomment-6336148808.
