<!-- Sao nguyen van truong body cua readback-pr-1414.json (PR #1414, head 9804f64). Nhan: loi_khai_co_neo. -->

Packet #387 revision 2 generation 1 (packet B). Lease `ops/leases/wp387-r2-g1-claude.yaml` (nhánh `ops/wp387-b-spec`, `c97ac06`). Đặc tả `ops/specs/LAUNCHER-BAM-LOG-NEN-WINDOWS-r1.md`, sha256 `c67ecfa7caef071ddf3888e9e47f2082284b57ca15de37377e3ce3f9bd5fe3af` (đã tự kiểm: `lease_publish.py check` rc 0, băm khớp).

## Định danh

| | |
|---|---|
| base | `3b647461db7c8ded1bddd9aafc5c6aa5eead223f` |
| exact head | `9804f642ad9c7abcc9e7ae4877c2ff133ef31f00` (commit 2; commit 1 là `966ee164b5b7bcd7f5df9e4674bb7b0fb8ef9515`) |
| tree | `13c48c05ed0a87c288c79386876c5f78315828f6` |
| `git diff --numstat base..H` | `20 13 .claude/dev/launcher.py` · `313 64 .claude/dev/launcher_test.py` ⇒ **333 dòng thêm** (trần 450), đúng 2 tệp write set |

## Thay đổi

- **M1** `_nen_do_cay_truoc_bam()` nhận Linux và Windows. Darwin và nền khác giữ hành vi packet A (nợ `wp387-darwin-chua-do`).
- **M2** vòng dò của `_cho_cay_chet_truoc_bam` dò theo nền bằng đúng dòng M2 của đặc tả: Linux hỏi nhóm tiến trình, Windows hỏi `_pid_trong_job(job)`, Windows thiếu job là không đo được. Không gọi `_cay_da_chet`. Docstring khai phạm vi (breakaway, khe `Popen` → gán job).
- **M3** Windows không xoá ngay bản chụp prompt kể cả khi job rỗng.
- **M4** `VERSION` 1.6.1 → 1.6.2.
- **M5** fixture r387 cho Windows: bắt tay gán job (`job-da-gan`), quyền sở hữu job ghi lúc gán (`_r387_boc_job`), teardown nhánh job chờ job rỗng rồi đóng handle đúng một lần và không ném, teardown `co_chau=False` chạy dưới `finally`, `os.killpg` chỉ dùng khi có.
- **M6** 9 ca r387 mở cho Linux + Windows; thêm (e6)–(e9), (t2)–(t6); (a′) đi qua `_r387_doi_chung_a`.
- **M7** cập nhật `_R387_KHOI_MOC` và `_R387_DONG_CAY`; thêm 6 mục `DOT_BIEN` (W1–W6) và 7 mục `DOT_BIEN_HARNESS` (H1–H7).
- **Commit 2 (`9804f64`)**: fixture của ca (i) ép đồng hồ giả tăng ngặt (xem "Đo native Windows", lượt 1).

## Đo native Windows (N4, N5)

Do phiên điều phối đo trên Desktop `DESKTOP-T9R33P2`, Windows-11-10.0.26300, Python 3.12.10, cây sạch. Số liệu dưới đây là lời báo của phiên điều phối; log nằm trên máy đó (thư mục `F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS\`), executor không tự đo được. Đã dùng 3/3 lượt Windows native.

**Lượt 2 — exact head `9804f64` (07:47–07:59Z, log `wp387b2-out-20261119T074702Z`): ĐẠT**

- **L1**: 13/13 ca `1/1 qua` (gồm (i)).
- **L3**: (a) 5/5, (c) 5/5.
- **N5**: `run.json` có `version` 1.6.2, `ma_thoat` 0, `job_windows` true, `log_bam_cay_da_chet` true, `log_bam_cho_giay` 0.0.
- **L2**: bản lọc 22/0/9 (sha256 `5d5cd9b0…`) `DOT BIEN: 31/31 dat`; W5 `OK giet 1/1`; nhãn W5 `r387(g) Windows xoa ban chup`, nhãn W7 `ket_thuc_utc da gom thoi gian doi`.
- **Toàn suite head**: 330/340 (tổng 426, bỏ qua 86, hỏng 10), 0 dòng `BO QUA r387`.

**Lượt 3 — base `3b64746`, cùng điều kiện (08:03–08:11Z, log `wp387b3-out-20261119T080325Z`)**

Developer Mode (quyền symlink) được bật giữa lượt 1 và lượt 2, nên base được đo lại để so cùng điều kiện.

- **Toàn suite base**: 321/331 (bỏ qua 95, hỏng 10).
- Tập bỏ qua base − head = đúng 9 ID r387; head − base = ∅.
- Tập 10 ca hỏng base = head (`t53`, `r15`, 4×`r925`, 3×`r926`, `r927`): đỏ sẵn trên máy đó, delta 0.

**Lượt 1 — head cũ `966ee16` (log `wp387b-out-20261119T071249Z`): lý do của commit 2**

- N5 và L3 đạt; L1 12/13; L2 29/31.
- ĐỎ: (i) `r387_a_nen_khac_giu_moc_ket_thuc_base` — `r387(i) moc ket_thuc_utc phai lay SAU unlink ban chup (ban chup con tren dia: [False, False])`. Đồng hồ Windows thô: hai lần gọi `gio()` liên tiếp trả cùng giá trị nên phép lọc theo `ket_thuc_utc` khớp hai phần tử (cả hai `False` — launcher đúng, fixture sai). Hai mục `r387_a_nen_khac_doi_moc`, `r387_a_nen_khac_moc_truoc_unlink` vì thế báo `SAI - KHONG DO DUOC (neutral do: (i))`.
- Sửa ở commit 2 (chỉ `.claude/dev/launcher_test.py`, +5/−2; một push thêm được chủ kho duyệt theo lời phiên điều phối): trong `gio()`, mốc trả về không lớn hơn mốc trước thì cộng 1 micro giây. Phép so `con == [False]` và mọi vế khác giữ nguyên.

## Đã đo trên Linux (container cloud, Python 3.13.18, `core.abbrev=7`)

Trên head `9804f64` (07:43–07:44Z): `--lap-ca` (i) 1/1; `t117` 1/1; `r387_a_nen_khac_doi_moc` và `r387_a_nen_khac_moc_truoc_unlink` áp vào bản sao `git archive HEAD` vẫn làm (i) đỏ bằng `TinHieuChotCa` (`moc ket_thuc truoc phep do xoa prompt: 0.033` và `ban chup con tren dia: [True]`); Ruff F delta 0; `diff --check` rỗng.

Trên head `966ee16` — base và head dựng thành hai clone trong cùng một lệnh, chạy tuần tự; `/tmp/.git` không tồn tại trước và sau khi đo:

| # | lệnh | kết quả |
|---|---|---|
| N1 | `--lap-ca <ca> --lan 1` cho (e), (t), 9 ca mở, `t117`, `t71` (06:13Z) | mỗi ca `1/1 qua, 0 bo qua, 0 hong` |
| N1 nhãn | áp từng mục W1–W4, W6, H1–H7 vào bản sao `git archive HEAD`, `--lap-ca <ca đích> --lan 1`, lấy dòng `HONG <ca>:` (06:14:47Z) | **12/12**: mỗi mẫu khớp đúng 1 chỗ (H2: `[1, 1]`), `py_compile` rc 0, đúng một dòng `HONG`, nhãn khớp §4b |
| N2 | bỏ cập nhật `_R387_KHOI_MOC` rồi `--lap-ca t117… --lan 1`; tương tự `_R387_DONG_CAY` (06:16:20Z) | cả hai rc 1, `HONG t117…` nêu đúng mục; trên head `t117` ĐẠT |
| N3 suite | `python .claude/dev/launcher_test.py` | base (06:17:03Z→06:23:48Z) rc 0 `424/424 … (tong 426, bo qua 2, hong 0)`; head (06:23:48Z→06:30:28Z) y hệt; tập ID bỏ qua head = base = {`t62_qua_han_ma_khong_giet_het_cay_phai_tra_125`, `r484_g4_windows_sid_alias_identity`} |
| N3 đột biến | `python .claude/dev/launcher_test.py --dot-bien` | base (06:30:28Z→06:42:45Z) rc 0 `DOT BIEN: 720/720 dat (6 khong do duoc)`; head (06:42:45Z→06:55:21Z) rc 0 `DOT BIEN: 732/732 dat (7 khong do duoc)`; tập `KHONG DO DUOC` head = base ∪ {`r387_b_windows_xoa_prompt_khi_job_rong`}; 0 dòng `SAI` |
| N6 | numstat, `ruff 0.15.15 check --select F` (base vs head), `doctrine-scan`, `adr-song`, `git diff --check`, `.githooks/eol_policy.py --all --json` | 2 tệp, ≤ 450; Ruff delta 0; doctrine-scan rc 0; adr-song rc 0; `diff --check` rỗng; eol `"ok": true` |
| doctor | `python .claude/dev/launcher.py doctor` | rc 0 trên head và base |

### CI và review

| head | CI (check-runs, chỉ Ubuntu) | Codex connector |
|---|---|---|
| `966ee16` | 40 success + 1 skipped, 0 đỏ (run 44475834648, 44475834824, 44475834857) | lượt 1/10: "Didn't find any major issues", Reviewed commit `966ee164b5` |
| `9804f64` | lúc 08:13Z: 40 success + 1 skipped, `gate-registry (ubuntu-latest)` còn đang chạy (run 44481907535, 44481912683, 44481912757, 44481998590) | lượt 2/10: "Didn't find any major issues", Reviewed commit `9804f642ad` |

### Nhãn đỏ từng mục (N1)

| mục | ca đích | dòng `HONG` (rút gọn) |
|---|---|---|
| W1 `r387_b_windows_khong_do` | (e) | `r387(e8) Windows job rong phai True: False` |
| W2 `r387_b_windows_dung_nhom` | (e) | `r387(e6) goi _thanh_vien_nhom tren Windows` |
| W3 `r387_b_job_none_thanh_rong` | (e) | `r387(e7) Windows thieu job phai False ngay: kq=True ngu=[] do=[]` |
| W4 `r387_b_windows_long_cay_da_chet` | (e) | `r387(e6) goi _cay_da_chet` |
| W6 `r387_b_linux_di_nhanh_job` | (e) | `r387(e9) Linux goi _pid_trong_job` |
| H1 `r387_fx_dong_truoc_khi_cho` | (t) | `r387(t2) thu tu do/dong: [('dong',), ('do',), ('dong',)]` |
| H2 `r387_fx_bao_gan_truoc_khi_gan` | (t) | `r387(t4) job-da-gan ghi truoc khi gan: [True] …` |
| H3 `r387_fx_bo_kiem_closehandle` | (t) | `r387(t3) CloseHandle that bai khong bao: '' …` |
| H4 `r387_fx_khong_dong_job` | (t) | `r387(t2) thu tu do/dong: [('do',)]` |
| H5 `r387_fx_phat_dau_khi_gan_hong` | (t) | `r387(t4b) gan that bai van phat dau: None True` |
| H6 `r387_fx_don_dep_ngoai_finally` | (t) | `r387(t5) teardown khong chay khi ne: SENTINEL / '' / dong=[]` |
| H7 `r387_fx_loi_bam_nuot_teardown` | (t) | `r387(t6) loi bam nuot loi teardown` |

Mọi dòng mang tiền tố `TinHieuChotCa:`. Neo cũ `r387_teardown_nuot_loi` vẫn khớp đúng một chỗ (đường `add_note` mới dùng tên biến `loi_goc`). H6 đổi `finally:` của khối teardown thành `else:`.

## Chưa đo

- Toàn suite + `--dot-bien` Linux tại chỗ trên head `9804f64` (chỉ có CI Ubuntu của head này; một job còn chạy lúc cập nhật thân PR).
- Darwin: không đo (nợ `wp387-darwin-chua-do`).

## Ghi chú cho reviewer

- `_r387_chay` đặt `m._r387_pgid = None` ở đầu mỗi lời gọi, nên teardown nhánh pgid dưới `finally` không dùng pgid của lượt trước khi `_r1252_run` ném (khớp §8).
- Hàm đóng mặc định là `ctypes.windll.kernel32.CloseHandle`, phân giải bên trong `try` của teardown.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

https://claude.ai/code/session_015GtxrZPctMA2qwxSJDd8nw
