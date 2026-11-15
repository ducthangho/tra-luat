# Đặc tả packet `CI-PACKET-LOOP-SONG-SONG` r1: chạy `packet_loop_test.py` theo làn song song trong job

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
windows: required

| trường | giá trị |
|---|---|
| packet_id | `CI-PACKET-LOOP-SONG-SONG`, revision 1, generation 1 |
| trang_thai | **nháp, chờ chủ kho duyệt băm** (chạm E5, xem `pham_vi_e`) |
| packet_issue | **RỖNG** vì chưa mở Issue. Mở sau khi chủ kho duyệt băm đặc tả này |
| nguon_cap_viec | Chủ kho yêu cầu tối ưu các test CI dài, nhất là `gate-packet-loop` (nhiệm vụ giao cho phiên đo ngày 15-11-2026). Căn cứ đo: `ops/specs/CI-TOI-UU-THOI-GIAN-BAO-CAO-20261115.md` §2–§4, phương án P1 |
| review_class | `sensitive`: đổi bộ máy thi hành của bộ test mà check bắt buộc `gate-packet-loop (ubuntu-latest)` chạy, kể cả vòng đột biến tự kiểm |
| base | `origin/master` lúc cấp lease. Lúc soạn: `426d1b06e292a7db272a0f942bef0794479b58a6` (đo 01:04Z 15-11) |
| depends_on | `[]` |
| executor · reviewer | chủ kho chọn khi cấp lease. Reviewer phải khác họ model với executor (`cross_approved`) |
| assurance mục tiêu | `cross_approved` trên exact head, cộng audit của chủ kho trước merge (E5) |

**Giới hạn lời khai.** Mọi khẳng định ở đây chỉ chứng minh tới đúng phép đo ghi kèm. Ba trạng thái: có · không ·
**KHÔNG ĐO ĐƯỢC**; trạng thái thứ ba làm cổng ĐỎ.

## 1. Phép đo nền

Từ báo cáo đi kèm (mọi số đo trên `ubuntu-latest`, master `072d45a`):

- Bước `packet-loop selftest`: trung vị 90,5 phút, p90 118,5 phút trên 32 lượt đầy đủ thành công 08→14-11. Nó là
  đường găng của mọi lượt PR; job kế tiếp (`gate-ops`) xong ở phút 23,2 trung vị.
- Runner có 4 vCPU (`nproc` = 4, 14-11); bước này dùng một tiến trình.
- Lượt bấm giờ trọn (run `43624717342`): pha nền 58,5 phút cho 1.493 ca, pha đột biến 61,4 phút cho 1.829 đột biến.
- Chia 4 theo chỉ số: 4 job riêng lần lượt 26,5 · 18,6 · 57,0 · 29,2 phút; 4 tiến trình chung một runner 40,5 · 35,4 ·
  71,4 · 43,9 phút. Không ca nào đỏ vì thứ tự hay vì chạy đồng thời; ba ca kiểm kê đỏ chỉ vì bộ bọc đo lọc `MUTANTS`
  tại chỗ.
- Mô phỏng chia theo chi phí, 4 làn: 22,6 phút việc mỗi làn (quy về trung vị CI). Nhân hệ số tranh chấp đo được 1,5–1,9
  ⇒ ước 34–43 phút. Đây là ước lượng; A8 đo thật.

## 2. Write set — 1 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `.claude/dev/packet_loop_test.py` | M1–M6 |

Trước khi cấp lease phải hỏi `ai-dang-giu` cho W1: lúc soạn, PR #1318 (`agent/wp1315-r3-g3-codex`, mở) chạm
`.claude/dev/packet_loop_test.py` và `.claude/dev/packet_loop.py`.

Kích thước dự kiến: 1 tệp, 300–450 dòng thêm (ước theo #668, nơi bộ máy mảnh + gom + tự kiểm của `cong_cu_test.py` đặt
trần ~600 dòng cho 5 tệp). Vượt 450 dòng thêm là chạm trần của `ADR-0053`.

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| `.github/workflows/ci.yml` | packet này không cần đổi workflow: giá trị mặc định của M1 đã cho 4 làn trên runner Linux. Chia job là P3 của báo cáo, soạn sau khi có số canary A8 |
| tách `wp1303_target_human_chain` | với 4 làn, ca 24,5 phút vẫn ngắn hơn một làn (30 phút việc ở lượt bấm giờ); chỉ cần khi chia ≥ 6 làn (P4) |
| `.pyc` checked-hash cho lời gọi CLI | đổi đường gọi mà hàng nghìn ca dựa vào; P6 riêng |
| thêm, bớt hay sửa ca và đột biến | packet chỉ đổi cách thi hành |
| làn > 1 trên Windows | Windows giữ đường tuần tự; xem M1 |
| `SyntaxWarning` ở dòng 3786 | không liên quan thời gian |

## 4. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | Biến `PACKET_LOOP_TEST_LAN`. Vắng biến: `N = min(4, os.cpu_count() or 1)` khi `platform.system() == "Linux"`, `N = 1` ở nền khác. Có biến: khớp ĐÚNG `^[1-8]$` thì `N` là số ấy; mọi giá trị khác (kể cả rỗng, khoảng trắng, `04`) ⇒ rc≠0 và thông báo, TRƯỚC khi chạy ca nào. `N = 1` ⇒ đi đúng đường `_legacy_main` hiện có, thứ tự và nội dung dòng in như trước | W1 |
| M2 | **Phân việc.** Tập việc = ca nền và đột biến còn lại SAU các phép lọc nền mà `main()` đang làm. Chia `N` làn bằng xếp-việc-dài-trước vào làn có tổng nhỏ nhất, dùng bảng chi phí tĩnh `CHI_PHI_UOC` (giây, lấy từ lượt bấm giờ của báo cáo); việc vắng trong bảng nhận chi phí mặc định theo loại (0,31 s cho ca, 1,06 s cho đột biến); hoà thì xếp theo tên. Hàm phân việc thuần, tất định, KHÔNG sửa `CASES` hay `MUTANTS` toàn cục | W1 |
| M3 | **Làn con.** Cha chạy `N` tiến trình con `sys.executable packet_loop_test.py` ở chế độ làn (`--lan k/N --ra <tệp>`, tệp ra nằm NGOÀI cây kho), đồng thời. Con tự tính lại phân hoạch, chạy đúng phần của làn qua CÙNG mã thi hành ca và đột biến hiện có (thân vòng đột biến của `_legacy_main` tách thành hàm dùng chung cho cả hai đường), rồi ghi biên nhận dòng JSON: dòng đầu `{phien_ban, lan, so_lan, sha256_test, sha256_san_pham, bam_danh_sach_viec}`; mỗi ca nền một dòng `{ca, hang, thong_diep}` với `hang` thuộc tập đóng đủ để dựng lại đúng lớp của giá trị trong `ket` (đạt · `BoQua` có/không `OSError` · `_TinDungGia` · `CliSapDo` · `AssertionError` · chuỗi); mỗi đột biến một dòng `{ten, dong_in, so_loi, thieu_bat_buoc}`. Con không in dòng `TỔNG`. Mọi thứ ca tự in ra stdout/stderr ở con (ví dụ các dòng `{"test": "wp1178_r3", …}`, `R25_ADOPTION …`) được cha chép nguyên văn vào đầu ra của mình, theo từng làn, không nuốt | W1 |
| M4 | **Gom, fail-close.** Cha đọc đủ `N` biên nhận. ĐỎ (TỔNG ĐỎ, rc≠0, nêu lý do) khi: một làn thoát khác 0 · thiếu hay thừa biên nhận · một việc vắng, lặp, hay nằm sai làn so với phân hoạch cha tự tính · `sha256_test`, `sha256_san_pham`, `bam_danh_sach_viec` lệch với cha · dòng hỏng hay `hang` ngoài tập đóng. Hợp lệ thì dựng lại `ket`, chạy các phần 1–5 của `_legacy_main` với logic không đổi, in dòng đột biến theo thứ tự của `MUTANTS`; `_WP1174_OUTCOMES`, `_WP1174_LEGACY_FAILURE_COUNT` và `_carrier1174` dùng kết quả gom | W1 |
| M5 | **Dòng đo.** Khi `N > 1`, in `LAN: N` và mỗi làn một dòng `LAN k/N: <giây> s · <số ca> ca · <số đột biến> đột biến`, đặt TRƯỚC khối `SỐ LIỆU`. Dòng cuối giữ nguyên dạng `TỔNG: ĐẠT` hay `TỔNG: <n> lỗi` | W1 |
| M6 | **Tự kiểm.** Mỗi chốt của M1–M4 có ca tự kiểm chạy qua đường tiến trình con THẬT trên một bộ việc giả nhỏ (vài ca giả, vài đột biến giả), và có đột biến RIÊNG trong `MUTANTS` gỡ đúng chốt ấy làm ca đích của nó ĐỎ. Đối chứng khác họ theo luật hiện có | W1 |

## 5. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | **Tương đương.** Trên cùng một cây, chạy `PACKET_LOOP_TEST_LAN=1` rồi `=4`. (i) Dãy *dòng phán quyết* — các dòng bắt đầu bằng `nền:`, `  ok  `, `  ĐỎ  `, `  BỎ QUA  `, các dòng tiêu đề và kết luận của AC 18/AC 19, khối `SỐ LIỆU` và dòng `TỔNG` — bằng nhau từng byte và đúng thứ tự. (ii) Các dòng còn lại, sau khi bỏ dòng `LAN…` và thay mọi đường dẫn dưới thư mục tạm bằng `<TMP>`, bằng nhau theo đa tập | `diff` của (i) hay của đa tập (ii) khác rỗng. Đột biến M6 "làn bỏ việc cuối" phải làm A1 đỏ khi chạy tay |
| A2 | Gom ĐỎ đúng lý do với từng ca: làn rc≠0 · thiếu biên nhận · thừa biên nhận · việc lặp · việc vắng · việc sai làn · băm test lệch · băm sản phẩm lệch · dòng hỏng · `hang` lạ | ca tự kiểm M6; đột biến gỡ từng chốt ⇒ ca đích ĐỎ (mỗi chốt một đột biến, không gộp) |
| A3 | Miền biến M1: `0`, `9`, `a`, rỗng, ` 4`, `04`, `4 ` ⇒ rc≠0 và chưa chạy ca nào; vắng biến trên nền không phải Linux ⇒ `N = 1` | ca tự kiểm + đột biến nới miền |
| A4 | **Không sửa sổ toàn cục.** Ở `N = 4`, ba ca `kg_m5_kiem_ke`, `kg_t_ma_tran`, `dot_bien_test_khai_bao_chay_va_giet_dung_ca` XANH, và dòng AC 18 vẫn `0 ngoại lệ` (bốn thứ này đỏ dưới bộ bọc lọc tại chỗ, báo cáo §3.4) | đột biến "làn lọc `MUTANTS` tại chỗ" ⇒ ít nhất một trong ba ca ĐỎ |
| A5 | Phân hoạch tất định và phủ đúng: tính hai lần cho cùng kết quả; hợp các làn bằng tập việc; các làn rời nhau; mọi `N` từ 1 tới 8 | đột biến "hoà theo thứ tự ngẫu nhiên", "bỏ việc cuối" ⇒ ca ĐỎ |
| A6 | Người tiêu thụ đầu ra không đổi: dòng cuối khớp `^TỔNG: ĐẠT$` (mẫu `CUOI:^TỔNG: ĐẠT$` của các `danh_gia_gate.py` dưới `ops/land/**`); trên Linux vẫn in `WP1174_NATIVE_REPORT_V1`; các dòng bằng chứng do ca tự in (`{"test": …}`) còn đủ trong log; `_carrier1174` không báo cây đổi (biên nhận nằm ngoài cây) | chạy trọn trên Linux; thiếu dòng nào là ĐỎ |
| A7 | Delta = 0: `python -m ruff check --select F .claude/dev/packet_loop_test.py` so với base; bộ chạy trọn ĐẠT ở `N` mặc định trên Linux, và ở `N = 1` trên Windows theo `ADR-0060` M3 | đo hai vế trong cùng một lệnh |
| A8 | **Canary sau land, không phải cổng land.** Lượt đầy đủ đầu tiên sau land trên `ubuntu-latest`: bước `packet-loop selftest` ≤ 45 phút, log có `LAN: 4` và bốn dòng `LAN k/4`. Ai đo: phiên land. Đọc lại: REST `actions/runs/<id>/jobs` và log job | ở trạng thái `chưa đo được` tới khi đo thật; vượt 45 phút thì ghi số và mở việc cho P3/P4 của báo cáo |

Trước khi đóng băng đã chạy trên nền những gì đo được lúc ấy: A1–A5 đo hành vi mới nên đúng màu "chưa làm" (biến
`PACKET_LOOP_TEST_LAN` và chế độ `--lan` chưa tồn tại trên `426d1b0`); A6, A7 canh bất biến và xanh sẵn trên CI master.

## 6. `luat_dung`

- Điểm dừng của `docs/PROTOCOL_DA_PHIEN.md` §12; trần kích thước của `ADR-0053`; trần lời gọi Codex của `ADR-0055`;
  điều kiện merge của `ADR-0060`.
- **E2** khi chạm trần `ADR-0053` hay `ADR-0055`: mang theo số dòng hay số lời gọi đã dùng, còn thiếu bao nhiêu, để làm gì.
- **E1** khi A1 không đạt sau khi đã đổi thiết kế làn một lần mà cùng hình dạng chênh lệch còn đó: mang theo gốc rễ,
  hai thiết kế đã thử, một đề xuất.
- **E3** khi số đo cho thấy chạy song song làm một ca chập chờn mà muốn giữ `N > 1` thì phải nới chính ca ấy: mang theo
  ca nào, số lần đỏ trên số lần chạy, hậu quả của việc nới.

## 7. `pham_vi_e`

- E4: **không chạm**. Không đi ra ngoài kho, không đổi ruleset (context bắt buộc `gate-packet-loop (ubuntu-latest)` giữ
  nguyên tên và giữ nguyên lệnh chạy).
- E5: **khai chạm** vì không rõ. Packet đổi bộ máy thi hành và tổng hợp kết quả của bộ test sau một check bắt buộc;
  một lỗi ở gom có thể làm cổng xanh mà không chạy đủ ca. Theo `ADR-0067`, không rõ thì coi là thuộc. Hệ quả: chủ kho
  duyệt băm đặc tả và audit trước merge.

## 8. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục. Kế thừa hình dạng mảnh + gom của #661 (`CI-DOT-BIEN-CHIA-MANH`) và #668
(`CI-G5-CONG-CU-CHIA-MANH`): con chỉ gửi DỮ LIỆU ĐO, cha tự tính lại phân hoạch và tự kết luận; thiếu hay lệch ⇒ ĐỎ.

## 9. `chua_do_duoc`

- Thời lượng thật ở `N = 4` khi chia cân (A8). Hệ số tranh chấp 1,5–1,9 đo trên phân hoạch lệch.
- Ca chập chờn dưới tranh chấp CPU: mới có một lượt cho mỗi kiểu chia. Bảy chỗ `timeout=` cố định trong tệp test là
  chỗ cần nhìn trước.
- Đường làn trên Windows: packet giữ `N = 1` ở đó, nên chưa ai đo làn trên Windows.
- Danh tính executor và reviewer: chủ kho chọn khi cấp lease.
