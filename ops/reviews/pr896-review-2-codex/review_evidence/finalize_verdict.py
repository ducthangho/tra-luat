from pathlib import Path
import re
p=Path('VERDICT.md'); s=p.read_text(); marker='### verdict-surface-bo-sot-pr889-luot1'; start=s.index(marker); end=s.index('\n### HƯỚNG ',start); finding=s[start:end].replace('receipt.yaml:96','receipt.yaml:97'); journal=s[s.index('### HƯỚNG 1:'):start]+s[end:]; journal=journal.replace('Kết luận: LỖI của kỳ vọng phủ ngữ nghĩa: xoá caveat khỏi receipt, cả t26/t27/t138 vẫn xanh 1/1. Các chốt không có răng đối với caveat CHƯA ĐƯỢC KHAI; không coi cổng xanh là chứng minh đủ caveat.','Kết luận: KHÔNG PHẢI LỖI riêng của hợp đồng t26/t27/t138; đây là giới hạn đã đo: xoá caveat khỏi receipt, cả ba vẫn xanh 1/1. Các chốt không có răng đối với caveat CHƯA ĐƯỢC KHAI; không coi cổng xanh là chứng minh đủ caveat. Finding cần sửa là thể hiện bị bỏ sót ở Hướng 13.').replace('numstat.txt:','numstat.txt (trích tối đa 1800 ký tự):')
# Keep all measured sections and outputs, put direction 14 variants together for readability.
sections=re.findall(r'### HƯỚNG .*?(?=\n### HƯỚNG |\Z)',journal,re.S)
def key(t):
 m=re.match(r'### HƯỚNG (\d+)',t); return int(m.group(1))
sections=sorted(sections,key=key); journal='\n\n'.join(t.strip() for t in sections)+'\n'
head='''verdict: changes_requested
reviewed_sha: 8d56009a09af7b3ef93801df105f9483de212cc7
Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

## KẾT LUẬN VỀ HAI FINDING CŨ

- P2 pr896-review-1 (t162): **ĐÃ ĐÓNG**. `CLAUDE.md:171` giới hạn t162 ở output `os`, nói rõ phải đọc `exclude`/`if` của từng job và dẫn chốt G5 cho mảnh/gom. Sáu mutant `exclude`/`if`/`needs` của cả hai job `gate-cong-cu*`: t162/t161 vẫn xanh 1/1, G5 đỏ; đổi nhánh output os: t162 đỏ 0/1, t161/G5 xanh. Đổi nguồn os riêng: t161 đỏ. Không còn vế "đọc ca ấy là đọc ma trận HIỆN HÀNH". `git diff --exit-code 3bc4244 8d56009 -- CLAUDE.md`: rc=0, không có diff (Hướng 1, 11, 19).
- P1 pr915-review-1 (surface): **ĐÓNG MỘT PHẦN** khi kiểm đủ mọi verdict như chỉ thị. Hai thể hiện lượt 2 được finding cũ nêu đích danh **đã đóng**: đúng caveat + dòng README, đúng dòng 9 và đúng run. Hai thể hiện lượt 3 cũng được đính chính đúng ở dòng 444/309. Nhưng grep độc lập tìm **5** verdict #870/#889 tự khai `codex_service`; #889 **lượt 1**, dòng 7, vẫn thiếu caveat và hàng README dù run `9f946d71` ghi `codex_cli`. Đếm một P1 cho cùng lớp lỗi còn sót, không mở lại bốn thể hiện đã sửa (Hướng 13, 14; finding cuối tệp).

Cây đã đo có tree `e93305541ae7d7f87fa5c57dd610fa1be829b0f7`. Phạm vi ghi chỉ là thư mục giao việc và scratch `/tmp/pr896-r2-audit-b3269a02/`; mọi mutant/hint áp trên clone local từ `mirror.git`, checkout đúng reviewed SHA. Không gọi mạng/push. Các phép đo dùng Python với `PYTHONDONTWRITEBYTECODE=1`; lệnh git trong harness kế thừa `GIT_OPTIONAL_LOCKS=0`. Không tự đặt tên execution surface cho phiên này.

## BẢNG ĐO

| Khẳng định | Bên giao khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Exact checkout | Head 8d56009; không shallow | `git rev-parse HEAD HEAD^{tree}` đúng SHA/tree trên; `--is-shallow-repository` = false; status rỗng (H1/H19) | Có |
| CLAUDE.md giữ nguyên bản vá P2 | Bằng tại 3bc4244 | `git diff --exit-code 3bc4244 8d56009 -- CLAUDE.md`: rc=0, stdout rỗng | Có |
| t162 đánh giá output os thật | Push, PR thường/nhãn windows, từng runner_set | CLI gốc t162 1/1; đổi nhánh windows-only trả hai nền: t162 rc=1, 0/1; t161/G5 rc=0 (H11) | Có |
| t162 không khóa exclude/if/needs | Phải đọc YAML cấp job | Cả 6 mutant trên hai job mảnh/gom: t162/t161 rc=0, 1/1 (H11) | Có |
| Phạm vi gate-cong-cu* | Phần mảnh/gom có G5 | YAML chỉ có `gate-cong-cu`, `gate-cong-cu-gop`; cả 6 mutant bị `loi_g5_workflow` phát hiện, rc=1, mỗi mutant 1 lỗi | Có, phủ đủ các job tiền tố tại SHA này |
| t161 chỉ giữ cấu trúc | Chung nguồn os, không fromJSON trong output | Đổi os riêng: t161 đỏ 0/1; bọc fromJSON output: t161/t162 đỏ 0/1, G5 xanh; đổi ngữ nghĩa nhánh: t161 xanh (H11) | Có |
| Không còn khai đọc test là ma trận hiện hành | Câu cũ đã bỏ | `rg -n 'đọc ca ấy là đọc ma trận HIỆN HÀNH\u007cđổi ma trận mà quên ca ấy' CLAUDE.md`: rc=1, không match (H19) | Có |
| Caveat surface cho #870/#889 lượt 2 | Bổ sung ở cả sidecar + README | run 2699e2d8 / d955f9ef đều CLI; verdict dòng 9; hàng README 701/707; text đính chính đúng (H13) | Có |
| Caveat surface cho #870/#889 lượt 3 | Bổ sung tương tự | run 94125115 / 4764bd6f đều CLI; verdict dòng 444/309; hàng README 717/722; text đúng (H13) | Có |
| Caveat đủ mọi verdict cần nó | Phải kiểm hết các *-verdict.md | `grep -nH codex_service ...`: 5 verdict; #889 lượt 1 dòng 7, run 9f946d71 CLI, không caveat/hàng README (H13) | **Không: P1** |
| Chốt khi mất một hàng README | t27 bảo vệ mục lục caveat đã khai | Xoá riêng từng hàng của 4 caveat hiện có: t27 rc=1, 0/1; t26/t138 rc=0, 1/1 (H14) | Có; t26/t138 không có răng với biến thể này |
| Chốt khi mất caveat trong receipt | Không được suy cổng xanh = đủ caveat | Xoá riêng caveat khỏi từng receipt: t26/t27/t138 đều rc=0, 1/1 (H14) | Giới hạn: cả ba không có răng khi caveat chưa được khai |
| Model #870 lượt 3 | 21 sự kiện, 21 response_id; gpt-6.1-sol | Đếm trực tiếp JSON: 21/21, mọi event=response.created, model chỉ gpt-6.1-sol, DO_DUOC (H12) | Có |
| Model #889 lượt 3 | 19 sự kiện, 19 response_id; gpt-6.1-sol | Đếm trực tiếp JSON: 19/19, cùng model/trạng thái (H12) | Có |
| Model #915 lượt 1 | 26 sự kiện, 26 response_id; gpt-6.1-sol | Đếm trực tiếp JSON: 26/26, cùng model/trạng thái (H12) | Có |
| Byte/hash verdict mới | #870 45798 / 0021b5b2…; #889 28705 / c05bc41d…; #915 46455 / 839757cc… | Tính SHA-256 và len(byte): khớp toàn bộ hash đầy đủ trong sidecar; bản phẳng = bản thư mục (H12) | Có |
| reviewed_sha/tree #870 mới | 06a50c5 / 0fa694da… | Dòng 2 verdict = run.head = receipt; git tree đúng 0fa694daf17e10c37fc3e61690531ade4bd528bf (H12) | Có |
| reviewed_sha/tree #889 mới | 094e8d1 / 55f5edf2… | Dòng 2 verdict = run.head = receipt; git tree đúng 55f5edf2f8601c976f390e8994193129a71203a1 (H12) | Có |
| reviewed_sha/tree #915 mới | 2789cbb / 6f299d7f… | Dòng 2 verdict = run.head = receipt; git tree đúng 6f299d7f70269ec32522fc4ea28c9d2d70c5424b (H12) | Có |
| base_sha | Lần lượt 9e9a74b / e63961f / 50a59a9 | Git giải ra đúng OID đầy đủ trong receipt; khớp PROMPT.md; là ancestor, numstat trùng byte (H16) | Có |
| thoi_luong_giay | 741.994 / 533.139 / 690.678 | JSON và hiệu hai timestamp đều đúng ba số ấy; ma_thoat=0, trạng thái xong (H12) | Có |
| prompt_sha256 | 5e69b5fe… / a7e97c93… / 29eba906… | SHA-256 PROMPT.md = từng trường JSON, đủ 64 hex được ghi ở H12 | Có |
| so_p* và verdict | #870/#889 approve 0/0/0/0; #915 changes_requested 0/1/0/0 | Dòng Kết quả + dòng 1 verdict khớp receipt và cap_nhat (H12/H16) | Có |
| evidence_url | cc0a3c9 chỉ mang hiện vật | Cả 3 URL ghim cc0a3c98ff8fee7aefa0e64982fa3532da2877d8; git show blob bằng verdict; 106 tệp đều trong ops/reviews, không receipt/code sản phẩm (H12/H16) | Có |
| Chuỗi commit #915 | 3bc4244 doc +3/-2; 7cfe062 hiện vật 91 tệp; 2789cbb ghi sổ 4 tệp | git diff-tree/numstat đúng 1/91/4 tệp; diff.patch #870/#889 trùng byte Git; diff #915 bỏ khỏi kho tái lập đúng 1334705 byte/hash (H16) | Có |
| Assurance #870/#889 | cross_approved | Approve trên đúng head đã merge; reviewer gpt đọc được từ run; executor claude suy theo provider, giới hạn đã có caveat (H12/H16) | Đủ theo nguồn đã khai; không chứng nhận model executor bằng máy |
| Assurance #915 / #896 | cross_reviewed; reviewer_assurance_81 CHUA DAT | changes_requested 1 P1 nên không nâng cross_approved; không có approve sạch trên 816f439 hoặc trạng thái sửa (H12/H16) | Có tại SHA đang chấm |
| cap_nhat ba hồ sơ | Lượt/provider/verdict/SHA/count/assurance từ receipt | Sáu đối chiếu mỗi hồ sơ đều true (H16) | Có |
| §10.2.2 Run | Push master, attempt 1, success; run 39752735359 / 39921552473 / 39983914661 | Đọc readback-run, đúng head 5f288ea / 6ac385f / 27dcc3b, path ci.yml (H15) | Có, nguồn tồn tại |
| §10.2.2 Checkout | Job 119738461348 / 120319840559 / 120524600728 | Log chứa SHA đúng; jobs đúng run/head, runner_id khác 0, labels Ubuntu; artifact head/tree khớp Git, identity_after bằng identity (H15) | Có, nguồn tồn tại |
| §10.2.2 Gate output | Artifact 12415205903 / 12488609174 / 12515154206 | JSON/output có thật; pass, rc=0, positive_verified=true; marker thật 1731/1731; SHA-256 output khớp (H15) | Có cho bytes JSON/output đã lưu |
| Digest ZIP tải từ REST | Summary nói digest tải về khớp REST | Digest trong readback-artifacts khớp summary; raw ZIP không lưu, không băm lại ZIP được (H15) | **KHÔNG ĐO ĐƯỢC lại raw ZIP**; giới hạn đã ghi zip KHONG kem |
| §10.2.2 Workflow definition / landed | not_measured (403); cả 3 landed=false | Summary + YAML giữ đúng trạng thái thiếu; blob ci.yml ba ref khớp Git chỉ là bằng chứng phụ, không nâng thành definition của run (H15) | Có về giới hạn khai; không lấy 3/4 làm 4/4 |
| SHA256SUMS ba hiện vật mới | Sạch | `sha256sum -c SHA256SUMS`: rc=0, 16/30/54 dòng OK (H12) | Có |
| SHA256SUMS cả lịch sử liên quan | Không sửa byte lịch sử | Tám thư mục review: rc=0, lần lượt 7/31/16/23/22/30/32/54 OK (H17) | Có |
| SHA256SUMS provenance land | Sạch | `sha256sum -c SHA256SUMS.txt`: rc=0, #870 18, #889 21, #896 25 dòng OK (H15) | Có |
| Cây gốc không bị sửa | Reviewer chỉ đọc + đo | Snapshot 7425 tệp thường gồm .git: added=[], removed=[], changed_content_or_mode=[]; git status kể cả ignored rỗng (H19) | Có so snapshot H1 |

Các lệnh gate bắt buộc chạy **tại `cay-kho/`**; rc và kết luận thật:

| Lệnh | rc | Kết luận / bằng chứng dương |
|---|---|---|
| `python3 ops/lease_publish_test.py --chi-ca=t26_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t27_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t138_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t161_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/lease_publish_test.py --chi-ca=t162_` | 0 | `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | `bien_nhan_v2: 235 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 288`; `TỔNG: ĐẠT` |
| `python3 ops/land_evidence_nguon.py --root .` | 0 | `land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73`; `TỔNG: ĐẠT` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | JSON `"ok": true`, files_scanned=115, claims_flagged=381, advisory_count=381; không gọi 381 advisory là không có claim |

## BẢNG SĂN

Nhật ký được ghi tăng dần trong lúc đo; các mục dưới giữ command và output thật. Các ca gate được ghi riêng để dễ kiểm N/N, không dùng chín ca gate làm chín hướng săn độc lập. Các hướng độc lập gồm định danh Git, phạm vi workflow qua mutant, byte/model của receipt, phủ nghĩa caveat, phản chứng quan hệ receipt–README, nguồn bốn mốc CI, base/diff/cập nhật và kiểm hint.

'''
# Escape the one regex alternation in table; raw pipes inside code spans still delimit GFM table cells.
head=head.replace('HIỆN HÀNH|đổi ma trận',r'HIỆN HÀNH\|đổi ma trận')
p.write_text(head+journal+'\n## FINDING CÒN MỞ\n\n'+finding+'\n')
print('VERDICT first 3 lines:'); print('\n'.join(p.read_text().splitlines()[:3])); print('unique_hunting_directions='+str(len({key(t) for t in sections}))+'; direction_variants='+str(len(sections))); print('bytes='+str(p.stat().st_size)); print('HINT.patch bytes='+str(Path('HINT.patch').stat().st_size))
