# Handoff wp1236 đợt C — ứng viên `ac523ae` (revision 12, generation 1)

Nguồn có thẩm quyền của thư mục này là `handoff.yaml`; tệp này chỉ giải thích những chỗ một bảng YAML không nói hết.
Ứng viên CHƯA push (ADR-0060 M5/M12): lấy bằng bundle.

```bash
git fetch ops/handoff/wp1236-c-r12-g1/ac523ae/wp1236-c-ac523ae.bundle claude/wp1236-c-r12-g1:claude/wp1236-c-r12-g1   # cần base f602325
git rev-parse claude/wp1236-c-r12-g1            # ac523aebd876640b369e94511fd44e81bace0908
git rev-parse 'claude/wp1236-c-r12-g1^{tree}'   # e62a4e166e9f181f2a291337d8c527dd84fbaf7e
```

## 1. Luật 9 áp cho đợt C thế nào, và vì sao không nguyên văn

Đặc tả ghi `quet_dot_bien.py do <module> <test> <kho>`. Bộ quét ghim (sha256 `1b3e4a9e…`, KHÔNG sửa) không chạy thẳng được trên
`packet_loop.py` + `packet_loop_test.py`. Đo được:

- nó ghi bản đột biến ra tệp tên `gate_output_doi_chieu.py`, đặt biến `GATE_OUTPUT_DOI_CHIEU_MA`, và đòi tệp test có `CA` cùng
  `chay_ca(ten)` trả rc 3 khi GIẾT — giao diện của tệp test đợt A; `packet_loop_test.py` không có;
- `sinh` trên cả `.claude/dev/packet_loop.py` (7,6k dòng) không xong trong 600 s (bị cắt, chưa ra manifest).

Cách đã làm:

| phần | nội dung |
|---|---|
| module đưa cho `do` | `luat9/d2b_trich.py`: khối D2b cắt NGUYÊN VĂN từ `packet_loop.py` tại `ac523ae`, từ dòng mốc `# --- #1236 đợt C` tới trước `def cmd_kiem_dong_wp` (hai hằng regex, `_d2b`, `_d2b_kiem`). Lệnh cắt: `python3 luat9/d2b_noi.py trich .claude/dev/packet_loop.py <ra>` |
| test đưa cho `do` | `luat9/d2b_noi.py` (bộ nối, dev-side, ngoài write set): ghép bản đột biến của khối vào `packet_loop.py` của kho, rồi gọi ĐÚNG `chay_suite` của `packet_loop_test.py` cho từng ca `cong_d2b_*` |
| khi nào tính GIẾT | chỉ khi bộ phân hạng của chính `packet_loop_test.py` ra `GIET`, tức ca ném `ChotB4(<tên ca>)`. CLI sập hay dựng fixture hỏng ⇒ `HONG` (bộ quét xếp `VO_CAN`) |
| kho (B) | rỗng (`luat9/kho_rong.jsonl`) |
| ca không đưa vào `CA` | `cong_d2b_tu_kiem_phan_hang`: nó đọc mỏ neo văn bản của bản gốc, mà bản đột biến là dạng `ast.unparse` |

Kết quả trên `ac523ae`: `TONG 178 · GIET 174 · SONG_SACH 4 · CHI_LOI_VO_CAN 0 · LOI_CHAY 0`, có dòng `HOAN_TAT`. Bốn đột biến sống
đều tương đương, chứng minh ở `handoff.yaml` (`luat_9.song_tuong_duong`) và `luat9/ledger_A.tsv`.

Tái lập (Python 3.13, từ gốc kho đang ở `ac523ae`, cây sạch):

```bash
D=ops/handoff/wp1236-c-r12-g1/ac523ae/luat9      # hoặc bản chép của thư mục này
python3 $D/d2b_noi.py trich .claude/dev/packet_loop.py /tmp/d2b_trich.py && sha256sum /tmp/d2b_trich.py   # ceb9f97d…
WP1236C_GOC="$PWD" python3 ops/reviews/wp1236-r10-soan/quet_dot_bien.py do /tmp/d2b_trich.py $D/d2b_noi.py $D/kho_rong.jsonl --thu-muc-ra /tmp/D --song-song 4
python3 $D/ledger.py /tmp/D /tmp/d2b_trich.py /tmp/ledger_A.tsv
```

Giới hạn của cách này, nói thẳng: neo của bộ quét băm khối cắt, bộ nối, manifest và kho — KHÔNG băm `packet_loop.py` hay
`packet_loop_test.py` (bộ nối đọc chúng từ kho). Băm hai tệp ấy ghi ở `handoff.yaml` (`sha256_tep_tai_head`). Ba dòng ngoài khối
(lời gọi `_d2b`, `import tarfile`, chuỗi help) không nằm trong manifest.

## 2. Bảng C1–C9 của đặc tả ↔ ca và đột biến

| đặc tả | ca | đột biến khai báo |
|---|---|---|
| C1 passed hợp lệ | `cong_d2b_c1_passed_dat` | mC1 `d2b_mC1_khong_chay` · `d2b_chay_moi_gia_tri` · `d2b_doc_cay_lam_viec` |
| C2 thiếu nguồn | `cong_d2b_c2_thieu_nguon` | mC2 `d2b_mC2_thieu_nguon_bo_qua` · `d2b_bo_dang_oid` |
| C3 lệch neo, attempt | `cong_d2b_c3_neo` · `cong_d2b_c3_attempt_kieu` | mC3 · mC4 · mC9 (`d2b_mC3_bo_neo_run`, `d2b_mC4_bo_neo_head`, `d2b_mC9_bo_neo_attempt`) · mC10 `d2b_mC10_attempt_khong_int` · `d2b_attempt_bo_duong` · `d2b_neo_attempt_ban_kem` · `d2b_attempt_ca_mien` |
| C4 tệp không passed | `cong_d2b_c4_kiem_tep` | mC5 `d2b_mC5_nhan_moi_trang_thai` · `d2b_dung_lai_symlink` |
| C5 đường dẫn | `cong_d2b_c5_duong_dan` · `cong_d2b_c5_mode` | mC12 `d2b_mC12_nhan_hai_cham` · mC6 `d2b_mC6_ops_bat_ky` · mC11 `d2b_mC11_bo_mode` · `d2b_nhan_mot_cham` · `d2b_readback_ops_bat_ky` · `d2b_duong_dan_khop_dau` |
| C6 owner_waived | `cong_d2b_c6_mien` | mC7 `d2b_mC7_mien_thuan_loi_khai` · mC14 `d2b_mC14_in_dat_khi_vi_pham` · `d2b_mien_head_none` · `d2b_mien_thu_muc_goc` · `d2b_mien_nhan_tep` |
| C7 module không nạp được | `cong_d2b_c7_module_vang` · `…_khong_nap` · `…_nem` · `cong_d2b_c7_git_loi` | mC8 `d2b_mC8_gop_rc_12` · `d2b_nuot_loi_do` · `d2b_bo_rc_git` |
| C8 D2 cũ giữ nguyên | các ca `cong_c_d*`, `cong_c_fixture_crlf` (không sửa kỳ vọng) | các đột biến `c1106_d*` cũ vẫn bị giết |
| C9 OID không trên remote | `cong_d2b_c9_oid` · `cong_d2b_c9_oid_khong_phai_commit` | mC13 `d2b_mC13_bo_remote` · `d2b_remote_bat_ky` · `d2b_bo_loai_commit` |

Mỗi biến thể so đúng bộ (rc, danh sách lý do `THIẾU  D2b …` theo thứ tự, các dòng `D2b …` của stdout); rc 8 thì so đúng dòng
`KHÔNG ĐO ĐƯỢC …`. Mười trên mười bốn ca chạy thêm một đối chứng đạt trên CÙNG kho tạm; bốn ca còn lại (ba ca module hỏng/vắng, ca O không lên remote) có
kho cố ý không hợp lệ nên không có đối chứng tại chỗ.

## 3. Tên lý do ↔ biến thể phát ra đúng lý do ấy

`thieu_nguon` (c2, 16 biến thể, cả nhánh miễn) · `attempt_kieu` (c3_attempt_kieu: thiếu, `True`, `0`, `-1`, `"1"`, `1.0`, `2.0`) ·
`oid_khong_tren_remote` (c9: chỉ nhánh cục bộ, remote khác `origin`, thẻ có chú thích, OID vắng, git bị ngắt) · `duong_dan_sai`
(c5_duong_dan: 17 chuỗi `tep` + 9 chuỗi `readback_thu_muc`) · `symlink_hoac_mode:<đường dẫn>` (c5_mode: tệp là symlink, thư mục là
symlink, tệp vắng, tệp là thư mục, thư mục vắng, readback là tệp) · `kiem_tep:failed:-` và `kiem_tep:not_measured:provenance_0` (c4) ·
`neo_run` · `neo_attempt` · `neo_head` (c3_neo, riêng từng cái và cả ba) · `mien:tac_gia` · `mien:sha` · `mien:url` · `mien:readback`
(c6) · hai dòng `D2b ĐẠT` (c1, c6) · rc 8 (c7, bốn ca).

Chín điều kiện của `kiem_mien` là của đợt A; D2b chỉ chuyển tiếp, nên đợt C đo bốn điều kiện đủ để khoá `head = merge_commit`,
thư mục readback và việc chuyển tiếp nguyên tên.

## 4. Rủi ro Windows biết trước (chưa đo — M3 là việc của điều phối)

- Ca `van_ban_tu_do` truyền U+0001, U+2028, U+2029 và một ký tự ngoài BMP qua YAML → argv của `git.exe`. Trên Linux đạt; Windows chưa đo.
- Symlink trong fixture đi thẳng vào index (`update-index --cacheinfo 120000,…`), không cần quyền tạo symlink. Biến thể
  `provenance_la_symlink` trỏ đích TRONG thư mục để đột biến `d2b_dung_lai_symlink` vẫn lộ khi `tarfile` chép đích thay cho symlink.
- Đường dẫn dài nhất fixture ghi ra trong kho tạm (đo): `ops/land/pr1440-wp1319-provenance/ci-provenance-44669622916/provenance.yaml`, 75 ký tự.
- `tarfile.extractall(filter=…)` cần Python ≥ 3.12.

## 5. Tệp trong thư mục

`handoff.yaml` · `wp1236-c-ac523ae.bundle` · `gate/` (16 log mảnh, `manh.tong`, `gom.log`, `gate2.tong`, `dot_bien_khai_bao.log`,
đuôi log selftest và `ci_dang_ky_test`, `ruff_head.log`, `bundle_verify.log`) · `luat9/` (bộ nối, khối cắt, kho rỗng, `do.log`,
`ledger.py`, `ledger_A.tsv`, thư mục `D` của lệnh `do`) · `cong_cu/` (script đã dùng để chạy gate; công cụ nháp của executor, không
phải cổng).
