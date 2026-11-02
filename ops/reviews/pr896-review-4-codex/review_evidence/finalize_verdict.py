from pathlib import Path
import json
import re
import yaml

base = Path(__file__).resolve().parents[1]
root = base / 'cay-kho'
p = base / 'VERDICT.md'
progress = p.read_text()
if not progress.startswith('verdict: dang_lam\n'):
    raise RuntimeError('Already finalized')
states = json.loads((base / 'review_evidence/proven-states.json').read_text())

def node_at(node, path):
    for key in path:
        if isinstance(node, yaml.SequenceNode):
            node = node.value[key]
        else:
            node = next(v for k, v in node.value if k.value == key)
    return node

def lineno(rel, path):
    return node_at(yaml.compose((root / rel).read_text()), path).start_mark.line + 1

prefix = '''verdict: changes_requested
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
'''

body = progress.split('## NHẬT KÝ TĂNG DẦN', 1)[1]
findings = '''

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
'''
for item in states['review']:
    findings += f"| `{item['receipt']}` | {item['line']} | `{item['next_verdict']}` / `{item['next_reviewed_sha']}` |\n"
findings += '''
VẤN ĐỀ: Các mô tả “BAN VA CHUA duoc review”/“CHUA duoc cross-review lai” thiếu mốc ngay tại câu đang được nâng thành cảnh báo có hiệu lực. Những review tiếp theo đã nằm trong candidate và thực sự đối chiếu bản vá. PR455 các lượt sau có cả kết quả vá thật, vá hờ và finding mới; bất kể đóng đến đâu, “chưa được review” không còn đúng. PR896 lượt2 dòng7 đóng P2 t162; dòng8 xác nhận hai thể hiện P1 của #915 đã đóng, còn sót một thể hiện khác; lượt3 dòng6 đóng nốt thể hiện đó. Không gọi toàn bộ verdict cũ là approve và không kết luận đã có review sạch cho toàn ứng viên hiện nay.

ĐÃ THỬ NGHIỆM: `state_audit.py` đo đủ 8 cặp receipt→verdict, đọc phần đối chiếu của từng verdict; `proven-states.json/log` lưu ID, commit ghi receipt, exact reviewed SHA kế tiếp và nguyên ba hàng mục lục mới nhất. Hash các verdict này khớp receipt (H5); t26/t27/t138 và bốn gate không phát hiện trạng thái cũ (H6/H8).

GỢI Ý VÁ: neo mô tả từng caveat vào commit ghi receipt và dẫn lượt review tiếp theo, đồng bộ README; bổ sung ghi chú lịch sử cho khối land cũ. HINT sửa đúng 8 receipt, các hàng liên quan và nối ghi chú land. Không xoá kết quả review cũ. Chưa có ca sẵn có đối chiếu ngữ nghĩa này; cần ca đọc mốc/cặp verdict kế tiếp, đột biến bỏ mốc và phục hồi lời khai hiện hành “chưa review” phải đỏ. Nguy cơ là gộp “đã review” với “đã đóng toàn lớp/approve”; hint giữ ranh giới ấy.

ĐỘ TIN: cao.

### phu-nhan-ancestry-chi-tren-nhanh-da-cu  [P1]  Hai mươi ba receipt còn phủ nhận quan hệ Git đã có trên master

TỆP/DÒNG: bảng dưới là vị trí trường chứa mệnh đề sai tại candidate. OID đầy đủ và hai mã thoát có trong `review_evidence/proven-states.json/log`.

| receipt trong ops/reviews/ | dòng trường | OID đo ancestry |
|---|---|---|
'''
for item in states['ancestry']:
    rel = 'ops/reviews/' + item['receipt']
    name = item['receipt']
    d = yaml.safe_load((root / rel).read_text())
    if item['schema'] == 1:
        path = ['truy_xuat_ghi_chu']
    elif name.startswith('wp678-spec-'):
        idx = next(i for i,c in enumerate(d['verdict_usage_caveats']) if c['id']=='REVIEWED-SHA-CHI-TREN-NHANH-SPEC')
        path = ['verdict_usage_caveats',idx,'mo_ta']
    elif name.startswith(('doctrine-scan-','wp538-','wp540-')):
        path = ['anchor','mo_ta']
    else:
        path = ['anchor','gioi_han']
    findings += f"| `{name}` | {lineno(rel,path)} | `{item['oid']}` |\n"
findings += '''
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
'''
for q in sorted((root / 'ops/reviews').glob('*.receipt.yaml')):
    d = yaml.safe_load(q.read_text())
    for c in d.get('verdict_usage_caveats') or []:
        if c.get('id') != 'SURFACE-TU-KHAI-KHAC-RECEIPT-RUNTIME-CHUA-DO-DUOC':
            continue
        line = re.search(r'Verdict dong (\d+)',c['mo_ta'])[1]
        run_id = re.search(r'run ID khai ([0-9a-f]+)',c['mo_ta'])[1]
        findings += f"| `{Path(d['verdict_path']).name}` | {line} | `{run_id}` |\n"

findings += '''

## GIỚI HẠN VÀ HIỆN VẬT

- Các kết luận trên neo đúng candidate đã ghi đầu tệp; không dùng tên nhánh để thay SHA. Không gọi mạng nên không chứng thực trạng thái GitHub hiện hành, chỉ đối chiếu dữ liệu/lịch sử Git được giao.
- Không viết lại testcase hay mã sản phẩm; chỉ chạy ca có sẵn và đột biến tài liệu/receipt trên clone ngoài cay-kho. Kết quả mất caveat sống sót được ghi là giới hạn của chốt, không gán thành lỗi sản phẩm chưa được chứng minh.
- `HINT.patch`: gợi ý tài liệu/biên nhận đã dry-run --fuzz=0 và kiểm trên clone; **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Tệp không có tác dụng đổi verdict của candidate. Tài liệu bổ sung legacy không phải receipt mới hay quyền approval.
- Mọi phép đo đã nêu có log/script ở `review_evidence/`; không yêu cầu tái chạy các driver cũ chứa đường dẫn sandbox đã mất. Snapshot/stream đã OMITTED và attestation runtime ngoài tệp lưu không được coi là tự đo lại.
'''
p.write_text(prefix + body + findings)
print('finalized',p,'bytes=',p.stat().st_size)
