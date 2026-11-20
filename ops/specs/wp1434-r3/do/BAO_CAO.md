# wp1434 r3 — Báo cáo đo nền mutation testing (chỉ đọc)

Sinh bởi `thu_thap.py --tinh` từ ảnh chụp (MANIFEST sha256 `fc95bc3b8bdec1e3121b971531d34e2207edf32c75080fa9a8e07814144ffee3`). Đặc tả sha256 `0247845e6dd643388f7219781ebff553b605e59d731481d10a024e80ae8232b4`.
Cohort đóng băng: T0 `2026-10-21T01:16:24Z` · T1 `2026-11-20T01:16:24Z` · master `711cb190daaa267cb919c10f4030d38172a37a93` · 62 khoảng con liệt kê `ci.yml`.
- `ci-dot-bien-du.yml`: 62 lượt, 64 cặp (run_id, run_attempt); bị loại khỏi cohort: không
- `ci.yml`: 1573 lượt, 1647 cặp (run_id, run_attempt); bị loại khỏi cohort: {'chua_completed_luc_thu': 2}

Không có mục khuyến nghị tối ưu (ngoài phạm vi packet). Mọi con số dưới đây đọc từ `BASELINE.json`.

## Quy tắc §3 và ba trạng thái

- **phan_loai_dong**: theo thu tu: (a) conclusion==skipped -> bo_qua (thoi luong khong_ap_dung, chi dem); (b) mang_sang neu job_id da xuat hien o attempt truoc HOAC started_at < created_at cua attempt chua dong; (c) con lai -> thuc_thi (gom job hong/huy da chay)
- **giay_thuc_thi**: tong completed_at - started_at cua dong thuc_thi hop le, moi attempt; dong thieu moc/dao bi loai va dem o so_dong_loai
- **dau_cuoi_suy_ra_tu_job**: max(completed_at) cua dong thuc_thi hop le o attempt cuoi TRU created_at cua attempt 1; KHONG dung updated_at cua run (chi ghi kem updated_at_tham_khao); attempt cuoi khong co dong thuc_thi hop le -> khong_do_duoc
- **giay_cho**: started_at - created_at cua tung dong thuc_thi
- **ba_trang_thai**: 0 la do_duoc; skipped/khong ton tai -> khong_ap_dung; thieu moc, thoi gian dao, het han, cat cut, loi API -> khong_do_duoc (khong thay bang 0, khong kep am ve 0)
- **thong_ke**: chi tren phan do_duoc; trung_vi = statistics.median; p90 = sorted[ceil(0.9*n)-1]; so_loai = so phan tu bi loai
- **lan**: doc tu log job chuan-bi thuc_thi: dong `che_do=duong_nhanh|day_du` cuoi cung; khong co thi dong `DUONG_NHANH: khong phan loai - ... luon DAY_DU` -> day_du; khong co ca hai hoac thieu log -> khong_do_duoc (KHONG suy tu gia tri mac dinh cua workflow)
- **nen**: nhan runner cua dong job (labels); `khong_ro` = labels rong (job bi huy truoc khi duoc cap runner)
- **rerun**: so_luot_co_rerun = so luot co run_attempt > 1; so_job_hong_o_attempt_truoc = so dong thuc_thi conclusion==failure o attempt < attempt cuoi (KHONG goi la flaky)

## Độ phủ nguồn

| nguồn | yêu cầu | có | hết hạn | cắt cụt | lỗi | không thu (hết khung) | có log, không có bản ghi |
|---|---|---|---|---|---|---|---|
| jobs | 1635 | 1635 | 0 | 0 | 0 | 0 | 0 |
| attempt | 133 | 133 | 0 | 0 | 0 | 0 | 0 |
| log_manh | 440 | 376 | 0 | 37 | 11 | 0 | 16 |
| log_dang_ky_du | 58 | 51 | 0 | 0 | 1 | 0 | 6 |
| log_khac_du | 61 | 53 | 0 | 0 | 8 | 0 | 0 |
| log_dang_ky_ci | 1103 | 832 | 0 | 0 | 0 | 0 | 271 |
| log_chuan_bi | 1529 | 1491 | 0 | 0 | 35 | 0 | 3 |
| artifact_manh | 390 | 390 | 0 | 0 | 0 | 0 | 0 |

`log_dang_ky_ci` chỉ yêu cầu ở dòng `gate-registry` thực thi có bước registry không `skipped`; `log_chuan_bi` để đọc làn.

## M1 — full audit (`ci-dot-bien-du.yml`)

- 62 lượt · kết luận {'cancelled': 7, 'failure': 2, 'success': 53} · lượt có rerun 2 · job hỏng ở attempt trước 10
- Lượt đủ 8 mảnh success, một attempt: 42. Tổng giây 8 job mảnh mỗi lượt: n=42 · tổng 543527 · trung vị 13282 · p90 13614 · max 13884 s
- Giây một job mảnh (các lượt ấy): n=336 · tổng 543527 · trung vị 1672.5 · p90 1761 · max 1809 s
- Lượt đủ mới nhất `43990524880` (2026-11-17T00:47:54Z): job mảnh n=8 · tổng 13010 · trung vị 1621.5 · p90 1730 · max 1730 s; mục theo log 321, theo artifact 321; giây thực thi 14524; đầu-cuối suy ra từ job 1745 s

| job gốc \| nền | thống kê giây (dòng thực thi, mọi lượt) |
|---|---|
| dot-bien-du | ubuntu-latest | n=58 · tổng 99597 · trung vị 1680 · p90 2964 · max 3628 s |
| dot-bien-gop | ubuntu-latest | n=53 · tổng 603 · trung vị 10 · p90 13 · max 60 s · loại 3 |
| dot-bien-manh | ubuntu-latest | n=440 · tổng 633788 · trung vị 1639.5 · p90 1760 · max 1809 s |
| probe | ubuntu-latest | n=3 · tổng 84 · trung vị 28 · p90 28 · max 28 s |
| windows-probe | windows-latest | n=2 · tổng 57 · trung vị 28.5 · p90 30 · max 30 s |

Dòng `KET QUA` trong log mảnh: 321 khoá (chế độ | khoá). 10 khoá có trung vị giây lớn nhất:

| chế độ \| khoá | n | trung vị s | p90 s | max s |
|---|---|---|---|---|
| full_mutant_audit | tk:gop-cli-bo-qua | 48 | 54.1 | 55.8 | 57.4 |
| full_mutant_audit | tk:bo-chuan-hoa-ban-sao | 51 | 53.3 | 55.4 | 58.3 |
| full_mutant_audit | tk:moc-nhan-sai-dinh-dang | 46 | 53.15 | 55.2 | 55.7 |
| full_mutant_audit | tk:bo-cua-khong-lam-gi | 52 | 53.1 | 55.4 | 56 |
| full_mutant_audit | tk:ghi-so-doc-kenh-xac-thuc | 49 | 53.1 | 55 | 55.6 |
| full_mutant_audit | tk:ghi-so-gop-dich | 47 | 53.1 | 55.1 | 55.9 |
| full_mutant_audit | tk:entropy-giu-mot-byte | 49 | 53 | 55.1 | 55.3 |
| full_mutant_audit | tk:r528-ha-tang-mkdir-ngoai-try | 47 | 53 | 55.1 | 55.7 |
| full_mutant_audit | tk:tk-summary-count | 47 | 53 | 55 | 56.7 |
| full_mutant_audit | tk:archive-boc-lop-dong-ten | 52 | 52.9 | 55.1 | 56 |

Từng lượt, từng job, từng bước job mảnh, từng artifact: `BASELINE.json` → `M1.luot`.

## M2 — gate CI (`ci.yml`)

- 1573 lượt · kết luận {'cancelled': 542, 'failure': 67, 'success': 964} · làn {'day_du': 945, 'duong_nhanh': 542, 'khong_do_duoc': 86} · lượt có rerun 55 · job hỏng ở attempt trước 187

| sự kiện \| làn | lượt | giây thực thi | đầu-cuối suy ra từ job |
|---|---|---|---|
| tất cả | 1573 | n=1514 · tổng 15057171 · trung vị 12163 · p90 18519 · max 37911 s · loại 59 | n=1512 · tổng 4507308 · trung vị 1732 · p90 3812 · max 333753 s · loại 61 |
| pull_request | day_du | 705 | n=705 · tổng 9669927 · trung vị 14920 · p90 19486 · max 37911 s | n=705 · tổng 2267987 · trung vị 1973 · p90 3782 · max 325649 s |
| pull_request | duong_nhanh | 454 | n=454 · tổng 1080444 · trung vị 1159.5 · p90 3940 · max 29779 s | n=454 · tổng 603497 · trung vị 532.5 · p90 2403 · max 79904 s |
| pull_request | khong_do_duoc | 28 | n=24 · tổng 2115 · trung vị 23 · p90 315 · max 630 s · loại 4 | n=24 · tổng 4218 · trung vị 58.5 · p90 385 · max 1885 s · loại 4 |
| push | day_du | 240 | n=240 · tổng 4187702 · trung vị 16504.5 · p90 21789 · max 26078 s | n=238 · tổng 1532874 · trung vị 3141 · p90 6332 · max 333753 s · loại 2 |
| push | duong_nhanh | 88 | n=88 · tổng 116965 · trung vị 690 · p90 3135 · max 3408 s | n=88 · tổng 90154 · trung vị 487.5 · p90 2212 · max 6359 s |
| push | khong_do_duoc | 58 | n=3 · tổng 18 · trung vị 5 · p90 11 · max 11 s · loại 55 | n=3 · tổng 8578 · trung vị 122 · p90 8454 · max 8454 s · loại 55 |

Job nhóm `gate*` (làn `day_du`, dòng thực thi; đủ mọi làn/nền ở `M2.theo_job`):

| job gốc \| nền \| làn | thống kê giây | bỏ qua | mang sang | kết luận |
|---|---|---|---|---|
| gate | ubuntu-latest | day_du | n=951 · tổng 630653 · trung vị 713 · p90 872 · max 1611 s | 0 | 0 | {'cancelled': 161, 'failure': 47, 'success': 743} |
| gate | windows-latest | day_du | n=4 · tổng 5317 · trung vị 1542.5 · p90 1693 · max 1693 s | 0 | 0 | {'cancelled': 2, 'success': 2} |
| gate-cong-cu | ubuntu-latest | day_du | n=7613 · tổng 8274704 · trung vị 1068 · p90 1826 · max 2949 s · loại 2 | 0 | 0 | {'cancelled': 1771, 'failure': 77, 'success': 5767} |
| gate-cong-cu | windows-latest | day_du | n=4 · tổng 769 · trung vị 191.5 · p90 199 · max 199 s | 0 | 0 | {'success': 4} |
| gate-cong-cu-gop | khong_ro | day_du | n=145 · tổng 0 · trung vị 0 · p90 0 · max 0 s · loại 103 | 0 | 0 | {'cancelled': 248} |
| gate-cong-cu-gop | ubuntu-latest | day_du | n=726 · tổng 10475 · trung vị 13 · p90 17 · max 289 s | 0 | 0 | {'cancelled': 3, 'failure': 39, 'success': 684} |
| gate-nhanh-gop | khong_ro | day_du | n=33 · tổng 0 · trung vị 0 · p90 0 · max 0 s · loại 23 | 0 | 0 | {'cancelled': 56} |
| gate-nhanh-gop | ubuntu-latest | day_du | n=899 · tổng 16082 · trung vị 15 · p90 19 · max 351 s | 0 | 0 | {'cancelled': 6, 'failure': 13, 'success': 880} |
| gate-nhanh-gop | windows-latest | day_du | n=4 · tổng 120 · trung vị 31.5 · p90 36 · max 36 s | 0 | 0 | {'success': 4} |
| gate-nhanh-manh | ubuntu-latest | day_du | n=7613 · tổng 620135 · trung vị 65 · p90 93 · max 2949 s · loại 1 | 0 | 0 | {'None': 1, 'cancelled': 256, 'failure': 46, 'success': 7311} |
| gate-nhanh-manh | windows-latest | day_du | n=32 · tổng 5121 · trung vị 169 · p90 197 · max 230 s | 0 | 0 | {'success': 32} |
| gate-ops | ubuntu-latest | day_du | n=951 · tổng 979754 · trung vị 1023 · p90 1629 · max 2949 s | 0 | 0 | {'cancelled': 210, 'failure': 24, 'success': 717} |
| gate-ops | windows-latest | day_du | n=4 · tổng 4998 · trung vị 1478 · p90 1512 · max 1512 s | 0 | 0 | {'cancelled': 2, 'success': 2} |
| gate-packet-loop | khong_ro | day_du | n=17 · tổng 0 · trung vị 0 · p90 0 · max 0 s · loại 20 | 0 | 0 | {'cancelled': 37} |
| gate-packet-loop | ubuntu-latest | day_du | n=914 · tổng 1773352 · trung vị 2113.5 · p90 3461 · max 8524 s · loại 4 | 0 | 0 | {'cancelled': 220, 'failure': 20, 'success': 678} |
| gate-packet-loop | windows-latest | day_du | n=4 · tổng 9557 · trung vị 1963 · p90 5096 · max 5096 s | 0 | 0 | {'cancelled': 3, 'success': 1} |
| gate-packet-loop-manh | ubuntu-latest | day_du | n=2739 · tổng 415287 · trung vị 137 · p90 226 · max 797 s · loại 1 | 0 | 0 | {'None': 1, 'cancelled': 359, 'failure': 6, 'success': 2374} |
| gate-registry | khong_ro | day_du | n=35 · tổng 0 · trung vị 0 · p90 0 · max 0 s · loại 27 | 0 | 0 | {'cancelled': 62} |
| gate-registry | ubuntu-latest | day_du | n=893 · tổng 1098927 · trung vị 1265 · p90 2208 · max 5368 s · loại 2 | 0 | 0 | {'cancelled': 216, 'failure': 31, 'success': 648} |
| gate-registry | windows-latest | day_du | n=4 · tổng 1381 · trung vị 374.5 · p90 393 · max 393 s | 0 | 0 | {'cancelled': 1, 'success': 3} |

Bước của `gate-cong-cu*`, `gate-nhanh-*`, `gate-registry`, `gate-packet-loop*`: 250 khoá ở `M2.theo_buoc`. 12 khoá có tổng giây lớn nhất:

| job gốc \| nền \| làn \| bước | thống kê giây |
|---|---|
| gate-cong-cu | ubuntu-latest | day_du | G5 manh ban kinh dot bien (#668) | n=7414 · tổng 7955967 · trung vị 1057 · p90 1795 · max 2470 s |
| gate-packet-loop | ubuntu-latest | day_du | packet-loop selftest | n=703 · tổng 1741720 · trung vị 2437 · p90 3702 · max 8492 s |
| gate-registry | ubuntu-latest | day_du | test registry (phạm vi + các bộ chưa được nối) | n=877 · tổng 1073065 · trung vị 1252 · p90 2180 · max 3060 s |
| gate-nhanh-manh | ubuntu-latest | day_du | chạy mảnh nhanh_don_duoc (targeted_mutant_gate) | n=7445 · tổng 405700 · trung vị 48 · p90 76 · max 92 s |
| gate-packet-loop-manh | ubuntu-latest | day_du | packet-loop selftest | n=2625 · tổng 305528 · trung vị 104 · p90 184 · max 351 s |
| gate-registry | ubuntu-latest | duong_nhanh | test registry (phạm vi + các bộ chưa được nối) | n=222 · tổng 253993 · trung vị 1337.5 · p90 2184 · max 2516 s |
| gate-cong-cu | ubuntu-latest | duong_nhanh | G5 manh ban kinh dot bien (#668) | n=189 · tổng 247594 · trung vị 1381 · p90 1848 · max 1933 s |
| gate-nhanh-manh | ubuntu-latest | duong_nhanh | chạy mảnh nhanh_don_duoc (targeted_mutant_gate) | n=1997 · tổng 109984 · trung vị 48 · p90 77 · max 88 s |
| gate-cong-cu | ubuntu-latest | day_du | Run actions/checkout@v4 | n=7447 · tổng 67594 · trung vị 9 · p90 11 · max 959 s |
| gate-nhanh-manh | ubuntu-latest | day_du | Run actions/checkout@v4 | n=7451 · tổng 65856 · trung vị 9 · p90 11 · max 175 s |
| gate-cong-cu | ubuntu-latest | day_du | cài rg cho G5 (cài xong đo lại) | n=7431 · tổng 55345 · trung vị 5 · p90 10 · max 234 s |
| gate-packet-loop-manh | ubuntu-latest | duong_nhanh | packet-loop selftest | n=368 · tổng 43554 · trung vị 107 · p90 178 · max 307 s |

## M2b — thời gian theo bộ test và chế độ (`CI_DANG_KY_THOI_GIAN`)

45 khoá (job nguồn | nền | bộ). 15 khoá có tổng giây lớn nhất:

| job nguồn \| nền \| bộ | bản ghi | rc≠0 | chế độ: n / trung vị / p90 (s) |
|---|---|---|---|
| gate-registry | ubuntu-latest | ops/ci_provenance_test.py | 660 | 1 | day_du: 660 / 1371.686 / 2181.415 |
| gate-registry | ubuntu-latest | .claude/hooks/pretooluse_guard_test.py | 829 | 3 | day_du: 134 / 1009.181 / 1261.389; nhe: 695 / 25.953 / 34.767 |
| gate-registry | ubuntu-latest | ops/cloud_agent_creds_test.py | 428 | 4 | day_du: 428 / 319.861 / 339.001 |
| gate-registry | ubuntu-latest | ops/land_evidence_nguon_test.py | 829 | 7 | day_du: 829 / 95.546 / 119.054 |
| dot-bien-du | ubuntu-latest | ops/ci_provenance_test.py | 40 | 0 | day_du: 40 / 1296.541 / 2525.795 |
| dot-bien-du | ubuntu-latest | .claude/hooks/pretooluse_guard_test.py | 51 | 0 | day_du: 51 / 1046.378 / 1280.736 |
| gate-registry | ubuntu-latest | .claude/hooks/subagent_ghi_detect_test.py | 829 | 0 | day_du: 124 / 276.071 / 407.612; nhe: 705 / 10.973 / 15.526 |
| gate-registry | ubuntu-latest | .claude/dev/doc_receipt_thu_hoi_test.py | 829 | 0 | day_du: 829 / 11.35 / 182.724 |
| gate-registry | ubuntu-latest | .claude/dev/mcp_gh_test.py | 829 | 0 | day_du: 829 / 36.853 / 58.636 |
| dot-bien-du | ubuntu-latest | .claude/hooks/subagent_ghi_detect_test.py | 51 | 0 | day_du: 51 / 266.728 / 359.967 |
| dot-bien-du | ubuntu-latest | ops/cloud_agent_creds_test.py | 40 | 0 | day_du: 40 / 325.267 / 346.795 |
| dot-bien-du | ubuntu-latest | ops/land_evidence_nguon_test.py | 46 | 0 | day_du: 46 / 104.863 / 117.818 |
| dot-bien-du | ubuntu-latest | ops/nhanh_don_duoc_test.py | 51 | 0 | day_du: 1 / 3219.692 / 3219.692; nhe: 50 / 1.315 / 1.822 |
| gate-registry | ubuntu-latest | ops/kiem_ho_so_land_test.py | 684 | 0 | day_du: 684 / 4.208 / 5.256 |
| dot-bien-du | ubuntu-latest | .claude/dev/doc_receipt_thu_hoi_test.py | 49 | 0 | day_du: 49 / 11.091 / 183.509 |

## M3 — kiểm kê tĩnh

- `.claude/dev/ci_dang_ky_test.py` (import, `len()`): DANG_KY=29 · MOI=15 · NHE=3 · MOI_WINDOWS=1 · CACH_LY=0 · DA_NOI=14
- `ops/nhanh_don_duoc_test.py` (import, `len()`): CA=8 · TU_KIEM=56 · DOT_BIEN=10 · DOT_BIEN_TU_KIEM=255
- Đếm literal bằng `ast` trên 29 bộ `*_test.py` ở SHA meta: 27 bảng đo được, 14 `khong_do_duoc` (chỉ sinh khi chạy/import), 6 bộ không có bảng tên chuẩn.

| bộ | bảng đo được bằng ast |
|---|---|
| `.claude/dev/chon_reviewer_test.py` | DOT_BIEN=45 |
| `.claude/dev/codex_cred_test.py` | CA=18 · DOT_BIEN=18 |
| `.claude/dev/doc_receipt_thu_hoi_test.py` | CA=47 |
| `.claude/dev/idiom_py_test.py` | CA=7 |
| `.claude/dev/launcher_test.py` | DOT_BIEN=572 |
| `.claude/dev/mcp_github_doc_test.py` | DOT_BIEN=20 |
| `.claude/dev/packet_loop_test.py` | MUTANTS=88 |
| `.claude/dev/probe_mang_test.py` | DOT_BIEN=5 |
| `.claude/hooks/pretooluse_guard_test.py` | CA=44 · DOT_BIEN=43 |
| `.claude/hooks/subagent_ghi_detect_test.py` | CA=45 · DOT_BIEN=25 |
| `ops/ci_duong_nhanh_test.py` | DOT_BIEN=351 |
| `ops/ci_provenance_test.py` | TU_KIEM=2 |
| `ops/cloud_agent_creds_test.py` | DOT_BIEN=91 · TU_KIEM=2 |
| `ops/codex_cloud_setup_test.py` | DOT_BIEN=13 · CA=13 |
| `ops/cong_cu_test.py` | DOT_BIEN=254 |
| `ops/kiem_ho_so_land_test.py` | CA=11 |
| `ops/kiem_nhan_hint_test.py` | CA=6 |
| `ops/land_evidence_nguon_test.py` | DOT_BIEN=116 · TU_KIEM=2 |
| `ops/nhanh_don_duoc_test.py` | DOT_BIEN=10 · TU_KIEM=56 · DOT_BIEN_TU_KIEM=255 |

## 5 điểm tốn thời gian nhất theo giây thực thi (nhóm job, cả cohort)

| # | workflow | job gốc | tổng giây thực thi | số dòng thực thi | trung vị s |
|---|---|---|---|---|---|
| 1 | ci.yml | gate-cong-cu | 8542030 | 7832 | 1079.5 |
| 2 | ci.yml | gate-packet-loop | 1796318 | 1489 | 42 |
| 3 | ci.yml | gate-registry | 1371883 | 1472 | 913 |
| 4 | ci.yml | gate-ops | 1238470 | 1508 | 757.5 |
| 5 | ci.yml | gate-nhanh-manh | 830933 | 11997 | 59 |

Nguồn: tổng `completed_at − started_at` của mọi dòng `thuc_thi` cùng tên gốc trong các tệp `jobs/*` của ảnh chụp (URL từng lượt ở `M1.luot[].nguon`, `actions/runs/<id>/jobs?filter=all`).

## M4 — đối chiếu lời khai

Lệnh: `rg -n -i 'đột biến|dot.bien|mutant|mutation|mảnh' .github/workflows CLAUDE.md docs ops/specs/wp1166* | rg -i "<M4_RG2>" (tuong duong: hai regex M4_RG1 roi M4_RG2 trong thu_thap.py, ap tren `git show <sha_master>:<tep>`)`. 36 dòng khớp; kết luận: {'khong_do_duoc': 31, 'khop': 3, 'lech': 7}.

| vị trí | lời khai | số đo | kết luận | ghi chú |
|---|---|---|---|---|
| `.github/workflows/ci-dot-bien-du.yml:9@711cb190daaa` | 52 ca | 56 | **lech** | anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact |
| `.github/workflows/ci-dot-bien-du.yml:9@711cb190daaa` | 239 tu dot bien | 255 | **lech** | anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact |
| `.github/workflows/ci-dot-bien-du.yml:9@711cb190daaa` | 10 dot bien san pham | 10 | **khop** | anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact |
| `.github/workflows/ci-dot-bien-du.yml:11@711cb190daaa` | ~73 800 s noi tiep | 13010 s = tong 8 job manh | **lech** | khop neu trong ±20% (loi khai dang '~'); luot 43990524880 (luot du 8 manh success moi nhat cua cohort): https://api.github.com/repos/ducthangho/tra-luat/actions/runs/43990524880/jobs?filter=all |
| `.github/workflows/ci-dot-bien-du.yml:11@711cb190daaa` | 8 manh ≈ 2,6 h/manh (9 360 s) | 1621.5 s = trung vi 8 job manh (1531–1730 s) | **lech** | khop neu trong ±20%; luot 43990524880 (luot du 8 manh success moi nhat cua cohort): https://api.github.com/repos/ducthangho/tra-luat/actions/runs/43990524880/jobs?filter=all |
| `.github/workflows/ci.yml:568@711cb190daaa` | 8 manh skipped (0 phut runner) o duong_nhanh | 517 luot duong_nhanh tao sau 2026-10-23T23:37:49Z: dong gate-cong-cu {'bo_qua': 521, 'thuc_thi_khong_runner': 2}; ca cohort (542 luot duong_nhanh): {'bo_qua': 521, 'thuc_thi': 205, 'mang_sang': 29} | **khop** | chi tinh luot tao SAU committer-time cua dong loi khai (git blame --first-parent --porcelain -L 568,568 711cb190daaa -- .github/workflows/ci.yml); khop neu khong dong gate-cong-cu nao la thuc_thi CO runner (thuc_thi_khong_runner = dong bi huy truoc khi duoc cap runner: labels rong, khong buoc nao, khong phai skipped); lan doc tu log chuan-bi |
| `.github/workflows/ci.yml:934@711cb190daaa` | 52 ca | 56 | **lech** | anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact |
| `.github/workflows/ci.yml:934@711cb190daaa` | 239 tu dot bien | 255 | **lech** | anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact |
| `.github/workflows/ci.yml:934@711cb190daaa` | 10 dot bien san pham | 10 | **khop** | anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact |
| `.github/workflows/ci.yml:1121@711cb190daaa` | run 43845962754: mot job 2 gio 21 phut | job gate-packet-loop (ubuntu-latest) dai nhat cua luot: 8524 s = 2 gio 22 phut 4 giay; buoc dai nhat cua job ay: 8492 s | **lech** | khop neu thoi luong JOB cat hoac lam tron ve phut bang 141 phut; https://api.github.com/repos/ducthangho/tra-luat/actions/runs/43845962754/jobs?filter=all |

## Lời khai lệch

- `.github/workflows/ci-dot-bien-du.yml:9@711cb190daaa` — khai “52 ca”, đo 56. anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact
- `.github/workflows/ci-dot-bien-du.yml:9@711cb190daaa` — khai “239 tu dot bien”, đo 255. anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact
- `.github/workflows/ci-dot-bien-du.yml:11@711cb190daaa` — khai “~73 800 s noi tiep”, đo 13010 s = tong 8 job manh. khop neu trong ±20% (loi khai dang '~'); luot 43990524880 (luot du 8 manh success moi nhat cua cohort): https://api.github.com/repos/ducthangho/tra-luat/actions/runs/43990524880/jobs?filter=all
- `.github/workflows/ci-dot-bien-du.yml:11@711cb190daaa` — khai “8 manh ≈ 2,6 h/manh (9 360 s)”, đo 1621.5 s = trung vi 8 job manh (1531–1730 s). khop neu trong ±20%; luot 43990524880 (luot du 8 manh success moi nhat cua cohort): https://api.github.com/repos/ducthangho/tra-luat/actions/runs/43990524880/jobs?filter=all
- `.github/workflows/ci.yml:934@711cb190daaa` — khai “52 ca”, đo 56. anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact
- `.github/workflows/ci.yml:934@711cb190daaa` — khai “239 tu dot bien”, đo 255. anh xa: '52 ca' <-> len(TU_KIEM), '239 tu dot bien' <-> len(DOT_BIEN_TU_KIEM), '10 dot bien san pham' <-> len(DOT_BIEN); import ops/nhanh_don_duoc_test.py@711cb190daaa; doi chieu phu: luot du moi nhat 43990524880 co 321 muc theo log, 321 theo artifact
- `.github/workflows/ci.yml:1121@711cb190daaa` — khai “run 43845962754: mot job 2 gio 21 phut”, đo job gate-packet-loop (ubuntu-latest) dai nhat cua luot: 8524 s = 2 gio 22 phut 4 giay; buoc dai nhat cua job ay: 8492 s. khop neu thoi luong JOB cat hoac lam tron ve phut bang 141 phut; https://api.github.com/repos/ducthangho/tra-luat/actions/runs/43845962754/jobs?filter=all

## Không đo được

646 mục nguồn (chi tiết + URL ở `BASELINE.json` → `khong_do_duoc.chi_tiet`). Tóm tắt theo dạng:

- 269 × ban ghi CI_DANG_KY_THOI_GIAN job <id> luot <id> (ket luan job cancelled) — khong_co_ban_ghi
- 110 × thoi luong job <id> (gate-cong-cu-gop) luot <id> — thoi_gian_dao (completed_at < started_at)
- 52 × thoi luong job <id> (gate-registry) luot <id> — thoi_gian_dao (completed_at < started_at)
- 43 × thoi luong job <id> (gate-nhanh-gop) luot <id> — thoi_gian_dao (completed_at < started_at)
- 37 × log manh job <id> luot <id> — cat_cut
- 29 × thoi luong job <id> (gate-packet-loop) luot <id> — thoi_gian_dao (completed_at < started_at)
- 23 × log job <id> (chuan-bi, ket luan job failure) — loi (HTTP 404)
- 16 × log manh job <id> luot <id> — khong_co_ban_ghi
- 12 × log job <id> (chuan-bi, ket luan job cancelled) — loi (HTTP 404)
- 8 × log job <id> (dot-bien-manh, ket luan job failure) — loi (HTTP 404)
- 7 × thoi luong job <id> (gate-cong-cu) luot <id> — thoi_gian_dao (completed_at < started_at)
- 6 × ban ghi CI_DANG_KY_THOI_GIAN job <id> luot <id> — khong_co_ban_ghi
- 6 × log job <id> (dot-bien-gop, ket luan job cancelled) — loi (HTTP 404)
- 6 × thoi luong job <id> (gate) luot <id> — thoi_gian_dao (completed_at < started_at)
- … và 9 dạng khác (xem `khong_do_duoc.tom_tat`)
- Lời khai M4 không có phép đo tương ứng: 31 (danh sách ở `M4.loi_khai`).
- M3: bảng không phải literal tĩnh hoặc literal rỗng được điền khi chạy — ghi `khong_do_duoc`, không chạy bộ để lấy số.
- Thời điểm workflow hoàn tất: API attempt không trả `completed_at`; chỉ có `dau_cuoi_suy_ra_tu_job`.
- Workflow đột biến ngoài cohort (vd. `packet-loop-dot-bien.yml`) không được thu: đặc tả §2 chỉ định hai workflow.

## Kết quả hai bộ phân loại §6 (trên tập đường dẫn của packet)

Tập đường dẫn (mọi tệp là `A`, mode `100644`): `ops/specs/wp1434-r3/do/BAO_CAO.md`, `ops/specs/wp1434-r3/do/BASELINE.json`, `ops/specs/wp1434-r3/do/COHORT.json`, `ops/specs/wp1434-r3/do/fixtures/artifacts.json`, `ops/specs/wp1434-r3/do/fixtures/attempt_cuoi_rong.json`, `ops/specs/wp1434-r3/do/fixtures/buoc.json`, `ops/specs/wp1434-r3/do/fixtures/cohort_bien.json`, `ops/specs/wp1434-r3/do/fixtures/log_chuan_bi.log`, `ops/specs/wp1434-r3/do/fixtures/log_chuan_bi_cu.log`, `ops/specs/wp1434-r3/do/fixtures/log_dang_ky_cat_cut.log`, `ops/specs/wp1434-r3/do/fixtures/log_dang_ky_con.log`, `ops/specs/wp1434-r3/do/fixtures/log_dang_ky_thieu.log`, `ops/specs/wp1434-r3/do/fixtures/log_manh_cat_cut.log`, `ops/specs/wp1434-r3/do/fixtures/log_manh_con.log`, `ops/specs/wp1434-r3/do/fixtures/log_manh_thieu.log`, `ops/specs/wp1434-r3/do/fixtures/luot_hai_attempt.json`, `ops/specs/wp1434-r3/do/fixtures/mang_sang_cung_job_id.json`, `ops/specs/wp1434-r3/do/thu_thap.py`
- `phan_loai_tu_diff` ⇒ `["duong_nhanh", "DUONG_NHANH: toan bo 18 tep doi khop allowlist ops/{land,leases,reviews,specs}/** - dung duong nhanh"]`
- `ly_do_ve_day_du` ⇒ `[]`
- `phan_loai_packet_loop` ⇒ `["bo_qua", "PACKET_LOOP: bo_qua vi 18 tep doi khong cham tap phu thuoc cua bo ca"]`
- `tim` ⇒ `{"so_test_song": 29, "so_hien_vat": 2, "vi_tri_la": [], "tep_packet_trong_ket_qua": []}`

Làn của PR phải được đo lại trên log CI thật trước merge (đặc tả §6); kết quả trên là phép chạy tại chỗ của hai hàm phân loại.
