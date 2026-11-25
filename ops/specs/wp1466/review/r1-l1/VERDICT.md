verdict: changes_requested
reviewed_sha: 925f851ed526537f5b55fa2b6815017a31a028a2
spec_sha256: 0ea82600b66455960c9dd3ca872c5251d00d2ec9dd85a30d4ff5baaca9637bfa
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, session_id: KHONG_DO_DUOC}
review_axes: [Spec, Standards/Security]
assurance: cross_approved (đề nghị; executor họ claude)
dem: {so_lop: 12, so_bieu_hien: 30, P0: 0, P1: 4, P2: 7, P3: 1}

Review đặc tả r1, không phải review mã triển khai. Chưa đủ điều kiện duyệt băm: có 12 finding còn mở. Số P đếm finding; mỗi finding dưới đây là một lớp. Số biểu hiện đếm theo các nhóm được chỉ rõ trong BẢNG LỚP, không đếm lại mỗi lần cùng lời khai xuất hiện.

Băm local khớp blob của commit được giao. HEAD `925f851ed526537f5b55fa2b6815017a31a028a2`, tree `62d44003f1c4155300ce2a6007eedaf25920f010`; base `48d372e14f190dae83a75ccbca8ee9a0b25635c5`, tree `dff76e42cd1aa8dbf524c1f145274e50d2c8eef6`. Mirror không shallow, `core.abbrev=7`, 382 remote ref trong snapshot. Các phép đo dưới đây chạy ngày 20-11-2026, khoảng 18:35–18:44 UTC, trên snapshot được cấp, không phải trạng thái GitHub trực tiếp.

Kết quả nổi bật: dựng đúng sáu khối protocol được **+39/−2**; 44 tên ca và 33 tên đột biến khớp; bộ ca nền chọn lọc **71/71 đạt**. Tuy nhiên, quy tắc khớp trọn đoạn chỉ nhận **2/8 neo** của chính bản dự kiến. Một số ô INV gán nhầm tính chất cho cổng/ca, và bảng chưa bao phủ các bất biến đã được protocol gọi đích danh.

Việc tách luật/bảng/cổng verdict có thể tạo phần hữu ích độc lập; tự nó không vi phạm trần. Hai OID opt-in hợp lệ. Tổng dự kiến wp1466 là 382 dòng thêm, được làm tròn thành khoảng 380; chưa có diff triển khai để kết luận vượt trần hay đòi `nang_tran`. Không lấy 555 dòng của **nhánh đặc tả** làm kích thước PR giao nộp. KN-1 chưa phải packet được cấp việc; khi soạn phải khóa dependency/base sau wp1466, không mở hai PR chồng write set. Nếu tổ chức thành Mission thì đường integration của ADR-0044/§5 vẫn áp dụng. Thứ tự B4 land trước theo chỉ thị chủ kho được giữ.

## ĐỐI CHIẾU LƯỢT TRƯỚC

không áp dụng — lượt 1

## BẢNG LỚP

| slug lớp | finding IDs/biểu hiện | hạng còn mở | nguồn lượt/SHA | phương án chung hoặc lý do vá riêng | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| neo-sai-don-vi-khop | F01; 6 neo: 2, 3, 4, 5, 7, 8 | P1 | r1 / 925f851ed526537f5b55fa2b6815017a31a028a2 | Định nghĩa đúng đơn vị cấu trúc rồi so trọn | Dựng sáu khối thật; 2/8 bằng trọn đoạn |
| neo-thieu-nghia-vu | F02; 4 nghĩa vụ bị bỏ mà giữ cả tám neo | P1 | r1 / cùng SHA | Ma trận nghĩa vụ → neo → ca → mutant | Bốn phép bỏ văn bản trong bộ nhớ |
| cong-khong-do-bat-bien | F03; INV-04, 05, 06, 13, 15, 16: 6 biểu hiện | P1 | r1 / cùng SHA | Gắn đúng phép kiểm; phần chưa đo ghi giới hạn/nợ | Đọc mã/ca thật; 71 ca chọn lọc đạt không chứng minh độ phủ |
| thieu-truy-vet-yeu-cau | F04; 2 nhóm: thiếu INV quan trọng, audit chưa có nợ | P1 | r1 / cùng SHA | Lập ma trận phủ nguồn và 23 điểm audit | So §1/§8/§12 và audit 62 dòng |
| kiem-chuoi-khong-doc-cau-truc | F05; G1, G7, G8: 3 biểu hiện | P2 | r1 / cùng SHA | Đọc cấu trúc khai báo trong vùng hợp lệ | Phân tích mã/hợp đồng; không dựng chuỗi tấn công |
| duong-dan-chua-khep-trong-goc | F06; G7: 1 biểu hiện | P2 | r1 / cùng SHA | Kiểm đích resolve và root, không chỉ hai dạng cấm | Chỉ mô tả phản chứng đường dẫn theo chỉ thị |
| moc-chuyen-tiep-mau-thuan | F07; 1 hợp đồng cutover có hai vị từ | P2 | r1 / cùng SHA | Một luật hiệu lực, một bảng chân trị | Có hai ô chéo bất đồng; chưa có cổng KN-1 |
| tieu-chi-dong-xoa-khong-do-hanh-vi | F08; N8: 1 biểu hiện | P2 | r1 / cùng SHA | So phạm vi sửa thay cho suy từ dòng xóa | Thêm `pass` vô hại vào hàm cũ vẫn chỉ −1 |
| dem-khong-khai-tap-ca | F09; hai chỗ khai 1581: S10 và §18 | P3 | r1 / cùng SHA | Tách tổng đăng ký khỏi tập áp dụng trên Linux | 1582 đăng ký; 1581 áp dụng Linux |
| schema-bo-sot-provider-hop-le | F10; hợp đồng kế thừa v1: 1 biểu hiện | P2 | r1 / cùng SHA | V2 định nghĩa đầy đủ provider và identity hợp lệ | V1 chỉ nhận claude/codex/human; v2 chưa giao |
| tien-kiem-lease-chua-du | F11; 2 biểu hiện: độ mới ref, giao prefix | P2 | r1 / cùng SHA | So SHA+tên và giao effective write set chuẩn hóa | Snapshot hiện không có người giữ bốn tệp |
| doi-diem-goi-cong-chua-du-yeu-cau | F12; doctrine-scan: 1 biểu hiện | P2 | r1 / cùng SHA | Giữ entrypoint được yêu cầu hoặc khai quyết định đổi | Xóa §8.3 ở scratch, doctrine-scan vẫn rc 0 |

## BẢNG SĂN

Các script, log và bản dựng được lưu cùng verdict trong `out/`. Chúng chỉ đọc checkout; các bản sửa/thư mục test nằm trong `out/`. `rc=1` của `git diff --no-index` dưới đây nghĩa là **có khác biệt**, không phải phép đo hỏng.

HƯỚNG 1: tính toàn vẹn, base và opt-in trần

- giả thuyết: blob hoặc OID opt-in không đúng đối tượng/không phải commit land.
- lệnh: `sha256sum cay-kho/ops/specs/wp1466.md`; `git -C cay-kho rev-parse HEAD origin/master`; `python -B out/measure.py` (hai bộ `cat-file -e L:path`, `cat-file -e L^1:path`, kiểm L trong `rev-list --first-parent origin/master`).
- output: băm đúng đầu verdict; HEAD/base đúng; `SHALLOW false ABBREV 7`; `OID 55 0 128 0`; `OID 53 0 128 0`.
- kết luận: **KHÔNG PHẢI LỖI**. Trần áp dụng cho PR sản phẩm là 6 tệp/450 dòng thêm; trục lời gọi chọn ADR-0055. Không suy thêm quyền cho review đặc tả không gắn PR.

HƯỚNG 2: đo lại số nền và sáu vị trí cổng

- giả thuyết: số dòng, receipt, JSON, lease hoặc diff tham chiếu đã bị làm tròn/sai phạm vi.
- lệnh: `python -B out/measure.py`; `python -B out/leases.py`; `python -B out/more_measure.py`.
- output: `LINES ... 2732, 7284, 6220, 1688, 1221, 277`; `RECEIPTS 352 bang_lop_text 0`; `JSON 4561 PARSE 4559 VALID_V1 []`; `RECORDS 536 LEASED_AT 504 LIVE 8 TOMBSTONED 3`; `REGISTRY 1582 1864`; `CA_COUNT_LINUX 1581`.
- kết luận: **LỖI** về đơn vị sổ ca (F09); các số nền còn lại tái lập được như bảng đo. Số 380 ref là ảnh cũ có thời điểm, không gọi việc snapshot nay có 382 là chứng cứ số đo lúc 17:47 sai.

HƯỚNG 3: khả năng nghiệm thu chính các khối protocol

- giả thuyết: sáu khối tự mâu thuẫn với matcher và N5.
- lệnh: `python -B out/protocol_probe.py`.
- output: `P1..P5_ANCHOR_COUNTS [1, 1, 1, 1, 1]`, `P6_ANCHOR_COUNT 1`; `PROTO_NUMSTAT 39 2`; neo 1/6: `FULL 1`; neo 2/3/4/5/7/8: `FULL 0` dù `CONTAINS 1` cho từng neo.
- kết luận: **LỖI**, F01. Không viết cổng sản phẩm thay executor; chỉ áp công thức matcher được đặc tả quy định.

HƯỚNG 4: độ phủ nghĩa vụ, độc lập với lỗi matcher

- giả thuyết: có thể mất luật cốt lõi mà giữ đủ tám neo.
- lệnh: `python -B out/protocol_probe.py`.
- output: bốn dòng `SEMANTIC_REMOVAL delete_search_class/delete_convergence/delete_repeat_history/delete_checkpoint_journal SOURCE_COUNT 1 ALL_EIGHT_SUBSTRING_PRESENT True ERR []`.
- kết luận: **LỖI**, F02. Đây là đối chiếu sự bảo toàn chuỗi sau khi bỏ từng đoạn thường; không khai cổng `bat-bien` chưa tồn tại đã chạy xanh.

HƯỚNG 5: cổng thật có đo tính chất trong ô INV không

- giả thuyết: tên ca tồn tại nhưng phép kiểm khác bất biến được quảng bá.
- lệnh: `python -B out/contract_probe.py`; `python -B -u out/run_selected.py`; đọc `packet_loop.py:792,3551,3662`, `ci.yml:268`, `eol_policy_test.py:525`.
- output: 18/18 tham chiếu ca có mặt; `RESULT 71 PASS 71 FAIL_OR_SKIP {}`; K0 chỉ kiểm ancestry và PR head; `cmd_init` không đọc session ID; `cmd_record_codex_call` không đọc bộ đếm attempt/vòng; `eol-policy selftest` chạy fixture, bước kiểm index thật là `eol-policy survey`.
- kết luận: **LỖI**, F03. Ca xanh chứng minh hành vi hẹp hiện có, không mở rộng nghĩa của nó.

HƯỚNG 6: vùng không render, khai báo ca và vị trí nợ

- giả thuyết: matcher nhận phần chỉ nhắc tên thay vì khai báo thật.
- lệnh: `python -B out/contract_probe.py`; `sed -n '1874,1915p' cay-kho/.claude/dev/packet_loop.py`; đọc G1/G7/G8 tại dòng 383/389/390 đặc tả.
- output: `MASK_BRANCHES {'fence': True, 'html_comment': True, 'html_block_parser': False}`; G7 nhận dòng `def` hoặc mẫu đăng ký bằng chuỗi; `G8_SCOPE` chỉ đòi tên nợ ở bất cứ đâu trong ADR.
- kết luận: **LỖI THIẾT KẾ**, F05/F06. Không dựng payload HTML, chuỗi độc hại, đường dẫn thoát gốc hoặc symlink tấn công; các phản chứng đó chỉ mô tả bằng lời.

HƯỚNG 7: bảo toàn entrypoint doctrine-scan

- giả thuyết: lệnh chủ kho yêu cầu vẫn báo sạch khi nghĩa vụ §8.3 biến mất.
- lệnh: `python -B out/contract_probe.py` (bỏ §8.3 trong bản dựng `out/proposed-tree`, chạy entrypoint thật, rồi hoàn nguyên scratch).
- output: `DOCTRINE_WITHOUT_8_3 0 doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine`.
- kết luận: **LỖI**, F12. Điều này độc lập với việc sau này `bat-bien` có thể đỏ.

HƯỚNG 8: phối hợp và đường CI tiêu thụ cổng

- giả thuyết: write set giao #1460 hoặc cổng mới không được chạy khi chính bốn tệp của packet đổi.
- lệnh: `python -B out/leases.py`; `python -B out/more_measure.py`; `python -B out/contract_probe.py`.
- output: `HOLDERS` cả bốn đường wp1466 đều `[]`; `.claude/dev/ci_dang_ky_test.py` do `wp1236-a-r9-g1-claude-20261120` giữ; #1460 r5 dự kiến sửa tệp này, nhưng wp1466 không sửa nó; #1462 r5 giao đúng hai tệp `packet_loop.py`/`packet_loop_test.py`. Selector trả `chay` cho cả bốn đường wp1466, `bo_qua` cho bốn tệp ca ngoại vi S14 nêu.
- kết luận: **KHÔNG PHẢI LỖI** về giao write set hiện tại; nợ tập phụ thuộc có thật và đã khai. **LỖI** ở hợp đồng tiền kiểm tổng quát F11; không kết luận từ mirror rằng hiện đã đủ điều kiện cấp lease.

HƯỚNG 9: chuyển tiếp và schema cho mọi loại review

- giả thuyết: hợp đồng KN-1 khác ADR nguyên văn hoặc loại bỏ reviewer hợp lệ.
- lệnh: `python -B out/contract_probe.py`; đọc v1 schema và §8.1 ADR dự kiến/§14.5.
- output: `CUTOVER True False False True False`; `CUTOVER False True True True False` (các cột có header trong log); `SCHEMA_V1_PROVIDER ['claude', 'codex', 'human']`.
- kết luận: **LỖI THIẾT KẾ**, F07/F10. Chưa có schema v2 hay bộ kiểm để chạy end-to-end.

HƯỚNG 10: độ nhạy của tiêu chí “không sửa mã cũ”

- giả thuyết: đếm dòng xóa không chứng minh phạm vi sửa.
- lệnh: `python -B out/contract_probe.py`.
- output: `EPILOG_MATCH 1`; `EXISTING_FUNCTION_CHANGED_NUMSTAT 1 2 1 ...`: đổi epilog và thêm một dòng `pass` vô hại trong hàm cũ vẫn chỉ xóa một dòng.
- kết luận: **LỖI**, F08. Đây là phản chứng phạm vi, không phải bản vá sản phẩm và không phải payload gây hại.

## BẢNG ĐO

Nguồn chi tiết: [measure.log](measure.log), [leases.log](leases.log), [protocol-probe.log](protocol-probe.log), [more-measure.log](more-measure.log), [selected.log](selected.log), [contract-probe.log](contract-probe.log). Các script tương ứng cho phép đo lại; không cần dữ liệu trên GitHub để tái lập phần offline.

| khẳng định | đặc tả khai | đo được | khớp? |
|---|---|---|---|
| Băm đặc tả, HEAD, base | các giá trị ở đầu tệp | đúng như đầu verdict | có |
| S1 số nhánh | 380 lúc 17:47 | snapshot được cấp: 382 | khác thời điểm; không chứng minh sai lịch sử |
| S1 ba ref cũ rồi lệch 0; B4 đổi head 18:28 | 3 → 0 | chỉ có snapshot cuối, không có hai bản ls-remote lịch sử | KHÔNG ĐO ĐƯỢC |
| OID ADR-0055 | rc 0/128/0 | rc 0/128/0 | có |
| OID ADR-0053 | rc 0/128/0 | rc 0/128/0 | có |
| Sáu tệp cổng, số dòng | 2732/7284/6220/1688/1221/277 | cùng sáu số, cả đếm LF và splitlines | có |
| S3 ADR | 66, max 0067 | 66, max 0067 | có |
| Ref có ADR ≥0068 | 0/380 | 0/382 ở snapshot | có về không tranh số tại snapshot |
| `ADR-0068` trên master | 1 dòng mô tả mutant | 1, `ops/land/pr1317-.../ma-luot1-VERDICT.md:35` | có |
| S4 người giữ bốn tệp | 0 | 0 lease còn hạn chưa bị thay thế giao bốn tệp | có trong snapshot |
| S4 wp1448 | giữ ba tệp nêu, hạn 23-11 08:00Z | cùng tên lease, cùng ba tệp và hạn | có |
| S5 lease | 536; 8 còn hạn; 3 có bia mộ; 504 có leased_at | 536/8/3/504; thiếu trường 32 | có |
| S6 `bang_lop`, `class_slug`, `doi_chieu_luot`, `KET_LUAN` | 0·7·0·0·0·0; 0×6; 0×6; 0·2·0·0·0·0 | đúng từng vị trí | có |
| S7 `review_verdict` trên sáu cổng | 0×6 | 0×6 | có |
| S7 `SCHEMA_REVIEW` trong launcher_test | 9 dòng | 9 | có |
| S7 JSON tracked/parse được/hợp v1 | 4561/4559/0 | 4561/4559/0 | có |
| B7 số trường required của v1 | 16 | 16 | có; không chứng minh hỗ trợ đủ provider |
| S8 receipt và khóa bang_lop | 352/0 | 352/0, kiểm cả text lẫn khóa YAML gốc | có |
| S8 `ops/bien_nhan_v2.py` nhắc bang_lop | 0 | 0 | có |
| S9 §20 | 66; A=50, B=16 | 66/50/16 | có |
| A: có nhắc/chưa đo/0 cổng/cụ thể/không cổng/rỗng | 17/6/12/12/3/0 | 17/6/12/12/3/0 | có |
| S10 adr-song nền | 66/66, rc 0 | 66/66, rc 0 | có |
| S10 doctrine-scan nền | 12 tệp, rc 0 | 12, rc 0 | có |
| S10 bat-bien nền | rc 2, chưa tồn tại | rc 2, chưa tồn tại | có |
| S10 sổ ca | 1581 | 1582 đăng ký duy nhất; 1581 áp dụng Linux | thiếu đơn vị chính xác, F09 |
| S10 MUTANTS/adr_song/adr_/doctrine_scan | 1864/40/19/17 | 1864/40/19/17 | có |
| S11 fixture ADR | có .git mặc định; chỉ §19, §20 | `_repo_adr_gia(co_git=True)` và phần dựng tương ứng | có |
| S12 PR #836 | 3 tệp +1275 | 3, +1275/−40, merge f1979a5ddd5b04562e054cc87beb5f28c7a7e934 | có |
| S12 PR #1116 | 5 tệp +452 | 5, +452/−7, merge aeecf9f675bb1b6c9db5db35c49a803d118c9efb | có |
| S12 PR #1127 | 5 tệp +318 | 5, +318/−18, merge f2102fc388a884d994f7bfeb29ef6863b9972b66 | có |
| S12 PR #1317 | 3 tệp +367 | 3, +367/−15, merge 426d1b06e292a7db272a0f942bef0794479b58a6 | có |
| S13 ADR nguyên văn | 138 dòng | 138 | có |
| S13 protocol | +39/−2; sáu mỏ neo mỗi cái 1 lần | +39/−2; 1/1/1/1/1/1 | có |
| S13 schema prototype, validator, ca prototype | 73 dòng; jsonschema 4.26.0; 26 ca; bat-bien 72 dòng không trống, 37/37 | nguyên mẫu/log không có trong hiện vật được giao | KHÔNG ĐO ĐƯỢC |
| S13 cây dự kiến adr-song/doctrine-scan | 67/67 rc 0; rc 0 | 67/67 rc 0; 12 tệp rc 0 | có; ADR scratch mang trạng thái Proposed, không giả approval |
| S13 ba dạng ô cổng | 15/5/1 trên 21 ô | 15/5/1 | có về hình, không về nghĩa |
| S14 workflow nhắc kiem-merge/adr-song | 0/0 | 0/0 | có |
| S14 tập phụ thuộc | bốn đường sản phẩm có; bốn tệp ca ngoại vi không | selector thật: 4 chay / 4 bo_qua | có; nợ đã khai |
| S14 ruleset 20856202 | 6 required check | mã có 5 CHECK_BAT_BUOC; không có readback ruleset trong mirror | KHÔNG ĐO ĐƯỢC ruleset; không đồng nhất hai tập |
| S15 1172 | 8 dòng; tiêu đề Mission ghim | 8, hàm `_1174_installed_mission` ghim Mission #1172 | có |
| §3 số tham chiếu ca | 18 trên 15 dòng cổng | 18/15; cả 18 có mặt | có; xem F03/F05 |
| G1–G12 | 12 chốt | 12 | có |
| Ca mới | 44 = 36 đỏ/KĐĐ + 4 xanh + 4 G12 | 44 = 27 đỏ + 9 KĐĐ + 4 xanh + 4 G12 | có, khử trùng kho_that_xanh |
| Đột biến mới | 33 = 32 sản phẩm + 1 test | 33 tên; 32 inv_* và 1 t1466_* | có về danh sách; chưa có implementation |
| Neo G9 | 8 | 8 chuỗi; chỉ 2 khớp TRỌN đoạn | không, F01 |
| Ước toàn bộ | khoảng 700, 5 hoặc 7 tệp | 138+39+73+175+275 = 700; 5/7 theo thành phần khai | phép cộng đúng; phần ước chưa có diff |
| Ước wp1466 | khoảng 380, 4 tệp | 138+39+80+125 = 382, 4 | hợp lý về làm tròn; 80/125 chưa đo được |
| Phương án cổng trước | khoảng 470 | 138+13+73+95+150 = 469 | hợp lý về làm tròn |
| Ước KN-1 | khoảng 330, 6 tệp | 73+95+150+15 = 333; 6 đường nêu | hợp lý về làm tròn |
| Windows theo đường | .claude/dev/** required | phân loại cô lập hai .py = required; hai .md = not_required | có; không phải đã chạy Windows |
| Audit nguồn | 62 dòng, 23 điểm, 3 chặn | 62; A1–A3, B1–B15, C1–C5 | có |
| Trạng thái Issue #1466/#1462, giờ tạo, 0 comment, PR đóng | số liệu REST theo thời điểm trong spec | mirror không chứa các response ấy | KHÔNG ĐO ĐƯỢC |
| Hậu land N15, CI PR H, full mutant H | chưa đo/đòi tương lai | chưa có H triển khai hay lượt CI tương ứng | KHÔNG ĐO ĐƯỢC |

Đo từng mẫu ở bảng INV, theo đúng thứ tự sáu cổng S3 của đặc tả:

| INV / mẫu | đặc tả | đo lại |
|---|---|---|
| 01/02: ai-dang-giu / ai_dang_giu / RC_DANG_GIU | 11·5·0·0·0·0 | 11·5·0·0·0·0 |
| 03: nguyên từ LIVE | 0×6 | 0×6 |
| 04: refs/pull/ | 0·1·1·0·0·0 | 0·1·1·0·0·0 |
| 05: eol/EOL/gitattributes | 0·0·0·0·24·0 | 0·0·0·0·24·0 |
| 06: RC_PROVIDER | 0·9·0·0·0·0 | 0·9·0·0·0·0 |
| 07: reviewed_sha/reviewing_head_sha | 4·49·0·0·0·0 | 4·49·0·0·0·0 |
| 08: spec_hash/spec_sha256 | 0·28·0·0·0·0 | 0·28·0·0·0·0 |
| 09: changed_paths; quan hệ diff/changed với write_set | 0×6; 0×6 | 0×6; 0×6 |
| 10: tested_sha | 0×6 | 0×6 |
| 11: model_family/ho_model | 15·33·0·0·0·0 | 15·33·0·0·0·0 |
| 12: bang_lop; class_slug | 0·7·0·0·0·0; 0×6 | cùng hai kết quả |
| 13: effective_review_class/_kiem_lop_review/RC_LOP | 15·0·0·0·0·0 | 15·0·0·0·0·0 |
| 14: chup-workspace/chup_workspace/ghi_workspace | 0·0·21·0·0·0 | 0·0·21·0·0·0 |
| 15: MOC_10_2_2/moc_10_2_2 | 0·3·0·0·0·0 | 0·3·0·0·0·0 |
| 16: codex_review_calls/RC_TRAN | 0·34·0·0·0·0 | 0·34·0·0·0·0 |
| 17: ADR-0067/uy_quyen_quyet_dinh | 0×6 | 0×6 |
| 18: Drive MCP/Sheets MCP | 0×6 | 0×6 |
| 19: NGUOI_CO_THAM_QUYEN/RC_TU_CAP | 13·15·0·0·0·1 | 13·15·0·0·0·1 |
| 20: doctrine | 1·27·5·0·5·1 | 1·27·5·0·5·1 |
| 21: mien_p3 | 0·3·0·0·0·0 | 0·3·0·0·0·0 |

Các mẫu `numstat`, `tran_loi_goi_codex`, `tran_kich_thuoc_sensitive` đều 0×6; `ghi hộ|ghi_ho` = 0·1·0·1·0·0, đúng lời khai. Đây chỉ là phép định vị; kết luận ngữ nghĩa nằm dưới đây.

## ĐỐI CHIẾU TỪNG INV

| INV | nguồn | cổng/ca thực sự kiểm gì | kết luận |
|---|---|---|---|
| 01 | §1(1), §4 đúng | r812_nguoi_giu_khac kiểm người giữ khác ở đường record-lease; không cưỡng chế mọi đường đăng | giới hạn này đã khai trong ADR |
| 02 | §1(2), §5 đúng | r812_nguoi_giu_prefix_giao_nhau kiểm giao prefix ở record-lease | đúng phần được đo; giới hạn đường đăng đã khai |
| 03 | §1(3), §11 đúng | không có phản chứng boundary/ruleset trong kho được trỏ | `chưa đo` và KN-6 công khai; không coi là có cổng |
| 04 | §1(5), §13 đúng | K0 kiểm ancestry/base và PR head, không đọc authorization, không kiểm deploy | F03 |
| 05 | §1(6), §9 đúng nhưng nên giữ ngoại lệ binary/golden | selftest kiểm fixture staged; survey --all mới kiểm index ứng viên | F03 |
| 06 | §1(8), §2 đúng | init so nhãn provider/họ model; ca trùng claude, không đo phiên giữ hai vai | F03 |
| 07 | §1(9) đúng | hai ca trỏ đo head review/state và run.json; bằng chứng CI/ủy quyền có các consumer khác | chứng cứ được trỏ chỉ cho phần review; không suy từ hai ca thành đã audit toàn bộ CI/authorization |
| 08 | §3.2 đúng | K1 so spec hash và metadata nguồn; ca cong_c_k1_hash chỉ đổi hash | có chốt hash; ca này riêng lẻ không chứng minh toàn bộ luật revision |
| 09 | §5 đúng | sáu cổng không có phép so diff với effective write set được nêu | nợ INV-09 đã đặt tên, KN-2 |
| 10 | §7 đúng | không consumer handoff/tested_sha trong sáu cổng | nợ INV-10, KN-3 |
| 11 | §8 đúng | c49 từ chối cross_approved cùng họ model tại consumer biên nhận | đúng phần họ model; giới hạn K4 đã khai; không thay audit assurance sensitive |
| 12 | §7/§8/§8.3 đúng | mặc định chưa cưỡng chế bảng lớp; bảy lần nhắc không phải K4 | nợ INV-12 có tên; các vấn đề neo F01/F02 |
| 13 | §8 đúng | `_kiem_lop_review` chỉ siết schema_version ≥2; dưới 2 return sau cảnh báo | thiếu giới hạn này trong ADR, F03 |
| 14 | §8/§8.2 đúng | ca launcher bắt delta `.git/x` khi bật --chup-workspace | giới hạn cờ tùy chọn đã khai; snapshot không chứng minh lịch sử chưa từng ghi-rồi-hoàn-nguyên |
| 15 | §10.2.2 đúng | D2 kiểm bốn nhãn thuộc DAT_MOC; không thu/xác minh bốn nguồn provenance | F03 |
| 16 | §12 đúng | record-codex-call kiểm trục lời gọi; pl_m3_codex kiểm Codex và tương tác trần vòng | không bao phủ attempt và không-reset xuyên phiên như cả câu INV, F03 |
| 17 | §12, ADR-0067 đúng | không cổng đọc mã E/sổ | nợ INV-17, KN-4 |
| 18 | CLAUDE.md là nguồn ngoài protocol, đã khai đúng | chưa có gate runtime được trỏ | nợ INV-18, KN-5; C4 nêu rõ lựa chọn này |
| 19 | §1(4), §4 đúng trong giới hạn người cấp | các ca chặn tên provider/tên giả trong granted_by | đúng kiểm allowlist; không chứng minh danh tính người quyết, giới hạn ADR-0067 còn áp |
| 20 | §13 đúng | doctrine-scan chặn sao chép nguyên văn/ngram; ca chép §5.1 | có phép đo chép, không phải chứng minh không lệch nghĩa; F12 về neo mới |
| 21 | §8 đúng | K3/K5 và hai ca trỏ chặn connector P1/P3 không miễn | đúng hai đường; offline chưa đọc findings/bảng lớp là nợ INV-12 đã khai |

## NGHIỆM THU, L2/L3/L6 VÀ GIỚI HẠN PHẠM VI

M1–M4 chiếu lần lượt vào đúng bốn đường dẫn, không có mục tiêu cần tự ý sửa `ci_dang_ky_test.py`. N1/N2 có vế dương trên nội dung mới, vế âm trên nội dung cũ và neo blob băm; đòi đúng byte ở đây có nghĩa, không phải lỗi vì Markdown có thể ngắt dòng. Số khối và vị trí chèn đo riêng từng nơi. N3/N4 xanh sẵn trên nền là đúng; N5 đỏ vì lệnh chưa có là đúng. N6/N7 hiện kiểm được danh sách, chưa kiểm được triển khai ca/mutant. N8 có phản chứng F08. N9 Ruff chưa chạy trong review này. N10 selftest đầy đủ chưa chạy, không nhận lại lời “đạt theo CI master” làm bằng chứng mới. N11 chưa có diff sản phẩm. N12–N14 cần H triển khai và readback CI/authority thật. N15 đã khai ai đo và lúc đo sau land; chưa đạt trước khi có lượt ấy.

Đối với L6: phần đo sáu vị trí và mỗi ô được làm riêng, không dùng tổng để che tệp trống. Hợp đồng G9 vi phạm cách khớp toàn bộ phát biểu và đơn vị đoạn (F01/F02); G1/G7/G8 thiếu phạm vi cấu trúc (F05). Các ID/khoá/schema có hình thức cố định không cần biến thể số viết chữ; các câu nghĩa vụ văn xuôi cần được khóa bằng nội dung đầy đủ. N8 không thể dùng numstat làm chứng cứ không sửa hàm.

Về ADR-0067/L7: C1/C4 và audit/merge đều khai E5; Windows và trần khai E2; không có ngân sách mềm tự đặt. Không phát hiện điểm hỏi mới không có mã trong §17. Riêng việc đổi entrypoint chủ kho yêu cầu chưa được trình như một thay đổi yêu cầu có căn cứ E3 (F12). Không coi duyệt một băm trong tương lai là bằng chứng đã chấp nhận thay đổi ấy.

## FINDINGS

### neo-sai-don-vi-khop [P1] F01 — Cây protocol đúng đặc tả không thể qua quy tắc khớp trọn đoạn

TỆP/DÒNG: `ops/specs/wp1466.md:360–369,391,418`.

VẤN ĐỀ: G9 đòi đủ tám neo, so TRỌN trên từng đoạn tách ở dòng trống. Bản dựng P1–P6 chỉ có neo 1 và 6 là trọn đoạn. Neo 2 là tiêu đề đậm mở đầu đoạn dài 510 ký tự; neo 3 nằm trong đoạn 544 ký tự; neo 4 và 5 nằm trong cùng đoạn danh sách 1.633 ký tự; neo 7 là một ô trong đoạn bảng; neo 8 bỏ dấu chấm phẩy và các câu sau của đoạn. Sáu biểu hiện cùng lớp này làm N5 đỏ trên chính đầu ra N2 bắt buộc. Nếu “khớp trọn” lại được hiểu thành tìm chuỗi con đủ dài thì điều kiện chống hậu tố sai không còn rõ nghĩa.

GỢI Ý VÁ: **Ở đâu:** mục 8.3 và bảng neo, vì đó là hợp đồng matcher. **Cách:** chỉ rõ đơn vị cho từng loại (heading, item, ô, phát biểu đầy đủ), dùng cùng chuẩn hóa cho nguồn và hằng. **Ca khóa:** vế dương trên chính sáu khối, ngắt dòng lại còn xanh, thay phần cuối phát biểu đỏ, mutant bỏ ranh giới chết. **Nguy cơ:** nới sang substring toàn tệp làm câu phủ định/hậu tố trái nghĩa vẫn qua.

ĐÃ THỬ NGHIỆM: `python -B out/protocol_probe.py` rc 0; `PROTO_NUMSTAT 39 2`; kết quả FULL của tám neo lần lượt `1,0,0,0,0,1,0,0`. Đây là công thức của spec, không phải một implementation bat-bien đã được giao.

ĐỘ TIN: cao.

### neo-thieu-nghia-vu [P1] F02 — Có thể mất bốn nghĩa vụ cốt lõi mà giữ nguyên cả tám neo

TỆP/DÒNG: `ops/specs/wp1466.md:158–181,360–367,391`.

VẤN ĐỀ: Bỏ riêng từng phần sau vẫn giữ đủ tám chuỗi: (1) yêu cầu quét mọi biểu hiện cùng lớp; (2) công thức |F|/|U| theo lớp; (3) không reset lịch sử bởi revision/scope cut; (4) cả khối P5 buộc ghi sổ `xet_lai_cach_lam`. Vì vậy sửa F01 vẫn chưa làm G9 bảo vệ nghĩa vụ Q1 và chỉ thị chủ kho. Neo số 8 chỉ giữ câu “đòi xem lại cách làm”, không giữ cách ghi sổ, quyền tự quyết và điều kiện E1/E3.

GỢI Ý VÁ: **Ở đâu:** Q3, danh sách neo và ca G9. **Cách:** lập ánh xạ từng nghĩa vụ Q1/§8.3/§12 sang phát biểu được kiểm; giữ nguồn duy nhất ở protocol. **Ca khóa:** bỏ/đảo từng nghĩa vụ phải đỏ; chỉ ngắt dòng phải xanh; mỗi phép bỏ kiểm có mutant riêng. **Nguy cơ:** khóa cả đoạn quá rộng dễ bắt oan thay đổi biên tập không đổi nghĩa; phải định nghĩa phạm vi chứ không tăng tùy ý số chuỗi.

ĐÃ THỬ NGHIỆM: `python -B out/protocol_probe.py` rc 0, bốn dòng `SEMANTIC_REMOVAL ... SOURCE_COUNT 1 ALL_EIGHT_SUBSTRING_PRESENT True ERR []`. Đã quét toàn bộ tám neo và bảy mục Q1, không chỉ câu công thức.

ĐỘ TIN: cao.

### cong-khong-do-bat-bien [P1] F03 — Sáu ô “có cổng” mạnh hơn điều cổng và ca thực sự đo

TỆP/DÒNG: `ops/specs/wp1466.md:171–175,260–270,298–310`.

VẤN ĐỀ:

- **INV-04:** `kiem-merge` K0 chỉ kiểm base/ancestry và head PR. `cong_c_k0_pr_head` đổi head từ xa; không kiểm authorization land hay tách deploy. Mục Giới hạn không nói phần authority của INV này chưa được cổng trỏ tới đọc.
- **INV-05:** bước `eol-policy selftest` chạy các fixture; ca được trỏ tạo `moi.py` CRLF trong kho giả và kiểm staged. Cổng kiểm EOL của ứng viên là bước **`eol-policy survey`**, lệnh `eol_policy.py --all --json`, ngay sau đó. Ô bảng trỏ sai bước.
- **INV-06:** `init` và `init_cung_provider_thoat_4` chỉ kiểm nhãn provider/họ model; không đọc ID phiên hay việc một phiên chuyển vai. Ghi “guard chỉ là lời nhắc” không khai giới hạn của chính `init` được bảng chọn.
- **INV-13:** `_kiem_lop_review` trả về cho schema_version <2, chỉ cảnh báo nếu có ngày mới. Dòng INV và mục Giới hạn không công khai cửa legacy này, trong khi đang hứa fail-closed cho mọi packet.
- **INV-15:** D2 kiểm các giá trị nhãn trong `moc_10_2_2`; `cong_c_d2_not_measured` chỉ đổi một nhãn. Nó không kiểm repository/run/attempt/checkout/workflow definition/artifact mà §10.2.2 gọi là bốn mốc provenance. Không nên nâng “đủ bốn nhãn đạt” thành đã có phép xác minh bốn mốc.
- **INV-16:** `record-codex-call` cưỡng chế trục lời gọi. Attempt do cửa khác quản; vòng review do `record-review` quản; `pl_m3_codex` không thử đổi phiên/prompt/state-dir để chứng minh toàn bộ lịch sử không reset. Giới hạn hiện chỉ nhắc việc lời gọi phải được ghi và dòng khai trần chưa được đọc.

Đây không phải yêu cầu wp1466 phải sửa toàn bộ các cổng cũ. Chính Q2 yêu cầu cổng đọc đúng bất biến và phần còn lại phải được khai. Việc đóng băng bảng sai khiến người đọc coi các nghĩa vụ chưa được cưỡng chế là đã có bảo vệ.

GỢI Ý VÁ: **Ở đâu:** sáu ô `p2-moi` và mục Giới hạn/Nợ của ADR. **Cách:** đổi sang đúng consumer; với bảo vệ một phần, tách phát biểu hoặc ghi cụ thể phần có máy và phần kỷ luật có nợ. **Ca khóa:** mỗi ca đo đúng vị từ của phần được gắn cổng; đối chứng giữ nhãn nhưng bỏ evidence thực; với EOL, vi phạm index thật phải đỏ qua survey. **Nguy cơ:** đổi tất cả thành “0 cổng” cũng sai vì một phần đã có máy; không xóa bằng chứng dương hiện có.

ĐÃ THỬ NGHIỆM: `python -B out/contract_probe.py`; đọc thân cổng/ca ở bảng INV; `python -B -u out/run_selected.py` → 71/71 đạt, gồm 14 ca packet-loop được bảng trỏ (một ca trùng họ doctrine đã khử trùng), hai họ adr/doctrine và ca kiểm mỏ neo mutant. Không chạy bốn ca ngoại vi được viện dẫn; đã đọc định nghĩa của chúng. Không dùng 71/71 để khẳng định toàn bộ bất biến đúng.

ĐỘ TIN: cao.

### thieu-truy-vet-yeu-cau [P1] F04 — Bảng 21 INV và mục audit bỏ sót nghĩa vụ mà không có nợ tương ứng

TỆP/DÒNG: `ops/specs/wp1466.md:119,283–315,230–247,504–516`.

VẤN ĐỀ: Hai nhóm thiếu có cùng cơ chế: danh sách đầu vào được chọn chưa đối chiếu ngược với nguồn.

1. **Bất biến protocol:** không có dòng cho §1(7) “chat/label/assignee/board không là nguồn sự thật”; §1(10) về durable facts/single-writer authority; ba bất biến đích danh §12 **(a), (b), (c)** về gate trước push, push thêm và nhánh sổ sách; giới hạn hai executor writer ở §8 (audit B13 đã nêu việc nâng lên ba). INV-19 chỉ nêu người cấp lease, không bao phủ cả authority/transition và các quy tắc push. Không có nợ có tên cho phần bị bỏ.
2. **Audit:** B8/B15 được ghi “kỷ luật, không gộp” nhưng không có tên nợ. Các phần A3 (đọc nguồn trước), B9 (sandbox/identity thực), B10 (lease-spec-runtime lệch), B11 (prompt được lưu/băm/neo trước giao), B13 và C1–C4 không có quyết định gộp/nợ rõ. B6 chỉ chuyển phần stdout vào KN-1, chưa chỉ ra nơi giữ nghĩa vụ giao verdict/receipt bền. Không thể suy mọi phần này đã nằm trong nợ handoff hay schema chỉ vì cùng dùng từ “evidence”.

Mục tiêu chủ kho là mọi nguyên tắc quan trọng có cổng hoặc nợ có tên và máy canh bảng; việc đặt thêm INV-18 ngoài protocol không bù các bất biến đã có trong protocol mà bị bỏ.

GỢI Ý VÁ: **Ở đâu:** mục 7/M2, `p2-moi`, mục Nợ và mục 15. **Cách:** ma trận từ từng bất biến nguồn và A1–C5 tới INV/cổng/nợ có tên; trường hợp đồng nghĩa giải thích ánh xạ, không bắt mỗi ý thành một INV riêng. **Ca khóa:** kiểm thiếu một ID đã được chốt làm đỏ; audit thủ công xác nhận danh sách ID đã phủ nguồn trước khi khóa. **Nguy cơ:** thêm số lượng ID mà không tách nghĩa rõ sẽ làm bảng dài nhưng vẫn thiếu độ phủ; số 21 phải đo lại, không giữ vì thẩm mỹ.

ĐÃ THỬ NGHIỆM: `git -C cay-kho show origin/ops/wp1172-kiem83-thamkhao:ops/specs/wp1172-kiem83/AUDIT_TUAN_THU_PHIEN_DIEU_PHOI_20261120.md` → 62 dòng, 23 điểm; đối chiếu toàn bộ 21 dòng `p2-moi`, chín dòng mục 15 và mục Nợ. `python -B out/more_measure.py` xác nhận 23/21 và đúng ref audit.

ĐỘ TIN: cao.

### kiem-chuoi-khong-doc-cau-truc [P2] F05 — G1, G7 và G8 vẫn nhận dấu vết chữ thay cho khai báo hợp lệ

TỆP/DÒNG: `ops/specs/wp1466.md:171–181,369,383,389–390`.

VẤN ĐỀ:

- **G1:** `_che_khong_render` chỉ che rào và comment HTML. Một **toàn bảng có header+separator**, đặt trong khối HTML không được render thành bảng, vẫn có các dòng liên tiếp đúng hình G1. Kiểm thuộc-về-bảng bằng header không giải quyết toàn bộ vùng HTML chứa cả bảng. Không dựng nội dung phản chứng theo giới hạn của lượt review.
- **G7:** dòng trông như định nghĩa hàm hoặc chuỗi `("tên",` không chứng minh Python định nghĩa/đăng ký tên ấy. Chúng có thể nằm trong literal nhiều dòng, comment hoặc phần mô tả. Đây là “không có ca thật” khác với giới hạn được ADR chấp nhận “ca có thật nhưng có đo đúng không”.
- **G8:** Q2 yêu cầu nợ **ghi ở mục Nợ**. G8 chỉ yêu cầu token backtick ở đâu đó trong ADR, không che vùng không render, không bó vào mục Nợ. Khi mục nợ bị bỏ mà còn một lần nhắc lịch sử, điều kiện thiết kế vẫn đạt.

GỢI Ý VÁ: **Ở đâu:** hợp đồng G1/G7/G8 và các ca/đột biến tương ứng. **Cách:** xác định vùng khai báo Markdown hợp lệ; đối với Python dùng cấu trúc nguồn/đăng ký được chấp nhận, không import mã tùy ý để “kiểm tên”; nợ phải là mục hiện hành trong vùng Nợ. **Ca khóa:** phiên điều phối dựng các trường hợp chỉ còn chữ ở vùng không khai báo; đối chứng khai báo thật vẫn xanh, mutant bỏ phạm vi phải bị giết. **Nguy cơ:** parser quá hẹp có thể từ chối các ca đăng ký sinh bằng bảng hiện có; phải thử đủ 18 tham chiếu thật.

ĐÃ THỬ NGHIỆM: đọc `_che_khong_render` tại `packet_loop.py:1874–1915` và hợp đồng G1/G7/G8; `python -B out/contract_probe.py` → mask chỉ có fence/comment, G8 không bó mục. **Không chạy payload** và không khai đã có exploit end-to-end của `bat-bien` tương lai.

ĐỘ TIN: cao về thiếu điều kiện cấu trúc; hành vi implementation tương lai chưa đo được.

### duong-dan-chua-khep-trong-goc [P2] F06 — G7 chỉ chặn absolute/“..”, chưa bảo đảm đích tệp ca nằm trong gốc

TỆP/DÒNG: `ops/specs/wp1466.md:356,388–389,405`.

VẤN ĐỀ: G7 yêu cầu đường tương đối không có `..`; ca thoát gốc chỉ thử hai dạng absolute và có đoạn `..`. Một đường hoàn toàn tương đối vẫn có thể qua symlink ở tệp/cha tới ngoài gốc. Những cách biểu diễn đường dẫn khác nền cũng chưa có luật chuẩn hóa chung. G6 có chữ “dưới gốc” cho **tệp cổng**, nhưng G7 không nêu điều kiện resolve tương ứng cho **tệp ca**. Vì vậy một implementation tuân nguyên văn G7 vẫn có thể công nhận định nghĩa bên ngoài snapshot được review.

GỢI Ý VÁ: **Ở đâu:** hợp đồng đọc tệp chung ở 8.3 và G7; không chỉ thêm vài chuỗi cấm vào ca. **Cách:** xác định chuẩn đường repo-relative, resolve và kiểm đích nằm dưới root; xử lý symlink không đọc được/thoát root bằng KĐĐ đỏ. **Ca khóa:** điều phối tạo đối chứng liên kết nội bộ hợp lệ và liên kết ra ngoài có tệp/định nghĩa thật; mutant bỏ kiểm containment phải đổi màu đúng ca. **Nguy cơ:** resolve khác nền và file chưa tồn tại cần kết quả rõ; không dùng thiếu tệp làm lý do giả để test thoát gốc đỏ.

ĐÃ THỬ NGHIỆM: đối chiếu G6/G7/8.4 với §5 protocol (resolve symlink/parent và giữ trong worktree). **KHÔNG ĐO ĐƯỢC bằng thực thi** vì chưa có cổng và chỉ thị cấm reviewer dựng payload đường dẫn; hướng thử chỉ mô tả bằng lời.

ĐỘ TIN: cao về lỗ hợp đồng; chưa đo mã tương lai.

### moc-chuyen-tiep-mau-thuan [P2] F07 — ADR và KN-1 chọn hai phạm vi hiệu lực khác nhau

TỆP/DÒNG: `ops/specs/wp1466.md:202–210,499`.

VẤN ĐỀ: ADR nói không xét lại review bắt đầu trước cutover, hàng Q4 mã chỉ áp cho review bắt đầu từ land cổng. §14.5 lại thêm “và cho mọi H có ngày commit từ thời điểm ấy”. Nếu hiểu là hợp hai tập, review đã bắt đầu trước mốc trên H có ngày commit ở phía sau mốc bị chặn trái miễn hồi tố; nếu hiểu là giao hai điều kiện, review mới trên H cũ lại được bỏ qua. Timestamp commit không phải thứ tự land và có thể lệch đồng hồ; đây không phải chỉ khác cách diễn đạt. Hợp đồng nói đã đo/không quyết lại nhưng chưa có bảng chân trị hay ca chuyển tiếp.

GỢI Ý VÁ: **Ở đâu:** bảng Hiệu lực ADR và §14.5 cùng một lần. **Cách:** chọn một vị từ, định nghĩa nguồn/mốc thời gian và xử lý dữ liệu thiếu; nếu chủ định áp thêm theo H thì ghi rõ ngoại lệ và authority. **Ca khóa:** đủ bốn ô review trước/sau × H trước/sau, cùng ca thời gian vắng/lệch; mutant đảo điều kiện hoặc dùng sai mốc phải chết. **Nguy cơ:** hồi tố âm thầm hoặc mở đường giữ H cũ để bỏ cổng mới.

ĐÃ THỬ NGHIỆM: `python -B out/contract_probe.py` in bảng chân trị; hai ô chéo bất đồng giữa luật ADR và một trong hai cách hiểu KN-1. Chưa chạy cutover thật vì schema v2 chưa tồn tại.

ĐỘ TIN: cao.

### tieu-chi-dong-xoa-khong-do-hanh-vi [P2] F08 — N8 suy “không sửa hàm cũ” từ đúng một dòng xóa

TỆP/DÒNG: `ops/specs/wp1466.md:107,398,421`.

VẤN ĐỀ: N8 khẳng định sửa hàm cũ sẽ làm dòng xóa lớn hơn 1. Thêm dòng vào hàm cũ không xóa dòng nào; sau đổi epilog bắt buộc, tổng vẫn −1. 57 ca adr/doctrine và chốt mỏ neo cũ không phủ mọi hành vi của tất cả hàm sẵn có mà §6 cấm sửa. Tiêu chí số dòng vì thế không thực hiện phép âm đã hứa.

GỢI Ý VÁ: **Ở đâu:** N8. **Cách:** so diff/AST hoặc vùng nguồn được phép đổi, với ngoại lệ tường minh cho hằng/hàm mới, parser và epilog; vẫn chạy hồi quy. **Ca khóa:** thêm dòng trong hàm cũ, thêm nhánh cũ, đổi một hàm không thuộc họ adr/doctrine đều phải bị phép kiểm phạm vi từ chối; thêm hàm mới hợp lệ vẫn qua. **Nguy cơ:** AST có thể bỏ qua comment/format; nếu hợp đồng đòi giữ byte thì cần so nguồn chứ không chỉ AST.

ĐÃ THỬ NGHIỆM: `python -B out/contract_probe.py`: thêm `pass` vô hại vào `cmd_doctrine_scan` và đổi epilog trên hai tệp `.txt` dưới out, `git diff --no-index --numstat` → **+2/−1**. Không sửa code checkout.

ĐỘ TIN: cao.

### dem-khong-khai-tap-ca [P3] F09 — 1581 là tập áp dụng Linux, không phải toàn sổ đăng ký

TỆP/DÒNG: `ops/specs/wp1466.md:55,546`; liên quan phép cộng sổ nền ở N6 dòng 419.

VẤN ĐỀ: Hai chỗ gọi 1581 là “sổ ca”. Trên chính blob nền, `CASES` có **1582 tên duy nhất**. `packet_loop_test_manh.ca_dang_ky` gọi main qua bước lọc nền mới còn **1581** trên Linux, loại `wp1174_windows_claim_rejected`. Con số 1581 có cơ sở, nhưng đơn vị bị thiếu; không được đem nó cộng số ca mới rồi đối chiếu với toàn registry ở N6. Đây là lỗi khai phạm vi theo L1, không phải đã phát hiện mất một ca Linux.

GỢI Ý VÁ: **Ở đâu:** S10, §18 và N6. **Cách:** ghi cả tổng đăng ký và tập áp dụng trên nền, chọn cùng một phép đếm trước/sau. **Ca khóa:** in số trước lọc/sau lọc và phần sai khác; không cần thêm test sản phẩm cho sửa số liệu này. **Nguy cơ:** đổi cả hai thành 1582 rồi đòi Linux chạy ca Windows cũng sai.

ĐÃ THỬ NGHIỆM: `python -B out/contract_probe.py` → `CA_COUNT_REGISTRY 1582 UNIQUE 1582`, `CA_COUNT_LINUX 1581`, sai khác đúng `{'wp1174_windows_claim_rejected'}`; hash tệp test bằng blob origin/master, không phải drift.

ĐỘ TIN: cao về hai số và đơn vị; hạng P3 vì đây là làm rõ phép đếm, không có test Linux bị mất.

### schema-bo-sot-provider-hop-le [P2] F10 — “V1 cộng thêm khóa” chưa đủ cho verdict của mọi reviewer được protocol cho phép

TỆP/DÒNG: `ops/specs/wp1466.md:183–210,493–508`.

VẤN ĐỀ: Q4 áp cho **mọi** review, còn hợp đồng KN-1/B7 mô tả v2 là v1 cộng các khóa mới và nói cổng kiểm chúng không cần thêm mã. V1 giữ enum provider `claude|codex|human`, enum identity tương ứng không có Google Antigravity. Protocol hiện hành cho phép `google_antigravity` với họ model/surface/transport khai riêng. Giữ các ràng buộc v1 rồi chỉ thêm khóa sẽ từ chối reviewer hợp lệ, không liên quan nợ phủ finding lượt trước. Đây là thiếu hợp đồng của KN-1 mà wp1466 đang muốn đóng băng, không phải lỗi v1 lịch sử cần sửa tại chỗ.

GỢI Ý VÁ: **Ở đâu:** §14/B7 và phạm vi Q4. **Cách:** chỉ rõ v2 giữ điều gì, thay enum/identity nào để tương thích protocol; v1 vẫn bất biến. **Ca khóa:** verdict AG hợp lệ qua, cùng họ model nhưng khai cross_approved vẫn bị xử theo luật assurance; provider/surface không khớp đỏ. **Nguy cơ:** mở enum thành chuỗi tùy ý sẽ làm yếu kiểm identity thay vì hỗ trợ đúng provider.

ĐÃ THỬ NGHIỆM: đọc `.github/coordination/schemas/review_verdict.v1.schema.json`; `python -B out/contract_probe.py` → `SCHEMA_V1_PROVIDER ['claude', 'codex', 'human']`; đối chiếu phần provider đầu protocol và §7/§8. Không có nguyên mẫu v2 để xác minh tác giả đã sửa enum ngoài lời hợp đồng.

ĐỘ TIN: vừa; v2 chưa giao nên kết luận giới hạn ở hợp đồng “chỉ cộng khóa”.

### tien-kiem-lease-chua-du [P2] F11 — Điều kiện bắt đầu chưa chứng minh ref mới và không có giao write set

TỆP/DÒNG: `ops/specs/wp1466.md:28,46,49`.

VẤN ĐỀ: Có hai điều kiện còn thiếu trong phép tiền kiểm được mô tả:

- So **tập tên** sau fetch không chứng minh SHA từng ref bằng máy chủ. Chính S1 ghi ba ref stale dù tên khớp. Adapter cross-review đã yêu cầu so hai chiều cặp SHA+tên và xét cả ref ngoài origin; lệnh ai-dang-giu đọc cả local heads/remotes.
- `_lease_cham_duong` chỉ so chuỗi bằng nhau, còn write set của §5 là exact/prefix đã chuẩn hóa. Hỏi đúng bốn filename không thấy lease giữ thư mục cha; hỏi `docs/adr/` như S4 không thấy lease chỉ giữ tệp con. Điều kiện rc 0 vì thế chưa chứng minh “không ai giữ effective write set”.

Snapshot này không cho thấy va chạm thật ở bốn tệp; finding nói về hợp đồng lúc bắt đầu sau B4, khi ref/lease đã đổi, không cáo buộc đang có hai writer.

GỢI Ý VÁ: **Ở đâu:** điều kiện (3) dòng 28 và lệnh đo lại S4. **Cách:** dùng đầy đủ phép đo độ mới ref của adapter, rồi kiểm giao exact/prefix chuẩn hóa trên tập lease còn hiệu lực; không dùng output rỗng như chứng cứ nếu quét hỏng. **Ca khóa:** ref cùng tên khác SHA; lease prefix cha giữ filename; lease tệp con giao yêu cầu thư mục; đối chứng hai đường không giao. **Nguy cơ:** dùng lời gọi mạng làm mới trong reviewer read-only trái bootstrap; việc fetch/cấp snapshot thuộc bước cấp môi trường, còn checker cần ghi giới hạn độ mới.

ĐÃ THỬ NGHIỆM: đọc `lease_publish.py:713–790` và phần ai-dang-giu của adapter; `python -B out/leases.py` quét 536 bản ghi, 8 còn hạn, 3 bia mộ; kiểm giao prefix trong snapshot cho bốn tệp ra 0. Không gọi GitHub để tuyên bố snapshot còn mới ở thời điểm cấp lease tương lai.

ĐỘ TIN: cao.

### doi-diem-goi-cong-chua-du-yeu-cau [P2] F12 — Chuyển neo ra khỏi doctrine-scan bỏ lại entrypoint chủ kho yêu cầu

TỆP/DÒNG: `ops/specs/wp1466.md:15,107,120,525`.

VẤN ĐỀ: Chỉ thị đầu vào yêu cầu `doctrine-scan` neo §8.3 và dòng bất biến §1. D4 tự chuyển toàn bộ sang `bat-bien`, đồng thời §6 cấm sửa `cmd_doctrine_scan`. Với thiết kế này, người gọi doctrine-scan theo các adapter hiện hành vẫn nhận “sạch” khi §8.3 bị bỏ. Cổng mới có thể được gọi trong CI là một bảo vệ bổ sung, nhưng không làm hợp đồng của entrypoint cũ đáp ứng yêu cầu đã chọn. Không có nợ riêng hay dòng E3 trình bày việc bỏ yêu cầu entrypoint đó; lý do “nó chỉ đọc n-gram” mô tả hiện trạng, chưa là bằng chứng không thể mở rộng.

GỢI Ý VÁ: **Ở đâu:** D4, §6 và M3. **Cách:** có thể dùng một hàm kiểm chung và để doctrine-scan tiêu thụ phần neo cần thiết; nếu giữ cổng riêng thì trình rõ thay đổi yêu cầu/ảnh hưởng consumer để chủ kho quyết, hoặc ghi nợ đúng phần chưa làm. **Ca khóa:** gọi chính doctrine-scan trên bản thiếu §8.3/dòng bất biến phải đỏ; bản nguyên vẹn và bản chỉ ngắt dòng phải xanh. **Nguy cơ:** gọi toàn bộ bat-bien từ doctrine-scan có thể làm fixture cũ thiếu ADR/bảng đỏ oan; cần chọn seam kiểm đúng phạm vi, không thêm nhánh bỏ qua mù.

ĐÃ THỬ NGHIỆM: `python -B out/contract_probe.py` → bản dựng thiếu toàn §8.3 vẫn `rc=0`, `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine`. Đã phục hồi scratch sau phép đo.

ĐỘ TIN: cao về khác biệt yêu cầu và kết quả entrypoint.

## CHƯA ĐO ĐƯỢC VÀ GIỚI HẠN BẢO ĐẢM

- Không có implementation `bat-bien`, schema v2, bộ kiểm verdict, 44 ca hay 33 mutant mới. Không khai đã chạy chúng; 71/71 là ca **nền chọn lọc**, không phải toàn suite và không phải nghiệm thu mã mới.
- Nguyên mẫu ngoài kho S13 (26 ca verdict, 37 ca bat-bien, 72 dòng mã, schema 73 dòng, version jsonschema tại máy soạn) không được giao. Phần ấy không tái lập độc lập được. Dựng protocol/ADR và đếm danh sách không thay bằng chứng prototype.
- Không chạy full selftest, toàn packet-loop, Ruff, Windows hay full mutant CI. Không có CI exact-H, approval/waiver/audit/merge của triển khai tương lai. N15 vẫn chưa đo.
- Mirror không chứa response REST lịch sử: số comment/giờ tạo Issue, tình trạng PR đóng #1462, ruleset/bypass actors và branch protection chưa xác minh độc lập. Không đánh đồng 5 check trong `CHECK_BAT_BUOC` với 6 check của ruleset. Đây là hai nguồn có phạm vi khác nhau, không phải bằng chứng đặc tả sai số 6.
- Chỉ mô tả phản chứng cần payload đường dẫn/chuỗi độc hại; không soạn hoặc chạy payload. Các lỗi thiết kế loại này được ghi đúng mức chứng cứ, không giả kết quả khai thác.
- Model/effort thực phục vụ và session ID chưa có nguồn đo riêng trong lượt này; khai KHONG_DO_DUOC, không suy từ model yêu cầu trong đặc tả. Assurance ở header là **đề nghị theo assignment**, không phải approval hay quyền land.
- Cuối phép đo, tracked/untracked checkout không có delta; HEAD/base/băm đặc tả giữ nguyên. Có một file ignored `launcher.cpython-313.pyc` mtime `18:34:04Z`, trước lượt này; không xóa/sửa nó. Không có snapshot hash ignored đầu lượt nên không tuyên bố đã chứng minh toàn bộ lịch sử không ghi. Các lệnh reviewer dùng `-B`, test con đặt `PYTHONDONTWRITEBYTECODE=1`, cache/thư mục tạm mới ở `out/`.

Không sửa kho, không push, không ghi API GitHub. Kết quả review và mọi bản dựng/nháp mới nằm trong `out/`.
