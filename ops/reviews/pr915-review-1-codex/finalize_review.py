from pathlib import Path
import re
p=Path('VERDICT.md');s=p.read_text()
assert Path('review-evidence/final_integrity.log').is_file(), 'final snapshot still running'
assert 'rc=0\n' in Path('review-evidence/final_integrity.log').read_text()
rows=[
('Neo đối tượng','HEAD 2789cbb…; base 50a59a9','`review_probe.py preflight` (H1): HEAD đầy đủ, tree=6f299d7f70269ec32522fc4ea28c9d2d70c5424b; base=50a59a945026a2ab2f97dc0e7ef7b5a540e17652','Có'),
('Nguồn diff và cây đầy đủ','diff.patch/numstat tại head được giao','H1: `git diff`/`--numstat` khớp từng byte; is_shallow=false; core.abbrev=7; status rỗng','Có'),
('Phạm vi ba commit','3bc4244 sửa CLAUDE; 7cfe062 hiện vật; 2789cbb biên nhận/README','`review_probe.py provenance` (H4): lần lượt 1, 91, 4 tệp; danh sách đầy đủ ở review-evidence/*-numstat.txt','Có'),
('t162 đọc từ workflow','Chỉ output os của chuan-bi','`review_probe.py static_scope` (H14): `raw_expr = wf_data["jobs"]["chuan-bi"]["outputs"]["os"]`; H8: đổi exclude/needs/if đều t162 PASS','Có'),
('t162 đánh giá ngữ cảnh thật','push/PR thường/PR windows/từng runner_set','`review_probe.py workflow` (H8): chạy nguyên t162 trên bản sao workflow baseline PASS; bỏ nhánh windows-only ⇒ FAIL với kết quả hai OS','Có, cho các ngữ cảnh ca assert; không thay việc đọc từng job'),
('Phân biệt output os với ma trận job','t162 không đọc exclude/if cấp job','H8: 6/6 đột biến độc lập ở hai job vẫn t162 PASS; H14 xác minh các chỗ đọc workflow trong AST','Có'),
('Chốt G5 kiểm exclude','Mảnh/gom có chốt riêng','H8: bỏ exclude của gate-cong-cu hoặc gate-cong-cu-gop ⇒ loi_g5_workflow báo matrix sai','Có'),
('Chốt G5 kiểm needs/if','Hai job mảnh/gom bị ghim needs/if','H8: lần lượt bỏ needs/if ở từng job ⇒ 4/4 lỗi đúng thông điệp; baseline không lỗi','Có'),
('Phạm vi gate-cong-cu*','Phần mảnh/gom được kiểm','H8: tại SHA này prefix chỉ có [gate-cong-cu, gate-cong-cu-gop], khớp hai hằng JOB_G5_MANH/GOP','Có; không suy cho mọi gate* hay job thêm trong tương lai'),
('t161','Chỉ kiểm cấu trúc, không đánh giá biểu thức','H14: t161 PASS; AST có 0 lời gọi evaluator; mã kiểm nguồn matrix.os và output fromJSON','Có'),
('Bản phẳng #870','79752 byte; sha256 8b222ab3…','`review_probe.py receipts` (H2 đo lại): 79752; hash đầy đủ 8b222ab37b7de41499829abb52d1958043ee8fd2969212596277aacc211026a6; flat==original','Có'),
('Bản phẳng #889','34167 byte; sha256 c5fe298a…','H2 đo lại: 34167; c5fe298af73bb6081ecf44638b7fce7e7dd220c11c3ddcee5ba5fcc234a4b612; flat==original','Có'),
('Bản phẳng #896','63341 byte; sha256 3feaad3e…','H2 đo lại: 63341; 3feaad3e207ae2dea5323cb6f831ba2980546ec1d3febeead6d415baccbbb803; flat==original','Có'),
('Ba reviewed_sha/tree/base','06a50c5/0fa694d/9e9a74b; 094e8d1/55f5edf/e63961f; 816f439/3da0ce2/1ccc314','H2 đo lại: đầy đủ OID khớp verdict, run.head, git rev-parse tree; diff/numstat của từng thư mục khớp git diff base..reviewed_sha','Có; OID đầy đủ ở output H2'),
('Head đã merge của ba PR','Reviewed SHA là parent thứ hai của 5f288ea/6ac385f/27dcc3b','H2 đo lại: `git rev-parse <merge>^2` khớp từng reviewed_sha','Có, từ Git cục bộ'),
('Kết quả và so_p* #870/#889','#870 approve 0/0/0/0; #889 approve 0/0/0/0','H2 đo lại: dòng 1/dòng Kết quả và cả bốn số trong từng receipt khớp','Có'),
('Kết quả và so_p* #896','changes_requested 0/0/1/0; finding t162-khong-khoa-toan-bo-ma-tran-job','H2 đo lại: dòng Kết quả và receipt đều 0/0/1/0; finding và HINT nằm trong hiện vật','Có; đây là số lịch sử, khác finding của lượt #915 này'),
('SHA256SUMS ba thư mục','Các hiện vật nguyên vẹn','`review_probe.py hashes` (H3): `sha256sum -c SHA256SUMS` rc=0 cả ba; 31/22/32 OK; không tệp bỏ sót ngoài manifest tự thân','Có'),
('evidence_url','Neo commit 7cfe062, chỉ mang hiện vật','H4: 7cfe06212cb43f92d5753940116079e671d9c385; 91 tệp đều nằm trong ba thư mục hoặc ba bản phẳng, 0 receipt; URL blob khớp byte verdict','Có; đối chiếu Git offline, không gọi URL'),
('Launcher version/rc/state','1.5.0; ma_thoat 0; xong; worktree_sach true','`review_probe.py run_metadata` (H5): cả ba trường khớp run.json; run ID khớp session_run_id','Có cho metadata đã lưu'),
('Thời lượng launcher','496.137; 380.787; 712.54 giây','H5: số trong receipt khớp run.json; hiệu timestamp tương ứng 496.137080; 380.787461; 712.539633','Có trong sai số làm tròn 0.001 giây'),
('Băm PROMPT.md','2c58af0d…; 00773f21…; 27dbb858…','H5: sha256 thực ba PROMPT.md khớp đầy đủ prompt_sha256 trong run.json và tiền tố trong ghi chú','Có; hash đầy đủ ở H5'),
('stdout/checkpoint','Metadata run neo hiện vật','H5: stdout_byte/stdout_sha256/checkpoint_sha256 đều khớp byte tệp trong thư mục','Có'),
('14 dòng đầu stderr','Lưu header; full log 1287629/2085807/1076780 byte không vào kho','H5: ba header đều 14 dòng, v0.163.0/model/effort/session khớp sidecar; stderr_byte trong run.json đúng ba số','Đo được header/metadata; hash/byte full stderr không kiểm lại được vì thiếu log đầy đủ'),
('Assurance','cross_reviewed; KHÔNG cross_approved vì không khoá model','H5: recursive model_keys=[] cả ba run.json; header tự khai gpt-6.1-sol/xhigh; receipt để model_da_chay KHONG_DO_DUOC','Có về giới hạn bằng chứng; không xác nhận backend model'),
('Bề mặt tự khai trong hai verdict','#870/#889 codex_service; #889 còn nói không chạy qua codex exec','`review_probe.py identity_claims` (H11): launcher + receipt + header CLI mâu thuẫn câu tự khai; không caveat nói codex_service','KHÔNG — một P1, hai hiện vật review'),
('Surface đối chứng #896','codex_cli','H11: VERDICT.md:7, run.json:47 và receipt.surface đều codex_cli','Có'),
('Hai snapshot gốc #870','672374 byte mỗi tệp; cùng hash 5b88623b…; KHÔNG vào kho','`review_probe.py snapshot_caveats` (H6): không tracked snapshot; hash đầy đủ chỉ xuất hiện ở README/receipt, không có byte artifact để băm','KHÔNG ĐO ĐƯỢC hash/kích thước/đẳng nhất gốc; caveat đã khai rõ vắng, không tính thêm finding'),
('P2-DA-VA-CHUA-REVIEW-LAI','Đã áp nguyên hint ở 3bc4244','`review_probe.py patch_history` (H7): patch -p0 --fuzz=0 rc=0 trên blob parent trong /tmp; kết quả đúng byte 3bc4244 và HEAD','Có về bản vá; “chưa review lại” là lời khai lịch sử, không chứng minh vắng review bên ngoài bằng Git'),
('14 caveat + 3 hàng mục lục','17 hàng README mới','`review_probe.py index_claims` (H12): 5/4/5 caveat + mỗi verdict 1 hàng; 14 mô tả khớp nguyên nội dung receipt','Có với các caveat đã khai; còn thiếu caveat P1 của H11'),
('Mỏ neo và lời khai con người','Ancestry cũ, người giao việc/submitter/session executor theo (b)','H2/H4 đo được ancestry và commit; không có raw conversation/audit để độc lập xác minh người chỉ thị, ai viết verdict hay tính độc lập thực tế','Phân biệt lời khai và Git; không nâng thành đo máy'),
('Cổng bien_nhan_v2','Đạt','`review_probe.py mandatory_gates` (H9): rc=0; 232 ĐẠT v2, 11/11 legacy, 42 nợ, 0 vi phạm/không đo được, tổng 285; TỔNG: ĐẠT','Có'),
('Cổng doctrine-scan','Sạch','H9: rc=0; quét 10 tệp, 0 chỗ chép doctrine','Có'),
('Cổng doc-claims-check','ok=true','H9: rc=0; JSON "ok": true; raw stdout/stderr lưu ở review-evidence/gate-2.*','Có'),
('t26/t27/t138','Gọi riêng từng hàm phải đạt','`review_probe.py required_cases` (H10): mỗi hàm chạy riêng trong subprocess, rc=0 và dòng DAT','Có; t138 là ca receipt admission trên kho giả, không phải đo model identity'),
('Quét bí mật ba thư mục','Sạch','H10: python3 scripts/pkg_secret_scan.py ops/reviews/<từng thư mục>, rc=0, stdout/stderr rỗng cả ba','Có theo bộ mẫu scanner'),
('HINT.patch mới','Caveat sửa surface, giữ nguyên các verdict','`python3 build_hint.py` (H13): dry-run/apply -p0 --fuzz=0 rc=0; t26/t27 đạt trên bản sao; bỏ từng cảnh báo ⇒ t27 FAIL đúng ID','Có trên bản sao; chưa áp trên cây thật'),
('Checkout cuối lượt','Chỉ đọc cay-kho/','`review_probe.py final_integrity` (H15): snapshot cả .git/content/mode/symlink trước/sau bằng nhau, status kể cả ignored rỗng; HEAD/tree giữ nguyên','Có; không gọi mạng/push'),
]
header='| khẳng định | PR khai | đo được (lệnh) | khớp? |\n|---|---|---|---|\n'
table=header+''.join('| '+' | '.join(x.replace('|','\\|') for x in row)+' |\n' for row in rows)
assert header in s;s=s.replace(header,table,1)
s=s.replace('verdict: dang_lam\n','verdict: changes_requested\n',1)
s=s.replace('reviewed_sha: 2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f\n','reviewed_sha: 2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f\nKết quả: 0 P0, 1 P1, 0 P2, 0 P3.\n',1)
s=s.replace('Đang đo độc lập tại SHA chỉ định; chỉ đọc cay-kho/, mọi bản đột biến nằm ngoài cây.', '''Đã đo độc lập tại exact SHA chỉ định, tree `6f299d7f70269ec32522fc4ea28c9d2d70c5424b`; base `50a59a945026a2ab2f97dc0e7ef7b5a540e17652`. Một lớp P1, hai hiện vật review: tự khai sai bề mặt chạy trong verdict #870/#889, chưa đính chính qua caveat. Câu sửa CLAUDE.md, byte/băm/OID/số P của ba biên nhận và mọi cổng được yêu cầu đều khớp.

Reviewer: codex; provider: openai_codex; transport: machine/tool-mediated. Execution surface/model của chính lượt này: KHÔNG ĐO ĐƯỢC độc lập từ hiện vật launcher được giao; phiên có công cụ shell, không suy danh tính backend từ tên agent. Review theo chỉ thị trực tiếp của chủ kho, không packet/lease, chỉ đọc cay-kho/. Không tự cấp assurance/approval/land. Các blob lịch sử chỉ dùng đối chiếu nguồn mà receipt đang khai; workflow hiện hành luôn lấy ở HEAD được giao.

Mọi hướng được nối vào báo cáo sau khi chạy. H2 lần đầu rc=1 do helper giả định base/tree phải là dòng YAML riêng; verdict #896 ghi chúng trong văn xuôi. Đã sửa helper ngoài checkout và đo lại trọn ba biên nhận thành công; giữ cả transcript lần đầu để không che lỗi phép đo. Đây không phải lỗi repository. Hai SyntaxWarning của Python 3.13 ở docstring test có sẵn, không làm các ca thất bại.

Lệnh tái lập các hướng từ thư mục giao việc: `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py <tên-hướng>`. Script chạy các cổng từ cay-kho/, đặt TL_CACHE_DIR ở review-evidence/cache, tắt bytecode và GIT_OPTIONAL_LOCKS. Bảng H2/H5 giữ đầy đủ SHA; toàn bộ stdout cổng dài nằm ở review-evidence/.''',1)
s+='''

## Kết luận kiểm tra bắt buộc

| Lệnh (cwd cay-kho/) | rc | Dòng kết luận thật |
|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | 0 | `bien_nhan_v2: 232 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 285`; `TỔNG: ĐẠT` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | JSON `"ok": true` |
| Gọi riêng `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi()` | 0 | `DAT (goi rieng ham)` |
| Gọi riêng `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()` | 0 | `DAT (goi rieng ham)` |
| Gọi riêng `t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR()` | 0 | `DAT (goi rieng ham)` |
| `python3 scripts/pkg_secret_scan.py ops/reviews/pr870-review-2-codex` | 0 | stdout/stderr rỗng; không phát hiện |
| `python3 scripts/pkg_secret_scan.py ops/reviews/pr889-review-2-codex` | 0 | stdout/stderr rỗng; không phát hiện |
| `python3 scripts/pkg_secret_scan.py ops/reviews/pr896-review-1-codex` | 0 | stdout/stderr rỗng; không phát hiện |

Đã kiểm HINT trên bản sao, không áp vào cay-kho/. Snapshot cuối xác nhận nguồn và .git không đổi. Hai snapshot gốc #870 và full stderr lịch sử vắng khỏi kho: không xác nhận hash/byte của dữ liệu không được giao. Các giới hạn ấy đã được caveat công khai; finding yêu cầu sửa ở lượt này chỉ là mâu thuẫn surface chưa được đính chính.
'''
p.write_text(s)
print('final_verdict=changes_requested; P0=0 P1=1 P2=0 P3=0')
print('measurement_rows='+str(len(rows)))
print('hunt_directions='+str(len(set(re.findall(r'^### HƯỚNG (\d+):',s,re.M)))))
print('HINT.patch bytes='+str(Path('HINT.patch').stat().st_size))
assert len(set(re.findall(r'^### HƯỚNG (\d+):',s,re.M)))>=6
assert s.splitlines()[:3]==['verdict: changes_requested','reviewed_sha: 2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f','Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.']
assert s.count('```')%2==0
