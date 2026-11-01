from audit_common import *

p=ROOT/'VERDICT.md'
t=p.read_text()
t=t.replace('Đang hoàn tất phép đo. Đã xác nhận finding P3, nên chưa đạt ngưỡng không P0/P1/P2/P3. Chỉ ghi trong sandbox; không cấp quyền merge/land.',
'''Hoàn tất cross-review PR #1119 lượt 1: **request_changes — 0 P0, 0 P1, 0 P2, 2 P3**. Ba tệp cache nguồn bị bỏ mà không khai, và hai caveat #1114 mô tả sai rằng DIFF.patch không vào kho. Cổng HEAD/base đều đạt, đột biến băm bị chặn đúng cả bốn biên nhận, các mỏ neo/telemetry đối chiếu được đều khớp; README giữ đủ hàng cũ và thêm đúng 23 hàng. Ngưỡng người dùng yêu cầu không còn P0/P1/P2/P3 chưa đạt. Không cấp quyền merge/land.''')
t=t.replace('Nhật ký tăng dần và kết quả phép đo sẽ được bổ sung dưới đây.', 'Nhật ký tăng dần và kết quả phép đo ở dưới; các script ở gốc sandbox, output trong `evidence/`.')
t=t.replace('`PYTHONDONTWRITEBYTECODE=1 python3 audit_bytes.py` cùng phép kiểm caveat sẽ ghi tiếp','`PYTHONDONTWRITEBYTECODE=1 python3 audit_claims.py` (đối chiếu byte: `python3 audit_bytes.py`)')
t=t.replace('Các lỗi (nếu có) nằm ở mapping_failures/omissions/manifest và original_diff_equal;', 'Output `mapping_failures=[]`, manifest sạch, original_diff_equal=true cả bốn; ba thiếu khai được chỉ ra ở omissions của #1114 lượt 1;')
p.write_text(t)

append('''Bảng cổng đo lại: chạy từ `work/base` và `work/head`, `PYTHONDONTWRITEBYTECODE=1`, `core.abbrev=7`. Lệnh bao và rc: `python3 audit_gates.py {base,head}`; toàn bộ stdout/stderr đã lưu.

| Lệnh thực trong mỗi bản sao | Base | HEAD | Delta |
|---|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | rc0; 287 ĐẠT v2, tổng 340 | rc0; 291 ĐẠT v2, tổng 344 | +4 v2; vi phạm 0→0; KHÔNG ĐO ĐƯỢC 0→0 |
| `python3 ops/land_evidence_nguon.py --root .` | rc0; 75 ĐẠT, 25/28 miễn trừ, tổng 100 | cùng output | 0 |
| `python3 ../../direct_gates.py .` | rc0; 3 PASS | rc0; 3 PASS | 0 |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0; quét 10 tệp, 0 chỗ chép doctrine | cùng output | 0 |
| `git diff --check f4b513d HEAD` | rc0; rỗng | rc0; rỗng | 0 |

Ba hàm được gọi trực tiếp: `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi`, `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc`, `t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen`. Hai SyntaxWarning về escape trong lease_publish_test.py xuất hiện ở cả base và HEAD; không có lỗi mới. Biên nhận: legacy 11/11 và nợ 42 giữ nguyên; nợ câu lịch sử L-REVIEW=1, L-ANCESTRY=60, L-SURFACE=0 giữ nguyên (`evidence/{base,head}-bien-nhan.stdout`).''')

rows=json.loads((EVID/'bytes.json').read_text())
lines=['Byte/độ phủ — lệnh `PYTHONDONTWRITEBYTECODE=1 python3 audit_bytes.py`, output `evidence/bytes.json`:','',
 '| Thư mục | Tệp nguồn cấp | Chép khớp byte | Vắng, khai đúng hash/bytes | Vắng chưa khai | SHA256SUMS entries/rc |',
 '|---|---:|---:|---:|---:|---|']
for r in rows:
    lines.append('| '+r['archive']+' | '+str(r['source_files'])+' | '+str(r['archived_source_files'])+' | '+str(sum(x['matches_declaration'] for x in r['omissions']))+' | '+str(sum(not x['declared'] for x in r['omissions']))+' | '+str(r['manifest_entries'])+'/rc'+str(r['manifest_rc'])+' |')
lines+=['', 'Bốn bản phẳng bằng VERDICT nguồn. Tập manifest phủ đúng mọi tệp đã lưu trừ chính SHA256SUMS, gồm OMITTED.txt; không thiếu, thừa hoặc trùng mục. Lệnh thật `sha256sum -c SHA256SUMS` chạy riêng trong từng thư mục, lần lượt 59/45/45/92 dòng OK. Tổng 250 tệp nguồn cấp: 237 chép khớp byte, 10 vắng đã khai đúng, 3 vắng chưa khai. Các thư mục cay-kho/work/copies và nguồn con không được cấp trong đầu vào không nằm trong phép kiểm kê này.', '',
 'Hai DIFF.patch bị bỏ của #1110: `git diff c6dd7b3 e137f8c` và `git diff fb74c6e 3a3aac5` đều sinh **261239 bytes**, SHA256 `79c3d941cbfbc0cb32301c73d00237885aaf275bfef3aef347c1a5ded42968b6`, bằng byte nguồn. Bốn launcher.err đều 0 bytes, SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Bốn tệp nguồn >500 KB bị bỏ có kích thước 2043534, 822015, 838749, 1415498 bytes; hash/bytes đều khớp OMITTED.txt (`evidence/bytes.json`).', '',
 'Ba tệp thiếu khai của P3 bo-sot-cache-khong-khai — output do audit_bytes.py tự băm, tiền tố đường dẫn `nguon/review1114a/evidence/ruff-cache-created/`:','',
 '| Tệp | Bytes | SHA256 |','|---|---:|---|']
for o in rows[2]['omissions']:
    if not o['declared']: lines.append('| `'+o['source'].removeprefix('evidence/ruff-cache-created/')+'` | '+str(o['bytes'])+' | `'+o['sha256']+'` |')
append('\n'.join(lines))

rs=json.loads((EVID/'receipts.json').read_text())
lines=['Biên nhận — lệnh `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipts.py`: mỗi biên nhận 82 đối chiếu, tổng 328, `failures=[]`. Dữ liệu actual/expected từng trường nằm trong `evidence/receipt-checks.json`.','',
 '| PR/lượt | reviewed_sha | tree | run_id | Giây / sự kiện model | sandbox_trang_thai |',
 '|---|---|---|---|---|---|']
for r in rs:
    lines.append('| '+r['receipt'].removesuffix('-verdict.receipt.yaml')+' | `'+r['reviewed_sha']+'` | `'+r['reviewed_tree']+'` | `'+r['run_id']+'` | '+str(r['duration'])+' / '+str(r['model_events'])+' | '+r['sandbox']+' |')
lines+=['', '''Cả bốn run.json ghi ma_thoat=0, trang_thai=xong, mọi sự kiện model gpt-6-astra và effort xhigh; duration khớp hiệu timestamp sau làm tròn 3 chữ số. Prompt SHA256 bằng PROMPT.md; run/launcher/checkpoint và băm stdout/stderr khớp. Caveat SANDBOX-KHONG-DO-DUOC có đúng ở #1110 lượt 1, #1114 lượt 1 và lượt 2; vắng đúng ở #1110 lượt 2. KHONG_DO_DUOC không chứng minh không có sandbox: các run đó vẫn có mẫu quan sát, nhưng sampler ghi lỗi DanhTinhDoi.

Các lệnh git trong audit_receipts.py cho: `f4b513d^2=3a3aac561ba359c08dfe92d95584b56494fc12d4`, `fb74c6e^2=51435a44659c4026539497a47ace971a71a64f40`; `git merge-base --is-ancestor e137f8c f4b513d` và `... e101b11 fb74c6e` đều rc0. Hai lượt 1 không được đồng nhất với head cuối. Hai merge đều là tổ tiên origin/master tại chỗ; ngày commit 2026-11-01 và message mang đúng số PR. Đây là phép đo git, không xác nhận yêu cầu API merge đã gửi.

`git merge-base --is-ancestor cf5acfa HEAD` rc0; cả bốn URL neo đúng commit `cf5acfa7282ec42ef282015fa27fc642a4515588`, đúng verdict_path; `git show <anchor>:<path>` bằng byte verdict và hash receipt. `_tinh_lop_tu_write_set` trên từng diff base..reviewed_sha cho sensitive ở cả bốn, số đường dẫn lần lượt 46/46/1/1. Dòng verdict, Reviewed commit, số finding P0/P1/P2/P3=0/0/0/0 khớp nguồn; caveat P3 không bị đếm thành finding.

`python3 audit_claims.py` cho 45 đối chiếu kết luận/log lịch sử khớp. Cụ thể: #1110 lượt 1 có 41 bản sao/2 khai bỏ/116 đối chiếu trong nguồn verdict; cả hai lượt #1110 có delta README lịch sử +4, mất0; diff ops/reviews giữa hai lượt rỗng. #1114 cả hai lượt có 52/52 và 80/80 trong log nguồn; lượt 2 cộng lại các worker được 26/1800→0/1800, đếm 20 chuyển R→Z/1200, thời gian suite tăng 15.017 s (4.92%). Các con số này đối chiếu câu ket_luan với hiện vật nguồn của lượt cũ, không phải số hiện vật được ghi sổ trong PR #1119 và không phải chạy lại review lịch sử.

Tiền lệ pr1058 lượt 1/2 và pr1075 lượt 1: 22 trường cố định × 3 × 4 đều bằng nhau (`evidence/claims.json.precedent`). Các khác biệt nội dung có căn cứ: pr1058 lượt 1 changes_requested nên có assurance_KHONG_dat và không có ket_luan; bốn verdict mới approve nên cross_approved và có ket_luan. Caveat head-cuối được thêm cho hai lượt 1, sandbox caveat theo run tương ứng; không phát hiện lệch tiền lệ khác ngoài mô tả loại DIFF sai đã nêu.''']
append('\n'.join(lines))

ms=json.loads((EVID/'mutations.json').read_text())
lines=['Đột biến — `PYTHONDONTWRITEBYTECODE=1 python3 audit_mutations.py`, chỉ thay ký tự đầu verdict_sha256 từng tệp trong `work/mutant`, không chạm clone gốc. Output nguyên văn trong `evidence/mutant-*.stdout/.stderr`:','',
 '| Biên nhận | Băm trước→sau (tiền tố) | bien_nhan_v2 | t26 | Đích bị báo đỏ |', '|---|---|---:|---:|---|']
for m in ms:
    lines.append('| '+m['receipt']+' | '+m['old'][:12]+'→'+m['new'][:12]+' | rc'+str(m['bien-nhan']['rc'])+' | rc'+str(m['direct']['rc'])+' | đúng tệp; foreign_receipts=[] |')
lines+=['', 'bien_nhan_v2 báo `blob tại evidence_url băm ... nhưng biên nhận khai verdict_sha256 ...`; t26 báo `LỆCH BĂM`. Hai t27 vẫn PASS ở mỗi bản đột biến. Chỉ dùng đột biến hash để đáp ứng yêu cầu mỗi biên nhận một trường đo được; không suy rằng đã thử đột biến riêng mọi trường reviewed_sha/evidence_url.', '',
 '''Giới hạn: GitHub hiện tại, nội dung/job CI Windows thật và kết quả CI ngoài các tệp cấp, quyền credential/actor đăng, chỉ thị chủ kho trong phiên executor, giá trị expectedHeadSha gửi lên API, URL còn phục vụ trên GitHub: **KHÔNG ĐO ĐƯỢC**. Dòng “Windows that do o CI ngoai luot review” được coi là lời khai ngoài review, không là phép đo của lượt này. Phiên/nhà cung cấp độc lập phía máy chủ, toàn bộ argv chạy lịch sử và phiên bản CLI ngoài hiện vật được cấp: **KHÔNG ĐO ĐƯỢC**. Đã đối chiếu metadata hiện vật; không nâng tính mạnh của nó thành xác thực ngoài nguồn. Các thư mục nguồn con/cây kho lịch sử đã bị loại khỏi đầu vào không được tự suy là đã kiểm byte. Không dựng nội dung nhạy cảm và không chạy mạng.''']
append('\n'.join(lines))
print('VERDICT.md finalized:',len(p.read_bytes()),'bytes')
