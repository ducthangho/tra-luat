Packet #387 · `LAUNCHER-BAM-LOG-SAU-CAY-CHET` revision 1 · generation 1 (packet A, chỉ Linux) · lease `wp387-r1-g1-claude` (`ops/leases/wp387-r1-g1-claude.yaml` @ `c992be6a4dd37dede6b0b76af485328f6a02d8a4`, nhánh `ops/wp387-r1-g1-lease`).
Đặc tả: `ops/specs/LAUNCHER-BAM-LOG-SAU-CAY-CHET-r1.md` tại commit lease, sha256 byte thô `a2dbdb0cab14f42fea36c6a2bec5326f3be7775c1edcb941b15ecc800319eaff` (đã đo bằng `git show … | sha256sum`, khớp `spec_hash`).

## Neo

| | |
|---|---|
| base | `d1ca71a4b30eb5816c3e7be43c87a18acdf3fd7a` |
| head H | `5bcea6cdf56ae6b4ba76345837927870af2ef86e` |
| tree | `2d44e1e7f32ed94de3696d97fc2efa05e4937161` |
| numstat `base..H` | `55 3 .claude/dev/launcher.py` · `395 2 .claude/dev/launcher_test.py` — 2 tệp, **+450 dòng thêm** (trần 450, `ADR-0053`; đúng bằng trần, biên 0) |

Một commit, một lần push, đúng hai tệp của write set. `git diff --stat 641108c d1ca71a -- .claude/dev/launcher.py .claude/dev/launcher_test.py` rỗng (đặc tả đo trên `641108c`, hai tệp không đổi tới base).

## Nội dung

- **M1** `lenh_run` ghi `log_bam_cay_da_chet`, `log_bam_cho_giay`, `log_bam_luc_utc` (gán ngay trước vòng băm). `_nen_do_cay_truoc_bam()` là chỗ duy nhất quyết nền. Dòng xoá prompt thành `cay_da_chet = log_cay_chet if _nen_do_cay_truoc_bam() else (_thanh_vien_nhom(p.pid) == [])`; dòng `            and cay_da_chet):` giữ nguyên.
- **M2** `_cho_cay_chet_truoc_bam(pid, job, han)` + `_HAN_CHO_CAY_TRUOC_BAM_LOG = 10.0`: một deadline monotonic; nền khác Linux trả `False` ngay. Trong `lenh_run`: `ket_thuc = _bay_gio()` → mốc monotonic → đợi → ghi hai khoá → rồi mới `so_moi = _doc_so(...)`. Nền khác Linux lấy lại `ket_thuc` ngay trước `ban_ghi.update(ket_thuc_utc=…)`. Ctrl-C trong lúc đợi: `false` + cờ `ngat_khi_cho`, xét sau khối `kq_chup`, chỉ khi `xong`; `ma_that` không đổi.
- **M3** `VERSION` `1.6.0` → `1.6.1`.
- **M4** mười một ca `r387_*` (t, a, a′, b, c, d, e, i, f, g, h) và fixture `_r387_*`. Fixture không có đường gửi tín hiệu.
- **M5** MỘT neo sửa: `xoa_prompt_khi_wrapper_vua_thoat` neo sang dòng gọi đợi.
- **M6** MƯỜI SÁU đột biến `DOT_BIEN` mới, HAI đột biến `DOT_BIEN_HARNESS` mới; không thêm gì vào `DA_BIET_TRUNG`.

## Đã đo (Linux, container phiên executor, Python 3.13.18, `core.abbrev=7`)

Mọi phép đo dưới đây trên tree `2d44e1e` (tree của H), cây sạch. Phép đo tay chạy trên bản sao `git ls-files` ngoài checkout.

**Toàn suite** — `python3 -B .claude/dev/launcher_test.py`, 2026-11-18T09:33:11Z → 09:39:32Z, rc 0:
`424/424 ca DA CHAY QUA (tong 426, bo qua 2, hong 0)`. Hai ca bỏ qua: `t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`, `r484_g4_windows_sid_alias_identity` (đúng tập của base theo §0 đặc tả; tôi không chạy lại toàn suite của base).

**Runner đột biến ĐỦ BẢNG** — `python3 -B .claude/dev/launcher_test.py --dot-bien`, 09:39:38Z → 09:51:32Z, rc 0, dòng cuối:
`DOT BIEN: 720/720 dat  (6 khong do duoc tren nen nay)`, 0 dòng `SAI`.
Sáu mục `KHONG DO DUOC`: `r1335_N3c_win_giu_argv0_goc`, `r1335_F2_win_path_theo_cwd_launcher`, `g4_windows_sid_alias_not_normalized`, `g4_windows_LA_not_current_owner`, `g2_windows_directory_pin_access` (năm mục điều kiện `windows`) và `124_khi_chau_con_song` (ca đích `t62` bỏ qua). Khớp danh sách N4.

**N1**
- (a), (a′): `--lap-ca … --lan 1` ⇒ `1/1 qua` mỗi ca (và đạt trong toàn suite).
- Đối chứng base, 09:32:27Z: `launcher_test.py` của head + `launcher.py` của `d1ca71a` (`VERSION = "1.6.0"`), `--lap-ca r387_m1_chau_ghi_muon_khai_pham_vi_bam --lan 1` ⇒ rc 1,
  `HONG r387_m1_chau_ghi_muon_khai_pham_vi_bam: TinHieuChotCa: r387(a) cay chua chet ma khai None` · `LAP …: 0/1 qua, 0 bo qua, 1 hong`. Ca đi qua vế băm rồi đỏ ở vế khoá.
- Runner: `r387_khai_cay_chet_luon_true`, `r387_ket_thuc_sau_vong_cho`, `r387_fixture_gui_tin_hieu_theo_pid_chau` ⇒ `OK giet 1/1` ca (a).
- Đo tay: xoá vế băm khỏi thân (a) ⇒ (a′) rc 1, `TinHieuChotCa: r387(a') than (a) do o ve khac, khong phai ve bam: …`.

**N2** — (b) đạt. `r387_khai_cay_chet_luon_false`, `r387_moc_bam_truoc_khi_con_thoat` ⇒ `OK giet 1/1` ca (b). Đo tay: xoá dòng gán `log_bam_luc_utc` ⇒ (b) rc 1, `TinHieuChotCa: r387(b) log_bam_luc_utc=None phai co va khong truoc ket_thuc_utc=…` (không `KeyError`).

**N3** — (t), (c), (d), (e), (i), (f), (g), (h) đạt. Mười một ca chạy lần lượt bằng `--lap-ca` (mỗi ca một tiến trình): 17,6 s wall cộng lại. Runner, mỗi mục `OK giet 1/1` đúng ca đích: `r387_teardown_nuot_loi` ⇒ (t); `r387_bo_vong_cho` ⇒ (c); `r387_khong_do_duoc_van_cho` ⇒ (d); `r387_nhan_ket_qua_sau_han`, `r387_ngu_khong_tru_lan_do`, `r387_a_nen_khac_van_do`, `r387_a_nen_khac_ngu_thua` ⇒ (e); `r387_a_nen_khac_doi_moc`, `r387_a_nen_khac_moc_truoc_unlink` ⇒ (i); `r387_cho_sau_doc_lai_stop` ⇒ (f); `xoa_prompt_khi_wrapper_vua_thoat` ⇒ `t76`; `r387_ngat_khi_doi_bi_nuot`, `r387_ngat_che_ket_qua_chup`, `r387_ngat_ghi_130_vao_so` ⇒ (h).

**N4** — suite và runner như trên; đủ 18 đột biến mới `OK giet 1/1`. Trong runner đủ bảng: `nhom_luon_rong` ⇒ `t67`, `ban_chup_de_lai_tren_dia` ⇒ `t71`, `r1252_none_la_chet`/`r1252_windows_khong_dung_job`/`r1252_windows_bo_ngu`/`r1252_windows_khong_cho_job` ⇒ `r1252_khong_do_duoc`, đều `OK giet 1/1`. `t117` đạt; ngoại lệ trùng vẫn chỉ `{"hook_phien_bo_phep_so_nang_luc": 2}`.
Đo tay trên bản sao: trả neo M5 về mẫu cũ ⇒ `t117` rc 1 (`xoa_prompt_khi_wrapper_vua_thoat` đếm lệch); thêm một dòng `            time.sleep(0.1)` vào hàm đợi ⇒ `t117` rc 1 (`r1252_windows_bo_ngu`, `dem=2 mong=1`).

**N5** — không đo native; đường nền khác Linux đo trên Linux bằng (e5), (i) và bốn đột biến `r387_a_nen_khac_*` (trên).

**N6**
- `ruff check --no-cache --select F .claude/dev/launcher.py .claude/dev/launcher_test.py` (ruff **0.16.9**, bản có trong container; đặc tả dùng 0.17.5): head rc 1, 5 F841 ở `launcher_test.py` dòng 2767, 3695, 3937, 4421, 6465; base rc 1, đúng 5 mục ấy cùng dòng ⇒ delta 0. Phản chứng: thêm tên chưa định nghĩa trên bản sao ⇒ `Found 6 errors`.
- `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 (`sạch — đã quét 12 tệp`). `… adr-song --root .` rc 0 (`66 ADR … khớp 1–1`). Phép đỏ: chưa đo.
- `git diff --check d1ca71a..H` rỗng, rc 0.
- `launcher.py doctor`: head rc 0; `launcher.py` của base (bản sao rời, cùng máy, cùng cwd) rc 0. Phép đỏ: chưa đo.
- Một lượt `launcher.py run … -- python3 -c "print('N6')"` (09:40:00Z, rc 0): `run.json` có `"version": "1.6.1"`, `log_bam_cay_da_chet: true`, `log_bam_cho_giay: 0.002`, `log_bam_luc_utc: 2026-11-18T09:40:00.330946+00:00`, `ket_thuc_utc: …00.329040+00:00`.
- Tầm quét preflight §6 trên base (`git grep -n -E 'stdout_sha256|ket_thuc_utc|thoi_luong_giay|log_bam_|run\.json' -- '*.py' ':!ops/**'`): ngoài hai tệp write set chỉ có `ci_dang_ky_test.py` (khoá của sổ khác), `packet_loop.py` K4 và test của nó. Không thấy bộ khoá cố định nào của `run.json`.

## Chưa đo được

- Windows và Darwin thật: chưa chạy (thuộc packet B).
- CI trên H: chưa có kết quả lúc mở PR.
- Review: chưa có lượt nào (executor không gọi Codex theo chỉ thị giao việc).
- Toàn suite và runner đủ bảng của BASE không chạy lại trong phiên này; so với base dựa vào §0 đặc tả và vào danh sách tên ca bỏ qua.
- Dung sai thời gian của (a), (d), (e), (i) chỉ đo trên container này, mỗi ca vài lượt.

## Ghi chú thi hành

- Tổng dòng thêm đúng 450, không còn biên. Mọi push thêm có dòng mới sẽ vượt trần.
- Vế "nhật ký kill RỖNG" nằm trong `_r387_nhat_ky_kill()`: khối kết thúc không lỗi thì hàm ấy khẳng định nhật ký rỗng (tức sau các vế trong khối, đúng thứ tự của (a)). Ca (c) cũng chạy trong khối này.
- Ca có tham số `do=` của `_r387_chay` thay phép dò BÊN TRONG `lenh_run` (ca d, f, i); teardown luôn dùng phép dò thật.
- `--dot-bien` lọc (chỉ mục r387 + neo M5, bảng hook/harness nguyên) trên bản sao, 09:27:28Z → 09:32:02Z: rc 0, `DOT BIEN: 177/177 dat`. Chỉ là bước dò trước; bằng chứng N4 là lượt đủ bảng.
- Protocol §13 xếp review offline trước push; lượt này đẩy và mở draft trước theo chỉ thị giao việc, review do phiên điều phối lo.

---
_Generated by [Claude Code](https://claude.ai/code/session_015Gtxrb4huMrRxF2Lw4t79M)_