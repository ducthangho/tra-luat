# Đặc tả packet `LAUNCHER-SANDBOX-LAY-MAU` r2 (errata của r1): tha "chuyển cha bình thường" trong luồng lấy mẫu sandbox

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
windows: required

| trường | giá trị |
|---|---|
| packet_id | `LAUNCHER-SANDBOX-LAY-MAU`, revision 2 (errata của r1: chỉ sửa A2 cột đột biến và A10 tập ca bỏ qua — mục `errata_r2` cuối tệp), generation 1 |
| packet_issue | #1105 |
| nguon_cap_viec | Issue #1105 (chủ kho mở 01-11-2026 03:10Z); chủ kho duyệt mở soạn đặc tả 01-11-2026 ~06:55Z, nguyên văn *"Mở soạn đặc tả #1105 đi"*, qua phiên điều phối `session_015GtxraXfMD1t2FJLzzGDr4`. Packet ĐẢO một phần quyết định THU HẸP của chủ kho ở WP748 r27 (26-10-2026), hồ sơ `ops/land/pr957-wp748-r27-provenance/verdicts/` |
| review_class | `sensitive` — phép đo assurance §8.1 (`sandbox_trang_thai`) và `.claude/dev/**` |
| base | `origin/master` lúc cấp lease (đo khi soạn: `c6dd7b3`). Điều kiện cấp lease: #1079 đã land hoặc lease `wp1079-r1-g1-claude` đã thu hồi (xem §3) |
| depends_on | #1079 (`LAUNCHER-TEST-ORACLE-VA-FIXTURE`) — chung `.claude/dev/launcher_test.py` |
| executor | `anthropic_claude` (Claude Code remote, Linux) + máy Windows của chủ kho qua Desktop Commander cho A10 |
| reviewer | `openai_codex` qua `launcher.py run` (offline, neo SHA ứng viên, `ADR-0060` M12) + connector `@codex review` trên PR draft |

Lời duyệt của chủ kho trong phiên soạn `session_015GtxraZvXy8g4RiLdGHMoE` (phiên con của điều phối
`session_015GtxraXfMD1t2FJLzzGDr4`), 01-11-2026 ~07:00–07:45Z:
vòng 1 Q1–Q10 *"Đồng ý khuyến nghị cả 10 câu"*; vòng 2 Q11–Q15 *"Đồng ý khuyến nghị cả 5 câu vòng 2"*; sửa trần
*"Sửa trần <=10, <=850"* (Q16: kích thước, ≤ 10 tệp / ≤ 850 dòng thêm); vòng 3 Q16–Q19 *"Đồng ý khuyến nghị cả 4
câu vòng 3"*; bốn điểm phiên soạn tự thêm khi viết — (1) tổ tiên vắng khi đọc lại chuỗi thì bỏ nhánh (§2.1),
(2) biểu hiện thứ 8 của lớp thì checkpoint (§7), (3) A6 đồng bộ tất định, (4) năm nhãn `sandbox_lech` (§2.3) —
*"Duyệt cả 4 điểm, đóng băng đi"*. Bản đồ câu ↔ quyết định ở §8.

## 1. Vì sao — số đo (01-11-2026, `origin/master` = `c6dd7b3`)

| # | sự kiện | số đo | đơn vị / thời điểm |
|---|---|---|---|
| S1 | `run.json` Codex thật trong kho | **8/9** `KHONG_DO_DUOC`, lý do `luong lay mau sandbox hong (DanhTinhDoi)`; 1/9 `DO_DUOC` (`a6634cfc`). Tệp: `ops/land/pr1100-wp1089-r2-provenance/verdicts/run-{c611c6b9,dfebe0ba}.json` và 7 tệp `ops/land/pr1073-wp1039-r1-provenance/verdicts/run-*.json` | đếm TỆP `run.json`; đo 06:59Z |
| S2 | sandbox thật vẫn chạy ở cả 8 lượt hỏng | mỗi tệp có `sandbox_quan_sat` chứa `codex-linux-sandbox` và `bwrap` với `--unshare-net` | đo 06:59Z |
| S3 | hồ sơ không nói lệch VÌ SAO | `ghi_so` chỉ ghi `loi[0]`; `run.json` không có nhánh, cạnh hay trạng thái cha | `rg -c sandbox_lech .claude/dev/launcher.py` = 0, đo 07:37Z |
| S4 | tái hiện không gọi model: `_LayMauSandbox` của master lấy mẫu `codex sandbox -- sh -c …` (codex-cli 0.166.0, container Linux này) | lệnh không bỏ lại tiến trình nền: **3/3** `DO_DUOC`; lệnh `sh -c "sleep 3 & sleep 0.6"; sleep 1.5` và biến thể lồng hai tầng: **6/6** `KHONG_DO_DUOC (DanhTinhDoi)` | đếm LƯỢT chạy; đo ~07:05Z |
| S5 | dạng của lệch ở S4 (bộ theo dõi `/proc` độc lập, chu kỳ 10 ms) | ở mọi lượt hỏng: `sleep` đổi ppid khi cha cũ ĐÃ VẮNG khỏi `/proc`; `starttime` giữ; cha mới là tổ tiên NẰM TRONG cây của gốc codex (init của pid namespace bwrap), không phải PID 1, không phải ngoài cây | đo ~07:08Z |
| S6 | lớp `sandbox-process-identity-race` ở r27 | 7 biểu hiện (R27-PID-04, 04b, 04c, 04d, 04e, 04f, 04g) qua 7 vòng r27a–r27g; r27 land ở 850 dòng thêm / 2 tệp | đếm BIỂU HIỆN finding; đọc hồ sơ r27 |

Kết luận đo được: quyết định THU HẸP r27 (*"một lượt bình thường **đôi khi** bị hạ"*) trên Codex thật là **8/9**,
và cơ chế khớp với S5 — vòng đời bình thường của tiến trình nền trong bwrap. Phần chưa đo được ở §6.

## 2. Thay đổi

### 2.1 Quy tắc tha (Q1, Q2, Q3)

Thiết kế giữ nguyên (`_LayMauSandbox`, hàng đợi chuỗi tổ tiên, `self.canh` xuyên lượt). Thêm **đúng một** quy
tắc tha. Một lần đổi ppid của tiến trình `c` (cha cũ `P`, cha mới `N`) là **chuyển cha bình thường** khi và chỉ
khi đạt CẢ BA vế:

- **(i)** `c` giữ nguyên `(pid, starttime)` giữa hai lần đọc;
- **(ii)** `P` không còn sống với cùng danh tính: `P` vắng khỏi `/proc`, HOẶC trạng thái của `P` (trường thứ 3 của
  `/proc/<P>/stat`) là `Z` hoặc `X`, HOẶC `starttime` của `P` khác giá trị đã xác thực của `P`;
- **(iii)** `N` thuộc chuỗi tổ tiên **đã xác thực** của `c` — chuỗi từ gốc tới `P` được lưu lúc `c` được xác thực
  lần cuối, kể cả chính gốc — và `(pid, starttime)` của `N` hiện khớp giá trị đã lưu trong chuỗi ấy.

Đạt cả ba ⇒ không ghi lỗi; cập nhật cạnh đã xác thực của `c` thành `(N, starttime)`; đếm `chuyen_cha_trong_cay`.
Thiếu bất kỳ vế nào ⇒ `DanhTinhDoi` như hiện nay. Riêng: `N` là PID 1 hoặc ngoài chuỗi (vế (iii) hỏng, (i)(ii) đạt)
⇒ `DanhTinhDoi`, đếm `chuyen_cha_ngoai_cay` (Q3: chưa đo thấy ca này, không nới khi chưa có bằng chứng).

Áp cho **hai** chỗ lệch hiện ghi `DanhTinhDoi`:
- **xuyên lượt** — nhánh `self.canh` (cùng `starttime`, khác ppid);
- **trong lượt** — `sau != (cha, bd)` khi đọc lại stat của con (Q4): đạt quy tắc ⇒ **bỏ nhánh** trong lượt này
  (không vào hàng đợi, không ghi quan sát, không lỗi); lượt sau sẽ thấy `c` dưới `N`.

Tổ tiên trong chuỗi đọc lại mà **vắng** khỏi `/proc` ⇒ bỏ nhánh, không lỗi, không ghi quan sát (cùng ngoại lệ "tiến
trình đã biến mất" vốn có; không tạo quan sát mới nên không khai mạnh hơn phép đo — nhận định của r27c, dòng 368).
Tổ tiên còn sống mà `starttime` hoặc ppid đổi (không đạt quy tắc) ⇒ `DanhTinhDoi` như hiện nay.

**Không đổi:** gốc tái dùng PID ⇒ `RuntimeError` (R27-PID-04); gốc không ghim được ⇒ `GocKhongGhimDuoc`, không ghim
muộn (04d); đọc bị từ chối (`PermissionError`, `OSError` khác) ⇒ lỗi (R27-PROC-03); đối chiếu `self.canh` chạy TRƯỚC
`return` khi gốc vắng (04g); `starttime` của tiến trình đang đọc đổi ⇒ `DanhTinhDoi` (04/04b); toàn bộ bảng số đối
số và danh sách cho phép (R27-PARSE-02/02b, R27-ALLOW-01).

### 2.2 Hàm thuần phân loại (Q10, Q19)

Logic quyết định của §2.1 nằm trong **một hàm thuần** ở `.claude/dev/launcher.py` (không đọc `/proc`, không gọi
`platform`), nhận danh tính cũ/mới của `c`, trạng thái quan sát được của `P`, chuỗi tổ tiên đã lưu và danh tính
hiện của `N`; trả **một** nhãn của §2.3 hoặc nhãn "tha". `_quet` gọi hàm này ở cả hai chỗ của §2.1. Hàm chạy được
trên mọi nền, để A3 đo được trên Windows thật.

### 2.3 Chẩn đoán `sandbox_lech` (Q5, Q13)

`ghi_so` **luôn** ghi `ban_ghi["sandbox_lech"]`: dict có ĐÚNG năm khoá cố định, giá trị là số nguyên ≥ 0, kể cả khi
mọi giá trị bằng 0, kể cả trên nền không phải Linux. Không chứa pid, tên tiến trình hay đường dẫn.

| khoá | đếm SỐ LẦN (sự kiện lệch) khi |
|---|---|
| `chuyen_cha_trong_cay` | đạt (i)(ii)(iii) — được tha |
| `chuyen_cha_ngoai_cay` | đạt (i)(ii), hỏng (iii) |
| `cha_con_song` | đạt (i), hỏng (ii) |
| `tai_dung` | hỏng (i): `starttime` của tiến trình đang đọc đổi trong lượt |
| `to_tien_doi` | một tổ tiên còn sống trong chuỗi đọc lại có `starttime` hoặc ppid khác giá trị đã lưu |

Gốc tái dùng (`RuntimeError`) không đếm vào `sandbox_lech`. Một sự kiện lệch vào đúng một khoá.

### 2.4 Câu khai `sandbox_gioi_han` (Q12)

Trong `_SANDBOX_GIOI_HAN`, câu *"Moi lech danh tinh tien trinh (ke ca vong doi binh thuong nhu cha zombie) =>
KHONG_DO_DUOC: co the ha nham mot luot binh thuong, khong bao gio khai manh hon phep do"* được thay bằng câu chứa
nguyên văn cụm: `chuyen cha khi cha cu da mat/Z va cha moi la to tien da xac thuc thi duoc tha; moi lech khac (ke ca
chuyen ra ngoai cay hay PID 1) => KHONG_DO_DUOC`. Chú thích khối R27-PID-04b/c/d trong `_quet` được viết lại theo
§2.1, giữ nguyên lịch sử r27 (quyết định THU HẸP 26-10-2026) và ghi quyết định mới này kèm Issue #1105.

## 3. Write set

```yaml
write_set:
  - .claude/dev/launcher.py
  - .claude/dev/launcher_test.py
  - ops/handoff/wp1105-g1-claude.md
```

Ba tệp. `ops/handoff/wp1105-g1-claude.md` chỉ sống trên nhánh lease/handoff, không vào diff PR (diff PR: 2 tệp).
`launcher_test.py` đã có trong sổ đăng ký `.claude/dev/ci_dang_ky_test.py` (dòng 79) — không thêm tệp test mới,
không chạm sổ đăng ký.

Xung đột đo lúc soạn (07:00Z 01-11-2026, `ops/lease_publish.py ai-dang-giu` trên clone có đủ `refs/heads/*` từ
origin; 7 ref không nhập được vì clone nguồn khi ấy còn nông — đo lại bắt buộc trước khi cấp lease):
`.claude/dev/launcher.py` ⇒ `NGƯỜI_GIỮ 0`; `.claude/dev/launcher_test.py` ⇒ `NGƯỜI_GIỮ 1: wp1079-r1-g1-claude`
(`lease_expires_at_utc: 2026-11-02T06:22:00Z`). Cấp lease cho packet này khi lease ấy còn hiệu lực là tự tạo cửa
sổ hai writer — phiên cấp lease phải đo lại và thấy `NGƯỜI_GIỮ 0` cho cả hai tệp.

```yaml
nang_tran:
  ai_nang: ducthangho   # chủ kho, protocol §2; phiên soạn đặc tả 01-11-2026, nguyên văn "Sửa trần <=10, <=850", chốt nghĩa ở Q16
  can_cu: >-
    Lớp lỗi sandbox-process-identity-race đã đi 7 vòng r27 và land ở 850 dòng thêm / 2 tệp (S6). Packet này chạm
    đúng hàm ấy và phải giữ toàn bộ phản chứng cũ (24 đột biến r27_* trong DOT_BIEN của launcher_test.py, đếm 07:37Z)
    trong khi thêm hàm thuần, chẩn đoán, fixture tiến trình thật và đột biến cho từng vế của quy tắc. Ước tính lúc
    soạn: launcher.py 60–100 dòng thêm, launcher_test.py 200–350 dòng thêm, tức có thể vượt 450. Không tách được:
    tách quy tắc khỏi phản chứng của nó là land một chốt nới mà chưa có răng.
  tran_cu: "ADR-0053@8ab1007: <= 6 tệp / <= 450 dòng thêm"
  tran_moi: "<= 10 tệp / <= 850 dòng thêm"
```

Trần lời gọi Codex: dòng khai `ADR-0055` ⇒ trần **10**; không có dòng khai `ADR-0052`. Ngân sách mềm do chủ kho
duyệt (Q9, Q17): dùng tối đa **4**; hai lượt liên tiếp chưa approve ⇒ Review Rescue Checkpoint (`ADR-0037`), hỏi
chủ kho trước lời gọi kế tiếp. Lượt bị cắt sau khi đã sinh output vẫn tính một lời gọi.

## 4. Nghiệm thu (mỗi dòng: phép đo, nền, và đột biến làm nó ĐỎ)

Tên ca mới mang tiền tố `r1105_`; tên dưới đây là bắt buộc để A-tiêu chí trỏ được. "Đột biến" là mục mới trong
`DOT_BIEN` của `launcher_test.py`, chạy bằng `--dot-bien`, phải giết **đúng ca đích ghi trong cột** (tín hiệu
`TinHieuChotCa` của ca đó, không phải lỗi vô can).

| # | tiêu chí | nền | đột biến làm ĐỎ (ca đích) |
|---|---|---|---|
| A1 | `python .claude/dev/launcher_test.py` ra `N/N`, hai số BẰNG NHAU; `--dot-bien` ra `M/M` bị giết, hai số bằng nhau | linux | — (cổng tổng) |
| A2 | Mọi phản chứng cũ giữ kỳ vọng cũ: trong `r927_lay_mau_loi_doc_va_danh_tinh_doi_khong_bi_nuot` bảy kịch bản `quyen` `danh_tinh_con` `goc_tai_dung` `to_tien_doi` `cha_zombie` `to_tien_doi_cha` `goc_khong_ghim` vẫn ra lỗi ghi trong ca và `KHONG_DO_DUOC`; trong `r927_canh_cha_doi_giua_hai_luot_quet` năm kịch bản `ra_ngoai` `vao_goc` `doi_chung` `goc_mat_chau_doi` `goc_mat_chau_mat` vẫn đúng kỳ vọng cũ. Không xoá, không đổi kỳ vọng kịch bản nào. 24 đột biến `r27_*` hiện có: mỗi cái hoặc giữ nguyên, hoặc (nếu chuỗi mã nó vá đã đổi) được thay bằng đột biến TƯƠNG ĐƯƠNG mang cùng tên và cùng ca đích; tổng số đột biến `r27_*` sau packet ≥ 24 | linux | `r1105_bo_ve_ii` (bỏ vế (ii)) ⇒ `vao_goc` ĐỎ · `r1105_bo_ve_iii` (bỏ vế (iii)) ⇒ `cha_zombie` ĐỎ (chỉ kịch bản này cô lập vế (iii); `ra_ngoai` hỏng cả (ii) vì cha cũ còn sống nên KHÔNG dùng làm đích) · `r1105_bo_ve_i` (tha cả khi `starttime` đổi) ⇒ `danh_tinh_con` ĐỎ · `r1105_tha_to_tien_doi` (tha tổ tiên còn sống đổi `starttime`) ⇒ `to_tien_doi` ĐỎ |
| A3 | `r1105_phan_loai_lech_ham_thuan`: hàm thuần §2.2, bảng ca phủ ĐỦ sáu đầu ra (tha + năm nhãn §2.3), mỗi vế (i)(ii)(iii) có một ca chỉ hỏng đúng vế ấy; `P` ở ba dạng của vế (ii) (vắng / `Z`/`X` / `starttime` khác) mỗi dạng một ca dương; `N` = PID 1 và `N` ngoài chuỗi mỗi cái một ca âm. Ca KHÔNG đọc `/proc`, KHÔNG rẽ theo nền | linux + windows | `r1105_ham_tha_moi_ca` (luôn trả "tha") và `r1105_ham_khong_tha` (không bao giờ trả "tha") ⇒ ca ĐỎ; `r1105_ham_bo_trang_thai_X` (chỉ nhận `Z`) ⇒ ca ĐỎ |
| A4 | `r1105_cha_zombie_ve_to_tien` (Q11): dựng y như kịch bản `cha_zombie` nhưng cháu chuyển về **gốc** ⇒ `loi == []`, `sandbox_lech["chuyen_cha_trong_cay"] == 1`, có quan sát ⇒ `DO_DUOC`. Cặp với `cha_zombie` (ppid=1, vẫn đỏ ở A2): hai ca chỉ khác vế (iii) | linux | `r1105_khong_tha_trong_luot` (gỡ quy tắc ở chỗ trong-lượt) ⇒ ca này ĐỎ |
| A5 | `r1105_chuyen_cha_xuyen_luot`: hai lượt quét một sampler; lượt 2 cháu (còn sống, `starttime` giữ) đổi ppid về gốc trong khi cha cũ đã vắng ⇒ không lỗi, cạnh trong `self.canh` cập nhật về gốc, `chuyen_cha_trong_cay == 1`. Đối chứng cùng ca: cha cũ CÒN sống ⇒ `DanhTinhDoi`, `cha_con_song == 1` | linux | `r1105_khong_tha_xuyen_luot` (gỡ quy tắc ở nhánh `self.canh`) ⇒ ĐỎ · `r1105_tha_khong_cap_nhat_canh` (tha mà giữ cạnh cũ) ⇒ ĐỎ |
| A6 | `r1105_tien_trinh_that_ve_subreaper` (Q6 tầng 1): tiến trình THẬT, không giả `/proc`: helper đặt `PR_SET_CHILD_SUBREAPER` (đóng vai init namespace), sinh con, con sinh cháu; ca gọi `_quet` MỘT lượt khi cháu còn dưới con, rồi cho con thoát và ĐỢI tới khi `/proc/<cháu>/stat` báo ppid = helper (đồng bộ tất định, không ngủ đoán giờ), rồi gọi `_quet` lượt hai — tức đi đúng nhánh xuyên lượt. Sampler gốc = helper ⇒ `loi == []`, `chuyen_cha_trong_cay ≥ 1`, và có ít nhất một quan sát (argv giả `bwrap` hợp lệ theo bảng số đối số, dựng như `_R27_BWRAP`) ⇒ `DO_DUOC`. Thiếu `prctl` (không phải Linux) ⇒ ca trả lý do bỏ qua; trên Linux mà không đặt được subreaper ⇒ ĐỎ, không bỏ qua | linux | `r1105_khong_tha_xuyen_luot` ⇒ ca này ĐỎ (cùng đột biến với A5, ca đích thứ hai) |
| A7 | `r1105_sandbox_lech_luon_co`: `ghi_so` trên (a) sampler sạch, (b) sampler có lỗi, (c) sampler nền không phải Linux (`luong is None`, dựng tường minh, không phụ thuộc nền chủ — bài học R27-TEST-05) ⇒ cả ba có `sandbox_lech` đúng năm khoá §2.3, giá trị `int ≥ 0`; giá trị không chứa chuỗi | linux + windows | `r1105_bo_sandbox_lech_khi_sach` (chỉ ghi khi có lệch) ⇒ ĐỎ · `r1105_dem_sai_khoa` (đếm `chuyen_cha_ngoai_cay` vào `chuyen_cha_trong_cay`) ⇒ A4 hoặc A3 ĐỎ |
| A8 | `r1105_gioi_han_khai_dung_pham_vi` (Q12, L6): đo trên CHUỖI ĐÃ ĐÁNH GIÁ `m._SANDBOX_GIOI_HAN % m._CHU_KY_SANDBOX` (không đo Markdown, không bị ngắt dòng) — vế dương: chứa nguyên cụm §2.4; vế âm: KHÔNG chứa `ke ca vong doi binh thuong nhu cha zombie`. Cùng ca: `r927_lenh_run_ghi_effort_va_sandbox_vao_run_json` (hoặc ca mới cạnh nó) đòi `run.json` có khoá `sandbox_lech` | linux | đột biến trả câu cũ ⇒ vế âm ĐỎ; đột biến cắt hậu tố `(ke ca chuyen ra ngoai cay hay PID 1) => KHONG_DO_DUOC` ⇒ vế dương ĐỎ |
| A9 | `git diff --numstat <base_oid> <candidate_oid>`: chỉ `.claude/dev/launcher.py` và `.claude/dev/launcher_test.py`; tổng dòng thêm ≤ 850 (khối `nang_tran` §3). Trước khi tính, kiểm staged/unstaged/untracked rỗng | — | thêm tệp thứ ba vào diff ⇒ ĐỎ; vượt 850 ⇒ dừng, checkpoint chủ kho |
| A10 | Windows theo `ADR-0060` M3 (bước 2: diff chạm `.claude/dev/**` và đặc tả khai `windows: required`), trên máy chủ kho qua Desktop Commander theo `ADR-0057`/`0058`/`0059` (khoá, kiểm tải, thư mục riêng, sổ đo): hai lượt — nền và ứng viên — dựng trong MỘT lệnh, mỗi lượt chạy trọn `launcher_test.py`, ghi danh sách test ID kèm kết quả; đủ M3 (a)–(c). **Tập ca được bỏ qua trên Windows là TƯƠNG ĐỐI theo nền, không phải danh sách cố định** (errata r2): gọi `B_nen` là tập (tên ca, lý do bỏ qua) của lượt nền và `B_ung` của lượt ứng viên, cùng máy, cùng lệnh; điều kiện là `B_ung ⊆ B_nen ∪ {r1105_cha_zombie_ve_to_tien, r1105_chuyen_cha_xuyen_luot, r1105_tien_trinh_that_ve_subreaper}` (ba ca mới chỉ chạy trên Linux vì cần `/proc`), so cả TÊN lẫn LÝ DO. Lượt nền hiện đã bỏ qua nhiều ca chỉ có `/proc` (ví dụ `t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan`, `t157_giet_cay_khi_stat_EACCES_van_tron_ven`, `r743_con_song_tham_do_bang_stat_giu_errno_moi_phien_ban` và năm ca `r927_*` liệt kê ở r1) — những ca ấy được tha vì đã bỏ qua sẵn trên nền. Ca bị bỏ qua trên ứng viên mà KHÔNG có trong vế phải ⇒ không xanh; ca có trong `B_nen` mà đổi lý do ⇒ không xanh. A3 và A7 PHẢI chạy (không bỏ qua) trên ứng viên Windows | windows (local) | ca nào của A3/A7 bị bỏ qua trên Windows ⇒ ĐỎ; máy không `Online` quá 24 giờ ⇒ packet `blocked` (không tự miễn, `ADR-0060` Tham số) |
| A11 | `full_mutant_audit` theo `ADR-0060` M9: **bắt buộc** (diff chạm `.claude/dev/**`) | linux (CI) | thiếu receipt hoặc waiver `owner_waived` đúng scope §10.2.3 khi merge |
| A12 | Gate phụ trên ứng viên: `python -m ruff check --select F` cho hai tệp, DELTA so nền = 0 (ruff không có sẵn trong container soạn — cài khi thi hành, đo nền và ứng viên cùng lệnh); `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `git diff --check` rc 0 | linux | — (cổng canh bất biến; xanh sẵn trên nền là đúng) |
| A13 | **Canary M1** (Q6 tầng 3, Q15): `run.json` của lượt cross-review Codex offline trên SHA ứng viên cuối (`ADR-0060` M12), chạy bằng `launcher.py` CỦA CHÍNH ứng viên ⇒ `sandbox_trang_thai == "DO_DUOC"` và có `sandbox_lech`. Bằng chứng: sha256 của `launcher.py` đã chạy (ghi trong handoff, đo bằng `sha256sum` trên đường dẫn đã truyền cho lệnh) khớp sha256 của blob `<candidate_oid>:.claude/dev/launcher.py`. Lượt chạy bằng `launcher.py` của master ⇒ KHÔNG tính | linux | không khớp sha256 ⇒ không tính (ĐỎ); `KHONG_DO_DUOC` ⇒ ĐỎ, xử như §6 |
| A14 | Bằng chứng tay (Q6 tầng 2), ghi trong handoff, KHÔNG phải test: lặp phép đo S4 (`codex sandbox`, lệnh bỏ lại tiến trình nền, ≥ 3 lượt) trên nền và trên ứng viên; ghi số lượt `DO_DUOC` mỗi bên và `sandbox_lech` của ứng viên | linux | ứng viên vẫn `KHONG_DO_DUOC` ở lệnh S4 ⇒ ĐỎ |

Chạy thử trên nền `c6dd7b3` lúc soạn (07:37Z): `--lap-ca` của bốn ca `r927_*` ở A2 ra `1/1 qua` mỗi ca; mọi ca
`r1105_*` ra `khop 0 ca` (chưa làm — đúng màu); `rg -c sandbox_lech .claude/dev/launcher.py` = 0 (A7/A8 chưa làm);
cụm cũ `ke ca vong doi binh thuong nhu cha zombie` có 1 dòng (vế âm A8 ĐỎ trên nền, đúng màu). A1, A10–A13 đo khi
thi hành.

## 5. Ngoài phạm vi

- Tha chuyển cha về PID 1 / ra ngoài cây (Q3): r2, chỉ khi `sandbox_lech.chuyen_cha_ngoai_cay` trên lượt Codex thật
  cho thấy nó xảy ra.
- Đổi nguồn bằng chứng (cgroup, đặt launcher làm subreaper) hay đổi lời khai `DO_DUOC` (Q1 phương án b, c).
- Lấy mẫu sandbox trên Windows/macOS (vẫn `KHONG_DO_DUOC` theo nền).
- `workflow_dispatch windows-only` (Q19: lượt A10 trên máy chủ kho thay cho nó trong nghiệm thu này; CI Windows tự
  động của kho giữ nguyên).
- Cổng máy đọc khai báo nền trong đặc tả (chưa kiểm cổng nào làm việc này; nếu muốn thì là packet riêng).
- Sửa `docs/PROTOCOL_DA_PHIEN.md` §8.1 hay hồ sơ land #1039/#1089.

## 6. `chua_do_duoc`

- Lệch ở **8 lượt Codex thật** của S1 có đúng dạng S5 hay không: `run.json` cũ không ghi chi tiết (S3), nên đây là
  suy từ tái hiện `codex sandbox`, không phải đo trên chính tám lượt ấy. A13 là phép đo đầu tiên trên lượt thật.
- A13 là MỘT lượt: một `DO_DUOC` không chứng minh tỷ lệ. Nếu A13 ra `KHONG_DO_DUOC`: đọc `sandbox_lech` của lượt ấy;
  lệch thuộc `chuyen_cha_ngoai_cay` ⇒ checkpoint chủ kho (ứng viên cho r2 theo §5), không tự nới quy tắc; lệch khác ⇒
  finding của packet.
- Hành vi trên kernel/phiên bản codex khác container soạn (codex-cli 0.166.0, Linux 6.18): chưa đo.
- Thời lượng A10 (`launcher_test.py` trọn bộ trên Windows, hai lượt) và A11: chưa đo cho packet này.
- Máy Windows của chủ kho có `Online` trong thời gian thi hành hay không: chỉ biết lúc đo (`list_devices`).

## 7. hinh_dang_ke_thua

Chép từ hồ sơ r27 (`ops/land/pr957-wp748-r27-provenance/verdicts/wp748-r27-r27a-verdict.md` … `-r27g-verdict.md`),
đơn vị là BIỂU HIỆN finding:

| lớp | biểu hiện | trạng thái cuối r27 | quan hệ với packet này |
|---|---|---|---|
| `sandbox-process-identity-race` | **7**: R27-PID-04, 04b, 04c, 04d, 04e, 04f, 04g | đóng ở r27g (approve) | packet MỞ LẠI đúng 04c (cha zombie, *"closed by design"* theo quyết định THU HẸP); 04, 04b, 04d, 04e, 04f, 04g phải ở nguyên trạng đóng (A2) |
| `sandbox-argv-boundary` | 2: R27-PARSE-02, 02b | đóng | không chạm; giữ đóng (A2) |
| `sandbox-sampling-errors-hidden` | 1: R27-PROC-03 | đóng | không chạm; giữ đóng (A2) |
| `sandbox-output-not-closed` | 1: R27-ALLOW-01 (P1) | đóng | `sandbox_lech` chỉ chứa khoá cố định và số (A7) — cùng nguyên tắc danh sách cho phép |
| `sandbox-status-tests-native-platform-dependence` | 1: R27-TEST-05 | đóng | A3/A7 dựng nền tường minh, đo native trên Windows (A10) |

Bộ đếm hình dạng của lớp thứ nhất bắt đầu ở **7**, không ở 0 — đã quá ngưỡng "cùng hình dạng lặp ba lần" của
CLAUDE.md. Vì vậy biểu hiện MỚI ĐẦU TIÊN của `sandbox-process-identity-race` trong review của packet này (biểu hiện
thứ 8) ⇒ dừng, checkpoint chủ kho với câu *"có nên làm việc này không"* trước khi vá. Độc lập với chốt hai lượt liền
chưa approve ở §3.

## 8. Bản đồ quyết định (phiên soạn, 01-11-2026)

| câu | quyết định | nằm ở |
|---|---|---|
| Q1 | giữ thiết kế, thêm một quy tắc tha hẹp | §2.1 |
| Q2 | ba vế (i)(ii)(iii) | §2.1 |
| Q3 | PID 1 / ngoài cây vẫn `DanhTinhDoi` | §2.1, §5 |
| Q4 | lệch trong lượt đạt quy tắc ⇒ bỏ nhánh, không lỗi | §2.1 |
| Q5, Q13 | `sandbox_lech` năm khoá, luôn ghi | §2.3, A7 |
| Q6 | M1 ba tầng: fixture thật, `codex sandbox` tay, canary | A6, A14, A13 |
| Q7 | write set 3 tệp, `depends_on` #1079 | §3 |
| Q8, Q16 | trần kích thước ≤ 10 tệp / ≤ 850 dòng thêm (`nang_tran`) | §3 |
| Q9, Q17 | dòng khai `ADR-0055` (trần 10), ngân sách mềm 4 | §3 |
| Q10, Q19 | hàm thuần chạy mọi nền; Windows qua `ADR-0060` M3 local, không `workflow_dispatch` | §2.2, A3, A10 |
| Q11 | giữ `cha_zombie`, thêm `r1105_cha_zombie_ve_to_tien` | A2, A4 |
| Q12 | câu `sandbox_gioi_han` mới | §2.4, A8 |
| Q14 | base ghim lúc cấp lease | bảng đầu |
| Q15 | Claude executor, Codex reviewer, canary bằng `launcher.py` của ứng viên | bảng đầu, A13 |
| Q18 | dòng khai `ADR-0060` + `windows: required` | đầu tệp, A10, A11 |

## `errata_r2`

- r1 đóng băng ở commit `981d44df`, blob `f01fa1d2`, sha256 `d73a9506…` (issuecomment-6555126339). r2 do phiên điều phối
  `session_015GtxraXfMD1t2FJLzzGDr4` soạn theo hai finding P2 của Codex connector trên PR #1112 (head `981d44d`); mọi chỗ khác giữ
  nguyên từng byte so với r1.
- **A10 (review comment 4434823433).** r1 liệt kê đúng tám ca được bỏ qua trên Windows và cấm mọi ca bỏ qua khác, nhưng nhiều ca
  hiện có ngoài danh sách bỏ qua vô điều kiện khi không phải Linux (đo trên master: `t156_…`, `t157_…`, `r743_…` đều
  `return "bo qua: nhanh /proc chi co tren Linux"`), nên ngay cả một bản cài đặt đúng cũng không thể đạt A10. r2 đổi sang quy tắc
  TƯƠNG ĐỐI theo lượt nền cùng máy: tập bỏ qua của ứng viên ⊆ tập bỏ qua của nền ∪ ba ca `r1105_` chỉ-Linux, so cả tên và lý do.
  A3/A7 vẫn bắt buộc chạy trên Windows.
- **A2 (review comment 4434823437).** r1 đòi `r1105_bo_ve_iii` làm `ra_ngoai` ĐỎ, nhưng kịch bản `ra_ngoai` của
  `r927_canh_cha_doi_giua_hai_luot_quet` đổi ppid của cháu về 1 trong khi cha cũ CÒN sống (`mat = ()`), tức hỏng cả vế (ii) — bỏ riêng
  vế (iii) vẫn ra `DanhTinhDoi` qua vế (ii), nên ca đích ấy không đo được đột biến. r2 chỉ giữ `cha_zombie` làm ca đích của
  `r1105_bo_ve_iii` (kịch bản này đạt (i)(ii) và chỉ hỏng (iii)); `ra_ngoai` vẫn nằm trong A2 như một phản chứng giữ kỳ vọng cũ.
- **Không đổi:** write set, trần, `tran_loi_goi_codex`, `dieu_kien_merge`, `windows: required`, `depends_on`, mọi tiêu chí khác.

