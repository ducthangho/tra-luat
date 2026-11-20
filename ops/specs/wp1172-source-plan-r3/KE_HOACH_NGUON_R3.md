# KẾ HOẠCH NGUỒN r3 — tối ưu mutation testing (Mission #1172, PR1–PR8) — bản sửa 4

## 1. Trạng thái

- **Trạng thái: `proposed`.** Chưa ai duyệt; chưa đóng băng (sha256 do phiên điều phối ghi sau khi nhận tệp).
- **Bản thay thế cho kế hoạch nguồn r2 đã MẤT; KHÔNG phải bản gốc.** r2 (sha256 `f4611b0f…`) không còn và không được
  dựng lại ở đây. r3 là một kế hoạch mới, đặt tên riêng, dựng trên phép đo. Không câu nào dưới đây là trích từ r2.
- **Nguồn nền:** `ops/specs/wp1434-r3/do/BASELINE.json`, sha256
  `6100c8e18907f59b1abbdc44195861cc2310c654ce8dcfa2e74ca4ffa155f54c`, tại merge commit
  `5e5d2cc192758b5a372a875827987b6f471704c0` (băm đã đo lại: khớp). Cohort `meta.T0` = 2026-10-21T01:16:24Z,
  `meta.T1` = 2026-11-20T01:16:24Z, `meta.sha_master` = `711cb190…`. Mọi số dòng mã trích dưới đây đọc tại `5e5d2cc`.
- **Bản này sửa bản `43137d53…`** (chuỗi: `c9090f77…` → `7fe0545b…` → `43137d53…`) sau ba lượt review Codex; vòng 3b còn
  1 P2 (G4) + 2 P3, đều xử lý ở đây, không đổi thiết kế. Vòng
  2: 5/9 finding vòng 1 đã đóng, 4 đóng một phần, thêm R3-10; mọi giá trị `[B: …]` khớp. Nền số GIỮ NGUYÊN trừ `[DX-2]`
  (tính lại, khử trùng). Thứ tự, bao đóng bảo thủ, audit cộng thêm, mặc định hằng đêm, kết cục PR8 giữ nguyên. Mục 10.
- PR0 (#1166, ghim SHA cho full audit) đã xong; r3 không đổi gì của PR0.
- **Quy ước nguồn số.** `[B: đường.khoá]` = đọc thẳng từ BASELINE. `[DX-n]` = DẪN XUẤT, cách tính ở mục 9. Số không mang
  một trong hai nhãn là ƯỚC LƯỢNG và được nói rõ tại chỗ.
- Soạn ở chế độ chỉ đọc: không chạy bộ test hay vòng đột biến nào, không sửa kho.

## 2. Vấn đề, theo số đo

1. **Quy mô.** 1573 lượt `ci.yml` trong 30 ngày `[B: M2.so_luot]`, tổng 15 057 171 giây thực thi, trung vị 12 163 s/lượt,
   p90 18 519 s `[B: M2.moi_luot.tat_ca.giay_thuc_thi]`. Làn: `day_du` 945 · `duong_nhanh` 542 · `khong_do_duoc` 86
   `[B: M2.theo_lan]`.
2. **Một bước chiếm hơn nửa.** Bước `G5 manh ban kinh dot bien (#668)` của `gate-cong-cu` (làn `day_du`, Ubuntu):
   n=7414, tổng 7 955 967 s, trung vị 1057 s, p90 1795 s
   `[B: M2.theo_buoc.bang."gate-cong-cu | ubuntu-latest | day_du | G5 manh ban kinh dot bien (#668)"]` = 52,8 % tổng
   giây `ci.yml`. Cả job: 8 542 030 s `[B: top5_giay_thuc_thi[0]]`. Trong mã: mỗi đột biến chạy lại TRỌN bộ ca
   (`_do_ban_kinh`, `ops/cong_cu_test.py`), 490 đột biến × 61 ca `[B: M3.bang."ops/cong_cu_test.py"]`, tối đa 4 tiến
   trình con song song mỗi mảnh; job chạy ở MỌI lượt không phải `duong_nhanh`, bất kể diff chạm gì.
3. **Phần PR và phần push.** `gate-cong-cu` làn `day_du`: 5,71 triệu s ở `pull_request`, 2,57 triệu s ở `push`
   `[DX-2]`. Lượt PR `day_du`: 705 lượt, 9 669 927 s `[B: M2.moi_luot.theo_su_kien_va_lan."pull_request | day_du"]`.
4. **Registry bị một bộ kéo.** `ops/ci_provenance_test.py` trong `gate-registry`: 660 bản ghi, TẤT CẢ `day_du`, tổng
   1 000 101 giây-bộ, trung vị 1371,7 s `[B: M2b.bang."gate-registry | ubuntu-latest | ops/ci_provenance_test.py"]`; bước
   registry trung vị 1252 s `[B: M2.theo_buoc.bang."gate-registry | ubuntu-latest | day_du | test registry (phạm vi + các
   bộ chưa được nối)"]`. Hai bộ ĐÃ có chế độ nhẹ theo diff chỉ `day_du` 134/829 và 124/829 lần
   `[B: M2b.bang."gate-registry | ubuntu-latest | .claude/hooks/pretooluse_guard_test.py"]`,
   `[…subagent_ghi_detect_test.py]`. `ci_provenance_test` (398 đột biến `[B: M3.bang."ops/ci_provenance_test.py"]`)
   chưa nằm trong bảng `NHE`.
5. **Lượt bị huỷ.** 542/1573 lượt `cancelled` `[B: M2.theo_ket_luan]`, mang 3 633 319 s = 24,1 % `[DX-1]`. Riêng G5 làn
   `day_du`: 1771 dòng mảnh `cancelled` `[B: M2.theo_job.bang."gate-cong-cu | ubuntu-latest | day_du".ket_luan]`.
6. **Full audit không phải khoản lớn, và không "hằng tuần".** `ci-dot-bien-du.yml`: 62 lượt `[B: M1.so_luot]`, 55
   `workflow_dispatch` + 7 `schedule` `[B: M1.luot[].su_kien]`, 61 SHA khác nhau `[B: M1.luot[].head_sha]`; một lượt đủ:
   trung vị 13 282 s cho 8 job mảnh `[B: M1.luot_du_8_manh_success.tong_giay_8_job_manh_moi_luot]`. 62 lượt ấy trải
   2026-09-26 … 2026-11-17; trong `[T0, T1]` là 54 lượt, 700 504 s `[DX-5]` = 4,7 % so với `ci.yml`. r3 KHÔNG cắt khoản này.
7. **Nền đã dịch trong chính cohort.** wp892 (23-10) bỏ mảnh G5 ở `duong_nhanh` (266 557 s
   `[B: M2.theo_job.bang."gate-cong-cu | ubuntu-latest | duong_nhanh"]` là chi phí trước đó). wp1343/wp1353 (16→17-11) thay
   `gate-packet-loop` một khối (1 796 318 s `[B: top5_giay_thuc_thi[1]]`) bằng 16 mảnh và chuyển 1864 đột biến
   `[B: M3.bang.".claude/dev/packet_loop_test.py".MUTANTS]` cùng hai ca dài `CA_DAI` sang `packet-loop-dot-bien.yml` hằng
   đêm, NGOÀI cohort. r3 không tính `gate-packet-loop` là chỗ còn cắt; mốc so là tiểu cohort sau 17-11 `[DX-4]`.
8. **Bộ phân loại so với gốc cũ.** `doc_diff` (`ops/ci_duong_nhanh.py`) hợp thêm diff `base.sha của sự kiện → github.sha`;
   master tiến sau `base.sha` thì thay đổi của chính master lọt vào tập "tệp đổi" và ép `day_du` (quan sát: PR #1439, run
   44666569674). Tần suất: không có trong BASELINE.
9. **Hiện trạng sau merge KHÔNG phải "luôn đủ".** 88 lượt `push | duong_nhanh`
   `[B: M2.moi_luot.theo_su_kien_va_lan."push | duong_nhanh".so_luot]` bỏ cả ma trận G5 (`ci.yml`:570-572) và bước
   registry; ở lượt push `day_du`, registry vẫn chọn chế độ nhẹ theo diff (`ci_dang_ky_test.py`:864-897). Chỉ bộ ca
   packet-loop được wp1353 bảo đảm chạy ở mọi push. Kế hoạch phải nói đúng hiện trạng này (mục 4, I5).

## 3. Chỉ số mục tiêu

Tổng theo tuần trong cohort dao động 1,31–4,73 triệu s `[DX-6]`, nên chỉ số chính là số chuẩn hoá theo lượt; tổng 30 ngày
quy về khối lượng cohort (1187 lượt PR + 386 lượt push `[B: M2.luot[].su_kien]`).

**Quần thể so sánh (đóng băng).** PR4 đổi kết quả phân loại, nên "lượt `day_du`" trước và sau không cùng quần thể. Từ PR1,
mỗi lượt ghi cả phân loại theo luật CŨ lẫn luật đang chạy; G1–G3 tính trên các lượt PR mà **luật cũ** xếp `day_du`, tách
ba dòng: mọi kết luận · `success` · `cancelled`. Lượt không đọc được phân loại vào dòng "không rõ", không vào tử hay mẫu.

| # | Chỉ số | Nền | Mục tiêu | Độ nhạy (HEURISTIC) |
|---|---|---|---|---|
| G1 | Giây thực thi trung bình mỗi lượt PR `day_du` (luật cũ), mọi kết luận | cohort 13 716 s (9 669 927 / 705) `[B: …"pull_request \| day_du".giay_thuc_thi]`; mốc sau 17-11: 10 659 s, n=184, lệch chuẩn 4603 `[DX-4]` | sau PR3: ≤ 9 600 s (−10 %); sau PR6: ≤ 7 500 s (−30 %); PR6 bị từ chối ⇒ dừng ở ≤ 9 600 | ≈ 1 070–1 340 s nếu coi các lượt là độc lập `[DX-7]`; chúng KHÔNG độc lập (nhiều lượt/PR, 101/184 lượt mốc bị huỷ) nên nghiệm thu dùng bootstrap theo CỤM PR |
| G2 | Tổng giây `ci.yml` / 30 ngày, quy về khối lượng cohort | 15 057 171 s `[B: M2.moi_luot.tat_ca.giay_thuc_thi.tong]` | sau PR3: ≤ 13,8 triệu; sau PR6+PR7: ≤ 12,0 triệu; PR6 bị từ chối ⇒ ≤ 13,8 triệu | suy từ trung bình theo (sự kiện, làn luật cũ) × số lượt cohort; không so tổng thô |
| G3 | Đầu-cuối trung vị, lượt PR `day_du` `success` một attempt | cohort 2742 s; mốc sau 17-11: 1775 s, n=71, p25 1590 `[DX-4]` | sau PR3: p25 ≤ 1 300 s; sau PR6: trung vị ≤ 1 500 s | chưa có phép tính lực cho trung vị; khoảng bootstrap 1688–1865 chỉ là độ bất định của MỐC. Đòi n ≥ 150 lượt mỗi vế và khoảng bootstrap theo cụm PR của HIỆU hai trung vị không chứa 0 |
| G4 | **G4a** tỷ lệ CHỌN chế độ G5 (đường nhanh đang chạy · bỏ mới PR3 · đích · đủ · không phân loại được) và **G4b** tỷ lệ PHỦ HOÀN TẤT (phép quy có thứ tự dưới bảng), cùng một mẫu số | G4a: đủ = 100 % theo CHÍNH SÁCH; G4b: CHƯA ĐO | sau PR3: G4a `bo_moi` ≥ 10 % (trung tâm 23 %), không tính `duong_nhanh_dang_chay`; G4b `thieu_bang_chung` ≤ 2 % mẫu số; `dang_do`, `gom_hong` chỉ báo cáo; mọi lượt của mẫu số rơi vào đúng một loại | ±3–4 điểm % ở n≈700 nếu độc lập; báo kèm khoảng theo cụm PR |
| G5 | Tỷ lệ làn `day_du` | 945/1573 = 60,1 % `[B: M2.theo_lan]`; PR 705/1187 = 59,4 % | KHÔNG đặt mục tiêu giảm. Sau PR4: bộ đếm SAI SÓT TỒN DƯ (phân loại đang chạy ≠ oracle ngữ cảnh mới) = 0; bộ đếm LỢI ÍCH (luật cũ ≠ ngữ cảnh mới) chỉ báo cáo, kỳ vọng > 0 | ±2,4 điểm % (nhị thức, n=1573) |
| G6 | Full audit M9: DANH TÍNH mục và job | 321 khoá `[B: M1.muc_ket_qua_theo_khoa.so_khoa]`; job `dot-bien-du`, 8 `dot-bien-manh`, `dot-bien-gop` `[B: M1.theo_job]` | tập khoá sau ⊇ tập khoá trước (so TÊN, không so số đếm); sau PR5 thêm đúng 8 mảnh G5 + gom G5 | đếm chính xác |

**Mẫu số G4 (đóng băng, không đổi).** Lượt `pull_request`, attempt cuối của mỗi `run_id`, mà `chuan-bi` hoàn tất và luật
CŨ xếp `day_du`. Lượt được luật đang chạy xếp lại (ca dương của PR4) và lượt dang dở VẪN nằm trong mẫu số; không loại
chúng ra, vì loại là tạo thiên lệch chọn mẫu.

**G4a — chế độ ĐƯỢC CHỌN** (mỗi lượt của mẫu số đúng một loại): `duong_nhanh_dang_chay` (luật đang chạy xếp
`duong_nhanh`; G5 bị bỏ theo luật SẴN CÓ của wp892) · `bo_moi` (`che_do` đang chạy = `day_du` và `cong_cu=bo_qua` của PR3)
· `dich` (từ PR6) · `du` · `khong_phan_loai_duoc`. Mục tiêu "bỏ mới ≥ 10 %" chỉ đếm `bo_moi`.

**Phép quy G4b — phủ HOÀN TẤT, CÓ THỨ TỰ và VÉT CẠN.** Xét từ trên xuống, bước ĐẦU TIÊN khớp quyết định loại; bước 10
nhận mọi thứ còn lại, nên mỗi lượt rơi vào đúng một loại. Bước 0–1 áp cho MỌI lượt PR và đưa lượt ra ngoài mẫu số.

| Bước | Điều kiện ở attempt cuối | Loại | Trong mẫu số | Tính vào trần 2 % |
|---|---|---|---|---|
| 0 | `chuan-bi` bị huỷ/hỏng trước khi in phân loại | `huy_truoc_phan_loai` | không (đếm riêng) | không |
| 1 | luật cũ KHÔNG xếp `day_du` | `ngoai_mau_so` | không | không |
| 2 | không đọc được chế độ đang chạy (log/output thiếu) | `thieu_bang_chung` | có | CÓ |
| 3 | đang chạy `duong_nhanh` + job gom `success` in "KHÔNG ĐO" với dấu của `duong_nhanh` | `duong_nhanh_co_bang_chung` | có | không; KHÔNG tính vào "bỏ mới" |
| 4 | `cong_cu=bo_qua` (PR3) + job gom `success` in "KHÔNG ĐO" với dấu của bỏ mới | `bo_moi_co_bang_chung` | có | không |
| 5 | 8 biên nhận mảnh hợp lệ chế độ `du` + job gom `success` | `du_hoan_tat` | có | không |
| 6 | 8 biên nhận mảnh hợp lệ chế độ `dich` + job gom `success` (từ PR6) | `dich_hoan_tat` | có | không |
| 7 | job gom `failure`/`cancelled`/không khởi động, khi mọi biên nhận cần có đã đủ HOẶC chế độ chọn là bỏ (bước 3–4 dang dở) | `gom_hong` | có | không; báo riêng |
| 8 | chọn `du` hoặc `dich`, bị huỷ/đỏ, thiếu ít nhất một biên nhận | `dang_do` (kèm chế độ) | có | không; báo riêng |
| 9 | job báo `success` nhưng biên nhận thiếu, sai chế độ, sai head, hoặc dấu "KHÔNG ĐO" không khớp chế độ đã chọn | `thieu_bang_chung` | có | CÓ |
| 10 | mọi trường hợp còn lại | `thieu_bang_chung` | có | CÓ |

Chỉ bước 5 và 6 là phủ hoàn tất; bước 7 và 8 KHÔNG bao giờ thành hoàn tất. Trần: `thieu_bang_chung` (bước 2, 9, 10) ≤ 2 %
mẫu số. "100 % đủ" hôm nay là phát biểu CHÍNH SÁCH (điều kiện job), không phải phép đo: trong 184 lượt mốc, 95 attempt
cuối không có đủ 8 job G5 `success` (số của reviewer; không suy ra 95 lượt "không rõ", chỉ chứng minh chọn đủ ≠ hoàn tất
đủ). Phủ hoàn tất lịch sử để CHƯA ĐO, trừ khi PR1 dựng lại được từ artifact. Chi phí của mọi loại vẫn nằm trong G1/G2.

**Cách đo lại.** Bộ thu MỞ RỘNG của PR1 (bản mới, không sửa `ops/specs/wp1434-r3/**`), cùng quy tắc `meta.quy_tac`, thêm
bản ghi theo (run_id, attempt, sự kiện, head): chế độ dự định, chế độ thực chạy, lý do bỏ, trạng thái hoàn tất, dấu hiệu
dương. Bộ thu của #1434 gom theo job/nền/làn, không có danh tính lượt, nên KHÔNG đo được G4. Kiểm 14 ngày sau PR3; cohort
30 ngày ở PR8.

## 4. Bất biến an toàn (không thương lượng)

- **I1 — Không giảm full audit M9.** `ci-dot-bien-du.yml` giữ lịch, giữ ma trận gốc (mọi ca dưới mỗi tự đột biến), giữ
  K7 của `ADR-0060`. Lượt targeted không thay được nó. r3 chỉ THÊM (PR5). Bảo toàn theo DANH TÍNH đột biến/ca, không
  theo số đếm.
- **I2 — Mỗi đột biến bị giết ĐÚNG LÝ DO.** Không sửa bảng đột biến để lấy thời gian; giữ phân hạng tín dụng giả; chế độ
  không chạy đủ ca thì không được in "bán kính 1/N" và bản ghi của nó phải mang trường chế độ mà bên đọc kiểm.
- **I3 — Fail-closed ba trạng thái.** Bỏ/giảm chỉ mở bằng đúng một chuỗi cho phép; rỗng, lạ, vắng, lỗi nội bộ, không đo
  được ⇒ chạy đủ. Chưa chứng minh được tính độc lập thì KHÔNG bỏ.
- **I4 — Không bỏ test để lấy xanh.** Job bắt buộc vẫn khởi động, in dấu hiệu dương nói nó đo gì và không đo gì.
- **I5 — Bảo đảm sau merge, phát biểu ĐÚNG phạm vi.** r3 không thêm ngoại lệ nào ở sự kiện `push` cho G5: trên push,
  G5 chạy đủ khi và chỉ khi `che_do != duong_nhanh`, đúng như hôm nay. Ngoại lệ ĐANG CÓ, đã duyệt, r3 giữ nguyên và liệt kê:
  (a) push `duong_nhanh` (diff thuần hồ sơ; wp892/wp1113; 88 lượt trong cohort) bỏ G5 và bước registry; (b) registry `NHE`
  theo diff áp cả ở push (#643/#647/#651), bù bằng lượt đủ của `ci-dot-bien-du.yml`; (c) packet-loop: bộ ca chạy ở mọi
  push (wp1353), bảng đột biến chạy hằng đêm. Vì vậy r3 KHÔNG khai "master luôn được đo đủ"; nó khai: *mọi PR được r3
  cho bỏ MỚI hoặc giảm G5 đều đang ở `che_do` = `day_du` và có đóng góp merge ngoài allowlist hồ sơ đã kiểm, nên lượt push của merge commit ấy là `day_du` và chạy G5 đủ* —
  mệnh đề này là tiêu chí nghiệm thu đo được của PR3 và PR6. Với PR2, phạm vi bù sau merge là (b), không rộng hơn.
- **I6 — Kiểm kê không lùi theo danh tính.** Tập tên các bảng `M3.bang.*` sau mỗi PR ⊇ trước PR, trừ mục được đặc tả
  nêu tên và lý do.

**Năm phép chứng minh, ghi vào đặc tả của mỗi PR:** (a) ca hành vi HAI CHIỀU cho luật mới; (b) đột biến RIÊNG cho từng
chốt mới, gồm đột biến "nới danh sách cho phép", phân hạng bằng lớp ngoại lệ riêng của ca (không bằng `rc ≠ 0`); (c) ca
cho cả ba trạng thái; (d) đối chiếu A/B dựng trong MỘT lệnh trên cùng SHA khi PR khai "kết quả không đổi", so trên TOÀN
BỘ định danh đột biến hiện hành; (e) một lượt `full_mutant_audit` `success` trên đúng head (K7) và lượt push sau merge
đọc theo nhãn job.

## 5. Tám packet

**Thứ tự đề xuất (một chuỗi):** PR1 quan sát → PR2 → PR3 (bật có kiểm chứng) → PR4 → PR5 → PR6 → PR7 → PR8.
**Đồ thị phụ thuộc:** giữ mặc định, với HAI thay đổi nêu rõ: (i) PR6 phụ thuộc thêm PR3 (ngoài PR4+PR5), vì chế độ đích
dùng output và tập phụ thuộc của PR3; (ii) điều kiện "sau PR6" của PR7 được thoả khi PR6 **đã land HOẶC đã bị chủ kho từ
chối bằng văn bản**, để nhánh không-PR6 chạy được. Còn lại: PR1 sau PR0 · PR2 sau PR1 · PR3, PR4 sau PR1+PR2 · PR5 sau
PR0+PR1+PR2 · PR7 sau PR3+PR6 · PR8 sau PR7 + quyết định của chủ kho.
**Ánh xạ nhãn so với bản `c9090f77`:** PR1 mới = đo/quan sát (gồm phần đo của PR4 cũ) · PR2 giữ · PR3 mới = PR1 cũ ·
PR4 mới = PR3 cũ · PR5, PR6, PR7, PR8 giữ nhãn (phần "cân mảnh" của PR4 cũ sang PR7).
PR4, PR7 mang tiêu chí huỷ đo được; khi kích hoạt, packet đóng ở dạng "đã đo, không đổi mã", nhãn giữ nguyên. Mọi PR
đụng `ci.yml` thuộc lớp nhạy cảm; lớp review cụ thể do đặc tả từng packet chốt theo protocol.

### PR1 — Quan sát: đo thời gian G5, bóng tập phụ thuộc, bóng phân loại, bộ thu theo lượt

- **Vấn đề.** Ba con số lớn nhất của kế hoạch chưa có phép đo: tỷ lệ PR độc lập với G5, chi phí ca đích so với ca khác,
  tần suất phân loại đổi do lệch gốc. Bộ thu hiện tại không có danh tính lượt (mục 3).
- **Phạm vi (KHÔNG đổi hành vi cổng nào).**
  1. *Thời gian G5, tách năm đại lượng:* thời gian tường của bước ở tiến trình cha; với từng tiến trình con: mốc bắt
     đầu/kết thúc (khoảng) và CPU; với từng đột biến: dựng cây · ca ĐÍCH · các ca khác. Tối đa 4 con chạy chồng nhau, nên
     đối chiếu thời gian tường bằng HỢP các khoảng / đường găng, KHÔNG bằng tổng; phần không phân bổ được báo riêng. Các
     số này chỉ để báo cáo: bản ghi phán quyết và bộ nhận của job gom không đọc chúng.
  2. *Bóng tập phụ thuộc:* `chuan-bi` in quyết định `cong_cu` DỰ KIẾN theo bao đóng bảo thủ của PR3, kèm định danh lượt;
     không job nào đọc nó.
  3. *Bóng phân loại:* in kết quả phân loại theo luật cũ và theo ngữ cảnh so sánh mới của PR4, kèm bốn OID đầu vào
     (`base.sha` sự kiện, cha thứ nhất, head, `github.sha`). Từ đó hai bộ đếm TÁCH RIÊNG: **LỢI ÍCH** = luật cũ ≠ ngữ
     cảnh mới (thứ PR4 mang lại); **SAI SÓT TỒN DƯ** = phân loại đang chạy ≠ oracle ngữ cảnh mới đã kiểm (trước PR4 chỉ
     ghi để làm mốc; sau PR4 phải = 0).
  4. *Bộ thu mở rộng:* bản ghi theo (run_id, attempt, sự kiện, head) như mục 3; thêm `packet-loop-dot-bien.yml`; thêm thời
     gian theo bước của `gate` và `gate-ops`.
- **Write set dự kiến.** `ops/cong_cu_test.py` (ghi thời gian), `ops/ci_duong_nhanh.py` + `ops/ci_duong_nhanh_test.py`
  (hai dòng bóng), `.github/workflows/ci.yml` chỉ khi cần biến môi trường, thư mục đặc tả/bộ thu MỚI dưới `ops/specs/`.
- **Nghiệm thu.** Năm phép của mục 4; A/B một lệnh cùng SHA: bản ghi phán quyết của mọi định danh đột biến hiện hành
  giống hệt trước/sau; đột biến "dòng bóng lọt vào `GITHUB_OUTPUT`" phải làm ca đỏ; hợp các khoảng con khớp thời gian
  tường của bước trong ±10 %, phần lệch báo thành "không phân bổ"; bộ thu mới chạy lại trên ảnh chụp #1434 tái lập các
  khoá `[B: …]` trích ở mục 2 và hai phép khoá của `[DX-2]`; fixture của bộ thu cho ĐỦ mười bước của phép quy G4b, mỗi
  fixture rơi vào đúng một loại, trong đó bắt buộc có: lượt chế độ đủ bị huỷ giữa chừng (như run 44126854175: cả 8 mảnh
  `cancelled`) KHÔNG thành `du_hoan_tat`; ca dương của PR4 (luật cũ `day_du`, đang chạy `duong_nhanh`, job gom `success` in
  "KHÔNG ĐO") ra `duong_nhanh_co_bang_chung`, KHÔNG ra `thieu_bang_chung` và KHÔNG được tính vào mục tiêu "bỏ mới"; đủ 8
  biên nhận nhưng job gom `cancelled` (như run 44443875641, job 135300180039) ra `gom_hong`; chọn bỏ mà job gom
  `cancelled` ra `gom_hong`.
- **Tiết kiệm kỳ vọng.** 0 (thêm vài giây mỗi mảnh). **Rủi ro.** Trung bình (đụng tệp test nóng và bộ phân loại, nhưng
  không đổi quyết định nào). **Hoàn tác:** revert.
- **Phụ thuộc:** PR0. **Windows:** một lượt dispatch `windows-only` (Windows chạy mảnh 0 ca nền). **Full M9:** có (K7).
  **Human audit:** khuyến nghị.

### PR2 — Chế độ nhẹ theo diff cho `ci_provenance_test` trong registry

- **Vấn đề.** Mục 2.4: 1 000 101 giây-bộ, 660/660 lần `day_du`, là đường găng của `gate-registry` (trung vị job 1265 s
  `[B: M2.theo_job.bang."gate-registry | ubuntu-latest | day_du"]`).
- **Thiết kế.** Mở rộng cơ chế SẴN CÓ (#643/#647/#651): thêm bộ vào `NHE` với cờ nhẹ MỚI của chính bộ; cờ chỉ bỏ vòng 398
  đột biến, GIỮ ca nền và tự kiểm phân hạng `TU_KIEM` ở mọi lượt; `MAU_DAY_DU`/`MAU_NHE` riêng để dòng nhẹ không đọc thành
  dòng đủ; vùng = cặp bộ/đích + `VUNG_CHUNG` + phần đo thêm. Lượt `ci-dot-bien-du.yml` không có biến diff nên vẫn chạy đủ
  (`loi_workflow_dot_bien_du`). **Chính sách push:** theo đúng luật đang áp cho ba bộ `NHE` hiện có, tức push cũng chọn
  nhẹ theo diff (ngoại lệ (b) của I5); phương án ép đủ ở push là câu hỏi Q3. Xét cùng lúc `ops/cloud_agent_creds_test.py`
  (428 bản ghi, 133 426 giây-bộ) và `ops/land_evidence_nguon_test.py` (829, 77 974) `[B: M2b.bang.*]`, chỉ đưa vào nếu vùng gọn.
- **Write set dự kiến.** `.claude/dev/ci_dang_ky_test.py`, `ops/ci_provenance_test.py`; `ci.yml` chỉ khi băm
  `BAM_GATE_REGISTRY` buộc đổi.
- **Nghiệm thu.** Năm phép của mục 4, gồm đột biến "cờ nhẹ rò sang lượt đủ", "vùng thiếu tệp đích", "cờ nhẹ bỏ luôn tự
  kiểm phân hạng"; diff chạm vùng ⇒ `day_du`, không đo được ⇒ `day_du`; lượt đủ sau merge in dòng đủ với TẬP tên đột biến
  ⊇ trước PR; đo lại: tỷ lệ `day_du` của bộ ≤ 30 % bản ghi, trung vị bước registry ≤ 600 s (đọc thời gian JOB/BƯỚC).
- **Tiết kiệm kỳ vọng.** ƯỚC LƯỢNG: nếu tỷ lệ `day_du` như hai bộ tiền lệ (≈16 %), mỗi lượt được nhẹ cắt ≈ 950–1050 s
  giây job (đường găng còn lại ≈ 320–400 s, do `cloud_agent_creds_test` trung vị 319,9 s) ⇒ 0,4–0,7 triệu s / 30 ngày.
  Nếu chủ kho chọn ép đủ ở push (Q3): trừ khoảng 0,15–0,24 triệu (240 lượt push `day_du` × 650–1000 s).
- **Rủi ro.** Thấp–trung bình. **Hoàn tác:** bỏ bộ khỏi `NHE` (một dòng) hoặc revert.
- **Phụ thuộc:** PR1. **Windows:** một lượt dispatch. **Full M9:** có. **Human audit:** khuyến nghị.

### PR3 — Bật: G5 trên PR chỉ chạy khi diff chạm BAO ĐÓNG phụ thuộc bảo thủ (đã qua bóng)

- **Vấn đề.** Mục 2.2–2.3. Bản trước đề xuất tập phụ thuộc theo vết inotify; vết ấy KHÔNG đủ làm hợp đồng: `_goi_ngoai`
  (`ops/cong_cu_test.py`:2697-2735) quét mọi `*.py` trực tiếp dưới `ops/` và `.claude/dev/` và dùng TÊN tệp của
  `scripts/*.py`, nên thêm/xoá/đổi tên tệp cũng đổi kết quả; tiền lệ wp1343 tự khai không đo đọc qua object git và `CA_DAI`.
- **Thiết kế.** Output thứ ba `cong_cu=chay|bo_qua` của `ops/ci_duong_nhanh.py`. `bo_qua` (bỏ MỚI) CHỈ khi: sự kiện
  `pull_request`; `che_do` đang chạy = `day_du`; diff đo được, khác rỗng, đường dẫn sạch; đóng góp merge ĐÃ KIỂM có ít
  nhất một đường dẫn NGOÀI allowlist hồ sơ; và KHÔNG mục nào của diff (kể cả thêm, xoá, đổi tên, đổi mode,
  symlink) rơi vào **bao đóng bảo thủ**: toàn bộ `ops/` trừ bốn tiền tố hồ sơ, toàn bộ `.claude/dev/`, `scripts/*.py` (mức
  tên), `.github/`, tệp cấu hình gốc kho, cùng mọi đường dẫn mà vết inotify + rà tĩnh các lời gọi `git` trong ca chỉ ra.
  Push ⇒ `chay`. **Vô hiệu hoá:** bao đóng mang băm của `ops/cong_cu_test.py`, `ops/cong_cu.py`, `ops/bash_nen.py` lúc
  đo; băm lệch với cây đang chạy ⇒ `chay` cho MỌI lượt tới khi đo lại. `gate-cong-cu-gop` vẫn bắt buộc, in "KHÔNG ĐO" với
  dấu riêng cho lý do này.
- **Điều kiện bật (trong chính PR, trước commit bật).** (1) ≥ 14 ngày dữ liệu bóng của PR1; (2) không lượt nào có bóng
  `bo_qua` mà G5 đỏ vì lý do không phải hạ tầng; lượt không phân loại được tính là CHƯA đạt; (3) ca đối kháng: thêm tệp mới
  vào `ops/`, đổi tên/xoá tệp trong bao đóng, đổi mode, symlink, đổi tệp chỉ đọc qua object git, đường dẫn có ký tự lạ;
  cộng ba ca phân biệt: diff CHỈ hồ sơ ⇒ `duong_nhanh`, nhãn bỏ sẵn có, KHÔNG phải bỏ mới; diff ngoài bao đóng và ngoài
  allowlist ⇒ bỏ mới, push sau merge `day_du` có G5; gốc cũ (master thêm tệp trong bao đóng sau `base.sha`) ⇒ `chay`;
  (4) mệnh đề I5 đo được, áp trên ỨNG VIÊN CUỐI ĐÃ MERGE: ánh xạ PR → head cuối được merge → merge commit → lượt push;
  mọi PR có head cuối mang bóng `bo_qua` MỚI phải có lượt push ấy ở `day_du` với 8 mảnh G5 `success`. Quan sát bóng của
  head đã bị thay thế và của PR còn mở báo riêng (`bi_thay_the`, `cho`), không tính đạt cũng không tính trượt;
  (5) chủ kho quyết phần giảm bảo đảm trước merge còn lại (Q1) TRƯỚC khi bật, không dời tới PR8.
- **Write set dự kiến.** `ops/ci_duong_nhanh.py` + test, `.github/workflows/ci.yml`, `ops/cong_cu_test.py` (nhánh gom),
  `.claude/dev/ci_dang_ky_test.py` (`loi_g5_workflow`), biên bản đo bao đóng.
- **Tiết kiệm kỳ vọng.** Tỷ lệ bỏ `f`: 10–35 %, trung tâm 23 % (ƯỚC LƯỢNG `[DX-3]`, `[DX-8]`: trong 793 log, 381 không
  chạm tập đoán hẹp nhưng 201 trong số đó đổi tệp mà phép quét `t16` đọc ⇒ còn 180 = 22,7 %; 135 không xác định). Ở khối
  lượng cohort, với giả định bằng chi phí: `f × 5,71` = 0,6–2,0 triệu s, trung tâm 1,3 `[DX-2]`. `f` tính trên 793 lượt
  ĐÃ là `day_du`, không gồm lượt `duong_nhanh`. Số thật thay bằng dữ liệu bóng trước khi bật.
- **Rủi ro.** Trung bình–cao; lỗi bao đóng lộ ở lượt push `day_du` sau merge (master đỏ). **Hoàn tác:** công tắc một dòng
  cho bộ phân loại luôn trả `chay`, hoặc revert.
- **Phụ thuộc:** PR1+PR2. **Windows:** một lượt dispatch. **Full M9:** có. **Human audit:** có.

### PR4 — Bộ phân loại dùng MỘT ngữ cảnh so sánh đã kiểm (cha thứ nhất của merge ref)

- **Vấn đề.** Mục 2.8. Sửa riêng số hạng thứ ba của `doc_diff` là KHÔNG đủ: `doc_raw_ba_cap` (:305-325) và `kiem_mode_git`
  (:618-635) vẫn dùng cặp `(goc, hop)` cũ và từ chối khi hợp đường dẫn lệch `doi`; `main` (:813-821) chỉ xuất
  `goc/dau/hop`. Phân loại ra `duong_nhanh` thì `kiem-re` vẫn trả "không đo được" trong đúng ca cần sửa.
- **Thiết kế.** Một cấu trúc ngữ cảnh duy nhất, dựng một lần và kiểm: `goc_su_kien` (giữ nguyên, để truy vết), `goc_so`
  (cha thứ nhất của `github.sha`), `dau`, `hop`. `goc_so` chỉ được dùng khi `github.sha` có đúng hai cha, cha hai =
  `head.sha`, và `goc_su_kien` là tổ tiên của cha một; sai một điều kiện hoặc git lỗi ⇒ ngữ cảnh cũ hoặc "không đo được".
  CÙNG ngữ cảnh ấy đi vào `doc_diff`, `doc_raw_ba_cap`, `kiem_mode_git`, `kiem_diff_check`/`kiem_nhi_phan`, và được xuất
  qua `GITHUB_OUTPUT` để `kiem-re` đọc lại đúng nó. Chốt criss-cross và đổi tên phía base giữ nguyên, đổi gốc.
- **Write set dự kiến.** `ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py`, `.github/workflows/ci.yml` (output mới),
  `.claude/dev/ci_dang_ky_test.py` nếu băm job đổi.
- **Nghiệm thu.** Năm phép của mục 4. Ca đầu-cuối dương đi qua CẢ bộ phân loại lẫn `kiem-re`: master chỉ thêm tệp mã không
  liên quan sau `base.sha` ⇒ PR hồ sơ ra `duong_nhanh` và `kiem-re` rc=0; ở ca này bộ đếm LỢI ÍCH = có (luật cũ ≠ ngữ
  cảnh mới), bộ đếm SAI SÓT TỒN DƯ = không. Ca biên: master đổi tên hồ sơ ra vùng mã ⇒ `day_du`; criss-cross; đổi mode;
  cha thứ nhất dị dạng (một cha, ba cha, cha hai ≠ head) và git lỗi ở từng lệnh ⇒ vẫn fail-closed về `day_du`. Sau merge:
  **SAI SÓT TỒN DƯ = 0** (không lượt nào có phân loại đang chạy khác oracle ngữ cảnh mới đã kiểm, tính lại độc lập từ
  bốn OID đã ghi); bộ đếm LỢI ÍCH được BÁO CÁO, không đòi về 0.
- **Tiêu chí huỷ.** Dùng bộ đếm LỢI ÍCH của PR1 (KHÔNG dùng "hai gốc khác nhau"). Quần thể: lượt `pull_request`, attempt
  cuối, có đủ bốn OID và cả hai kết quả phân loại, trong ≥ 14 ngày bóng. Dưới 2 % số lượt ấy có luật cũ ≠ ngữ cảnh mới ⇒
  đóng "đã đo, không đổi mã".
- **Tiết kiệm kỳ vọng.** KHÔNG ƯỚC LƯỢNG ĐƯỢC từ BASELINE. Mỗi lượt trả về đúng làn cắt ≈ 13 716 − 2 380 ≈ 11 300 s
  `[B: …"pull_request | day_du"]`, `[B: …"pull_request | duong_nhanh"]` (1 080 444 / 454).
- **Rủi ro.** Cao. **Hoàn tác:** revert. **Phụ thuộc:** PR1+PR2. **Windows:** không. **Full M9:** có. **Human audit:** có.

### PR5 — Thêm G5 bán kính ĐỦ vào full audit, kèm hợp đồng phủ và biên nhận riêng

- **Vấn đề.** G5 bán kính không nằm trong `ci-dot-bien-du.yml`. Muốn PR6 giảm G5 trên từng lần đẩy thì M9 phải mang nó
  trước, và phải CHỨNG MINH được là đã mang: K7 (`packet_loop.py`:3637-3641) chỉ đòi mọi job trả về đều `success`, không
  có kiểm kê job kỳ vọng; chốt hình dạng (`ci_dang_ky_test.py`:1193-1205) ghim đúng ba job cũ; bộ chọn biên nhận
  (:1088-1131) nhận JSON của `nhanh_don_duoc`, còn G5 ghi văn bản `MANH`/`BKCON` với lược đồ khác (:8137-8140, :8167-8207).
- **Thiết kế.** Thuần cộng thêm vào M9. (1) Nhóm 8 mảnh G5 + gom G5, checkout ghim SHA sự kiện và đo lại HEAD như PR0.
  (2) Đường chọn/kiểm biên nhận RIÊNG cho G5: mỗi mảnh mang head, băm tệp test, chế độ = `du`, run_id + attempt; gom chọn
  đúng một bên sản xuất hợp lệ mỗi mảnh, rồi dựng lại phân hoạch từ `DOT_BIEN` của chính nó. (3) **Kiểm kê kỳ vọng độc
  lập**: job thu cuối cùng đòi đủ TÊN các job gốc (`dot-bien-du`, 8 `dot-bien-manh`, `dot-bien-gop`) + 8 mảnh G5 + gom G5,
  mỗi job `success`, và đòi tập định danh đột biến/ca đã đo = tập trong mã tại SHA ấy; thiếu, thừa, trùng ⇒ đỏ. Job thu là
  một job của workflow nên K7 hiện có ("mọi job success") đã bắt nó, không phải sửa K7. (4) Mở rộng chốt hình dạng workflow
  một cách tường minh.
- **Write set dự kiến.** `.github/workflows/ci-dot-bien-du.yml`, `.claude/dev/ci_dang_ky_test.py`, `ops/cong_cu_test.py`
  (trường chế độ trong bản ghi mảnh, nếu chưa có).
- **Nghiệm thu.** Năm phép của mục 4, cộng các ca ÂM, mỗi ca phải làm job thu ĐỎ: thiếu hoặc tắt một nhóm job; thiếu/trùng
  mục; bản ghi sai chế độ (đích đội lốt đủ); nền đỏ hoặc không rõ; giết bằng tín dụng giả; sai SHA; biên nhận cũ hoặc trộn
  attempt. Dương: một lượt audit `success` trên head của PR với đủ kiểm kê; tập 321 khoá cũ ⊆ tập khoá mới (G6).
- **Tiết kiệm kỳ vọng.** ÂM: ≈ 8 × 1057 ≈ 8 500 s mỗi lượt audit; 54 lượt/30 ngày `[DX-5]` ⇒ +0,46 triệu s. Nếu chủ kho từ
  chối PR6 (Q2) thì PR5 KHÔNG mở.
- **Rủi ro.** Trung bình (đụng workflow M9, theo hướng siết). **Hoàn tác:** revert về hình dạng PR0.
- **Phụ thuộc:** PR0+PR1+PR2. **Windows:** không. **Full M9:** có, chính lượt ấy là bằng chứng. **Human audit:** có.

### PR6 — G5 chế độ đích trên từng lần đẩy PR; bán kính đủ ở audit K7 và ở push `day_du`

- **Vấn đề.** Sau PR3, PR chạm bao đóng (ước 65–90 % lượt PR `day_du`) vẫn chạy mọi ca dưới mọi đột biến ở mỗi lần đẩy.
- **Thiết kế.** Theo khuôn WP748 r16 của `nhanh_don_duoc`: trên `pull_request`, mỗi đột biến G5 chỉ chạy ca đích và phải
  bị giết bằng chốt của ca ấy; bản ghi mảnh mang chế độ = `dich`; bộ nhận của job gom PR chỉ nhận đúng chế độ kế hoạch đã
  khai, và dòng báo ghi "bán kính KHÔNG ĐO ở lượt này". Bán kính đủ đo ở nhóm job của PR5 trên đúng head trước merge và ở
  lượt push `day_du` sau merge. Chế độ đích CHỈ khi diff nằm trọn trong vùng K7 buộc audit; ngoài vùng ấy ⇒ chạy đủ.
- **Điều kiện mở packet.** PR5 đã land với đủ ca âm và một lượt audit đủ trên đúng head; số của PR1 (ca đích so với ca
  khác) cho thấy cắt được ≥ 60 % giây JOB của bước. **Điều kiện bật trong PR:** benchmark CÙNG HEAD đủ-so-với-đích, dựng
  trong một lệnh, giữ nguyên nền và phép phán giết; báo riêng giây job tiết kiệm và độ trễ đầu-cuối.
- **Write set dự kiến.** `ops/cong_cu_test.py`, `ops/ci_duong_nhanh.py` + test, `.github/workflows/ci.yml`,
  `.claude/dev/ci_dang_ky_test.py`.
- **Nghiệm thu.** Năm phép của mục 4; đột biến "chế độ đích in dòng bán kính như chế độ đủ", "diff ngoài vùng K7 vẫn được
  chế độ đích", "gom nhận bản ghi đích khi kế hoạch là đủ"; trên cùng SHA: tập đột biến bị giết ở chế độ đích = tập bị giết
  đúng đích ở chế độ đủ, VÀ chế độ đủ có phép đo hoàn tất cho mọi định danh; phản chứng: đột biến bán kính 2 qua chế độ
  đích nhưng làm đỏ job thu của PR5; mọi lượt của mẫu số G4 rơi vào đúng một loại.
- **Tiết kiệm kỳ vọng.** Xem bảng chung cuối mục. **Rủi ro.** Cao: giữa hai lượt audit, bán kính trên head PR không
  được đo. **Hoàn tác:** công tắc đưa PR về chế độ đủ, hoặc revert.
- **Phụ thuộc:** PR3+PR4+PR5 (thêm PR3 so mặc định). **Windows:** một lượt dispatch. **Full M9:** có. **Human audit:** có.

### PR7 — Phần tồn dư độc lập

- **(a) Job rỗng ở `duong_nhanh`.** `gate-nhanh-manh` mở 8 job để in dòng bỏ qua: 4340 dòng job, 205 677 s
  `[B: M2.theo_job.bang."gate-nhanh-manh | ubuntu-latest | duong_nhanh"]` (một phần là trước wp1113). Ma trận lấy từ output
  của `chuan-bi`: `duong_nhanh` ⇒ một phần tử, job gom vẫn in "KHÔNG ĐO". Huỷ nếu số đo sau wp1113 dưới 0,05 triệu s/30 ngày.
- **(b) Cân mảnh G5 theo chi phí đo được** (từ PR1), chỉ khi p90/trung vị của bước (1795/1057) do lệch tải chứ không do
  nhiễu runner; nghiệm thu A/B trên toàn bộ định danh đột biến. Cắt độ trễ (G3), không cắt giây máy.
- **(c) Workflow đột biến hằng đêm: mặc định GIỮ NGUYÊN.** Chỉ được dùng lại kết quả khi có đủ: bao đóng đo riêng cho
  MỌI đột biến hằng đêm và `CA_DAI` (workflow, giàn chạy, đường dẫn và mode, đầu vào không phải tệp như lịch sử git); nhân
  chứng là một lượt ĐÃ CHẠY THẬT, đủ 16 mảnh có dấu hiệu dương từng mảnh/ca (lượt bỏ qua KHÔNG làm mới nhân chứng); nơi lưu
  và quyền đọc biên nhận; hạn dùng; lượt ép chạy hằng tuần; không đọc được ⇒ chạy. Không khoanh được các đầu vào ấy thì
  phần này đóng "đã đo, không đổi mã". KHÔNG áp cho `ci-dot-bien-du.yml`.
- **(d) `gate-ops`** (1 238 470 s `[B: top5_giay_thuc_thi[3]]`): chỉ hành động nếu số theo bước của PR1 chỉ ra một bước
  trên 50 % và có vùng diff gọn; nếu có thì mở đặc tả riêng.
- **Write set dự kiến.** `.github/workflows/ci.yml`, `.claude/dev/ci_dang_ky_test.py`, `ops/cong_cu_test.py` (b); (c) nếu
  mở: `.github/workflows/packet-loop-dot-bien.yml`, `.claude/dev/packet_loop_test_manh.py`.
- **Nghiệm thu.** Năm phép của mục 4 cho từng phần; ba commit tách để hoàn tác riêng.
- **Tiết kiệm kỳ vọng.** (a) 0,05–0,15 triệu s (ƯỚC LƯỢNG); (b) 0 giây máy; (c), (d) CHƯA BIẾT. **Rủi ro.** Trung bình.
- **Phụ thuộc:** PR3 + PR6 (đã land hoặc đã bị từ chối bằng văn bản). **Windows:** một lượt dispatch cho (a).
  **Full M9:** có. **Human audit:** khuyến nghị.

### PR8 — Đo lại 30 ngày, sửa lời khai lệch, phân loại kết cục, đóng mission

- **Phạm vi.** Chạy bộ thu mở rộng trên cohort 30 ngày mới; bảng nền/sau cho G1–G6 trên quần thể đóng băng, kèm khoảng
  bootstrap theo cụm PR; sửa 10 lời khai `lech` và rà 22 `khong_do_duoc` `[B: M4.theo_ket_luan]` theo số đo mới, mỗi số
  ghi điều kiện đo; danh sách rủi ro tồn dư. Không đổi hành vi cổng.
- **Ba kết cục, ghi riêng cho TỪNG chỉ số:** `dat` (đạt mục tiêu) · `do_khong_dat` (đo được, không đạt) ·
  `ngoai_le_chu_kho_chap_nhan` (không đạt, chủ kho chấp nhận bằng văn bản, nêu lý do). Hoàn tất PHÉP ĐO không phải là đạt
  kết quả: mission chỉ được khai "thành công" khi mọi chỉ số là `dat` hoặc `ngoai_le_chu_kho_chap_nhan`; còn
  `do_khong_dat` chưa có quyết định thì mission đóng ở trạng thái "đã đo, chưa đạt".
- **Nhánh PR6 bị từ chối.** PR5 không mở; PR7 chạy với điều kiện (ii) của đồ thị; mục tiêu dùng cột "PR6 bị từ chối" của
  bảng mục 3; PR8 ghi rõ PR5/PR6 là `khong_thuc_hien_theo_quyet_dinh`, không ghi như đã hoàn thành.
- **Write set dự kiến.** Thư mục đặc tả/đo mới dưới `ops/specs/`, chú thích trong hai workflow, `docs/**` liên quan.
- **Tiết kiệm kỳ vọng.** 0. **Rủi ro.** Thấp. **Hoàn tác:** revert.
- **Phụ thuộc:** PR7 + quyết định của chủ kho. **Windows:** không. **Full M9:** có nếu diff chạm `.github/workflows/**`.
  **Human audit:** có (điểm audit thật của chủ kho cho cả mission).

### Tiết kiệm G5 tính CHUNG (MINH HOẠ, không phải dự báo đã đo)

PR3 và PR6 cùng phụ thuộc phần G5 được bỏ, nên không cộng độc lập. Hai khoản khác bản chất, tính riêng:
- **Chi phí JOB tránh được (PR3):** `f_c · V`. `V` = 5,71 triệu s là giây JOB `gate-cong-cu` ở PR `day_du` `[DX-2]`, gồm cả
  checkout/cài đặt/tải artifact (`ci.yml`:594-635); job bị bỏ thì mất trọn. `f_c` là phần GIÂY JOB nằm trong các lượt được
  bỏ. Bảng dưới dùng **giả định bằng chi phí** `f_c = f` (lượt được bỏ tốn bằng lượt trung bình); giả định này chưa đo, và
  101/184 lượt mốc bị huỷ `[DX-4]` cho thấy chi phí mỗi lượt rất không đều.
- **Chi phí BƯỚC cắt được (PR6):** `(1 − f_b) · V_b · s_b`. `V_b` = 5,44 triệu s là giây riêng BƯỚC G5 `[DX-2]`; phần ngoài
  bước (`V − V_b` ≈ 0,26 triệu s, khoảng 46 s mỗi job) chế độ đích KHÔNG cắt. `f_b` là phần GIÂY BƯỚC nằm trong các lượt
  được bỏ, một đại lượng KHÁC `f_c` (tỷ trọng bước trong job không đều giữa các lượt); `(1 − f_b)·V_b` chính là giây bước
  còn lại đủ điều kiện, PR1 đo trực tiếp. `s_b` = phần giây bước mà chế độ đích cắt.
- **Trừ trọn chi phí audit thêm (chỉ khi có PR6):** `A` = 54 lượt `[DX-5]` × (8 × 1068 s trung vị JOB
  `[B: M2.theo_job.bang."gate-cong-cu | ubuntu-latest | day_du".trung_vi]` + 13 s trung vị job gom
  `[B: M2.theo_job.bang."gate-cong-cu-gop | ubuntu-latest | day_du".trung_vi]`, n=726) ≈ 0,46 triệu s.

**Tiết kiệm = f_c·V + (1 − f_b)·V_b·s_b − A** (triệu s / 30 ngày, khối lượng cohort). Bảng dưới dùng HAI giả định chưa đo:
bằng chi phí job (`f_c = f`) và `f_b = f_c`. Giả định mọi PR chạm bao đóng đều nằm trong vùng K7 là cận TRÊN cho khoản thứ hai.

| Kịch bản | không PR6 | PR6, `s_b` = 0,6 | PR6, `s_b` = 0,9 |
|---|---|---|---|
| `f` = 0,10, bằng chi phí | 0,57 | 3,05 | 4,52 |
| `f` = 0,23 (trung tâm), bằng chi phí | 1,31 | 3,37 | 4,62 |
| `f` = 0,35, bằng chi phí | 2,00 | 3,66 | 4,72 |
| `f` = 0,23 nhưng lượt được bỏ chỉ tốn NỬA lượt trung bình (`f_c` = `f_b` = 0,115) | 0,66 | 3,09 | 4,53 |

**Vì sao `f_b` phải tách khỏi `f_c` (phép kiểm tính toán).** Hai job cùng 100 s, bước G5 lần lượt 10 s và 90 s; bỏ job thứ
nhất: `f_c` = 100/200 = 0,5 nhưng `f_b` = 10/100 = 0,1. Với `s_b` = 0,6, phần bước còn lại cắt được là (1 − 0,1)·100·0,6
= 54 s; dùng nhầm `f_c` sẽ ra (1 − 0,5)·100·0,6 = 30 s. Bảng trên KHÔNG đo `f_b`; nó giả định `f_b = f_c`.

**Quy ước làm tròn:** ô trong bảng làm tròn gần nhất tới 0,01; ĐẦU MÚT của khoảng tổng làm tròn RA NGOÀI tới 0,1 (cận
dưới xuống, cận trên lên); phần trăm làm tròn gần nhất. Cộng PR2 (0,4–0,7) và PR7a (0,05–0,15): **không PR6 ≈ 1,0–2,9 triệu
s (7–19 % của 15,06 triệu), trung tâm 2,0** (cận trên tính ra 2,85, ghi 2,9 theo quy ước ra ngoài; cận dưới 1,02); kịch bản
chi phí không đều kéo điểm trung tâm xuống ≈ 1,3. **Có PR6 ≈ 3,5–5,6 triệu s (23–37 %)** (tính ra 3,50 và 5,57). Mọi ô là ước lượng, sẽ được
THAY bằng số đo có trọng số chi phí của PR1 (giây job theo lượt, ca đích so với ca khác); mục tiêu G1/G2 đặt thận trọng hơn
điểm trung tâm tương ứng. Phần G5 ở push (2,57 triệu s `[DX-2]`) không đổi.

## 6. Phương án đã loại

1. **Bỏ G5 ở push `day_du` khi cây trùng cây PR đã đo** (≈ 2,57 triệu s `[DX-2]`). Loại: tiền lệ wp1353 (hồ sơ land cần
   dấu hiệu dương trên chính merge commit) và đó là lớp bù duy nhất của PR3/PR6 cho diff ngoài vùng K7.
2. **Giảm hoặc lấy mẫu bảng đột biến.** Loại: phá I2/I6, không tất định; mỗi đột biến canh đúng một chốt. Không mở lại chỉ
   để đạt mục tiêu thời gian.
3. **Thay full audit M9 bằng lượt targeted, hoặc chỉ giữ lịch tuần.** Loại: trái `ADR-0060` M9/K7; 700 504 s `[DX-5]` là
   4,7 %, và 61/62 lượt là SHA khác nhau nên không có lượt lặp để gộp. Không mở lại chỉ để đạt mục tiêu thời gian.
4. **Thêm mảnh hoặc runner lớn hơn cho G5.** Loại: chỉ cắt thời gian tường. Chi phí cố định mỗi job ở 8 mảnh đã là checkout
   67 594 + rg 55 345 + shellcheck 23 456 + pip 19 732 ≈ 166 000 s `[B: M2.theo_buoc.bang."gate-cong-cu | ubuntu-latest |
   day_du | …"]`.
5. **`paths:` / `paths-ignore:` ở mức workflow.** Loại: check bắt buộc vắng mặt thì PR kẹt, và vắng mặt trông giống xanh.
6. **Xếp job nặng sau job rẻ để giảm phí lượt bị huỷ.** Loại: mảnh G5 bị huỷ đã chạy trung bình 538 s (953 603 / 1771
   `[DX-2]`), chờ thêm 2–3 phút cứu được ít mà mọi lượt thành công dài thêm.
7. **Cache kết quả bán kính theo băm cây, dùng lại giữa các PR.** Loại ở r3: thêm lớp "kết quả có thể chưa từng chạy".
8. **Chỉ chạy làn nặng khi PR hết draft.** Loại ở r3: BASELINE không có trạng thái draft theo lượt; đổi nghĩa "CI đúng head".
9. **Bật bỏ G5 theo vết inotify ngay ở packet đầu** (PR1 của bản trước). Loại: vết truy cập không bắt được thay đổi thành
   viên thư mục và đọc qua object git; `[DX-8]` cho thấy tập đoán hẹp khai thừa hơn một nửa.

## 7. Câu hỏi chủ kho cần quyết (5)

- **Q1 (quyết TRƯỚC khi bật PR3).** Chấp nhận rằng PR ngoài bao đóng bảo thủ không đo G5 trước merge, lớp bù là lượt push
  `day_du` sau merge? Khuyến nghị: CÓ, với năm điều kiện bật của PR3; nếu không thì PR3 đóng "đã đo, không đổi mã".
- **Q2.** Chấp nhận cặp PR5+PR6? Khuyến nghị: CÓ nếu số PR1 cho `s` ≥ 0,6 và PR5 qua đủ ca âm; nếu không, bỏ CẢ HAI (PR5
  một mình chỉ thêm chi phí) và dùng cột "PR6 bị từ chối".
- **Q3. Chính sách push cho bộ mới của PR2:** theo luật `NHE` đang có (push cũng nhẹ theo diff) hay ép đủ ở push? Khuyến
  nghị: theo luật đang có, vì diff chạm `ops/**/*.py` đã buộc audit K7 trên đúng head và lượt audit chạy registry đủ; ép
  đủ ở push tốn thêm 0,15–0,24 triệu s và tạo hai luật cho cùng một cơ chế.
- **Q4.** Tối ưu nội tại vòng lặp `full_mutant_audit` (giữ ma trận, làm nhanh giàn chạy) có thuộc mission? Khuyến nghị:
  KHÔNG trong r3 (4,7 %, chạm thẳng I1).
- **Q5.** Độ dài cohort và ngưỡng: khuyến nghị 14 ngày bóng trước PR3/PR4, kiểm 14 ngày sau PR3, 30 ngày ở PR8; chỉ số
  không đạt ghi `do_khong_dat`, không tự hạ mục tiêu.

## 8. Lỗ hổng phép đo ảnh hưởng tới kế hoạch

| Lỗ hổng `[B: khong_do_duoc.*]` hoặc ngoài phạm vi thu | Ảnh hưởng | Cách xử lý |
|---|---|---|
| Tỷ lệ PR độc lập với G5: không có trong BASELINE | `f` là ước lượng 10–35 % | Bóng của PR1 ≥ 14 ngày; PR3 không bật khi chưa có |
| Log `gate-cong-cu` không được thu ⇒ không có giây theo đột biến, theo ca đích | `s` chưa có chân | PR1 đo năm đại lượng; PR6 không mở trước đó |
| Bộ thu #1434 gom theo job/nền/làn, không có danh tính lượt | Không đo được G4, không tách đủ/đích | Bộ thu mở rộng trong write set của PR1 |
| `packet-loop-dot-bien.yml` ngoài cohort | Chi phí hằng đêm, tình trạng 1864 đột biến + `CA_DAI`: chưa biết | PR1 đưa vào bộ thu; PR7c mặc định giữ nguyên |
| `M2.theo_buoc` không có `gate`, `gate-ops` | 0,74 + 1,24 triệu s chưa phân rã `[B: M2.theo_job.bang."gate | ubuntu-latest | *"]`, `[B: top5_giay_thuc_thi[3]]` | PR1 đo; r3 không hứa cắt |
| 269 bản ghi `CI_DANG_KY_THOI_GIAN` của job bị huỷ không có | M2b lệch về job chạy xong | PR2 nghiệm thu bằng thời gian job/bước |
| 86 lượt không rõ làn `[B: M2.theo_lan]`; 35 log `chuan-bi` lỗi 404 | Mẫu số làn thiếu 5,5 % | 2 133 s `[B: …"pull_request | khong_do_duoc"]`, `[B: …"push | khong_do_duoc"]`; vào dòng "không rõ" |
| Dòng `thoi_gian_dao` (110 `gate-cong-cu-gop`, 52 `gate-registry`, 43 `gate-nhanh-gop`, 29 `gate-packet-loop`) | Job bị huỷ trước khi có runner | Loại theo quy tắc ba trạng thái; không thay bằng 0 |
| Không có `completed_at` của workflow | G3 là "đầu-cuối suy ra từ job" | Giữ `meta.quy_tac.dau_cuoi_suy_ra_tu_job` ở cả hai lần đo |
| 37 log mảnh cắt cụt + 16 thiếu (audit) | Chỉ ảnh hưởng `M1.muc_ket_qua_theo_khoa`; artifact đủ 390/390 `[B: do_phu.artifact_manh]` | G6 so tập khoá theo artifact |
| Tần suất phân loại cũ ≠ mới do lệch gốc | PR4 chưa có cỡ | Bộ đếm LỢI ÍCH của PR1; tiêu chí huỷ 2 % |
| Nền trộn trước/sau wp892, wp1343; mốc sau 17-11 nhỏ và nhiều lượt huỷ | Tổng cohort cao hơn hiện trạng; độ nhạy chỉ là heuristic | Quần thể đóng băng + bootstrap theo cụm PR ở PR8 |
| 22 lời khai M4 `khong_do_duoc`, 10 `lech` | Chú thích workflow nêu số cũ (vd. "~73 800 s nối tiếp" đo ra 13 010 s) | PR8 sửa, ghi điều kiện đo |

## 9. Phép dẫn xuất (không phải khoá BASELINE)

- **[DX-1]** Cộng `giay_thuc_thi.gia_tri` của `M2.luot[]` theo `ket_luan`: `cancelled` 3 633 319 / 15 057 171 = 24,1 %.
- **[DX-2]** Từ ảnh chụp thô `jobs/**/p*.json` (đệ quy, GỒM các trang lồng `c30` của hai lượt 40527993854 và
  40528783769), ghép `run_id` với `su_kien`/làn của `M2.luot[]`, áp ĐÚNG quy tắc của bộ thu (`meta.quy_tac.phan_loai_dong`:
  bỏ `skipped`, mỗi `job_id` đếm một lần, dòng mang sang không tính lại, loại thời lượng âm). Kết quả tái lập
  `top5_giay_thuc_thi[0]`: 7832 dòng, 8 542 030 s. Tách: PR `day_du` 5694 dòng, 5 706 598 s (riêng bước G5 5 443 208 s);
  push `day_du` 1923 dòng, 2 568 875 s (bước 2 510 857 s); PR `duong_nhanh` 205 dòng, 266 557 s; PR KHÔNG RÕ LÀN 10 dòng,
  0 s (thời lượng 0 là số ĐO ĐƯỢC, giữ nguyên; không gán các dòng này vào `day_du`). Bốn nhóm cộng: 5694 + 1923 + 205 +
  10 = 7832 dòng. Hai phép khoá: tổng dòng và tổng giây phải bằng khoá BASELINE; hai lượt có trang lồng phải có mặt và mỗi `job_id` xuất hiện đúng một lần. Số
  TRANG THÔ, không khử trùng, chỉ để tham khảo: 8102 dòng, 9 019 102 s (đội 5,585 % so với BASELINE); PR `day_du` thô 5914
  dòng, 6 113 166 s, gồm `cancelled` 1771 dòng / 953 603 s và `failure` 69 dòng. (Số 5810/5 896 141/62/7998 của bản `7fe0545b` đã rút.)
- **[DX-3]** Từ 1491 log `chuan-bi`, dòng `DUONG_NHANH:` cuối: 793 lượt "DAY_DU vì diff có N tệp ngoài allowlist" (in tối
  đa 5 tên; 261 lượt bị cắt). So với tập ĐOÁN hẹp (`ops/bash_nen.py`, `ops/cong_cu*`, `ops/cai_cong_cu.sh`,
  `ops/cai_actionlint.sh`, `.github/workflows/`, `ops/lease_publish_test.py`, `.claude/dev/launcher.py`): 277 chạm · 381
  không chạm · 135 không xác định. Output `packet_loop` ở lượt `day_du`: `chay` 171 · `bo_qua` 59.
- **[DX-4]** Lọc `M2.luot[]`: `created_at ≥ 2026-11-17`, `pull_request`, `day_du`. Giây thực thi mọi kết luận: n=184 (101
  lượt bị huỷ), trung bình 10 659, lệch chuẩn MẪU 4603. Đầu-cuối của lượt `success` một attempt: n=71, trung vị 1775, p25
  theo hạng gần nhất 1590, bootstrap phần trăm vị 4000 lần lặp cho 1688–1865 (reviewer tái lập với seed 0).
- **[DX-5]** Lọc `M1.luot[]` với `created_at ≥ meta.T0`: 54 lượt, tổng `giay_thuc_thi` 700 504 s.
- **[DX-6]** Gom `M2.luot[]` theo tuần từ 2026-10-21: 4,44 · 4,73 · 2,33 · 1,31 · 2,25 triệu s (tuần cuối thiếu ngày).
- **[DX-7]** 2,8 × lệch chuẩn × √(1/n₁ + 1/n₂), lệch chuẩn 4603, n₁=184: n₂=700 ⇒ 1 068 s; n₂=184 ⇒ 1 344 s. HEURISTIC:
  giả định các lượt độc lập, điều này không đúng.
- **[DX-8]** Phép nhạy bao đóng của reviewer (`revplan1/review_numbers.py`, `closure_sensitivity`): trong 381 log "không
  chạm" của DX-3, 201 đổi tệp mà phép quét `t16` (`_goi_ngoai`) đọc ⇒ còn 180/793 = 22,7 %. Là phép nhạy, không phải tỷ
  lệ bỏ đã đo; bao đóng của PR3 còn rộng hơn phép quét ấy.

## 10. Thay đổi so với bản c9090f77 (vòng 1), 7fe0545b (vòng 2), 43137d53 (vòng 3b)

| Finding | Mức | Chỗ xử lý | Cách đóng |
|---|---|---|---|
| R3-01 | P2 | PR1 (bóng), PR3 (thiết kế + năm điều kiện bật), DX-8, bảng tiết kiệm, Q1, phương án loại 9 | Bỏ hợp đồng "vết inotify"; bao đóng bảo thủ tính cả thành viên thư mục, thêm/xoá/đổi tên/mode, đọc qua git; vô hiệu hoá theo băm; bóng ≥ 14 ngày và ca đối kháng TRƯỚC khi bật; `f` hạ từ 48 % xuống 23 % (10–35 %); quyết định giảm bảo đảm dời lên Q1, trước khi bật |
| R3-02 | P2 | PR4 | Một ngữ cảnh so sánh đã kiểm dùng chung cho phân loại, raw/mode, `kiem-re` và output; ca đầu-cuối dương + ca biên; tiêu chí huỷ 2 % tính trên số lượt LẬT phân loại (cờ cũ ≠ mới của PR1) |
| R3-03 | P2 | Mục 2.9, I5, PR2 (chính sách push), PR3 điều kiện (4), Q3 | I5 phát biểu đúng phạm vi và liệt kê ba ngoại lệ đang có; bỏ câu "mọi push chạy đủ"; lớp bù của PR3/PR6 thu về mệnh đề đo được; chi phí phương án ép đủ ở push nêu ở PR2/Q3 |
| R3-04 | P2 | PR5, PR6, I1, I6, G6 | Đường biên nhận riêng cho G5; kiểm kê kỳ vọng độc lập (job gốc + 8 mảnh G5 + gom + job thu); bảo toàn theo danh tính; bảy ca âm; PR6 chỉ mở sau một lượt audit đủ trên đúng head |
| R3-05 | P2 | PR1 mục 1, PR6 điều kiện mở/bật, năm phép (d) | Tách thời gian tường, khoảng/CPU của con, dựng cây, ca đích, ca khác; đối chiếu bằng hợp khoảng; so toàn bộ định danh hiện hành thay cho số 490; benchmark cùng head đủ-so-với-đích trước khi bật |
| R3-06 | P2 | Mục 3 (quần thể đóng băng, G4 bốn tỷ lệ, cách đo lại), PR1 mục 4, mục 8 | Bộ thu mở rộng có danh tính lượt/attempt/sự kiện/head và chế độ, nằm trong write set của PR1, có trước mọi kỳ nghiệm thu 14 ngày; G1–G3 tính trên lượt mà luật CŨ xếp `day_du`, tách theo kết luận |
| R3-07 | P2 | PR7c | Mặc định giữ nguyên lượt hằng đêm; chỉ dùng lại khi có bao đóng riêng (gồm `CA_DAI`), nhân chứng chạy thật, lưu trữ, hạn dùng, ép tuần, fail-closed; thiếu thì đóng không đổi mã |
| R3-08 | P3 | PR8, đồ thị (ii), bảng mục 3 | Ba kết cục riêng cho từng chỉ số; mission "thành công" đòi quyết định bằng văn bản cho chỉ số không đạt; nhánh PR6 bị từ chối chạy được, có mục tiêu riêng |
| R3-09 | P3 | Thứ tự mục 5, bảng tiết kiệm chung, cột "Độ nhạy", phương án loại 2–3 | Thứ tự: quan sát → PR2 → PR3 có kiểm chứng → PR5 trước PR6 → phần độc lập của PR7 → PR8; tiết kiệm là hàm của `f` và `s` trừ chi phí audit; độ nhạy gắn nhãn heuristic, nghiệm thu theo cụm PR; giữ nguyên việc loại lấy mẫu và thay M9 |

| R3-02 (vòng 2) | P2 | Mục 3 dòng G5, PR1 mục 3, PR4 nghiệm thu + tiêu chí huỷ | Tách hai bộ đếm: LỢI ÍCH (luật cũ ≠ ngữ cảnh mới, kỳ vọng > 0) và SAI SÓT TỒN DƯ (phân loại đang chạy ≠ oracle ngữ cảnh mới, đòi = 0); ca gốc-cũ dương: lợi ích = có, tồn dư = không; cha dị dạng vẫn fail-closed; quần thể luật cũ của G1–G3 giữ nguyên |
| R3-03 (vòng 2) | P2 | I5, PR3 thiết kế + điều kiện bật (3)(4) | Bỏ mới chỉ khi `che_do` đang là `day_du` VÀ có đóng góp merge ngoài allowlist đã kiểm; bỏ sẵn có của `duong_nhanh` mang nhãn riêng, không vào `f`; nhân chứng sau merge áp trên ứng viên cuối đã merge, quan sát chờ/bị thay thế báo riêng; thêm ba ca phân biệt |
| R3-06 (vòng 2) | P2 | Mục 3 dòng G4 + bảng phân loại G4, PR1 nghiệm thu | Mẫu số tường minh; tách tỷ lệ CHỌN chế độ khỏi tỷ lệ PHỦ hoàn tất; năm loại kết cục; "100 %" chỉ là phát biểu chính sách, phủ hoàn tất lịch sử để "chưa đo"; ngưỡng 2 % áp cho `thieu_bang_chung` trên mẫu số; fixture chặn lượt đủ dang dở thành hoàn tất |
| R3-10 (vòng 2) | P2 | DX-2, mục 2.3, PR3 tiết kiệm, bảng tiết kiệm, phương án loại 1 | DX-2 tính lại theo quy tắc khử trùng/mang sang của bộ thu, tái lập đúng BASELINE (7832 dòng, 8 542 030 s): PR `day_du` 5 706 598 s, push 2 568 875 s; `V` 5,90 → 5,71; số trang thô nêu riêng với mức đội 5,585 %; có hai phép khoá |
| R3-09 (vòng 2) | P3 | "Tiết kiệm G5 tính CHUNG" | Tách chi phí JOB tránh được (`f_c`·`V`) khỏi chi phí BƯỚC cắt được ((1−`f_c`)·`V_b`·`s_b`), trừ trọn chi phí audit; nêu giả định bằng chi phí; thêm kịch bản chi phí không đều; gắn nhãn minh hoạ, thay bằng số PR1 |

| R3-06 (vòng 3b) | P2 | Mục 3 dòng G4 + "Phép quy G4b", PR1 nghiệm thu | Giữ mẫu số đóng băng; G4a thêm loại "đường nhanh đang chạy" tách khỏi "bỏ mới PR3"; G4b là phép quy CÓ THỨ TỰ, vét cạn, mười bước, mỗi lượt đúng một loại (gồm huỷ trước phân loại, đường nhanh có bằng chứng, gom hỏng/huỷ sau đủ biên nhận, thu bỏ-qua dang dở); nêu loại nào tính vào trần 2 %; thêm ba fixture |
| R3-09 (vòng 3b) | P3 | "Tiết kiệm G5 tính CHUNG" | Tách `f_b` (phần giây BƯỚC trong lượt được bỏ) khỏi `f_c`; bảng nêu rõ giả định `f_b = f_c`; thêm ví dụ hai job 100 s với bước 10 s và 90 s |
| R3-11 (vòng 3b) | P3 | DX-2, "Tiết kiệm G5 tính CHUNG" | Liệt kê nhóm thứ tư (10 dòng PR không rõ làn, 0 s) để bốn nhóm cộng đủ 7832; trích khoá BASELINE cho trung vị 13 s của job gom; nêu quy ước làm tròn (đầu mút khoảng làm tròn RA NGOÀI) |

Thay đổi đồ thị phụ thuộc so với mặc định: đúng hai điểm (i) và (ii) ở đầu mục 5; không thay đổi nào khác.
