import json
from pathlib import Path
import shutil

BASE=Path(__file__).resolve().parent
dest=BASE.parent/'VERDICT.md'
shutil.copyfile(dest, BASE/'VERDICT.progress.md')
ancestry=json.loads((BASE/'ancestry-details.json').read_text())
reviews=json.loads((BASE/'review-states.json').read_text())
surfaces=json.loads((BASE/'surfaces.json').read_text())
mutations=json.loads((BASE/'mutations.json').read_text())
facts=json.loads((BASE/'final-state.json').read_text())
hint=json.loads((BASE/'hint-results.json').read_text())

text='''verdict: changes_requested
reviewed_sha: 1a276a15192013fdb1e472db409133b53ac57944
Kết quả: 0 P0, 2 P1, 0 P2, 0 P3.

## KẾT LUẬN VỀ FINDING CŨ

- P1 `muc-luc-luot3-van-khai-hint-chua-ap`: **ĐÃ ĐÓNG**. `ops/reviews/README.md:1055` ghi HINT lượt 3 đã áp tại `2e4183bc2dc40e6bc306e377fc442ff0f405bbe0`, đúng con trực tiếp của `c8c1ee0`; không còn mô tả HINT chưa áp như hiện hành. Receipt và hàng caveat cùng ghi lịch sử. “Chua merge” ở cuối hàng nói PR #947, phù hợp ancestry với master ghim (H2, H9).
- P1 `trang-thai-chua-review-da-bi-verdict-sau-bac`: **ĐÓNG MỘT PHẦN theo lớp**. Đúng **8/8 thể hiện cũ đã đóng**: mốc ghi receipt tồn tại, dẫn đúng verdict kế tiếp và exact reviewed SHA, băm khớp; README/land đã nhận nội dung hint. Còn hai receipt PR #870/#889 lượt 1, mỗi receipt có hai trường và hai hàng README vẫn phủ nhận review đã có (H7, finding bên dưới).
- P1 `phu-nhan-ancestry-chi-tren-nhanh-da-cu`: **ĐÓNG MỘT PHẦN**. Các trường nhắm trong hint và supplementary v1 đã nhận đủ nội dung; 23 hàng OID đều đúng, 92/92 phép đo rc0. Tuy nhiên **7 trong chính các receipt cũ** còn trường khác nói “hiện chỉ là một nhánh”/“không phải tổ tiên master”, không có mốc lịch sử (H6). Không tính bảy thể hiện đó là bảy finding độc lập.
- P2 `surface-service-cli-con-sot-ngoai-13`: **ĐÃ ĐÓNG**. PR526 dòng 151 đã có caveat receipt v2 + hàng README; slice-b-c dòng 19 đã có supplementary caveat + hàng README, receipt v1 giữ nguyên. Cả hai phân biệt lời khai với nguồn runtime vắng, không tự chọn surface. Quét mở rộng tìm 25 tự khai service rõ nghĩa, đều có caveat/đính chính; 15 caveat thiếu runtime (13 cũ + 2) đều khớp tệp/dòng/ID/hàng README (H8).

Hai P1 còn lại là bản sao trạng thái cũ tại exact SHA đang chấm; không phải nội dung hint bị executor áp thiếu. Không đổi kết quả review lịch sử, không suy landed hoặc authority từ ancestry/cổng xanh. Phạm vi là hai lớp được giao; không gọi mạng hoặc push.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| HEAD, cây đầy đủ, detached | 1a276a1 | `git rev-parse HEAD HEAD^{tree}`; `git rev-parse --is-shallow-repository`; HEAD/tree và lịch sử khớp H1 | Có |
| Cha và master base | cha 77a0a45; merge master 3e973a0 | `git show -s --format=%P 1a276a1 77a0a45` (H1) | Có |
| Diff/numstat giao kèm | patch cha→head và toàn PR→master | `audit.py history`: cả bốn tệp byte_match=True | Có |
| Áp nguyên hint | 31 tệp áp nguyên | 31 receipt + supplementary YAML mới = **32 blob** khớp nguyên hint; hai tệp còn lại README/land chèn tay; tổng hint 34 path (H2) | Có về nội dung; ghi rõ đơn vị đếm |
| Ba hunk chèn tay | một land, hai README | Trên cha: đúng ba hunk fail vì context; Counter +/- của diff không thiếu dòng hint; land thêm 4 dòng ngoài hint, README thêm 2 cặp +/- ngoài hint (H2) | Có |
| Receipt lượt 4 ngoài hint | đổi CHUA-AP→DA-AP | `git diff --numstat 77a0a45 1a276a1 -- <receipt>` = 2/2; ID và mô tả đồng bộ README (H9) | Có |
| “commit kế tiếp sau 77a0a45” | nơi áp hint lượt 4 | `git rev-list --ancestry-path --reverse 77a0a45..1a276a1` chỉ trả full candidate OID (H2/H9) | Có |
| Mốc lịch sử lượt 3/4 | 8879165/c8c1ee0; ff4ab57/77a0a45 còn CHUA-AP | `claims.py`: đọc blob receipt/land ở bốn OID; các ID CHUA-AP hiện diện; hint được áp ở commit kế sau mốc tương ứng (H9) | Có |
| Mục lục lượt 3 | hint đã áp ở 2e4183b | README:1055 + diff c8c1ee0..2e4183b có đủ +/- HINT lượt 3 (H9) | Có |
| Tám trạng thái chưa review cũ | đã neo lịch sử và chỉ verdict kế tiếp | `states.py reviews`: 8/8, reviewed_sha receipt/verdict và hash đúng; verdict kế tiếp chưa có ở commit mốc (H7) | Có cho 8 thể hiện |
| Lớp chưa review còn sót | phải quét ngoài tám tệp | #870/#889 lượt 1 vẫn phủ nhận; cả lượt 2/3 đã approve đúng SHA 06a50c5/094e8d1 (H7) | Không — P1 |
| 23 mệnh đề ancestry đã vá | OID là ancestor 101263f và 2e4183b | `states.py ancestry`: thêm đo master3e973a0 và candidate; 92/92 rc0; 22/22 mốc receipt v2 tồn tại (H6) | Có về các phép đo |
| Lớp ancestry còn sót | phải quét mọi trường | 7 trường ở ci-windows/doctrine-scan/wp538/wp540 còn phủ nhận hiện hành, 14/14 đo master/candidate rc0 (H6) | Không — P1 |
| Supplementary v1 | hai đính chính, giữ receipt đóng băng | `audit.py integrity`: hai hash verdict đúng, mỗi caveat có đúng 1 hàng README chứa đúng mo_ta; hai receipt bằng nguyên byte cha (H3) | Có |
| Hai surface mới và 13 cũ | đúng dòng/run, không chọn surface thiếu nguồn | `surfaces.py`: 15/15 điều kiện dòng/ID/README đúng; 0 run đúng ID; run_json_files=47 (H8) | Có; runtime thực tế KHÔNG ĐO ĐƯỢC lại |
| Surface toàn kho | tự khai khác nguồn cần caveat | 308 tệp/292 nội dung phân biệt; 25 tự khai service có caveat; 16 cặp receipt/run so được không lệch; tách 4 báo cáo chỉ mô tả finding (H8) | Không tìm thêm lỗi trong inventory này |
| Byte verdict | không sửa nguyên văn | 291 receipt hash/byte đúng; 269/269 *-verdict.md có băm chính/lồng khớp; 15 cặp bản phẳng/thư mục bằng byte; cha→head đổi 0 verdict, so master sửa 0 verdict cũ (H3/H11) | Có |
| YAML/ID caveat | parse được, không trùng ID trong receipt | Loader từ chối key trùng: 293 YAML = 291 receipt + supplementary + land; errors=[] (H3) | Có |
| Receipt miễn trừ băm | giữ nguyên v1 đóng băng | 11 ALLOWLIST_CUTOVER + 42 NO_DA_DO: 53/53 băm khớp và byte bằng cả cha lẫn master (H3) | Có |
| t26 riêng | N/N hai số bằng nhau | rc0, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| t27 riêng | N/N hai số bằng nhau | rc0, cùng kết luận 1/1 (H4) | Đạt |
| t138 riêng | N/N hai số bằng nhau | rc0, cùng kết luận 1/1 (H4) | Đạt |
| Xoá hàng README PR526 mới | đo ca nào đỏ | t26 rc0 1/1; t27 rc1 0/1; t138 rc0 1/1 (H5) | Chỉ t27 có răng |
| Xoá caveat PR526 mới | đo ca nào đỏ | cả ba rc0 1/1 (H5) | Cả ba không có răng |
| Xoá hàng supplementary slice-b-c trong README | đo ca nào đỏ | cả ba rc0 1/1 (H5) | Cả ba không có răng |
| Xoá caveat slice-b-c khỏi supplementary YAML | đo ca nào đỏ | cả ba rc0 1/1 (H5) | Cả ba không có răng |
| bien_nhan_v2 tại cay-kho | rc + kết luận | rc0; 238 ĐẠT v2, 11/11 legacy, 42 NỢ, 0 vi phạm/0 KHÔNG ĐO ĐƯỢC, tổng291; TỔNG: ĐẠT (H4) | Đạt |
| land_evidence_nguon tại cay-kho | rc + kết luận | rc0; 47 ĐẠT, 26/28 miễn trừ, 0 vi phạm/0 KHÔNG ĐO ĐƯỢC, tổng73; TỔNG: ĐẠT (H4) | Đạt |
| doctrine-scan tại cay-kho | rc + kết luận | rc0; sạch — đã quét 10 tệp, 0 chỗ chép doctrine (H4) | Đạt |
| doc-claims-check tại cay-kho | JSON ok:true | rc0, stdout parse JSON `"ok": true`, `strict: false` (H4) | Đạt |
| Chưa merge/land | phân biệt Git với quyết định chủ kho | 82359c4/2e4183b→master3e973a0 rc1; 4bc9432/604b8d9 cũng rc1; không lấy ancestry để kết luận landed (H6/H9) | Không báo oan |
| HINT mới | patch -p0 --fuzz=0 trên candidate | dry-run rc0/apply rc0, 10 path tài liệu/receipt v2; ba ca 1/1, bốn gate rc0 và JSON ok=true (H10) | Đã đo trên bản sao |
| Cây gốc cuối | không sửa cay-kho | HEAD/tree giữ nguyên, status gồm ignored rỗng; clone sau hoàn nguyên rỗng (H12) | Có |

## BẢNG SĂN

Mọi script/log nằm ở `review_evidence/`, ngoài cây được review. Các hướng sau ghi output thật, rút gọn phần lặp; dữ liệu đầy đủ ở log/JSON được dẫn. Các lệnh kiểm gốc chạy tại `cay-kho/`, các driver chạy tại thư mục chứa PROMPT.md với `PYTHONDONTWRITEBYTECODE=1`. Chỉ chạy testcase có sẵn; mọi đột biến tài liệu trên clone cục bộ của mirror.git, không đổi mã kiểm tra.

### HƯỚNG 1: Định danh cây và lịch sử

- giả thuyết: checkout sai SHA, shallow hoặc merge base không đúng.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho rev-parse --is-shallow-repository`; `git -C cay-kho show -s --format=%P 1a276a1 77a0a45`; `git -C cay-kho config core.abbrev`; `git -C cay-kho status --porcelain=v1`.
- output: HEAD `1a276a15192013fdb1e472db409133b53ac57944`; tree `8ec1b64d4b399303680723bb99d1619ad43485db`; shallow `false`; cha candidate `77a0a458c6c06f3aafa118953e8e2771daaed911`; cha merge `ff4ab57b11c94e7a3e12df1f8d8d0b202485951f 3e973a03b151e37cd402e0a723816eeaa8247193`; abbrev `7`; status rỗng.
- kết luận: KHÔNG PHẢI LỖI. Không dùng tên nhánh để thay OID.

### HƯỚNG 2: Tái dẫn xuất hint và đối chiếu chèn tay

- giả thuyết: áp thiếu/thừa/sai hint lượt 4.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py history` (rc0). Driver lấy blob tại cha vào `/tmp/pr896-r5-measure-453628b5/hint-parent`, áp `patch --batch --fuzz=0 -p0` rồi so blob và Counter các dòng +/-.
- output thật: `diff.patch`, `diff-pr947.patch`, `numstat.txt`, `numstat-pr947.txt`: cả bốn `byte_match=True`; `hint_paths=34 apply_to_parent_rc=1`; land hunk1 FAILED, README hunk6/hunk7 FAILED; `exact_hint_blob_matches=32` (31 receipt + 1 supplementary mới). Với cả land/README: `missing_hint_lines=0`; land `extra_delta_lines=4` (ghi_chu_luot4); README `extra_delta_lines=4` (hai cặp +/- caveat và mục lục lượt 4). `outside_hint=[ops/reviews/pr896-review-4-codex-verdict.receipt.yaml]`. Commit kế sau77a0a45 chính là candidate.
- kết luận: KHÔNG PHẢI LỖI về việc áp hint. Không thiếu dòng chèn tay nào, các phần thêm ngoài hint đúng lời giao. Các câu gốc còn sót được kiểm riêng. Chi tiết nguyên dòng ở `HƯỚNG 2 - doi chieu hint.log` và `hint-parent-apply.log`.

### HƯỚNG 3: YAML, băm và receipt đóng băng

- giả thuyết: sửa verdict, đổi receipt v1, phá YAML hoặc trùng ID.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py integrity` (rc0); loader YAML từ chối key trùng và đếm ID từng receipt; băm tệp thực, đọc allowlist từ AST nguồn.
- output thật: `yaml_parsed=293 receipts=291 verdict_hashes_match=291 flat_directory_pairs=15`; `ALLOWLIST_CUTOVER=11 NO_DA_DO=42 allowlist_matches=53`; `parent_changed_verdicts=[] master_modified_old_verdicts=[] errors=[]`. Hai supplementary entry có `hash_matches=true`, `readme_rows=1`, `description_matches=true`, `receipt_same_as_parent=true`.
- kết luận: KHÔNG PHẢI LỖI. Cả 53 tệp miễn trừ băm bằng byte cha và master. Supplementary không tự thành receipt/approval mới. Log `HƯỚNG 3 - toan ven.log`, `integrity-details.json`.

### HƯỚNG 4: Kiểm tra bắt buộc tại cây gốc

- giả thuyết: cổng đỏ hoặc xanh mà không chạy đúng ca.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/run_checks.py` (rc0), phóng riêng ba ca và bốn bộ kiểm với cwd `cay-kho/`.
- output thật:

| lệnh | rc | dòng kết luận |
|---|---|---|
| `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t138_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | `238 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 291`; `TỔNG: ĐẠT` |
| `python3 ops/land_evidence_nguon.py --root .` | 0 | `47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73`; `TỔNG: ĐẠT` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | stdout JSON parse được, `"ok": true`, `"strict": false` |

- kết luận: KHÔNG PHẢI LỖI của cổng; ba N/N đều bằng nhau. Có SyntaxWarning `invalid escape sequence '\\d'` ở tệp test, không ảnh hưởng rc. Không có ca báo `Codex home is inside a repository`. Log `.stdout/.stderr/.rc` theo tên bộ kiểm và `checks.json`.

### HƯỚNG 5: Đột biến độc lập trên clone

- giả thuyết: các ca sẵn có bảo vệ đủ hàng README/caveat mới.
- lệnh: `git clone --no-hardlinks --no-checkout <mirror.git> /tmp/pr896-r5-measure-453628b5/copy`; `git -C <copy> checkout --detach 1a276a15192013fdb1e472db409133b53ac57944`; `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/mutations.py` (rc0).
- output thật:

| đột biến (hoàn nguyên giữa từng lượt) | t26 | t27 | t138 |
|---|---|---|---|
| Xoá 1 hàng README PR526 mới, 480 byte | rc0 1/1 | **rc1 0/1** | rc0 1/1 |
| Xoá caveat PR526 mới, YAML còn danh sách rỗng | rc0 1/1 | rc0 1/1 | rc0 1/1 |
| Xoá 1 hàng README supplementary slice-b-c mới, 473 byte | rc0 1/1 | rc0 1/1 | rc0 1/1 |
| Xoá caveat slice-b-c khỏi supplementary YAML, 627 byte | rc0 1/1 | rc0 1/1 | rc0 1/1 |

- output lỗi t27 đúng nguyên nhân: `README.md: caveat 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC' của pr526-review-3-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr526-review-3-codex-verdict.md' ở CỘT 'tệp verdict'`. Mọi ca đã chạy=1, bỏ qua=0; `copy_status_after_restore=` rỗng.
- kết luận: KHÔNG PHẢI LỖI hiện hành của bản vá; ghi rõ giới hạn: chỉ t27 có răng với hàng PR526; t26/t138 không có răng với hàng đó; cả ba **không có răng** với ba đột biến còn lại. Các chốt không chứng minh đủ caveat hay ngữ nghĩa prose. `mutations.json` và 12 log giữ output đầy đủ.

### HƯỚNG 6: Ancestry ngoài trường được hint chọn

- giả thuyết: neo mốc cho một trường đã dọn hết mệnh đề ancestry trong cùng receipt.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py ancestry` (rc0); cho từng OID chạy `git -C cay-kho merge-base --is-ancestor <OID> <target>` với target `101263f`, `2e4183b`, master `3e973a0` và candidate.
- output thật: `old_23_receipts=23 checks=92 all_rc0=True`; `historical_receipt_anchors_exist=22/22`; `residual_unanchored_fields=7`. Bảy trường nêu ở finding đều rc(master,candidate)=[0,0]. Riêng chuỗi ci-windows: 2d8b4fb/7e2ef2e/4bc35d3/a45c8dc→master,candidate đều rc1; **chỉ c2f6898 rc0**, nên bác chính mệnh đề phủ định áp lên c2f6898, không nói cả năm đã vào master. `4bc9432` và `604b8d9` đều rc1 với master/candidate; `82359c4` và `2e4183b` rc1 với master, rc0 với candidate.
- kết luận: **LỖI P1**, giữ slug cũ `phu-nhan-ancestry-chi-tren-nhanh-da-cu`. Không kết luận land/authority/assurance từ phép đo này. Tệp `ancestry-details.json` chứa đủ OID, câu và rc.

### HƯỚNG 7: Quét trạng thái chưa review ngoài tám receipt

- giả thuyết: mọi cảnh báo chưa review đã có mốc lịch sử và verdict kế tiếp.
- lệnh: quét YAML scalars đệ quy (gồm `mo_ta` và `noi_dung`) cùng README/land; `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py reviews` (rc0); đọc phần đối chiếu trong bốn verdict #870/#889 lượt 2/3.
- output thật cuối: `old_review_caveats_historically_anchored=8 all_next_sha_and_hash_match=True`; tám verdict kế tiếp `cat-file -e <historical-anchor>:<verdict>` đều rc128, chưa tồn tại ở snapshot. PR870 lượt2/3 cùng `06a50c5feea77c2654f31edd26efeed7eeee62f5`, approve, băm khớp; PR889 lượt2/3 cùng `094e8d17ae4dfcf21dca63702c9262267bdc072c`, approve, băm khớp. PR870 verdict lượt2:13/20 ghi P2 đã vá thật cả hai vị trí; PR889 lượt2:7 ghi đã đo cả câu sửa thêm. Trong khi đó hai receipt lượt1 và README:704/710/1046/1047 vẫn phủ nhận review.
- kết luận: **LỖI P1**, giữ slug cũ `trang-thai-chua-review-da-bi-verdict-sau-bac`; tám thể hiện cũ đã đóng, lớp còn hai thể hiện. Không biến receipt lượt1 thành approve/cross_approved. Dữ liệu cuối ở `review-states.json` và `review-states-run.stdout`; bản nhật ký tăng dần ghi cả lần đầu parser chỉ đọc mo_ta (2 hàng) và lần đầu regex không nhận bullet/backtick, đã chỉnh thước đọc để đo đủ, không coi hạn chế parser là finding kho.

### HƯỚNG 8: Tự khai surface, kể cả cuối verdict

- giả thuyết: còn tự khai service trái run/receipt ngoài hai thể hiện lượt4.
- lệnh: `rg -n -i 'codex.service|service/api|execution.surface|bề mặt|surface:' cay-kho/ops/reviews --glob '*-verdict.md' --glob 'VERDICT.md'`; `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/surfaces.py` (rc0); đọc các đoạn tự khai và caveat.
- output thật: `verdict_files=308 distinct_content=292`; `run_json_files=47 parse_errors=[]`; `receipt_runtime_pairs=16 surface_mismatches=[]`; `service_self_claims=25 missing_caveat=[]`. Với 15 caveat thiếu runtime: dòng tự khai khớp, run ID được nhắc khớp receipt/nguồn v1, mỗi hàng README đúng một lần và đúng toàn mô tả; `matching_runtime_files=[]` cho cả 15. Sáu tự khai có run bác service đã có đính chính; bốn ci-g5 có caveat runtime không đo được. PR896 lượt2/3/4 và PR915 lượt1 chỉ nhắc chuỗi khi mô tả finding. Những câu API/shell chung không tự chứng minh một surface khác CLI; `claude_code_subagent` có giải thích chế độ subagent trong receipt, không tự kết tội khác nền.
- kết luận: KHÔNG PHẢI LỖI mới được chứng minh ở lớp surface; hai thể hiện P2 cũ đã đóng. Không chọn surface thực tế cho các run thiếu nguồn. `surfaces.json`, `surface-text.log` giữ inventory/câu đầy đủ.

### HƯỚNG 9: Đo mốc trong chính câu mới của bản vá

- giả thuyết: chèn đầy đủ hint nhưng neo sai OID/kết luận/commit áp.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/claims.py` (rc0); `git show` đọc receipt/land tại bốn mốc; so +/- hint lượt2/lượt3 với delta thực; đọc ba verdict #896 lượt2/3/4.
- output thật: `previous_verdict_supplied_equals_flat_and_directory=true`; `previous_hint_supplied_equals_stored_artifact=true`; verdict lượt4 `39386` byte, sha256 `7357b499ae543c7e80feebae18495e46ce819a3bff5fd3f25cbccb9933e357e8`, khớp receipt. Hai phép `hint_at_82359c4`/`hint_at_2e4183b` có `missing_plus_minus_lines=[]`, cha lần lượt578fb4b/c8c1ee0. Mốc8879165/c8c1ee0 có ID HINT-LUOT3-CHUA-AP; ff4ab57/77a0a45 có HINT-LUOT4-CHUA-AP. Hàng README mới lượt3:1055, lượt4:1056; hai caveat đều đúng1 hàng và same_description=true. Delta receipt lượt4 `2\t2`; commit kế sau77a0a45 là full candidate OID. Land mới measured_at_sha2e4183b dẫn đúng kết luận lượt2 về P2 t162/hai thể hiện P1 và lượt3 về pr889 lượt1.
- kết luận: KHÔNG PHẢI LỖI mới tại các câu bản vá đã viết. Giữ câu lịch sử riêng với trạng thái candidate; lỗi các trường khác ghi H6/H7. `claims.json`/`claims-run.stdout` giữ từng khẳng định.

### HƯỚNG 10: Gợi ý vá kiểm trên bản sao đúng SHA

- giả thuyết: HINT mới không áp sạch, đổi nhầm lịch sử/v1 hoặc phá cổng.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py` (rc0); tại clone candidate chạy `patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>` rồi áp và chạy lại đúng ba ca/bốn cổng.
- output thật: `changed_files=10; verified_verdict_hashes=291`; dry-run rc0, apply rc0, không FAILED/fuzz/offset; chỉ 9 receipt v2 và README. t26/t27/t138 đều rc0 `1/1 đạt; đã chạy=1, bỏ qua=0`; bien_nhan_v2 rc0 `238 ĐẠT v2 · 11/11 legacy · 42 NỢ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng291`, TỔNG ĐẠT; land rc0 `47 ĐẠT · 26/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng73`, TỔNG ĐẠT; doctrine rc0 sạch10tệp/0chỗ; doc-claims rc0 JSON ok=true. YAML sửa parse được, không trùng ID; mô tả caveat/readme khớp; clone sau hoàn nguyên status rỗng.
- kết luận: KHÔNG PHẢI LỖI của HINT theo các phép đo. Gợi ý neo bảy trường còn sót và hai hồ sơ chưa review vào mốc cũ, thêm kết quả hiện tại; không sửa verdict/v1/mã test, không nâng assurance. `HINT.patch` **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Log `hint-dry-run.stdout` và `hint-results.json`.

### HƯỚNG 11: Băm lồng của các verdict được dẫn

- giả thuyết: chỉ kiểm receipt chính bỏ băm nested ci-windows lượt1–4.
- lệnh: quét đệ quy `verdict_sha256` trong 291 receipt; SHA-256 mọi `*-verdict.md`; `git -C cay-kho diff --name-only 77a0a45 1a276a1 -- 'ops/reviews/*-verdict.md'`.
- output thật: `all_star_verdict_md=269 hash_covered=269`; `untouched_star_verdict_md_parent_to_candidate=True`. Chi tiết `all-verdict-hashes.json`.
- kết luận: KHÔNG PHẢI LỖI về byte của mọi verdict phẳng liên quan. Không gọi mọi bản phụ `VERDICT.md` trong thư mục là bản nguyên byte của verdict phẳng: 15 cặp đã kiểm riêng theo path receipt; một số bản khác là artifact khác và không được phép suy hash qua tên.

### HƯỚNG 12: Giữ nguyên cây giao review

- giả thuyết: kiểm tra/hint làm bẩn cây gốc.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored=matching`; status clone sau hoàn nguyên.
- output thật: HEAD/tree như H1, status gốc rỗng cả ignored; status clone rỗng. HINT 30930 byte, SHA256 `9c400529c2a4026be3049b9b3494221c9961c662d5768b3769a5687cdf52daff`.
- kết luận: KHÔNG PHẢI LỖI. `final-state.json` giữ kết quả; không sửa `cay-kho/`.

## FINDING

### phu-nhan-ancestry-chi-tren-nhanh-da-cu [P1] Bảy receipt còn mệnh đề ancestry hiện hành ở trường ngoài hunk

TỆP/DÒNG (đều trong `ops/reviews/`):

| receipt | trường/dòng | OID neo verdict | rc master / candidate |
|---|---|---|---|
'''
for x in ancestry['residual']:
    text+='| `'+x['receipt']+'` | `'+x['field']+'`, '+str(x['line'])+' | `'+x['oid']+'` | '+ '/'.join(str(v) for v in x['ancestor_rc'].values())+' |\n'
text+='''
VẤN ĐỀ: `1a276a1` đã neo lịch sử `anchor.mo_ta`, nhưng bỏ `anchor.gioi_han` của ba doctrine-scan, hai wp538 và wp540. Các trường còn nguyên “mo neo **hien chi la mot nhanh**”; wp538 lượt1 và wp540 còn trực tiếp nói “**khong phai to tien ... master**”. WP538 lượt1 còn suy “Nhanh xoa duoc va SHA se thanh khong tra duoc”. Cùng receipt hiện có một trường nhận ancestor đã có và một trường tiếp tục phủ nhận như hiện hành. Câu đính chính trong trường bên cạnh không gắn mốc cho chính `gioi_han` tự khai “hiện”. Ci-windows bỏ sót `chuoi_verdict_ghi_chu:70` nói cả năm verdict “KHONG phai to tien cua master”, còn ghi phép đo c2f6898→origin/master là KHONG, trong khi chính c2f6898→master ghim và candidate đều rc0. Không báo “CHUA land” đơn lẻ là sai, cũng không nói bốn OID còn lại đã vào master.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py ancestry` ⇒ rc0; **14/14** phép đo cho bảy hàng với master `3e973a03b151e37cd402e0a723816eeaa8247193` và candidate đều rc0, trái câu hiện hành. `ancestry-details.json` lưu nguyên scalar/dòng/OID và cả năm OID ci-windows. Ba ca/bốn gate tại candidate vẫn xanh (H4), nên chúng không có răng về các mệnh đề sai này. Các trường tồn tại từ trước bản vá; không gọi đây là regression do executor chèn tay.

GỢI Ý VÁ: gắn chính bảy scalar còn sót vào commit ghi receipt, ghi phép đo mới trên hai exact OID, giữ cường độ/assurance và phân biệt landed. `HINT.patch` có đủ bảy hunk, dry-run sạch; không đụng byte verdict/v1.

ĐỘ TIN: cao.

### trang-thai-chua-review-da-bi-verdict-sau-bac [P1] Hồ sơ lượt 1 của PR870 và PR889 vẫn phủ nhận hai lượt review đã có

TỆP/DÒNG:

| receipt trong ops/reviews/ | trường assurance | caveat HEAD-MERGE-CHUA-REVIEW-LAI | README cảnh báo / mục lục | SHA đã review lại |
|---|---|---|---|---|
| `pr870-review-1-codex-verdict.receipt.yaml` | 27 | 97 | 704 / 1046 | `06a50c5feea77c2654f31edd26efeed7eeee62f5` |
| `pr889-review-1-codex-verdict.receipt.yaml` | 28 | 104 | 710 / 1047 | `094e8d17ae4dfcf21dca63702c9262267bdc072c` |

VẤN ĐỀ: assurance ghi “head da merge ... KHONG duoc review lai”; caveat PR870 nói “Khong co luot review nao tren 06a50c5”, PR889 nói head094e8d1 “KHONG duoc review lai”. Hai hàng cảnh báo đang hiệu lực và hai hàng mục lục lặp lại câu đó, không có mốc lịch sử. Tại exact candidate đã có `pr870-review-2` **và** `pr870-review-3` review đúng full06a50c5, cũng có `pr889-review-2` **và** `pr889-review-3` review đúng full094e8d1; cả bốn verdict approve, băm khớp receipt. Verdict lượt2 còn đọc và kết luận rõ bản vá P2/câu sửa thêm. Đây là cùng lớp P1 lượt4: tám thể hiện được nêu đã đóng, còn hai receipt ngoài danh sách ấy. Không sửa kết quả/assurance lịch sử của lượt1 chỉ vì lượt sau approve.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py reviews` ⇒ rc0; bốn `matches_oid=true`, `hash_matches=true`, verdict=approve. Đọc `pr870-review-2-codex-verdict.md:13` và bảng đối chiếu:20; `pr889-review-2-codex-verdict.md:7`. Quét ngược commit ghi receipt đầu tiên (`600b6ce`/`e02d0c3`): verdict lượt1 tồn tại rc0, lượt2/3 chưa có rc128, nên có mốc lịch sử kiểm được để bảo toàn lời cũ. Ba ca và bốn gate gốc vẫn xanh; chúng không bắt được ngữ nghĩa chưa-review này. Chi tiết từng scalar/hàng ở `review-states.json`.

GỢI Ý VÁ: neo cả assurance, caveat, hàng cảnh báo và mục lục vào commit ghi receipt cũ, dẫn hai verdict kế tiếp và exact SHA; giữ kết quả/băm/assurance lượt1. `HINT.patch` sửa đủ hai receipt + bốn hàng README, dry-run sạch và kiểm sau áp xanh. Không sửa byte verdict đã băm.

ĐỘ TIN: cao.

## PHỤ LỤC ĐO THEO TỪNG THỂ HIỆN

23 dòng dưới là các phép đo trong câu đã được hint lượt4 neo mốc. Mỗi dòng chạy `git merge-base --is-ancestor <OID> <target>` với target theo thứ tự101263f / 2e4183b / master3e973a0 / candidate1a276a1; rc0 là quan hệ tồn tại. Bảng này xác nhận phép đo, không che bảy trường còn sót đã báo.

| receipt trong ops/reviews/ | OID | rc bốn target |
|---|---|---|
'''
for x in ancestry['patched']:
    text+='| `'+x['receipt']+'` | `'+x['oid']+'` | '+ '/'.join(str(v) for v in x['ancestor_rc'].values())+' |\n'
text+='''
Tám caveat chưa-review cũ: SHA dưới được đối chiếu cả receipt lẫn header/bullet của verdict kế tiếp và SHA256 tệp verdict, đều đúng; tất cả có mốc receipt tồn tại và README nhận đủ dòng hint.

| receipt cũ trong ops/reviews/ | verdict kế tiếp | full reviewed_sha kế tiếp |
|---|---|---|
'''
for x in reviews['old_eight']:
    text+='| `'+x['receipt']+'` | `'+x['next_verdict']+'` | `'+x['next_reviewed_sha']+'` |\n'
text+='''
15 caveat thiếu runtime (13 cũ + 2 lượt4): mỗi dòng có đúng dòng tự khai, ID được nhắc khớp nguồn, **0 run.json** đúng ID trong47run hiện có, đúng1hàng README chứa nguyên mô tả. Đây là đối chiếu hai lời khai; không chọn surface thực tế.

| verdict trong ops/reviews/ | dòng tự khai | ID khai trong nguồn |
|---|---|---|
'''
for x in surfaces['service_self_claims']:
    c=x['condition']
    if c:
        text+='| `'+x['verdict']+'` | '+str(c['declared_line'])+' | '+', '.join('`'+str(i)+'`' for i in c['run_ids'])+' |\n'
text+='''
## GIỚI HẠN VÀ HIỆN VẬT

- `VERDICT.md` được tạo `dang_lam` ngay từ đầu và nối sau mỗi hướng; nhật ký tăng dần trước khi sắp lại báo cáo cuối giữ ở `review_evidence/VERDICT.progress.md`. Các số/kết quả ở báo cáo cuối lấy từ phép đo cuối đã đọc đúng cả mo_ta/noi_dung và các dạng header; log thử thước ban đầu không được dùng làm kết luận về kho.
- Chỉ xác minh dữ liệu/lịch sử Git và hiện vật được giao, không chứng nhận GitHub hiện hành hoặc context/runtime bị lược khỏi kho. Những ID không có run.json không được coi là đã đo runtime. Không tự đặt tên execution surface cho phiên review này.
- `HINT.patch` là artifact gợi ý từ clone, định dạng `patch -p0`, dry-run `--fuzz=0` sạch trên exact candidate; chưa áp vào `cay-kho/`, không có quyền merge/land. Nợ độ phủ ca có sẵn được ghi như giới hạn, không nâng riêng thành finding sản phẩm.
- HEAD/tree và cây gốc giữ nguyên; mọi hiện vật mới ở thư mục chứa PROMPT.md hoặc `/tmp` ngoài kho được review. Không gọi mạng/push, không viết testcase hay sửa mã cổng.
'''
dest.write_text(text)
print('VERDICT_bytes='+str(len(text.encode()))+' lines='+str(len(text.splitlines())))
