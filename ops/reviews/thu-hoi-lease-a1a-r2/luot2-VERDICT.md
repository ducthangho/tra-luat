verdict: changes_requested
reviewed_spec_sha256: 1bfdc7bbe15bf28543fcdbdc3269f78beb0f00ffd5e5e510b11de1a66bd58cc6
reviewed_sha: 981b9ea1d4bfaa0511cfbc8d9bdee9d8c151c86f
P1: 1   P2: 3   P3: 0
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); biến thể và effort phục vụ thực tế KHÔNG ĐO ĐƯỢC

Review độc lập bản nháp 2, không phải nghiệm thu implementation A1a r2. Bản ghi sớm đã được tạo và bổ sung trong lượt này. Execution surface: dịch vụ Codex có công cụ shell (codex_service), transport machine; không suy danh tính model/effort từ dòng yêu cầu `gpt-6-astra/high` trong SPEC. Không gọi mạng, không sửa cây `cay-kho/`; các script và kho phản chứng tự soạn nằm trong `scratch/`. HEAD/tree đo được là `981b9ea1d4bfaa0511cfbc8d9bdee9d8c151c86f` / `bf575cf5f2b52641ca4e0b8c24b88d1ee4e74846`.

Hai quyết định E8 đã được thực thi về **phạm vi quyền và nguồn**: M14 chỉ dự báo, M4 chỉ lấy cây mốc Q6. Không yêu cầu chủ kho quyết lại hai câu ấy; không có finding mới thuộc lớp `nguon-duoc-tin-ma-chua-xac-minh`, không tăng bộ đếm lần 7 thành 8. P1 còn lại là thiếu phép kiểm ID/tên bắt buộc của Q6 trong thuật toán dẫn xuất được chỉ định. **Số đo thật 11/3/92, digest và kết quả rỗng đều tái lập được**; P1 không dựa vào cáo buộc các số ấy sai.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Các đường script dưới đây chạy từ cwd bằng `python3 -B`; JSON là bản in đã chạy, không phải output điền tay. Mô hình M14/A4 được gắn nhãn riêng, không nhận là implementation đã ship.

| Finding lượt 1 | Trạng thái | Đối chiếu và bằng chứng chạy được |
|---|---|---|
| F1 — `nguon-duoc-tin-ma-chua-xac-minh` | **ĐÓNG** | SPEC:47,124,151,193–196,301–305 rút quyền xoá holder và cấm dùng `DU_BAO` để cấp lease. `python3 -B scratch/repro_m14.py` (`scratch/m14.json`, `cache_oid`): chỉ đổi OID cache master, OID bare đứng yên; dự báo mô hình `KHONG→CHE`, rc vẫn `11→11`; ở **mỗi snapshot**, rc và dãy dòng không dự báo bằng lệnh hiện tại không cờ. A19 có L sống trên side vẫn giữ L. Đây đúng quyết định prediction-only; các thiếu sót nghiệm thu mới ở F8–F10 không tự cấp lại quyền cho cache. |
| F2 — `mien-lich-su-vuot-quyet-dinh` | **ĐÓNG-MỘT-PHẦN** | Phần nguồn/mốc/clock đã **đóng đúng E8**: SPEC:141,268–291 ghim đúng cây A0 và giờ commit. Chạy `do_q6.py` cho JSON byte-match bản cung cấp; `scratch/repro_q6.py`: cây sau thêm cặp không đổi kết quả cây ghim. Nhưng hợp đồng Q6 đầy đủ vẫn thiếu kiểm ID/tên (F11), nên không đóng toàn bộ yêu cầu “Q6 + (b)”. Không còn quét mọi ref để ghim hằng. |
| F3 — `con-hieu-luc-bo-mat-trang-thai-thu-ba` | **ĐÓNG** | SPEC:276–277 phân biệt một chiều ⇒ rc3, hai chiều đã thay ⇒ loại, hết hạn trước ⇒ loại. `scratch/q6.json`: `one-way-new` rc3; `replaced-new` chỉ giữ `(y,z)`, loại `(x,y)`; cặp hợp lệ rc0. Thêm cặp ở cây sau không đổi cây ghim; side không thể làm chết N trong cây ấy. Ca t123 hiện tại chạy lại **1/1, bỏ qua0, rc0** (`scratch/t123.log`). |
| F4 — `dot-bien-khong-khop-seam-consumer` | **ĐÓNG** | A18:218 nay đo phép so digest, có positive control đầy đủ và nhận diện `Chan(12)` thay vì bất kỳ lỗi nào. `scratch/repro_seams.py` / `scratch/seams.json`: pin Q3 cho rc0 và receipt đúng; newline/đổi một ký tự ⇒ Chan12; gỡ phép so ⇒ hai ca thành0; nới nhận digest newline ⇒ riêng ca ấy thành0; bốn guard còn lại có phản chứng riêng. F8 cùng lớp nhưng ở seam M14 mới, không phải tái mở lỗi A18 đã vá. |
| F5 — `thieu-nhanh-nghiem-thu` | **ĐÓNG** | A4:207 đã có cả hai khoá; mô hình hợp đồng A4 trong `scratch/seams.json` giết bốn mutant bằng bốn ca riêng. A7:210 có đủ `(L,N)/(L,khác)/(khác,N)`; chạy chính `_du_bao_check` với mutant tại phép so cho `[0,8,8]`, chỉ-cũ `[0,0,8]`, chỉ-mới `[0,8,0]`, luôn-đúng `[0,0,0]`. Schema v2 chưa có nên không khai đã chạy production A4. |
| F6 — `so-do-khong-khop` | **ĐÓNG** | `scratch/measure.py`: tại head mới `23e16979`, **+161/−2, net159**, 2047→2206, toàn bộ năm vị trí symbol mới đúng. Bảng bốn hạn gây sai “lần lượt” đã bỏ khỏi nguồn hằng; hạn muộn nhất mới `2026-09-08T10:17:12Z` và giờ mốc đúng qua Q6 độc lập. Tổng 422–663 khớp phép cộng. |
| F7 — `baseline-nghiem-thu-bi-troi` | **ĐÓNG** | A16:216 dùng OID bất biến, tách kiểm sync. `scratch/seams.json`, A16: master thêm `unrelated.txt` độc lập; diff B→H trước/sau byte-equal, đúng ba đường +1/−0; diff ref động→H có thêm `0 1 unrelated.txt`. Cần ghi OID baseline thực trong lease/evidence khi thi công, không chỉ điền ref. |

## Findings

### F8 — P2 — `dot-bien-khong-khop-seam-consumer`

**Vị trí:** SPEC:151,188,193–195,222 (A22(iii)); đối chiếu `cay-kho/ops/lease_publish.py:1937,1944` và bộ quét :529–541.

M14 được đặt trong `_du_bao_ai_dang_giu`, nhưng `lenh_ai_dang_giu` gọi `_quet_lease_toan_kho` **trước** hàm ấy. YAML hỏng làm bộ quét ném `Chan(12)` ngay, kể cả có một bản L hợp lệ ở side. A22(iii) đòi trạng thái `KHONG_XAC_DINH` nhưng không chỉ rõ đây là unit của bộ phân loại hay đầu ra CLI. Theo đường CLI hiện tại, không tới được seam để phát dòng đó hoặc giết mutant “làm tròn trạng thái”. Tự stub scanner để qua không chứng minh hành vi CLI; sửa scanner để bỏ lỗi lại đụng bất biến luật cũ.

**Đã chạy:** `python3 -B scratch/repro_m14.py > scratch/m14.json`; fixture `A22iii` là kho Git thường, bare local, tệp L YAML lỗi cú pháp thông thường, không chuỗi thoát/helper/object giả. Hook quan sát gắn đúng hàm dự báo hiện tại:

```text
không cờ: rc=12, chỉ có dòng PHẠM_VI trước Chan
có cờ:    rc=12, hook_called=False, forecast=[]
mô hình thay thân hàm dự báo: vẫn hook_called=False, forecast=[]
```

**Sửa:** định rõ hai ca: unit gọi trực tiếp hàm đọc/phân loại cây để đo YAML hỏng→`KHONG_XAC_DINH`; CLI giữ lỗi scanner và mọi dòng không dự báo của baseline, không đòi dòng M14 khi preflight đã chặn. Hoặc nêu tường minh cách điều phối khác và chứng minh bất biến. HINT chọn phương án unit + CLI để không thay luật cũ. P2 vì thiếu hợp đồng seam khiến executor phải tự quyết; không gọi đây là lỗi fail-open đã ship.

### F9 — P2 — `du-bao-ba-trang-thai-mo-ho`

**Vị trí:** SPEC:184–191,222.

Bảng ba trạng thái chưa là một hàm đơn trị. Với hai bản L trong **cùng cây**, một bản L→N đối xứng và một bản L không bia mộ, cả điều kiện tồn tại `CHE` lẫn điều kiện trùng L mâu thuẫn `KHONG_XAC_DINH` đều đúng. Không có thứ tự ưu tiên. Chuyển mâu thuẫn sang **đầu N** còn không được hàng lỗi đề cập: `_bia_mo_doi_xung` chỉ cần thấy một N trỏ ngược là True, dù cây còn một N khác không trỏ ngược. Cặp chia nhánh đã được xử lý đúng; truyền đúng cây chưa đủ xử lý ID mâu thuẫn trong cây.

YAML hỏng cũng không bảo đảm đọc được `lease_id == L`; cần nói rõ lỗi parse không gán được ID ảnh hưởng những ID nào, thay vì buộc executor tự suy ID bằng tên/regex. Vì đây là dự báo, thiếu sót làm sai/không nhất quán trạng thái dự báo, không tự đổi authority.

**Đã chạy:** cùng script M14, hai fixture `duplicate-L`/`duplicate-N`:

```text
duplicate-L: CHE_exists=True; KXD_conflict=True
duplicate-N: mô hình dùng đúng cây + _bia_mo_doi_xung ⇒ CHE
```

Lệnh hiện tại vẫn rc11 nhờ L sống; không cần nguồn giả. Mô hình cho KXD ở duplicate-L là **lựa chọn ưu tiên của reviewer**, không phải điều đặc tả hiện đã chốt. Mô hình cho CHE ở duplicate-N chứng minh lỗ của cách triển khai trực tiếp theo hàng CHE; không giả danh output r2.

**Sửa:** chốt ưu tiên lỗi→CHE→KHONG; kiểm mâu thuẫn ở cả hai đầu L/N trước khi hỏi tồn tại cặp; định nghĩa mâu thuẫn, xử lý sai kiểu và lỗi parse không có ID. Thêm hai ca riêng trùng L/trùng N và phản chứng gỡ riêng mỗi chốt. HINT giữ lỗi trong phạm vi dự báo.

### F10 — P2 — `thieu-nhanh-nghiem-thu`

**Vị trí:** M14 SPEC:151 so với A19:219; xem thêm ma trận A19–A22 tại :219–228.

M14 đòi dòng không dự báo **giống hệt**, kể cả so với luật trước A1a. A19 chỉ so **tập dòng** của hai lần chạy ứng viên. Tập làm mất thứ tự và số lần xuất hiện; nó không chứng minh bất biến đã hứa. Cũng chưa có phép so với mã baseline bất biến: hai chế độ cùng đổi đầu ra cũ vẫn có thể bằng nhau. Ca rc11/chứa L có răng với mutant xoá L, nhưng không bao phủ toàn bộ bất biến.

**Đã chạy:** `scratch/repro_m14.py`, `A19_set_hole`: giữ mọi dữ liệu và rc11/holder L, chỉ thêm một dòng PHẠM_VI trùng trong lượt có dự báo:

```text
A19_set_equal=True
M14_sequence_equal=False
```

Dòng dự báo CHE vẫn có đúng như control. Do đó một mutant vi phạm M14 vẫn qua chính phép đo mà A19 mô tả.

**Sửa:** cùng map ref và clock, so ba lần: baseline bất biến không cờ, ứng viên không cờ, ứng viên có cờ; so **dãy** dòng (giữ số lần/thứ tự) hoặc bytes sau khi loại dòng DU_BAO, rc, holder và stderr. Thêm mutant in lặp/đổi thứ tự và thay đầu ra ở cả hai chế độ. Không dùng `origin/master` trôi làm mã baseline; dùng OID nghiệm thu A16.

Ma trận mutant của M14 cũng cần khai bằng tập đích thực đo: “hỏi mọi ref” có thể giết cả A20 và A22(i); bỏ toàn bộ dòng trạng thái giết nhiều ca. Đó không chứng minh hai ca vô dụng. Điều khoản :228 cho phép giải thích collateral, nên **không tính việc một mutant giết nhiều ca thành finding riêng**. HINT làm rõ tập đích thay vì ép mutant nhận diện tên ca để chỉ đỏ một chỗ.

### F11 — P1 — `q6-thieu-kiem-id-ten`

**Vị trí:** SPEC:141,268–291 (thuật toán §8.2 và script được chỉ định); `do_q6.py:9–20`; luật cha `cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md:377–380`.

Q6 yêu cầu dẫn xuất cặp từ cây mốc và **kiểm hai chiều/ID/tên**. Thuật toán mới chỉ nêu parse/trùng/hai chiều; script lấy `str(lease_id)` làm khoá, không kiểm miền/kiểu ID, không so ID với tên tệp. Tệp YAML không phải mapping hoặc thiếu ID còn bị bỏ qua mà không vào `yaml_hong_hoac_trung`. Phép so digest khi chạy lại **cùng script** không chứng minh các chốt này đã chạy.

**Đã chạy:** `python3 -B scratch/repro_q6.py > scratch/q6.json`. Trong các kho nhỏ bình thường, x→y đối xứng, y còn hạn tại clock ghim:

```text
valid:      x.yaml lease_id=x; y.yaml lease_id=y ⇒ rc0, giữ (x,y)
wrong-name: unrelated.yaml lease_id=x; y.yaml lease_id=y ⇒ rc0, giữ (x,y)
non-map:    thêm bad.yaml là danh sách ⇒ rc0, yaml_hong_hoac_trung=[]
missing-id: thêm bad.yaml thiếu ID    ⇒ rc0, yaml_hong_hoac_trung=[]
duplicate:  thêm bản cùng ID         ⇒ rc3 (chốt này có hoạt động)
```

Hai ca đầu có cùng OID blob và cùng digest biểu diễn cặp; đổi riêng tên làm hỏng điều kiện ID/tên nhưng bằng chứng ghim vẫn xanh. Đây là **mâu thuẫn với phép kiểm bắt buộc của Q6**, nên P1 theo thang của prompt. Không nâng thành cáo buộc cache xoá holder, và không nói tập production hiện rỗng đã mở quyền.

**Đo kiểm giới hạn ảnh hưởng trên nguồn thật:** walker độc lập đi từ chiều cũ→mới thay vì vòng mới→cũ của script vẫn cho **11** cặp, cùng digest, **không đầu nào trong 11 cặp sai tên**. 92 tài liệu có ID gồm **89 `.yaml` và 3 `.yaml.nhap`**; ba bản nháp không thuộc 11 cặp. Nếu gọi 92 là miền lease đã kiểm tên thì sai nghĩa; đó là số tài liệu script nạp. Đây là phần cần làm rõ cùng F11, không thêm một finding số đo riêng. Tại C được chốt mọi lease mới trong 11 cặp đã hết hạn; hằng vẫn phải rỗng sau khi bổ sung kiểm.

**Sửa:** khai miền lease/miền chẩn đoán; kiểm kiểu/miền ID, tên của cả hai đầu và schema liên quan **trước** lọc (b); fail rc3 cho lỗi trong miền lease, không ép `str` hay biến schema sai thành rỗng. Thêm ca đổi riêng tên đầu cặp và đối chứng sạch, in provenance path/blob. Sửa script hiện vật review ở nhánh riêng theo :114–115, không mở write_set A1a. HINT sửa hợp đồng trong SPEC; executor vẫn phải sửa script rồi chạy lại, không nhận HINT là bằng chứng code đã sửa.

## Bảng đo lại

Mọi giờ UTC ngày 26-09-2026. `M` = `python3 -B scratch/measure.py`; `Q` = lệnh `python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z`; `I` = `python3 -B scratch/repro_q6.py`; `C` = `python3 -B scratch/checks.py`. JSON giữ lệnh/rc và output tương ứng; số dòng là số tại blob được nêu, không neo bằng ref động.

| Số SPEC / lời khai | Số reviewer đo | Lệnh / hiện vật | Giờ UTC |
|---|---|---|---|
| SPEC sha256 `1bfdc7bb…`, 316 dòng | Đúng full SHA header; 316 dòng, 36.433 B; bằng tệp ở mirror | M, `scratch/measure.json` | 22:57:13 |
| HEAD `981b9ea1`; master `24c48e28` | Khớp full OID; tree ở đầu verdict | M | 22:57:13 |
| r1 `64f92d40…`, 211 dòng, 21.775 B | Khớp cả ba; nháp1 `a5aacafa…` cũng khớp | M | 22:57:13 |
| 11 hai chiều / 3 một chiều / 92 lease | 11 / 3 / **92 tài liệu có ID** = 89 `.yaml` + 3 `.yaml.nhap`; xem F11 về nghĩa miền đầu vào | Q byte-match `q6-do-2026-09-26.json`; I walker độc lập | 22:56:18; 23:05 |
| Digest `8f372ccd…` | `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48` | Q và I tính độc lập cùng JSON compact, sorted tuple4 | cùng trên |
| 0 YAML hỏng/trùng, 0 KXD; (b) 0 | Script rc0, đúng các số trên nguồn thật. Không suy thành validator đủ — F11 | Q / `scratch/q6-rerun.json` | 22:56:18 |
| Hạn muộn nhất `2026-09-08T10:17:12Z` | Đúng; tại 10:17:11 giữ1, tại 10:17:12 giữ0 | I / `real_clocks` | 23:05 |
| Giờ mốc `2026-09-10T04:55:37Z` | `%cI` = `2026-09-10T11:55:37+07:00`, cùng thời điểm | M; `git -C cay-kho show -s --format=%H\ %cI 0721811` | 22:57:13 |
| Clock ≥ hạn muộn nhất không đổi kết quả | Đúng với cây này: tại biên, giờ mốc, 26-09 22:50 và 2099 đều giữ0; chứng minh tổng quát ở dưới | I | 23:05 |
| Mốc tổ tiên HEAD/master; full40 | Tổ tiên HEAD rc0; mốc đúng40. OID khác vẫn tổ tiên bị chốt equality bắt; 39 ký tự Git vẫn nhận nhưng chốt format bắt; object thiếu Git rc128 | `scratch/a6.json` | 23:05 |
| #589 head23e16979: +161/−2, net159 | Khớp; test file riêng +2900/−5 như E10 | M, `git diff --numstat 24c48e28 23e16979 -- …` | 22:57:13 |
| #589 source 2206; BIA:1103, descriptor:1107, forecast-check:1921, forecast-holder:1951, holder:2093 | Khớp **tất cả** | M | 22:57:13 |
| Source nền2047, symbol §1 | Khớp các vị trí 934/942/944/948/1021/1258/1277/1281/1307/1386/1722/1762/1934/482 | M | 22:57:13 |
| Test7288, 168 hàm; workflow178, checkout57, upload173 | Khớp số tĩnh; không nhận lại 168/168 từ lần chạy bị huỷ | M | 22:57:13 |
| A6: gate fetch-depth0, ci.yml:90 | Đúng, checkout tại86, fetch-depth tại90 | `sed -n '84,94p' cay-kho/.github/workflows/ci.yml` | 23:02 |
| Ước tổng422–663 | min=120+5+50+2+25+110+110=422; max=180+12+70+6+45+180+170=663 | M | 22:57:13 |
| E11:435 heads | **435/435**, hiệu hai chiều rỗng; endpoint là bare local | M, local ls-remote / for-each-ref | 22:57:13 |
| §1/§2 số quét cũ495/465/234/10,428 ref | Snapshot hiện tại **502/471/240/10**,435 heads; nguồn chẩn đoán mọi ref, không dùng ghim Q6 | C / `all_refs_diagnostic.log` | 23:03:34–23:04 |
| Holder Python r17-g15, mỗi đường1 (15:47–15:56) | Hiện mỗi đường1, rc11 nhưng ID **r21-g19**; workflow/spec vẫn0 rc0; target ci registry hiện3 rc11 | C / `checks.json` | 23:03–23:04 |
| t123 không lan bia mộ ngoài phạm vi | **1/1**, đã chạy1, bỏ qua0, rc0 | C / `t123.log` | 23:03:34 |
| A15 doctrine-scan / adr-song | rc0: 10 tệp, 0 chỗ chép; rc0:50 ADR/50 dòng, khớp1–1 | C / `doctrine.log`, `adr.log` | 23:03:34 |

Các số quét mọi ref/holder thay đổi so số **cũ có timestamp**, trong khi master vẫn đứng yên: ref mới chứa lease thế hệ mới. Không quy drift đó thành finding vì SPEC đã ghi thời điểm cũ và không dùng nó làm nguồn hằng. Cần đo lại lúc cấp lease như §8.3 đã yêu cầu; số holder hiện tại **chưa** cho phép cấp A1a.

Chứng minh lời khai mọi C≥`2026-09-08T10:17:12Z`: tập 11 cặp là cố định theo cây; từng hạn lease mới ≤ mốc biên ấy. `trang_thai` kiểm `het <= now` **trước** bia mộ. Với clock UTC hợp lệ ở miền datetime, tất cả luôn `HET_HAN`, không vào `giu`/`kxd`; không cần thử mọi thời điểm. Chọn giờ commit làm C hợp lý và tái lập được. Phép đo không chứng nhận lại thời gian REST land trên GitHub.

## Nghiệm thu

Đây là đánh giá khả năng đo của **đặc tả**, không phải chứng nhận r2 đã qua suite.

| Ca | Kết luận |
|---|---|
| A1–A3 | Kế thừa r1, phân biệt schema/tập khoá, audit-only và khoá vào digest. Chưa có schema v2 để nghiệm thu mã. |
| A4 | Đủ hai khoá × None/thiếu/chuỗi và runner; mô hình bốn mutant có bốn đích riêng. |
| A5 | Giữ profile production rỗng; không tự duyệt manifest để vượt cổng. |
| A6 | Equality độc lập+40hex+ancestry có răng, kể cả Git chấp nhận OID viết ngắn. Ngoại lệ archive không được dùng trong CI checkout có .git. |
| A7 | Đủ ba mutant và hai ca âm; đã chạy consumer thật. Mutant luôn-đúng giết cả hai âm đúng như SPEC khai. |
| A7b | Consumer thật với hằng rỗng cho Z→W sau mốc dự báo8. Mô hình mutant nạp tuple của cây hiện tại cho0. Cùng script Q6 kiểm cây mốc đứng yên/cây sau thêm cặp có hiệu lực. Cần thêm validator ID/tên cho dẫn xuất, F11; A7b hiện không đo nó. |
| A8–A12 | Kế thừa B1–B5 r1. Không soạn payload byte/escape mới trong lượt này; các hướng ấy chỉ mô tả. A11 có ba close mutant riêng; nền thiếu /proc phải ghi không đo được, không khai pass. |
| A13 | Đếm tĩnh168 khớp. Chỉ t123 được chạy trọn và dùng làm bằng chứng ở lượt này; chưa có số ca mới nên không thể nghiệm thu N mới. |
| A14 | Chưa chạy actionlint/shellcheck delta cho implementation r2; không khai xanh. |
| A15 | Hai cổng chạy trực tiếp qua subprocess, rc đọc riêng: đều0 với bằng chứng dương ở bảng. |
| A16 | Baseline bất biến đúng protocol; kiểm thực bằng đồ thị Git thường có drift độc lập. |
| A17 | Đủ ba lỗi tag/SHA/count; hằng test độc lập. Không suy từ việc Q1 được chủ kho duyệt thành đã xác minh tag online trong lượt này. |
| A18 | Đã đo consumer thật và các mutant với Q3 ghim tạm trong module của reviewer; không sửa mirror. Gỡ policy-present sinh TypeError nên test phải đòi đúng Chan12 — bản nháp2 đã ghi đúng điều này. |
| A19 | Chốt giữ L/rc11 có răng; chốt toàn bộ đầu ra chưa đủ (F10). |
| A20 | Side-only ra KHONG trên mô hình; mutant tìm mọi ref ra CHE. |
| A21 | Tự kiểm bẫy thành công: blob bia mộ được scanner đại diện bằng `refs/remotes/origin/a-first`, không phải master. Mutant dựa representative chỉ giết A21 trong bộ fixture đã chạy. |
| A22 | Cặp chia nhánh đã có đường đo; ref vắng dựng được với preflight cũ vẫn qua; YAML hỏng cần tách seam (F8); thiếu ca trùng L/N (F9). Không được coi trạng thái helper là kết quả của CLI. |

**Ma trận mô hình M14 đã chạy** (`scratch/m14.json`). Control gọi đúng `lenh_ai_dang_giu` của mirror; reviewer chỉ thay helper dự báo bằng mô hình và mutant nêu tên. Trong các ca CLI có thể tới helper, dãy dòng không dự báo/rc bằng baseline hiện tại. Đây là kiểm tra tính khả thi, không phải implementation r2.

| Mutant | Ca đổi màu thực đo |
|---|---|
| CHE thì xoá L khỏi danh sách scanner đang dùng | A19 |
| Bỏ toàn bộ dòng trạng thái | A19, A20, A21, A22(i), A22(ii) |
| Tìm cặp đối xứng trên mọi ref | A20, A22(i) |
| Hỏi `muc['ref']` | A21 |
| Chỉ kiểm chiều ngược trên toàn kho | A22(i) |
| Làm tròn lỗi đối xứng thành KHONG | A22(i); YAML hỏng CLI chưa tới seam để đổi màu |
| Ném Chan khi ref vắng | A22(ii) |
| In lặp PHẠM_VI trong lượt dự báo | **Không bị phép so tập A19 giết**, vi phạm phép so dãy M14 (F10) |

Vì vậy không thể khai tất cả mutant đều đúng **một** ca đích theo câu chữ hiện tại. Có mutant dùng chung cố ý giết nhiều ca; hãy ghi tập đích và scope thật. Với A22(iii), thiếu đổi màu là do chưa tới seam, không phải “tương đương” A22(i).

**Luật và write_set:** §3.2/§4 yêu cầu Issue+lease, đặc tả chưa đóng băng không cấp việc; §8 yêu cầu review độc lập exact SHA; §12 checkpoint E8 đã thay cách làm, không chỉ thêm chốt. Chủ kho đã cho 4 lời gọi theo đầu vào, không tự reset ngân sách; lượt này là2/4. ADR-0044 vẫn ≤3 tệp/≤300 dòng thêm; 422–663 chỉ là ước, cần ngoại lệ hoặc revision tách trước lease. ADR-0047 vẫn Proposed, profile production vẫn rỗng; không trao authority cho dòng dự báo, không tự điền nguồn tin cậy. Q1/Q3 là giá trị EVIDENCE cung cấp, không phải readback mới của reviewer.

Ba đường write_set đủ cho phần mã/test/workflow được mô tả, kể cả helper phân loại trong cùng `lease_publish.py`; các sửa script/evidence do F11 phải ở nhánh review riêng như SPEC:114–115. Không thêm packet_loop/docs/leases vào A1a. M12 chỉ sửa upload-artifact; không lấy review này làm quyền sửa checkout hoặc gọi CI tay. `doctrine-scan`/`adr-song` xác nhận cấu trúc tài liệu, không thay phép đối chiếu ngữ nghĩa Q6 ở F11.

## Phản chứng đã chạy

1. `python3 -B do_q6.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z > scratch/q6-rerun.json` — rc0; `cmp scratch/q6-rerun.json q6-do-2026-09-26.json` rc0.
2. `python3 -B scratch/measure.py > scratch/measure.json` — rc0; số dòng/symbol/hash/numstat/ref/tổng ước.
3. `python3 -B scratch/repro_q6.py > scratch/q6.json` — rc0 của harness; JSON lưu riêng rc0/3 từng lần gọi script. Gồm cặp sạch, sai tên, non-map, thiếu ID, trùng, một chiều, thay tiếp, cây ghim/cây sau, biên clock và walker độc lập.
4. `python3 -B scratch/repro_m14.py > scratch/m14.json` — rc0; kho Git thường và bare local; ghi gọi helper, rc, các dòng trước/sau; cache OID thay trong scratch, endpoint bare giữ nguyên. Mô hình có chủ ý riêng cho M14 chưa triển khai.
5. `python3 -B scratch/repro_seams.py > scratch/seams.json` — rc0; A18/A7 chạy code consumer thật nạp trong bộ nhớ và scoped source mutants; A4 là mô hình; A7b mutant là mô hình nạp tuple từ cây sau (không khai đã có production derivation); A16 dùng commit Git thường.
6. `python3 -B scratch/checks.py > scratch/checks.json` — rc0; lưu rc trực tiếp từng subprocess. Chạy chọn đúng `--chi-ca=t123`, hai cổng doctrine/ADR, chẩn đoán mọi ref và holder thật.
7. A6 ở `scratch/a6.json`: các lệnh `git -C cay-kho merge-base --is-ancestor <giá trị> 981b9ea1d4bfaa0511cfbc8d9bdee9d8c151c86f`, so riêng equality/regex; không qua pipeline để suy rc.
8. `python3 -B scratch/make_hint.py`; `patch --dry-run -p0 < HINT.patch` — rc0. Patch chỉ là gợi ý sửa SPEC, chưa áp lên SPEC/mirror. Có hunk cho cả bốn finding P1/P2.

**Hướng chỉ MÔ TẢ:** đường thoát cây, tên đồng tự Unicode, payload chuỗi thoát/byte không hợp lệ, helper Git giả, object giả/cạnh giả. Không tự soạn hoặc chạy các payload ấy. Các counterexample ở đây dùng tên ASCII bình thường, YAML/JSON và commit/blob do Git thật tạo; YAML lỗi cú pháp ở A22 không chứa escape payload.

**Lần chạy không dùng làm bằng chứng:** ban đầu gõ `--chi-ca t123` (có dấu cách); runner chỉ nhận `--chi-ca=t123`, nên đã bắt đầu toàn suite. Đã ngắt bằng Ctrl-C, rc130; không dùng log đó để khẳng định N/N hoặc closure. Lượt chọn đúng với TMPDIR dưới cwd đã chạy lại trọn vẹn. Không tự soạn các fixture nhạy cảm trong suite. `git status --porcelain` trên mirror vẫn rỗng; không có pyc trong mirror.

## KHÔNG ĐO ĐƯỢC

- Không đọc lại GitHub/REST hoặc mạng: E8 là quyết định được cung cấp để áp dụng, không phải quyết định reviewer mới xác thực online. Không chứng nhận lại Q1 tag, Q3 body1379B, #589 trạng thái open/merged, giờ land thực, advertisement máy chủ hoặc quyền người đăng.
- Tập435 ref đã so được với **bare local**; OID cache không được chứng nhận là OID máy chủ. Không lấy phép đo này cấp authority mới.
- Chưa có implementation r2/schema v2/hàm phân loại M14 để chứng nhận pass; mô hình chỉ chứng minh hợp đồng hoặc phản chứng lỗ nghiệm thu. Chưa đo delta actionlint/shellcheck, full suite N mới, số dòng thi công thật, số test v1 bị ảnh hưởng, profile production, ngân sách object, Windows hay C1a1b.
- Không tái tạo snapshot ref 428 lúc15:47 hay run168/168 lịch sử. Drift hiện tại ghi riêng ở bảng, không sửa lịch sử thành số mới.
- Không xác minh được backend model variant/effort; tự khai đúng phần biết được ở header, không nhận chỉ thị `gpt-6-astra/high` là measurement.

`HINT.patch` không rỗng. Đây là patch-as-hint cho mọi P1/P2; executor phải tự dẫn xuất, sửa script liên quan, đo lại rồi xin review trên băm đặc tả mới. Review này không cấp lease, không phê duyệt ngoại lệ ADR-0044, không đóng băng hoặc merge.
