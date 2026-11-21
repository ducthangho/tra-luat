verdict: changes_requested
reviewed_sha: 3c89d87fffbc06a59ad276bb3171e43ef89c2768
spec_sha256: baf01d45ba30512e768466fd077842346644db730d69471a44efb2a40b6b9139
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: 1, so_bieu_hien_mo: 3, P0: 0, P1: 0, P2: 1, P3: 0, so_lop_no_ke_nhiem: 4}
hoi_tu: {U: 1, F: 0, ty_le: "0/1 = 0%", lop_moi: 0, lop_tai_mo: 0, lop_lan_thu_bay: [kiem-chuoi-khong-doc-cau-truc, duong-dan-chua-khep-trong-goc, moc-chuyen-tiep-mau-thuan, tieu-chi-dong-xoa-khong-do-hanh-vi, schema-bo-sot-provider-hop-le, tien-kiem-lease-chua-du]}

Review **đặc tả r7**, không phải phê duyệt mã giao nộp hay cấp lease. Còn một lớp P2 `tien-kiem-lease-chua-du`: danh sách đầu vào chưa đóng đối với tham số miễn trừ sau đăng, nguồn import trong tiến trình cha và cách scanner đọc tên tệp lease. Các đường PyYAML và policy cụ thể của lượt 6 đã được sửa, nhưng chưa đủ để đóng toàn lớp. Ba biểu hiện mới F11.g/h/i cùng slug cũ; không tách/gộp lớp. Số P0–P3 ở đầu báo cáo đếm **lớp**, không đếm biểu hiện.

Đã kiểm băm **đầu tiên**, khớp giá trị được giao; tệp bằng blob tại reviewed SHA, tree `af50833d0c1d503ef4921526fde1abe00f2d90f4`. Băm verdict lượt 6 khớp `2a0590460bc42eb0324c11ea69706112fc2dda49108ab29f7a7b04265068d34c`. Chỉ ghi dưới `out/`; các push trong bộ dựng ca chỉ tới bare origin giả dưới `out/tmp/`. Không sửa/push kho được review, không ghi GitHub. Liên kết hiện vật dưới đây tính từ tệp verdict này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### Theo từng finding

Đã đọc và đối chiếu các nhóm còn mở trước khi săn biểu hiện mới. Bốn nhãn dùng theo §8: ĐÃ VÁ THẬT · VÁ HỜ · VÁ SINH LỖI MỚI · CHƯA VÁ. Không phát hiện trường hợp cần nhãn VÁ SINH LỖI MỚI; biểu hiện mới cùng lớp không tự chứng minh rằng r7 gây ra nó.

| finding lượt 6 | slug | nhãn | bằng chứng tự đo |
|---|---|---|---|
| F11.e — policy/schema canonical đã đổi trong V, B vẫn cũ | tien-kiem-lease-chua-du | ĐÃ VÁ THẬT | Chạy nguyên `hunt.py`/`followup.py` lượt 6 trên khối r7: bốn đường B cũ nay rc1 vì policy; cặp server/cache bằng nhau trước 3e. Ba đường `irrelevant_*` vẫn rc0. Bộ r7 kiểm thêm xóa, thêm rồi xóa, nhánh phụ và merge. |
| F11.f — dependency Python ngoài nguồn được khai | tien-kiem-lease-chua-du | VÁ HỜ | Ba đường PyYAML `.py`/sourceless `.pyc`/PYTHONPATH cũ không còn nạp local; kho sạch vẫn rc0. Nhưng `parent-boundary.log` xác nhận `os.py` nguyên trạng trong clone được nạp tại dòng đầu của khối khi thiếu `-I`, có `-S -X frozen_modules=off`. P4 chỉ khai phần **trước** dòng đầu. F11.h là biểu hiện còn lại của cùng nghĩa vụ nguồn mã. |
| F05.b — khai báo ca theo cấu trúc | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | Patch nguyên mẫu bằng byte; phần thêm vẫn không có consumer ngữ nghĩa ca ↔ ô INV. N8 chỉ kiểm phạm vi. §0/§6/§14 tiếp tục giao #1469. |
| F05.c — nợ phải thuộc mục Nợ | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | Parser độc lập đếm 25 tên tham chiếu nằm trong 27 nợ hiện tại; mã mới không mở ADR theo tham chiếu để kiểm quan hệ đó. Nghĩa vụ vẫn ở #1469. |
| F06 — containment reader cổng/ca/ADR | duong-dan-chua-khep-trong-goc | CHƯA VÁ | Patch chỉ có reader protocol; G1/mutant G1 bảo vệ protocol, không bổ sung ba reader kế nhiệm. §0 vẫn loại chúng. |
| F07 — vị từ và nghiệm thu cutover | moc-chuyen-tiep-mau-thuan | CHƯA VÁ | Không thêm vị từ hay ca cutover trong patch hoặc N1–N16; §0/§14 vẫn giao #1470. |
| F10 — schema identity v2 và consumer | schema-bo-sot-provider-hop-le | CHƯA VÁ | Bốn tệp nguyên mẫu không có schema/consumer v2; §0/§14 vẫn loại hợp đồng này và giao #1470. |

### Theo lớp

| slug | nhãn lớp | biểu hiện còn mở | thuộc bảng (i) hay (ii) và vì sao |
|---|---|---|---|
| tien-kiem-lease-chua-du | VÁ HỜ | F11.g/h/i; F11.e và các đường PyYAML cụ thể cũ đã đóng | (i): §1 vẫn hứa tiền kiểm đầy đủ, danh sách đầu vào đóng và dừng khi không đo được. |
| kiem-chuoi-khong-doc-cau-truc — phần kế nhiệm | CHƯA VÁ | F05.b/c | (ii): #1469; phần khóa văn bản của wp1466 vẫn đóng. |
| duong-dan-chua-khep-trong-goc | CHƯA VÁ | F06 | (ii): #1469; không nhận lại hợp đồng reader kế nhiệm. |
| moc-chuyen-tiep-mau-thuan | CHƯA VÁ | F07 | (ii): #1470. |
| schema-bo-sot-provider-hop-le | CHƯA VÁ | F10 | (ii): #1470. |

**Không tái mở lớp đã đóng:** [r6-r7.diff](r6-r7.diff) chỉ thay phần tiền kiểm và metadata/số đo/giới hạn/lịch sử liên quan. Trong 13 fenced blocks, chỉ `tien-kiem` đổi; 12 khối còn lại bằng byte. Patch nguyên mẫu vẫn có sha256 `838bbccba7309c0989fb22b0433b7e33c683677129061bd0a9bef5b203123b55`. §2, §4–§15 giữ nguyên; §16–§19 có giải thích tiền kiểm mới, nên không khai “mọi dòng ngoài §1 bất biến”. [setup.log](setup.log), [measure.log](measure.log).

Tự dựng base + patch, đo lại khóa byte, AST, sổ runtime và các ca/mutant liên quan để kiểm việc không tái mở. F11.d cũng vẫn đóng: các ref riêng không làm mất lease A; mutant M1 làm sai đúng sáu ca ref riêng. Hai lớp đã đóng về khóa văn bản và phạm vi AST không nhận thêm finding ở lượt này.

**Hội tụ:** U=1 theo bảng (i) cuối lượt 6; F=0 vì chưa đóng toàn lớp. Không lấy việc đóng riêng F11.e hoặc ba đường PyYAML làm F=1. Không tính bốn lớp nợ kế nhiệm vào U. Danh sách sáu slug lịch sử ở `lop_lan_thu_bay` tiếp tục cách ghi của lượt 6, không có nghĩa sáu lớp đều còn mở trong wp1466; lớp còn mở qua cả bảy lượt là `tien-kiem-lease-chua-du`.

Chuyển tiếp r5→r6 là 0/1, r6→r7 cũng 0/1: nay có **hai chuyển tiếp liên tiếp dưới 50%**, ngoài tín hiệu lớp lặp ≥3 lượt. Theo §12 cần dừng vòng vá để xét lại cách làm và ghi `xet_lai_cach_lam`; mục sổ đã tóm trong chỉ thị giải thích hướng r7 nhưng không biến kết quả r7 thành đạt. Đây không tự sinh câu hỏi chủ kho. Vẫn có phương án có thể đo; chưa có căn cứ kết luận E1 bế tắc hoặc E2 hết ngân sách.

## BẢNG LỚP (i) — lớp MỞ của wp1466

| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| tien-kiem-lease-chua-du | F11.g: `--sau-dang` chưa thuộc danh sách và miễn lease theo ID tự khai; F11.h: import `os` ngoài nguồn trước T0; F11.i: scanner vẫn đọc tên Git không `-z` | P2 | Lớp r1–r6; biểu hiện đo/đọc trên r7 `3c89d87` | Kiểm closure cả luồng gọi và dependency, gồm argv, tiến trình cha và giao thức byte của scanner. Các chốt riêng thuộc ba biên khác nhau; cùng một nghĩa vụ tiền kiểm. | `closed_inputs.py`, `parent_boundary.py`, `quoted_names.py`. F11.g có đối chứng đổi kết quả; F11.h đo nguồn nạp, không dựng mã giả ĐẠT; F11.i đo quote trên tên có sẵn và đọc scanner, không dựng payload tên lease. |

## BẢNG LỚP (ii) — nợ kế nhiệm có authority

| slug lớp | biểu hiện | Issue kế nhiệm | tên nợ | bằng chứng wp1466 không còn khai gì |
|---|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc | F05.b/c | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | §0:21, §6, §14 loại consumer ngữ nghĩa; patch không đổi. |
| duong-dan-chua-khep-trong-goc | F06 | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | §0:21 loại ba reader cổng/ca/ADR; G1 chỉ đọc protocol. |
| moc-chuyen-tiep-mau-thuan | F07 | #1470 | INV-12-CONG-VERDICT-THEO-LOP | §0:22, §14 không đặt thiết kế/tiêu chí cutover trong wp1466. |
| schema-bo-sot-provider-hop-le | F10 | #1470 | INV-12-CONG-VERDICT-THEO-LOP | §0:22 loại schema/provider/consumer v2; patch không bổ sung. |

Authority kế thừa: quyết định E2 “Duyệt tách 3 packet”, [comment 7053593553](https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7053593553), được dẫn trong §0 và các verdict trước. Đã kiểm sự nhất quán của nội dung được giao, **không** readback GitHub trực tiếp để tái xác thực comment hoặc trạng thái Issue hiện tại. Nhãn CHƯA VÁ của bảng (ii) không kéo các nghĩa vụ đã tách có authority trở lại bảng (i).

## BẢNG SĂN

Các hướng dưới độc lập về cơ chế; biến thể trong một hướng không tính thành hướng mới. Lệnh chạy ở thư mục làm việc; output là trích từ log reviewer, không lấy số tác giả thay phép đo.

| hướng độc lập | LỆNH | OUTPUT THẬT | kết luận / giới hạn |
|---|---|---|---|
| 1. Tập ref phải so cả OID | `/usr/bin/python3 -B out/hunt.py` | `same_names_changed_oid`: rc1, thiếu 1 cặp/thừa 1 cặp | Bắt nhánh cùng tên đổi đầu. |
| 2. Ref riêng, worktree phụ, alternates | `/usr/bin/python3 -B out/hunt.py`; `/usr/bin/python3 -B out/followup.py` | Hai ca worktree rc1 đúng A; `ALTERNATES_REFSET_EXACT True REF_COUNT 2 PRIVATE_OBJECT_READABLE commit PRIVATE_REF_VISIBLE False` | Object riêng đọc được không đồng nghĩa ref riêng được quét; F11.d không tái mở. |
| 3. Grafts và môi trường Git | `/usr/bin/python3 -B out/hunt.py`; bộ 21 ca qua `run_mutations.py` | Graft trong clone làm ancestry tại clone rc0, tiền kiểm rc1; bốn biến `GIT_DIR`, `GIT_WORK_TREE`, `GIT_OBJECT_DIRECTORY`, `GIT_NAMESPACE` đều rc1 đúng lease A | Các đường này đã bị cô lập; không gọi mọi cấu hình đều an toàn. |
| 4. Policy thay đổi giữa 3d/3e | `/usr/bin/python3 -B out/followup.py` | `PAIRS_EQUAL_BEFORE_3E True`; policy/schema B cũ sau thay đổi rc1; cả ba `irrelevant_*` rc0 | F11.e sửa thật. |
| 5. Lịch sử policy và ranh giới “liên quan” | `/usr/bin/python3 -B out/closed_inputs.py`; bộ 21 ca | `merge_ours`/`merge_revert`: rc1, `policy 0+1`; `policy_notes_inside`: rc1; notes ngoài coordination hoặc tên không chứa chuỗi: rc0 | Không thấy bỏ lịch sử trong các topology đã thử; phạm vi substring rộng hơn hai tệp §5. |
| 6. PyYAML trực tiếp/gián tiếp | `/usr/bin/python3 -B out/hunt.py`; `/usr/bin/python3 -B out/followup.py`; bộ 21 ca | `LOCAL_DEPENDENCY False`; trace local `.py`/`.pyc` rỗng; `.pth` trỏ yaml clone bị dừng trước khi marker được tạo | Ba đường cũ đóng; đây không chứng minh mọi mã trước T0 đều đã cô lập. |
| 7. Biên tiến trình cha trước re-exec | `/usr/bin/python3 -B out/parent_boundary.py` | `OS_PRELOADED False`; không `-I`, có `-S -X frozen_modules=off`: `local_os true`; thêm `-I`: false; `-I` bình thường: rc0/ĐẠT | F11.h. Script ngoài clone, PYTHONPATH trỏ clone chứa os.py **nguyên trạng**. Ca có `-S` cuối cùng rc1 vì thiếu PyYAML. |
| 8. Danh tính miễn sau đăng | `/usr/bin/python3 -B out/closed_inputs.py` | `sau_before rc1`; `sau_other_packet_id rc0/ĐẠT`; `sau_missing_own rc1`; `sau_two_live_correct_id rc1` | F11.g: cùng V/B, argv đổi quyết định; không phải ref race. |
| 9. Giao thức tên đường dẫn của scanner | `python3 -B out/quoted_names.py` | Tên Unicode có sẵn: `default PARSED_EQUALS_PATH False SUFFIX_LOG False`; `nul ... True ... True`; blob B dòng749 không `-z`, dòng757 kiểm hậu tố | F11.i. Không tạo path đối kháng; hệ quả với lease YAML được phân tích bằng lời. |
| 10. Lỗi dữ liệu/công cụ và template local | `/usr/bin/python3 -B out/hunt.py`; `/usr/bin/python3 -B out/closed_inputs.py` | YAML hỏng, thiếu hàm, không master, server rỗng/vắng đều rc1; `local_init_template marker_copied false`; `clone_config_init_template rc0` | Không quy mọi đường fail-closed đều hỏng; config init.templateDir ở clone không lọt vào init kho tạm trong phép thử. |
| 11. Khóa byte, AST, runtime registry | `/usr/bin/python3 -B out/regression.py`; `/usr/bin/python3 -B out/independent.py`; `/usr/bin/python3 -B out/final_check.py` | `TONG 167 LECH 0 []`; 7 `HASH_MATCH True`; registry ghi đè mutant cũ rc1 | Kiểm lớp đã đóng và giới hạn AST bằng phép đo runtime riêng. |
| 12. Snapshot, drift và trần | `/usr/bin/python3 -B out/measure.py` | `BRANCH_REFS 393`; `TOTAL 434 4 FILES 4 HEADROOM 16`; tiền kiểm rc1 đúng B4; opt-in hợp lệ | Đo offline; không phải kết luận được cấp lease hay máy chủ hiện tại không đổi. |

## BẢNG ĐO

Môi trường Linux, Python **3.13.18**, Git **2.43.0**, Ruff **0.16.9**, `core.abbrev=7`. Đợt dựng bắt đầu **05:11:07 UTC 21-11-2026**. Các log có mốc UTC riêng. Khối r7 được trích từ blob đặc tả và so bằng byte với script giao kèm; các fixture và bản sao đặt dưới `out/`. `base` là `48d372e`, `prototype` là base + patch r5, `master` là `4e56f00` + cùng patch; không coi các cây thử này là H giao nộp đã được approve.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| SHA/băm | reviewed SHA và sha256 đầu báo cáo | tệp bằng blob; cả hai khớp | Có |
| Khối tiền kiểm | 137 dòng không trống | 137; byte script bằng fenced block | Có |
| Bộ cũ | 33/33 | `TONG 33 kịch bản: đúng 33 · sai 0` | Có |
| Bộ mới r7 | 21/21 | `TONG 21 kịch bản r7: đúng 21 · sai 0` | Có |
| 14 đột biến | từng tập ca đỏ như §18 | 14/14 đúng tập ca; số ca sai theo M1…M12: 6/3/1/2/4/2/3/2/1/1/1/1/1/1 | Có; xem bảng chi tiết dưới |
| F11.e cũ | bốn đường đổi rc0→1, đối chứng không liên quan giữ xanh | đúng bốn đường; `irrelevant_*` rc0 | Có |
| F11.f cũ | không nạp yaml từ clone | trace không còn local; sạch rc0, có A rc1 | Có cho các đường cũ |
| Danh sách đầu vào đóng | 11 V + 5 P bao hết quyết định | thiếu hợp đồng cho `--sau-dang`; nguồn import ở dòng đầu nằm ngoài biên P4 | Không — F11.g/h |
| Mọi ls-tree/log dùng -z | §18(i) | scanner blob B vẫn `ls-tree -r` không -z | Không — F11.i |
| Không đổi nguyên mẫu và khối khác | cùng patch r5; chỉ tiền kiểm đổi | patch bằng byte; 12/13 fenced blocks không đổi | Có |
| Checksum hiện vật | SHA256SUMS bundle | r7 26/26; nguyên mẫu r5 20/20 | Có với tập hiện vật được giao |
| Ráp protocol/ADR | sáu điểm ghép; ADR theo mẫu | 6 neo mỗi cái1; protocol bằng byte; ADR khớp sau 7 placeholder | Có |
| Bảng bất biến/nợ | 28 = 15 cổng + 12 kỷ luật + 1 chưa đo; 27 nợ | đúng các số hạng; cả 15 cổng có nợ; 25 tên được trỏ nằm trong 27 nợ; 18 tham chiếu ca | Có về dữ liệu, không suy consumer ngữ nghĩa |
| Mười luật gốc | giữ nguyên nghĩa/chữ sau nối dòng | 10/10 bằng sau nối dòng riêng từng mục | Có |
| Bảy đơn vị khóa | địa chỉ + băm raw + duy nhất | parser độc lập 7/7 địa chỉ/băm; mỗi raw1 lần; hằng mã bằng kết quả | Có |
| Biến thể khóa | 167 | 167/167, không lệch | Có |
| N8 | 109 dòng, 42 mã + 23 test | 42/42 mã; 23/23 test; 0 sai | Có |
| Sổ runtime | 1582→1639; Linux1581→1638; 57 mới; mutant1864→1890 | đúng số hạng, thứ tự nền, bộ ba mutant cũ và tập NHAM | Có |
| Răng sổ | ghi đè mutant cũ phải đỏ | `r1187_drop_doc_guard` bị phát hiện, registry rc1; cùng biến thể N8 rc0 | Có; runtime bổ sung cho AST |
| Ca liên quan | 190 doctrine và40 ADR | 190/190; 40/40; rc0 | Có |
| Mutant nguyên mẫu | 26 mới +21 cũ | 26/26 và 21/21 bị giết, đối chứng sống; nền 60/60 và 132/132, skip 0; rc0 | Có |
| Marker/target | mỗi marker1; ca mới có target | 26 marker đều 1; 57/57 ca mới có target | Có |
| Quét sáu cổng | các vector riêng từng tệp | 29 vector phân biệt đều khớp 6 số hạng | Có |
| Ruff | delta 0 | hai cây cùng16 lỗi: F8413/F4018/F5412/F8113; rc1 cả hai, delta 0 | Có; không gọi Ruff xanh |
| Kích thước | 4 tệp,+434−4 | code+76−1;test+163−1;protocol+46−2;ADR+149; còn16 dòng dưới450 | Có |
| Drift nền | tập đo không đổi | base→master29 commit/120 đường; giao tập đo bằng0 | Có với đúng tập đã khai |
| ADR |66 trên master, max0067; không nhánh cạnh tranh |66 trên base;67 trên cây thử;0 trong393 ref có0068+ | Có offline |
| Biên nhận |352, chưa có bang_lop |352/0 | Có offline |
| Ref hiện tại | S17:392 nhánh lúc04:56:46 | snapshot được giao393 nhánh | Khác mốc; không kết luận số quá khứ sai |
| Lease S17 |551/17/12/5 lúc04:57:23 | cùng mốc:551/17/12/5; lúc05:13:35 cũng vậy | Có |
| Cổng trên ba cây | doctrine-scan/adr-song | base, prototype, master+patch đều rc0; ADR 66/67/67 | Có offline |
| B4 chặn | hai đường code đang có người giữ | hai code rc11,docs rc0; tiền kiểm393ref/551bản ghi/5hiệu lực rc1 đúng B4 | Có offline |
| Trần0053/0055 | opt-in hợp lệ;6tệp/450dòng; lời gọi này8/10 | mỗi dòng1, RC kiểm ADR0/128, nằm first-parent; không shallow; không opt-in 0052 | Có về kho;8/10 theo chỉ thị |

Năm lease còn hiệu lực ở mốc đo: `wp1236-a-r10-g1-claude-20261121`, `wp1448-r6-g6-claude`, `wp1462-r8-g2-claude`, `wp1475-r1-g1-claude`, `wp433-r9-g5-claude`. Khối không đạt trên snapshot thật là kết quả đúng, không phải lỗi hạ tầng hay hồi quy.

## ĐỐI CHIẾU 14 ĐỘT BIẾN TIỀN KIỂM

Lệnh thực: `TMPDIR="$PWD/out/tmp" PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -B out/run_mutations.py out out/base/ops/lease_publish.py`. Lượt hợp lệ **05:13:23–05:23:35 UTC**, kết thúc rc0; mỗi lượt con được ghi riêng với rc thật. `python3 -B out/summarize_mutations.py` so **tập tên**, không chỉ số lượng: `TOTAL_MUTANTS 14 MATCH 14`. [Log tổng](mutations-rerun.log), [bảng máy đọc](mutation-summary.json).

| đột biến | số ca sai bộ 33 / bộ 21 | tập đích đo được |
|---|---|---|
| M1 | 6 / 0 | sáu `rieng_*` |
| M2 | 1 / 2 | B riêng; hai graft |
| M3 | 1 / 0 | scanner trong cây làm việc bị sửa |
| M4 | 2 / 0 | policy và schema hiện diện |
| M5 | 0 / 4 | policy xóa, thêm rồi xóa, nhánh phụ, xóa trong merge |
| M5b | 0 / 2 | nhánh phụ và xóa trong merge |
| M6 | 0 / 3 | ba `f_khong_I_*` |
| M7 | 0 / 2 | yaml từ clone qua .pth; thiếu yaml |
| M8 | 0 / 1 | .pth import module clone |
| M9a | 0 / 1 | git trong clone trước T1 |
| M9b | 0 / 1 | git cây chính khi chạy worktree phụ |
| M10 | 0 / 1 | GIT_GRAFT_FILE |
| M11 | 0 / 1 | server đổi ở T6 |
| M12 | 0 / 1 | info/grafts trong clone |

Bản r6 nguyên văn: bộ 33 đúng 33, bộ 21 sai 17; bản r5: bộ 33 sai 9, bộ 21 sai 18. Các số và tên đích khớp §18.

Cần đọc chính xác câu ở §1 “không đột biến nào làm đỏ một ca ĐẠT”: nếu **ĐẠT là kết quả tiền kiểm rc0** thì câu đó sai. M6 làm cả ba `f_khong_I_*` từ rc0 thành rc1 tại T4, marker vẫn vắng; chính bảng V6 xếp chúng ở cột ca ĐẠT. Tập mục tiêu M6 vẫn đúng như tác giả chỉ định, không có ca ngoài tập bị ảnh hưởng. Đây là giới hạn cách diễn đạt số đo của cùng lớp tiền kiểm, không phải một mutant còn sống hay một lớp mới. Nó cũng cho thấy M6 chứng minh hành vi tự re-exec, không tự chứng minh an toàn của mọi mã chạy trước re-exec.

## ĐÁNH GIÁ DANH SÁCH VÀ CÁC TIỀN ĐỀ

**V1–V5:** Ref, ancestry và lựa chọn blob đã có đối chứng thật. T6 bổ sung việc hỏi lại cả cặp tên/OID ở cuối. T2 bắt policy/schema trên master V và lịch sử thêm/xóa/merge đã đo. Tuy nhiên ghim blob scanner ở B chỉ bảo đảm **chạy đúng mã đã chọn**, không chứng minh mã ấy đọc đủ mọi lease; F11.i nằm bên trong dependency đó. V3 nêu B nhưng không có dòng tương ứng cho đối số `--sau-dang` dù đối số này trực tiếp loại một người giữ khỏi kết quả.

**V6–V8:** `-I` có hiệu lực trong tiến trình con và đã chữa các đường PyYAML cũ. V7 kiểm vị trí trước import có ích; ca `.pth` tới YAML clone dừng trước marker. V8 chỉ kiểm các mục **còn hiện diện** trong `sys.modules` tại T7, sau khi import đã thực thi. Nó không phải nhật ký mọi mã từng chạy, không thấy tiến trình cha, và không chứng minh mã ngoài danh sách chưa gây tác dụng trước chốt. Hướng một module tự gỡ khỏi bảng hoặc thay metadata chỉ mô tả bằng lời, không soạn payload. Không thêm finding đã-thử cho hướng chưa dựng đó. F11.h đã có phép đo độc lập, không cần giả thuyết module độc hại để bác câu “os đã nạp sẵn, không tra sys.path”.

**V9–V11:** Hai chốt vị trí git, môi trường cục bộ dựng từ rỗng và việc dùng kho tạm có ca/đột biến riêng. Với worktree phụ, chính tác giả đã khai git trong cây chính có thể chạy ở T1 rồi mới bị chặn; đó là kiểm kết quả sau chạy, không bảo đảm “không mã nào từ clone từng chạy”. Không suy rộng V9 thành kiểm nội dung hay chữ ký git. `info/grafts` cục bộ và GIT_GRAFT_FILE bị chặn trong các phép đo; không có phản chứng mới ở hai đường này.

| tiền đề | đánh giá tính hợp lý / có thể đóng rẻ hơn không | giới hạn đo |
|---|---|---|
| P1 — đường tới máy chủ, auth/proxy/config vận chuyển | Hợp lý làm gốc tin cậy vận hành: script cục bộ không tự chứng minh bên trả lời là GitHub thật. Có thể ghim URL/transport nếu muốn thu hẹp, nhưng xóa mọi config auth làm mất đường đo thật. Không xem ls-remote khớp là bằng chứng xác thực máy chủ. | Chỉ origin giả và mirror được giao; không kiểm server, proxy, auth thật. Không đọc secrets. |
| P2 — config clone | Chấp nhận tiền đề trong phạm vi các lời gọi clone và P1, nhưng câu “chỉ đẩy về DỪNG hay chọn B đã công bố” là lập luận có điều kiện: phải tin Git và kho tạm thực sự tách cấu hình. Thử `init.templateDir` local với marker dữ liệu cho thấy init kho tạm không copy marker. Không có bằng chứng để nâng thành cách ly mọi config. | Không chứng minh mọi khóa/include, khác owner/safe.directory, mọi loại worktree. Không báo một bypass config chưa đo. |
| P3 — nội dung interpreter/stdlib/site-packages/git | Hợp lý làm phần mềm nền tin cậy. Kiểm vị trí không kiểm nội dung; thêm một checksum cũng chỉ dời gốc tin cậy sang manifest. Nhưng P3 không bao gồm một `os.py` nằm trong clone; vị trí ngoài danh sách không tự thành tin cậy chỉ vì thực thi ở parent. | Không audit mọi thư viện, loader, file `.pth`, native extension, template/cache cài đặt của Git, hoặc khả năng tự sửa metadata. |
| P4 — mã trước dòng đầu khi gọi thiếu -I | Việc thừa nhận tác dụng startup là đúng. Tự re-exec không hoàn tác parent; vì vậy không được gọi đường hỗ trợ này là fail-closed từ lúc khởi động. Biên tiền đề hiện tại **hẹp hơn thực tế**: F11.h chạy ở dòng đầu, trước T0. Đây là biên có thể thu hẹp bằng hợp đồng invocation tin cậy/không hỗ trợ tự cứu từ một parent chưa tin cậy; không có lý do coi mọi cờ được giữ nguyên đều đã cô lập. | Đã đo -S/-X và đối chứng -I, không viết module làm giả kết quả. Không thể dùng T7 trong child để chứng minh lịch sử parent. |
| P5 — clock, TMPDIR, SHA-1/object | Đồng hồ và tính toàn vẹn kho object là tiền đề hệ thống hợp lý; ảnh chụp không tự xác thực chúng. TMPDIR có thể ghim vào scratch được kiểm để thu hẹp với chi phí thấp, nhưng chưa thấy phản chứng gây xanh giả và không nâng gợi ý này thành finding riêng. | Không đổi đồng hồ, không thử va chạm/object bị can thiệp, quyền thư mục của chủ khác hay race cùng UID. |

**Policy có quá hẹp/quá rộng không:** với đúng §5 của protocol được giao, cả hai đường policy/schema được nêu tên đều nằm trong tập của r7; các thử thêm/xóa, nhánh phụ, merge `ours`, merge rồi revert không tìm thấy bỏ sót. Ngược lại, substring `change-impact` dưới toàn `.github/coordination` **rộng hơn** hai đường canonical: một tệp ghi chú bình thường tên `change-impact-notes.md` cũng làm rc1 và bị gọi là policy. Cùng nội dung ở `docs/` hoặc tên `notes.md` thì rc0. Đây là một điều kiện bắt đầu bảo thủ được khai rõ, chưa phải xanh giả; không mở lớp mới vì việc đó. Nó không phải phép đọc ngữ nghĩa policy: câu “re-evaluate theo §5” không chứng minh tệp ghi chú thực sự đổi closure. Nếu sau này nguồn policy có thẩm quyền được chuyển ra ngoài tập đó, phạm vi phải được xét lại; review này không chứng minh tương thích mọi protocol tương lai.

## L3, L6, L7 VÀ TRẦN

**L3:** Các chốt tiền kiểm được liệt kê có răng trong các ca được liệt kê. Tổng 54/54 và việc giết 14 đột biến chỉ chứng minh các chốt đó; chúng không chứng minh danh sách đầu vào đủ. Không có ca r7 kiểm danh tính của tham số miễn sau đăng, tổ hợp cờ parent nêu ở F11.h, hay giao thức tên của scanner F11.i. Phản chứng độc lập mở rộng thước đo ra ngoài danh sách tác giả. Những ca sau land/CI/Windows vẫn chưa đo, không coi là đạt.

**L6:** Bảy khóa được tự tính từ địa chỉ và byte thô, có dương/âm và đối chứng ngoài đơn vị; 167 biến thể kiểm CRLF/whitespace/hiển thị/duy nhất. Không nối dòng để làm khóa raw xanh. Với mười bất biến gốc thì nối dòng riêng từng mục để so, không ghép qua mục. Vector cổng được đo riêng trên đủ sáu vị trí §20, không dùng tổng gộp. Có chuỗi tên cổng không đồng nghĩa cổng cưỡng chế ngữ nghĩa. F11.i cho thấy lời khai bao quát các lệnh gọi cũng phải kiểm cả dependency, không chỉ grep khối ngoài.

**L7/ADR-0067:** Không tự đặt ngân sách mềm hay yêu cầu hỏi chủ kho ở lượt thứ N. C1/C4 E5 và C3 E2 của §17 vẫn là các quyết định cần đúng authority; review này không tạo lời duyệt băm, miễn Windows, audit hoặc quyền merge. Quyết định đi thẳng master chỉ bao ba packet #1466/#1469/#1470, không đổi đường land B4. Mục sổ `xet_lai_cach_lam` r7 được dùng theo bản tóm trong chỉ thị, không giả nhận đã mở URL không truy cập được.

**ADR-0053/0055:** Hai opt-in ghim đúng commit land; mỗi dòng một lần, file ADR có ở commit và không có ở parent thứ nhất, commit nằm trên first-parent master của mirror. Không có opt-in 0052. Nguyên mẫu **4 tệp, +434 −4**, dưới trần **6 tệp/450 dòng thêm**, dư 16 dòng; không bảo đảm mã giao nộp sau B4 vẫn trong trần. Lượt gọi này **8/10 theo chỉ thị**, không reset theo revision/provider; còn 2 lời gọi trên trục này nếu không có tiêu dùng khác chưa được giao. Không tự đo lịch sử API hay backend model/effort; không cấp thêm ngân sách từ báo cáo.

### tien-kiem-lease-chua-du [P2] Danh sách chưa bao hết đầu vào và chưa kiểm đủ các nguồn đọc gián tiếp

**TỆP/DÒNG:** `cay-kho/ops/specs/wp1466.md:71` (hợp đồng danh sách đóng), `:78` (tự chạy lại), `:81`–`:88` (import trước chốt), `:91` (argv), `:185` (gọi scanner), `:209`–`:214` (miễn theo ID), `:224`–`:239` (V/P), `:981` (giới hạn, lời khai `-z`). Dependency được nạp từ blob B: `cay-kho/ops/lease_publish.py:749`, `:757`.

**VẤN ĐỀ:**

**F11.g — đầu vào miễn trừ sau đăng vắng khỏi danh sách.** `sau` được lấy trực tiếp từ `sys.argv`; V3 chỉ nói tới B, không V/P nào nhận danh tính lease được miễn. Vòng giao write set bỏ qua mọi bản ghi có `lid == sau`; kiểm cuối chỉ đòi có một bản ghi còn hiệu lực mang ID đó. Không có liên kết tới lease wp1466 vừa được đăng, packet/revision/generation hay băm đặc tả đang dùng.

Phép đo dùng dữ liệu bình thường, một lease A hợp lệ về các trường mà scanner đọc, còn hạn đến 2030 và giữ `.claude/dev/packet_loop.py`. Trên **cùng B/V**, không cờ trả rc1 vì A; truyền ID của A vào `--sau-dang` trả rc0/ĐẠT dù chưa có lease wp1466. Truyền ID wp1466 vắng mặt thì rc1; đăng thêm lease wp1466 và dùng đúng ID ấy thì vẫn rc1 vì A. Như vậy đã phân biệt được đầu vào bị bỏ sót với ref race, lỗi fixture hoặc việc bỏ qua lease của chính mình theo thiết kế.

Đây không phải cáo buộc workflow thật đã truyền nhầm ID hay đã cấp quyền sai. Người chạy đúng hướng dẫn có thể cung cấp đúng ID; vấn đề là danh sách được khai là đóng **mọi đầu vào quyết định**, trong khi giá trị miễn trừ quan trọng này vừa không được đóng, vừa không được khai/biện minh thành tiền đề. Chỉ thêm tên nó vào bảng mà không ràng buộc danh tính sẽ không chứng minh tính chất “lease vừa đăng của wp1466”.

**F11.h — mã ở dòng đầu chạy trước ranh giới mà P4 khai.** Khối bắt đầu bằng `import os, sys`, sau đó mới kiểm `sys.flags.isolated`. Chú thích khẳng định os đã được nạp sẵn nên không tra sys.path. Điều đó sai với các cờ khởi động mà V6 chưa loại trừ: `-S -X frozen_modules=off`.

Tôi chép **nguyên** `os.py` từ stdlib vào clone, giữ script tiền kiểm **ngoài** clone, đặt PYTHONPATH trỏ clone. Trace thật cho thấy parent nhập clone/os.py ngay ở dòng đầu, rồi mới exec child isolated. Đo riêng trước script: `OS_PRELOADED False`. Thêm `-I` ngay từ đầu loại nguồn local; bỏ `-X frozen_modules=off` cũng loại nó trên Python 3.13 này. Chạy `-I` bình thường vẫn ĐẠT trên kho sạch. Ca có `-S` cuối cùng DỪNG vì PyYAML không nằm trên đường nạp: **không** gọi nó là xanh giả, nhưng việc thực thi mã ngoài nguồn trước chốt đã được xác nhận.

P4 chỉ khai mã chạy **TRƯỚC dòng đầu**, như sitecustomize/usercustomize. Import này chạy **TẠI dòng đầu**, nên không thuộc tiền đề đó. V6 hứa cờ/PYTHONPATH/script directory được đóng; T7 ở child không còn nhìn thấy module parent. Nếu mã clone thực hiện tác dụng hoặc kết thúc trước re-exec thì chốt sau không chứng minh fail-closed; phần hệ quả này chỉ mô tả bằng lời, không dựng payload. Chữa bằng cách ngầm hiểu P4 rộng hơn chính câu viết sẽ làm đặc tả lại khai mạnh hơn phép đo.

**F11.i — lời khai `-z` không phủ scanner gián tiếp.** §18(i) viết mọi ls-tree/log của quyết định dùng `-z`, nên core.quotePath không đổi tên được đọc. Nhưng `_quet_lease_toan_kho`, được khối gọi ở T4, vẫn chạy `_git(..., "ls-tree", "-r", ref, "--", "ops/leases")` tại blob B dòng749. Sau tách tab, nó kiểm `duong.endswith((".yaml", ".yml"))` và bỏ qua khi sai, không giải mã tên được Git quote, không báo không đo được.

Theo đúng giới hạn thử nghiệm của chỉ thị, tôi không tạo tên lease đối kháng. Tôi dùng một tên Unicode **đã có sẵn** trong kho để đo cách Git trả tên: output mặc định có dấu nháy bao quanh, tên parse không bằng path và kiểm hậu tố `.log` trả False; cùng lệnh thêm `-z` thì bằng path và hậu tố trả True. Đây là bằng chứng về giao thức Git đang dùng, không phải lời khai đã chạy một ca bỏ lease đầu-cuối.

Hệ quả với lease chỉ mô tả: một tên YAML bị Git quote sẽ có dấu nháy đóng ở cuối, nên rơi vào `continue` trước safe_load và trước các kiểm hiệu lực/write set. Khối không có chốt kiểm các tên bị bỏ, không có tiền đề “mọi tên lease luôn thuộc tập tên không bị quote”. Scanner vẫn nhìn ref đúng V nhưng có thể trả tập lease thiếu. Việc lease_id trong **nội dung** phải ASCII không kiểm tên tệp đã bị loại trước khi đọc; validator `ops/thu-hoi` ở phần khác cũng không nằm trên đường gọi này. Đã xác nhận lời khai `-z` sai bằng mã và phép đo; chưa đo thực tế máy chủ có một lease như thế.

Ba biểu hiện giữ **P2** của lớp tiền kiểm: phải giải quyết trước khi approve đặc tả còn hứa tiền kiểm này. Không chuyển chúng sang nợ #1469/#1470, không gọi lớp mới, không tái mở các lớp đã đóng về khóa protocol hoặc N8.

**GỢI Ý VÁ:** Dữ liệu thiết kế để người soạn tự dẫn xuất: lập bảng theo **toàn bộ graph gọi**, gồm argv và định danh lease bị loại, mã chạy trước isolated boundary, và mọi giao thức dữ liệu của scanner. Với `--sau-dang`, đối chiếu định danh đầy đủ với bằng chứng lease vừa đăng hoặc khai rõ một tiền đề người gọi và vì sao chưa kiểm; chỉ regex ID không đo được quyền miễn. Với parent, xác định invocation tin cậy ngay từ đầu, phạm vi cờ được hỗ trợ và phần nào không thể cứu bằng re-exec; bản sao os.py nguyên trạng là đối chứng tái lập được. Với tên Git, dùng decoder/giao thức NUL hoặc chốt fail-closed trên tập tên có thể đọc đầy đủ trước khi gọi scanner cũ. Nếu cần đổi hợp đồng/scanner ngoài phạm vi hiện tại thì đó là revision thiết kế, không reviewer tự vá kho. Các phép dương/âm và đột biến cần nhắm từng tính chất này, đồng thời giữ các ca ref/policy đã xanh.

**ĐÃ THỬ NGHIỆM:** [closed_inputs.py](closed_inputs.py), [closed-inputs.log](closed-inputs.log), [parent_boundary.py](parent_boundary.py), [parent-boundary.log](parent-boundary.log), [quoted_names.py](quoted_names.py), [quoted-names.log](quoted-names.log). Output tiêu biểu:

```text
sau_before: rc 1, lease ... ['fxa-r1-g1-claude']
sau_other_packet_id: rc 0, TIỀN KIỂM: ĐẠT
sau_missing_own: rc 1
sau_two_live_correct_id: rc 1, lease ... ['fxa-r1-g1-claude']
external_nonisolated_nosite_nofrozen: rc 1, local_os true
external_isolated_nosite_nofrozen: rc 1, local_os false
external_isolated_normal: rc 0, local_os false, TIỀN KIỂM: ĐẠT
OS_PRELOADED False
CASE default PARSED_EQUALS_PATH False SUFFIX_LOG False
CASE nul PARSED_EQUALS_PATH True SUFFIX_LOG True
```

Các dòng trên chỉ rút tên nhãn/phần liên quan; log/JSON đầy đủ giữ nguyên câu lệnh và output. Không có patch production hoặc sửa branch executor; bản sao nguyên mẫu dùng để kiểm, không phải hint đã được approve.

**ĐỘ TIN:** Cao cho F11.g và nguồn import F11.h (Python/Git thật, đối chứng trên cùng trạng thái); cao cho mâu thuẫn `-z` và nhánh bỏ tên trong scanner. Hệ quả bỏ lease F11.i là phân tích đường mã có bằng chứng về định dạng đầu vào, **chưa** tái hiện đầu-cuối vì giới hạn không dựng payload đường dẫn. Không suy ba phép này thành bằng chứng đã cấp lease sai thật trên GitHub.

## HIỆN VẬT VÀ NHỮNG GÌ KHÔNG ĐO ĐƯỢC

- `hunt.py` và `followup.py` là bản sao nguyên byte từ lượt 6; helper 33 cũng nguyên byte r6. `checksum-and-refs.log` ghi phép so. Khối tiền kiểm trích từ spec, không sửa để đo nền.
- `run_mutations.py` dùng đúng 14 biến thể của tác giả, thêm ghi log từng lượt con và tắt ký commit **chỉ trong fixture**. Lần thử đầu `mutations.log` hỏng ở commit fixture vì global signing gọi dịch vụ không truy cập được; không ca nào ở lần đó được tính là mutant bị giết. Lượt có bằng chứng hợp lệ ở `mutations-rerun.log` và `mutation-details/`.
- `setup.py`, `regression.py`, `independent.py`, `measure.py`, `counts.py`, `final_check.py` dựng và đo bản sao riêng. Phép đọc băm địa chỉ/raw độc lập không import parser sản phẩm. Các log cũ được giữ để giải thích lỗi harness, không thay dữ liệu mới.
- Source snapshot trước/sau gồm tracked/untracked/ignored, nội dung, size, mtime và đích symlink của `cay-kho` và `kho.git`; kết quả `final-check.log`: 18.089 mục ở cả hai mốc, delta 0; `git status` rỗng, HEAD/tree/spec hash giữ nguyên. Snapshot hai mốc không chứng minh không từng ghi rồi hoàn nguyên giữa hai mốc. Sandbox thực là workspace-write; tính read-only của cây nguồn ở đây dựa trên cách gọi lệnh và phép đối chiếu, không giả nhận kernel khóa mọi file nguồn.
- Không đo GitHub thật, Issue/comment/ruleset/branch protection hiện tại, lịch sử API, model/effort backend hoặc session identity được máy xác thực. Mirror 393 nhánh là snapshot, không thay lần fetch/ls-remote ở lúc cấp lease thật.
- Không chạy full suite toàn kho, full mutant CI, Windows, N16 sau land, hay mã B4 tương lai. Cổng chọn lọc trên prototype/master+patch không thay các gate bắt buộc trên H giao nộp. Không có quyền miễn Windows, cấp lease, audit, merge hoặc deploy phát sinh từ verdict.
- Không dựng payload mã độc, traversal, tên lease đối kháng, module tự che dấu hoặc giả máy chủ. Không chứng minh an toàn cho mọi loader, template/cache Git, config include, safe.directory, object hỏng, race hay thời gian. Các khả năng chỉ mô tả bằng lời được tách khỏi kết quả đã chạy.

Đóng gói hiện vật: [SHA256SUMS](SHA256SUMS); kiểm cuối ở [seal.log](seal.log). Với bảng (i) còn một lớp P2, verdict là **changes_requested**.
