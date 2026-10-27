from pathlib import Path
import json,re,hashlib,subprocess
B=Path(__file__).resolve().parent.parent;P=B/'VERDICT.md';R=B/'cay-kho'
s=P.read_text()
s=s.replace('- P1 verdict-surface-bo-sot-pr889-luot1 (lượt 2): đang đo.','- P1 verdict-surface-bo-sot-pr889-luot1 (lượt 2): **ĐÃ ĐÓNG**. Tại 82359c4, receipt có caveat và README có hàng cảnh báo đúng dòng 7, run `9f946d714c2344fa9691c3d7d4f1b2d9`, run.json:47 `codex_cli`, chương trình `codex`, header `OpenAI Codex v0.163.0`. Verdict 75193 byte, SHA256 `6aa03cacbde6f33a41ba4af60e408b2c742da5959390f28a9cf8420b5cb098f5`, khớp receipt/SHA256SUMS và giữ nguyên từ cha. Tái áp nguyên HINT lượt 2 trên hai tệp ở cha tạo đúng blob của 82359c4. **Lớp lỗi chưa hết toàn kho**: wp766 còn biểu hiện có run JSON bác bỏ, và 13 cặp tự khai service/receipt CLI thiếu điều kiện nguồn được ghi riêng dưới đây.')
rows=[
('HEAD/tree, không shallow','82359c4, cây đầy đủ','`git rev-parse HEAD HEAD^{tree}` = 82359c4… / 32cf81c2614a91c7ced8fc77781b01dcb12fc8a7; `--is-shallow-repository` false; status đầu rỗng','Có'),
('Diff bản vá và toàn PR','2 tệp +5 dòng; PR so master 356eb26','`python3 evidence/history_audit.py`: cả diff.patch/numstat.txt/diff-pr947.patch/numstat-pr947.txt equals_supplied=True','Có'),
('Áp NGUYÊN HINT lượt 2','patch -p0 --fuzz=0 trên cha 578fb4b','`python3 evidence/validate_hint.py`: old_hint_rc=0, cả hai target_blob_match=True','Có'),
('Caveat mới dẫn nguồn','verdict:7, run 9f946d71, run.json:47, CLI v0.163.0','`python3 evidence/old_p1_audit.py`: đúng nguyên câu service/phủ nhận codex exec; JSON CLI/program codex; header khớp','Có'),
('README của P1 cũ','Một hàng nâng caveat','Cùng script: README_matching_rows=1; đúng nguyên caveat receipt','Có'),
('Byte verdict pr889-review-1','75193, 6aa03cac…','Cùng script: đủ SHA256 như kết luận; flat_equals_directory=True, unchanged_since_parent=True, sha256sum_rc=0 (23 mục OK)','Có'),
('Quét mọi verdict tự khai service','Không chỉ nhóm #870/#889','267 verdict; 12 tệp chứa codex_service = 10 tự khai + 2 chỉ mô tả finding; 5/10 đã đính chính, 4/10 ci-g5 có caveat không đo được, 1/10 wp766 còn sót (surface_audit.py)','Không: P1 wp766'),
('Các cách viết service/API khác','Cần quét cả tên diễn giải','service_spelling_audit.py: 13 cặp service/receipt CLI; tìm mọi run.json không có run_id tương ứng (service-runtime-search.log)','Không: P2 thiếu điều kiện'),
('Verdict lượt 2 nguyên byte','66095 byte, a2b588b6…','receipt_audit.py: SHA256 a2b588b64535203f9e481240e7f014ae0f34f84b8a776e646b573666e5bd689f; phẳng = thư mục = verdict-cu','Có'),
('Finding count lịch sử','changes_requested 0/1/0/0','Header verdict dòng 1/3 khớp so_p0/1/2/3 = 0/1/0/0; reviewed SHA vẫn 8d56009','Có, lịch sử'),
('reviewed_sha/tree/base','8d56009 / e9330554… / 50a59a9…','receipt_audit.py: OID đủ khớp run.head, git tree; 3bc4244^ = base; 21fe565^2 = reviewed_sha','Có'),
('Hai bản vá được review','3bc4244 và cc0a3c9..a9bc934','history_audit.py: hai commit là ancestor của 8d56009, rc=0; historical-diffs.log: diff/numstat của cả hai khớp byte','Có'),
('Run metadata lượt 2','launcher 1.5.0, xong, rc0, 600.539, clean=true, CLI','receipt_audit.py: đủ các trường khớp; duration theo timestamp 600.539266, làm tròn 600.539','Có, metadata của run'),
('Prompt lượt 2','64404d73…','SHA256 PROMPT.md = 64404d73a93d9f43878adc436e1cbe761a5f930cdf011a793e31b896b166812a = run.prompt_sha256','Có'),
('Model phục vụ được lưu','25 sự kiện, 25 response_id khác nhau, gpt-6.1-sol','receipt_audit.py: events=25 / unique_response_id=25; 25 response.created và 25 gpt-6.1-sol; trạng thái DO_DUOC','Có ở trace launcher được lưu'),
('Serving effort / cờ CLI đầy đủ / session independence','xhigh là yêu cầu; lệnh CLI và phiên độc lập được thuật lại','run.json chỉ lưu chương trình/số đối số/van_tay; stderr trong kho chỉ có hai dòng Reading additional input; không có nguồn độc lập cho toàn argv, phiên bản CLI hay serving effort/session','KHÔNG ĐO ĐƯỢC lại; không suy thêm'),
('stdout/stderr của run','254 / 78 byte và hash trong JSON','receipt_audit.py: byte/hash hai stream đều khớp đầy đủ; phần stderr bị bỏ ghi riêng 27643975 byte/320518 dòng','Có; không phục dựng được phần bỏ'),
('Evidence URL ghim commit chỉ mang hiện vật','25e7d1167856c3beea2552f49a6c1ded0a128fdf','git diff-tree: 108 path chỉ trong thư mục lượt 2 + verdict phẳng; evidence_blob_equal=True; không có receipt/README/land trong commit đó','Có, blob Git local; không gọi mạng'),
('SHA256SUMS lượt 2','Tệp được lưu có băm','sha256sum -c SHA256SUMS tại thư mục: rc=0, 106/106 mục OK; log evidence/pr896-r2-sha256.log','Có'),
('OMITTED.txt','snapshot 1056144 byte/sha256 fca16267…, bỏ copy/','receipt_audit.py: snapshot/copy vắng; 107 tệp hiện tại, lớn nhất 73441 byte; không còn byte gốc để hash lại','Đo được sự vắng; hash/byte tệp bỏ KHÔNG ĐO ĐƯỢC'),
('Năm hàng README lượt 2','4 cảnh báo + 1 mục lục','receipt_audit.py: row_count=5; 3 cảnh báo về checkout/driver/OMITTED khớp hiện vật; cảnh báo HINT và vế HINT ở mục lục đã cũ','Một phần: P1 trạng thái HINT'),
('Khối land lượt 2 không sửa dòng cũ','Chỉ nối cuối','history_audit.py: prefix_preserved=True tại commit 765ae89 và so master 356eb26; sau ghi sổ byte khối không đổi','Có'),
('Trạng thái/đơn vị land','landed false; CHUA DAT; cần chủ kho chấp nhận','YAML parse: False / CHUA DAT; don_vi_land_de_xuat có CAN chu kho chap nhan, KHONG tu chon','Có; chỉ là đề xuất'),
('HINT chưa áp / caveat vẫn thiếu','receipt:111–114; README:731/1028; land:234/242','history_audit.py: caveat_count 0 ở 578fb4b, 1 ở 82359c4; old-HINT tái áp tạo đúng blob target','Không hiện hành: P1; đúng ở 765ae89/578fb4b'),
('t26 nền','Cần N/N hai số bằng nhau','python3 ops/lease_publish_test.py --chi-ca=t26_: rc0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0','Có'),
('t27 nền','Cần N/N hai số bằng nhau','python3 ops/lease_publish_test.py --chi-ca=t27_: rc0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0','Có'),
('t138 nền','Cần N/N hai số bằng nhau','python3 ops/lease_publish_test.py --chi-ca=t138_: rc0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0','Có'),
('Bỏ hàng README mới','Chốt phải đo lại cho bản vá này','mutations.py trên clone mirror.git checkout 82359c4: t26 rc0 1/1; t27 rc1 0/1; t138 rc0 1/1','Chỉ t27 có răng'),
('Bỏ caveat receipt mới','Không suy nền xanh = đủ caveat','Cùng clone, khôi phục README trước: t26/t27/t138 đều rc0 1/1','Cả ba không có răng với bỏ caveat'),
('bien_nhan_v2','Đo tại cay-kho exact SHA','python3 ops/bien_nhan_v2.py --root .: rc0; 236 ĐẠT v2, 11/11 legacy, 42 NỢ, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC, tổng289; TỔNG: ĐẠT','Đạt gate, không chứng minh ngữ nghĩa mọi câu'),
('land_evidence_nguon','Đo tại cay-kho exact SHA','python3 ops/land_evidence_nguon.py --root .: rc0; 47 ĐẠT, 26/28 miễn trừ, 0 vi phạm/0 KHÔNG ĐO ĐƯỢC, tổng73; TỔNG: ĐẠT','Đạt gate'),
('doctrine-scan','Đo tại cay-kho exact SHA','python3 .claude/dev/packet_loop.py doctrine-scan --root .: rc0; sạch — đã quét 10 tệp, 0 chỗ chép doctrine','Đạt gate'),
('doc-claims-check','Phải ok:true','python3 scripts/tl.py doc-claims-check --json: rc0; JSON parse ok=True, strict=False','Đạt gate'),
('Secret scan hiện vật lượt 2','Đo đúng thư mục','python3 scripts/pkg_secret_scan.py ops/reviews/pr896-review-2-codex: rc0, stdout/stderr rỗng; main() trả 0 khi hits rỗng, không in summary khi sạch','Đạt theo giao diện lệnh'),
('HINT mới','Gợi ý, chưa áp cây giao review','validate_hint.py: dry-run/apply --fuzz=0 rc0 trên clone; t26/t27/t138 rc0 1/1; hai gate receipt/land TỔNG: ĐẠT; 17 tệp tài liệu/receipt','Đã thử trên clone')]
header='## BẢNG ĐO\n| khẳng định | bên giao khai | đo được (lệnh) | khớp? |\n|---|---|---|---|\n'
table=header+''.join('| '+' | '.join(row)+' |\n' for row in rows)
assert header in s;s=s.replace(header,table,1).replace('Đang thu thập output thật; sẽ nối thêm sau mỗi hướng thử.','Mỗi hướng bên dưới có giả thuyết, lệnh, output thật và kết luận; log/script giữ tại `evidence/` ngoài cây được review. Khi không ghi cwd khác, lệnh kiểm kho chạy tại `cay-kho/`; script audit chạy tại thư mục chứa PROMPT.md.')
s=s.replace('- lệnh: Python đọc receipt YAML, `run/run.json`, dòng 7 verdict, header; SHA256; `git show 578fb4b:ops/reviews/pr889-review-1-codex-verdict.md`; `sha256sum -c SHA256SUMS` tại `ops/reviews/pr889-review-1-codex/`.','- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/old_p1_audit.py` (đọc receipt/run/header/SHA256, `git show 578fb4b:ops/reviews/pr889-review-1-codex-verdict.md`, và `sha256sum -c SHA256SUMS` tại thư mục hiện vật).')
P.write_text(s)
print('measurement_rows',len(rows),'hunt_directions',len(re.findall(r'^### HƯỚNG \d+:',s,re.M)),'findings',len(re.findall(r'^### [a-z].*\[P\d\]',s,re.M)))
