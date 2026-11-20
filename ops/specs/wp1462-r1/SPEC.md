# wp1462 r2 — B4 của kế hoạch nguồn r4: công tắc CHO PHÉP theo lớp giảm và bên tiêu dùng tin cậy trong `kiem-merge` (CONG-TAC-G5)
packet_id: wp1462
revision: 2

Trạng thái: `proposed`, CHƯA đóng băng. Thay r1 (cùng đường dẫn, commit `7582454`, sha256 `3ca1c75001d96e46e342a042f343ca192fba5626298fc118e5ce0932a8c8661f`). Review đặc tả Codex `wp1462-spec-review-1` trả `changes_requested` với 8 finding P2 (B4-S01…B4-S08); r2 sửa cả tám, bảng đối chiếu ở mục "Thay đổi so với r1". Đặc tả Packet #1462, vai B4 của Mission #1172 theo **kế hoạch nguồn r4** (`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md`, nhánh `ops/wp1172-plan-r4`, sha256 `0f287ce4369fbeb7b1939daa8de5db7c27c2a4efdc1a21f2fccdd37dc9d83fbe`). Quyết định chủ kho: Mission r84 (`owner_decisions.Q9`: (a)–(d) theo khuyến nghị); thẩm quyền soạn đặc tả và trần: Mission r85 (`packet_graph` vai B4, `envelope.provider_budgets.per_new_packet`, `r85_constraints`). Mọi tham chiếu "§" là mục của kế hoạch r4; nơi đặc tả này và kế hoạch khác nhau thì **đặc tả này thắng** cho packet này, và mọi chỗ khác chữ kế hoạch được liệt kê ở mục "Chỗ khác chữ kế hoạch". Rủi ro: nhạy cảm (tệp nóng `.claude/dev/packet_loop.py`, cổng merge). Nền đo: `origin/master` = `0f9aa2a2cc697129e1f5be72feddf60986286865` (đo 16:10Z 20-11-2026); blob `.claude/dev/packet_loop.py` = `3db1abae`, `ops/ci_duong_nhanh.py` = `e43f514c`, `.github/workflows/ci.yml` = `a1db88d9` tại commit ấy.

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

Trước PR3, bộ phân loại của `master` không in khoá `cong_cu` hay `g5_che_do`, nên bước 4 chỉ ra `duong_nhanh`, `khong_giam` hoặc `la`: không lời GET nào được gửi và không PR nào đạt nhờ (β).

### 5. Tính lại bằng mã `master` — hợp đồng H1 (đầu ra của bộ phân loại)
Hai hàm nội bộ, tên do executor đặt, vai cố định: **hàm chạy** `(root, cay_ma, goc, dau) -> lớp` làm mọi việc dưới đây với mã lấy từ commit `cay_ma`; **điểm gọi sản xuất** DUY NHẤT trong K2b gọi nó với `cay_ma` = `goc` = M và `dau` = H. Không đối số CLI, biến môi trường hay tệp nào đưa được `cay_ma`/`goc` khác M vào điểm gọi sản xuất.
- **Đầu vào.** M = OID của `refs/remotes/origin/master` (đã qua tự kiểm 7a). Commit hợp C = commit hai cha (`goc`, `dau`) dựng từ `git merge-tree --write-tree` với danh tính và ngày cố định; merge xung đột hoặc git lỗi ⇒ `la`. Không dùng `--base` của người gọi, không dùng `refs/pull/<n>/merge`, không dùng cây làm việc.
- **Mã chạy.** Đúng blob `ops/ci_duong_nhanh.py` tại `cay_ma`, trong một cây tạm dựng đúng từ cây của `cay_ma` (bộ phân loại thấy cây ấy là cây làm việc của nó, đọc object của kho `--root`), bằng tiến trình con `python -I` với hạn 120 s. Điểm vào là điểm vào sẵn có: không đối số, biến `CI_DUONG_NHANH_SU_KIEN=pull_request`, `CI_DUONG_NHANH_GOC=<goc>`, `CI_DUONG_NHANH_DAU=<dau>`, `CI_DUONG_NHANH_MERGE=C`. Môi trường dựng MỚI từ danh sách cho phép (`PATH`, `SYSTEMROOT`, `TEMP`, `TMP`, `TMPDIR`, `HOME`, `USERPROFILE`, cộng biến git cần cho thư mục object tạm); không truyền `GITHUB_OUTPUT` hay biến `CI_DUONG_NHANH_*` nào khác.
- **Không để lại gì.** Sau lượt gọi — đạt, đỏ, hết hạn hay kết thúc bằng `SystemExit` — kho `--root` không có thêm ref, worktree đăng ký hay object (commit C và cây merge nằm trong thư mục object tạm), và mọi thư mục tạm của lượt gọi đã bị xoá.
- **Đọc đầu ra.** rc phải 0; stdout phải là UTF-8 hợp lệ. Chỉ ba khoá được đọc, mỗi khoá là dòng `<khoá>=<giá trị>` khớp trọn dòng: `che_do` (ĐÚNG một dòng, ∈ {`day_du`, `duong_nhanh`}); `cong_cu` (0 hoặc 1 dòng, ∈ {`chay`, `bo_qua`}); `g5_che_do` (0 hoặc 1 dòng, ∈ {`du`, `dich`}). Dòng khác bị bỏ qua. Ánh xạ: `duong_nhanh` và KHÔNG có `cong_cu=bo_qua`/`g5_che_do=dich` ⇒ `duong_nhanh`; `day_du` + `cong_cu=bo_qua` + không `dich` ⇒ `bo_moi`; `day_du` + `g5_che_do=dich` + không `bo_qua` ⇒ `che_do_dich`; `day_du` không kèm cả hai ⇒ `khong_giam`. Mọi thứ khác — rc ≠ 0, hết hạn, stdout không phải UTF-8, thiếu `che_do`, khoá lặp, giá trị ngoài tập (kể cả thừa khoảng trắng hay `\r`), `duong_nhanh` kèm quyết định giảm, cả `bo_qua` lẫn `dich`, không có tệp bộ phân loại tại `cay_ma` — ⇒ `la`.
- **Nghĩa vụ của PR3/PR6:** in `cong_cu=bo_qua` / `g5_che_do=dich` đúng dạng trên từ điểm vào ấy; chạy được dưới `python -I` (không import module anh em bằng tên trần). Giá trị ngoài hợp đồng là `la` ⇒ đỏ ở cổng merge.

Số đo lúc soạn (16:37Z 20-11-2026, phiên cloud Linux), gọi là **đường trực tiếp**: với mỗi merge trong `git log --first-parent --merges -60 0f9aa2a2cc697129e1f5be72feddf60986286865` (60 merge, mỗi cái hai cha), chạy `python -I ops/ci_duong_nhanh.py` của blob `e43f514c` trong cây làm việc tại commit ấy, với `GOC` = cha một, `DAU` = cha hai, `MERGE` = chính merge commit THẬT ⇒ 60/60 lượt rc 0 và đúng một dòng `che_do`: 42 `day_du`, 18 `duong_nhanh`. Bảng 60 dòng `<OID merge> <che_do>\n`, theo đúng thứ tự `git log` ấy, có sha256 `aa932267e766cf3f6e242f35febe3692909f3e909cb510177ba83d780bfc849a`. Đây là bộ phân loại HÔM NAY chạy trên lịch sử (cha một lịch sử làm gốc), KHÔNG phải đầu vào sản xuất của K2b (M sống) và không phải bằng chứng các PR ấy từng đi làn nào trên CI. Review lượt 1 đo thêm: đưa 60 head đã merge ấy vào với M hiện tại thì cả 60 ra `duong_nhanh` vì diff rỗng — phép phát lại kiểu đó vô nghĩa và không được dùng.

### 6. Đọc sống công tắc — hai tầng tách rời
**6a. Tầng chính sách** (hàm đọc công tắc của một lớp):
- Gửi ĐÚNG MỘT yêu cầu cho mỗi lượt cần đọc, tới `https://api.github.com/repos/ducthangho/tra-luat/actions/variables/<TÊN>` (URL ghép từ hằng), qua tầng vận chuyển 6b. Header: `Accept: application/vnd.github+json`, `X-GitHub-Api-Version`, `User-Agent` trung tính; nếu biến môi trường `GH_TOKEN` khác rỗng thì thêm `Authorization: Bearer`, không có thì gửi không xác thực. Giá trị token không bao giờ được in. Token chỉ ảnh hưởng việc ĐỌC ĐƯỢC hay không; nó không đổi được giá trị đọc về.
- **Dấu hiệu dương (đủ cả bốn):** mã 200; có ít nhất một header tên bắt đầu `x-github-` (không phân biệt hoa thường); thân dài không quá 65 536 byte và là JSON object hợp lệ (UTF-8 hợp lệ, cấm khoá trùng) với `name` là chuỗi bằng đúng `<TÊN>`; `value` kiểu chuỗi.
- **Bốn trạng thái:** `khop` (dương và `value` = chuỗi cho phép của lớp) · `khong_khop` (dương, giá trị khác, kể cả rỗng) · `vang_hoac_khong_quyen` (404 có header `x-github-`) · `khong_doc_duoc` (mọi thứ còn lại: mã khác kể cả 3xx, 200 thiếu header GitHub, thân lạ hay quá dài, JSON hỏng, `name` khác, `value` không phải chuỗi, tầng vận chuyển ném lỗi, `--repo` khác hằng, biến cấm đọc ở mục 8). CHỈ `khop` cho giảm.

**6b. Tầng vận chuyển** — MỘT hàm `_rest_get(url, headers, han) -> (status, headers, body)`, mọi vào/ra mạng của `packet_loop.py` đi qua nó, dùng `urllib` của thư viện chuẩn:
- chỉ phương thức GET, không thân yêu cầu;
- KHÔNG theo chuyển hướng: phản hồi 3xx được trả nguyên mã cho tầng chính sách; đích chuyển hướng không nhận yêu cầu nào, nên `Authorization` không bao giờ tới máy chủ thứ hai (review lượt 1 đo: bộ xử lý chuyển hướng mặc định của `urllib` chép `Authorization` sang đích);
- đọc tối đa 65 537 byte thân rồi dừng;
- `han` (mặc định 15 s ở điểm gọi sản xuất) vừa là hạn mỗi thao tác socket vừa là hạn tường của CẢ lời gọi, kiểm giữa các lần đọc; quá hạn ⇒ ném lỗi;
- không thử lại; lỗi kết nối, TLS, hết hạn đều ném một lớp lỗi mà tầng chính sách đổi thành `khong_doc_duoc`;
- tôn trọng cấu hình proxy của môi trường (phiên cloud cần).

Đo 16:19:34Z 20-11-2026 từ phiên cloud soạn đặc tả (một client: `urllib`, không token): `/actions/variables` và `/actions/variables/<tên>` trả **403, không `Server`, 0 header `x-github-`**, thân *"Access to this GitHub Actions path is not permitted through this proxy."*; cùng lúc `/repos/<kho>` trả 200 có 4 header `x-github-`. Hệ quả: phiên cloud loại này ở trạng thái `khong_doc_duoc` ⇒ mọi PR thuộc (β) bị đòi G5 đủ khi `kiem-merge` chạy từ đó (giá đã chấp nhận ở Q9(b)).

### 7. Tự kiểm cây (chỉ ở bước 3 của mục 4)
- **7a.** `git ls-remote origin refs/heads/master` phải trả đúng OID của `refs/remotes/origin/master^{commit}` cục bộ. `kiem-merge` KHÔNG tự fetch; lệch hoặc không đo được ⇒ từ chối, in cách chữa (`git fetch origin master` rồi chạy lại).
- **7b.** Tệp `packet_loop.py` đang chạy phải cùng blob với `M:.claude/dev/packet_loop.py`, so bằng `git hash-object --path=.claude/dev/packet_loop.py` (để checkout CRLF không gây lệch giả) với OID của blob tại M.
Hai phép này bắt chạy NHẦM cây; chúng không chống người cố ý sửa công cụ (§4 A+1 nói đúng như thế). `launcher.py` và các module khác không được kiểm.

### 8. Cờ siết và biến cấm đọc (cả hai chỉ siết)
- `--siet-g5-du` (cờ không tham số của `kiem-merge`): đòi `che_do_thuc_chay` = `du` trên đúng H cho PR đang xét, tắt cả (α) lẫn (β). Ai chạy `kiem-merge` cũng dùng được.
- Biến môi trường `PACKET_LOOP_CAM_DOC_CONG_TAC` khác rỗng ⇒ không gửi yêu cầu, công tắc ở `khong_doc_duoc`.
- Không có cờ hay biến nào theo chiều ngược lại.

### 9. Dòng chẩn đoán (stdout thật, không bị `_dk` nuốt)
- K2b in ĐÚNG MỘT dòng `LAN_G5 che_do_thuc_chay=<dich|khac> buoc=<siet|tu_kiem|tinh_lai|bang_chung|audit|cong_tac> lop=<duong_nhanh|bo_moi|che_do_dich|khong_giam|la|chua_tinh> master=<M|-> ket_qua=<dat|do>` khi và chỉ khi K2b đã chạy và `che_do_thuc_chay` ≠ `du`. `buoc` là bước ra quyết định; `lop=chua_tinh` và `master=-` khi dừng trước bước 4.
- Nếu đã gửi yêu cầu đọc công tắc, thêm ĐÚNG MỘT dòng `CONG_TAC lop=… bien=… trang_thai=… doc_luc=<UTC> updated_at=<chuỗi|-> request_id=<x-github-request-id|-> gia_tri=<JSON, tối đa 120 ký tự|->`. Nếu đạt nhờ (β), thêm ĐÚNG MỘT dòng `HIEU_LUC den=<doc_luc + 30 phút>`.
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
| (ii) Đọc được và không dính bản đệm, trên máy sẽ chạy `kiem-merge` cho phán quyết (β) | Máy được chỉ định: máy bàn Windows của chủ kho, với một token CHỈ ĐỌC Variables đặt ở `GH_TOKEN`. Trên biến thử: đọc giá trị 1 → chủ kho đổi → đọc phải ra giá trị 2 → chủ kho xoá → đọc phải ra 404 có header GitHub. Đọc bằng `urllib` theo đúng luật mục 6 (script đo do điều phối đặt ở `ops/specs/wp1462-r1/do/`), không bằng client khác | Chủ kho, trên máy ấy | Máy ấy chưa dùng được cho phán quyết (β): không đọc được ⇒ chạy đủ. Phiên cloud: đã đo `khong_doc_duoc` (mục 6) |
| (iii) API trả gì cho giá trị có khoảng trắng/xuống dòng đầu-cuối | Chủ kho đặt biến thử ba giá trị như thế, đọc lại | Chủ kho, cùng máy ở (ii) | Không đổi thiết kế: so khớp vốn tuyệt đối, hai chuỗi cho phép không có khoảng trắng |
| (iv) Lượt chạy lại và lượt mở lại PR có đọc lại `vars` | `ci.yml` chưa đọc `vars` trước PR3, B4 không có workflow trong write set | — | `khong_do_duoc` ở B4; chuyển thành điều kiện đo trong đặc tả PR3 |
| (v) `vars` ở `chuan-bi` là biến mức kho, không bị environment che | Như (iv) | — | Như (iv) |
| (vi) Máy chạy `kiem-merge` chạy được bộ phân loại của `master` | Đường trực tiếp của mục 5 trên máy ấy, đối chiếu sha256 của bảng 60 dòng | Điều phối (cloud: đã đo, khớp); chủ kho (máy bàn) | Máy ấy không dùng cho phán quyết (α)/(β) |

Luật đóng băng (theo quyết định điều phối sau review lượt 1; chủ kho xác nhận khi duyệt băm): (1) đặc tả ĐƯỢC đóng băng khi hàng (i) hoặc (ii) còn `khong_do_duoc`; khi ấy lệnh cấm đặt `CHO_PHEP` giữ nguyên và mọi máy chưa đo ở trạng thái không đọc được ⇒ chạy đủ. Vì Mission r85 ghi `depends_on` "W measured before the B4 spec is frozen", Mission revision cài B4 (mục Quy trình) phải ghi rõ quyết định này thay điều kiện ấy. (2) Không kết quả nào của (i)–(vi) đổi hợp đồng mã ở trên, vì mọi nhánh không đo được đã dẫn về chạy đủ; chúng chỉ quyết định có được đặt `CHO_PHEP` không, máy nào được dùng, và nội dung runbook. (3) Kết quả nào mâu thuẫn một câu của đặc tả này ⇒ sửa thành revision mới, không sửa tại chỗ. (4) Bản ghi `DO_Q9A.yaml` phải có trước khi BẤT KỲ ai đặt `CHO_PHEP`, và là đầu vào của mục 7 runbook.

## Nghiệm thu

### Giàn thử (bắt buộc, tự nó có ca kiểm)
- **GT-1 Đồ giả chính sách.** Thay `_rest_get` trong tiến trình bằng đồ giả GIỮ trạng thái (đổi được giá trị giữa hai lần đọc; trạng thái nằm trong TỆP để sống qua tiến trình; ghi nhật ký mọi yêu cầu: phương thức, URL, tên header). Dùng cho mọi ca chính sách (nhóm R, D, Q, T).
- **GT-2 Tầng vận chuyển THẬT.** Các ca nhóm X gọi chính hàm `_rest_get` thật tới máy chủ HTTP cục bộ trên `127.0.0.1` do ca dựng (không TLS, không proxy cho loopback, không kết nối ra ngoài); máy chủ ghi nhật ký yêu cầu nhận được. Đồ giả GT-1 KHÔNG được dùng ở nhóm X.
- **GT-3 Tiến trình con có giàn.** Một trình bọc chạy ở tiến trình MỚI: nạp `packet_loop.py` đang thử, cài đồ giả GT-1 đọc trạng thái từ tệp, rồi gọi đúng điểm vào CLI (`main`) với đối số `kiem-merge`. CHỈ trình bọc này được chạy `kiem-merge` ở tiến trình con mà không đặt biến cấm đọc.
- **GT-4 Cấm mạng thật.** Mọi lượt `kiem-merge` bằng tiến trình con KHÁC GT-3 đều đặt `PACKET_LOOP_CAM_DOC_CONG_TAC=1`. Trong các ca trong-tiến-trình và trong GT-3, mọi kết nối socket tới địa chỉ không phải loopback ném một lớp lỗi riêng và được đếm; ĐỎ khi bộ đếm ấy khác 0 ở bất kỳ ca nào. Ca tự kiểm: một lời gọi cố ý tới địa chỉ ngoài loopback phải bị chặn và được đếm.
- **GT-5 Bộ phân loại của fixture** là tệp `ops/ci_duong_nhanh.py` do ca test đặt vào `origin/master` của kho fixture. Bộ test KHÔNG đọc `ops/ci_duong_nhanh.py` thật (tệp ấy ngoài `PHU_THUOC_PACKET_LOOP`).
- **GT-6 Tín dụng giết.** Ca mới mang tiền tố `cong_b4_`; khẳng định đích của mỗi ca ném lớp riêng `ChotB4(AssertionError)`, định nghĩa trong tệp test và không mã sản phẩm nào ném được. Một đột biến của bảng dưới chỉ được tính GIẾT khi ca đích của nó đỏ bằng `ChotB4` do chính ca ấy ném; mọi kết cục khác — CLI sập, `AssertionError` thường, lỗi dựng fixture, hết hạn, ca khác đỏ — là TÍN DỤNG GIẢ. Bốn ca tự kiểm bộ phân hạng, mỗi ca một kết cục giả: đột biến làm CLI sập; đột biến làm bước dựng fixture ném; đột biến làm ca quá hạn; đột biến làm đỏ một ca KHÁC ca đích — cả bốn phải ra TÍN DỤNG GIẢ. Cách phân hạng của các đột biến cũ không đổi.
- **GT-7 Đối chứng khoẻ.** Bốn fixture chuẩn, mỗi cái đạt rc 0 với mọi K0–K7 đạt: ĐC-du (8 mảnh `du`); ĐC-α (mảnh `skipped`, M xếp `duong_nhanh`); ĐC-β (mảnh `skipped`, M in `cong_cu=bo_qua`, công tắc `bo_moi` khớp); ĐC-δ (bằng chứng `dich`, M in `g5_che_do=dich`, có run audit, công tắc `che_do_dich` khớp). Mỗi phản chứng trong bảng là MỘT thay đổi so với đúng một fixture chuẩn, nên đỏ của nó chỉ do chốt đang thử.

### Bảng chốt → phản chứng → đột biến
Mỗi hàng: một chốt mới; một CA ĐÍCH nêu kết cục bắt buộc — đa số là phản chứng phải ĐỎ ở `K2b làn G5` trong khi mọi điều kiện khác đạt, vài hàng ghi rõ "phải ĐẠT" hoặc một khẳng định trên nhật ký; và một đột biến RIÊNG gỡ đúng chốt ấy, làm ca đích sai kết cục và bị chính ca ấy giết theo GT-6. Cột "nền" là fixture chuẩn mà ca đích sửa.

| ID | Chốt | Nền | Ca đích và kết cục bắt buộc | Đột biến riêng |
|---|---|---|---|---|
| G01 | Job thuộc đúng run R | ĐC-du | 8 mảnh `success` nằm ở run `ci.yml` khác (id nhỏ hơn) trên H; mảnh của R `skipped` | gom job của mọi run |
| G02 | Job thuộc đúng attempt A | ĐC-du | 8 mảnh `success` ở attempt 1; R đang ở attempt 2 với mảnh `skipped` | bỏ so `run_attempt` |
| G03 | `head_sha` của job = H | ĐC-du | một mảnh mang `head_sha` khác | bỏ so `head_sha` của job |
| G04 | R đúng workflow `ci.yml` | ĐC-du | run id lớn hơn, `path` khác, giữ 8 mảnh `success`; run `ci.yml` có mảnh `skipped` | chọn R không lọc `path` |
| G05 | R đúng kho | ĐC-du | run id lớn hơn mang `repository.full_name` khác giữ 8 mảnh `success` | chọn R không lọc kho |
| G06 | R đúng H | ĐC-du | run id lớn hơn mang `head_sha` khác giữ 8 mảnh `success` | chọn R không lọc `head_sha` |
| G07 | Đủ 8 mảnh 0..7 | ĐC-du | thiếu mảnh 7 | chỉ đòi 7 mảnh |
| G08 | Mỗi tên job đúng một lần | ĐC-du | hai job cùng tên mảnh 3, một `success` một `failure` | lấy job đầu tiên khớp tên |
| G09 | `conclusion` job = `success` | ĐC-du | một mảnh `cancelled`, bước đủ vẫn `success` | bỏ kiểm `conclusion` job |
| G10 | `status` job = `completed` | ĐC-du | một mảnh `in_progress` kèm `conclusion` `success` | bỏ kiểm `status` job |
| G11 | `steps` là list object có `name` chuỗi | ĐC-du | một mảnh thiếu `steps` | thiếu `steps` coi là đạt |
| G12 | Bước đủ đúng một lần | ĐC-du | một mảnh có hai bước S_DU | đòi "ít nhất một" |
| G13 | Bước đủ `success` | ĐC-du | bước S_DU của một mảnh `skipped`, job vẫn `success` | bỏ kiểm `conclusion` bước |
| G14 | Bước đủ `completed` | ĐC-du | bước S_DU `in_progress` kèm `conclusion` `success` | bỏ kiểm `status` bước |
| G15 | `du` loại trừ bước đích `success` | ĐC-du | một mảnh có cả S_DU và S_DICH `success` | bỏ điều kiện loại trừ ở `du` |
| G16 | `dich` đòi bước đích ở MỌI mảnh | ĐC-δ | một mảnh có S_DICH `skipped` | `dich` khi "có mảnh nào đó" có bước đích |
| G17 | `dich` loại trừ bước đủ `success` | ĐC-δ | một mảnh có cả hai bước `success` | bỏ điều kiện loại trừ ở `dich` |
| G18 | `dich` đòi job `success` | ĐC-δ | một mảnh `failure`, bước đích `success` | `dich` bỏ kiểm `conclusion` job |
| Q01 | K2b chỉ chạy khi K2 đạt | fixture cũ K2 đỏ, không mảnh | đầu ra phải trùng byte với base; có thêm dòng K2b hay `LAN_G5` là đỏ | chạy K2b cả khi K2 đỏ |
| Q02 | Cờ siết tắt (α) | ĐC-α + `--siet-g5-du` | phải đỏ | bỏ nhánh cờ siết |
| Q03 | Cờ siết tắt (β), không gửi yêu cầu | ĐC-β + `--siet-g5-du` | phải đỏ, nhật ký 0 yêu cầu | cờ siết xét sau bước 4 |
| Q04 | Tự kiểm 7a | ĐC-α | remote `master` tiến thêm một commit, cục bộ chưa fetch | bỏ 7a |
| Q05 | 7a không đo được ⇒ từ chối | ĐC-α | `ls-remote` trả rc ≠ 0 | `ls-remote` lỗi coi là khớp |
| Q06 | Tự kiểm 7b | ĐC-α | blob `packet_loop.py` tại M khác tệp đang chạy | bỏ 7b |
| Q07 | Tự kiểm không chạy khi `du` | ĐC-du | cùng lệch của Q04 và Q06 ⇒ phải ĐẠT, trùng byte với base | chạy tự kiểm trước bước 1 |
| Q08 | 7b so qua bộ lọc git | ĐC-α | tệp đang chạy là bản CRLF của đúng blob tại M, kho bật chuyển đổi EOL ⇒ phải ĐẠT | so băm byte thô của tệp |
| T01 | Mã chạy là blob tại M | ĐC-α đổi: M in `day_du`; cây làm việc và H mang bộ phân loại luôn in `duong_nhanh` | phải đỏ | chạy tệp của cây làm việc |
| T02 | Làn không lấy từ bằng chứng lượt PR | fixture mảnh `skipped` (lượt PR tự xếp `duong_nhanh`), M in `day_du` | phải đỏ | mảnh `skipped` coi là `duong_nhanh` |
| T03 | `goc` là M, không phải `--base` | ĐC-α đổi: bộ phân loại fixture in `duong_nhanh` chỉ khi `GOC` = `--base` | phải đỏ | truyền `--base` làm `goc` |
| T04 | Merge xung đột ⇒ `la` | ĐC-α | M và H sửa cùng dòng một tệp | xung đột thì dùng cây của H |
| T05 | rc ≠ 0 ⇒ `la` | ĐC-α | bộ phân loại in `che_do=duong_nhanh` rồi thoát rc 1 | rc ≠ 0 vẫn đọc stdout |
| T06 | Hết hạn ⇒ `la` | ĐC-α | bộ phân loại in đủ rồi treo quá hạn (ca dùng hạn ngắn qua tham số nội bộ) | hết hạn thì dùng phần đã in |
| T07 | Khoá lặp ⇒ `la` | ĐC-α | hai dòng `che_do`: `duong_nhanh` rồi `day_du` | lấy dòng đầu |
| T08 | Giá trị ngoài tập ⇒ `la` | ĐC-α | `che_do=duong_nhanh\r` | cắt khoảng trắng trước khi so |
| T09 | Thiếu `che_do` ⇒ `la` | ĐC-β | chỉ in `cong_cu=bo_qua` | thiếu `che_do` coi là `day_du` |
| T10 | `duong_nhanh` kèm quyết định giảm ⇒ `la` | ĐC-α | thêm `cong_cu=bo_qua` | bỏ kiểm tổ hợp này |
| T11 | Cả `bo_qua` lẫn `dich` ⇒ `la` | ĐC-β | thêm `g5_che_do=dich` | ưu tiên `bo_moi` |
| T12 | stdout không UTF-8 ⇒ `la` | ĐC-α | chèn byte `0xff` vào một dòng khác | giải mã kiểu thay thế |
| T13 | Không tệp bộ phân loại tại M ⇒ `la` | ĐC-α | M không có `ops/ci_duong_nhanh.py`, cây làm việc có | thiếu ở M thì lấy ở cây làm việc |
| T14 | Môi trường theo danh sách cho phép | ĐC-α đổi: bộ phân loại fixture in `duong_nhanh` chỉ khi KHÔNG thấy `GITHUB_OUTPUT` và biến lạ `CI_DUONG_NHANH_X`; người gọi đặt cả hai | phải ĐẠT; đột biến làm nó đỏ | truyền nguyên môi trường người gọi |
| T15 | Không để lại gì | ĐC-α và một ca `la` | sau lượt gọi `for-each-ref`, `worktree list`, `count-objects -v` của kho và danh sách thư mục tạm phải bằng trước | bỏ bước dọn |
| R01 | Chỉ đúng chuỗi mới giảm | ĐC-β | giá trị sai một ký tự; và giá trị rỗng | giá trị khác rỗng coi là khớp |
| R02 | Không bỏ hoa thường | ĐC-β | chuỗi cho phép viết hoa | so sau `casefold` |
| R03 | Không cắt khoảng trắng | ĐC-β | chuỗi cho phép kèm dấu cách đầu; và kèm `\n` cuối | so sau `strip` |
| R04 | Chỉ mã 200 | ĐC-β | 403 có header GitHub, thân mang đúng chuỗi | bỏ kiểm mã |
| R05 | 404 không cho giảm | ĐC-β | biến bị xoá (404 có header GitHub) | 404 coi là khớp |
| R06 | Đòi header `x-github-` | ĐC-β | 200 đúng chuỗi, không header GitHub nào (ca proxy) | bỏ kiểm header |
| R07 | JSON chặt | ĐC-β | thân có khoá `value` hai lần (lạ trước, đúng sau); và thân không phải JSON | giải mã JSON thường |
| R08 | `name` phải đúng tên | ĐC-β | 200, `name` là tên biến khác, `value` đúng chuỗi | bỏ kiểm `name` |
| R09 | `value` phải là chuỗi | ĐC-β | `value` là list chứa đúng chuỗi | ép `str()` rồi so |
| R10 | Đúng biến của lớp | ĐC-δ | chỉ biến `bo_moi` mang chuỗi của `bo_moi`; biến `che_do_dich` vắng | mọi lớp đọc biến `bo_moi` |
| R11 | Đúng chuỗi của lớp | ĐC-β | biến `bo_moi` mang chuỗi của `che_do_dich` | chấp nhận chuỗi của bất kỳ lớp nào |
| R12 | `--repo` = hằng kho | ĐC-β với `--repo` và readback của kho khác | phải đỏ, 0 yêu cầu | ghép URL từ `--repo` |
| R13 | Biến cấm đọc | ĐC-β + biến cấm | phải đỏ, 0 yêu cầu | lờ biến cấm |
| R14 | Không nguồn dự phòng (R4-25) | ĐC-β, đồ giả ném lỗi; chuỗi cho phép có trong tên bước, trong một trường của `--workflow-jobs`, trong `--chu-kho-comment`, trong biến môi trường cùng tên biến công tắc | phải đỏ | không đọc được thì tìm chuỗi trong readback jobs |
| R15 | Tầng vận chuyển ném ⇒ không giảm | ĐC-β | đồ giả ném lỗi kết nối | lỗi vận chuyển coi là khớp |
| R16 | Thân quá dài ⇒ không giảm | ĐC-β | thân hợp lệ đúng chuỗi, đệm khoảng trắng JSON tới 65 537 byte | bỏ kiểm độ dài |
| R17 | Đúng một GET, đúng URL | ĐC-β và ĐC-δ | nhật ký phải có đúng một yêu cầu GET tới đúng URL của lớp | gửi hai yêu cầu; và đổi đường dẫn |
| R18 | Token không lộ | ĐC-β với `GH_TOKEN` là chuỗi đánh dấu | chuỗi ấy không có trong stdout/stderr; header `Authorization` có trong nhật ký | in header ở dòng `CONG_TAC` |
| D01 | `che_do_dich` đòi bằng chứng `dich` | ĐC-δ | mảnh `skipped` | bỏ điều kiện (i) |
| D02 | `che_do_dich` đòi run audit | ĐC-δ | không `--dot-bien-du-*`, không dòng miễn | bỏ điều kiện (ii) |
| D03 | Dòng miễn không thay run audit | ĐC-δ | không run audit, có dòng `full_mutant_audit: <H> mien` của chủ kho (K7 vẫn đạt) | dùng nguyên kết quả K7 |
| D04 | Run audit phải `success` đúng H | ĐC-δ | run audit `success` trên SHA khác | bỏ so `head_sha` của run audit |
| D05 | Điều kiện cục bộ trước lời GET | ĐC-δ ở phản chứng D01 và D02 | nhật ký 0 yêu cầu | đọc công tắc trước |
| X01 | Chỉ GET, không thân | GT-2 | máy chủ phải thấy đúng một yêu cầu GET, độ dài thân 0 | gửi POST |
| X02 | Không theo chuyển hướng | GT-2: máy chủ A trả 302 tới máy chủ B (cũng loopback); B trả 200 đúng chuỗi | hàm phải trả mã 302; B nhận 0 yêu cầu | dùng opener mặc định |
| X03 | Trần byte | GT-2: thân 1 MiB | phần thân trả về không quá 65 537 byte | đọc hết thân |
| X04 | Hạn tường | GT-2: máy chủ nhỏ giọt một byte mỗi 0,2 s, `han` = 1 s | phải ném lỗi trong 3 s | chỉ đặt hạn mỗi thao tác socket |
| X05 | Lỗi kết nối ném đúng lớp | GT-2: cổng loopback không ai nghe | phải ném lớp lỗi mà 6a đổi thành `khong_doc_duoc` | nuốt lỗi, trả mã 200 thân rỗng |
| X06 | Header đi nguyên vẹn | GT-2 | máy chủ phải nhận đúng `Authorization` và `Accept` đã truyền | bỏ header khi gửi |
| O01 | Dòng `LAN_G5` đúng luật mục 9 | ĐC-du, ĐC-α, ĐC-β, một ca đỏ | số dòng `LAN_G5` phải lần lượt 0, 1, 1, 1; `CONG_TAC` 0, 0, 1, theo ca; `HIEU_LUC` 0, 0, 1, 0 | in `LAN_G5` cả khi `du` |
| H01 | Ca cấu trúc `ci.yml` (tiêu chí 5) | YAML tổng hợp | xem tiêu chí 5 | chấp nhận 0 bước đủ |

Bảng có 72 hàng (đếm HÀNG mang ID); hàng nào ghi hai đột biến hoặc hai phản chứng thì mỗi cái là một mục riêng trong bảng `MUTANTS` và một ca riêng. Mỗi hàng nhóm R, D còn một đối chứng ngược chiều sẵn có: chính fixture nền của nó ĐẠT.

### Tiêu chí
1. **A/B không đổi hành vi (B-2), dựng trong MỘT lệnh.** Base = merge-base của H với `origin/master`. Tập fixture = MỌI ca hiện có đi qua bộ dựng `_c1106` (tại nền: 119 dòng chứa `_c1106_ca(` và 5 dòng chứa `_c1106(`, đếm DÒNG bằng `grep -c`, 16:10Z 20-11-2026; executor đếm lại theo CA tại base và báo con số cùng danh sách tên). Bộ dựng dùng chung chỉ được thêm bằng chứng `du` mặc định (8 job mảnh có bước S_DU `success`, đúng run/attempt/head), theo tiền lệ K7 của #1120. Mỗi fixture dựng MỘT lần, hai vế (`packet_loop.py` của base và của head, mỗi vế kèm `launcher.py` của chính nó) chạy trên cùng thư mục fixture. ĐỎ khi: một ca có rc, stdout hoặc stderr lệch một byte; hoặc số ca được so nhỏ hơn số ca đếm tại base.
2. **A/B bề mặt đổi, với phép chiếu có định nghĩa.** Cùng tập fixture ở HÌNH DẠNG CŨ (không job mảnh). Phép chiếu P bỏ khỏi đầu ra của head ĐÚNG các hiện vật của K2b: dòng stdout bắt đầu bằng `LAN_G5 `, `CONG_TAC ` hoặc `HIEU_LUC `; dòng stderr `THIẾU  K2b làn G5: …`; và tên `K2b làn G5` cùng dấu phân cách của nó trong dòng tổng kết. Ba lớp ca: (a) base đỏ ở K2 ⇒ head trùng byte với base, KHÔNG qua P; (b) base đỏ nhưng K2 đạt ⇒ rc bằng nhau, P(head) trùng byte với base, và head có đúng một dòng `LAN_G5`, đúng một dòng `THIẾU` của K2b; (c) base ĐẠT ⇒ head rc 12, stdout là đúng một dòng `LAN_G5`, stderr là đúng dòng `THIẾU` của K2b và dòng tổng kết chỉ nêu K2b. ĐỎ khi có lệch nào ngoài ba khuôn ấy, hoặc có ca base đỏ mà head đạt (B-1). Bộ so có tự kiểm chạy cùng lệnh, ĐỎ nếu một ca tự kiểm sai: chấp nhận đúng hiện vật dự định ở (b) và (c); TỪ CHỐI khi head thêm một dòng stdout không thuộc ba loại, khi có hai dòng `LAN_G5`, khi dòng `THIẾU` của một điều kiện khác đổi một ký tự, khi rc lệch ở (b), khi ca lớp (a) có bất kỳ hiện vật K2b nào.
3. **Mọi ca cũ giữ kỳ vọng.** Không ca nào của `packet_loop_test.py` bị xoá hay đổi rc/lý do kỳ vọng; thay đổi duy nhất ở phần cũ là bộ dựng dùng chung ở tiêu chí 1 và phần mở rộng bộ phân hạng ở GT-6. ĐỎ khi diff của tệp test chạm kỳ vọng của một ca cũ.
4. **Bảng chốt.** Mỗi hàng của bảng có ca phản chứng đỏ đúng chỗ, fixture nền của nó đạt, và đột biến của nó bị ca ấy giết theo GT-6. Bằng chứng: executor chạy từng cặp (đột biến, ca đích) tại chỗ, nộp bảng ID · tên đột biến · tên ca · phân hạng; reviewer chạy lại độc lập. ĐỎ khi một hàng thiếu ca, thiếu đột biến, đột biến sống, hoặc đột biến chỉ có tín dụng giả. Bảng đột biến của `packet_loop_test.py` KHÔNG thuộc `ci-dot-bien-du.yml`; nó chạy ở `packet-loop-dot-bien.yml` theo lịch sau merge, đọc kết quả lượt đầu tiên sau merge là việc ghi ở M8, không chặn merge.
5. **Ca cấu trúc `ci.yml`, bền qua PR6.** Một hàm kiểm nhận văn bản YAML và trả đạt/không: trong job `gate-cong-cu`, ma trận `manh` đúng 0..7, số bước tên S_DU = 1, số bước tên S_DICH ∈ {0, 1}. Chạy trên sáu YAML tổng hợp: chỉ bước đủ (hình dạng hôm nay) ⇒ đạt; bước đủ + một bước đích (hình dạng PR6 phải có) ⇒ đạt; không bước đủ ⇒ không đạt; hai bước đủ ⇒ không đạt; hai bước đích ⇒ không đạt; ma trận thiếu mảnh 7 ⇒ không đạt. Và chạy trên `.github/workflows/ci.yml` THẬT ⇒ đạt; trong kho có `.git` mà thiếu tệp ⇒ ĐỎ, không bỏ qua. Ca này KHÔNG cấm bước đích: PR6 thêm bước ấy mà không phải sửa `packet_loop_test.py`.
6. **Tiến trình mới (GT-3), bốn lượt nối tiếp trên cùng tệp trạng thái của ĐC-β:** đúng chuỗi ⇒ ĐẠT; đổi giá trị ⇒ ĐỎ; xoá biến ⇒ ĐỎ; đặt lại đúng chuỗi ⇒ ĐẠT. Mỗi lượt là một tiến trình riêng; nhật ký ghi đúng một yêu cầu mỗi lượt; bộ đếm kết nối ngoài loopback bằng 0. Đối chứng: cùng ĐC-β chạy bằng tiến trình con THƯỜNG (có biến cấm, GT-4) ⇒ ĐỎ với 0 yêu cầu.
7. **Nằm im trước PR3.** Với bộ phân loại fixture chỉ in `che_do` và `packet_loop` (hình dạng hôm nay), mọi ca ghi 0 yêu cầu REST: ĐC-α đạt, và fixture mảnh `skipped` mà M in `day_du` thì đỏ.
8. **Phát lại ngoại tuyến trên lịch sử thật (ngoài bộ ca, script trong `ops/specs/wp1462-r1/do/`).** Mục đích hẹp: chứng minh HÀM CHẠY của mục 5 (dựng commit hợp, cây tạm, môi trường, đọc đầu ra) cho cùng kết quả với đường trực tiếp trên dữ liệu thật; nó KHÔNG đi qua tự kiểm cây, KHÔNG dùng M sống và không thay các ca fixture của K2b. Định nghĩa: tập = 60 merge của `git log --first-parent --merges -60 0f9aa2a2cc697129e1f5be72feddf60986286865`; với mỗi merge gọi hàm chạy với `cay_ma` = `0f9aa2a2cc697129e1f5be72feddf60986286865` (blob bộ phân loại `e43f514c`), `goc` = cha một, `dau` = cha hai, đồ giả GT-1 đếm yêu cầu. Kỳ vọng độc lập: bảng 60 dòng sinh bằng đường trực tiếp (merge commit thật, không qua hàm chạy), executor sinh lại và sha256 phải bằng `aa932267e766cf3f6e242f35febe3692909f3e909cb510177ba83d780bfc849a`. ĐẠT khi và chỉ khi: 60/60 lượt của hàm chạy trả đúng lớp tương ứng từng dòng (`duong_nhanh` ⇒ `duong_nhanh`; `day_du` ⇒ `khong_giam`), tức đúng 18 và 42; 0 lượt `la`; 0 yêu cầu REST; kho không thêm ref, worktree, object. Lệch dù một dòng ⇒ ĐỎ: executor dừng và báo OID, không tự giải thích cho qua.
9. **Cổng kho:** `packet_loop_test` N/N với hai số BẰNG NHAU (CI: 16 mảnh + job gom đạt; N sau = N trước + số ca mới, báo cả ba số; sổ ca tại nền: 1582 ca, review lượt 1 đo); Ruff F delta = 0 so với base trên hai tệp `.py` của write set và 0 lỗi F trên tệp `.py` mới (nền Ruff của hai tệp CHƯA ĐO ở lượt soạn đặc tả và ở review lượt 1: cả hai máy không có Ruff); `doctrine-scan` và `adr-song` rc 0; CI PR Ubuntu xanh trên H; một lượt `ci-dot-bien-du.yml` `success` trên đúng H với mọi job `success` (K7, vì diff chạm `.claude/dev/**`); đọc lượt push sau merge theo nhãn job. Báo delta thời gian của `gate-packet-loop-manh` (tổng 16 mảnh) trước/sau.
10. **Runbook:** tệp ở mục 10 có đủ mười mục, trong đó mục 3 có nguyên văn điều khoản G5 đủ trước PR5; nghiệm thu là lời duyệt của chủ kho theo danh sách ấy, không có ca máy.

## Write set
- `.claude/dev/packet_loop.py` (gồm câu ranh giới ở docstring đầu tệp: nay có MỘT lời GET chỉ đọc, và đọc `GH_TOKEN`)
- `.claude/dev/packet_loop_test.py`
- `ops/specs/wp1462-r1/` — `SPEC.md`, `RUNBOOK_CONG_TAC.md`, `do/` (bản ghi đo Q9(a), script đo, script và kết quả A/B, script và kết quả phát lại; không tệp `*_test.py`)

Không tệp nào khác. Đã rà (16:10Z 20-11-2026): chuỗi "K0–K7" có ở `docs/adr/0060-dieu-kien-merge-va-moc-ready.md`:158, `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md`:159, `docs/PROTOCOL_DA_PHIEN.md`:1643, `.claude/skills/land-packets/SKILL.md`:64 và dòng trợ giúp của lệnh; điều kiện mới mang tên `K2b` nên bốn tệp tài liệu ấy vẫn đúng chữ và KHÔNG vào write set. Không tài liệu nào liệt kê cờ của `kiem-merge` ngoài `--dot-bien-du-*` ở adapter `land-packets`; cờ `--siet-g5-du` được ghi ở trợ giúp lệnh và runbook. `.claude/dev/packet_loop_test_manh.py` chia mảnh theo thứ tự đăng ký, không có bảng trọng số ⇒ không cần sửa. `ops/ci_duong_nhanh.py`, `.github/workflows/ci.yml`, `.claude/dev/ci_dang_ky_test.py` KHÔNG thuộc B4 (phần đọc `vars` ở `chuan-bi` thuộc PR3). Nợ có tên, không làm ở đây: adapter `land-packets` chưa trỏ tới runbook và chưa nói "chạy `kiem-merge` từ cây `origin/master`". Lease (`ops/leases/…`) là hiện vật của điều phối trên nhánh `ops/wp1462-r1`, không thuộc PR giao nộp.

## Quy trình và quyền
- **Trước lease — ba bước tách rời, đúng thứ tự.** (1) Chủ kho duyệt BĂM đặc tả, sau khi review đặc tả Codex không còn finding P0–P3. (2) Một **Mission revision** riêng do điều phối soạn và chủ kho duyệt được CÀI: nó nhận Packet #1462 vào thi công và ràng buộc số packet, revision và generation, đúng băm đặc tả đã duyệt, base thi công, write set, provider và bề mặt chạy của executor và reviewer, các trần ở gạch dưới, và quyết định về `depends_on` ở mục phép đo. (3) Sau đó mới cấp lease; trước khi cấp chạy `ai-dang-giu` trên mọi ref cho hai tệp `.claude/dev/` và thư mục đặc tả. Duyệt băm KHÔNG tự nó trao quyền thi công: Mission r85 chỉ nhận B4 ở mức soạn đặc tả (`admitted_spec_drafting`).
- **Hai bộ trần tách nhau, theo Mission r85 (`per_new_packet`).** Soạn đặc tả: tác giả 3 lượt, review đặc tả Codex 4 lượt; tại lúc soạn r2 đã dùng 2/3 và 1/4 (theo thông báo của điều phối, không phải số tác giả tự đo). Thi công: attempts 3; review mã Codex 3; CI PR Ubuntu 3; `ci-dot-bien-du.yml` 1; connector 2; CI rerun 1; Windows CI 0. Trước MỖI lời gọi, điều phối đọc lại bộ đếm đã dùng / đã giữ chỗ / trần của đúng trục ấy; chạm trần thì dừng và hỏi.
- Executor: Claude Code (Fable 5.2), phiên cloud riêng. Reviewer: Codex service gpt-6-astra, mức xhigh, phiên độc lập, chỉ đọc; reviewer CHẠY ca và đột biến có sẵn, hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời cho điều phối.
- Chủ kho tự audit exact-H trước LẦN ĐẨY ĐẦU của H; điều phối không ký thay. Merge do chủ kho bấm.
- **Windows:** diff chạm `.claude/dev/` nên K6 xếp `required`; theo quy tắc thường trực "không Windows CI" và r85 (chạy Windows tại chỗ chỉ cho B3), packet này MIỄN Windows bằng dòng miễn của chủ kho. Máy đọc công tắc được chỉ định là máy bàn Windows của chủ kho; nó chỉ được dùng cho phán quyết (β) sau khi phép đo (ii) đạt VÀ các ca `cong_b4_*` đã chạy xanh tại chỗ trên máy ấy dưới một thẩm quyền riêng. Trước PR3 không phán quyết (β) nào tồn tại, nên điều này không chặn B4; phán quyết (α) chạy được từ phiên cloud Linux.
- Trước khi đẩy H: cập nhật nhánh lên `master` mới nhất và đo lại làn; PR này là `day_du`. Lượt `kiem-merge` cho chính PR này chạy bằng mã của `master` TRƯỚC B4.
- Không ai đặt `CHO_PHEP` trong packet này. Sau khi land: B4 nằm im cho tới khi PR3 land VÀ chủ kho tự đặt biến sau khi Q9(a) đạt.

## Chỗ khác chữ kế hoạch (để review soi)
- **D-1 Phạm vi tự kiểm cây.** §4 A+1 viết "lệch ⇒ từ chối" không kèm phạm vi. Đặc tả này chỉ chạy tự kiểm khi quyết định cần tính lại bằng mã `master` (bước 3), để B-2 đúng từng byte và để bộ ca hiện có không phải mang blob của công cụ. Điều phối giữ lựa chọn này sau review lượt 1.
- **D-2 Tên điều kiện** là `K2b` (con của K2), không phải `K8`, để không sửa hai ADR, protocol và adapter. Điều phối giữ.
- **D-3 Chốt thêm ngoài chữ kế hoạch, đều chỉ siết:** K2b tự ràng buộc run/attempt/head của job mảnh; `--repo` phải bằng hằng kho mới đọc công tắc; lớp `che_do_dich` đòi bằng chứng `dich` trên H; biến cấm đọc; không theo chuyển hướng; trần 65 536 byte; hạn tường.
- **D-4 Runbook nằm trong `ops/specs/wp1462-r1/`** thay vì `docs/`, theo write set của Mission r85.
- **D-5 (iv) và (v)** của phép đo không đo được trong B4 và chuyển sang đặc tả PR3.
- **D-6 Đóng băng khi W chưa đo xong** (luật đóng băng (1)): khác chữ §7 "phép đo chuẩn bị → Q9 → đóng băng"; lệnh cấm đặt `CHO_PHEP` là thứ giữ an toàn, và Mission revision cài B4 phải ghi quyết định này.

## Thay đổi so với r1
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

## Ngoài phạm vi
Đặt, đổi, xoá biến công tắc thật; đọc `vars` ở `chuan-bi` và mọi sửa `ci.yml`, `ops/ci_duong_nhanh.py`, `ops/cong_cu_test.py` (PR3, PR6); cặp biến của C2 và mọi thay đổi K7/M9; sửa K0–K7, ADR, protocol, adapter; cổng phía máy chủ đọc biến tại lúc merge; cơ chế chứng minh ai đã đặt biến; Windows CI; B1, B2, B3, PR2–PR8; route production, LIVE.
