verdict: changes_requested
reviewed_sha: 05d12f1e326a7822a8d94b699eee32926af3284c
spec_sha256: 5357004a67d83528dc903d6a29a989eeedc373d21ec4812d453db95320ef84f4
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop_mo_wp1466: 1, so_bieu_hien_mo: 1, P0: 0, P1: 0, P2: 1, P3: 0, so_lop_no_ke_nhiem: 4}
hoi_tu: {U: 3, F: 2, ty_le: "2/3 = 66,67%", lop_moi: 0, lop_tai_mo: 0, lop_lan_thu_nam: [kiem-chuoi-khong-doc-cau-truc, duong-dan-chua-khep-trong-goc, moc-chuyen-tiep-mau-thuan, tieu-chi-dong-xoa-khong-do-hanh-vi, schema-bo-sot-provider-hop-le, tien-kiem-lease-chua-du]}

Review **đặc tả r5**, không phải approval mã thi công hay quyền cấp lease/merge. Băm được kiểm đầu tiên, khớp cả tệp local lẫn blob tại reviewed_sha; tree nguồn là `863bdf10a88490ee381955b135a98341178dcd9c`. Nguyên mẫu được tự dựng từ mirror: checkout `48d372e14f190dae83a75ccbca8ee9a0b25635c5`, áp patch bằng `git apply -p1`; dựng thêm một bản trên `5a152c18dfb0890a9031bf05c31ab7cab534a652`. Hai bản ấy là working tree thử, không phải H đã nghiệm thu.

**Còn một P2:** tiền kiểm xác minh tập ref `origin` nhưng quyết định hiệu lực lease từ tập ref rộng hơn. Bản ghi thay thế chưa công bố, chỉ có trên nhánh local hoặc remote phụ, làm cả bước 3c, 3d và 3e bỏ qua lease đang giữ tệp trên máy chủ. Đã tái hiện riêng hai đường vào và đối chứng đảo màu khi gỡ riêng ref chưa công bố. Vì thế chưa đóng được `tien-kiem-lease-chua-du`.

Các số chính tái lập được: +434/−4 trên 4 tệp; Ruff F 16→16; 190/190 ca; 26/26 đột biến mới, 21/21 cũ; 48/48 phản chứng lượt 4 và tổng 167/167 phép byte; N8 65/65; tiền kiểm mẫu 19/19. Hai cổng trên master mới đều rc 0. Tổng xanh này không phủ phản chứng ngoài ma trận về nguồn ref.

Môi trường đo: Linux, Python 3.13.18, Git 2.43.0, Ruff 0.16.9; `core.abbrev=7`; ngày 21-11-2026 UTC. ID phiên và model/effort thực phục vụ không có bằng chứng đủ để đo: `KHONG_DO_DUOC`. `6333e553` là mã run được giao, không tự coi là session ID của model. Assurance đầu tệp chỉ là mức đề nghị cho cặp họ model, không phải kết luận approve.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### Theo từng finding

Đã đọc và lập đối chiếu trước khi săn thêm. Nguồn là verdict r4 trên `937d135d903fe71a1660b138ebb2234cbc10bdbc`, băm tự đo `400234b2ce15af8ed09571643f695fea56744bd10a12b03d500e9177e7039175`, đúng băm r5 khai. Bảng dưới đủ **5 nhóm biểu hiện bảng (i)** và **5 nhóm biểu hiện thuộc 4 lớp bảng (ii)** cuối lượt 4. Các nhãn không gọi việc chuyển phạm vi là vá.

| finding lượt 4 | slug | nhãn | bằng chứng tự đo |
|---|---|---|---|
| F05.f — lớp đọc văn bản làm mất CR trong K01–K07 | kiem-chuoi-khong-doc-cau-truc | ĐÃ VÁ THẬT | `byte-probes.log`: 7/7 `crlf_inside_K*` nay rc 9; parser byte riêng băm 7/7 đơn vị chuẩn đúng. Vòng mutant thật giết `inv_doc_qua_text` bằng 9 ca. |
| F05.g — cắt khoảng trắng cuối mục K01/K03 | kiem-chuoi-khong-doc-cau-truc | ĐÃ VÁ THẬT | Cả hai `trailing_space_K01/K03` rc 9; mở rộng cả bảy khóa, tab/NBSP/CR và dòng biên đều đúng màu. `inv_cat_cuoi_muc` bị giết bởi 5 ca; không dùng chỉ hai phản chứng cũ để đóng. |
| F08.c — binding ở default/decorator/DEF | tieu-chi-dong-xoa-khong-do-hanh-vi | ĐÃ VÁ THẬT | `pv_ma.log`, `pv_test.log`: 8 biến thể từ reviewer r4 đều đỏ; default/decorator ở cả hai chế độ và class-global bị chặn. Cả ma trận 42+23 đúng; cây nguyên mẫu hợp lệ vẫn xanh. Annotation bị compile từ chối, không tính nó như một bypass hành vi hợp lệ. |
| F11.b — closure trước cấp lease | tien-kiem-lease-chua-du | ĐÃ VÁ THẬT | Trong phạm vi bốn đường của wp1466: policy/schema có mặt đều dừng, policy vắng mới xét tiếp; prefix/case/effective-only/planned của fixture đều bị chặn. `preflight19-rerun.log` 19/19; `preflight-snapshot.log` xác nhận policy 0 trên B. Không suy đã có công cụ closure tổng quát. |
| F11.c — chưa có tiền kiểm đủ nghĩa vụ trước công bố | tien-kiem-lease-chua-du | VÁ HỜ | Có khối trước/sau công bố thật, nhưng `preflight-extra.log` cho thấy cả 3c/3d/3e xanh khi dữ liệu chưa công bố triệt tiêu người giữ thật. Cơ chế xét giao vẫn dựa vào tập lease chưa chứng minh được nguồn. |
| F05.b — khai báo ca theo cấu trúc | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | Patch không có consumer đối chiếu ca với ô INV; §0/§6/§14/§19 tiếp tục bỏ nghĩa vụ và giao #1469. N8 đọc AST để canh phạm vi sửa, không nhận lại hợp đồng ngữ nghĩa ca của #1469. |
| F05.c — nợ phải thuộc mục Nợ | kiem-chuoi-khong-doc-cau-truc | CHƯA VÁ | Tự đếm 25 tên được trỏ đều nằm trong 27 nợ ADR chỉ chứng minh dữ liệu hiện tại. Cổng mới không mở ADR để kiểm quan hệ này; phần consumer vẫn ở #1469. |
| F06 — containment tệp cổng/ca/ADR kế nhiệm | duong-dan-chua-khep-trong-goc | CHƯA VÁ | Cổng nguyên mẫu chỉ mở protocol. Hai ca G1 có sẵn chạy đạt, mutant G1 giết 1; không coi đó là vá containment ba loại tệp thuộc #1469. |
| F07 — vị từ và nghiệm thu cutover | moc-chuyen-tiep-mau-thuan | CHƯA VÁ | Không vị từ/bộ ca cutover trong patch hay N1–N16; §0/§14 giao #1470. Bảng hiệu lực ADR vẫn chỉ định thời điểm. |
| F10 — schema identity v2/consumer | schema-bo-sot-provider-hop-le | CHƯA VÁ | Không schema v2 hay consumer identity mới trong bốn tệp; phần thiết kế/tiêu chí tiếp tục thuộc #1470. Việc đổi người soạn không thêm lời hứa schema. |

### Theo lớp

| slug | nhãn lớp | biểu hiện còn mở | thuộc bảng (i) hay (ii) và vì sao |
|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc — phần wp1466 | ĐÃ VÁ THẬT | 0 trong phạm vi bảng (i) | F05.f/g đã đóng; các phép byte, biên, che tại địa chỉ, nhân bản và ID đều được chạy lại. |
| kiem-chuoi-khong-doc-cau-truc — phần kế nhiệm | CHƯA VÁ | F05.b/c | (ii): đủ cắt lời hứa, tên nợ và #1469. Không tuyên bố toàn bộ slug lịch sử đã được vá. |
| tieu-chi-dong-xoa-khong-do-hanh-vi | ĐÃ VÁ THẬT | 0 | F08.c đóng; ngữ pháp cho được nguyên mẫu thực, ngăn các đường binding cũ đã kiểm. Tác dụng phụ động được r5 khai giới hạn riêng. |
| tien-kiem-lease-chua-du | VÁ HỜ | F11.c/d: dữ liệu ref chưa xác minh làm sai người giữ | (i): điều kiện bắt đầu 3d/3e vẫn hứa xác minh không người giữ khác. INV-02 tổng quát không nhận thay nghĩa vụ này. |
| duong-dan-chua-khep-trong-goc | CHƯA VÁ | F06 | (ii), #1469; không có lời hứa mới kéo về wp1466. |
| moc-chuyen-tiep-mau-thuan | CHƯA VÁ | F07 | (ii), #1470; không có lời hứa mới kéo về wp1466. |
| schema-bo-sot-provider-hop-le | CHƯA VÁ | F10 | (ii), #1470; không có lời hứa mới kéo về wp1466. |

**Hội tụ theo chỉ thị lượt này:** U là ba lớp bảng (i) cuối lượt 4. F là phần wp1466 của `kiem-chuoi-khong-doc-cau-truc` và lớp `tieu-chi-dong-xoa-khong-do-hanh-vi`: **2/3 = 66,67%**. Không đưa nợ bảng (ii) vào tử số hoặc mẫu số. Đoạn cuối §19 r5 dùng U=6 và nêu trần 3/6 hoặc 2/6; tôi ghi rõ khác biệt ấy, áp U=3 được chỉ thị giao, không dùng cách tính trong đặc tả để thay quy ước review này.

Không lớp mới; không lớp đã đóng bị tái mở. Biểu hiện F11.d nối thẳng lớp cũ F11; hai namespace ref là hai đường vào cùng **một nhóm biểu hiện**, không tạo hai slug. Không tách/gộp lớp nên không cần bảng đổi slug. Sáu slug ở `lop_lan_thu_nam` giữ đủ lịch sử năm lượt, kể cả phần đã chuyển kế nhiệm hoặc vừa đóng ở lượt này. Checkpoint §12 sau lượt 3 đã được ghi theo sự kiện giao; số lần lặp tự nó không là lý do đổi verdict. Điều chưa chữa đúng gốc ở F11 là xác minh **nguồn dữ liệu quyết định**, không chỉ thêm bước so đường dẫn và chạy lại cùng phép đọc.

Các lớp đã đóng trước r5 được soi lại: 7 băm chuẩn, 10 nguồn nguyên văn, 15/15 ô cổng có nợ, ca dời/nhân bản, 26 mốc duy nhất, đăng ký động và hai vòng mutant thật đều giữ kết quả. Quyết định E5 về chuỗi ba packet vẫn có đúng phạm vi; chưa thấy tái mở các lớp ấy.

## BẢNG LỚP (i) — lớp MỞ của wp1466

| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| tien-kiem-lease-chua-du | F11.c tiếp tục; F11.d: ref chưa công bố tham gia bia mộ, làm 3c/3d/3e xanh giả. Một nhóm, hai đường vào local-head và remote phụ. | P2 | r1 → r2 → r3 → r4 `937d135` → r5 `05d12f1` | Ràng buộc tập ref quyết định lease với tập đã được xác minh; dùng cùng bất biến ở trước và sau đăng. Không vá riêng theo tên nhánh fixture. | Hai thử nghiệm độc lập đều xanh; bỏ riêng ref chưa công bố thì đỏ. Không cấp lease GitHub, không thực sự chạy hai executor. |

## BẢNG LỚP (ii) — nợ kế nhiệm có authority

| slug lớp | biểu hiện | Issue kế nhiệm | tên nợ | bằng chứng wp1466 không còn khai gì |
|---|---|---|---|---|
| kiem-chuoi-khong-doc-cau-truc | F05.b/c: AST ca và quan hệ nợ với mục Nợ | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | §0/§6/§14/§19 cắt hợp đồng; N8/so-dang-ky kiểm phạm vi và bảo toàn sổ, không kiểm ngữ nghĩa ô INV/ca hay mở ADR từ tham chiếu. |
| duong-dan-chua-khep-trong-goc | F06: giữ đích đọc của tệp cổng, ca, ADR trong gốc | #1469 | INV-BANG-DOI-CHIEU-NGU-NGHIA | Không ba loại reader ấy trong patch. G1 duy nhất của wp1466 là protocol. |
| moc-chuyen-tiep-mau-thuan | F07: cutover | #1470 | INV-12-CONG-VERDICT-THEO-LOP | Không vị từ, thiết kế hay tiêu chí cutover trong wp1466. |
| schema-bo-sot-provider-hop-le | F10: identity v2 | #1470 | INV-12-CONG-VERDICT-THEO-LOP | Không schema/consumer v2 mới; không tiêu chí wp1466 nghiệm thu phần này. |

Authority E2/E5 lấy từ sự kiện của chỉ thị và bản chép trong đặc tả; không tự khai đã readback comment GitHub. Nợ INV-02 tổng quát chưa có Issue riêng, nhưng không dùng nó chuyển F11 đang mở ra bảng (ii).

## BẢNG SĂN

Lệnh chạy từ thư mục làm việc được giao. Log kèm theo là output của lượt này; các script người soạn được đọc rồi chép/chạy trên cây reviewer tự dựng. Parser băm, phản chứng ref và các phép đo bổ sung do reviewer dựng. Lỗi setup được tách khỏi kết quả sản phẩm.

| hướng độc lập | LỆNH | OUTPUT THẬT | kết luận |
|---|---|---|---|
| 1. OID, băm, master drift, trần | `python3 -B out/measure.py` | `SPEC_BLOB_EQUALS True`; `ORIGIN_REFS 393 BRANCHES 392`; `MASTER_DRIFT 24 commits 116 paths`; `MEASURED_CHANGED ['.claude/skills/work-packet/SKILL.md']`; `TOTAL 434` | Tệp adapter được cổng quét có đổi; đã kiểm lại cổng trên master mới. Tập sáu cổng và các tệp đo số nền không đổi. |
| 2. Địa chỉ và đơn vị băm độc lập | cùng lệnh | 7 `HASH_MATCH True VISIBLE True`; `CODE_LOCK_TABLE_MATCH True`; `SIX_ANCHORS [1,1,1,1,1,1]`; `PROTOCOL_EXACT True` | Ráp sáu thay đổi ra đúng từng byte, không dùng hàm parser sản phẩm để xác nhận chính nó. |
| 3. Byte, biên, che, địa chỉ, cardinality | `python3 -B out/sc/probes_r5.py out/prototype out/locks.json out/tmp/byte-probes` | `TONG 167 LECH 0 []`, trong đó 48 phép lượt 4 | F05.f/g đóng; che tại chỗ và bản sao không hiển thị đúng màu; giá thứ tự khối đã khai. |
| 4. Tệp hợp lệ, EOL, EOF, Unicode | `python3 -B out/format_extra.py` | `no_final_lf 0`; `extra_final_lf 0`; `unlocked_note_crlf 0`; `blank_lines_at_eof 0`; `NFKC_CANONICAL_I_VS_CYRILLIC False`; số ASCII/toàn khoảng `True` | Không tìm thấy chặn oan ở các dạng EOF này. CRLF toàn tệp/BOM đỏ trong bộ 167; giới hạn chữ cùng hình đúng như r5 khai. |
| 5. N8 trên mã thật và biến thể binding | `python3 -B out/sc/thu_pv5.py out ma 2`; tương tự `test 2` | `TONG ma: dung 42 sai 0`; `TONG test: dung 23 sai 0` | Tổng 65/65; nguyên mẫu sạch hợp lệ. Ngữ pháp đủ để viết bản nguyên mẫu. |
| 6. Canh phạm vi AST ngoài ma trận | `python3 -B out/n8_extra.py` | clean rc0; omit_epilog rc1; omit_epilog_delete_old_comment và omit_epilog_reflow_old_assignment rc0 | N8 không phải phép so byte toàn bộ các nút được cho sửa. Hai biến thể sau giữ AST/hành vi cũ; không dùng chúng làm bằng chứng binding lọt hoặc tái mở F08.c. Epilog đúng của nguyên mẫu đã đọc riêng. |
| 7. Sổ đăng ký và bảo toàn mục cũ | `python3 -B out/sc/so_dang_ky.py out/base out/prototype`; `python3 -B out/registry_negative.py` | sạch `SỔ ĐĂNG KÝ: ĐẠT`; ghi đè `r1187_drop_doc_guard` rc1 đúng khóa; đảo dãy ca rc1 `day_con_giu_thu_tu=false` | Có răng độc lập với tổng số lượng và N8. |
| 8. Ca và vòng mutant thật | `python3 -B out/sc/chay5.py out/prototype out/tmp/suite ca` (tương tự `adr`, `moi`, `cu`) | ca190/190; ADR40/40; nền60/60 và132/132, bỏ qua0; 26/26 và21/21 dòng ok, mỗi dòng có3 đối chứng sống; `TỔNG: ĐẠT` | Chỉ tập đã chọn, không gọi là full suite/full audit. |
| 9. Mốc, danh sách target, số đăng ký | `python3 -B out/counts_extra.py`; `python3 -B out/small_measure.py` | 26 `MARKER … 1`; `ALL_NEW_TARGETED True MISSING []`; 57 ca mới,25 mutant mã+1 mutant test | Không tái mở lớp mốc tự khớp/đối chứng khác họ. |
| 10. Tiền kiểm mẫu và ba trạng thái | `env PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 -B out/sc/fx_tien_kiem.py out out/base/ops/lease_publish.py` | `TONG 19 kịch bản: đúng 19 · sai 0`; bảy đối chứng raw matcher đều rc0/không người giữ | Policy/ref/kiểu dữ liệu lỗi dừng đúng trong tập mẫu; không chứng minh tập ref đủ tin cậy. |
| 11. Ref ngoài origin, cả trước và sau đăng | `python3 -B out/preflight_extra.py` | cả hai namespace: `PRIVATE_SHA_ON_SERVER False`; 3c rc0; `STEP_3D rc0`; `STEP_3E rc0`; bỏ ref riêng ⇒ rc1, chỉ đúng lease cũ | **LỖI F11**, cùng cơ chế ở hai đường vào. Hạn không đọc được ⇒ rc1/KHÔNG ĐO ĐƯỢC, đối chứng fail-closed thật. |
| 12. Lease snapshot và trôi thời gian | `python3 -B out/coordination.py`; `python3 -B out/historical_counts.py` | snapshot550/17/12/5 tại giờ03:24:55; tái dựng ref trước thay đổi ⇒549/16/11/5 | Phân biệt trôi dữ liệu với lời khai sai; không lấy tổng5 trùng làm bằng chứng mọi số hạng trùng. |
| 13. #1460, CI admission, registry file và Ruff contract | `python3 -B out/ci_contract.py`; `python3 -B out/small_measure.py` | base/prototype/master: `registry [[],30,30]`, `ruff_contract [[],3]`; bốn đường PR và push master đều `chay` | Thêm CASES/MUTANTS không đòi sửa sổ đăng ký tệp của #1460. Evidence workflow tương lai phải đo lại. |
| 14. Bare Ruff F | `python3 -B out/ruff_delta.py` | Ruff0.16.9; mỗi bên rc1/16 lỗi; `STABLE_DELTA_NEW []`, `STABLE_DELTA_REMOVED []` | Delta0; không khai bare lint rc0. |
| 15. Bảo toàn nguồn | `python3 -B out/final_check.py` | băm spec/HEAD/tree giữ nguyên; so manifest file và git diff trong `final-check.log` | Chỉ quan sát đầu/cuối; không coi prompt read-only là mount cưỡng chế. |

Log chính: [measure](measure.log), [byte-probes](byte-probes.log), [N8 ma](pv_ma.log), [N8 test](pv_test.log), [preflight19](preflight19-rerun.log), [phản chứng ref](preflight-extra.log), [sổ đăng ký](registry.log), [sổ âm](registry-negative.log), [mutant mới](moi.log), [mutant cũ](cu.log), [ca](ca.log), [ADR](adr.log), [counts](counts-extra.log), [số nhỏ](small-measure.log), [lease lịch sử](historical-counts.log), [tiền kiểm snapshot](preflight-snapshot.log), [Ruff](ruff.log), [CI contract](ci-contract.log), [kiểm cuối](final-check.log).

## BẢNG ĐO

Các phép ngày 21-11-2026 UTC. Con số lịch sử chỉ tái dựng được trong điều kiện nêu bên dưới, không phải quan sát máy chủ ở thời điểm quá khứ.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| Định danh spec | r5/05d12f1/5357004a… | OID và băm đầy đủ đầu verdict; local=blob | Có |
| Dài spec/ký tự lạ | 913/0 | 913 dòng;0 ký tự thuộc nhóm kiểm | Có |
| Tác giả/executor/reviewer | Opus5.5 thay Fable5.2 soạn; executor Fable5.2; Codex review | Đúng đầu tệp, bảng§1,D16; assurance vẫn cross_approved | Có về nội dung; E2 là sự kiện được giao |
| Verdict r4 | 400234b2…9175;3P2/5 nhóm;4 lớp nợ | Băm khớp; tự đối chiếu đủ10 nhóm | Có |
| Lịch sử lớp | 18 | 18 slug; không đổi tên/tách/gộp | Có |
| Audit nguồn/ma trận | 62 dòng/23 điểm | blob a8affd58 đọc rc0/62; riêng§15.2 có23 hàng | Có |
| Bộ hiện vật | băm patch838bbccb…;532 dòng | Khớp; SHA256SUMS của gói giao20/20 | Có cho gói giao; 23 tệp máy tác giả là tập khác |
| Các khối giữ từ r4 | khoa+8 khối protocol | 9/9 bằng byte r4 | Có |
| Ba khối mã | 109/21/64 dòng không trống | Đúng; byte trích từ spec bằng ba script giao | Có |
| Ref | 392 nhánh | 392, thêm1 symref HEAD ⇒393 ref origin | Có |
| Master | 5a152c1 | Đúng fullOID;24 commit/116 đường từ base | Có |
| Drift trên tập đo§3 | 0 tệp | 0 trong đúng tập§3; adapter work-packet có đổi ở ngoài tập này | Có; adapter đã kiểm lại bằng cổng |
| Opt-in0053/0055 | rc0/rc128/first-parent có | Cả hai đúng trên mirror không shallow | Có offline; chưa đo độ mới live |
| ADR nền/cạnh tranh số | 66, max0067;0/392 ref≥0068 | Đúng | Có |
| Lease03:24:55 | 549/16/11/5 | Snapshot mới550/17/12/5; tái dựng ref cũ549/16/11/5 | Khớp lịch sử tái dựng; snapshot đã trôi |
| Lease02:57:49 | 549/17/11/6 | Tái dựng549/17/11/6 | Có với cùng giới hạn |
| Người giữ4 đường | 0/0/1/1 | Đúng, hai.py do wp1462-r8-g2-claude giữ | Có |
| Tiền kiểm trên master | DỪNG chỉ vìB4;policy0/link0 | Bản sao dùng mirror làm origin: rc1 đúngB4;policy0/link0 | Có offline; không thay ls-remote GitHub |
| Biên nhận | 352;0 cóbang_lop | 352/0 | Có |
| Sáu vị trí cổng | vector§3/S5/ôINV | Đã đo riêng30 vector, khớp | Có; đếm nhắc tên không chứng minh cưỡng chế |
| ADR/protocol/mã/test |149;+46−2;+76−1;+163−1 | Đúng từng tệp | Có |
| Tổng/trần |4 tệp;+434−4;≤450 |434, còn16 dòng;diff-check rc0 hai base | Có cho nguyên mẫu |
| ADR template | bằng byte ngoài7 chỗ trống | Khớp;149 dòng; trạng thái Proposed | Có cho cây thử; chưa đạtN1 củaH |
| INV |28=15+12+1;15 ô cổng có nợ;18 trỏ ca | Đúng từng số | Có |
| Nợ |27;25 tên được trỏ |27/25;không tên thiếu | Có về dữ liệu |
| Nguồn§1 |10 mục nguyên văn |10/10 sau nối dòng từng mục | Có |
| Khóa/mốc |7 bộ bốn;6 neo;3 mốcN8 |7/7;6×1;3×1 | Có trên base được thử |
| CASES |1582→1639 | Đúng;1639 tên khác nhau | Có |
| Linux |1581→1638 | Đúng;chênh duy nhất wp1174_windows_claim_rejected | Có |
| MUTANTS |1864→1890 | Đúng;0 bộ ba cũ đổi;NHAM_TEST nền⊆H | Có |
| Tập mới |57 ca/26 mutant |57/26;25 mã+1 test;57/57 ca có target | Có |
| Nhóm ca chọn/ADR |190/190;40/40 | Đúng;0 thất bại/bỏ qua trong tập chọn | Có |
| Vòng mới |nền60/60;26/26 | Đúng;26 dòngok với3 đối chứng sống mỗi mutant | Có |
| Vòng cũ |nền132/132;21/21 | Đúng;21 dòngok với3 đối chứng sống mỗi mutant | Có |
| Số giếtG1–G9/K01–K07 | bảng§8.3 | Từng dòngok khớp;K01–K07=8,4,6,4,9,4,3; bỏ gọi=52;fixture=2 | Có |
| N8 |ma42/test23;65 đúng |42/42 và23/23 | Có |
| Byte |48 cũ+119 mới |167/167;riêng48 đầu đúng | Có |
| Tiền kiểm mẫu |19/19;7 khác raw matcher |19/19;7/7 raw matcher rc0 | Có; phản chứng ngoài tập còn lỗi |
| Ký tự lạ.py |mã0→0;test7→7 | Đúng cả số lượng và tập ký tự | Có |
| Caller |4 adapter/1 workflow/21CLI test cũ |4/1/21;họ cũ132 | Có |
| Cưỡng chếADR thử |0·11·0·0·0·0 | Đúng vector trên cây thử | Có |
| Cổng prototype/master mới |doctrine0;ADR67/67 rc0 | Đúng cả hai cây;quét12 adapter | Có |
| Cổng nguồn chưa áp |doctrine xanh/ADR66 | Tự chạy rc0/rc0;66/66 | Có |
| RuffF |16→16;delta0 |16→16;F8413,F4018,F8113,F5412;delta ổn định0 | Có;bare lint rc1 |
| RegistryCI/Ruff contract |không claim đếmCASES bằng registry tệp |30/30 tệp và3/3 hợp đồng ởbase/prototype/master | Bổ sung, không xung đột#1460 |
| Ruleset6check/Issueopen/bypassactors | REST tại giờ ghi trongspec | Không có readback server của lượt này | KHÔNG ĐO ĐƯỢC trực tiếp |

Sự trôi lease có nguồn cụ thể: ref `ops/bundled-tach-manh-spec` tiến qua `7762f2b` lúc03:29:21Z rồi `9f11ed7` lúc03:29:37Z, thêm g5 và bia mộ g4 sau giờ03:24:55Z của S4. Tôi tạo mirror riêng dưới `out/historical.git`, đưa **ref ấy** về `2d8c5041536195e0f9ba91f239d03887ec6909e1`, giữ các ref khác, rồi chạy lại phép quét ở hai giờ tác giả nêu: cả số hạng và danh sách active khớp. Đây là tái dựng có điều kiện từ lịch sử, không phải khẳng định đã chứng kiến snapshot server cũ. Không báo 549 là số sai chỉ vì snapshot mới có550.

Wrapper vòng mới trả tuple cuối có số25 vì mutant thứ26 nhắm tệp test và chạy qua đường riêng. Đếm log thật có đủ26 dòngok, gồm `t1466_fixture_ve_trung_tinh`; không lấy số25 của callback để kết luận mất mutant.

### tien-kiem-lease-chua-du [P2] Tiền kiểm tin bia mộ từ ref chưa được xác minh với máy chủ

TỆP/DÒNG: `cay-kho/ops/specs/wp1466.md:95` (T1), `:115` và `:117` (T4), `:68` (3e). Consumer nền: `ops/lease_publish.py:543` (`_cac_ref_cuc_bo`), `:713` (`_quet_lease_toan_kho`), `:806` (`_bia_mo_doi_xung`).

VẤN ĐỀ: T1 chứng minh cặp tên/SHA của `refs/remotes/origin/*` bằng máy chủ. Nhưng T4 không chỉ đọc tập ấy: `_cac_ref_cuc_bo` còn đọc `refs/heads/*` và mọi remote khác. `chan_nhanh_tut_sau=True` không loại nhánh local không upstream; nó cũng không xác minh remote phụ với origin. Bia mộ hai chiều được kết luận từ bất kỳ bản ghi nào trong tập đọc rộng này.

Trong fixture, máy chủ có lease A còn hạn, giữ `.claude/dev/packet_loop.py`, với một chiều trỏ sang B nhưng chưa có bản ghi B trên máy chủ. Chỉ đọc dữ liệu đã công bố thì A vẫn là người giữ và khối dừng. Một bản nháp B xác nhận chiều ngược, chỉ có ở ref chưa công bố của clone, làm T4 coi A đã bị thay thế. T1 vẫn khớp vì ref origin không đổi. 3c dùng cùng nguồn quét nên cũng trả không người giữ. Sau khi thêm lease của wp1466 vào **origin giả cục bộ**, 3e tiếp tục xanh dù snapshot máy chủ có cả A và lease mới giao nhau. Không cần đổi policy, đường dẫn, băm spec, mã cổng hay giả rc.

Đã quét cả hai đường vào cùng cơ chế: nhánh local không upstream và `refs/remotes/backup/...`. Hai nhánh đều cho cùng kết quả; gỡ riêng ref chưa công bố, giữ nguyên máy chủ và toàn bộ lease đã công bố, làm tiền kiểm quay về đỏ đúng A. Lỗi có thể khiến người cấp lease bắt đầu executor thứ hai khi người giữ thật vẫn còn quyền ghi. Đây là hậu quả có điều kiện từ phép kiểm đã tái hiện; tôi không thực sự cấp lease GitHub hoặc chạy hai executor.

GỢI Ý VÁ: dữ liệu gợi ý là dùng đúng tập ref/OID đã chứng minh thuộc snapshot máy chủ để quyết định hiệu lực lease, hoặc fail-closed với mọi ref ngoài tập ấy chưa được xác minh. Cùng quy tắc phải áp trước và sau đăng. Phép kiểm đóng lớp cần giữ được các đối chứng 19 ca hiện có và chặn cả hai nguồn bia mộ chưa công bố; không chỉ cấm tên nhánh fixture. Cần phân biệt snapshot đã xác minh với khả năng thay đổi của server sau phép đo. Không đề nghị bỏ điều kiện sau đăng hay đổi authority C5.

ĐÃ THỬ NGHIỆM: `python3 -B out/preflight_extra.py`, output thật ở [preflight-extra.log](preflight-extra.log):

```text
local_head PRIVATE_SHA_ON_SERVER False
local_head STEP_3C 0 NGƯỜI_GIỮ 0: không có
local_head_STEP_3D rc 0 ... TIỀN KIỂM: ĐẠT
local_head_STEP_3E rc 0 ... TIỀN KIỂM: ĐẠT
local_head_AFTER_REMOVING_PRIVATE_REF rc 1 ... ['fxa-r1-g1-claude']
other_remote PRIVATE_SHA_ON_SERVER False
other_remote STEP_3C 0 NGƯỜI_GIỮ 0: không có
other_remote_STEP_3D rc 0 ... TIỀN KIỂM: ĐẠT
other_remote_STEP_3E rc 0 ... TIỀN KIỂM: ĐẠT
other_remote_AFTER_REMOVING_PRIVATE_REF rc 1 ... ['fxa-r1-g1-claude']
```

Hai fixture đều bắt đầu bằng server-only rc1; việc bỏ ref riêng không đổi server. Probe hạn không đọc được trả rc1/KHÔNG ĐO ĐƯỢC, nên không quy mọi nhánh fail-closed đều hỏng. F11.b về policy vắng và phép so đường dẫn hẹp đã đóng; F11.c chưa đóng vì nền dữ liệu quyết định còn thiếu điều kiện. Do wp1466 vẫn hứa tiền kiểm ở§1, không đủ điều kiện chuyển biểu hiện này sang bảng(ii).

ĐỘ TIN: cao về mã, tập ref và kết quả trước/sau đăng; không có chứng cứ một va chạm executor thực tế đã xảy ra trên GitHub.

## L3, L6, authority và phối hợp

- **L3:** G1–G9 có ca và đột biến chạy thật; N8 có đối chứng xanh/đỏ và ngữ pháp nhận được nguyên mẫu; sổ đăng ký có hai phản chứng độc lập. 19 ca tiền kiểm chưa phủ nguồn bia mộ, vì vậy không dùng 19/19 để đóng F11. N13–N16 vẫn là evidence tương lai của H/merge, không được thay bằng kết quả local.
- **L6(a):** bảy khóa chuẩn là vế dương; xóa/dời/nhân bản/đổi byte là vế âm; riêng p4-cu/p5-cu được loại bằng phép ráp byte độc lập. **(b):** chọn đơn vị cố định có băm; ngắt dòng lại làm đổi byte và đỏ, là giá công bố của thiết kế. **(c):** mỗi địa chỉ/cardinality và mỗi vị trí cổng được đo riêng. **(d):** ID là grammar số cố định, không hứa hiểu số viết bằng chữ; không áp phép suy diễn ngôn ngữ tương đương. **(e):** đủ sáu vị trí protocol§20,30 vector; các ô có nợ giữ phân biệt “nhắc tên” và “cưỡng chế”.
- **CRLF/BOM/EOF:** CRLF toàn tệp và BOM đầu tệp đỏ trong bộ đã công bố; `.gitattributes` cho protocol `eol: lf`, r5§18 nêu rõ giá checkout bị editor đổi CRLF. BOM đổi dòng tiêu đề dùng làm địa chỉ nên không giữ cùng địa chỉ byte. Bỏ LF cuối tệp, thêm dòng rỗng cuối, và CRLF trong ghi chú ngoài khóa đều xanh. Không kết luận đã thử mọi dạng Markdown/encoding hợp lệ.
- **NFKC/Cf:** có phép gộp biểu diễn, nhưng không có hai ID canonical `INV-NN` khác nhau bị hợp nhất: chữ số ASCII giữ nguyên; thay byte trong bảng khóa bị hash bắt trước. Dạng toàn khoảng/vô hình ngoài K01 bị từ chối có chủ ý. Chữ Kirin cùng hình không bị NFKC gộp, đúng giới hạn đã khai; wp1466 không hứa chống mọi giả mạo thị giác. Không lấy giới hạn đó làm finding mới ngoài hợp đồng.
- **N8:** các đường binding của r4 đã bị ngữ pháp/compile chặn. Nguyên mẫu chạy được và đủ57 ca/26 mutant chứng minh ngữ pháp không làm bản H hiện tại bất khả thi. N8 vẫn không chứng minh tác dụng phụ động của hàm/lời gọi sổ; r5 đã khai và đặt phép bảo toàn sổ cùng hồi quy phía sau. Probe bổ sung về epilog/chú thích chỉ cho giới hạn của kiểm AST, không chứng minh thay đổi hành vi cũ; không nâng nó thành lỗi binding.
- **D5/D9/D12 và L7:** đây là lựa chọn triển khai để thực hiện hợp đồng đề xuất; không tìm thấy quyết định chủ kho nào bị chúng đảo riêng. Toàn packet đã khai E5, chưa freeze, và C1 vẫn đòi chủ kho duyệt toàn bộ spec_hash; E2 đổi người soạn không đổi executor hoặc assurance. Không cần thêm một điểm hỏi chỉ vì người soạn chọn thuật toán. D12 vẫn phải sửa lỗi kỹ thuật nêu trên trước khi freeze; câu tự khai “fail-closed” không miễn phép kiểm. ADR-0054 đóng băng, ADR-0060/0062 là luật merge.
- **Trần:** hai OID opt-in hợp lệ trong lịch sử mirror. Nguyên mẫu4/434 nằm trong6/450, chỉ còn16 dòng; không cấp ngoại lệ cho bản sửa tương lai. Phải đo lại trên base sauB4. Không suy lượt này reset lịch sử hay ngân sách; áp trần cho review đặc tả không gắn PR vẫn là giới hạn r5 tự khai.
- **C5/B4:** E5 chỉ cho #1466/#1469/#1470 merge master; không bao gồmB4. 3a–3f là tiền kiểm cấp lease, không thay nhánh nhận hoặc quyền merge; không tìm thấy việc r5 tự đổi C5 qua khối này. B4 đang giữ hai.py; yêu cầu first-parent/base và ba mốc phải kiểm lại khi B4 land. Lượt này chưa có diff cuối hoặc đường land hoàn tất củaB4 để chứng nhận điều kiện bắt đầu ấy đã đạt.
- **#1460:** đã đọc spec r7 từ ref `origin/ops/wp1460-r1` ở `163ece8087bf38f864e49d59206af937b2421f47`. B1a sửa `.claude/dev/ci_dang_ky_test.py`, workflow full-audit và hai hiện vật hợp đồng; không giao bốn tệp code của wp1466. `ci_dang_ky_test.kiem()` đăng ký **tệp bộ test**, không đóng băng số CASES/MUTANTS của packet_loop; đo30/30 giữ nguyên sau patch. `so-dang-ky` chỉ là script nghiệm thu ngoài PR, không thêm tệp thứ năm. Tuy vậy #1460 đổi workflow mà N14 tiêu thụ, nên H sau đó phải dùng đúng workflow/job/evidence thực, không dùng log workflow cũ. Lease đang giữ ci_dang_ky_test là wp1236-r10, không phải wp1460 trong snapshot.

## Những gì KHÔNG đo được và giới hạn

Không chạy Windows, full packet_loop1638 ca Linux, `scripts/tl.py --selftest`, full mutant audit toàn kho, CI GitHub, `kiem-merge`, waiver exact-H hoặc canary hậu-land N16. Không đo live ruleset/bypass actors/branch protection, Issue open hay độ mới ref với GitHub; local fake origin và mirror snapshot không thay các phép đo đó. Không readback các URL quyết định E2/E5/checkpoint; chúng là sự kiện được cung cấp. Không kiểm chứng toàn bộ15 dòng label/assignee/board bằng ngữ nghĩa; chỉ đếm lại đúng từng vị trí.

Không tự dựng payload thoát đường dẫn hay chuỗi độc hại. Ca symlink/path đã có được chạy từ fixture giao; hướng chuỗi symlink nhiều bước, đường có biểu diễn đặc biệt và cấu hình Git làm thay cách đọc object chưa được biến thành phản chứng mới trong lượt này. Không khai đã chứng minh tiền kiểm an toàn cho các hướng chưa đo đó. Thử nghiệm mới về ref dùng kho giả, dữ liệu lease/bia mộ và đường dẫn thông thường; mọi commit/ref/công bố fixture chỉ ở các kho riêng dưới `out/`, không đẩy ref nào tới kho tra-luat hay GitHub.

Lỗi setup đầu tiên của19 fixture và probe ref: Git kế thừa cấu hình ký commit, dịch vụ ký không truy cập được trong sandbox. Đây là lỗi môi trường, không phải tiền kiểm đã đỏ đúng. Đã chạy lại với `commit.gpgsign=false` chỉ trong môi trường tiến trình tạo **commit fixture**, có output19/19 và log phản chứng đầy đủ. `batches.json` giữ rc1 của lượt setup đầu, không xóa lịch sử ấy. Phép đếm ma trận ban đầu lấy cả ba hàng câu hỏi C1/C3/C4; đã giới hạn đúng§15.2, ra23. Tái dựng lịch sử lease ban đầu thêm một remote-ref mà chưa đưa head-ref nguồn về cùng commit; đã sửa cả tập nguồn của bản sao rồi đo lại. Không dùng các kết quả setup sai làm finding hoặc evidence đạt.

Gói giao có20 mục checksum kiểm được. Danh sách23 tệp trên máy tác giả và các băm log gốc trong§18 không có đủ hiện vật log gốc ở đây để chứng nhận tất cả; các số test được chạy lại thay vì tin băm log tác giả. Trạng thái ADR nguyên mẫu vẫn `Proposed (cây thử, chưa duyệt)`, nên chưa đạt N1 của H và không tạo authority.

Mọi hiện vật của lượt nằm dưới `out/`. Cây nguồn không có delta nội dung/mtime quan sát được giữa hai manifest; HEAD/tree/spec hash và git diff đầu/cuối khớp, xem `final-check.log`. Snapshot quan sát đầu/cuối không chứng minh toàn bộ lịch sử giữa hai mốc. Sandbox thực là workspace-write có chỉ thị chỉ ghi `out/`, không phải mount nguồn cưỡng chế read-only. Không sửa kho, không push tới remote thật, không gọi API GitHub ghi.
