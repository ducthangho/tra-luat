verdict: changes_requested
reviewed_spec_sha256: a5aacafac1e69c78ad3dd56e5c977527600fe6dad320656dd7ed29688f7bc313
reviewed_sha: f8a37c046f37f1b094d125b3a0c9f833bd0e83a7
P1: 2   P2: 5   P3: 0
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); tên biến thể và effort thực tế KHÔNG ĐO ĐƯỢC

Review độc lập đặc tả r2, chưa có implementation r2. Áp ngưỡng của yêu cầu: không còn P1/P2/P3 mới approve. Bản ghi sớm đã được tạo trước phép đo dài; bản này thay kết luận tạm. Mọi giờ dưới đây là UTC ngày 26-09-2026. Không mạng; không sửa `cay-kho/`. Bộ suite chạy trên bản sao `git archive` trong `scratch/`.

Hai P1 thuộc thiết kế nguồn thẩm quyền: M14 nâng cache thành nguồn được phép loại holder; M4 đổi nguồn/mốc của Q6 mà quyết định (b) trong E1 chỉ đổi bộ lọc. Đây không phải lỗi có thể chữa chỉ bằng thêm test happy path.

## Findings

### F1 — P1 — `nguon-duoc-tin-ma-chua-xac-minh`

**Vị trí:** SPEC:139, 159–171 (M14, §5.1), A19–A22:194–197.

`refs/remotes/origin/master` là ref ghi được bởi người có quyền ghi kho cục bộ. Tên ấy không chứng minh commit đã review/merge. `_quet_lease_toan_kho` chỉ so tên máy chủ với tên cache (`lease_publish.py:300–310, 508–513`); không so OID, không dùng discovery canonical/profile. M14 còn cho caller chọn ref được ưu tiên qua `--nhanh-mac-dinh`. Khác luật cũ giữ lại một bản L sống ở ref khác, luật mới loại **mọi** bản L khi thấy bia mộ trên ref được gọi là canonical.

Ngoài ra `_bia_mo_doi_xung` (:575–598) tìm lease mới trên **toàn bộ cac_lease**. Bia mộ cũ trên default cộng chiều ngược chỉ ở nhánh phụ cũng trả True. Do đó câu “bia mộ chỉ trên nhánh phụ không che toàn kho” chưa chặn trường hợp **một nửa** chứng cứ do nhánh phụ cung cấp.

**Đã chạy:** `TMPDIR="$PWD/scratch" python3 -B scratch/repro.py` → `scratch/repro.log`. Kho thường, bare local, lease fixture; không helper Git giả. `model_M14_*` là mô hình tối thiểu đúng quy tắc đề xuất, **không phải implementation đã ship**; `current_rc` gọi chính `lenh_ai_dang_giu` của mirror.

```text
cache-before:       current_rc=11, model_M14_rc=11, holders=[L]
CACHE_NAME_SETS_EQUAL True; SERVER_OID != CACHE_OID
cache-after:        current_rc=11, model_M14_rc=0, holders=[]
cli-selects-private: current_rc=11, model_M14_rc=0, holders=[]
split-pair:         current_rc=11, model_M14_rc=0, holders=[]
```

Fixture giữ một bản L sống trên `z-live`; chỉ `git update-ref` cache default đổi, máy chủ bare không đổi. Đây là counterexample **mất holder mới do M14**, không nhận công cho lỗ cache vốn có của luật cũ. `split-pair` giữ bản L không bia mộ trên side, đầu mới N chỉ có trên side; default không đủ hai chiều để kết luận thay hợp lệ.

**Sửa:** trước phép loại holder, yêu cầu snapshot đủ ba lớp ADR-0047, map tên/OID và symref canonical, object/edge xác minh; ràng buộc provenance của **cả hai đầu** bia mộ. Cờ chỉ đối chiếu tên, không chọn authority. Không xác minh được ⇒ 12. Thêm từng ca cache khác OID, nhánh cờ sai, cặp chia nhánh, profile chưa duyệt. Không tự điền profile để vượt A5.

**Hệ quả scope:** profile production vẫn rỗng, duyệt profile ngoài A1a. Cần checkpoint quyết định phụ thuộc nguồn được duyệt hoặc chuyển thay đổi verdict M14 sang A1b, không vừa tuyên bố sửa production vừa chỉ có fixture nội bộ. Hình dạng này đã có bộ đếm 6 ở §7, nay là lần 7: protocol §12 đòi xem lại cách làm. Trần 4 lời gọi không miễn checkpoint đó.

### F2 — P1 — `mien-lich-su-vuot-quyet-dinh`

**Vị trí:** SPEC:129 (M4), 184/186 (A6/A7b), 240–265 (§8.2).

Spec cha r9 Q6 (`cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md:377–381`) yêu cầu OID readback sau A0, cặp dẫn xuất từ **đúng cây mốc**, kiểm ID/tên/hai chiều, hai blob và băm biểu diễn; ghi rõ “Không lấy HEAD lúc A1” và “Feature tomb không bổ sung lịch sử”. E1 quyết định (b) chỉ nói **lọc cặp có lease mới còn hiệu lực**, không trao quyền đổi nguồn này.

R2 thay thành commit master executor chọn rồi quét **mọi ref**. OID master không định danh tập đầu vào: nhánh phụ thay đổi mà master đứng yên vẫn thêm cặp vào hằng có thẩm quyền. Đồng thời không ghim clock, nên ngay cả mọi OID ref đứng yên, hết hạn cũng đổi tập. A6 kiểm ancestry và A7b fixture thuật toán đều không chứng minh hằng ghim đúng nguồn/mốc.

**Đã chạy:** `TMPDIR="$PWD/scratch" python3 -B scratch/repro.py`:

```text
SNAPSHOT_A <cùng OID master> []
SNAPSHOT_B <cùng OID master> [['L', 'N']]
SNAPSHOT_C_SAME_REFS_LATER <cùng OID master> []
```

A→B chỉ tiến `z-side` trên bare và cache; giờ lọc vẫn `2026-09-26T15:48:00Z`. B→C giữ mọi ref, đổi clock đến hạn. Hai endpoint đều local. Đọc nguồn luật: `sed -n '375,385p' cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md`.

**Sửa:** giữ Q6 và chỉ áp bộ lọc (b), hoặc xin quyết định bổ sung có phạm vi cho việc đổi **nguồn/mốc**, đưa vào revision trước đóng băng. Đóng băng clock và provenance (OID, blob/path, digest tập); đo lại hằng thật từ receipt, thêm phản chứng cây mốc đứng yên/feature thay. Bảng 4 cặp hiện tại là chẩn đoán quét toàn ref, chưa là chứng cứ tập ghim theo Q6. `HINT.patch` không tự cấp quyết định đổi Q6.

### F3 — P2 — `con-hieu-luc-bo-mat-trang-thai-thu-ba`

**Vị trí:** SPEC:247–248, 186 (thuật toán (b), A7b), đối chiếu M14/A20.

“Có bản CÒN_HẠN và không bản nào có bia mộ đối xứng True” chưa tương đương “còn hiệu lực” của cổng:

* Lease mới N có bia mộ **một chiều** được coi là còn hiệu lực bởi thuật toán vì False không phải True, trong khi reader báo KHÔNG_XÁC_ĐỊNH.
* N sống trên default nhưng có bản bị thay hai chiều **chỉ trên side** bị loại khỏi (b), trong khi chính M14/A20 và luật hiện tại vẫn giữ N trên default.

**Đã chạy:** cùng `scratch/repro.py`:

```text
B_ONE_WAY [['L', 'N']]
B_ONE_WAY_READER 12 KHÔNG_XÁC_ĐỊNH: bia mộ một chiều 'N' -> 'missing' ...
B_SIDE_ONLY [['N', 'P']]
b-side-only-reader: current_rc=11, model_M14_holders=['N']
```

Vế hai không có `(L,N)` dù N vẫn là holder. Đây là thiếu hợp đồng ba trạng thái và nguồn áp bia mộ, không phải trôi giờ. Ca mẫu 4 cặp sạch không bộc lộ nó.

**Sửa:** định nghĩa chung predicate hiệu lực theo snapshot nguồn đã chốt ở F1/F2, phân biệt không bia mộ/đã thay/không xác định; trạng thái thứ ba phải làm phép đo đỏ, không tự nhận vào tập. Bia mộ side không được làm chết canonical N. A7b cần hai ca này, với lỗi/đầu ra đích riêng. Phạm vi áp lỗi cho lease liên quan/còn hạn phải rõ, tránh làm mất hành vi t123 (lease hết hạn hoặc không chạm đường không lan lỗi).

### F4 — P2 — `dot-bien-khong-khop-seam-consumer`

**Vị trí:** SPEC:193 (A18), 138 (M13).

M13 ghim **digest**; consumer chỉ so hai chuỗi hex ở :1859. Nó không nhận và không băm body comment. Vì vậy A18 đang yêu cầu đột biến “`.strip()` trước khi băm” ở một seam chưa tồn tại trong mục tiêu. Cho hai digest khác nhau vào consumer chứng minh phép so digest, không chứng minh producer băm bytes thô. Không kết luận cả A18 vô dụng: ca hash sai có răng với đúng đột biến consumer.

**Đã chạy:** `TMPDIR="$PWD/scratch" python3 -B scratch/q13.py` → `scratch/q13.log`:

```text
PIN True valid          rc=0; receipt.descriptor_q13_ghim=Q3
PIN True newline-hash   rc=12 tại descriptor
STRIP_MUTANT valid     rc=0
STRIP_MUTANT newline-hash rc=12 tại descriptor
GUARD_MUTATION drop-descriptor: newline-hash rc=0, wrong-hash rc=0
```

Đột biến `.strip()` tại **đầu vào thật là chuỗi hex** sống; chỉ xóa phép so thì ca đổi màu. Không có raw body trong E3 để tự kiểm sha256 của body online. Bốn guard policy/base đã chạy control và gỡ riêng; xem bảng nghiệm thu.

**Sửa:** ghi rõ A18 đo consumer so digest chính xác; dùng bỏ phép so hoặc cho phép thêm hash sai làm mutant. Readback bytes body/giờ/hash là bằng chứng producer riêng. Nếu thực sự muốn một ca băm body, phải nêu nguồn bytes fixture độc lập và hàm/seam cần đo, không giao executor tự thêm production behavior. Positive control phải mọi trường hợp lệ và có receipt, thay vì cho phép “dừng ở chốt kế tiếp” mà không chứng minh đường thành công.

### F5 — P2 — `thieu-nhanh-nghiem-thu`

**Vị trí:** SPEC:128/182 (M3/A4), 185 (A7).

A7 chỉ có “đúng cũ, sai mới” cho đột biến “so một vế”. Ca đó giết so-chỉ-cũ, **không** giết so-chỉ-mới. M3 còn đòi cả `image_os` và `image_version`, nhưng A4 chỉ nêu `image_os`; kiểm digest ở A3 không thay kiểm thiếu khoá/None của `image_version`.

**Đã chạy:** `TMPDIR="$PWD/scratch" python3 -B scratch/repro.py`:

```text
(cũ,mới)     chuẩn  mutant chỉ so mới
(L,N)          0          0
(L,other)      8          8
(other,N)      8          0
```

Sổ rỗng, hằng chỉ `(L,N)`; hàng âm ghi trong A7 vẫn xanh dưới mutant chỉ so mới. Đối chiếu A4: `sed -n '128p;182p' SPEC.md` in M3 có hai khoá, A4 chỉ một. Chưa có implementation v2 nên không khai đã chạy mutant `image_version`.

**Sửa:** thêm ca “sai cũ, đúng mới” và ánh xạ riêng hai mutant. A4 tham số hoá từng khoá, giữ khoá kia hợp lệ; mỗi khoá đo chuỗi/None/thiếu và đối chiếu runner.

### F6 — P2 — `so-do-khong-khop`

**Vị trí:** SPEC:65–67 (§1 PR #589), 260 (§8 thứ tự hạn).

Các sai số không chống đỡ thẩm quyền nên P2, không P1:

1. `+163 dòng` không phải dòng thêm hay tăng ròng của PR #589. Đo đúng là **+161/−2, tăng ròng 159**. 163 là tổng số dòng thay đổi. `2047 → 2206`, `BIA_MO_LICH_SU :944 → :1103` (+159).
2. Hạn “lần lượt” không khớp thứ tự bốn dòng bảng. Đúng lần lượt: **13:31, 00:00, 06:00, 05:02** ngày 27-09; không phải 00:00, 05:02, 06:00, 13:31. Mốc muộn nhất vẫn là 13:31 hôm sau; từ 15:48 là 21h43 ≈ **21,7 giờ** khi làm tròn một chữ số, không phải ~21,6. Quan hệ muộn nhất không cứu được ánh xạ hạn sai.

**Đã chạy:** `python3 -B scratch/numbers.py` và `python3 -B scratch/measure.py`:

```text
PR589_NUMSTAT 161 2 ops/lease_publish.py
LINES 24c48e28 2047
LINES 190def2f 2206
EXPIRY ci-registry-pretooluse-che-do-nhe-r1-g1-claude 2026-09-27T13:31:00Z
EXPIRY dang-lease-dau-truoc-kiem-sau-r17-g15-claude 2026-09-27T00:00:00Z
EXPIRY r378-symlink-doi-dac-quyen-r20-g20-claude 2026-09-27T06:00:00Z
EXPIRY wp570-bash-nen-r31-g31-opus 2026-09-27T05:02:00Z
```

**Sửa:** dùng numstat có đơn vị và tăng ròng riêng; sửa thứ tự hạn hoặc đưa hạn vào từng hàng.

### F7 — P2 — `baseline-nghiem-thu-bi-troi`

**Vị trí:** SPEC:191 (A16), đối chiếu protocol §3.2.1:177–188.

A16 lấy `origin/master..<head>` làm toàn bộ diff nghiệm thu, thiếu immutable acceptance baseline. Commit ngoài packet tiến master có thể làm chính diff không đổi bỗng chứa đường thứ tư; continuation/rebase cũng không được tự đổi baseline theo protocol. Ref động là dữ liệu đồng bộ, không phải OID hợp đồng nghiệm thu.

**Đã chạy:** `python3 -B scratch/baseline.py` → `scratch/baseline.log`. Candidate thêm đúng ba đường; master độc lập thêm `unrelated.txt`:

```text
BASELINE_DIFF: ba đường write_set, mỗi đường +1/−0
MOVING_MASTER_DIFF: ba đường trên, thêm 0 1 unrelated.txt
```

**Sửa:** A16 dùng OID immutable baseline và reviewed head được khai riêng trong evidence; thêm ca master tiến độc lập không đổi phạm vi đo. Phép kiểm sync/up-to-date vẫn riêng, không bị bỏ. HINT không dùng merge-base động để thay baseline.

## Bảng đo lại

Mã lệnh rút gọn trong bảng: `M = python3 -B scratch/measure.py`, `N = python3 -B scratch/numbers.py`, `B = python3 -B do_bia_mo.py cay-kho`. Các script/log nằm trong `scratch/`; dùng Git local tới `kho.git`, không phải readback GitHub.

| Đại lượng | Số SPEC | Số đo độc lập | Lệnh / bằng chứng | Giờ UTC |
|---|---|---|---|---|
| SHA256 r2, tracked source | a5aacafa… | Khớp đủ 64 hex, 288 dòng, 28.103 B; source HEAD khớp local SPEC | M; `sha256sum SPEC.md cay-kho/ops/specs/THU-HOI-LEASE-A1a-r2.md` | 16:01:38, 16:08 |
| HEAD; nền master | f8a37c04; 24c48e28 | Khớp hai OID đầy đủ. Ref nền là `refs/remotes/origin/master`; mirror không có local `master` | M | 16:01:38 |
| r1 | 211 dòng, 21.775 B, 64f92d40… | Khớp SPEC.r1 và blob tại `9db7145` | M; `git show 9db7145:ops/specs/THU-HOI-LEASE-A1a.md` | 16:01:38, 16:08:15 |
| lease_publish.py | 2047 dòng | 2047 | M | 16:01:38 |
| Hằng False/profile/BIA/descriptor | 934/942/944/948 | 934/942/944/948, giá trị đúng như khai | M | 16:01:38 |
| validator; profile; tập khoá; kiểm miền; digest | 1021/1258/1277/1281/1307 | Khớp cả năm | M | 16:01:38 |
| KhoObject; blob reader; dự báo; holder; scanner | 1386/1722/1762/1934/482 | Khớp cả năm | M | 16:01:38 |
| Consumer BIA, descriptor, receipt | 1783; 1857–1859; 1886 | Khớp các vị trí và consumer mô tả | `nl -ba cay-kho/ops/lease_publish.py` | 16:00–16:04 |
| Test file | 7288 dòng, 168 `def tNNN` | 7288, 168 (số tên lớn nhất 174 không phải số ca) | M | 16:01:38 |
| Suite nền | 168/168, bỏ qua 0, ~2m14 | **168/168 đạt; đã chạy=168, bỏ qua=0; rc=0**, ~136 giây | `git archive 24c48e28` vào scratch/suite; `TMPDIR="$PWD/scratch" python3 -B scratch/suite/ops/lease_publish_test.py > scratch/suite.log 2>&1`; lấy `$?` trực tiếp | 16:00:07–16:02:23 |
| Workflow | 178 dòng; checkout 57; upload 173 | 178; 57; 173, đều @v4 | M | 16:01:38 |
| r1 nền a270aea | 2042; BIA 939; forecast 1757; 166 ca; upload 147 | Khớp toàn bộ | N, `git show a270aea:<path>` | 16:06:09 |
| PR589 head 190def2f | +163 dòng, hunk -888,14 +888,173 | **+161/−2; net +159**, hunk khớp | N; `git diff --numstat 24c48e28 190def2f -- ops/lease_publish.py` | 16:06:09 |
| Ref names hai chiều | 428/428 lúc 15:47 | **430/430**, cả hai chiều rỗng tại mirror | M, local ls-remote + for-each-ref | 16:01:38 |
| Lease records / ID | 495/465 | **495/465** | B; scratch/b-measure.log | 16:00:07 và lần ghi log sau |
| Hai chiều / một chiều | 234/10 | **234/10** | B | cùng lần trên |
| Tập (b) | 4 cặp đúng danh sách | **Đúng 4 cặp, đúng danh sách**, cả clock replay 15:48:31 và clock review | N; scratch/numbers.log | chạy 16:06:09–16:06:15 |
| Hạn bốn lease theo thứ tự bảng | 00:00/05:02/06:00/13:31 | **13:31/00:00/06:00/05:02**, tất cả 27-09 | M | 16:01:38 |
| Muộn nhất sau giờ đo | ~21,6 giờ | 21h43 từ 15:48 đến 13:31 hôm sau ≈21,717h; làm tròn 21,7h (F6) | phép trừ timestamp | đối chiếu cuối 16:15 |
| M14 blob cũ | ab5b96a7, 4 remote ref | Khớp full OID `ab5b96a733e4459f96b443adfad97a5e9a8644de`, 4 ref, không bia mộ | M; ls-tree từng ref | 16:01:38 |
| M14 blob bia mộ | e6e2fa56, master +7 ref | Khớp full OID `e6e2fa56c4730dcc310470cddaa4c4dceaad2c22`, hiện **9 remote ref** (master +8), thêm nhánh spec | M | 16:01:38 |
| Representative blob bia mộ | ref phụ, không master | `refs/heads/claude/spec-a1a-r2-20260926` | M | 16:01:38 |
| Holder hai file Python | mỗi đường 1, rc11 | Khớp `dang-lease-dau-truoc-kiem-sau-r17-g15-claude` | M gọi trực tiếp lenh_ai_dang_giu | 16:01–16:02 |
| Workflow/spec path holder | 0, rc0 | 0, rc0 trên hai đường exact | M | 16:01–16:02 |
| M14 target ci registry | 2, rc11 | Khớp hai ID E5 | M | 16:01–16:02 |
| Ước tổng dòng | 392–611 | Tổng các số hạng đúng 392–611; không phải numstat thi công | N | 16:06:09 |
| C1a1a revision 5 | descriptor null/hex64 | Khớp blob ở ref được chỉ định, dòng 61/120 | `git show refs/remotes/origin/claude/spec-c1a1-doc-receipt-20260925:ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md` | 16:07:16 |

Ref 430 thay 428 và blob 9 thay 8 phù hợp drift mirror đã khai ở E7; không gán thành finding thẩm quyền, cũng không giả vờ đã khôi phục advertisement thật lúc 15:47. Lịch sử 473 ref / 350 tệp / 155/6 của r1 không tái tạo được từ map hiện tại; chỉ số file/line/function ở commit cũ tái đo được. Các số vòng lặp hình dạng 2/3/1/6 đã đối chiếu bảng r9:575–580; lịch sử số lượt online không được chứng nhận lại.

## Nghiệm thu A1–A22

“Có thể đo” dưới đây là đánh giá hợp đồng test; không phải tuyên bố implementation r2 đã đạt. A7b là tiêu chí bổ sung, không bị bỏ vì tên mục chỉ ghi A1–A22.

| Ca | Kết luận kiểm tra |
|---|---|
| A1 | Có thể đỏ bằng sai version/tập khoá. Executor cần liệt kê tập schema v2 hữu hạn; không suy “băm nhị phân khác” thành khoá tuỳ ý. |
| A2 | Có thể đỏ khi AUDIT đi lại vào digest; dùng hai profile chỉ khác audit và qua kiểm miền. |
| A3 | Có thể đỏ riêng từng khoá bắt buộc. Cần hiểu A2/A3 là hai mutant khác nhau với dấu vân tay khác nhau, không đòi một mutant làm hai điều ngược nhau cùng lúc. |
| A4 | Thiếu ma trận `image_version`, F5. |
| A5 | Hợp lệ; giữ PROFILE rỗng là fail-close. Chính điều này khiến M14 production phải giải quyết phụ thuộc ở F1. |
| A6 | Đo được dạng/ancestry nhưng chưa chứng minh nguồn mốc đúng Q6, F2. |
| A7 | Positive/inexistent đo được; thiếu ca sai cũ đúng mới, F5. Cần sổ rỗng để tránh precedence sổ che fixture. |
| A7b | Có thể xây ba subcase có assert riêng cho ba bộ lọc; hiện chưa đo hằng ghim thật và thiếu unknown/source-of-tombstone, F2/F3. |
| A8 | Hợp đồng byte lỗi → Chan/12 có thể đo. Phải phân biệt mã dự báo và mã CLI vì `_du_bao_check` trả list chẩn đoán, không tự trả mã thoát CLI. |
| A9 | Tiêm OSError tại reader là seam rõ; không nhận return None như thành công. |
| A10 | Byte CRLF là input phân biệt text-mode; phải so digest độc lập từ bytes nguồn. |
| A11 | Chưa có bản vá nên chưa chứng nhận ba mutant fd chết. Riêng stdin vốn được `_doc_thuc` đóng trước khi đọc (:1490), vì vậy fixture/đột biến cần chứng minh fd đích còn mở tại điểm đo; không coi xóa một close bị che là đã đo leak. Không dựng helper Git giả mới trong review này. |
| A12 | Snapshot clock rõ; caller/callee phải dùng cùng clock tiêm, đo giá trị từng bản ghi lẫn số lần gọi. |
| A13 | Nền đã đo 168/168, bỏ qua0, rc0. R2 chưa có mã nên chưa thể ghi N cuối. |
| A14 | Có actionlint và shellcheck trong môi trường; suite nền (gồm t137) đạt. Không chạy delta implementation chưa tồn tại; nền/head phải ghim cho lần thi công. |
| A15 | Chưa chạy doctrine-scan/adr-song cho mã r2 vì chưa có mã; lệnh tự nó không thay bằng chứng dương theo cuối §6. |
| A16 | Baseline trôi, F7. |
| A17 | Ba mutant tag/SHA/duplicate có đầu vào phân biệt. Hằng Q1 độc lập trong test đúng hướng; không chứng minh lại tag GitHub hiện tại. |
| A18 | Q3 ghim chạy được; hash có newline/sai một ký tự đều Chan12, receipt ghi Q3. F4 về seam và giới hạn bằng chứng. Ba mutant bỏ hash policy/base/old-policy cho ca đích rc0. Bỏ guard policy-vắng cho ca đích TypeError, cần kiểm chính xác lớp ngoại lệ, không ghi nhầm thành một đường được cấp quyền. |
| A19 | Đã dựng kho, gọi lệnh hiện tại: L vẫn giữ, rc11; mô hình M14 bỏ L. Positive fixture cần provenance thật của hai đầu theo F1. |
| A20 | Side-only vẫn giữ L, rc11; mutant all-refs bỏ L. Ca có răng, nhưng chưa bắt cặp chia hai nhánh/cache sai. |
| A21 | Đã tái hiện ref đại diện `origin/a-first`, khác default; lệnh hiện tại rc11. Mô hình theo `(blob,path)` bỏ L, mutant representative giữ L. |
| A22 | Missing default: luật hiện tại rc11; một chiều còn hạn/chạm đường: Chan12. Đo được hai hướng; cần mở rộng negative provenance F1. Không áp câu “như hiện tại” cho lease hết hạn/không chạm đường mà code đang chủ ý bỏ qua. |

Ma trận đã chạy trên ba fixture riêng; `X` = ca mất kỳ vọng:

| Quy tắc/đột biến | A19 | A20 | A21 |
|---|---|---|---|
| Mô hình M14 theo `(blob,path)` | qua | qua | qua |
| Bỏ M14 | X | qua | X |
| Bia mộ mọi ref che toàn kho | qua | X | qua |
| Xác định canonical bằng `muc['ref']` | qua | qua | X |

Ba cột phân biệt được. Một mutant thô làm lỗi chung có thể khiến nhiều ca đỏ; điều đó tự nó không chứng minh các ca tương đương. Điều cần báo là ma trận của từng mutant có scope rõ, không luật “một mutant làm cả ba đỏ ⇒ ba ca giống nhau” áp cho mọi mutant tưởng tượng.

**Đối chiếu luật và quyết định:** Q1/M12 và Q3/M13 khớp nguyên văn E1; Q3 đúng định nghĩa đã cung cấp, không được xác nhận online trong review. Ghim Q3 mở đúng nhánh marker mới trước đó bị chặn bởi None; đã chứng minh bốn guard còn lại vẫn đứng trên control, không thấy mở rộng khác từ riêng phép ghim. Metadata hợp lệ không phải revocation; cờ False vẫn cấm revocation như cha r9.

E1 #564 là đề nghị thêm ca chữa dạng 2 **hoặc nêu vì sao không**; không phải quyết định miễn ADR-0047 hay cho phép tin cache. §3.2/§4: r2 chưa đóng băng, chưa cấp lease, điều kiện chờ #579 và đo holder lại là đúng. F7 cần tách baseline. §8: lớp sensitive/độc lập có lý; tự khai họ model không thay receipt đo-máy. §12: F1 buộc checkpoint về phương pháp. ADR-0044 cho phép dừng revision hoặc khai lý do; §8.1 của SPEC đã khai ước vượt trần, không tự chọn ngoại lệ, đòi owner trước cấp lease: **hợp lệ ở giai đoạn đặc tả chưa ready**, không phải lời khai “đã đạt ≤300”. Write set ba đường đủ cho M12/M13 và thay mã/test M14; giải quyết F1 có thể đổi phụ thuộc/ước dòng, phải review lại, không tự mở tệp thứ tư. CLAUDE.md đòi quét toàn ref để không bỏ sót holder; không cho phép dùng mọi ref làm nguồn **thu hẹp** holder.

Với `_du_bao_check`, cặp đã ghim chỉ mở đúng `(cũ,mới)`, cặp khác vẫn 8; `lenh_check` gọi kiểm hạn trước khi dự báo. Vì thế giữ cặp đã hết hạn không tự hồi sinh lease trong **luật cũ hiện tại**. Không nâng kết luận này thành chứng minh cutover toàn production: Q6 còn đòi cùng map/clock và giải thích delta. Cặp sinh sau mốc bị dự báo8 là hạn chế bảo thủ đã khai, không phải lỗ mở quyền; “A1b ghim lại ngay trước” chưa chữa được nguồn/mốc/clock của F2.

## Phản chứng đã chạy

* `scratch/measure.py` / `scratch/measure.log`: file/symbol/ref/blob/holder hiện tại. Có một lần đo đầu dùng local `master` thất bại rc128; đã sửa đo đúng `refs/remotes/origin/master`, không sửa mirror.
* `scratch/numbers.py` / `scratch/numbers.log`: r1/r2/head589, tổng ước, replay clock (b). Kiểm AST thấy **0 literal dict profile schema1** và **1 ca gọi producer `hoso_adapter_do` là t136**; không suy thành “0 ca bị ảnh hưởng”. t136 đo producer động và cần được rà khi thi công v2.
* `scratch/repro.py` / `scratch/repro.log`: A19/A20/A21, cache khác OID, cờ nhánh phụ, cặp chia nhánh, snapshot cùng master khác map/clock, unknown/tombstone side, A7, A22. Tất cả kho dưới `scratch/repros/`; bare origin local.
* `scratch/q13.py` / `scratch/q13.log`: kho Git thường, marker/policy JSON, control None/Q3, hai hash sai, bốn guard, mutant strip trên digest và xóa riêng năm phép so/guard. Chỉ sửa module sao chép dưới scratch, không helper Git giả.
* `scratch/baseline.py` / `scratch/baseline.log`: baseline cố định so ref master tiến độc lập.
* `scratch/suite.log`: suite nền đầy đủ, exact archive `24c48e28`, rc0 và 168/168 không bỏ qua. Chạy lại fixture có sẵn trong kho theo yêu cầu; không tự soạn payload nhạy cảm mới.

**Chỉ MÔ TẢ, không tự soạn/chạy payload mới:** nguồn Git/helper bị thay, config rewrite nguồn, object/replace giả, đường thoát cây, đồng tự Unicode, chuỗi thoát. Các hướng này củng cố yêu cầu ADR-0047 nhưng không được tính thành bằng chứng phản chứng mới của reviewer. Counterexample F1 chỉ dùng ref/commit/branch/lease bình thường và đã đủ để bác giả định.

`HINT.patch` là unified diff cho `patch -p0` lên SPEC.md, phủ F1–F7; đã kiểm `patch --dry-run -p0 < HINT.patch` thành công. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm**. Đây là gợi ý sửa đặc tả, không phải phê duyệt quyết định nguồn/profile; những chỗ cần owner vẫn được ghi là điều kiện trước đóng băng. Không áp patch lên bản SPEC đang review.

## KHÔNG ĐO ĐƯỢC

* Q1 tags/REST GitHub, Q3 raw body 1379 B/updated_at/hai hash, danh tính và nguyên văn comment online: không mạng; chỉ đối chiếu bản chép E1–E3. Không dùng bare `origin` local làm chứng cứ máy chủ GitHub.
* Advertisement thực tại các giờ lịch sử 15:47/15:55, các nhánh cục bộ tụt 0/122 và 0/134 của phiên soạn, tập ref r1 đã xoá, trạng thái merged/closed của Issue/PR hiện tại. Mirror chứng minh object/ref của mirror, không trạng thái dịch vụ.
* Ngân sách review 4 lời gọi theo chỉ thị user được dùng cho lượt này; comment 5847670544 không có readback online. Biến thể model/effort phục vụ thực tế không có probe đáng tin; không sao chép tên model mong muốn trong SPEC thành tự khai thực tế.
* N/numstat/actionlint delta/doctrine/adr-song của implementation r2 chưa tồn tại; kích hoạt A1b, required checks/bypass, profile đầu tiên, ngân sách roots production, Windows, tác động C1a1b chưa có đặc tả.
* Chưa chốt giá trị BIA_MO_LICH_SU production hay chứng nhận ca v2 cuối cùng. `168/168` là nền, không phải nghiệm thu M1–M14.

Hoàn tất đối chiếu cuối: 2026-09-26T16:15Z; SPEC.md giữ nguyên băm, `git -C cay-kho status --porcelain` rỗng.
