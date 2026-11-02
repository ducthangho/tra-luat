verdict: changes_requested
reviewed_sha: 2e4183bc2dc40e6bc306e377fc442ff0f405bbe0
Kết quả: 0 P0, 3 P1, 1 P2, 0 P3.

## KẾT LUẬN VỀ FINDING CŨ

- P1 verdict-surface-bo-sot-wp766: **ĐÃ ĐÓNG / ĐÃ VÁ THẬT**. Caveat và hàng README đúng verdict dòng 12, run `5d4f7321d9a04ee1a87934e41fcf45c8`, run.json dòng 78 `codex_cli`, chương trình `codex`. Byte verdict giữ nguyên, băm khớp (Hướng 2–3, 5).
- P1 ho-so-luot2-van-khai-hint-chua-ap: **ĐÃ ĐÓNG / ĐÃ VÁ THẬT ở các vị trí lượt 2 đã nêu**. Receipt lượt 2, hai hàng README và khối land đã nhận đúng nội dung hint; có mốc 765ae89/578fb4b và commit áp 82359c4. Khối land lượt 3 cũng được chú giải lịch sử. Còn trạng thái cũ ở hồ sơ khác, gồm chính hàng mục lục lượt 3, là các finding bên dưới (Hướng 2, 10–11).
- P2 surface-service-cli-thieu-dieu-kien-nguon: **ĐÓNG MỘT PHẦN theo lớp**. Đúng 13/13 thể hiện cũ đã vá thật: đúng tệp/dòng/run ID, thiếu runtime được khai rõ, không tự chọn surface; nhưng quét mở rộng còn `pr526-review-3` và `slice-b-c-review-2` tự khai Codex service chưa có caveat. Phần 13 tệp cũ đã đóng; toàn lớp chưa hết (Hướng 4, 9).

Các finding tính theo cơ chế sai; bảng dưới mỗi finding liệt kê các thể hiện đã đo. Có ba nhóm trạng thái sai và một nhóm thiếu điều kiện nguồn. Một số thể hiện đã tồn tại ở cha/master; nhiệm vụ yêu cầu quét hiện trạng toàn kho, nên chúng vẫn được ghi, không gán là hồi quy do 2e4183b tạo ra. Không có kết luận approve, assurance hoặc quyền land từ việc các gate xanh.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Định danh cây | Exact SHA, detached, đầy đủ, abbrev7 | `git rev-parse HEAD HEAD^{tree}` = `2e4183bc2dc40e6bc306e377fc442ff0f405bbe0` / `f047c38ebb08fd51cec06d382dce37c4f28b03f4`; shallow=false; status rỗng (H1) | Có |
| Cha và phạm vi bản vá | c8c1ee0..2e4183b; toàn PR so 101263f | `audit.py history`: cả 4 diff/numstat byte_match=True; bản vá 18 tệp, +103/-7 | Có |
| 15 receipt áp nguyên hint | --fuzz=0 | `audit.py history`: cả 15 patched_blob_match=True, missing=extra=0 (H2) | Có |
| Phần chèn tay README/land | Hai hunk README + một hunk land lệch context | Áp hint lên cha rc1, đúng 3 hunk thất bại; so +/- không thiếu dòng hint nào; ngoài hint chỉ đổi caveat lượt 3 ở README và thêm 4 dòng land (H2) | Có |
| Đổi thêm receipt lượt 3 | CHUA-AP thành DA-AP-CAN-VERDICT-MOI | Diff đúng 2 dòng thêm/2 dòng xoá, giữ kết quả lịch sử; ngoài 17 tệp hint chỉ có receipt lượt 3 (H2) | Có |
| Giải xung đột #951 | Hai hunk dùng master cho pr889 lượt 1 | Receipt merge bằng nguyên blob master; hàng README caveat merge bằng hàng master, đúng 1 hàng (H2) | Có |
| “commit kế tiếp sau c8c1ee0” | Nơi áp hint lượt 3 | `git rev-list --ancestry-path --reverse c8c1ee0..2e4183b` chỉ có candidate, là con trực tiếp (H2) | Có; không báo sai vì cách định danh này |
| Caveat wp766 | Dòng12/run5d4f7321/run.json78/CLI | `audit.py caveats`: đúng tất cả; 29832B, SHA256 `e6e59c2a9958f454ec010ca2b60d102ff30e0d11378d061a106d07d1ffaba515` (H3) | Có |
| 13 caveat P2 | Đúng tệp/dòng/ID, không chọn bề mặt | 13 matches_receipt=True, 13 README_rows=1/text_match=True; 0 run.json đúng các ID trong 46 JSON toàn kho (H4) | Có, xem bảng 13 tệp cuối báo cáo |
| Hồ sơ lượt 2 | Mọi câu CHUA-AP của lượt 2 có mốc | Nội dung thay đúng hint, land có mục lịch sử 765ae89/82359c4 (H2/H10) | Có |
| Hồ sơ lượt 3 | Trạng thái hint đã được cập nhật | Caveat receipt/README + ghi chú land đúng; hàng mục lục README:1047 vẫn “HINT.patch luot 3 chua ap” (H10) | Không — P1 |
| “Chưa review lại” ngoài lượt 2 | Quét cả kho | 8 receipt + hàng README + land còn câu cũ, trong khi có verdict kế tiếp đọc bản vá (H10) | Không — P1 |
| “Chưa là tổ tiên master/chỉ trên nhánh” | Quét trạng thái ngoài danh sách | 23 receipt có mệnh đề trực tiếp trái `merge-base --is-ancestor <OID> 101263f` và candidate, đều rc0 (H11) | Không — P1 |
| Surface ngoài 13 | Quét mọi verdict và bản trong thư mục | 306 tệp, 291 nội dung phân biệt; còn 2 tự khai service/nguồn CLI chưa caveat (H9) | Không — P2 |
| Tự khai với nhắc finding | Không bắt nhầm chuỗi codex_service | 13 verdict phẳng chứa tên máy: 10 tự khai đã có caveat, 3 chỉ mô tả finding; đọc cả cuối tệp tìm 2 cách viết còn sót (H9) | Đã phân biệt |
| Receipt so với run JSON hiện có | Không tự suy surface từ tên agent | 15 cặp receipt/run đối chiếu được, không mismatch; các cặp không có runtime không được chọn surface (H9) | Có trong phần đo được |
| Byte verdict | Không sửa bản nguyên văn | 290 receipt hash+byte khớp; 14 cặp phẳng/thư mục giống byte; diff cha đổi 0 verdict; 4 path mới so master là hai cặp lượt 2/3 (H5) | Có |
| YAML và ID caveat | Không phá cấu trúc/trùng ID | 291 YAML (290 receipt + 1 land) parse với loader từ chối key trùng, errors=[] (H5) | Có |
| t26 riêng | N/N bằng nhau | rc0, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` (H6) | Có |
| t27 riêng | N/N bằng nhau | rc0, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` (H6) | Có |
| t138 riêng | N/N bằng nhau | rc0, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` (H6) | Có |
| Xoá hàng README wp766 mới | Ca nào có răng | Clone đúng SHA: t26 rc0 1/1; t27 rc1 0/1, đúng lý do thiếu hàng; t138 rc0 1/1 (H7) | Chỉ t27 có răng |
| Xoá caveat wp766 mới | Không suy xanh thành đủ caveat | Khôi phục README rồi xoá riêng 4 dòng receipt: cả ba rc0 1/1 (H7) | Cả ba không có răng |
| bien_nhan_v2 tại cay-kho | rc + kết luận dương | rc0; 237 ĐẠT v2, 11/11 legacy, 42 NỢ, 0 vi phạm/0 KHÔNG ĐO ĐƯỢC, tổng290; TỔNG ĐẠT (H8) | Đạt |
| land_evidence_nguon tại cay-kho | rc + kết luận dương | rc0; 47 ĐẠT, 26/28 miễn trừ, 0 vi phạm/0 KHÔNG ĐO ĐƯỢC, tổng73; TỔNG ĐẠT (H8) | Đạt |
| doctrine-scan tại cay-kho | rc + kết luận dương | rc0, sạch 10 tệp, 0 chép doctrine (H8) | Đạt |
| doc-claims-check tại cay-kho | JSON ok:true | rc0, stdout parse JSON `ok=true`, `strict=false` (H8) | Đạt |
| Runtime metadata lượt 2/3 | Run/head/prompt/duration/stream/model-event | `runtime_audit.py`: mọi đối chiếu True, events25/25 và29/29, elapsed làm tròn đúng, stream byte/hash đúng (H12) | Có ở tệp được lưu |
| SHA256SUMS lượt 2/3 | Hiện vật lưu nguyên byte | rc0, 106/106 và63/63 OK (H12) | Có |
| Snapshot/trace bị bỏ | OMITTED nêu băm/byte | Có bản kê, không còn byte nguồn; serving effort/toàn argv/context độc lập cũng không được tệp lưu chứng thực (H12) | KHÔNG ĐO ĐƯỢC lại; không coi là pass |
| HINT mới | patch -p0 --fuzz=0 sạch trên candidate | Dry-run rc0/apply rc0 ở clone, 34 tệp tài liệu/biên nhận; không sửa verdict/v1/gate; 7 lệnh kiểm sau áp rc0, ba ca1/1 và JSON ok=true (H13) | Đã đo trên bản sao |
| Cây giao review sau cùng | Giữ nguyên SHA/tree, không ghi | `git status --porcelain=v1 --untracked-files=all --ignored=matching` rỗng; HEAD/tree giữ nguyên (H13, xác minh cuối) | Có |

## BẢNG SĂN

Log và script ở `review_evidence/`, nằm ngoài `cay-kho/`. Mặc định lệnh cổng chạy tại `cay-kho/`; script audit chạy tại thư mục chứa PROMPT.md. Các script chỉ phân tích dữ liệu; chỉ chạy test có sẵn. Đột biến/hint chỉ áp trên bản sao từ mirror.git. Không gọi mạng hay push.


- Bắt đầu: đã đọc `runs/9b8d9a76/prompt.snapshot`; thư mục kết quả là thư mục chứa `PROMPT.md`. Chỉ đọc/đo trên `cay-kho/`; đột biến trên bản sao từ `mirror.git`, không gọi mạng.

### HƯỚNG 1: Định danh cây và ranh giới phép đo
- giả thuyết: checkout/ref được giao lệch SHA hoặc không đủ lịch sử.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho rev-parse --is-shallow-repository`; `git -C cay-kho status --porcelain=v1`; `git -C cay-kho show -s --format='%P' HEAD`; `git -C cay-kho config core.abbrev`.
- output: HEAD `2e4183bc2dc40e6bc306e377fc442ff0f405bbe0`; tree `f047c38ebb08fd51cec06d382dce37c4f28b03f4`; shallow `false`; status rỗng; cha `c8c1ee015f78fdb143a18cf926f9f3481c2a3dd1`; abbrev `7`.
- kết luận: KHÔNG PHẢI LỖI. Đã clone cục bộ `mirror.git` vào `/tmp/pr896-r4-audit-9b8d9a76/copy` và checkout detached đúng SHA để dùng cho đột biến.

### HƯỚNG 2: Tái dẫn xuất HINT lượt 3 và giải xung đột merge
- giả thuyết: phần chèn tay thiếu/thừa nội dung HINT hoặc merge lấy sai caveat master.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py history` (rc=0); script trích blob tại cha vào scratch, chạy `patch --batch --fuzz=0 -p0 -i <HINT-lượt-3>` rồi so diff và blob.
- output thật (`review_evidence/history.log`, `old-hint-apply.log`): bốn tệp diff/numstat giao kèm đều `byte_match=True`; áp nguyên hint lên cha rc=1; 15 receipt `patched_blob_match=True`, `missing_hint_lines=0`, `extra_delta_lines=0`; README thiếu 0 dòng hint, ngoài hint có 2 dòng +/- đổi caveat lượt 3; land thiếu 0 dòng hint, ngoài hint thêm 4 dòng `ghi_chu_luot3`. Tệp ngoài hint duy nhất là receipt lượt 3. Receipt pr889-review-1 của merge bằng nguyên blob master; hàng caveat README của merge bằng hàng master (`rows=1`). `next_commit_after_c8c1ee0=2e4183bc2dc40e6bc306e377fc442ff0f405bbe0`.
- kết luận: KHÔNG PHẢI LỖI về việc áp hint/giải xung đột. “Commit kế tiếp sau c8c1ee0” đo được là chính candidate, không kết luận câu đó sai vì thiếu tự ghi SHA. Việc nội dung còn sót trạng thái cũ được xét riêng.

### HƯỚNG 3: Caveat wp766 có neo đúng runtime không
- giả thuyết: caveat dùng sai run, sai dòng hoặc thay byte verdict để che mâu thuẫn.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py caveats` (rc=0; `review_evidence/caveats.log`).
- output: verdict dòng 12 tự khai `codex_service`; `ops/reviews/wp766-r1-g1-exec-review-1-codex/run.json` có `run_id=5d4f7321d9a04ee1a87934e41fcf45c8`, dòng 78 `execution_surface=codex_cli`, `lenh.chuong_trinh=codex`; đúng 1 run khớp. Verdict 29832 byte, SHA256 `e6e59c2a9958f454ec010ca2b60d102ff30e0d11378d061a106d07d1ffaba515`, khớp receipt. Nội dung caveat là đúng blob do hint tạo; không chứng thực model/effort hay tăng assurance.
- kết luận: KHÔNG PHẢI LỖI; P1 `verdict-surface-bo-sot-wp766` ĐÃ ĐÓNG.

### HƯỚNG 4: Đo đủ 13 caveat P2, không tự chọn bề mặt
- giả thuyết: caveat bỏ tệp, dẫn sai dòng/run hoặc lấy lời khai receipt làm phép đo runtime.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py caveats`.
- output: `P2_caveat_count=13`; cả 13 có `surface=codex_cli`, `matches_receipt=True`, `runtime_files=[]`, `README_rows=1`, `README_text_match=True`; script đọc đúng dòng tự khai service/API của từng verdict. Toàn kho có 46 `run.json` nhưng không run nào mang 13 ID này (pr493 lượt 5 đối chiếu cả ID viết tắt). Văn bản cả 13 caveat phân biệt hai lời khai, ghi thiếu runtime, yêu cầu bổ sung trước khi chọn surface, giữ byte verdict và không tăng assurance.
- kết luận: KHÔNG PHẢI LỖI; P2 `surface-service-cli-thieu-dieu-kien-nguon` ĐÃ ĐÓNG. Danh sách tệp, dòng, ID đầy đủ ở `review_evidence/caveats.log`.

### HƯỚNG 5: Toàn vẹn byte, YAML và ID caveat
- giả thuyết: bản vá thay verdict, phá YAML hoặc tạo ID caveat trùng trong receipt.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py integrity` (rc=0).
- output (`review_evidence/integrity.log`): `YAML_parsed=291 receipts=290 hash_and_bytes_match=290 flat_directory_pairs=14`; `errors=[]`. Có 268 verdict phẳng và 38 `VERDICT.md` trong thư mục. Diff cha→candidate đổi 0 verdict. So master có đúng 4 path verdict được THÊM (hai bản phẳng/thư mục của lượt 2 và 3), không phải sửa byte verdict cũ.
- kết luận: KHÔNG PHẢI LỖI; 290 băm/byte receipt khớp, 291 YAML parse bằng loader từ chối key trùng, không ID caveat trùng; 14 cặp bản phẳng/bản thư mục do receipt trỏ tới giống byte.

### HƯỚNG 6: Các ca bắt buộc trên cây gốc
- giả thuyết: rc xanh nhưng thiếu ca, hoặc số đạt khác mẫu số.
- lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1`): chạy riêng `python3 ops/lease_publish_test.py --chi-ca=t26_`, `--chi-ca=t27_`, `--chi-ca=t138_`.
- output thật: từng lệnh rc=0, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. Có SyntaxWarning `invalid escape sequence '\d'` trong tệp test, không ảnh hưởng rc/kết luận.
- kết luận: KHÔNG PHẢI LỖI; cả ba có N/N và hai số bằng nhau.

### HƯỚNG 7: Đột biến tài liệu trên clone tại exact SHA
- giả thuyết: nền xanh chứng minh cả hàng README và caveat mới đều được ca có sẵn bảo vệ.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/mutations.py` (rc=0); script chỉ đổi tài liệu trong clone `/tmp/pr896-r4-audit-9b8d9a76/copy`, HEAD đúng `2e4183b`, chạy ba tiền tố riêng rồi hoàn nguyên từng biến thể.
- output (`review_evidence/mutations.log`): xoá 1 hàng README wp766 mới (443 byte) ⇒ t26 rc0 `1/1`, t27 rc1 `0/1`, t138 rc0 `1/1`; t27 đỏ đúng lý do caveat thiếu ở cột id/hàng verdict. Khôi phục README, xoá 4 dòng caveat wp766 mới trong receipt (428 byte) ⇒ t26/t27/t138 đều rc0 `1/1`. `copy_status_after_restore=` rỗng.
- kết luận: KHÔNG PHẢI LỖI hiện hành của bản vá; đã đo giới hạn. Chỉ t27 có răng với mất hàng README; t26/t138 KHÔNG có răng với hàng ấy; CẢ BA KHÔNG có răng với mất caveat. Không suy ba ca xanh thành đủ caveat hay đúng ngữ nghĩa trạng thái.

### HƯỚNG 8: Bốn bộ kiểm bắt buộc tại cây gốc
- giả thuyết: bản vá gây lỗi schema/nguồn/doctrine hoặc doc-claims không thực sự ok.
- lệnh (cwd `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1`):
  - `python3 ops/bien_nhan_v2.py --root .` ⇒ rc=0; `bien_nhan_v2: 237 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 290`; `TỔNG: ĐẠT`.
  - `python3 ops/land_evidence_nguon.py --root .` ⇒ rc=0; `land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73`; `TỔNG: ĐẠT`.
  - `python3 .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ rc=0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
  - `python3 scripts/tl.py doc-claims-check --json` ⇒ rc=0; stdout parse JSON, `ok=true`, `strict=false`.
- output thật: các log `review_evidence/{bien_nhan_v2,land_evidence_nguon,doctrine,doc_claims}.log` và `.rc`.
- kết luận: KHÔNG PHẢI LỖI của gate; các lệnh đạt, không suy chúng kiểm được sự thật của mọi câu lịch sử.

### HƯỚNG 9: Quét mọi verdict tự khai surface, kể cả cuối tệp và bản trong thư mục
- giả thuyết: chỉ kiểm tên máy `codex_service`/13 tệp trong hint sẽ bỏ sót cách tự khai khác.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/surface_inventory.py`; `rg -n -i 'codex.service|service/api|execution.surface|bề mặt|surface:' cay-kho/ops/reviews --glob '*-verdict.md' --glob 'VERDICT.md'`; đọc các đoạn tự khai và receipt liên quan; quét mọi `run.json` trong kho theo ID/prefix.
- output thật (`review_evidence/surface-inventory.log`): `verdict_files=306 distinct_content=291`; `receipt_runtime_pairs_compared=15`, không có dòng `RECEIPT_RUNTIME_DIFFERENCE`. Tên máy `codex_service` xuất hiện trong 13 verdict phẳng: 10 tệp tự khai (6 đã đính chính rõ + 4 ci-g5 có caveat thiếu runtime), 3 tệp chỉ mô tả finding (pr896 lượt 2/3, pr915 lượt 1). 13 tệp service/API trong hint đã có caveat. Nhưng ngoài chúng: **pr526-review-3-codex-verdict.md:151** tự khai “execution surface Codex service qua công cụ shell”, receipt:55 ghi `surface: codex_cli`, run khai `f466d135`/`f466d135534244c1b888c9c0c44811b9`, 0 caveat; **slice-b-c-review-2-codex-verdict.md:19** tự khai “Execution surface: Codex service”, chính phần nguồn dòng 6 và receipt dòng 32 lại ghi `codex exec`, run khai `8ddb0c6f`; 3 caveat hiện có đều không nói về surface. Hai ID không có run.json tương ứng trong 46 tệp đã quét. Hai băm verdict vẫn khớp receipt.
- kết luận: LỖI P2 — còn hai thể hiện thiếu điều kiện nguồn ngoài 13 tệp; không đủ runtime evidence để chọn bề mặt thật. Các cách mô tả chung “API agent có shell” không tự phủ nhận CLI nên không tự ánh xạ chúng thành `codex_service`; các tên `claude_code_subagent` có giải thích chế độ subagent trong receipt, không phải bằng chứng chạy bằng một nền khác.

### HƯỚNG 10: Săn trạng thái patch/review cũ ngoài danh sách giao
- giả thuyết: mọi câu “HINT chưa áp”/“chưa review lại” đã được chặn ở đúng mốc lịch sử.
- lệnh: quét `ops/reviews/*.receipt.yaml`, README và `ops/land/pr896-*`; `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/state_audit.py` (rc=0); đọc verdict lượt kế tiếp và đối chiếu reviewed_sha.
- output (`review_evidence/proven-states.log`): README:1047 vẫn “HINT.patch luot 3 chua ap” trong khi caveat:749/receipt lượt 3 đổi thành DA-AP và diff candidate chứa đủ hint. Ngoài ra `review_claims_with_later_review=8`: receipt PR455 lượt 1–6, pr896 lượt 1 và pr915 lượt 1 vẫn khai chưa review; verdict kế tiếp có reviewed_sha tương ứng `c595292…`, `cb21284…`, `4ef73e6…`, `670071b…`, `5a78c15…`, `ca96016…`, `8d56009…`, `8d56009…`. PR896 lượt 2:7 đóng P2 t162; :8 xác nhận hai thể hiện P1 của #915 đã đóng, còn sót #889 lượt 1; lượt 3:6 đóng nốt thể hiện ấy. README:729/739/1042/1045 và land:190 còn nói chưa review. Những câu cũ của lượt 2 tại receipt/README nay có mốc 765ae89/578fb4b và commit áp 82359c4; hai khối land lượt 2/3 có đính chính lịch sử ở cuối, đúng nội dung hint.
- kết luận: LỖI — hai nhóm P1 trạng thái hiện hành sai; finding cũ về chính hồ sơ lượt 2 ĐÃ ĐÓNG, lớp trạng thái chưa sạch toàn kho. Không suy “đã review” thành approve hoặc hết mọi finding của các lượt cũ.

### HƯỚNG 11: Săn câu phủ nhận ancestry đã cũ, phân biệt merged với landed
- giả thuyết: các câu “chỉ trên nhánh/chưa là tổ tiên master” vẫn đúng hoặc đã ghi rõ mốc lịch sử.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/ancestry_states.py` và `python3 review_evidence/state_audit.py`; đo `git -C cay-kho merge-base --is-ancestor <OID> 101263f` và với `2e4183b`.
- output: bộ lọc trạng thái cho 37 receipt ứng viên (`ancestry-states.log`); sau đọc ngữ cảnh, giữ **23 receipt có mệnh đề trực tiếp phủ nhận ancestry/khẳng định chỉ trên nhánh**, cả 23 trả rc0 với master được ghim và candidate (`proven-states.json/log`). Gồm assurance-ho-model lượt 1; ci-windows lượt 5; doctrine-scan lượt 1–3; don-nhanh-base lượt 1 (v1); pr508 lượt 1–5; r330; wp538 lượt 1–2, wp540 lượt 1, wp541 lượt 1–2; wp678-spec lượt 7–12. Ví dụ wp678: reviewed_sha `088511f…`/`f958e14…`/`2469f3e…`/`42292b4…`/`e48423a…`/`d5a57c1…` đều ancestor master rc0, trái caveat “khong phai master”; pr508 blob `9196eaf…` ancestor master rc0, trái câu “chưa tới master”; r330 blob `5c71329…` rc0, trái câu “CHƯA phải tổ tiên master”.
- kết luận: LỖI P1 với các mệnh đề ancestry đó. KHÔNG lấy sự có mặt trong master để kết luận Packet đã landed, KHÔNG kết luận #566 đã land (604b8d9→master rc1), KHÔNG lấy mọi câu “chưa land” đơn lẻ trong 37 ứng viên làm finding. Trường hợp pr490 mô tả phép thử trên cây cũ/cây squash có ngữ cảnh lịch sử, không đếm là trạng thái hiện hành sai.

### HƯỚNG 12: Tái kiểm metadata và hiện vật của hai lượt ghi trong PR
- giả thuyết: receipt lượt 2/3 khai sai run/head/duration/model-event hoặc hiện vật lưu không khớp băm.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/runtime_audit.py` (rc=0); script đọc run JSON/receipt, hash prompt và stream, chạy `sha256sum -c SHA256SUMS` tại từng thư mục.
- output (`review_evidence/runtime.log`): cả hai launcher version 1.5.0, trạng thái xong, ma_thoat=0, worktree_sach=True; head/run ID/surface/prompt hash đều khớp receipt. Lượt 2 elapsed 600.539266, làm tròn 600.539; 25 events/25 response_id khác nhau; stdout254/stderr78 byte, hai hash đúng; checksum rc0 106/106 OK. Lượt 3 elapsed 562.081953, làm tròn 562.082; 29 events/29 response_id khác nhau; stdout540/stderr195 byte, hai hash đúng; checksum rc0 63/63 OK. Events lưu đều response.created/model gpt-6.1-sol; trạng thái JSON DO_DUOC.
- kết luận: KHÔNG PHẢI LỖI về metadata được lưu. Serving effort, toàn argv/phiên bản CLI thuật lại và sự độc lập context ngoài log không được phép đo này chứng thực. Các snapshot bị OMITTED và stderr đầy đủ đã bỏ không còn byte để hash lại; checksum của tệp được lưu không phục dựng được phần bỏ.

### HƯỚNG 13: Dẫn xuất và kiểm HINT mới
- giả thuyết: gợi ý vá khó áp hoặc đụng nhầm verdict/receipt v1/cổng.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py`; tại clone đúng candidate, `patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>` rồi áp trên clone và chạy lại ba ca t26/t27/t138 cùng bốn bộ kiểm bắt buộc.
- output: build rc0, `changed_files=34`; dry-run rc0, apply rc0, 34 path đều trong ops/reviews/ hoặc YAML land pr896, không FAILED/fuzz/offset. Sau áp trên clone: t26/t27/t138 từng rc0 `1/1 đạt; đã chạy=1, bỏ qua=0`; bien_nhan_v2 rc0 `237 ĐẠT v2 · 11/11 legacy · 42 NỢ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng290`, TỔNG ĐẠT; land rc0 `47 ĐẠT · 26/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng73`, TỔNG ĐẠT; doctrine rc0 sạch 10 tệp/0 chép; doc-claims rc0, JSON ok=true. 292 YAML parse được (290 receipt, 1 đính chính bổ sung, 1 land), 0 băm lệch/0 ID caveat trùng.
- kết luận: KHÔNG PHẢI LỖI của HINT theo các phép đo này. HINT chưa áp vào cây giao review; executor tự dẫn xuất/áp/đo. Giữ verdict và receipt v1 đóng băng; hai đính chính v1 nằm ở tài liệu bổ sung `ops/reviews/pr896-review-4-legacy-caveats.yaml` và README, không tự tạo receipt/authority mới. Ca sẵn có không đo ngữ nghĩa của mọi câu đính chính.


## FINDING

### muc-luc-luot3-van-khai-hint-chua-ap  [P1]  Hàng mục lục lượt 3 vẫn khai hint chưa áp

TỆP/DÒNG: `ops/reviews/README.md:1047`; đối chiếu hàng cảnh báo `:749`, `ops/reviews/pr896-review-3-codex-verdict.receipt.yaml:127`, land `:294`.

VẤN ĐỀ: Candidate đã áp đủ nội dung hint lượt 3, nhưng hàng mục lục tiếp tục ghi “HINT.patch luot 3 chua ap”, đồng thời nêu các thể hiện cũ như tình trạng đang thiếu. Không có mốc lịch sử gắn với vế trạng thái này, trong khi hàng cảnh báo của cùng tệp đã đổi thành DA-AP. Đây là sự thật về trạng thái patch sai tại exact SHA đang chấm, không phải yêu cầu đổi verdict `changes_requested` lịch sử thành approve. Câu “commit kế tiếp sau c8c1ee0” ở chỗ khác đo được là đúng.

ĐÃ THỬ NGHIỆM: `audit.py history` xác nhận đủ +/- của hint và 15 receipt khớp nguyên blob sau áp; `state_audit.py` xuất nguyên hàng1047; ba ca và bốn gate tại candidate vẫn xanh. Vì hàng này đang sai mà cổng vẫn xanh, các cổng sẵn có không có răng về sự thật của vế CHUA-AP.

GỢI Ý VÁ: sửa ngay ô mô tả hàng1047, neo trạng thái lịch sử vào 82359c4 và ghi hint áp tại 2e4183b; giữ số P/hash/verdict lịch sử. HINT có hunk đó. Ca khoá ngữ nghĩa chưa có trong bộ sẵn có; executor có thể thêm kiểm đối chiếu trạng thái hint ở mục lục với caveat và commit áp, đột biến phục hồi CHUA-AP phải đỏ. Nguy cơ cần tránh là biến “đã áp” thành “đã approve/được land”.

ĐỘ TIN: cao.

### trang-thai-chua-review-da-bi-verdict-sau-bac  [P1]  Tám receipt và các dòng dẫn vẫn nói bản vá chưa được review

TỆP/DÒNG: các dòng caveat sau; cùng nội dung ở bảng “Cảnh báo đang có hiệu lực” của README. Thêm README:1042/1045 và land `ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml:190`.

| receipt trong ops/reviews/ | dòng caveat | verdict kế tiếp / reviewed SHA |
|---|---|---|
| `pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml` | 92 | `pr455-bien-nhan-v2-review-2-codex-verdict.md` / `c595292cb63fb8c09d7d7b482cda20f9d5f0917f` |
| `pr455-bien-nhan-v2-review-2-codex-verdict.receipt.yaml` | 87 | `pr455-bien-nhan-v2-review-3-codex-verdict.md` / `cb212847375c2319fe0ccad3f7c00c90b870e3ba` |
| `pr455-bien-nhan-v2-review-3-codex-verdict.receipt.yaml` | 87 | `pr455-bien-nhan-v2-review-4-codex-verdict.md` / `4ef73e69d5f3c419634118983723355e25e38305` |
| `pr455-bien-nhan-v2-review-4-codex-verdict.receipt.yaml` | 91 | `pr455-bien-nhan-v2-review-5-codex-verdict.md` / `670071b700bd97a893d64393ffded0257957d0b3` |
| `pr455-bien-nhan-v2-review-5-codex-verdict.receipt.yaml` | 84 | `pr455-bien-nhan-v2-review-6-codex-verdict.md` / `5a78c150106ae381461354c77ba2023834330bbd` |
| `pr455-bien-nhan-v2-review-6-codex-verdict.receipt.yaml` | 90 | `pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md` / `ca960160b477cd16346a293aaa8752772a9921d4` |
| `pr896-review-1-codex-verdict.receipt.yaml` | 108 | `pr896-review-2-codex-verdict.md` / `8d56009a09af7b3ef93801df105f9483de212cc7` |
| `pr915-review-1-codex-verdict.receipt.yaml` | 91 | `pr896-review-2-codex-verdict.md` / `8d56009a09af7b3ef93801df105f9483de212cc7` |

VẤN ĐỀ: Các mô tả “BAN VA CHUA duoc review”/“CHUA duoc cross-review lai” thiếu mốc ngay tại câu đang được nâng thành cảnh báo có hiệu lực. Những review tiếp theo đã nằm trong candidate và thực sự đối chiếu bản vá. PR455 các lượt sau có cả kết quả vá thật, vá hờ và finding mới; bất kể đóng đến đâu, “chưa được review” không còn đúng. PR896 lượt2 dòng7 đóng P2 t162; dòng8 xác nhận hai thể hiện P1 của #915 đã đóng, còn sót một thể hiện khác; lượt3 dòng6 đóng nốt thể hiện đó. Không gọi toàn bộ verdict cũ là approve và không kết luận đã có review sạch cho toàn ứng viên hiện nay.

ĐÃ THỬ NGHIỆM: `state_audit.py` đo đủ 8 cặp receipt→verdict, đọc phần đối chiếu của từng verdict; `proven-states.json/log` lưu ID, commit ghi receipt, exact reviewed SHA kế tiếp và nguyên ba hàng mục lục mới nhất. Hash các verdict này khớp receipt (H5); t26/t27/t138 và bốn gate không phát hiện trạng thái cũ (H6/H8).

GỢI Ý VÁ: neo mô tả từng caveat vào commit ghi receipt và dẫn lượt review tiếp theo, đồng bộ README; bổ sung ghi chú lịch sử cho khối land cũ. HINT sửa đúng 8 receipt, các hàng liên quan và nối ghi chú land. Không xoá kết quả review cũ. Chưa có ca sẵn có đối chiếu ngữ nghĩa này; cần ca đọc mốc/cặp verdict kế tiếp, đột biến bỏ mốc và phục hồi lời khai hiện hành “chưa review” phải đỏ. Nguy cơ là gộp “đã review” với “đã đóng toàn lớp/approve”; hint giữ ranh giới ấy.

ĐỘ TIN: cao.

### phu-nhan-ancestry-chi-tren-nhanh-da-cu  [P1]  Hai mươi ba receipt còn phủ nhận quan hệ Git đã có trên master

TỆP/DÒNG: bảng dưới là vị trí trường chứa mệnh đề sai tại candidate. OID đầy đủ và hai mã thoát có trong `review_evidence/proven-states.json/log`.

| receipt trong ops/reviews/ | dòng trường | OID đo ancestry |
|---|---|---|
| `assurance-ho-model-review-1-claude-verdict.receipt.yaml` | 180 | `7d7f12249696e80238967c9ae2a8f360337db80e` |
| `ci-windows-review-5-claude-verdict.receipt.yaml` | 272 | `c2f68987b3f298de12b84cf29a934c7b844c8558` |
| `doctrine-scan-review-1-claude-verdict.receipt.yaml` | 137 | `bc5d0c6e4d3d5b3cc5d6f8c08ba1c005dd9bdadc` |
| `doctrine-scan-review-2-claude-verdict.receipt.yaml` | 137 | `80d816130fda69af75dc1d9ae76f3fc83b837773` |
| `doctrine-scan-review-3-claude-verdict.receipt.yaml` | 119 | `7d8bb69ac02b54075d63a9915e12e6d2bf28b513` |
| `don-nhanh-base-review-1-codex-verdict.receipt.yaml` | 29 | `e872e98e7b3612baf71fc177b54ce8b3bafd033d` |
| `pr508-review-1-codex-verdict.receipt.yaml` | 72 | `9196eaf70ca0d908b8d23ff26512c4e395e1e997` |
| `pr508-review-2-codex-verdict.receipt.yaml` | 72 | `9196eaf70ca0d908b8d23ff26512c4e395e1e997` |
| `pr508-review-3-codex-verdict.receipt.yaml` | 72 | `9196eaf70ca0d908b8d23ff26512c4e395e1e997` |
| `pr508-review-4-codex-verdict.receipt.yaml` | 72 | `9196eaf70ca0d908b8d23ff26512c4e395e1e997` |
| `pr508-review-5-codex-verdict.receipt.yaml` | 72 | `9196eaf70ca0d908b8d23ff26512c4e395e1e997` |
| `r330-rig-quyet-mau-audit-nguoi-verdict.receipt.yaml` | 168 | `5c713298c49c1dde5c550112d6bc4daf6b876735` |
| `wp538-review-1-claude-verdict.receipt.yaml` | 154 | `ab27f786a45de5df7aae23f7df7b4c4fb8eecb92` |
| `wp538-review-2-claude-verdict.receipt.yaml` | 157 | `ab27f786a45de5df7aae23f7df7b4c4fb8eecb92` |
| `wp540-review-1-claude-verdict.receipt.yaml` | 164 | `ab27f786a45de5df7aae23f7df7b4c4fb8eecb92` |
| `wp541-review-1-claude-verdict.receipt.yaml` | 154 | `34ebd10850d407b4cb1c1575284cc191e6f11bc5` |
| `wp541-review-2-claude-verdict.receipt.yaml` | 167 | `820aebc767e20f00ff2ef86d0a4d09d9e680c31d` |
| `wp678-spec-review-7-claude-verdict.receipt.yaml` | 97 | `088511f1fd75faf9bf01f0cf8da037a14fa6d22d` |
| `wp678-spec-review-8-claude-verdict.receipt.yaml` | 97 | `f958e147754bed8e9e7034dd28450681f19c3db0` |
| `wp678-spec-review-9-claude-verdict.receipt.yaml` | 97 | `2469f3ebed51dc228319cf375d7912bf7dbc0947` |
| `wp678-spec-review-10-claude-verdict.receipt.yaml` | 97 | `42292b4219901137607d3fd9adda26d49f7cfd5e` |
| `wp678-spec-review-11-claude-verdict.receipt.yaml` | 97 | `e48423a2719f64a5dfa2f85363874dfadf6c10f8` |
| `wp678-spec-review-12-claude-verdict.receipt.yaml` | 97 | `d5a57c1ac152c344eef1c3b2cfdee310bba35200` |

VẤN ĐỀ: Đây là các mệnh đề trực tiếp như “quan he to tien voi master CHUA CO”, “chưa tới master”, “commit công bố hiện chỉ được nhánh ops giữ”, “CHƯA phải tổ tiên master” hoặc “reviewed_sha … khong phai master”. Các OID này nay đều là tổ tiên của master ghim101263f lẫn candidate; câu chỉ-trên-nhánh ở caveat wp678 và pr508 còn được đưa lên bảng cảnh báo có hiệu lực. Cần gắn câu vào mốc ghi sổ và ghi phép đo mới. Các header/ngày ghi receipt không tự giải quyết mâu thuẫn khi trường/caveat tiếp tục phát biểu trạng thái hiện hành.

ĐÃ THỬ NGHIỆM: `state_audit.py` chạy `git merge-base --is-ancestor <OID> 101263f` và với `2e4183b` cho từng hàng: **46/46 phép đo rc=0**. Bộ lọc rộng cho37 ứng viên; đã loại các đoạn mô tả test lịch sử và câu “chưa land” đơn lẻ không đủ để bác bằng ancestry. Riêng #566 commit604b8d9→master rc1, nên không báo “#566 chưa land” là sai; ở r330 chỉ báo vế phủ nhận ancestry của5c71329. Các gate hiện có vẫn xanh.

GỢI Ý VÁ: bổ sung mốc tại các trường/caveat v2 và đồng bộ các hàng cảnh báo; giữ nguyên giá trị assurance/cường độ lịch sử, không suy landed từ merged. Receipt v1 `don-nhanh-base-review-1` đóng băng: ghi đính chính ở tài liệu bổ sung + README, không sửa receipt hay băm allowlist. HINT áp cách đó. Chưa có ca sẵn có kiểm sự thật của văn xuôi ancestry; ca executor bổ sung nên kiểm OID và mốc ghi trạng thái, đột biến giữ mệnh đề phủ nhận như hiện hành khi ancestry rc0 phải đỏ. Nguy cơ chính là nâng assurance/land chỉ bằng quan hệ Git hoặc sửa nhầm lịch sử v1.

ĐỘ TIN: cao về quan hệ Git và các câu phủ nhận được trích; không có kết luận về trạng thái land/authority của Packet.

### surface-service-cli-con-sot-ngoai-13  [P2]  Còn hai tự khai Codex service chưa được đính chính

TỆP/DÒNG:

- `ops/reviews/pr526-review-3-codex-verdict.md:151`; receipt cùng tên `.receipt.yaml:55` ghi `surface: codex_cli`, ID khai `f466d135`/`f466d135534244c1b888c9c0c44811b9`; không có `verdict_usage_caveats`.
- `ops/reviews/slice-b-c-review-2-codex-verdict.md:19` khai Codex service, trong khi dòng6 và receipt `.receipt.yaml:32` thuật lại `codex exec` qua launcher run `8ddb0c6f`; ba caveat hiện có không nhắc surface.

VẤN ĐỀ: Quét chỉ tên máy hoặc chỉ đầu tệp bỏ sót hai cách tự khai này (một ở cuối verdict). Trường hợp PR526 là đúng dạng service/receipt CLI của 13 tệp vừa vá. SLICE-B-C có nguồn CLI trong chính header verdict lẫn receipt v1. Không có run.json đúng run trong checkout để xác quyết runtime; hai lời khai cần điều kiện nguồn/caveat, không được tự lấy receipt thắng verdict hay ngược lại. Caveat chung về model/thiếu runtime không nói tới mâu thuẫn surface thì chưa đính chính câu ấy.

ĐÃ THỬ NGHIỆM: `surface_inventory.py` quét306 tệp/291 nội dung phân biệt; tìm cả phần sau dòng35 khi chứa cách viết service. Đọc độc lập hai đoạn tự khai/nguồn; quét46 run.json theo cả ID đầy đủ và prefix, đều0 match. Verdict PR526 25283B, SHA256 `3edee44df70479bb5cb3c2eb4c081eae13109285baef520a70ab1d86c92979d2`; SLICE-B-C14578B, SHA256 `c18e65c24cc0e74942fef1c4211d175fdb96a973294816ffdd1d0335b3bb8e00`; cả hai khớp receipt. Không có bằng chứng đủ để nâng thành P1 khai sai runtime.

GỢI Ý VÁ: thêm caveat vào receipt v2 PR526 và hàng README, ghi đúng dòng/run và thiếu nguồn để chọn surface. Receipt v1 SLICE-B-C giữ nguyên: bổ sung đính chính riêng và nâng README. HINT chứa hai cách này, không đổi byte verdict. Với caveat PR526, t27 có răng về hàng README; với việc thiếu caveat thì ba ca sẵn có không có răng (H7). Chưa có ca semantic sẵn có; executor có thể mở rộng inventory đối chiếu theo tên diễn giải và cả cuối verdict, đột biến mất caveat phải bị bắt. Nguy cơ là tự chọn CLI/service hoặc vô tình hạ/tăng assurance; hint không làm vậy.

ĐỘ TIN: cao về mâu thuẫn lời khai/thiếu caveat; runtime thực tế KHÔNG ĐO ĐƯỢC lại từ dữ liệu hiện có.

## ĐỐI CHIẾU ĐỦ 13 CAVEAT P2 CŨ

Mỗi hàng dưới có receipt ghi CLI, run ID trong caveat khớp receipt, đúng một hàng README trùng toàn mô tả; không run.json đúng ID/prefix trong kho. Đây là dữ liệu từ `audit.py caveats`, không suy bề mặt thực tế.

| verdict trong ops/reviews/ | dòng tự khai service/API | run ID khai |
|---|---|---|
| `phan-bien-quy-trinh-review-3-codex-verdict.md` | 15 | `4f5341d473c8442380dc2182f9cde013` |
| `phan-bien-quy-trinh-review-4-codex-verdict.md` | 13 | `06ceaec97a1e454a970cda425836dcf1` |
| `phan-bien-quy-trinh-review-5-codex-verdict.md` | 12 | `12574e98d66c4875b2333fa1adc0bf4c` |
| `pr455-bien-nhan-v2-review-1-codex-verdict.md` | 7 | `ea42cb4174e54db8a581f4a66f43bd2f` |
| `pr455-bien-nhan-v2-review-2-codex-verdict.md` | 9 | `0bc966b1409f4ca39f0f3707bdcb20d8` |
| `pr455-bien-nhan-v2-review-3-codex-verdict.md` | 9 | `32fca3390491423c83e84d37f9904a3b` |
| `pr455-bien-nhan-v2-review-4-codex-verdict.md` | 9 | `d0266c01c4a24dd8a55d02b4ffbdd6b2` |
| `pr455-bien-nhan-v2-review-5-codex-verdict.md` | 9 | `d86357ad0e4b4a6b96a7f5b2e3c1d9f4` |
| `pr455-bien-nhan-v2-review-6-codex-verdict.md` | 9 | `c7af46a4a1e34b0d9d3c86f5b0a2e7d1` |
| `pr455-bien-nhan-v2-review-7-gpt6astra-verdict.md` | 9 | `035d3cac9f2e4b7188d6a0c53e1b74af` |
| `pr455-bien-nhan-v2-review-8-gpt6astra-verdict.md` | 8 | `b7384eee92a045a1b145718ac5310081` |
| `pr460-bien-nhan-v2-review-9-gpt6astra-verdict.md` | 5 | `3bfdc70ca03647139a3da914246acd20` |
| `pr493-review-5-codex-verdict.md` | 8 | `5f5c24ba` |


## GIỚI HẠN VÀ HIỆN VẬT

- Các kết luận trên neo đúng candidate đã ghi đầu tệp; không dùng tên nhánh để thay SHA. Không gọi mạng nên không chứng thực trạng thái GitHub hiện hành, chỉ đối chiếu dữ liệu/lịch sử Git được giao.
- Không viết lại testcase hay mã sản phẩm; chỉ chạy ca có sẵn và đột biến tài liệu/receipt trên clone ngoài cay-kho. Kết quả mất caveat sống sót được ghi là giới hạn của chốt, không gán thành lỗi sản phẩm chưa được chứng minh.
- `HINT.patch`: gợi ý tài liệu/biên nhận đã dry-run --fuzz=0 và kiểm trên clone; **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Tệp không có tác dụng đổi verdict của candidate. Tài liệu bổ sung legacy không phải receipt mới hay quyền approval.
- Mọi phép đo đã nêu có log/script ở `review_evidence/`; không yêu cầu tái chạy các driver cũ chứa đường dẫn sandbox đã mất. Snapshot/stream đã OMITTED và attestation runtime ngoài tệp lưu không được coi là tự đo lại.
