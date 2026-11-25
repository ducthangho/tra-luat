verdict: changes_requested
reviewed_sha: 6c4ffe998954c0801fa69eb68d0406a543eb53f0
spec_sha256: fe67bfffe8cb0cb49bb31a945fcde5955f657669bd2d43ccb2de46ed05f75e45
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: 1, so_bieu_hien_mo: 2, P0: 0, P1: 0, P2: 1, P3: 0, so_lop_no_ke_nhiem: 4}
hoi_tu: {U: 1, F: 0, ty_le: "0/1 = 0%", lop_moi: 0, lop_tai_mo: 0, lop_lan_thu_sau: [kiem-chuoi-khong-doc-cau-truc, duong-dan-chua-khep-trong-goc, moc-chuyen-tiep-mau-thuan, tieu-chi-dong-xoa-khong-do-hanh-vi, schema-bo-sot-provider-hop-le, tien-kiem-lease-chua-du]}

Review **đặc tả r6**. Còn một lớp P2: nguồn quyết định của tiền kiểm chưa khép ở policy hiện hành và dependency Python. Phản chứng F11.d của r5 đã được chặn thật; hai biểu hiện F11.e/f bên dưới vẫn thuộc lớp `tien-kiem-lease-chua-du`. Không tách/gộp lớp, không tăng U theo số biểu hiện. Trường assurance là đích đề nghị, không phải xác nhận đã được approve.

Đã kiểm băm đặc tả đầu tiên và khớp, rồi mới tiếp tục. Tệp bằng blob tại SHA được giao; tree nguồn `a4785c5808428109b65b9f2654c41f830404bde8`. Băm verdict r5 cũng khớp `9ce3dce34b61252d70d418881684fdfe471cb7d147f02bffb08ba60ce59af767`. Chỉ ghi dưới `out/`; dựng bản sao để đo, không sửa/push kho thật, không gọi GitHub API ghi. Các đường dẫn hiện vật bên dưới tính từ thư mục làm việc; liên kết log tính từ tệp verdict này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### Theo từng finding

Đối chiếu nhóm còn mở của r5 trước khi săn thêm. Nhãn “CHƯA VÁ” ở bảng (ii) không kéo nợ đã được tách có authority về bảng (i).

| finding lượt 5 | slug | nhãn | bằng chứng tự đo |
|---|---|---|---|
| F11.c — nghĩa vụ tiền kiểm đầy đủ | tien-kiem-lease-chua-du | VÁ HỜ | 33 ca r6 đúng, nhưng `hunt.log` và `followup.log` xác nhận F11.e/f: master đã có policy trong V mà B cũ vẫn xanh; dependency ngoài V vẫn được nạp. |
| F11.d — bản ghi chưa công bố dựng bia mộ | tien-kiem-lease-chua-du | ĐÃ VÁ THẬT | Chạy nguyên `evidence-preflight_extra.py` r5: cả local head và remote phụ có `PRIVATE_SHA_ON_SERVER False`; 3c rc0, nhưng 3d/3e đều rc1 đúng lease A; bỏ ref riêng vẫn rc1. M1 làm đỏ lại cả sáu đường ref liên quan. |
| F05.b — khai báo ca theo cấu trúc | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | Patch r5/r6 bằng byte. Không consumer đối chiếu khai báo ca với ô INV trong phần mã thêm; §0/§6/§14 giữ việc này ở #1469. AST của N8 canh phạm vi sửa, không nhận lại hợp đồng ngữ nghĩa ca. |
| F05.c — nợ phải thuộc mục Nợ | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | Tự đếm 25 tên được trỏ nằm trong 27 nợ ADR. Đây là dữ liệu hiện tại; cổng mới không mở ADR theo tham chiếu để kiểm quan hệ đó. Consumer vẫn ở #1469. |
| F06 — containment tệp cổng/ca/ADR | duong-dan-chua-khep-trong-goc | CHƯA VÁ | Reader mới của nguyên mẫu chỉ đọc protocol. Ca G1 và mutant G1 giết 1 ca chỉ chứng minh containment protocol; không có ba reader thuộc #1469 trong patch. |
| F07 — vị từ và nghiệm thu cutover | moc-chuyen-tiep-mau-thuan | CHƯA VÁ | Không vị từ hay bộ ca cutover mới trong patch/N1–N16; §0/§14 vẫn giao #1470. Dòng thời điểm hiệu lực trong ADR không phải implementation cutover. |
| F10 — schema identity v2/consumer | schema-bo-sot-provider-hop-le | CHƯA VÁ | Bốn tệp nguyên mẫu không có schema v2/consumer identity mới; §0/§14 giữ hợp đồng ở #1470. Không có thay đổi r6 kéo nghĩa vụ về wp1466. |

### Theo lớp

| slug | nhãn lớp | biểu hiện còn mở | thuộc bảng (i) hay (ii) và vì sao |
|---|---|---|---|
| tien-kiem-lease-chua-du | VÁ HỜ | F11.e/f; F11.d đã đóng | (i): §1 vẫn hứa tiền kiểm trước/sau cấp lease; I-NGUON và điều kiện closure chưa đủ. |
| kiem-chuoi-khong-doc-cau-truc — phần kế nhiệm | CHƯA VÁ | F05.b/c | (ii): #1469; phần khóa văn bản của wp1466 vẫn đã đóng. |
| duong-dan-chua-khep-trong-goc | CHƯA VÁ | F06 | (ii): #1469, không nhận lại hợp đồng reader kế nhiệm. |
| moc-chuyen-tiep-mau-thuan | CHƯA VÁ | F07 | (ii): #1470, không thêm vị từ/nghiệm thu cutover. |
| schema-bo-sot-provider-hop-le | CHƯA VÁ | F10 | (ii): #1470, không thêm schema/consumer v2. |

**Kiểm không tái mở:** `out/r5-r6.diff` chỉ thay tiền kiểm và thông tin liên quan (revision, số đo, giải thích D12, lịch sử và giới hạn). Trong 13 khối fenced, chỉ `tien-kiem` đổi; 12 khối còn lại bằng byte, gồm ADR, các khối protocol, `khoa`, N8 và `so-dang-ky`. Patch nguyên mẫu r5/r6 bằng byte, SHA256 `838bbccba7309c0989fb22b0433b7e33c683677129061bd0a9bef5b203123b55`. Không diễn giải “chỉ sửa tiền kiểm” thành “mọi dòng ngoài §1 bất biến”: metadata liên quan ở các mục khác có đổi.

Tự chạy lại 167 phép khóa văn bản (0 lệch), N8 42 chế độ mã + 23 chế độ test (0 sai), 190 ca liên quan, 40 ca ADR, 26 mutant mới và 21 mutant cũ. Bảy khóa được tính lại độc lập bằng địa chỉ và byte thô, đều khớp. Do đó không có bằng chứng tái mở phần wp1466 của `kiem-chuoi-khong-doc-cau-truc` hoặc `tieu-chi-dong-xoa-khong-do-hanh-vi`, hay một lớp cũ khác. F11.b về policy hiện diện ngay trên B vẫn bị chặn; F11.e là biểu hiện mới của lớp F11 còn mở khi canonical đổi sau lúc chốt B.

U = 1; F = 0 vì lớp F11 chưa đóng toàn bộ phần wp1466. Không lấy việc đóng riêng F11.d làm F = 1. Danh sách `lop_lan_thu_sau` giữ lịch sử sáu slug lặp qua các lượt, không có nghĩa sáu lớp đều mở trong wp1466. Tỷ lệ trước là 2/3; tỷ lệ này 0/1 chưa tạo hai chuyển tiếp liên tiếp dưới 50%. Tín hiệu một lớp lặp ≥3 lượt của §12 vẫn còn và cần ghi nhận trong việc xét lại cách làm; không tự sinh một yêu cầu xin phép mới.

## BẢNG LỚP (i) — lớp MỞ của wp1466

| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| tien-kiem-lease-chua-du | F11.e: bỏ policy/schema canonical mới khi B cũ; F11.f: dependency Python ngoài V | P2 | Lớp r1–r5; hai biểu hiện đo trên r6/6c4ffe9 | Ràng buộc đủ nguồn quyết định. Hai chốt riêng vì phiên bản policy và bộ nạp mã là hai tầng khác nhau, cùng nghĩa vụ tiền kiểm. | `hunt.py`, `followup.py`; đã có đối chứng. Chưa dựng dependency giả gây bỏ lease; không tuyên bố đã quan sát cấp lease sai thật. |

## BẢNG LỚP (ii) — nợ kế nhiệm có authority

| slug lớp | biểu hiện | Issue kế nhiệm | tên nợ | bằng chứng wp1466 không còn khai gì |
|---|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc | F05.b/c: cấu trúc ca, nợ thuộc mục Nợ | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | §0:21 và §6/§14 loại hợp đồng ngữ nghĩa khỏi wp1466; N8/sổ đăng ký chỉ kiểm phạm vi và bảo toàn sổ. |
| duong-dan-chua-khep-trong-goc | F06: containment reader cổng/ca/ADR | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | §0:21 loại cả ba reader; G1 của wp1466 chỉ mở protocol. |
| moc-chuyen-tiep-mau-thuan | F07: cutover | #1470 | INV-12-CONG-VERDICT-THEO-LOP | §0:22 và §14 không đặt thiết kế/tiêu chí cutover cho wp1466. |
| schema-bo-sot-provider-hop-le | F10: identity v2 | #1470 | INV-12-CONG-VERDICT-THEO-LOP | §0:22 loại schema, provider và consumer v2; patch không triển khai chúng. |

Authority kế thừa như r4/r5: §0 dẫn quyết định E2 “Duyệt tách 3 packet”, [comment 7053593553](https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7053593553). Review này kiểm nội dung đã đóng gói và sự nhất quán của scope; không có readback GitHub trực tiếp để tái xác thực comment hay trạng thái Issue hiện tại.

## BẢNG SĂN

Các lệnh dưới đây đã chạy, output trích từ log do reviewer tạo. `hunt.py` và `followup.py` dựng bare origin giả dưới `out/tmp/`, dùng Git thật; các lệnh push trong chúng chỉ đến origin giả cục bộ. Không có push máy chủ thật. Không tạo payload đường dẫn/mã độc mới. Các ca đối kháng có sẵn được chạy lại nguyên bộ; hướng dependency dùng bản PyYAML đang cài, không sửa mã thư viện.

| hướng độc lập | LỆNH | OUTPUT THẬT | kết luận / giới hạn |
|---|---|---|---|
| 1. T1 so OID, không chỉ tên | `python3 -B out/hunt.py` → `same_names_changed_oid` | `rc: 1`; `máy chủ có mà bộ đệm thiếu 1 cặp, bộ đệm thừa 1 cặp` | Cùng tên, đầu nhánh đổi vẫn bị chặn. |
| 2. Namespace ref chưa xác minh / bia mộ | `python3 -B out/run_preflight.py` → `extra-r5.log`, `mutants.log` | `PRIVATE_SHA_ON_SERVER False`; `STEP_3C 0`; `STEP_3D rc 1`; `STEP_3E rc 1` ở cả hai namespace; M1 sai 6 | F11.d đóng; local, remote phụ, packed, replace và đường sau đăng có răng. |
| 3. Alternates cấp object nhưng không cấp ref | `python3 -B out/followup.py` → dòng cuối | `ALTERNATES_REFSET_EXACT True REF_COUNT 2 PRIVATE_OBJECT_READABLE commit PRIVATE_REF_VISIBLE False` | Object riêng vẫn đọc được bằng OID; ref riêng không lọt. Không nhầm cách ly ref với xóa object ngoài V. Chốt ancestry và cách chọn ref vẫn cần thiết. |
| 4. `info/grafts` của clone | `python3 -B out/hunt.py` → `graft_*` | ancestry trong clone `rc: 0`; `graft_private_B rc: 1`, `không phải master ... hay tổ tiên của nó` | Graft cục bộ đổi kết quả clone nhưng không đổi phép ancestry trong kho tạm. |
| 5. Worktree phụ | `python3 -B out/hunt.py` → `linked_private_retirement`, `invoked_from_linked_worktree` | Cả hai `rc: 1`; `lease còn hiệu lực giao write set wp1466: ['fxa-r1-g1-claude']` | Thử nhánh nháp trong worktree phụ và gọi từ worktree phụ; không làm mất người giữ. |
| 6. B cũ so với lease mới | `python3 -B out/hunt.py` → `ancestor_later_master_lease`, `ancestor_later_branch_lease` | Cả hai `rc: 1`; A vẫn là lease giao write set | Không phát hiện bỏ lease đăng sau B, cả trên master lẫn nhánh mới. |
| 7. B cũ so với policy/schema canonical mới | `python3 -B out/followup.py` → `policy_*`, `schema_*` | `PAIRS_EQUAL_BEFORE_3E True`; B cũ sau master đổi: `rc 0 ... policy 0 ... ĐẠT`; master mới: `rc 1 ... policy 1 ... DỪNG` | F11.e. Đổi `notes.txt` là đối chứng: B cũ/master mới đều rc0. Không phải race sau T1. |
| 8. Python import bắc cầu | `python3 -B out/hunt.py`; `python3 -B out/followup.py` | `imports_clean_local_script rc 0`, `LOCAL_DEPENDENCY True`; thêm `-I`: `LOCAL_DEPENDENCY False`; trace có `yaml/__init__.pyc` ở ca sourceless | F11.f. Đã chứng minh nguồn mã ngoài V đi vào quyết định; chưa làm parser giả hay xanh giả trong kho có lease chặn. |
| 9. Fail-closed khi dữ liệu/công cụ không đọc được | `python3 -B out/hunt.py`; `python3 -B out/run_preflight.py` | YAML hỏng, thiếu hàm, không master, origin rỗng/không truy cập, hạn không đọc được đều rc1; có `KHÔNG ĐO ĐƯỢC` ở các lỗi đọc | Không quy toàn bộ fail-closed đều hỏng. Lease có write_set rỗng cho rc0 được ghi lại, chưa có căn cứ để coi là finding riêng. |
| 10. Cấu hình kế thừa / `GIT_*` | `python3 -B out/hunt.py` → `env_*` | `GIT_DIR`: rc1, `remote origin already exists`; `GIT_WORK_TREE`: rc1; `GIT_NAMESPACE`: rc1; `GIT_OBJECT_DIRECTORY`: rc1 `FileNotFoundError` | Bốn biến thể đo đều không xanh giả. Ca cuối traceback không có dòng DỪNG nhưng rc khác 0 vẫn chặn theo §1. §18 đã đặt global/system/env config và URL vào tiền đề tin cậy; không coi đây là cách ly mọi config. |
| 11. Hồi quy khóa văn bản / phạm vi AST / hành vi sổ | `python3 -B out/regression.py`; `python3 -B out/independent.py`; `python3 -B out/final_check.py` | `TONG 167 LECH 0 []`; `TONG ma: dung 42 sai 0`; `TONG test: dung 23 sai 0`; 7 `HASH_MATCH True`; sổ phát hiện `r1187_drop_doc_guard` bị đổi | Khóa/N8 không tái mở. Sổ chạy thật cần đứng cùng N8; kiểm AST không thay kiểm giá trị runtime. |
| 12. Master drift, trần và phạm vi lời khai | `python3 -B out/measure.py`; `python3 -B out/counts.py` | `DRIFT_BASE 29 COMMITS 120 PATHS MEASURED []`; `TOTAL 434 4 FILES 4 HEADROOM 16`; `CALLS_ASSIGNED 7/10` | Trần prototype còn đạt; số lời gọi là dữ kiện giao việc, không phải tự truy xuất lịch sử API. |

Log chi tiết: [hunt.log](hunt.log), [hunt-results.json](hunt-results.json), [followup.log](followup.log), [extra-r5.log](extra-r5.log), [mutants.log](mutants.log), [measure.log](measure.log). File trace import giữ nguyên đường dẫn và thông tin loader để phân biệt script ngoài clone, script trong clone, PYTHONPATH và chế độ isolated.

## BẢNG ĐO

Môi trường: Linux, Python 3.13.18, Git 2.43.0, `core.abbrev=7`, Ruff 0.16.9. Đợt đo chính ngày 21-11-2026 UTC: dựng cây 04:17, hồi quy từ 04:18 đến 04:26, đo snapshot 04:22; thời điểm cụ thể và câu lệnh ở các log/JSON. `out/base` là checkout sạch base; `out/prototype` là base + patch; `out/master` là master mới + cùng patch. Hai cây sau là nguyên mẫu thử, không phải commit H giao nộp đã được approve.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| Định danh r6 | SHA và băm được giao | SHA/tree/băm khớp, tệp bằng blob | Có |
| Khối tiền kiểm | 82 dòng không trống; bản xuất bằng spec | 82; so byte bằng | Có |
| Số kịch bản tiền kiểm | 33 = 19 cũ + 14 mới | `TONG 33 kịch bản: đúng 33 · sai 0` | Có, trong bộ ca này |
| Ba mutant tiền kiểm | M1/M2/M3 đỏ 6/2/1 | Sai đúng 6/2/1; khối r5 nguyên văn sai 9 | Có |
| Phản chứng r5 | Đỏ ở 3d và 3e | Hai namespace đều rc1, đúng A; 3c vẫn rc0 | Có |
| 7 trường hợp raw matcher không đủ | `ai-dang-giu` rc0 nhưng tiền kiểm dừng | Policy, hai prefix, case, effective-only, planned/backslash, symlink: raw đều `NGƯỜI_GIỮ 0`; bộ 33 dừng đúng | Có |
| I-NGUON bao hết đầu vào quyết định | Cây `.py`/`.pyc` không tới quyết định; closure rỗng đủ theo B | Dependency local được nạp; policy mới trong V bị bỏ qua với B cũ | Không — F11.e/f |
| Các khối ngoài tiền kiểm | Không đổi nguyên mẫu/khóa/N8 | 12/13 fenced blocks không đổi, chỉ `tien-kiem` đổi; patch bằng byte | Có |
| Checksum hiện vật đã giao | Tệp tương ứng có băm | Bundle r6 12/12; bundle nguyên mẫu r5 20/20 | Có với tập đã giao; không giả nhận đã truy cập đủ 23 tệp đường dẫn riêng của tác giả |
| Dựng protocol/ADR | Sáu điểm ghép; ADR theo mẫu | 6 mốc mỗi mốc đúng 1; protocol ghép bằng byte; ADR đúng mẫu sau thay 7 placeholder | Có |
| Nội dung bất biến | 28 dòng, 15 cổng/12 kỷ luật/1 chưa xác định; 27 nợ | 28 = 15+12+1; cả 15 dòng cổng mang nợ; 18 tham chiếu ca; 25 tên được trỏ thuộc 27 nợ | Có về dữ liệu, không suy có consumer ngữ nghĩa |
| Luật gốc | Giữ mười bất biến | Cả 10 bằng sau nối dòng trong từng đoạn | Có |
| Bảy đơn vị khóa | Địa chỉ, duy nhất, băm raw | Parser độc lập: 7/7 địa chỉ+băm; mỗi bản raw xuất hiện 1; hằng mã bằng kết quả | Có |
| Kiểm byte r5 | 167 biến thể | 167/167, không lệch | Có |
| N8 | 109 dòng, 65 biến thể | 109; mã 42/42, test 23/23 | Có |
| Sổ runtime | 1582→1639 ca; Linux 1581→1638; 57 mới; 1864→1890 mutant | Đúng cả số hạng, thứ tự ca nền, giá trị mutant cũ và tập NHAM | Có |
| Răng của sổ | Ghi đè mutant cũ phải đỏ dù N8 đạt | Ghi đè đúng khóa có sẵn trong ví dụ spec; sổ chỉ ra `r1187_drop_doc_guard`, rc1; cùng tệp N8 rc0 | Có; xem `final-check-rerun.log` (đợt bổ sung từ 04:31:48 UTC) |
| Ca liên quan | 190 và 40 ADR | 190/190; 40/40; không fail | Có |
| Mutant mới/cũ | 26 mới, 21 cũ | 26/26 và 21/21 bị giết; nền 60/60 và 132/132, skip0; ba đối chứng mỗi vòng đúng | Có |
| Marker/target mutant | Mỗi marker 1, có ca đo thật | 26 marker đều 1; cả 57 ca mới có đích; số ca giết từng mutant khớp, kể cả K01–K07 = 8/4/6/4/9/4/3 | Có |
| Quét sáu vị trí | Vector đếm ở từng tệp | 29 vector mẫu phân biệt được tính lại, mỗi vector khớp sáu số hạng; mẫu lặp giữa bảng không tính thành hướng độc lập | Có |
| Ruff | Không thêm lỗi | Base/prototype cùng 16: F841=3, F401=8, F541=2, F811=3; delta0 | Có; không gọi Ruff là xanh |
| Kích thước nguyên mẫu | 4 tệp, +434 −4, dưới 450 | Mã +76−1; test +163−1; protocol +46−2; ADR mới +149; tổng +434−4; diff-check rc0 | Có; dư 16 dòng thêm, 2 tệp dưới trần 6 |
| ADR hiện có | 66, max0067; thêm thành67 | Base66; nguyên mẫu trên base và master đều67; 392 ref không có0068+ | Có trên snapshot |
| Cổng trên cây thật dựng lại | doctrine-scan/adr-song sạch | Base, prototype, master+patch đều rc0; ADR66/67/67, khớp bảng 1–1 | Có offline |
| Master drift | Không đổi tập tệp được đo | Base→master:29 commit/120 đường; giao với tập §3 bằng0; master r5→r6 đổi5 đường | Có với tập được khai, không nói cả repo đứng yên |
| Biên nhận | 352, chưa có bang_lop | 352/0 | Có trên snapshot |
| Lease tại mốc tác giả | 550/17/12/5 lúc04:07:39 | Dùng cùng thời điểm:550/17/12/5; lúc04:22:38:550/16/11/5 | Khớp tại mốc; một lease hết hạn, 5 lease hiệu lực không đổi |
| B4 đang chặn | Hai tệp mã do B4 giữ; tiền kiểm dừng | Hai đường mã rc11, người giữ `wp1462-r8-g2-claude`; hai đường docs rc0; tiền kiểm rc1 đúng một lý do B4 | Có offline; không được cấp lease từ kết quả này |
| Trần ADR-0053/0055 | Opt-in commit; 6 tệp/450 dòng; lần gọi này7/10 | Hai opt-in mỗi cái1 dòng, commit có ADR nhưng parent chưa có, đều trên first-parent; không shallow; không opt-in0052 | Có về dữ liệu kho; bộ đếm7/10 theo prompt |

Năm lease hiệu lực tại hai mốc trên: `wp1236-a-r10-g1-claude-20261121`, `wp1448-r4-g5-claude`, `wp1462-r8-g2-claude`, `wp1475-r1-g1-claude`, `wp433-r9-g5-claude`. Không coi thay đổi số lease còn hạn theo đồng hồ là lỗi của đặc tả đã ghi thời điểm.

Master hiện tại là `4e56f005785db1b04e043bb71fc694a674a8dc9f`. Năm đường đổi từ master lúc r5: `.claude/dev/launcher_test.py`, `ops/acceptance/cai-apt-backoff/r1/VERDICT.md`, `ops/cai_cong_cu.sh`, `ops/leases/cai-apt-backoff-r1-g1-claude.yaml`, `ops/specs/cai-apt-backoff-r1.md`. Tập đo §3 gồm sáu tệp cổng, protocol, thư mục ADR và các tệp test/runner/hooks được nêu; giao bằng0. `.claude/skills/work-packet/SKILL.md` có đổi từ base cũ ngoài tập này; đã chạy doctrine-scan trên master+patch để không suy rộng “không drift”.

## ĐÁNH GIÁ L3, L6, L7 VÀ AUTHORITY

**L3:** Các tiêu chí khóa byte, N8, ca/registry và mutant có phép đổi màu đã chạy. M1/M2/M3 chứng minh ba cơ chế vá cụ thể của tiền kiểm, chưa chứng minh mọi đầu vào của I-NGUON. Hai chiều còn thiếu là policy đổi giữa chốt B và lần tiền kiểm mới, và dependency nạp gián tiếp. Đây là thiếu ở hợp đồng còn hứa của wp1466, không phải nợ closure tổng quát có thể mặc nhiên chuyển sang #1469/#1470.

**L6:** Tự dựng protocol từ các khối, tính bảy băm bằng parser độc lập, đo dương/âm bằng bộ 167 và mutant. Khóa raw chủ ý đổi màu khi reflow làm đổi byte; không dùng chuẩn hóa dòng để làm khóa raw xanh. Với mười luật gốc, phép so nối dòng chỉ trong từng đoạn. ID, địa chỉ và vector ở sáu tệp được đo riêng; không dùng tổng chung thay số từng vị trí, cũng không lấy việc có chuỗi tên cổng làm bằng chứng cổng đã enforce ngữ nghĩa. Không bổ sung lời hứa bắt mọi chữ đồng hình ngoài phạm vi ID đã nêu.

**L7/ADR-0067:** C1 E5 vẫn là duyệt băm sau khi review hết P0–P3; C3 E2 là dòng miễn Windows trên H. Không có authority miễn trừ được sinh bởi review này. Quyết định E5 cho chuỗi #1466/#1469/#1470 đi thẳng master không mở rộng sang B4; điều kiện B4 nằm trên first-parent master và base chứa nó vẫn phải đo trước lease. Các quyết định E2/E5 được ghi trong hồ sơ, không coi là một lời duyệt hiện tại do reviewer tạo. Việc bổ sung đo hoặc sửa thiết kế D12 là phần người soạn có thể cụ thể hóa; không tự đặt “ngân sách mềm” hay một lần hỏi chủ kho vô căn cứ.

**Trần:** Opt-in ADR-0053 tại `8ab100793df9831505f495543a74044b91c2c9ab`; ADR-0055 tại `d2e3052d479d140b7e7b91df41ec4914fab7d544` được kiểm trong mirror. Prototype +434 còn dưới450, không đảm bảo patch thi công tương lai sau B4 vẫn dưới trần. Lời gọi này là7/10 theo giao việc; không reset theo revision/provider hay theo việc là review đặc tả. Chưa chạm trần, không có lý do xin nới trần ở lượt này. Không xác nhận model/effort backend thực phục vụ; session_id ghi KHONG_DO_DUOC.

### tien-kiem-lease-chua-du [P2] Policy hiện hành và dependency Python chưa được ràng buộc đủ vào tiền kiểm

**TỆP/DÒNG:** `cay-kho/ops/specs/wp1466.md:66`–`:70` (hợp đồng 3a–3e), `:76` (cách chạy tệp tạm), `:102`–`:107` (lời khai nguồn mã), `:116`–`:122` (B tổ tiên và policy chỉ đọc từ B), `:134`–`:139` (exec blob và gọi scanner). Dependency thực: `cay-kho/ops/lease_publish.py:745` (`import yaml` trong `_quet_lease_toan_kho`). Nghĩa vụ canonical đổi: `cay-kho/docs/PROTOCOL_DA_PHIEN.md:362`–`:364`.

**VẤN ĐỀ:**

F11.e — Chốt ancestry bảo đảm B là commit đã công bố, nhưng không bảo đảm policy của B còn là policy có thẩm quyền khi quyết định. Sau 3a/3d, master có thể nhận policy hoặc schema trước lần làm mới ref và T1 của 3e. Lúc ấy V đã có master mới, cặp tên/OID khớp hoàn toàn, nhưng T2 vẫn chạy `ls-tree ... ob` với B cũ; nó báo policy0 và ĐẠT. Protocol §5 buộc pause/re-evaluate mọi packet chưa terminal khi policy đổi. Cho phép B cũ để giữ base lease qua lần đăng không đủ để bỏ bước này.

Chuỗi đo đầy đủ trong `followup.py`: chọn B từ master → 3d rc0 → đăng lease của mình vào origin giả → 3e rc0 → công bố policy rồi fetch → xác nhận cặp server/cache bằng nhau **trước** 3e → 3e với B cũ rc0. Cùng trạng thái kho, dùng master mới thì rc1. Lặp riêng với schema cũng vậy. Đối chứng đổi tệp không liên quan vẫn rc0 với cả B cũ và master mới. Đây không phải giới hạn máy chủ đổi *sau* T1 đã khai ở §18. Fixture policy/schema là dữ liệu đơn giản để kiểm điều kiện “có tệp thì dừng” của chính đặc tả; không giả nhận đã tính một closure hợp lệ từ dữ liệu ấy.

F11.f — `exec(compile(blob))` cố định nguồn của module chính nhưng các câu import bên trong vẫn dùng bộ nạp Python hiện hành. Scanner nhập PyYAML qua `sys.path`. Chép nguyên thư viện đang cài vào thư mục `yaml/` chưa tracked trong clone rồi chạy tệp tiền kiểm tạm đặt ở gốc clone: trace xác nhận nạp `.py` từ cây làm việc. Script ở ngoài clone cũng gặp đường này nếu PYTHONPATH trỏ clone. Dạng sourceless `yaml/__init__.pyc` từ chính mã thư viện đó vẫn được nạp khi chạy `-B`. Do đó lời khai `.py`/`.pyc` không thể tới quyết định là sai; không cần sửa `lease_publish.py` hay thay ref.

Tiền đề tin cậy URL/global Git config/GIT_* ở §18 không giải quyết script directory mặc định của Python. Đường script trong clone tái hiện không cần thay PYTHONPATH. Nếu dependency bị thay thành parser có nghĩa khác, dữ liệu quyết định có thể bị sửa ngay khi đọc lease; hướng đó chỉ mô tả bằng lời, không dựng mã độc theo yêu cầu giao việc. Cụ thể đã quan sát sự vi phạm nguồn mã, chưa quan sát một parser giả làm mất lease.

Giữ **P2** như lớp r5: ảnh hưởng điều kiện tiền kiểm để cấp/giữ lease trước thi công, cần sửa trước khi approve spec. F11.d đã được vá, không gọi nó tái mở; hai biểu hiện này cho thấy lớp nghĩa vụ rộng F11.c chưa khép.

**GỢI Ý VÁ:** Ràng buộc việc dùng B cũ với policy canonical của master trong V: có thay đổi liên quan thì dừng để re-evaluate/revision theo §5, trước và sau đăng. Đối chứng đổi master không liên quan nên được giữ để tránh chặn mọi drift. Chỉ ép B bằng master ở mọi bước sẽ làm mất trường hợp giữ base hợp lệ sau đăng, nên cần quyết định rõ điều kiện thay vì chỉ đổi một phép so.

Với Python, định nghĩa môi trường chạy cô lập và nguồn dependency tin cậy, gồm import bắc cầu; chứng minh clone không nằm trong đường nạp. `-I` đã loại được đường local/PYTHONPATH trong môi trường thử, nhưng đây là dữ liệu thiết kế, chưa phải bản vá production hoàn chỉnh. Mất dependency phải ra KHÔNG ĐO ĐƯỢC. Cặp ca dependency local `.py`/sourceless `.pyc` và đối chứng trusted dependency giúp kiểm lời khai chính xác; không thể chỉ kiểm hash của module chính.

Cả hai chốt cần phép đo dương/âm và đột biến gỡ riêng chốt làm đổi màu; không có cơ sở đổi slug hoặc chuyển sang nợ kế nhiệm trong khi §1 còn hứa tiền kiểm này.

**ĐÃ THỬ NGHIỆM:** `python3 -B out/hunt.py`, `python3 -B out/followup.py`; script/log và các kho giả giữ dưới `out/`. Trích output:

```text
policy PAIRS_EQUAL_BEFORE_3E True
policy_3E_old_B_after_master_change rc 0 ... policy 0 | TIỀN KIỂM: ĐẠT
policy_3E_current_master_after_master_change rc 1 ... policy 1 | TIỀN KIỂM: DỪNG
schema PAIRS_EQUAL_BEFORE_3E True
schema_3E_old_B_after_master_change rc 0 ... policy 0 | TIỀN KIỂM: ĐẠT
schema_3E_current_master_after_master_change rc 1 ... policy 1 | TIỀN KIỂM: DỪNG
imports_clean_local_script rc 0 ... TIỀN KIỂM: ĐẠT
imports_clean_local_script LOCAL_DEPENDENCY True
imports_clean_local_script_isolated rc 0 ... TIỀN KIỂM: ĐẠT
imports_clean_local_script_isolated LOCAL_DEPENDENCY False
```

Dấu `...` chỉ rút phần OID/số lease; log đầy đủ không sửa. Với fixture có lease A chặn, bản PyYAML nguyên trạng vẫn trả rc1 dù nạp từ clone; với fixture sạch, rc0 đi cùng trace local. Hai kết quả này **không** được gọi là đã dựng xanh giả bỏ xung đột. `script_in_clone_sourceless_pyc` cho trace code object từ `.../kho/yaml/__init__.pyc`; script ngoài clone không PYTHONPATH là đối chứng không nạp local.

**ĐỘ TIN:** Cao đối với F11.e và provenance của F11.f: có Git/Python thật, đối chứng trên cùng trạng thái và nhiều đường vào. Hệ quả thay nghĩa parser là suy luận từ việc mã dependency được thực thi, chưa được thử bằng payload. Không suy luận rằng B tổ tiên làm mất lease đăng sau B: hai phép đo lease mới đều đỏ đúng.

## HIỆN VẬT VÀ NHỮNG GÌ KHÔNG ĐO ĐƯỢC

- Scripts tái lập chính: `setup.py`, `run_preflight.py`, `regression.py`, `hunt.py`, `followup.py`, `measure.py`, `independent.py`, `counts.py`, `final_check.py`; bản khối spec và helper dưới `sc/`. Script `setup.py` cần thư mục đích clone chưa tồn tại nếu dựng lại từ đầu.
- `preflight-results.json`, `regression-results.json` ghi lệnh/rc; `fx33.log`, `bytes.log`, `n8-ma.log`, `n8-test.log`, `registry.log`, `ca.log`, `adr.log`, `moi.log`, `cu.log` là log reviewer chạy. `independent-rerun.log` là phép tự tính địa chỉ/băm, không chỉ dùng hàm của tác giả. Không lấy hash log tác giả thay cho chạy độc lập.
- Đã lưu cả lỗi dựng phép đo của reviewer: regex fence ở lần setup đầu, parser độc lập ban đầu tính nhầm heading trong code fence, và fixture registry ban đầu thiếu Git/đặt câu lệnh sau main guard. Chúng đã được sửa; không tính những lỗi harness này thành finding sản phẩm hay một mutant bị giết. Dùng các log `*-rerun.log` tương ứng cho kết luận cuối.
- `source-before.json`/`source-after.json` đối chiếu 17.998 mục của `cay-kho` và `kho.git`: delta0 về nội dung, kích thước, mtime hoặc đích symlink; `git status --porcelain` rỗng, HEAD/tree/spec hash giữ nguyên. Mốc snapshot bảo toàn bắt đầu khi dựng phép đo, sau các lượt đọc ban đầu.
- Origin thật trên GitHub, trạng thái Issue/comment/ruleset/branch protection hiện tại, lịch sử lời gọi API và authority mới: không đo. Mirror 392 nhánh chỉ là snapshot được giao. Không có quyền cấp lease/merge phát sinh từ báo cáo.
- Không chạy full suite toàn repo, full mutant CI, Windows, N16 sau land hoặc mã B4 tương lai. Hai cổng trên master+patch và các suite chọn lọc không thay các kiểm bắt buộc trên H giao nộp. B4 vẫn là blocker trong snapshot.
- Không chứng minh an toàn cho mọi global/system Git config, mọi GIT_*, transport/xác thực, Python dependency hay va chạm SHA-1; chỉ đo các biến thể đã ghi. Khe server đổi sau T1 vẫn mở như spec đã thừa nhận. Không dựng payload mới kiểu tấn công đường dẫn hay dependency độc hại.

Với bảng (i) còn một lớp P2, verdict là **changes_requested**.
