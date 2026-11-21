# Đặc tả packet `CI-PROVENANCE-SONG-SONG` r1: chạy vòng đột biến của `ops/ci_provenance_test.py` song song

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
windows: required

| trường | giá trị |
|---|---|
| packet_id | `CI-PROVENANCE-SONG-SONG`, revision 1, generation 1 |
| trang_thai | **nháp, chờ chủ kho duyệt băm** (chạm E5, xem `pham_vi_e`) |
| packet_issue | **RỖNG** vì chưa mở Issue. Mở sau khi chủ kho duyệt băm đặc tả này |
| nguon_cap_viec | Chủ kho yêu cầu tối ưu các test CI dài (nhiệm vụ giao cho phiên đo ngày 15-11-2026). Căn cứ đo: `ops/specs/CI-TOI-UU-THOI-GIAN-BAO-CAO-20261115.md` §3.5 và §4, phương án P2 |
| review_class | `sensitive`: bộ test có vòng đột biến tự kiểm phân hạng (`TinHieuChotCa`, `TU_KIEM`) và chạy trong `test registry`, một vế của điều kiện land |
| base | `origin/master` lúc cấp lease. Lúc soạn: `426d1b06e292a7db272a0f942bef0794479b58a6` (đo 01:04Z 15-11) |
| depends_on | `[]`. Write set không giao với `CI-PACKET-LOOP-SONG-SONG` |
| executor · reviewer | chủ kho chọn khi cấp lease. Reviewer phải khác họ model với executor (`cross_approved`) |
| assurance mục tiêu | `cross_approved` trên exact head, cộng audit của chủ kho trước merge (E5) |

**Giới hạn lời khai.** Mọi khẳng định ở đây chỉ chứng minh tới đúng phép đo ghi kèm. Ba trạng thái: có · không ·
**KHÔNG ĐO ĐƯỢC**; trạng thái thứ ba làm cổng ĐỎ.

## 1. Phép đo nền

- Job `gate-registry`: trung vị 21,3 phút, p90 25,1 phút trên 32 lượt đầy đủ thành công 08→14-11.
- Log `gate-registry` của run `43579856328` (push `072d45a`), dòng `CI_DANG_KY_THOI_GIAN`: registry chạy hai bộ cùng
  lúc. `ops/ci_provenance_test.py` chạy từ giây 213,4 tới 1.520,1 (**1.306,7 s**); luồng kia xong mọi bộ còn lại ở giây
  559,1. Bộ dài thứ hai là `ops/cloud_agent_creds_test.py`, 331,0 s.
- `ci_provenance_test.py` in `CA: 63/63 dat` và `DOT BIEN: 398/398 bi giet dung ly do`. Ở chế độ mặc định nó gọi
  `chay_dot_bien` tuần tự cho 398 mục `DOT_BIEN`, mỗi mục một tiến trình con `--mot-ca` (cộng một lượt bản gốc cho mỗi
  ca đích, đã có bộ nhớ đệm `_NEN`): trung bình 3,3 s mỗi mục.
- Runner 4 vCPU (`nproc` = 4, 14-11). Hệ số tranh chấp khi 4 tiến trình cùng sinh tiến trình con trên runner này đo được
  1,5–1,9 (báo cáo §3.4, trên `packet_loop_test.py`; chưa đo riêng cho bộ này).
- Ước sau packet: `1.306,7 / 4 × (1,5–1,9) ≈ 490–620 s`, cộng 213 s chờ sau `doc_receipt_thu_hoi_test.py` ⇒ job
  registry khoảng 13–15 phút. Ước lượng, A6 đo thật.

## 2. Write set — 1 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `ops/ci_provenance_test.py` | M1–M4 |

Kích thước dự kiến: 1 tệp, 60–150 dòng thêm.

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| đổi thứ tự sổ `MOI` để `ci_provenance_test.py` chạy đầu tiên (bớt thêm ~3,5 phút) | sổ nằm ở `.claude/dev/ci_dang_ky_test.py`, ngoài write set; để cho packet chia job của báo cáo (P3) |
| nâng `CI_DANG_KY_WORKERS` từ 2 | giá trị bị ghim ở `ci.yml` và `ci_dang_ky_test.py`; job đang dài vì MỘT bộ, không vì thiếu luồng registry |
| chế độ `--dot-bien-dong` | đã song song sẵn; không chạy ở CI PR |
| thêm, bớt hay sửa ca và đột biến | packet chỉ đổi cách thi hành |
| `ops/ci_provenance.py` | mã sản phẩm, không cần đổi |

## 4. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | Biến `CI_PROVENANCE_TIEN_TRINH`. Vắng biến: `N = min(4, os.cpu_count() or 1)` trên Linux, `N = 1` ở nền khác (giữ nguyên hành vi Windows, nơi #997 đã gặp ca quá hạn). Có biến: khớp ĐÚNG `^[1-8]$` thì `N` là số ấy; mọi giá trị khác ⇒ rc≠0 và thông báo, TRƯỚC khi chạy ca nào | W1 |
| M2 | Ở chế độ mặc định (không đối số), vòng `DOT_BIEN` chạy qua `concurrent.futures.ThreadPoolExecutor(N)` (việc thật nằm ở tiến trình con nên luồng là đủ). Kết quả gom lại theo **thứ tự của `DOT_BIEN`**, không theo thứ tự xong. Lượt bản gốc của mỗi ca đích được tính TRƯỚC khi vào pool (hoặc dưới khoá), để `_NEN` không bị hai luồng cùng ghi. `TU_KIEM` giữ nguyên tuần tự hay cùng pool, miễn thứ tự in như cũ | W1 |
| M3 | Đầu ra giữ nguyên dạng mà sổ `MOI` của `.claude/dev/ci_dang_ky_test.py` đòi: bốn dòng cuối `CA: …`, `DOT BIEN: …`, `TU KIEM PHAN HANG: …`, `TONG: …` liền nhau ở cuối. Nếu in thêm dòng `TIEN TRINH: N` thì in ở ĐẦU đầu ra, trước mọi dòng `[…]` | W1 |
| M4 | Tự kiểm: một ca chạy bộ máy song song của M2 với hàm đột biến giả trả kết quả theo thứ tự xong bị đảo, và đòi đầu ra đúng thứ tự `DOT_BIEN`; một ca cho miền biến M1. Mỗi chốt có một mục đột biến riêng (trong `DOT_BIEN` hay `TU_KIEM`, theo hợp đồng `TinHieuChotCa` hiện có) gỡ đúng chốt ấy làm ca đích ĐỎ | W1 |

## 5. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | **Tương đương.** Trên cùng một cây, `CI_PROVENANCE_TIEN_TRINH=1` và `=4` cho đầu ra bằng nhau từng byte, sau khi bỏ dòng `TIEN TRINH:` nếu có | `diff` khác rỗng. Đột biến "gom theo thứ tự xong" phải làm A1 đỏ khi chạy tay |
| A2 | Miền biến M1: `0`, `9`, `a`, rỗng, ` 4`, `04` ⇒ rc≠0, chưa chạy ca nào; vắng biến trên nền không phải Linux ⇒ `N = 1` | ca tự kiểm M4 + đột biến nới miền |
| A3 | Thứ tự: ca tự kiểm M4 với thứ tự xong bị đảo ⇒ đầu ra vẫn đúng thứ tự `DOT_BIEN` | đột biến "gom theo `as_completed`" ⇒ ca ĐỎ |
| A4 | Sổ `MOI` vẫn nhận: `python .claude/dev/ci_dang_ky_test.py --chay` ở chế độ đủ cho dòng `CI_DANG_KY ops/ci_provenance_test.py: ĐẠT` | thêm một dòng giữa `CA:` và `TONG:` ⇒ mẫu của sổ không khớp ⇒ ĐỎ |
| A5 | Delta = 0: `python -m ruff check --select F ops/ci_provenance_test.py` so với base; bộ ĐẠT ở `N` mặc định trên Linux và ở `N = 1` trên Windows theo `ADR-0060` M3 | đo hai vế trong cùng một lệnh |
| A6 | **Canary sau land, không phải cổng land.** Lượt đầy đủ đầu tiên sau land: dòng `CI_DANG_KY_THOI_GIAN` ghi `ops/ci_provenance_test.py` ≤ 660 s và job `gate-registry` ≤ 16 phút. Ai đo: phiên land. Đọc lại: log job `gate-registry` | `chưa đo được` tới khi đo thật; vượt ngưỡng thì ghi số, không tự nới |

Trước khi đóng băng: A1–A3 đo hành vi mới nên đúng màu "chưa làm" trên `426d1b0` (biến chưa tồn tại); A4, A5 canh bất
biến và xanh sẵn trên CI master.

## 6. `luat_dung`

- Điểm dừng của `docs/PROTOCOL_DA_PHIEN.md` §12; trần kích thước của `ADR-0053`; trần lời gọi Codex của `ADR-0055`;
  điều kiện merge của `ADR-0060`.
- **E2** khi chạm trần `ADR-0053` hay `ADR-0055`: mang theo mức đã dùng, còn thiếu bao nhiêu, để làm gì.
- **E3** khi song song làm một mục đột biến đổi hạng (ví dụ quá hạn 300 s của `chay_con` dưới tranh chấp) mà muốn giữ
  `N > 1` thì phải nới hạn: mang theo mục nào, số đo, hậu quả.

## 7. `pham_vi_e`

- E4: **không chạm**.
- E5: **khai chạm** vì không rõ: bộ này là một phần của `test registry`, vế mà điều kiện land đọc; lỗi ở bộ gom kết quả
  có thể làm nó xanh mà chưa phân hạng đủ đột biến. Theo `ADR-0067`, không rõ thì coi là thuộc.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục. Cùng hình dạng với chế độ `--dot-bien-dong` đã có trong chính tệp
(`ThreadPoolExecutor` + kết quả gom theo danh sách gốc).

## 9. `chua_do_duoc`

- Hệ số tranh chấp thật của bộ này ở `N = 4` khi chạy cùng luồng registry thứ hai (A6).
- Ca nào của `ci_provenance_test.py` gần hạn 300 s dưới tranh chấp: chưa đo.
- Danh tính executor và reviewer: chủ kho chọn khi cấp lease.
