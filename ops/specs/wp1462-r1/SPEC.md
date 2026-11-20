# wp1462 r5 — B4 của kế hoạch nguồn r4: công tắc CHO PHÉP theo lớp giảm và bên tiêu dùng tin cậy trong `kiem-merge` (CONG-TAC-G5)
packet_id: wp1462
revision: 5
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

Trạng thái: `proposed`, CHƯA đóng băng. Thay r4 (cùng đường dẫn, commit `0cfb924`, sha256 `4952e70fca6fb23de56703dc8022d7fd1f841f6514884ac8c70786e687b0277e`); r4 thay r3 (commit `6a0612f`, sha256 `fcb2fc2c319b7652cfafe182927f13e4f68ae8321bc4c4cc4c6bda28f57eedf4`); r3 thay r2 (commit `0d80f45`, sha256 `f16c00227d7643554fe00116deef53cf6367d9c094bfd9ebd4419c3e95d69621`), bản ấy thay r1 (commit `7582454`, sha256 `3ca1c75001d96e46e342a042f343ca192fba5626298fc118e5ce0932a8c8661f`). Review đặc tả Codex lượt 1 (`wp1462-spec-review-1`): 8 finding P2 (B4-S01…B4-S08), r2 sửa. Lượt 2 (`wp1462-spec-review-2`): 7/8 đóng, B4-S05 đóng một phần, thêm B4-S09, B4-S10 (P2) và B4-S11 (P3); r3 sửa cả bốn. Lượt 3 (`wp1462-spec-review-3`): B4-S09, B4-S11 đóng; B4-S05 và B4-S10 đóng một phần; thêm B4-S12 (P2); r4 sửa cả ba. Lượt 4 (`wp1462-spec-review-4`, có slug lớp theo protocol §8.3): B4-S12 đóng; còn ba lớp P2 — `b4-predicate-mutation-proof` (B4-S05, lượt thứ tư), `b4-sensitive-size-authority` (B4-S10), `b4-eligibility-permission-contract` (B4-S13, mới); r5 sửa THEO LỚP, theo quyết định checkpoint §12 của điều phối tại `https://github.com/ducthangho/tra-luat/issues/1462#issuecomment-7046200733`. Bảng đối chiếu ở mục "Thay đổi". Dòng `tran_kich_thuoc_sensitive` ở đầu tệp kích hoạt trần `ADR-0053`; OID đã đo lúc soạn r3 (16:55Z 20-11-2026): tệp ADR có ở OID ấy, vắng ở cha thứ nhất `25cda362`, và OID nằm trên chuỗi first-parent của `origin/master` (kho không shallow). Đặc tả Packet #1462, vai B4 của Mission #1172 theo **kế hoạch nguồn r4** (`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md`, nhánh `ops/wp1172-plan-r4`, sha256 `0f287ce4369fbeb7b1939daa8de5db7c27c2a4efdc1a21f2fccdd37dc9d83fbe`). Quyết định chủ kho: Mission r84 (`owner_decisions.Q9`: (a)–(d) theo khuyến nghị); thẩm quyền soạn đặc tả và trần: Mission r85 (`packet_graph` vai B4, `envelope.provider_budgets.per_new_packet`, `r85_constraints`). Mọi tham chiếu "§" là mục của kế hoạch r4; nơi đặc tả này và kế hoạch khác nhau thì **đặc tả này thắng** cho packet này, và mọi chỗ khác chữ kế hoạch được liệt kê ở mục "Chỗ khác chữ kế hoạch". Rủi ro: nhạy cảm (tệp nóng `.claude/dev/packet_loop.py`, cổng merge). Nền đo: `origin/master` = `0f9aa2a2cc697129e1f5be72feddf60986286865` (đo 16:10Z 20-11-2026); blob `.claude/dev/packet_loop.py` = `3db1abae`, `ops/ci_duong_nhanh.py` = `e43f514c`, `.github/workflows/ci.yml` = `a1db88d9` tại commit ấy.

Đặc tả này KHÔNG dựng lại cơ chế nào kế hoạch đã rút: không kho uỷ quyền do máy kiểm (biến có thế hệ, comment của chủ kho, tệp git do chủ kho merge — R4-08, R4-19…R4-24, §12 (15)); không lấy log CI làm nguồn giá trị công tắc (R4-25, §12 (17)); không trạng thái `FULL` buộc mọi PR chạy đủ (§12 (16), Q9(c)); không `pull_request_target` (§12 (14)); không vị từ theo `updated_at`.

## Mục tiêu
Trước khi PR3 land, cổng merge phải có sẵn hai thứ để PR3/PR6 không tự cấp làn nhẹ cho mình: (1) một **công tắc mặc định ĐÓNG cho từng lớp giảm** (biến Actions mức kho; chỉ đúng một chuỗi cho phép mới mở; vắng, rỗng, lạ, không đọc được ⇒ chạy đủ); (2) một **bên tiêu dùng tin cậy trong `kiem-merge`**: khi bằng chứng trên H không có G5 đủ, nó tự tính lại làn bằng mã của `master` và tự đọc công tắc SỐNG qua REST trong chính lượt gọi, không tin output hay log của job PR. Trước PR3 chưa lớp giảm nào tồn tại, nên B4 phải **nằm im** (không mở được gì, không gọi REST trong vận hành thật) mà vẫn được kiểm bằng fixture và đồ giả.

## Hợp đồng

### 1. Bất biến (cưỡng chế bằng ca test ở mục Nghiệm thu)
- **B-1 Chỉ siết.** Không đường nào của B4 làm một lượt `kiem-merge` đang ĐỎ trên base thành ĐẠT. Trên mọi đầu vào mà base đạt, head hoặc đạt hoặc đỏ thêm đúng điều kiện mới `K2b làn G5`.
- **B-2 Không đổi hành vi khi có G5 đủ.** Bằng chứng trên H là `du` (mục 3) ⇒ rc, stdout, stderr của `kiem-merge` trùng BYTE với base (so trên lời gọi không có cờ mới); không chạy bộ phân loại, không tự kiểm cây, không mở kết nối, không in dòng mới nào — có hay không có cờ siết.
- **B-3 B4 không đặt và không cần `CHO_PHEP`.** Mã B4 chỉ gửi phương thức GET; không lời gọi nào tạo, sửa, xoá biến. Executor, reviewer và phiên điều phối không tạo hai biến công tắc ở bất kỳ giá trị nào. Nghiệm thu B4 không phụ thuộc biến thật.
- **B-4 Không đầu vào nào của người gọi nới được.** Giá trị công tắc, tên biến, chuỗi cho phép, máy chủ API, commit M, đường dẫn bộ phân loại và kết quả phân loại KHÔNG lấy từ đối số, tệp readback, biến môi trường, bộ đệm hay log. `kiem-merge` không giữ trạng thái giữa hai lượt gọi.
- **B-5 Ba trạng thái.** Mọi phép đo mới có ba kết cục: đạt · không đạt · không đo được; cái thứ ba luôn dẫn về đòi G5 đủ (đỏ), không bao giờ về đạt.
- **B-6 Không đổi K0–K7.** Thân K0, K1, K3–K7, hàm `_kiem_ci`, hằng `CHECK_BAT_BUOC` và mọi lệnh khác của `packet_loop.py` giữ nguyên hành vi. Được phép tách phần "run `ci-dot-bien-du.yml` success đúng H" của K7 thành hàm dùng chung, với điều kiện K7 không đổi kết quả trên mọi ca `cong_m9_*` hiện có.

### 2. Bảng lớp giảm và công tắc (hằng trong mã, đóng băng ở đây)

| Lớp giảm | Packet sinh ra lớp | Biến Actions mức kho | Chuỗi cho phép (`CHO_PHEP` của lớp) |
|---|---|---|---|
| `bo_moi` | PR3 | `TL_GIAM_G5_BO_MOI` | `cho-phep-bo-moi-pr3` |
| `che_do_dich` | PR6 | `TL_GIAM_G5_CHE_DO_DICH` | `cho-phep-che-do-dich-pr6` |

So khớp bằng `==` trên chuỗi đã giải mã JSON: không cắt khoảng trắng, không đổi hoa thường, không chuẩn hoá Unicode. `CHO_PHEP` của lớp này không mở lớp kia. Lớp thứ ba (C2, M9 theo rủi ro) do đặc tả C2 thêm cặp riêng vào bảng; B4 không khai trước cặp ấy và không đụng K7. Kho được đọc công tắc là hằng `ducthangho/tra-luat`; `--repo` khác hằng ấy ⇒ công tắc ở trạng thái không đọc được.

### 3. Bằng chứng G5 trên H — hợp đồng H2 (PR3 và PR6 phải theo trong write set của chính chúng)
Nguồn: các tệp `--workflow-runs` / `--workflow-jobs` mà K2 đã dùng. K2b TỰ ràng buộc danh tính, không dựa vào K2 (đo của review lượt 1: K2 hôm nay không kiểm run, attempt, head của job mảnh):
- **Run** R = run có `id` lớn nhất trong `--workflow-runs` thoả cả ba: `path` = `.github/workflows/ci.yml`, `head_sha` = H, `repository.full_name` = `--repo`. **Attempt** A = `run_attempt` của R.
- **Tập job** J = mọi job trong `--workflow-jobs` có (`run_id`, `run_attempt`) = (R.`id`, A). Job của run khác, của attempt khác, của workflow khác không bao giờ được tính.
- Mức tin của bằng chứng bằng đúng mức của K2 hôm nay (readback REST do người gọi lấy), không cao hơn. Không đọc log, artifact hay output job.

`che_do_thuc_chay` ∈ {`du`, `dich`, `khac`}. Gọi S_DU = `G5 manh ban kinh dot bien (#668)` và S_DICH = `G5 manh che do dich (PR6)`.
- `du` ⇔ với MỖI k ∈ 0..7: trong J có ĐÚNG MỘT job tên `gate-cong-cu (ubuntu-latest, k)`; job ấy có `head_sha` = H, `status` = `completed`, `conclusion` = `success`; `steps` là list mà mọi phần tử là object có `name` kiểu chuỗi; trong đó ĐÚNG MỘT bước tên S_DU, bước ấy `status` = `completed` và `conclusion` = `success`; và không bước nào tên S_DICH có `conclusion` = `success`.
- `dich` ⇔ cùng mọi điều kiện về 8 job, đổi vai hai tên bước: ĐÚNG MỘT bước S_DICH `completed`/`success`, và không bước S_DU nào có `conclusion` = `success`.
- `khac` ⇔ mọi trường hợp còn lại, kể cả không xác định được R.
- Hai chế độ PHẢI dùng chung MỘT hàm kiểm mảnh, tham số hoá theo (tên bước chính, tên bước kia); không viết hai bản. Nhờ đó mỗi chốt về job và bước chỉ có một chỗ trong mã, và một đột biến gỡ chốt ấy làm đổi kết cục của cả ca `du` lẫn ca `dich` tương ứng.

Nghĩa vụ của PR3/PR6: mọi chế độ không phải bán kính đủ KHÔNG được chạy bước tên S_DU tới `success`; chế độ đích chạy dưới đúng tên bước S_DICH, trong chính job `gate-cong-cu`; mỗi tên bước xuất hiện nhiều nhất một lần trong job ấy. Đổi tên job hay tên bước là đổi hợp đồng này và cần một packet sửa `packet_loop.py`. Tên S_DU đo tại `ci.yml` dòng 620 của nền (16:10Z 20-11-2026); S_DICH chưa tồn tại ở nền (quan sát, không phải chốt). Giới hạn nói thẳng: tên job và tên bước do `ci.yml` của PR định nghĩa; chốt cho PR sửa `ci.yml` vẫn là review `sensitive` và K7, như hôm nay.

### 4. Điều kiện mới `K2b làn G5` trong `cmd_kiem_merge`
Vị trí: một lời `_dk("K2b làn G5", …)` đặt SAU K7 trong thứ tự liệt kê, chỉ chạy khi K2 không có dòng thiếu (cùng khuôn "K5 chỉ chạy khi K3 đạt"); K2 đỏ thì K2b không chạy và không in gì. Tên `K2b` để nó là điều kiện con của K2: mọi tài liệu ghi "K0–K7" vẫn đúng chữ. Đỏ ⇒ một dòng `THIẾU  K2b làn G5: <lý do>` và rc 12 như mọi điều kiện khác.

Thứ tự quyết định, dừng ở bước đầu khớp:
1. `che_do_thuc_chay` = `du` ⇒ ĐẠT, im lặng (B-2), có hay không có cờ siết.
2. Có cờ `--siet-g5-du` ⇒ ĐỎ. Không tự kiểm, không tính lại, không đọc công tắc.
3. Tự kiểm cây (mục 7). Lệch hoặc không đo được ⇒ ĐỎ (từ chối).
4. Tính lại lớp bằng mã `master` (mục 5) ⇒ `duong_nhanh` | `bo_moi` | `che_do_dich` | `khong_giam` | `la`.
   - `la` ⇒ ĐỎ. `khong_giam` ⇒ ĐỎ (thiếu G5 đủ trên H).
   - `duong_nhanh` ⇒ ĐẠT — trường hợp (α), ngoại lệ đang có của wp892/#674; không đọc công tắc.
   - `bo_moi` ⇒ đọc sống công tắc của lớp (mục 6); `khop` ⇒ ĐẠT — trường hợp (β); mọi trạng thái khác ⇒ ĐỎ.
   - `che_do_dich` ⇒ ĐẠT khi và chỉ khi CẢ BA, xét đúng thứ tự này: (i) `che_do_thuc_chay` = `dich`; (ii) có run `ci-dot-bien-du.yml` `success` đúng H theo đúng phép đo của K7 nhánh run — dòng miễn `full_mutant_audit: <H> mien` KHÔNG thay được, và thiếu `--dot-bien-du-runs`/`--dot-bien-du-jobs` là không đạt; (iii) công tắc của lớp `khop`. Lời GET chỉ được gửi khi (i) và (ii) đã đạt.

Trước PR3, bộ phân loại của `master` không in khoá `dk_bo_moi` hay `dk_che_do_dich`, nên bước 4 chỉ ra `duong_nhanh`, `khong_giam` hoặc `la`: không lời GET nào được gửi và không PR nào đạt nhờ (β).

### 5. Tính lại bằng mã `master` — hợp đồng H1 (đầu ra của bộ phân loại)
Hai hàm nội bộ, tên do executor đặt, vai cố định: **hàm chạy** `(root, cay_ma, goc, dau) -> lớp` làm mọi việc dưới đây với mã lấy từ commit `cay_ma`; **điểm gọi sản xuất** DUY NHẤT trong K2b gọi nó với `cay_ma` = `goc` = M và `dau` = H. Không đối số CLI, biến môi trường hay tệp nào đưa được `cay_ma`/`goc` khác M vào điểm gọi sản xuất.
- **Đầu vào.** M = OID của `refs/remotes/origin/master` (đã qua tự kiểm 7a). Commit hợp C = commit hai cha (`goc`, `dau`) dựng từ `git merge-tree --write-tree` với danh tính và ngày cố định; merge xung đột hoặc git lỗi ⇒ `la`. Không dùng `--base` của người gọi, không dùng `refs/pull/<n>/merge`, không dùng cây làm việc.
- **Mã chạy.** Đúng blob `ops/ci_duong_nhanh.py` tại `cay_ma`, trong một cây tạm dựng đúng từ cây của `cay_ma` (bộ phân loại thấy cây ấy là cây làm việc của nó, đọc object của kho `--root`), bằng tiến trình con `python -I` với hạn 120 s. Điểm vào là điểm vào sẵn có: không đối số, biến `CI_DUONG_NHANH_SU_KIEN=pull_request`, `CI_DUONG_NHANH_GOC=<goc>`, `CI_DUONG_NHANH_DAU=<dau>`, `CI_DUONG_NHANH_MERGE=C`. Môi trường dựng MỚI từ danh sách cho phép (`PATH`, `SYSTEMROOT`, `TEMP`, `TMP`, `TMPDIR`, `HOME`, `USERPROFILE`, cộng biến git cần cho thư mục object tạm); không truyền `GITHUB_OUTPUT` hay biến `CI_DUONG_NHANH_*` nào khác.
- **Không để lại gì.** Sau lượt gọi — đạt, đỏ, hết hạn hay kết thúc bằng `SystemExit` — kho `--root` không có thêm ref, worktree đăng ký hay object (commit C và cây merge nằm trong thư mục object tạm), và mọi thư mục tạm của lượt gọi đã bị xoá.
- **Khung dòng (như nhau trên mọi nền).** stdout của tiến trình con được đọc dạng BYTE, không qua lớp dịch xuống dòng nào của tiến trình cha. Toàn bộ phải là UTF-8 hợp lệ. Tách dòng tại byte LF; ở MỖI dòng, nếu byte cuối là CR thì bỏ ĐÚNG MỘT byte CR ấy (khung CRLF mà Python trên Windows tự sinh khi `ops/ci_duong_nhanh.py` in ở chế độ văn bản: tệp ấy chỉ đặt `encoding`/`errors` cho stdout, không đặt `newline` — review lượt 2 đo bằng mô phỏng trên Linux, chưa đo trên Windows thật). Không cắt gì khác: CR thứ hai ở cuối dòng, CR giữa dòng, dấu cách, tab đều thuộc GIÁ TRỊ và làm giá trị ra ngoài tập. Việc đọc đầu ra nằm trong MỘT hàm thuần `(rc, stdout dạng byte) -> lớp`, dùng MỘT bộ đọc khoá chung cho cả ba khoá.
- **Hai thứ tách rời: ĐIỀU KIỆN CẤU TRÚC và QUYẾT ĐỊNH CI.** Cùng một điểm vào phục vụ hai bên tiêu dùng, bằng hai kênh khác nhau:
  - *Kênh stdout — điều kiện cấu trúc, bên đọc là `kiem-merge`.* Hai khoá `dk_bo_moi` và `dk_che_do_dich`, giá trị `co` hoặc `khong`, nói PR có ĐỦ ĐIỀU KIỆN CẤU TRÚC của lớp giảm ấy hay không (PR3: diff ngoài bao đóng; PR6: diff trọn trong vùng K7). Chúng được tính CHỈ từ diff và mã tại `master`, KHÔNG phụ thuộc công tắc, `vars` hay bất kỳ biến quyền nào: lời gọi tin cậy của mục này không truyền biến nào như thế, và bộ sinh phải in cùng giá trị `dk_*` dù biến quyền có mặt, vắng, hay sai. Đủ điều kiện cấu trúc KHÔNG phải là được phép: quyền chỉ đến từ lời GET sống của mục 6 trong chính lượt `kiem-merge`.
  - *Kênh `GITHUB_OUTPUT` — quyết định CI, bên đọc là `ci.yml`.* Các output mà job đọc (ví dụ `cong_cu`, chế độ G5) là quyết định ĐÃ qua công tắc: `chuan-bi` truyền giá trị `vars` của lớp cho bộ phân loại qua biến môi trường, và chỉ khi PR đủ điều kiện cấu trúc VÀ biến ấy mang đúng chuỗi cho phép thì output mới là quyết định giảm; vắng, rỗng, lạ ⇒ output là chạy đủ (§4 A+1 "Trong CI"). `kiem-merge` KHÔNG đọc kênh này và không truyền `GITHUB_OUTPUT` cho tiến trình con.
  - Các dòng stdout khác, kể cả dòng lặp lại quyết định CI như `cong_cu=…`, bị `kiem-merge` bỏ qua.
- **Đọc đầu ra.** rc phải 0. Chỉ ba khoá được đọc, mỗi khoá là dòng `<khoá>=<giá trị>` khớp trọn dòng (sau khi bỏ khung): `che_do` (ĐÚNG một dòng, ∈ {`day_du`, `duong_nhanh`}); `dk_bo_moi` (0 hoặc 1 dòng, ∈ {`co`, `khong`}); `dk_che_do_dich` (0 hoặc 1 dòng, ∈ {`co`, `khong`}). Ánh xạ: `duong_nhanh` và không khoá `dk_*` nào bằng `co` ⇒ `duong_nhanh`; `day_du` + `dk_bo_moi=co` + `dk_che_do_dich` khác `co` ⇒ `bo_moi`; `day_du` + `dk_che_do_dich=co` + `dk_bo_moi` khác `co` ⇒ `che_do_dich`; `day_du` và không khoá nào bằng `co` ⇒ `khong_giam`. Mọi thứ khác — rc ≠ 0, hết hạn, stdout không phải UTF-8, thiếu `che_do`, khoá lặp, giá trị ngoài tập (kể cả thừa dấu cách, hay còn CR sau khi bỏ khung), `duong_nhanh` kèm một `dk_*` bằng `co`, cả hai `dk_*` bằng `co`, không có tệp bộ phân loại tại `cay_ma` — ⇒ `la`.
- **Nghĩa vụ của PR3/PR6 (trong write set của chính chúng):** (1) in `dk_bo_moi` / `dk_che_do_dich` trên stdout từ điểm vào ấy, đúng dạng trên, mỗi khoá một dòng kết thúc bằng LF hoặc CRLF, không phụ thuộc biến quyền; (2) chỉ xuất quyết định giảm ra `GITHUB_OUTPUT` khi đủ điều kiện cấu trúc VÀ biến quyền do `chuan-bi` truyền mang đúng chuỗi cho phép của lớp (bảng mục 2); mọi trạng thái khác của biến ⇒ xuất chạy đủ; (3) chạy được dưới `python -I` (không import module anh em bằng tên trần); (4) có ca trong bộ test của chính chúng chứng minh (1) và (2) trên cùng một diff. Giá trị ngoài hợp đồng là `la` ⇒ đỏ ở cổng merge. B4 không sửa `ops/ci_duong_nhanh.py` hay `ci.yml`.

Số đo lúc soạn (16:37Z 20-11-2026, phiên cloud Linux), gọi là **đường trực tiếp**: với mỗi merge trong `git log --first-parent --merges -60 0f9aa2a2cc697129e1f5be72feddf60986286865` (60 merge, mỗi cái hai cha), chạy `python -I ops/ci_duong_nhanh.py` của blob `e43f514c` trong cây làm việc tại commit ấy, với `GOC` = cha một, `DAU` = cha hai, `MERGE` = chính merge commit THẬT ⇒ 60/60 lượt rc 0 và đúng một dòng `che_do`: 42 `day_du`, 18 `duong_nhanh`. Bảng 60 dòng `<OID merge> <che_do>\n`, theo đúng thứ tự `git log` ấy, có sha256 `aa932267e766cf3f6e242f35febe3692909f3e909cb510177ba83d780bfc849a`. Đây là bộ phân loại HÔM NAY chạy trên lịch sử (cha một lịch sử làm gốc), KHÔNG phải đầu vào sản xuất của K2b (M sống) và không phải bằng chứng các PR ấy từng đi làn nào trên CI. Review lượt 1 đo thêm: đưa 60 head đã merge ấy vào với M hiện tại thì cả 60 ra `duong_nhanh` vì diff rỗng — phép phát lại kiểu đó vô nghĩa và không được dùng.

### 6. Đọc sống công tắc — hai tầng tách rời
**6a. Tầng chính sách** (hàm đọc công tắc của một lớp):
- Gửi ĐÚNG MỘT yêu cầu cho mỗi lượt cần đọc, tới `https://api.github.com/repos/ducthangho/tra-luat/actions/variables/<TÊN>` (URL ghép từ hằng), qua tầng vận chuyển 6b. Header: `Accept: application/vnd.github+json`, `X-GitHub-Api-Version`, `User-Agent` trung tính; nếu biến môi trường `GH_TOKEN` khác rỗng thì thêm `Authorization: Bearer`, không có thì gửi không xác thực. Giá trị token không bao giờ được in. Token chỉ ảnh hưởng việc ĐỌC ĐƯỢC hay không; nó không đổi được giá trị đọc về.
- **Dấu hiệu dương (đủ cả bốn):** mã 200; có ít nhất một header tên bắt đầu `x-github-` (không phân biệt hoa thường); thân dài không quá 65 536 byte, được giải mã bằng UTF-8 CHẶT trước khi đưa cho bộ phân tích JSON (bộ phân tích không bao giờ nhận byte thô: `json.loads` trên byte tự dò UTF-16/UTF-32 — review lượt 4 đo), và chuỗi ấy là JSON hợp lệ, không khoá trùng, gốc là object, với `name` là chuỗi bằng đúng `<TÊN>`; `value` kiểu chuỗi.
- **Bốn trạng thái, mỗi cái có định nghĩa riêng và phải phân biệt được ở dòng `CONG_TAC`:** `khop` (dương và `value` = chuỗi cho phép của lớp) · `khong_khop` (dương, giá trị khác, kể cả rỗng) · `vang_hoac_khong_quyen` (404 có header `x-github-`) · `khong_doc_duoc` (mọi thứ còn lại: mã khác kể cả 3xx, 200 thiếu header GitHub, thân lạ hay quá dài, JSON hỏng, `name` khác, `value` không phải chuỗi, tầng vận chuyển ném lỗi, `--repo` khác hằng, biến cấm đọc ở mục 8). CHỈ `khop` cho giảm.

**6b. Tầng vận chuyển** — MỘT hàm `_rest_get(url, headers, han) -> (status, headers, body)`, mọi yêu cầu REST MỚI của B4 (tức các lượt đọc công tắc, không gì khác) đi qua nó, dùng `urllib` của thư viện chuẩn. Các đường git sẵn có (`_git_do`: `ls-remote` của K0, `fetch`/`ls-remote` của các lệnh khác) và `ls-remote` của tự kiểm 7a KHÔNG đổi và KHÔNG đi qua hàm này; B4 không chuyển lời gọi git nào sang `urllib` và không sửa lệnh nào khác. Luật của hàm:
- chỉ phương thức GET, không thân yêu cầu;
- KHÔNG theo chuyển hướng: phản hồi 3xx được trả nguyên mã cho tầng chính sách; đích chuyển hướng không nhận yêu cầu nào, nên `Authorization` không bao giờ tới máy chủ thứ hai (review lượt 1 đo: bộ xử lý chuyển hướng mặc định của `urllib` chép `Authorization` sang đích);
- đọc tối đa 65 537 byte thân rồi dừng;
- `han` (mặc định 15 s ở điểm gọi sản xuất) vừa là hạn mỗi thao tác socket vừa là hạn tường của CẢ lời gọi, kiểm giữa các lần đọc; quá hạn ⇒ ném lỗi;
- không thử lại; lỗi kết nối, TLS, hết hạn đều ném một lớp lỗi mà tầng chính sách đổi thành `khong_doc_duoc`;
- tôn trọng cấu hình proxy của môi trường (phiên cloud cần).

Đo 16:19:34Z 20-11-2026 từ phiên cloud soạn đặc tả (một client: `urllib`, không token): `/actions/variables` và `/actions/variables/<tên>` trả **403, không `Server`, 0 header `x-github-`**, thân *"Access to this GitHub Actions path is not permitted through this proxy."*; cùng lúc `/repos/<kho>` trả 200 có 4 header `x-github-`. Hệ quả: phiên cloud loại này ở trạng thái `khong_doc_duoc` ⇒ mọi PR thuộc (β) bị đòi G5 đủ khi `kiem-merge` chạy từ đó (giá đã chấp nhận ở Q9(b)).

### 7. Tự kiểm cây (chỉ ở bước 3 của mục 4)
- **7a.** `git ls-remote origin refs/heads/master` phải trả đúng OID của `refs/remotes/origin/master^{commit}` cục bộ. `kiem-merge` KHÔNG tự fetch; lệch hoặc không đo được ⇒ từ chối, in cách chữa (`git fetch origin master` rồi chạy lại).
- **7b.** Tệp `packet_loop.py` đang chạy phải cùng blob với `M:.claude/dev/packet_loop.py`, so bằng `git hash-object --path=.claude/dev/packet_loop.py` (để checkout CRLF không gây lệch giả) với OID của blob tại M. Một trong hai lệnh ấy (`hash-object`, `rev-parse M:<đường dẫn>`) thoát khác 0 hoặc trả đầu ra không phải một OID ⇒ không đo được ⇒ từ chối.
Hai phép này bắt chạy NHẦM cây; chúng không chống người cố ý sửa công cụ (§4 A+1 nói đúng như thế). `launcher.py` và các module khác không được kiểm.

### 8. Cờ siết và biến cấm đọc (cả hai chỉ siết)
- `--siet-g5-du` (cờ không tham số của `kiem-merge`): đòi `che_do_thuc_chay` = `du` trên đúng H cho PR đang xét, tắt cả (α) lẫn (β). Ai chạy `kiem-merge` cũng dùng được.
- Biến môi trường `PACKET_LOOP_CAM_DOC_CONG_TAC` khác rỗng ⇒ không gửi yêu cầu, công tắc ở `khong_doc_duoc`.
- Không có cờ hay biến nào theo chiều ngược lại.

### 9. Dòng chẩn đoán (stdout thật, không bị `_dk` nuốt)
- K2b in ĐÚNG MỘT dòng `LAN_G5 che_do_thuc_chay=<dich|khac> buoc=<…> lop=<duong_nhanh|bo_moi|che_do_dich|khong_giam|la|chua_tinh> master=<M|-> ket_qua=<dat|do>` khi và chỉ khi K2b đã chạy và `che_do_thuc_chay` ≠ `du`. `lop=chua_tinh` và `master=-` khi dừng trước bước 4. `buoc` là bước ra quyết định, đúng một trong sáu giá trị: `siet` (dừng ở bước 2); `tu_kiem` (dừng ở bước 3); `tinh_lai` (quyết định bởi lớp: `la`, `khong_giam` hoặc `duong_nhanh`); `bang_chung` (`che_do_dich`, điều kiện (i) sai); `audit` (`che_do_dich`, điều kiện (ii) sai); `cong_tac` (quyết định bởi trạng thái công tắc, đạt hoặc đỏ).
- Nếu K2b đã tới bước đọc công tắc — kể cả khi không gửi yêu cầu vì `--repo` khác hằng hoặc vì biến cấm đọc — thêm ĐÚNG MỘT dòng `CONG_TAC lop=… bien=… trang_thai=<khop|khong_khop|vang_hoac_khong_quyen|khong_doc_duoc> doc_luc=<UTC> updated_at=<chuỗi|-> request_id=<x-github-request-id|-> gia_tri=<JSON, tối đa 120 ký tự|->`. Nếu đạt nhờ trạng thái `khop`, thêm ĐÚNG MỘT dòng `HIEU_LUC den=<doc_luc + 30 phút>`.
- Ba loại dòng này đứng trước dòng `ĐỦ ĐIỀU KIỆN MERGE` (nếu có). K2b đạt im lặng (`du`) hoặc không chạy (K2 đỏ) ⇒ không dòng nào trong ba loại.
- `updated_at`, `request_id`, `HIEU_LUC` là dấu vết cho người đọc, KHÔNG phải vị từ. Cửa sổ 30 phút là quy trình (Q9(d)(iii)); máy không cưỡng chế.

### 10. Runbook công tắc
Tệp MỚI `ops/specs/wp1462-r1/RUNBOOK_CONG_TAC.md` (dev-side), đủ mười mục:
1. Điều kiện phải đóng ngay (§4 A+1, từ r2 §5.5): lỗi P0/P1 lọt qua một lượt giảm; bộ phân loại hoặc job gom kết luận sai; release dùng sai H; watchdog B2 báo `stale_or_missing`; audit đỏ chưa khoanh được vùng. Không khoanh được sự cố thuộc lớp nào thì đóng MỌI lớp.
2. Sau khi đóng: readback giá trị và ghi vào Issue sự cố.
3. Điều kiện bật lại, chép đúng §4 A+1: điều tra có kết luận ghi trong Issue sự cố; *full audit (`ci-dot-bien-du.yml`) `success` trên các H bị ảnh hưởng đã khoanh trong Issue ấy và trên đầu `master` lúc bật lại — khi full audit chưa mang G5 (trước PR5) thì kèm G5 đủ `success` trên chính các H ấy*; và quyết định mới bằng văn bản của chủ kho. Runbook nói rõ "chính các H ấy" gồm từng H bị ảnh hưởng VÀ đầu `master` lúc bật lại, và điều khoản G5 đủ còn hiệu lực cho tới khi `ci-dot-bien-du.yml` thật sự chạy G5 (tại nền, workflow ấy không có bước nào chạy `ops/cong_cu_test.py` — review lượt 1 đo). Lấy bằng chứng ấy không được phá trần: lượt `ci.yml` đủ trên một H không có sẵn chỉ tạo được bằng đường ở mục 8 dưới đây, mỗi lượt cần chủ kho cho phép riêng và tính vào ngân sách CI/Windows hiện hành.
4. Phiên AI không ghi biến công tắc.
5. `kiem-merge` là bước cuối trước khi đề nghị merge; phán quyết (β) dùng trong 30 phút, quá thì chạy lại; ai đổi công tắc thì mọi phán quyết xanh đang chờ merge hết hiệu lực.
6. Cách dùng `--siet-g5-du` và `PACKET_LOOP_CAM_DOC_CONG_TAC`.
7. Bảng W và bảng máy đã đo từ phép đo Q9(a); luật: W chưa đo xong hoặc còn thành viên chủ kho không chấp nhận ⇒ không đặt `CHO_PHEP`; máy chưa đo, đo thấy đọc phải bản cũ, hoặc (với máy Windows) chưa chạy các ca `cong_b4_*` ⇒ không dùng cho phán quyết (β).
8. Cách tạo một lượt G5 đủ trên H: với PR `duong_nhanh` hôm nay chỉ có dispatch `che_do=day_du`, kéo theo job Windows ⇒ mỗi lần dùng cần chủ kho cho phép riêng.
9. Readback `--workflow-jobs` phải là REST thô có trường `steps`; `kiem-merge` phải chạy từ cây trùng `origin/master` vừa fetch.
10. Rủi ro tồn dư Q9(d)(i)–(iv), chép đúng chữ §10.
Mọi mục là QUY TRÌNH của người; không cổng nào kiểm. Nghiệm thu của runbook là chủ kho duyệt theo danh sách mười mục này.

## Điều kiện tiên quyết — phép đo Q9(a)
Điều phối lập bản ghi `ops/specs/wp1462-r1/do/DO_Q9A.yaml` trên nhánh `ops/wp1462-r1` và đăng tóm tắt lên Issue #1462; lời duyệt băm của chủ kho dẫn tới bản ghi ấy. Mọi phép đo chỉ đọc; biến THỬ `TL_THU_Q9A_WP1462` do CHỦ KHO tự tạo, đổi, xoá — không phiên AI nào ghi biến. Mỗi hàng nhận một trong ba kết quả (đạt · không đạt · `khong_do_duoc`), kèm thời điểm và client đã dùng.

| Mục (§4 A+1) | Đường đo | Ai chạy | Không đo được thì |
|---|---|---|---|
| (i) Tập W | Cộng tác viên và vai trò (`gh api repos/ducthangho/tra-luat/collaborators --paginate`, một dòng, chạy trên `cmd` máy chủ kho); GitHub App đã cài cho kho và quyền Variables của từng App (trang cài đặt App); token cá nhân còn hiệu lực (fine-grained: quyền Variables; classic: scope `repo`), gồm token đứng sau phiên cloud và máy deploy — chỉ ghi TÊN, không ghi giá trị; `GITHUB_TOKEN` của các workflow (10 tệp trong `.github/workflows/` tại nền; khối `permissions:` + tài liệu, ghi rõ "theo tài liệu, chưa tự đo") | Chủ kho; điều phối đọc phần tệp workflow | Hàng `khong_do_duoc` được tính là THUỘC W (giả định xấu nhất); lệnh cấm đặt `CHO_PHEP` giữ nguyên tới khi đo xong |
| (ii) Đọc được và không dính bản đệm, trên máy sẽ chạy `kiem-merge` cho phán quyết (β) | Máy được chỉ định: máy bàn Windows của chủ kho, với một token CHỈ ĐỌC Variables đặt ở `GH_TOKEN`. Trên biến thử: đọc giá trị 1 → chủ kho đổi → đọc phải ra giá trị 2 → chủ kho xoá → đọc phải ra 404 có header GitHub. Đọc bằng `urllib` theo đúng luật mục 6 (script đo do điều phối đặt trên nhánh `ops/wp1462-r1`, ngoài PR giao nộp), không bằng client khác | Chủ kho, trên máy ấy | Máy ấy chưa dùng được cho phán quyết (β): không đọc được ⇒ chạy đủ. Phiên cloud: đã đo `khong_doc_duoc` (mục 6) |
| (iii) API trả gì cho giá trị có khoảng trắng/xuống dòng đầu-cuối | Chủ kho đặt biến thử ba giá trị như thế, đọc lại | Chủ kho, cùng máy ở (ii) | Không đổi thiết kế: so khớp vốn tuyệt đối, hai chuỗi cho phép không có khoảng trắng |
| (iv) Lượt chạy lại và lượt mở lại PR có đọc lại `vars` | `ci.yml` chưa đọc `vars` trước PR3, B4 không có workflow trong write set | — | `khong_do_duoc` ở B4; chuyển thành điều kiện đo trong đặc tả PR3 |
| (v) `vars` ở `chuan-bi` là biến mức kho, không bị environment che | Như (iv) | — | Như (iv) |
| (vi) Máy chạy `kiem-merge` chạy được bộ phân loại của `master` | Đường trực tiếp của mục 5 trên máy ấy, đối chiếu sha256 của bảng 60 dòng | Điều phối (cloud: đã đo, khớp); chủ kho (máy bàn) | Máy ấy không dùng cho phán quyết (α)/(β) |

Luật đóng băng (theo quyết định điều phối sau review lượt 1; chủ kho xác nhận khi duyệt băm): (1) đặc tả ĐƯỢC đóng băng khi hàng (i) hoặc (ii) còn `khong_do_duoc`; khi ấy lệnh cấm đặt `CHO_PHEP` giữ nguyên và mọi máy chưa đo ở trạng thái không đọc được ⇒ chạy đủ. Vì Mission r85 ghi `depends_on` "W measured before the B4 spec is frozen", Mission revision cài B4 (mục Quy trình) phải ghi rõ quyết định này thay điều kiện ấy. (2) Không kết quả nào của (i)–(vi) đổi hợp đồng mã ở trên, vì mọi nhánh không đo được đã dẫn về chạy đủ; chúng chỉ quyết định có được đặt `CHO_PHEP` không, máy nào được dùng, và nội dung runbook. (3) Kết quả nào mâu thuẫn một câu của đặc tả này ⇒ sửa thành revision mới, không sửa tại chỗ. (4) Bản ghi `DO_Q9A.yaml` phải có trước khi BẤT KỲ ai đặt `CHO_PHEP`, và là đầu vào của mục 7 runbook.

## Nghiệm thu

### Giàn thử (bắt buộc, tự nó có ca kiểm)
- **GT-1 Đồ giả chính sách.** Thay `_rest_get` (tầng 6b, chỉ phục vụ đọc công tắc) trong tiến trình bằng đồ giả GIỮ trạng thái (đổi được giá trị giữa hai lần đọc; trạng thái nằm trong TỆP để sống qua tiến trình; ghi nhật ký mọi yêu cầu: phương thức, URL, tên header). Dùng cho mọi ca của nhóm Q, C, P, O.
- **GT-2 Tầng vận chuyển THẬT.** Các ca nhóm V gọi chính hàm `_rest_get` thật tới máy chủ HTTP cục bộ trên `127.0.0.1` do ca dựng (không TLS, không proxy cho loopback, không kết nối ra ngoài); máy chủ ghi nhật ký yêu cầu nhận được. Đồ giả GT-1 KHÔNG được dùng ở nhóm V.
- **GT-3 Tiến trình con có giàn.** Một trình bọc chạy ở tiến trình MỚI: nạp `packet_loop.py` đang thử, cài đồ giả GT-1 đọc trạng thái từ tệp, rồi gọi đúng điểm vào CLI (`main`) với đối số `kiem-merge`. CHỈ trình bọc này được chạy `kiem-merge` ở tiến trình con mà không đặt biến cấm đọc.
- **GT-4 Cấm mạng thật.** Mọi lượt `kiem-merge` bằng tiến trình con KHÁC GT-3 đều đặt `PACKET_LOOP_CAM_DOC_CONG_TAC=1`. Trong các ca trong-tiến-trình và trong GT-3, mọi kết nối socket tới địa chỉ không phải loopback ném một lớp lỗi riêng và được đếm; ĐỎ khi bộ đếm ấy khác 0 ở bất kỳ ca nào. Ca tự kiểm: một lời gọi cố ý tới địa chỉ ngoài loopback phải bị chặn và được đếm.
- **GT-5 Bộ phân loại của fixture** là tệp `ops/ci_duong_nhanh.py` do ca test đặt vào `origin/master` của kho fixture. Bộ test KHÔNG đọc `ops/ci_duong_nhanh.py` thật (tệp ấy ngoài `PHU_THUOC_PACKET_LOOP`). Ngoài các bản giả tối giản cho từng vị từ, phải có MỘT **bộ sinh hai kênh** làm đúng cả hai nghĩa vụ của mục 5: nó tính điều kiện cấu trúc từ diff (theo một luật đường dẫn đơn giản của fixture), in `dk_*` trên stdout không phụ thuộc biến quyền, và ghi quyết định CI vào `GITHUB_OUTPUT` chỉ là giảm khi biến quyền (tên thay thế của fixture) mang đúng chuỗi cho phép. Tiêu chí 11 dùng bộ sinh này.
- **GT-6 Tín dụng giết.** Ca mới mang tiền tố `cong_b4_`; khẳng định đích của mỗi ca ném lớp riêng `ChotB4(AssertionError)`, định nghĩa trong tệp test và không mã sản phẩm nào ném được. Một đột biến của ma trận chỉ được tính GIẾT khi ca đích của nó đỏ bằng `ChotB4` do chính ca ấy ném; mọi kết cục khác — CLI sập, `AssertionError` thường, lỗi dựng fixture, hết hạn, ca khác đỏ — là TÍN DỤNG GIẢ. Bốn ca tự kiểm bộ phân hạng, mỗi ca một kết cục giả: đột biến làm CLI sập; đột biến làm bước dựng fixture ném; đột biến làm ca quá hạn; đột biến làm đỏ một ca KHÁC ca đích — cả bốn phải ra TÍN DỤNG GIẢ. Cách phân hạng của các đột biến cũ không đổi.
- **GT-7 Đối chứng khoẻ.** Bốn fixture chuẩn, mỗi cái đạt rc 0 với mọi K0–K7 đạt: ĐC-du (8 mảnh `du`); ĐC-α (mảnh `skipped`, M xếp `duong_nhanh`); ĐC-β (mảnh `skipped`, M in `dk_bo_moi=co`, công tắc `bo_moi` khớp); ĐC-δ (bằng chứng `dich`, M in `dk_che_do_dich=co`, có run audit `success` đúng H, công tắc `che_do_dich` khớp). Điều kiện chung của bốn fixture: `--repo` và mọi readback mang kho `ducthangho/tra-luat` (bộ dựng `_c1106` có tham số `repo`); `origin/master` của kho fixture chứa bộ phân loại giả (GT-5) và đúng blob `packet_loop.py` đang thử (cho 7b); diff của PR NẰM NGOÀI vùng M9 và không kích hoạt K6 (chỉ tệp tài liệu), nên K7 đạt mà không cần run audit hay dòng miễn — lớp do bộ phân loại giả quyết định, không do diff. Riêng ĐC-δ có thêm biến thể ĐC-δ-M9: diff chạm vùng M9, kèm run audit và dòng miễn Windows, vẫn đạt. Mỗi ca đích của ma trận là MỘT thay đổi so với đúng một fixture chuẩn (luật L-1), nên kết cục của nó chỉ do vị từ đang thử.

### Kiểm kê vị từ hợp đồng (chuẩn tắc) và luật chứng minh
Từ r5, đặc tả KHÔNG đóng băng ma trận ca–đột biến. Bốn lượt review liên tiếp tìm ra lỗ trong ma trận liệt kê sẵn (lớp `b4-predicate-mutation-proof`, lượt 1–4), nên theo quyết định checkpoint §12 của điều phối (`https://github.com/ducthangho/tra-luat/issues/1462#issuecomment-7046200733`) cách làm đổi: đặc tả đóng băng **KIỂM KÊ các vị từ độc lập** của hợp đồng và **LUẬT chứng minh**; executor dựng ma trận cụ thể và chứng minh từng cặp bằng CHẠY; reviewer mã kiểm ma trận trên H. Bảng 96 hàng của r4 bị RÚT khỏi phần chuẩn tắc.

**Luật chứng minh (áp cho MỖI vị từ trong kiểm kê):**
- **L-1 Một ca đích riêng.** Mỗi vị từ có ít nhất một ca đích `cong_b4_*` dành riêng cho nó: một fixture chuẩn (GT-7) sửa ĐÚNG MỘT chỗ làm vị từ ấy đổi giá trị, trong khi mọi vị từ khác và mọi điều kiện K0–K7 giữ nguyên kết cục (ca ghi lại kết cục K0–K7 và đòi chúng đạt, trừ vị từ Q01). Vị từ ghi "×2 chế độ" cần hai ca (một `du`, một `dich`); vị từ ghi "×4 đường thoát" cần bốn ca (trả thường · kết cục `la` · hết hạn · `SystemExit` hoặc ngoại lệ giữa chừng).
- **L-2 Khẳng định TRẠNG THÁI, không chỉ rc.** Ca đích khẳng định đúng giá trị quan sát được ghi ở cột "quan sát" (`LAN_G5.che_do_thuc_chay`, `LAN_G5.buoc`, `LAN_G5.lop`, `CONG_TAC.trang_thai`, số yêu cầu trong nhật ký, trạng thái hệ tệp/kho), cộng rc. Hai trạng thái cùng dẫn về đỏ (ví dụ `khong_khop` và `khong_doc_duoc`, `la` và `khong_giam`) phải được phân biệt bằng khẳng định ấy.
- **L-3 Một đột biến riêng.** Mỗi vị từ có một mục riêng trong bảng `MUTANTS`, gỡ hoặc đảo ĐÚNG vị từ ấy. Dưới đột biến, (mọi) ca đích của vị từ phải đổi giá trị quan sát và ném `ChotB4` (GT-6). Đột biến của vị từ này không được dùng làm bằng chứng cho vị từ khác.
- **L-4 Chứng minh bằng CHẠY.** Với từng cặp, executor chạy ca đích dưới mã đúng và dưới đột biến, rồi ghi vào `do/KET_QUA.md` một dòng: ID vị từ · tên ca · fixture nền · giá trị quan sát dưới mã đúng · tên đột biến · giá trị quan sát dưới đột biến · lớp ngoại lệ · phân hạng. Đó là ma trận của packet. Reviewer mã chạy lại độc lập trên H và đối chiếu ma trận với kiểm kê: thiếu vị từ, thiếu ca, thiếu đột biến, đột biến không đổi được giá trị quan sát, hay chỉ có tín dụng giả đều là finding.
- **L-5 Kiểm kê là SÀN.** Câu chuẩn tắc nào ở mục 3–9 chứa một điều kiện mà gỡ riêng nó ra làm đổi một giá trị quan sát được thì là một vị từ, dù có tên trong bảng dưới hay không. Executor gặp vị từ như thế thì THÊM vào ma trận (ID tiếp theo của nhóm) và báo điều phối; không vì thế mà sửa hợp đồng. Reviewer mã rà chiều ngược lại.
- **L-6 Không lối tắt.** Vị từ không chứng minh được (đột biến tương đương, không dựng được ca cô lập) ⇒ executor DỪNG và báo; không bỏ vị từ, không mượn ca khác, không đổi kỳ vọng ca cũ, không nới chốt sản xuất.

**Quan sát được** = rc; ba loại dòng chẩn đoán của mục 9; nhật ký yêu cầu của GT-1; nhật ký máy chủ của GT-2; số lượt chạy bộ phân loại và số lời git của tự kiểm (đếm trong tiến trình); trạng thái thư mục tạm và kho fixture. Ký hiệu: H = `--head`; R, J, N_k, S_DU, S_DICH như mục 3; M, C như mục 5.

**Nhóm E — bằng chứng G5 (mục 3).** Nguồn: `--workflow-runs`, `--workflow-jobs`, `--head`, `--repo`. Quan sát: dưới `--siet-g5-du`, rc và `LAN_G5.che_do_thuc_chay` (`du` ⇒ đạt, không dòng nào).

| ID | Vị từ (đúng khi) |
|---|---|
| E01 | run là ứng viên chỉ khi `path == ".github/workflows/ci.yml"` |
| E02 | … và `head_sha == H` (của RUN) |
| E03 | … và `repository.full_name == --repo` |
| E04 | R là ứng viên có `id` LỚN nhất; không có ứng viên ⇒ `khac` |
| E05 | job ∈ J chỉ khi `job.run_id == R.id` |
| E06 | job ∈ J chỉ khi `job.run_attempt == R.run_attempt` |
| E07 | với mỗi k, số job trong J tên N_k ≥ 1 |
| E08 | với mỗi k, số job trong J tên N_k ≤ 1 |
| E09 | lượng từ là MỌI k ∈ {0,…,7}: đủ tám chỉ số |
| E10 | `job.head_sha == H` (×2 chế độ) |
| E11 | `job.status == "completed"` (×2 chế độ) |
| E12 | `job.conclusion == "success"` (×2 chế độ) |
| E13 | `job.steps` có mặt và là list (×2 chế độ) |
| E14 | mọi phần tử của `steps` là object (×2 chế độ) |
| E15 | mọi phần tử của `steps` có `name` kiểu chuỗi (×2 chế độ) |
| E16 | số bước mang tên bước chính ≥ 1 (×2 chế độ) |
| E17 | số bước mang tên bước chính ≤ 1 (×2 chế độ) |
| E18 | bước chính có `status == "completed"` (×2 chế độ) |
| E19 | bước chính có `conclusion == "success"` (×2 chế độ) |
| E20 | không bước nào mang tên bước kia có `conclusion == "success"` (×2 chế độ) |
| E21 | ánh xạ chế độ: `du` ⇔ thoả E07–E20 với (chính, kia) = (S_DU, S_DICH); `dich` ⇔ thoả với (S_DICH, S_DU); còn lại `khac` |
| E22 | N_k, S_DU, S_DICH so đúng từng ký tự với hằng của mục 3 (tên lệch một ký tự không khớp) |

**Nhóm Q — thứ tự quyết định (mục 4, 8).** Nguồn: kết quả K2, cờ `--siet-g5-du`, nhóm E, lớp của nhóm C, trạng thái của nhóm P, `--dot-bien-du-*`, `--chu-kho-comment`.

| ID | Vị từ (đúng khi) | Quan sát |
|---|---|---|
| Q01 | K2b chạy ⇔ K2 không có dòng thiếu | có/không hiện vật K2b |
| Q02 | `du` ⇒ đạt và không làm gì thêm | rc 0; 0 dòng chẩn đoán; 0 lời git tự kiểm; 0 lượt phân loại; 0 yêu cầu |
| Q03 | không `du` và có cờ siết ⇒ đỏ ngay | `buoc=siet`; 0 tự kiểm; 0 lượt phân loại; 0 yêu cầu |
| Q04 | tự kiểm chạy TRƯỚC bộ phân loại; tự kiểm không đạt ⇒ đỏ | `buoc=tu_kiem`, `lop=chua_tinh`; 0 lượt phân loại; 0 yêu cầu |
| Q05 | lớp `la` ⇒ đỏ | `lop=la`, `buoc=tinh_lai`; 0 yêu cầu |
| Q06 | lớp `khong_giam` ⇒ đỏ | `lop=khong_giam`, `buoc=tinh_lai`; 0 yêu cầu |
| Q07 | lớp `duong_nhanh` ⇒ đạt, không đọc công tắc | rc 0; `lop=duong_nhanh`; 0 yêu cầu |
| Q08 | lớp `bo_moi` ⇒ đạt ⇔ trạng thái công tắc là `khop` | `buoc=cong_tac`; `CONG_TAC.trang_thai` |
| Q09 | `che_do_dich` (i): `che_do_thuc_chay == dich` | sai ⇒ `buoc=bang_chung`; 0 yêu cầu |
| Q10 | `che_do_dich` (ii): có run `ci-dot-bien-du.yml` `success` với `head_sha == H` theo phép đo của K7 nhánh run | sai ⇒ `buoc=audit`; 0 yêu cầu |
| Q11 | (ii) KHÔNG được thoả bằng dòng miễn `full_mutant_audit: <H> mien` | `buoc=audit` dù K7 đạt nhờ dòng miễn |
| Q12 | (ii) không thoả khi thiếu `--dot-bien-du-runs` hoặc `--dot-bien-du-jobs` | `buoc=audit` |
| Q13 | `che_do_dich` (iii): trạng thái công tắc của lớp là `khop` | sai ⇒ `buoc=cong_tac` |
| Q14 | yêu cầu đọc công tắc của `che_do_dich` được gửi ⇔ (i) ∧ (ii) | số yêu cầu: 0 khi (i) sai; 0 khi (i) đúng mà (ii) sai; 1 khi cả hai đúng |

**Nhóm S — tự kiểm cây (mục 7).** Nguồn: git của kho `--root`, tệp `packet_loop.py` đang chạy. Quan sát: `buoc=tu_kiem` và rc; với S07 là rc 0.

| ID | Vị từ (đúng khi) |
|---|---|
| S01 | `git ls-remote origin refs/heads/master` thoát rc 0 |
| S02 | đầu ra của nó là đúng một dòng và OID bằng OID cục bộ |
| S03 | `git rev-parse refs/remotes/origin/master^{commit}` thoát rc 0 |
| S04 | `git hash-object --path=…` trên tệp đang chạy thoát rc 0 (không đo được ⇒ từ chối) |
| S05 | `git rev-parse M:.claude/dev/packet_loop.py` thoát rc 0 (không đo được ⇒ từ chối) |
| S06 | hai OID của S04 và S05 bằng nhau |
| S07 | băm của S04 đi qua bộ lọc git theo đường dẫn (bản CRLF của đúng blob vẫn khớp) |
| S08 | tự kiểm không fetch và không đổi ref nào |

**Nhóm C — hàm chạy và đọc đầu ra (mục 5).** Nguồn: object git của kho `--root`; rc và stdout dạng byte của tiến trình con. Quan sát: `LAN_G5.lop`; với C30, C31 là thư mục tạm và kho.

| ID | Vị từ (đúng khi) |
|---|---|
| C01 | điểm gọi sản xuất truyền `cay_ma == goc == M` (không phải `--base`) |
| C02 | điểm gọi sản xuất truyền `dau == H` |
| C03 | `merge-tree` của (`goc`, `dau`) thoát rc 0; xung đột hoặc lỗi ⇒ `la` |
| C04 | C có đúng hai cha (`goc`, `dau`) theo thứ tự ấy và cây là kết quả của C03 |
| C05 | tệp được chạy là blob `cay_ma:ops/ci_duong_nhanh.py` (không phải cây làm việc, không phải H) |
| C06 | blob ấy vắng ⇒ `la` |
| C07 | cây tạm là cây của `cay_ma` (bộ phân loại đọc tệp anh em thì đọc bản tại M) |
| C08 | môi trường tiến trình con = danh sách cho phép ∪ bốn biến `CI_DUONG_NHANH_*` của mục 5 |
| C09 | tiến trình con chạy với `-I` |
| C10 | quá hạn 120 s ⇒ `la` |
| C11 | rc của tiến trình con == 0; khác ⇒ `la` |
| C12 | stdout là UTF-8 hợp lệ; không ⇒ `la` |
| C13 | dòng được tách tại byte LF |
| C14 | đúng một byte CR ở cuối dòng được bỏ (khung CRLF được nhận) |
| C15 | không byte nào khác bị cắt (CR thứ hai, dấu cách, tab thuộc giá trị) |
| C16 | khoá chỉ khớp ở đầu dòng và giá trị là phần còn lại của trọn dòng |
| C17 | số dòng `che_do` ≥ 1; không ⇒ `la` |
| C18 | số dòng `che_do` ≤ 1; không ⇒ `la` |
| C19 | giá trị `che_do` ∈ {`day_du`, `duong_nhanh`}; không ⇒ `la` |
| C20 | số dòng `dk_bo_moi` ≤ 1; không ⇒ `la` |
| C21 | giá trị `dk_bo_moi` ∈ {`co`, `khong`}; không ⇒ `la` |
| C22 | số dòng `dk_che_do_dich` ≤ 1; không ⇒ `la` |
| C23 | giá trị `dk_che_do_dich` ∈ {`co`, `khong`}; không ⇒ `la` |
| C24 | `duong_nhanh` và không khoá `dk_*` nào bằng `co` ⇒ lớp `duong_nhanh` |
| C25 | `duong_nhanh` kèm một khoá `dk_*` bằng `co` ⇒ `la` |
| C26 | `day_du`, `dk_bo_moi=co`, `dk_che_do_dich` khác `co` ⇒ `bo_moi` |
| C27 | `day_du`, `dk_che_do_dich=co`, `dk_bo_moi` khác `co` ⇒ `che_do_dich` |
| C28 | `day_du` và cả hai khoá bằng `co` ⇒ `la` |
| C29 | `day_du` và không khoá nào bằng `co` (vắng hoặc `khong`) ⇒ `khong_giam` |
| C30 | sau lượt gọi không còn thư mục tạm nào của nó (×4 đường thoát) |
| C31 | sau lượt gọi kho `--root` không thêm ref, worktree, object (×4 đường thoát) |

**Nhóm P — chính sách đọc công tắc (mục 2, 6a, 8).** Nguồn: hằng của mục 2; `--repo`; biến môi trường `GH_TOKEN` và `PACKET_LOOP_CAM_DOC_CONG_TAC`; bộ ba (mã, header, thân) do tầng 6b trả. Quan sát: `CONG_TAC.trang_thai`, nhật ký GT-1, rc.

| ID | Vị từ (đúng khi) |
|---|---|
| P01 | `--repo == "ducthangho/tra-luat"`; không ⇒ `khong_doc_duoc`, 0 yêu cầu |
| P02 | `PACKET_LOOP_CAM_DOC_CONG_TAC` rỗng hoặc vắng; không ⇒ `khong_doc_duoc`, 0 yêu cầu |
| P03 | mỗi lượt đọc gửi đúng một yêu cầu |
| P04 | URL bằng đúng hằng của mục 6a với tên biến của ĐÚNG lớp (bảng mục 2) |
| P05 | có header `Authorization: Bearer <GH_TOKEN>` ⇔ `GH_TOKEN` khác rỗng |
| P06 | giá trị `GH_TOKEN` không xuất hiện trong stdout và stderr |
| P07 | mã == 200 |
| P08 | có ít nhất một header mà tên, sau khi hạ chữ thường, bắt đầu bằng `x-github-` |
| P09 | độ dài thân ≤ 65 536 byte |
| P10 | thân giải mã được bằng UTF-8 CHẶT, và việc giải mã ấy xảy ra TRƯỚC khi phân tích JSON (thân UTF-16 hay UTF-32, có BOM hay không, không qua) |
| P11 | chuỗi đã giải mã là JSON hợp lệ |
| P12 | không object nào trong JSON có khoá trùng |
| P13 | giá trị gốc của JSON là object |
| P14 | `name` có mặt và kiểu chuỗi |
| P15 | `name` == tên biến của lớp |
| P16 | `value` có mặt và kiểu chuỗi |
| P17 | `value` == chuỗi cho phép của ĐÚNG lớp, so bằng `==` (không hạ hoa thường, không cắt khoảng trắng; chuỗi rỗng và chuỗi của lớp khác không khớp) |
| P18 | P07–P16 đúng và P17 đúng ⇒ `khop`; P07–P16 đúng và P17 sai ⇒ `khong_khop` |
| P19 | mã == 404 và P08 đúng ⇒ `vang_hoac_khong_quyen` |
| P20 | mọi trường hợp còn lại, kể cả tầng 6b ném lỗi ⇒ `khong_doc_duoc` |
| P21 | khi không `khop`, không nguồn nào khác (readback, comment, biến môi trường, tệp) được dùng để suy ra giá trị |

**Nhóm V — tầng vận chuyển (mục 6b).** Nguồn: đối số của `_rest_get`; phản hồi của máy chủ loopback (GT-2). Quan sát: nhật ký máy chủ, giá trị trả về hoặc lỗi ném.

| ID | Vị từ (đúng khi) |
|---|---|
| V01 | phương thức là GET |
| V02 | yêu cầu không có thân |
| V03 | phản hồi 3xx được trả nguyên mã; đích chuyển hướng nhận 0 yêu cầu |
| V04 | số byte thân đọc về ≤ 65 537 |
| V05 | tổng thời gian tường của lời gọi ≤ `han`; quá ⇒ ném lỗi vận chuyển |
| V06 | lỗi kết nối hoặc TLS ⇒ ném lỗi vận chuyển (không trả bộ ba giả) |
| V07 | mọi header truyền vào tới máy chủ nguyên giá trị |
| V08 | không thử lại: máy chủ nhận đúng một yêu cầu kể cả khi trả 5xx |

**Nhóm O — dòng chẩn đoán (mục 9).** Nguồn: trạng thái nội bộ của K2b. Quan sát: stdout.

| ID | Vị từ (đúng khi) |
|---|---|
| O01 | có đúng một dòng `LAN_G5` ⇔ K2b đã chạy và `che_do_thuc_chay` ≠ `du` |
| O02 | trường `che_do_thuc_chay` bằng giá trị của nhóm E |
| O03 | trường `buoc` bằng bước ra quyết định theo bảng của mục 9 |
| O04 | trường `lop` bằng lớp của nhóm C, hoặc `chua_tinh` khi dừng trước bước 4 |
| O05 | trường `master` bằng M, hoặc `-` khi dừng trước bước 4 |
| O06 | trường `ket_qua` là `dat` ⇔ K2b đạt |
| O07 | có đúng một dòng `CONG_TAC` ⇔ K2b đã tới bước đọc công tắc (kể cả khi P01 hoặc P02 chặn việc gửi) |
| O08 | `CONG_TAC.trang_thai`, `lop`, `bien` bằng trạng thái, lớp và tên biến thật |
| O09 | có đúng một dòng `HIEU_LUC` ⇔ K2b đạt nhờ trạng thái `khop`; `den` = `doc_luc` + 30 phút |
| O10 | ba loại dòng đi ra stdout thật và đứng trước dòng `ĐỦ ĐIỀU KIỆN MERGE` |

Kiểm kê có 114 vị từ (đếm HÀNG mang ID: E 22, Q 14, S 8, C 31, P 21, V 8, O 10). Số ca đích tối thiểu theo L-1 là 114 + 11 (ca thứ hai của E10–E20) + 6 (ba ca thêm cho mỗi vị từ C30, C31) = 131. Việc "chỉ `khop` mới cho giảm" không phải vị từ riêng của nhóm P: nó là Q08 và Q13.

**Ví dụ minh hoạ, KHÔNG chuẩn tắc** (để thấy hình dạng một dòng ma trận; executor không bị buộc theo đúng fixture này):
- E05: nền ĐC-α + cờ siết; run R giữ năm job bắt buộc và không có job mảnh; một run khác giữ 8 mảnh `du` cùng attempt và H. Mã đúng: rc 12, `che_do_thuc_chay=khac`. Đột biến "bỏ so `run_id` khi lập J": rc 0.
- P10: nền ĐC-β; thân là đúng JSON hợp lệ của biến nhưng mã hoá UTF-16 có BOM. Mã đúng: `trang_thai=khong_doc_duoc`. Đột biến "đưa thẳng byte cho bộ phân tích JSON": `trang_thai=khop`.
- Q14: nền ĐC-δ; run audit mang `head_sha` khác H. Mã đúng: `buoc=audit`, 0 yêu cầu. Đột biến "gửi yêu cầu ngay sau (i)": 1 yêu cầu.
- C30 (đường hết hạn): bộ phân loại giả treo quá hạn. Mã đúng: thư mục tạm của ca rỗng sau lượt gọi. Đột biến "chỉ dọn ở đường trả thường": còn thư mục.

### Tiêu chí
1. **A/B không đổi hành vi (B-2), dựng trong MỘT lệnh.** Base = merge-base của H với `origin/master`. Tập fixture = MỌI ca hiện có đi qua bộ dựng `_c1106` (tại nền: 119 dòng chứa `_c1106_ca(` và 5 dòng chứa `_c1106(`, đếm DÒNG bằng `grep -c`, 16:10Z 20-11-2026; executor đếm lại theo CA tại base và báo con số cùng danh sách tên). Bộ dựng dùng chung chỉ được thêm bằng chứng `du` mặc định (8 job mảnh có bước S_DU `success`, đúng run/attempt/head), theo tiền lệ K7 của #1120. Mỗi fixture dựng MỘT lần, hai vế (`packet_loop.py` của base và của head, mỗi vế kèm `launcher.py` của chính nó) chạy trên cùng thư mục fixture. ĐỎ khi: một ca có rc, stdout hoặc stderr lệch một byte; hoặc số ca được so nhỏ hơn số ca đếm tại base.
2. **A/B bề mặt đổi, với phép chiếu có định nghĩa và phân hoạch ĐỦ.** Cùng tập fixture của tiêu chí 1 ở HÌNH DẠNG CŨ (không job mảnh). Phép chiếu P bỏ khỏi đầu ra của head ĐÚNG các hiện vật của K2b: dòng stdout bắt đầu bằng `LAN_G5 `, `CONG_TAC ` hoặc `HIEU_LUC `; dòng stderr `THIẾU  K2b làn G5: …`; và tên `K2b làn G5` cùng dấu phân cách của nó trong dòng tổng kết. Mỗi ca thuộc ĐÚNG MỘT trong bốn lớp, xếp theo đầu ra của BASE bằng hai dấu hiệu đọc được (dòng stdout `ĐỦ ĐIỀU KIỆN MERGE trên …` và dòng tổng kết stderr `CHƯA ĐỦ ĐIỀU KIỆN MERGE: thiếu …`), không suy "K2 đạt" từ việc vắng một dòng: (z) base KHÔNG có cả hai dòng ấy — lệnh thoát trước khi chạy điều kiện nào, K2 `not_run` (tại nền có ít nhất bốn ca: `cong_c_k1_anchor`, `cong_c_k1_yaml_hong`, `cong_c_k1_khoa_trung`, `cong_c_k1_tag_hong`, đều rc 2 vì lease hỏng; review lượt 3 đo) ⇒ head trùng byte với base ở rc, stdout, stderr, KHÔNG qua P, không hiện vật K2b nào; (a) base có dòng tổng kết và dòng ấy nêu `K2 CI` ⇒ head trùng byte với base, KHÔNG qua P; (b) base có dòng tổng kết và dòng ấy không nêu `K2 CI` ⇒ rc bằng nhau, P(head) trùng byte với base, và head có đúng một dòng `LAN_G5`, đúng một dòng `THIẾU` của K2b; (c) base có dòng `ĐỦ ĐIỀU KIỆN MERGE` ⇒ head rc 12, stdout là đúng một dòng `LAN_G5`, stderr là đúng dòng `THIẾU` của K2b và dòng tổng kết chỉ nêu K2b. Ca có cả hai dòng, hoặc không xếp được, ⇒ ĐỎ. Executor báo số ca từng lớp và tên các ca lớp (z); bốn ca nêu trên phải nằm trong (z). ĐỎ khi có lệch nào ngoài bốn khuôn ấy, hoặc có ca base đỏ mà head đạt (B-1). Bộ so có tự kiểm chạy cùng lệnh, ĐỎ nếu một ca tự kiểm sai: CHẤP NHẬN đúng hiện vật dự định ở (b) và (c), và đầu ra không đổi ở (z) và (a); TỪ CHỐI khi head thêm một dòng stdout không thuộc ba loại, khi có hai dòng `LAN_G5`, khi dòng `THIẾU` của một điều kiện khác đổi một ký tự, khi rc lệch ở (b), khi ca lớp (a) có bất kỳ hiện vật K2b nào, khi ca lớp (z) có thêm dòng `LAN_G5` hoặc dòng `THIẾU` của K2b, và khi thông báo lỗi lease của một ca lớp (z) đổi một ký tự. Thứ tự kiểm đối số và lease của `cmd_kiem_merge` không đổi: K2b không chạy trước chúng.
3. **Mọi ca cũ giữ kỳ vọng.** Không ca nào của `packet_loop_test.py` bị xoá hay đổi rc/lý do kỳ vọng; thay đổi duy nhất ở phần cũ là bộ dựng dùng chung ở tiêu chí 1 và phần mở rộng bộ phân hạng ở GT-6. ĐỎ khi diff của tệp test chạm kỳ vọng của một ca cũ.
4. **Ma trận vị từ.** Executor nộp trong `do/KET_QUA.md` ma trận theo luật L-1…L-6, phủ MỌI vị từ của kiểm kê (114 hàng tại r5) và mọi vị từ thêm theo L-5. ĐỎ khi: một vị từ không có ca đích riêng hoặc không có đột biến riêng; một ca đích chỉ khẳng định rc mà không khẳng định giá trị quan sát của vị từ (L-2); đột biến không đổi được giá trị quan sát của ca đích; tín dụng chỉ là tín dụng giả (GT-6); hoặc thiếu ca cho một chế độ / một đường thoát mà vị từ đòi. Tín dụng của một đột biến chỉ tính trên (các) ca đích của vị từ ấy; ca khác đỏ theo là bán kính, không tính và không bị cấm. Reviewer mã chạy lại độc lập trên H và đối chiếu ma trận với kiểm kê. Bảng đột biến của `packet_loop_test.py` KHÔNG thuộc `ci-dot-bien-du.yml`; nó chạy ở `packet-loop-dot-bien.yml` theo lịch sau merge, đọc kết quả lượt đầu tiên sau merge là việc ghi ở M8, không chặn merge.
5. **Ca cấu trúc `ci.yml`, bền qua PR6.** Một hàm kiểm nhận văn bản YAML và trả đạt/không: trong job `gate-cong-cu`, ma trận `manh` đúng 0..7, số bước tên S_DU = 1, số bước tên S_DICH ∈ {0, 1}. Chạy trên sáu YAML tổng hợp: chỉ bước đủ (hình dạng hôm nay) ⇒ đạt; bước đủ + một bước đích (hình dạng PR6 phải có) ⇒ đạt; không bước đủ ⇒ không đạt; hai bước đủ ⇒ không đạt; hai bước đích ⇒ không đạt; ma trận thiếu mảnh 7 ⇒ không đạt. Và chạy trên `.github/workflows/ci.yml` THẬT ⇒ đạt; trong kho có `.git` mà thiếu tệp ⇒ ĐỎ, không bỏ qua. Ca này KHÔNG cấm bước đích: PR6 thêm bước ấy mà không phải sửa `packet_loop_test.py`.
6. **Tiến trình mới (GT-3), bốn lượt nối tiếp trên cùng tệp trạng thái của ĐC-β:** đúng chuỗi ⇒ ĐẠT; đổi giá trị ⇒ ĐỎ; xoá biến ⇒ ĐỎ; đặt lại đúng chuỗi ⇒ ĐẠT. Mỗi lượt là một tiến trình riêng; nhật ký ghi đúng một yêu cầu mỗi lượt; bộ đếm kết nối ngoài loopback bằng 0. Đối chứng: cùng ĐC-β chạy bằng tiến trình con THƯỜNG (có biến cấm, GT-4) ⇒ ĐỎ với 0 yêu cầu.
7. **Nằm im trước PR3.** Với bộ phân loại fixture chỉ in `che_do` và `packet_loop` (hình dạng hôm nay, không khoá `dk_*`), mọi ca ghi 0 yêu cầu REST: ĐC-α đạt với `lop=duong_nhanh`, và fixture mảnh `skipped` mà M in `day_du` thì đỏ với `lop=khong_giam`.
8. **Phát lại ngoại tuyến trên lịch sử thật (ngoài bộ ca, lệnh con của `ops/specs/wp1462-r1/do/do_b4.py`).** Mục đích hẹp: chứng minh HÀM CHẠY của mục 5 (dựng commit hợp, cây tạm, môi trường, đọc đầu ra) cho cùng kết quả với đường trực tiếp trên dữ liệu thật; nó KHÔNG đi qua tự kiểm cây, KHÔNG dùng M sống và không thay các ca fixture của K2b. Định nghĩa: tập = 60 merge của `git log --first-parent --merges -60 0f9aa2a2cc697129e1f5be72feddf60986286865`; với mỗi merge gọi hàm chạy với `cay_ma` = `0f9aa2a2cc697129e1f5be72feddf60986286865` (blob bộ phân loại `e43f514c`), `goc` = cha một, `dau` = cha hai, đồ giả GT-1 đếm yêu cầu. Kỳ vọng độc lập: bảng 60 dòng sinh bằng đường trực tiếp (merge commit thật, không qua hàm chạy), executor sinh lại và sha256 phải bằng `aa932267e766cf3f6e242f35febe3692909f3e909cb510177ba83d780bfc849a`. ĐẠT khi và chỉ khi: 60/60 lượt của hàm chạy trả đúng lớp tương ứng từng dòng (`duong_nhanh` ⇒ `duong_nhanh`; `day_du` ⇒ `khong_giam`), tức đúng 18 và 42; 0 lượt `la`; 0 yêu cầu REST; kho không thêm ref, worktree, object. Thêm phép hồi quy khung dòng trên BỘ SINH THẬT: với cùng 60 bộ ba, lấy stdout dạng byte của bộ phân loại thật theo hai cách — (a) như nó in trên Linux (LF); (b) chạy `main` của chính blob ấy với stdout là một `TextIOWrapper` đặt `newline="\r\n"` (mô phỏng lớp dịch của Windows) — rồi đưa cả hai vào hàm đọc đầu ra của sản xuất; 60/60 ở (b) phải ra đúng lớp như (a). Đối chứng hỏng: chèn một CR vào GIỮA giá trị `che_do` của một lượt ⇒ hàm phải trả `la`. Lệch dù một dòng ⇒ ĐỎ: executor dừng và báo OID, không tự giải thích cho qua. Đây là mô phỏng; chạy trên Windows thật vẫn là điều kiện riêng trước khi dùng máy ấy cho (α)/(β) (mục Quy trình).
9. **Cổng kho:** `packet_loop_test` N/N với hai số BẰNG NHAU (CI: 16 mảnh + job gom đạt; N sau = N trước + số ca mới, báo cả ba số; sổ ca tại nền: 1582 ca, review lượt 1 đo); Ruff F delta = 0 so với base trên hai tệp `.py` của write set và 0 lỗi F trên tệp `.py` mới (nền Ruff của hai tệp CHƯA ĐO ở lượt soạn đặc tả và ở review lượt 1: cả hai máy không có Ruff); `doctrine-scan` và `adr-song` rc 0; CI PR Ubuntu xanh trên H; một lượt `ci-dot-bien-du.yml` `success` trên đúng H với mọi job `success` (K7, vì diff chạm `.claude/dev/**`); `git diff --numstat` của đúng H so base, đo trước mỗi lần đẩy và mỗi lần xin review, nằm trong trần đang hiệu lực theo mục "Kích thước" (trần `ADR-0053`, hoặc `tran_moi` của khối `nang_tran` đã được chủ kho duyệt bằng số đo); đọc lượt push sau merge theo nhãn job. Báo delta thời gian của `gate-packet-loop-manh` (tổng 16 mảnh) trước/sau.
10. **Runbook:** tệp ở mục 10 có đủ mười mục, trong đó mục 3 có nguyên văn điều khoản G5 đủ trước PR5; nghiệm thu là lời duyệt của chủ kho theo danh sách ấy, không có ca máy.

11. **Tích hợp hai kênh (điều kiện cấu trúc khác quyết định CI), với bộ sinh hai kênh của GT-5, cho CẢ `bo_moi` lẫn `che_do_dich`.** Trên CÙNG một diff đủ điều kiện cấu trúc: (a) gọi bộ sinh kiểu CI (có `GITHUB_OUTPUT`) với biến quyền vắng, rỗng, sai một ký tự ⇒ tệp output ghi quyết định chạy đủ, còn stdout vẫn in `dk_<lớp>=co`; với biến quyền đúng chuỗi ⇒ output ghi quyết định giảm; (b) lượt `kiem-merge` trên fixture ấy — không truyền biến quyền nào — nhận ra đúng lớp (`LAN_G5.lop`), rồi ĐẠT khi và chỉ khi công tắc sống `khop`: thử đủ bốn trạng thái của mục 6a, ba trạng thái kia phải ĐỎ với đúng `CONG_TAC.trang_thai`; (c) người gọi `kiem-merge` đặt sẵn biến quyền đúng chuỗi trong môi trường của mình trong khi công tắc sống KHÔNG `khop` ⇒ vẫn ĐỎ (biến của người gọi không tới tiến trình con và không thay được lời GET); (d) trên một diff KHÔNG đủ điều kiện cấu trúc, công tắc sống `khop` ⇒ ĐỎ với `lop=khong_giam` và 0 yêu cầu. ĐỎ khi bất kỳ ô nào của (a)–(d) lệch, ở bất kỳ lớp nào trong hai lớp.


## Write set
- Trên nhánh `ops/wp1462-r1`, KHÔNG thuộc PR giao nộp (hiện vật của điều phối): `ops/specs/wp1462-r1/SPEC.md`, `ops/leases/wp1462-*.yaml`, `ops/specs/wp1462-r1/do/DO_Q9A.yaml` và script đo Q9(a).
- **PR giao nộp, đúng NĂM tệp:**
  1. `.claude/dev/packet_loop.py` (gồm câu ranh giới ở docstring đầu tệp: nay có lời GET chỉ đọc cho công tắc, và đọc `GH_TOKEN`)
  2. `.claude/dev/packet_loop_test.py`
  3. `ops/specs/wp1462-r1/RUNBOOK_CONG_TAC.md`
  4. `ops/specs/wp1462-r1/do/do_b4.py` — MỘT script, ba lệnh con: A/B của tiêu chí 1–2 kèm tự kiểm bộ so; phát lại và hồi quy khung dòng của tiêu chí 8 (tự sinh bảng kỳ vọng rồi đối chiếu sha256, không commit bảng); in bảng kết quả. Không phải `*_test.py`.
  5. `ops/specs/wp1462-r1/do/KET_QUA.md` — kết quả đo của executor: A/B, phát lại, MA TRẬN vị từ → ca đích → đột biến của tiêu chí 4, numstat, delta thời gian.

Không tệp thứ sáu. Cần tệp thứ sáu ⇒ DỪNG và báo. Đã rà (16:10Z 20-11-2026): chuỗi "K0–K7" có ở `docs/adr/0060-dieu-kien-merge-va-moc-ready.md`:158, `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md`:159, `docs/PROTOCOL_DA_PHIEN.md`:1643, `.claude/skills/land-packets/SKILL.md`:64 và dòng trợ giúp của lệnh; điều kiện mới mang tên `K2b` nên bốn tệp tài liệu ấy vẫn đúng chữ và KHÔNG vào write set. Không tài liệu nào liệt kê cờ của `kiem-merge` ngoài `--dot-bien-du-*` ở adapter `land-packets`; cờ `--siet-g5-du` được ghi ở trợ giúp lệnh và runbook. `.claude/dev/packet_loop_test_manh.py` chia mảnh theo thứ tự đăng ký, không có bảng trọng số ⇒ không cần sửa. `ops/ci_duong_nhanh.py`, `.github/workflows/ci.yml`, `.claude/dev/ci_dang_ky_test.py` KHÔNG thuộc B4 (phần đọc `vars` ở `chuan-bi` thuộc PR3). Nợ có tên, không làm ở đây: adapter `land-packets` chưa trỏ tới runbook và chưa nói "chạy `kiem-merge` từ cây `origin/master`".

## Kích thước
Quyết định của chủ kho (chat 20-11-2026, ghi ở Mission r86): đặc tả này KHÔNG mang khối `nang_tran` ước lượng (khối của r3 đã rút), vì `ADR-0053` đòi `can_cu` kèm số đo `git diff --numstat`.

- **Trần** là trần mặc định của lớp `sensitive` theo `ADR-0053`: ≤ 6 tệp và ≤ 450 dòng thêm theo `git diff --numstat`. Dòng `tran_kich_thuoc_sensitive` ở đầu tệp được GIỮ: theo mục "Hiệu lực" của ADR ấy, thiếu dòng khai thì trần lùi về ≤ 3 tệp / ≤ 300 dòng thêm, mà PR giao nộp có 5 tệp. Lease và Mission revision cài B4 ghi đúng cặp 6 tệp / 450 dòng thêm, không kèm ngoại lệ.
- **Trần áp vào CÁI GÌ.** Theo `ADR-0044` — luật mà `ADR-0053` chỉ thay một cặp số — "vượt một trong hai ngưỡng thì dừng TRƯỚC review". Vậy đối tượng bị trần là **ứng viên giao nộp**: diff base..H của đúng commit H sắp được ĐẨY hoặc sắp được đưa đi REVIEW (review mã Codex, audit exact-H của chủ kho, connector). Bản nháp trong cây làm việc và commit cục bộ chưa đẩy, chưa xin review KHÔNG phải ứng viên và không bị trần. Câu của Mission r86 ("executor measures numstat and stops before exceeding") được đọc theo đúng nghĩa ấy: dừng trước khi một ứng viên vượt trần được giao nộp; đây là quyết định checkpoint §12 của điều phối (`https://github.com/ducthangho/tra-luat/issues/1462#issuecomment-7046200733`), chủ kho xác nhận khi duyệt băm.
- **Đo ở đâu.** Trước MỖI lần đẩy H và trước MỖI lần xin review hay audit, executor đo `git diff --numstat <base> <H>` trên đúng năm tệp giao nộp và ghi số đo cùng hai SHA vào `do/KET_QUA.md`. Số tệp ≤ 6 và tổng dòng thêm ≤ 450 ⇒ được đẩy và xin review. Bằng đúng trần (450) là TRONG trần.
- **Vượt ⇒ DỪNG TRƯỚC review.** Số đo của H vượt trần (ví dụ 451 dòng thêm, hoặc tệp thứ bảy) ⇒ executor KHÔNG đẩy H, KHÔNG xin review hay audit nào, không cắt ca, đột biến hay bằng chứng để vừa trần, không tách PR. Nó nộp cho điều phối: numstat từng tệp của H, SHA của H và của base. Không ứng viên vượt trần nào tới tay reviewer hay lên remote.
- **Xin nâng bằng số đo.** Điều phối soạn khối `nang_tran` đủ bốn trường của `ADR-0053` — `ai_nang` (chủ kho), `can_cu` (vì sao không tách được, kèm NGUYÊN numstat đã đo và hai SHA), `tran_cu` (6 tệp / 450 dòng thêm), `tran_moi` — và trình chủ kho. Khối chỉ có hiệu lực khi chủ kho duyệt và nó đã được cài vào đặc tả (một revision chỉ thêm khối ấy, băm mới do chủ kho duyệt), vào Mission revision tương ứng và vào lease. Sau đó cùng luật áp với `tran_moi`: H có số đo ≤ `tran_moi` thì được đẩy và review; lớn hơn thì DỪNG TRƯỚC review lần nữa.
- **Điều đặc tả này KHÔNG khẳng định.** Ước lượng của tác giả (không phải số đo, không có thẩm quyền nào): 114 vị từ với ít nhất 131 ca đích, 114 đột biến và giàn thử khó nằm trong 450 dòng thêm, nên nhiều khả năng luật dừng sẽ được dùng ở lần đo đầu tiên. Con số ấy không cấp trước ngoại lệ nào.
- Không cổng máy nào canh trần này (`ADR-0044` và `ADR-0053` đều được §20 ghi là 0 cổng); executor, người cấp lease và reviewer đo bằng tay.

## Quy trình và quyền
- **Trước lease — ba bước tách rời, đúng thứ tự.** (1) Chủ kho duyệt BĂM đặc tả, sau khi review đặc tả Codex không còn finding P0–P3. (2) Một **Mission revision** riêng do điều phối soạn và chủ kho duyệt được CÀI: nó nhận Packet #1462 vào thi công và ràng buộc số packet, revision và generation, đúng băm đặc tả đã duyệt, base thi công, write set, provider và bề mặt chạy của executor và reviewer, các trần ở gạch dưới, trần kích thước mặc định của mục Kích thước (KHÔNG kèm khối `nang_tran` nào ở bước này), và quyết định về `depends_on` ở mục phép đo. (3) Sau đó mới cấp lease; trước khi cấp chạy `ai-dang-giu` trên mọi ref cho hai tệp `.claude/dev/` và thư mục đặc tả. Duyệt băm KHÔNG tự nó trao quyền thi công: Mission r85 chỉ nhận B4 ở mức soạn đặc tả (`admitted_spec_drafting`).
- **Hai bộ trần tách nhau.** Soạn đặc tả: Mission r85 (`per_new_packet`) cho tác giả 3 lượt, review đặc tả Codex 4 lượt; chủ kho nâng mỗi trục thêm 2 cho B4 (chat 20-11-2026, điều phối ghi vào Mission r86) ⇒ 5 và 6. Tại lúc soạn r5 đã dùng 5/5 và 4/6: r5 là lượt tác giả CUỐI trong trần. Cả quyết định nâng lẫn bộ đếm đều theo thông báo của điều phối, không phải số tác giả tự đo; mọi revision tiếp theo của đặc tả này, kể cả revision chỉ thêm khối `nang_tran` theo mục "Kích thước", cần chủ kho quyết về trần tác giả trước. Thi công: attempts 3; review mã Codex 3; CI PR Ubuntu 3; `ci-dot-bien-du.yml` 1; connector 2; CI rerun 1; Windows CI 0. Trước MỖI lời gọi, điều phối đọc lại bộ đếm đã dùng / đã giữ chỗ / trần của đúng trục ấy; chạm trần thì dừng và hỏi.
- Executor: Claude Code (Fable 5.2), phiên cloud riêng. Reviewer: Codex service gpt-6-astra, mức xhigh, phiên độc lập, chỉ đọc; reviewer CHẠY ca và đột biến có sẵn, đối chiếu ma trận trong `do/KET_QUA.md` với kiểm kê vị từ trên đúng H (luật L-4, L-5); hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời cho điều phối.
- Chủ kho tự audit exact-H trước LẦN ĐẨY ĐẦU của H; điều phối không ký thay. Merge do chủ kho bấm.
- **Windows:** diff chạm `.claude/dev/` nên K6 xếp `required`; khung dòng CRLF của bộ phân loại (mục 5) mới chỉ được mô phỏng trên Linux; theo quy tắc thường trực "không Windows CI" và r85 (chạy Windows tại chỗ chỉ cho B3), packet này MIỄN Windows bằng dòng miễn của chủ kho. Máy đọc công tắc được chỉ định là máy bàn Windows của chủ kho; nó chỉ được dùng cho phán quyết (β) sau khi phép đo (ii) đạt VÀ các ca `cong_b4_*` đã chạy xanh tại chỗ trên máy ấy dưới một thẩm quyền riêng. Trước PR3 không phán quyết (β) nào tồn tại, nên điều này không chặn B4; phán quyết (α) chạy được từ phiên cloud Linux.
- Trước khi đẩy H: cập nhật nhánh lên `master` mới nhất và đo lại làn; PR này là `day_du`. Lượt `kiem-merge` cho chính PR này chạy bằng mã của `master` TRƯỚC B4.
- Không ai đặt `CHO_PHEP` trong packet này. Sau khi land: B4 nằm im cho tới khi PR3 land VÀ chủ kho tự đặt biến sau khi Q9(a) đạt.

## Chỗ khác chữ kế hoạch (để review soi)
- **D-1 Phạm vi tự kiểm cây.** §4 A+1 viết "lệch ⇒ từ chối" không kèm phạm vi. Đặc tả này chỉ chạy tự kiểm khi quyết định cần tính lại bằng mã `master` (bước 3), để B-2 đúng từng byte và để bộ ca hiện có không phải mang blob của công cụ. Điều phối giữ lựa chọn này sau review lượt 1.
- **D-2 Tên điều kiện** là `K2b` (con của K2), không phải `K8`, để không sửa hai ADR, protocol và adapter. Điều phối giữ.
- **D-3 Chốt thêm ngoài chữ kế hoạch, đều chỉ siết:** K2b tự ràng buộc run/attempt/head của job mảnh; `--repo` phải bằng hằng kho mới đọc công tắc; lớp `che_do_dich` đòi bằng chứng `dich` trên H; biến cấm đọc; không theo chuyển hướng; trần 65 536 byte; hạn tường.
- **D-4 Runbook nằm trong `ops/specs/wp1462-r1/`** thay vì `docs/`, theo write set của Mission r85.
- **D-5 (iv) và (v)** của phép đo không đo được trong B4 và chuyển sang đặc tả PR3.
- **D-7 Điều kiện cấu trúc tách khỏi quyết định CI.** §4 A+1 nói `chuan-bi` truyền `vars` cho bộ phân loại và B4 đóng băng "đầu ra của bộ phân loại (giá trị nào thuộc lớp giảm nào)" mà không nói đầu ra ấy đã qua công tắc hay chưa. Đặc tả này đọc như sau và đóng băng cách đọc ấy (mục 5): stdout mang ĐIỀU KIỆN CẤU TRÚC `dk_*`, không phụ thuộc công tắc; quyết định CI qua `GITHUB_OUTPUT` mới bị công tắc chặn. Chủ kho xác nhận khi duyệt băm.
- **D-8 Trần kích thước áp cho ứng viên giao nộp.** Câu "stops before exceeding" của Mission r86 được đọc theo `ADR-0044` ("vượt ngưỡng thì dừng TRƯỚC review"), theo quyết định checkpoint §12 của điều phối; xem mục "Kích thước".
- **D-6 Đóng băng khi W chưa đo xong** (luật đóng băng (1)): khác chữ §7 "phép đo chuẩn bị → Q9 → đóng băng"; lệnh cấm đặt `CHO_PHEP` là thứ giữ an toàn, và Mission revision cài B4 phải ghi quyết định này.

## Thay đổi
### r2 so với r1 (review lượt 1)
| Finding (review lượt 1) | Sửa ở r2 |
|---|---|
| B4-S01 phép so A/B bề mặt đổi cấm chính dòng chẩn đoán bắt buộc | Mục 9 định nghĩa chính xác khi nào có dòng `LAN_G5`/`CONG_TAC`/`HIEU_LUC` và số lượng; tiêu chí 2 dùng phép chiếu P với ba lớp ca và tự kiểm bộ so (chấp nhận hiện vật dự định, từ chối trôi đầu ra); hàng O01 |
| B4-S02 ca cấu trúc cấm bước mà PR6 phải thêm | Tiêu chí 5: hàm kiểm chấp nhận cả hai hình dạng hợp lệ (0 hoặc 1 bước đích), từ chối thiếu/trùng/mơ hồ, thử trên sáu YAML tổng hợp và tệp thật; "chưa có bước đích" chỉ còn là quan sát ở mục 3 |
| B4-S03 đồ giả thay cả tầng vận chuyển nên chốt vận chuyển không được thử | Mục 6 tách 6a chính sách / 6b vận chuyển; GT-2 và nhóm X01–X06 gọi `_rest_get` THẬT tới máy chủ loopback (phương thức, không chuyển hướng và không chuyển `Authorization`, trần byte, hạn tường, lỗi kết nối, header); đột biến vận chuyển gắn vào ca nhóm X |
| B4-S04 ca tiến trình mới mâu thuẫn với biến cấm bắt buộc | GT-3 (trình bọc tiến trình con cài đồ giả trạng thái-trong-tệp, miễn DUY NHẤT), GT-4 (biến cấm cho mọi tiến trình con khác + chặn và đếm kết nối ngoài loopback); tiêu chí 6 có cả lượt đạt, lượt đỏ và đối chứng có biến cấm |
| B4-S05 28 đột biến không phủ hết chốt, thiếu run/attempt/head | Mục 3 để K2b tự ràng buộc R, A, J, H; danh sách 28 mục thay bằng bảng chốt → phản chứng → đột biến 72 hàng (G, Q, T, R, D, X, O, H); GT-6 lớp `ChotB4` và bốn ca tự kiểm tín dụng giả; GT-7 bốn đối chứng khoẻ |
| B4-S06 phát lại lịch sử không khớp đầu vào sản xuất, không có tiêu chí đạt thực chất | Mục 5 tách hàm chạy khỏi điểm gọi sản xuất và ghi rõ số đo lúc soạn là "đường trực tiếp"; tiêu chí 8 định nghĩa tập, OID mã, `goc`/`dau`, hàm được thử, bảng kỳ vọng độc lập có sha256, điều kiện đạt 18/42/0 `la`/0 REST, và nói rõ nó không đi qua tự kiểm cây; tiêu chí 7 giữ phần "nằm im" bằng fixture |
| B4-S07 runbook bỏ điều khoản G5 đủ trước PR5 | Mục 10 điểm 3 chép nguyên văn điều khoản, nêu phạm vi (từng H bị ảnh hưởng và đầu `master`), thời hạn hiệu lực và ràng buộc ngân sách; tiêu chí 10 kiểm điểm ấy |
| B4-S08 thiếu Mission revision trước lease | Mục Quy trình: ba bước duyệt băm → cài Mission revision (liệt kê thứ nó ràng buộc) → lease; tách trần soạn đặc tả 3/4 khỏi trần thi công 3/3; đọc lại bộ đếm trước mỗi lời gọi |

Thay đổi ngoài chữ của tám finding, nêu để lượt review sau soi: thứ tự bước 1–2 của mục 4 đảo lại (xét `du` trước cờ siết; kết quả không đổi, B-2 nay đúng cả khi có cờ); luật đóng băng và máy đọc công tắc theo quyết định điều phối (D-6, hàng (ii)); B-4 thêm "commit M".

### r3 so với r2 (review lượt 2)
| Finding (review lượt 2) | Sửa ở r3 |
|---|---|
| B4-S05 (đóng một phần) ma trận còn hàng mà đột biến không đổi được kết cục ca đích, fixture không cô lập K2b, thiếu chốt H2/bộ đọc | Bảng viết lại: 88 hàng, mỗi hàng ĐÚNG một ca đích và một đột biến, ghi cả kết cục dưới mã đúng lẫn dưới đột biến; nhóm G đo `du` qua cờ siết, bằng chứng sai chỗ dựng trên ĐC-α; tách R01/R02, R09/R10; đổi đột biến R12, R13; D02–D04 có tiền đề M9/dòng miễn rõ (GT-7, ĐC-δ-M9); thêm G12, G13, G19, G21, T08, T12, T13; mục 3 buộc một hàm kiểm mảnh chung và mục 5 một bộ đọc khoá chung, nên hàng `dich` và khoá tuỳ chọn là ca đích thứ hai của cùng đột biến; tiêu chí 4 đòi kết cục dưới cả hai phía và lệnh DỪNG khi gặp đột biến tương đương; danh sách hàng bị bỏ/đổi kèm lý do nằm ngay dưới bảng |
| B4-S09 thiếu luật khung dòng tương thích Windows | Mục 5 "Khung dòng": đọc stdout dạng byte, tách tại LF, bỏ ĐÚNG MỘT CR cuối mỗi dòng trên mọi nền, không cắt gì khác; hàng T09 (dấu cách), T10 (hai CR), T11 (CRLF được nhận); tiêu chí 8 thêm hồi quy trên bộ sinh thật với LF và CRLF mô phỏng, kèm đối chứng CR giữa giá trị; chạy Windows thật vẫn là điều kiện riêng |
| B4-S10 vượt trần kích thước `sensitive` mà không khai | Dòng khai `tran_kich_thuoc_sensitive: ADR-0053@8ab10079…` ở đầu tệp (ba phép đo OID ghi ở đoạn Trạng thái); Write set chốt PR giao nộp đúng 5 tệp; mục "Kích thước và `nang_tran`" có khối bốn trường, ước lượng theo thành phần, đo numstat trước mỗi review mã, dừng khi vượt, chép vào Mission revision và lease; tiêu chí 9 kiểm numstat |
| B4-S11 `_rest_get` bị viết thành mọi vào/ra mạng | Mục 6b: chỉ các yêu cầu REST mới của B4 (đọc công tắc); đường git sẵn có và `ls-remote` của 7a không đổi, không qua `urllib`; GT-1 nói rõ phạm vi |

Thay đổi ngoài chữ của bốn finding: hai script A/B và phát lại của r2 gộp thành một tệp `do/do_b4.py`, bảng kỳ vọng 60 dòng không commit mà sinh lại rồi đối chiếu sha256 (để giữ 5 tệp); bộ đếm trần soạn đặc tả cập nhật (tác giả 3/3, review 2/4).

### r4 so với r3 (review lượt 3)
| Finding (review lượt 3) | Sửa ở r4 |
|---|---|
| B4-S05 (đóng một phần) thiếu ca/đột biến riêng cho việc lọc J theo `run_id` của job | Hàng G24 theo đúng bố cục reviewer dựng (run đúng không có job mảnh, run khác giữ 8 mảnh `du` cùng attempt và H, dưới cờ siết); ghi chú dưới bảng tách "chọn R" khỏi "lập J". Rà cùng kiểu mọi chốt ghép của mục 3–6a, thêm T22, T25, R23, R24, D06 và hai ca đích thứ hai T23, T24. Bảng: 96 hàng, 85 đột biến |
| B4-S10 (đóng một phần) khối `nang_tran` chỉ có ước lượng | Theo quyết định chủ kho: RÚT khối ước lượng; mục "Kích thước" viết lại — lease dưới trần mặc định `ADR-0053` (giữ dòng khai vì thiếu nó trần lùi về 3 tệp), executor đo numstat khi thi công, sẽ vượt thì DỪNG, điều phối xin `nang_tran` bằng numstat đã đo, chủ kho duyệt, rồi mới vào đặc tả/Mission/lease; tiêu chí 9 và mục Quy trình sửa theo |
| B4-S12 tiêu chí 2 không phân hoạch đủ: ca bị từ chối trước K2 | Tiêu chí 2: bốn lớp (z)/(a)/(b)/(c) xếp theo hai dấu hiệu đọc được trong đầu ra của base, mỗi ca đúng một lớp; lớp (z) (thoát trước mọi điều kiện, K2 `not_run`) đòi trùng byte không qua phép chiếu, nêu tên bốn ca hiện có; bộ so thêm tự kiểm chấp nhận đầu ra không đổi của (z) và từ chối khi (z) có hiện vật K2b hoặc thông báo lỗi lease đổi |

Thay đổi ngoài chữ của ba finding: trần soạn đặc tả ghi theo quyết định nâng +2/+2 của chủ kho (5 tác giả, 6 review; đã dùng 4 và 3).

### r5 so với r4 (review lượt 4) — sửa THEO LỚP (protocol §8.3)
| Lớp (finding) | Biểu hiện review lượt 4 nêu | Một cách sửa chung ở r5 |
|---|---|---|
| `b4-predicate-mutation-proof` (B4-S05; lượt 1–4) | thiếu ca cho UTF-8 của thân REST; ca chỉ khẳng định rc, không khẳng định trạng thái (`khong_khop` / `vang_hoac_khong_quyen` / `khong_doc_duoc`, `la` / `khong_giam`); lời GET sau audit hỏng; dọn dẹp ở đường hết hạn và `SystemExit`; nhánh không đo được của 7b; ghi chú nhóm G mâu thuẫn fixture | ĐỔI CÁCH LÀM theo checkpoint §12: rút bảng 96 hàng; đóng băng KIỂM KÊ 114 vị từ (định nghĩa bool, nguồn, quan sát) và sáu luật L-1…L-6 (một ca đích riêng, khẳng định trạng thái, một đột biến riêng, chứng minh bằng chạy, kiểm kê là sàn, không lối tắt); executor dựng ma trận, reviewer mã kiểm trên H. Từng biểu hiện có vị từ riêng: P10 (UTF-8 chặt trước JSON), P18–P20 cùng L-2 (trạng thái chính xác), Q05/Q06 (`la` khác `khong_giam`), Q14 (0 yêu cầu khi (i) đúng mà (ii) sai), C30/C31 ×4 đường thoát, S04/S05 (7b không đo được). Mục 6a, 7, 9 được viết lại cho khớp (giải mã trước khi phân tích; lệnh lỗi ⇒ từ chối; `buoc` sáu giá trị; `CONG_TAC` cả khi không gửi yêu cầu). Ghi chú nhóm G không còn |
| `b4-sensitive-size-authority` (B4-S10; lượt 2–4) | luật dừng cho phép vượt trần rồi mới dừng | Mục "Kích thước": trần áp cho ỨNG VIÊN GIAO NỘP (H sắp đẩy hoặc sắp review), theo `ADR-0044` "dừng TRƯỚC review"; đo numstat của đúng H trước mỗi lần đẩy và mỗi lần xin review/audit; vượt ⇒ không đẩy, không review; cùng luật với `tran_moi`; ví dụ biên 450/451; D-8 ghi cách đọc câu của r86; tiêu chí 9 sửa theo |
| `b4-eligibility-permission-contract` (B4-S13; mới) | H1 không tách điều kiện cấu trúc khỏi quyết định CI đã qua công tắc; fixture in hằng che mất điều đó | Mục 5: hai kênh — stdout mang `dk_bo_moi` / `dk_che_do_dich` (điều kiện cấu trúc, không phụ thuộc biến quyền, bên đọc là `kiem-merge`), `GITHUB_OUTPUT` mang quyết định CI đã qua công tắc (bên đọc là `ci.yml`); bốn nghĩa vụ của PR3/PR6; vị từ C20–C29 dùng khoá mới; GT-5 thêm bộ sinh hai kênh; tiêu chí 11 thử cả hai lớp, mọi trạng thái công tắc, biến quyền của người gọi; D-7 ghi cách đọc §4 A+1 |

Thay đổi ngoài chữ của ba lớp: hai khoá mà `kiem-merge` đọc đổi tên từ `cong_cu` / `g5_che_do` (r1–r4) sang `dk_bo_moi` / `dk_che_do_dich`, hệ quả trực tiếp của lớp thứ ba; bộ đếm trần soạn đặc tả cập nhật (tác giả 5/5, review 4/6). Các bảng "Thay đổi" của r2–r4 bên trên là lịch sử và còn nhắc bảng hàng cùng tên khoá cũ.

## Ngoài phạm vi
Đặt, đổi, xoá biến công tắc thật; đọc `vars` ở `chuan-bi` và mọi sửa `ci.yml`, `ops/ci_duong_nhanh.py`, `ops/cong_cu_test.py` (PR3, PR6); cặp biến của C2 và mọi thay đổi K7/M9; sửa K0–K7, ADR, protocol, adapter; cổng phía máy chủ đọc biến tại lúc merge; cơ chế chứng minh ai đã đặt biến; Windows CI; B1, B2, B3, PR2–PR8; route production, LIVE.
