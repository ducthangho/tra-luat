from pathlib import Path
import json,hashlib,re
b=Path.cwd();o=b/'review_evidence';v=b/'VERDICT.md';(o/'VERDICT.progress.md').write_bytes(v.read_bytes())
def j(name):return json.loads((o/name).read_text())
parts=['''verdict: changes_requested
reviewed_sha: 05bc12e2b9008071ca28edbd4574e58644d48220
Kết quả: 0 P0, 2 P1, 1 P2, 0 P3.

## KẾT LUẬN VỀ FINDING CŨ

- P1 `phu-nhan-ancestry-chi-tren-nhanh-da-cu`: **ĐÃ ĐÓNG** ở 7/7 trường của 5 receipt nêu lượt 6. Bốn scalar v2 giữ đúng lời khai trong commit `77f272d435b0c23369b2348efa821c760d653036` / `62c2fceecac4d3e114f0ecfcb0980dc67514e0ee`; ba v1 giữ nguyên byte và có đúng supplementary caveat + hàng README. Mọi phép đo ancestry trong các đính chính tái chạy rc0 (H2, H3, H6). Quét lớp rộng hơn còn P1 về câu **PR #490 chưa merge** trong land evidence #491 (H15); không nhập phát hiện mới này vào bảy trường đã sửa.
- P1 `surface-service-cli-trong-ho-so-land`: **ĐÃ ĐÓNG** ở cả 3 verdict #832/#848/#862. Caveat đúng đường dẫn, dòng, hash và nguồn của chính lượt; #862 lượt 1 dùng transcript + land.review.luot_1, không mượn run lượt 2. Verdict không đổi byte (H11). Lớp khai surface còn **P2** ở #823 lượt 5 và #877 lượt 2: hai lời khai trái hồ sơ nhưng không có runtime gốc để chọn bên nào đúng (H12).

Lời khai mới do `05bc12e` thêm cũng được đối chiếu: mô tả `VERDICT.partial.md` của lần hỏng c0fa33fa sai nội dung hiện vật (P1, H16). Đây là kiểm lời giao mới; phần săn mở rộng trạng thái/surface vẫn phân biệt câu hiện hành, bản ghi lịch sử và lời trích khi mô tả finding.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Candidate/tree/master ghim | `05bc12e`, master `3e973a0`, đầy đủ | `git rev-parse`, `--is-shallow-repository`, status; tree `3412a314b129d1ee1473e528a5ec438378ccebe5`, shallow=false, sạch (H1/H17) | Có |
| Hai commit kể từ lượt 6 | `825dab1` chỉ hiện vật; `05bc12e` ghi sổ + áp hint | `git diff-tree`: 122 path của 825dab1 đều là hiện vật lượt 6; cha 825dab1=22382d8, cha 05bc12e=825dab1 (H2/H9) | Có |
| Bốn tệp diff/numstat giao kèm | đúng phạm vi delta và toàn PR | Tái sinh bằng `git -c core.quotepath=true diff`; 4/4 bằng byte (H2) | Có |
| Áp nguyên hint lượt 6 | 7 tệp, fuzz=0 | Tái áp trên blob 22382d8: rc0, 6/7 tệp bằng nguyên byte; README khác đúng 6 hàng **thêm**, gồm 5 caveat + 1 mục lục mới (H2) | Có về nội dung; README không bằng cả tệp |
| Bản verdict/hint lượt 6 | bản lưu nguyên byte | So với verdict-cu; cả hai bằng byte, SHA256SUMS 120/120 OK (H2/H9) | Có |
| Bốn trường v2 được neo | đúng commit và lời khai cũ | `git show <anchor>:<receipt>` và `git log -1`; 4/4 text + anchor khớp (H6) | Có |
| Ba v1 cần supplementary | giữ byte, đủ caveat/README | 3/3 băm, blob mốc, một hàng README và nguyên mô tả khớp (H6) | Có |
| Mốc và ancestry cũ/mới | đính chính đúng quan hệ Git | 48/48 mốc cũ là commit thêm receipt; 176/176 phép ancestry ghi trong các scalar/supplementary rc0 (H6) | Có |
| Đính chính surface land cũ | #832 lượt 7, #848 g3 lượt 1, #862 r21 lượt 1 | Băm/byte và đúng nguồn cùng lượt đều khớp (H11) | Có |
| Trạng thái chưa review đã sửa trước lượt 6 | dẫn verdict sau đúng head | 12/12 đối chiếu header, receipt SHA, băm khớp; verdict sau chưa tồn tại tại mốc cũ (H7) | Có |
| Surface ops/reviews | self-claim khác receipt phải được cảnh báo | 25 tự khai service có caveat/đính chính; 18 cặp receipt/run so được không lệch (H8) | Không tìm thêm lỗi ở các cặp này |
| Surface mở rộng land | các tự khai còn lại phải nhất quán hoặc có caveat | #823: service đối lập sổ 5 lượt CLI; #877: service đối lập lời hồ sơ về header CLI; cả hai thiếu caveat surface, không có run đúng head (H12) | **Không — P2** |
| Trạng thái PR #490 trong land #491 | `PR #479 và #490 chưa merge` | `git show 8cee941`, `merge-base --is-ancestor` tới master/candidate đều rc0, tới mốc cũ cdd0b1d rc1 (H15) | **Không — P1** |
| Lần chạy hỏng c0fa33fa | cùng head/prompt, rc1, 349.795s | Hai run.json khớp head/prompt; có trích lỗi server_overloaded lưu kèm (H16) | Có theo nguồn lưu |
| Nội dung partial của lần hỏng | chỉ dang_lam + một phép đo t26 | `wc -c`, `rg '^### '`: **28.214 byte, 14 mục**, gồm t27, t138, 4 cổng, Git và đột biến (H16) | **Không — P1** |
| Byte verdict trong sổ và caveat | không sửa hiện vật | 301 cặp verdict_path/verdict_sha256 đúng; 271 verdict phẳng có băm; 17 cặp phẳng/thư mục bằng byte; 137 entry manifest verdict đúng; không sửa verdict lịch sử so master (H3/H17) | Có |
| YAML/ID caveat | parse được, không trùng ID trong receipt | 368 YAML parse bằng loader từ chối key trùng; errors=[]; không trùng caveat ID trong từng receipt (H3) | Có |
| V1 miễn trừ băm | byte đóng băng | 11 ALLOWLIST_CUTOVER + 42 NO_DA_DO: 53/53 băm và byte bằng master/22382d8 (H3) | Có |
| t26 riêng | N/N bằng nhau | rc0, `1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| t27 riêng | N/N bằng nhau | rc0, `1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| t138 riêng | N/N bằng nhau | rc0, `1/1 đạt; đã chạy=1, bỏ qua=0` (H4) | Đạt |
| Xoá hàng README mới | ca nào đỏ | Xoá hàng mục lục hoặc hàng HINT-LUOT6: chỉ t27 đỏ rc1 0/1; t26/t138 vẫn 1/1 (H5) | Chỉ t27 có răng |
| Xoá caveat mới khỏi receipt | ca nào đỏ | t26/t27/t138 đều rc0 1/1 (H5) | **Cả ba không có răng** |
| bien_nhan_v2 tại cay-kho | rc + kết luận | rc0; 240 v2 + 11 legacy + 42 nợ =293, 0 vi phạm/0 không đo; TỔNG: ĐẠT (H4) | Đạt |
| land_evidence_nguon tại cay-kho | rc + kết luận | rc0; 47 ĐẠT, 26/28 miễn trừ, 0 vi phạm/0 không đo, tổng73; TỔNG: ĐẠT (H4) | Đạt |
| doctrine-scan tại cay-kho | rc + kết luận | rc0; sạch, 10 tệp, 0 chỗ chép doctrine (H4) | Đạt |
| doc-claims-check tại cay-kho | `ok=true` | rc0, stdout JSON có `"ok": true`, `"strict": false` (H4) | Đạt |
| HINT.patch lượt này | áp sạch trên clone exact SHA | 5 tệp, `patch --dry-run --batch --fuzz=0 -p0` rc0; áp thật rc0 (H13) | Đã đo trên bản sao |
| Ca/cổng sau hint | giữ điều kiện dương | Ba ca đều 1/1; bốn cổng rc0, JSON ok=true. Land sau sửa mất một miễn trừ và kiểm đủ luật vẫn ĐẠT (H14) | Đạt trên bản sao |
| Cây được chấm cuối lượt | chỉ đọc | HEAD/tree không đổi, status kể cả ignored rỗng, diff rc0 (H17) | Có |

## BẢNG SĂN

Các lệnh cổng chạy tại `cay-kho/`, trừ khi ghi rõ clone. Driver ở `review_evidence/`, đặt `PYTHONDONTWRITEBYTECODE=1`; chỉ dùng ca có sẵn, phép đọc/băm/Git và sửa tài liệu/biên nhận trên bản sao. Clone từ mirror.git nằm ở `/tmp/pr896-r7-mutations-rblaixtc/copy`, HEAD vẫn ghim 05bc12e. Không gọi mạng, push hoặc sửa cây được chấm. Nhật ký tăng dần giữ tại `review_evidence/VERDICT.progress.md`; log/JSON giữ từng kết quả. Số regex hit chỉ dùng chọn đối tượng đọc, không đếm thành finding.
''']
def direction(n,title,hyp,cmd,output,conclusion):
 parts.append(f'\n### HƯỚNG {n}: {title}\n\n- giả thuyết: {hyp}\n- lệnh: `{cmd}`\n- output thật:\n```text\n{output.rstrip()}\n```\n- kết luận: {conclusion}\n')
direction(1,'Định danh cây','sai SHA, cây bẩn hoặc shallow.','git -C cay-kho rev-parse HEAD HEAD^{tree} refs/remotes/origin/master; git status --porcelain; git log --oneline 22382d8..05bc12e',(o/'00-preflight.log').read_text().split('$ git diff --name-status')[0],'KHÔNG PHẢI LỖI. Shallow=false và core.abbrev=7 kiểm thêm ở H17.')
h=(o/'direction-2.log').read_text();keep=[l for l in h.splitlines() if not l.startswith('+|')]
direction(2,'Tái áp hint lượt 6 theo byte','lời khai áp nguyên hint sai hoặc thừa/sót hunk.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py history','\n'.join(keep),'KHÔNG PHẢI LỖI. README có đúng sáu hàng bổ sung; delta đầy đủ tại hint-readme-extra.diff. Các hàng hint thêm nguyên vẹn, sáu tệp khác khớp cả byte.')
direction(3,'YAML, hash verdict và v1','đổi byte hiện vật, phá YAML hoặc sửa v1.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/audit.py integrity',(o/'direction-3.log').read_text(),'KHÔNG PHẢI LỖI. integrity.json chứa từng băm/path; kiểm supplementary và toàn bộ land evidence cùng 293 receipt.')
checks=j('checks.json');out=[]
for x in checks.values():
 s=x['summary'];s=json.dumps(s,ensure_ascii=False) if isinstance(s,dict) else '\n'.join(s.strip().splitlines()[-2:]);out.append(' '.join(x['command'])+' | rc='+str(x['rc'])+' | '+s)
direction(4,'Ba ca riêng và bốn cổng tại cây gốc','xanh do skip hoặc thiếu kết luận dương.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/run_checks.py','\n'.join(out),'KHÔNG PHẢI LỖI của ca/cổng. Mọi ca chạy=1, skip=0; không gặp Codex home is inside a repository. Log stdout/stderr/rc được giữ riêng.')
m=j('mutations.json');out=[]
for r in m:
 out.append(r['mutation']+' removed_bytes='+str(r['removed_bytes']))
 for name,c in r['cases'].items():out.append(name+' rc='+str(c['rc'])+' '+c['summary'])
 for c in r['cases'].values():
  if c['error']:out.append(c['error'][0]);break
direction(5,'Xoá hàng và caveat mới trên clone','ca có sẵn bắt được việc mất thông tin mới.','git clone --no-hardlinks --no-checkout <mirror.git> /tmp/pr896-r7-mutations-rblaixtc/copy; git -C <copy> checkout --detach 05bc12e2b9008071ca28edbd4574e58644d48220; PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/mutations.py','\n'.join(out)+'\nstatus_after_restore=\'\'','KHÔNG PHẢI LỖI hiện hành thuộc các lớp săn, nhưng giới hạn đã chứng minh: t26/t138 không có răng với hai hàng README; t27 có răng. Cả ba không có răng khi xoá caveat mới khỏi receipt. Đã hoàn nguyên từng đột biến trước khi chuyển hướng.')
direction(6,'Mốc lịch sử và closure ancestry','neo sai OID/commit hoặc phép đo ancestry không đúng.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/closure_round6.py; git show <anchor>:<receipt>; git log -1 <anchor> -- <receipt>; git merge-base --is-ancestor <OID> <target>',(o/'direction-6.log').read_text(),'KHÔNG PHẢI LỖI; finding cũ đã đóng. 176 phép gồm target ghi trong câu và master/candidate ghim; không suy Packet đã landed. closure-round6.json giữ bảy trường mới và toàn bộ phép đo.')
r=j('states-reviews.json');out=[]
for group,items in r.items():
 out.append(group+' count='+str(len(items)))
 for x in items:out.append(x['verdict']+' sha='+x['expected_sha']+' receipt_sha_match='+str(x['receipt_sha_match'])+' header_match='+str(x['verdict_header_sha_match'])+' hash_match='+str(x['hash_match'])+' absent_at_anchor_rc='+str(x['next_absent_at_anchor_rc']))
direction(7,'Trạng thái chưa review và verdict kế tiếp','các đính chính trước đó dẫn sai head/hash hoặc mốc.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/states.py reviews','\n'.join(out),'KHÔNG PHẢI LỖI ở 12 đối chiếu. PR870/PR889 lượt 2/3 đều approve 0/0/0/0 trên đúng head; không biến kết quả lượt 1 thành approve.')
direction(8,'Surface trong ops/reviews','còn self-claim trái receipt/run chưa cảnh báo.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/surfaces.py; python3 review_evidence/runtime_index.py','\n'.join((o/'direction-8.log').read_text().splitlines()[:6])+'\nruntime_records=122','KHÔNG PHẢI LỖI mới trong 25 tự khai service của sổ review. Chỗ chỉ nhắc service/chatgpt_web khi mô tả finding không phải self-claim. Bốn ci-g5 có caveat thiếu runtime; lời mô tả README không nguyên byte nhưng đã cảnh báo giới hạn nguồn. 122 record bao gồm run-*.json và bản sao, không phải 122 run độc lập. Land ngoài inventory được kiểm tại H11/H12.')
r=j('new-claims.json');r.pop('new_caveats_rows',None)
direction(9,'Nguồn của receipt và land mới lượt 6','sai SHA/tree/run/hash/mục lục hoặc hiện vật.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/new_claims.py; sha256sum -c SHA256SUMS',json.dumps(r,ensure_ascii=False,indent=2),'KHÔNG PHẢI LỖI ở các scalar runtime, hash, hiện vật và liên kết đã đo. Năm caveat có đúng một hàng README và nguyên mô tả. Điều này không chứng minh mô tả đúng; câu về partial bị bác ở H16.')
r=j('status-checks.json');out=[f'yaml_paths={r["yaml_paths"]} inventory_counts={r["inventory_counts"]}']
for x in r['unreviewed_heads']:out.append(x['oid']+' receipt_matches='+str(len(x['receipt_matches']))+' verdict_header_matches='+str(len(x['verdict_header_matches'])))
for x in r['nonancestors']:out.append(x['oid']+' rc(master,candidate)='+str([x['master_rc'],x['candidate_rc']]))
for x in r['unmerged_specs']:out.append(x['path']+' ls-tree master='+repr(x['master_ls_tree'])+' candidate='+repr(x['candidate_ls_tree']))
out+=['HINT c8c1ee0 -> 2e4183b direct_child='+str(r['hint_history'][0]['direct_child']),'HINT 77a0a45 -> 1a276a1 direct_child='+str(r['hint_history'][1]['direct_child']),'land provenance verdict status: 103 paths, 82 matched lines']
direction(10,'Quét rộng các trạng thái','chỉ sửa danh sách cũ còn bỏ sót câu chưa review/áp/merge trong sổ và land.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/inventory.py; python3 review_evidence/status_checks.py; git merge-base --is-ancestor <OID> <ref>; git ls-tree <ref> -- <spec>','\n'.join(out),'Đã phân loại bằng ngữ cảnh và Git; P1 mới về #490 nằm ở H15. Các head kể trên chưa có verdict exact-SHA trong inventory nên không dùng review của ancestor/descendant để bác câu chưa review. Spec wp775/wp484 còn vắng ở cả master/candidate. pr696 có do_luc ghim bc57bca và 2026-09-30; pr684 nói rõ trạng thái TẠI THỜI ĐIỂM merge #684, không được đọc thành hiện tại của #689. Các HINT cũ đã có đính chính riêng ghim mốc. Nội dung verdict provenance là phép đo trên reviewed_sha riêng; câu chưa chạy hint trên KHO không có nghĩa executor chưa áp hint về sau. Số hit bao gồm chứa/chữa trong văn bản không dấu và lời trích; không coi từng hit là lỗi.')
r=j('land-round6.json');out=[]
for x in r:
 out.append(x['verdict']+':'+str(x['self_claim_line'])+' hash='+x['hash']+' hash_matches_caveat='+str(x['hash_matches_caveat'])+' same_master='+str(x['same_master'])+' same_prev='+str(x['same_prev']))
 out.append('source='+x['source'])
 if 'run_id' in x:out.append('run='+x['run_id']+' head='+x['head']+' surface='+x['surface']+' transport='+x['transport']+' program='+x['program']+' same_round_head='+str(x['same_round_head'])+' caveat_source_head_run_match='+str(x['caveat_source_head_run_match']))
 else:out+=['header='+repr(x['transcript_header']),'land_luot1='+x['land_luot1_reviewer'],'source_and_session_in_caveat='+str(x['source_and_session_in_caveat'])]
direction(11,'Closure ba surface land lượt 6','đính chính sai nguồn/dòng hoặc dùng run cùng SHA nhưng khác lượt.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/land_round6.py','\n'.join(out),'KHÔNG PHẢI LỖI. Cả ba self-claim vẫn nguyên byte và được đính chính rõ. #862 lượt 1 không dùng run-f0909b38 của lượt 2; #849 lượt 4/5 cũng đã có đính chính LOI TU PHAN LOAI trong review.luot_cuoi.reviewer.')
direction(12,'Surface land có nguồn thứ cấp trái lời tự khai','còn trường hợp tương tự slice-b-c-review-2, không có runtime gốc để phân xử.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/unresolved_land_surface.py',(o/'direction-12.log').read_text(),'LỖI P2 `surface-tu-khai-khac-ho-so-land-chua-co-caveat`. Đo được sự bất nhất văn bản và thiếu caveat; bề mặt thực chạy KHÔNG ĐO ĐƯỢC, không kết tội một lời khai runtime cụ thể là sai. Cảnh báo thiếu model/effort không tự cảnh báo mâu thuẫn surface.')
direction(13,'Áp hint trên exact candidate clone','hint không áp được, sửa v1/verdict hoặc YAML hỏng.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/build_hint.py; patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>',(o/'direction-13.log').read_text(),'KHÔNG PHẢI LỖI của hint cuối 5 tệp. Nhãn patch-as-hint có trong tệp; chỉ áp trên clone. Một lần dựng helper trước đó thử parse README bằng YAML đã dừng trước apply; đã sửa, dựng lại và kiểm lại bản cuối, không dùng lần kiểm clone sạch ấy làm bằng chứng hint (discarded-hint-builder-attempt.txt).')
r=j('hint-validation/checks.json');out=[]
for x in r.values():out.append(' '.join(x['command'])+' | rc='+str(x['rc'])+' | '+x['summary'])
direction(14,'Ca/cổng sau hint cuối','hint sửa văn bản nhưng làm hỏng cổng hoặc tính toàn vẹn.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/hint_checks.py (cwd clone với đúng 5 path modified)','\n'.join(out),'KHÔNG PHẢI LỖI của hint. Các kết quả này thuộc clone đã áp bản cuối 5 tệp. Sửa pr491 mất miễn trừ của land_evidence_nguon, nhưng kiểm đầy đủ vẫn đạt: 48 ĐẠT +25 miễn trừ=73; không sửa allowlist để lấy lại miễn trừ.')
r=j('pr490-status.json')
direction(15,'Khẳng định #490 chưa merge','nhãn nguồn THUẬT LẠI đã bị dùng thay mốc thời gian.','git blame -L 241,248 05bc12e -- ops/land/pr491-r358-ghi-so-land-evidence.yaml; git show -s --format="%H %P %s" 8cee941; git merge-base --is-ancestor 8cee941 <cdd0b1d/master/candidate>',json.dumps(r,ensure_ascii=False,indent=2),'LỖI P1 `pr490-chua-merge-trai-lich-su-git`. Không có mốc lịch sử cho hàng đang khai NỢ CŨ còn nguyên. Bản sửa neo lời khai vào cdd0b1d, giữ lịch sử và đính chính quan hệ Git hiện tại; không suy PR479 hay Packet đã landed. Các mô tả bot cùng reviewed head 2ec6171 trong receipt/README là thuật lại phép đối chiếu của lượt đó, không coi là lời tuyên #490 đang mở ngày nay.')
direction(16,'Mô tả hiện vật mới của lần hỏng','receipt mới tóm tắt thiếu nội dung tệp được chính nó trỏ tới.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/failed_run_claims.py; wc -c <VERDICT.partial.md>; rg -n "^### |^verdict:" <VERDICT.partial.md>',json.dumps(j('failed-run-claims.json'),ensure_ascii=False,indent=2),'LỖI P1 `mo-ta-partial-luot6-khong-khop-hien-vat`. Đo nội dung tệp frozen chứ không suy lần hỏng là review hoàn tất. Dòng dang_lam và việc không tính nó như verdict chốt vẫn đúng; phần chỉ có một t26 sai.')
direction(17,'Kiểm toàn vẹn cuối','cây gốc bị đổi hoặc hint lén sửa hiện vật/receipt v1.','PYTHONDONTWRITEBYTECODE=1 python3 review_evidence/final_checks.py; git status --porcelain=v1 --untracked-files=all --ignored; git diff --exit-code',json.dumps(j('final-state.json'),ensure_ascii=False,indent=2),'KHÔNG PHẢI LỖI. Cây gốc vẫn sạch kể cả ignored; clone có đúng 5 path tài liệu/receipt trong hint; 4 YAML hợp lệ và ID không trùng; 53 v1, mọi verdict giữ nguyên. 137 entry manifest verdict đều khớp, không có đường dẫn vắng.')
parts.append('''
## FINDING MỚI

### pr490-chua-merge-trai-lich-su-git [P1] Hồ sơ land #491 còn khai #490 chưa merge

TỆP/DÒNG: `ops/land/pr491-r358-ghi-so-land-evidence.yaml:244`, scalar `bookkeeping.4` bắt đầu ở dòng 242.

VẤN ĐỀ: Hàng hiện hành bắt đầu bằng “NỢ CŨ KHÔNG ĐỘNG TỚI”, khai “PR #479 và #490 chưa merge”. #490 đã merge bằng `8cee9410e958a6b9d956e080c11878fbd80d9f5f`, cha thứ hai `01e7f77d707cb093b5ba6d9b9d8577f40d025488`; merge ấy ở cả master ghim và candidate. “THUẬT LẠI” chỉ phân loại nguồn, không nói câu này đúng tại commit/thời điểm cũ nào. Không có caveat/đính chính cho hàng này. Đây là trạng thái Git đo được, không phải yêu cầu quyết định land của chủ kho.

ĐÃ THỬ NGHIỆM: H15: `git merge-base --is-ancestor 8cee941... 3e973a0...` rc0; cùng lệnh tới `05bc12e...` rc0. `git blame` và `git show cdd0b1d...:<path>` cho đúng scalar lịch sử; merge490→cdd0b1d rc1, nên có thể giữ câu ở mốc cũ thay vì trình bày như hiện hành. HINT thêm mốc và đính chính; đã áp sạch và qua cổng trên clone (H13/H14).

ĐỘ TIN: cao.

### mo-ta-partial-luot6-khong-khop-hien-vat [P1] Biên nhận mới khai sai nội dung partial đã lưu

TỆP/DÒNG: `ops/reviews/pr896-review-6-codex-verdict.receipt.yaml:126`; bản chiếu `ops/reviews/README.md:766`. Đối tượng được mô tả: `ops/reviews/pr896-review-6-codex/luot-hong-c0fa33fa/VERDICT.partial.md:7`.

VẤN ĐỀ: Hai chỗ do `05bc12e` thêm khẳng định “VERDICT.partial.md chi co dong dang_lam + mot phep do t26”. Tệp trong đúng SHA được chấm có **28.214 byte và 14 heading phép đo/đối chiếu**, gồm t27, t138, cả bốn cổng, lịch sử/băm/ancestry, đột biến README/caveat. Đây là lời khai mới sai về hiện vật có sẵn để đối chứng; không phải suy đoán về runtime hoặc diễn giải severity của verdict cũ.

ĐÃ THỬ NGHIỆM: H16: `wc -c` → 28214; `rg -n '^### |^verdict:'` → `verdict: dang_lam` + 14 mục, tên/dòng đầy đủ trong failed-run-claims.json. SHA256 partial `1d3f44f96f638c8224656b33385acf074ea2b168286a819dca4acbd0763ef869`. Run hỏng và run được tính có cùng prompt/head, nhưng tệp partial vẫn chưa chốt, không được tính thành verdict hoàn tất. HINT chỉ sửa mô tả ở receipt và README; giữ nguyên mọi hiện vật (H13/H14).

ĐỘ TIN: cao.

### surface-tu-khai-khac-ho-so-land-chua-co-caveat [P2] Hai tự khai service còn thiếu cảnh báo mâu thuẫn với hồ sơ

TỆP/DÒNG:

- `ops/land/pr823-wp802-provenance/verdict-luot5/wp802-g1-luot5-codex-verdict.md:6`; hồ sơ `ops/land/pr823-wp802-land-evidence.yaml:111` và dòng 114.
- `ops/land/pr877-wp854-provenance/verdicts/wp854-g1-luot2-codex-verdict.md:11`; hồ sơ `ops/land/pr877-wp854-land-evidence.yaml:78`.

VẤN ĐỀ: Đây đều là **tự khai của reviewer** `codex_service`, không phải nhắc chuỗi trong finding. #823 đồng thời ghi `review.so_loi_goi_codex_cli: 5`, và `luot_cuoi` nối chính lượt 5 với run b3d8a108/head 5c6c7a8. #877 đồng thời ghi các lượt review chỉ có “header CLI gpt-6.1-sol xhigh”. Hai hồ sơ không cảnh báo sự khác biệt surface; giới hạn hiện có chỉ nói model/effort/attestation. Không có run.json/transcript của chính lượt tương ứng trong cây để quyết định lời nào đúng. Do đó chỉ chấm **P2 thiếu điều kiện nguồn**, không chấm P1 khẳng định bề mặt thực tế sai và không tự đổi thành CLI. Cùng cách xử lý đã có ở supplementary caveat slice-b-c-review-2.

ĐÃ THỬ NGHIỆM: H12: đối chiếu đúng dòng verdict, YAML và comment #6247520447 lưu trong kho; comment khớp lượt 5/head/run. Trong 122 record run*.json (có bản sao) không có record mang hai reviewed head này; `verdict_usage_caveats` của hai hồ sơ đều vắng. Băm hai verdict lần lượt `b6ee86d0c9e523dfbe87718d12b4d646464e7a8720e9789f071f4aa04d6e3f01` và `612e86d854f4a7aad84a5f8e8d5986f58677e1b789d6ad3f176fefd1435cf277`, byte bằng master/22382d8. HINT thêm caveat thiếu nguồn, giữ cả hai lời khai lịch sử và không chọn surface; áp và cổng trên clone đều đạt (H13/H14).

ĐỘ TIN: cao về sự bất nhất và thiếu caveat; **KHÔNG ĐO ĐƯỢC** bề mặt thực chạy.

## GỢI Ý VÁ

`HINT.patch` là dữ liệu gợi ý, **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Năm tệp: land #491, #823, #877; receipt lượt 6 và README. Không đổi verdict, partial, receipt v1 hay allowlist. Đã `patch --dry-run --fuzz=0 -p0` và áp thật trên clone tại exact reviewed_sha, rồi chạy lại đủ ba ca + bốn cổng. SHA256 hint: `65e791768d947ee83be72e846274b0ce59ad6e230a20cb67fb6b5b43255bdff6`.
''')
v.write_text(''.join(parts))
assert v.read_text().splitlines()[:3]==['verdict: changes_requested','reviewed_sha: 05bc12e2b9008071ca28edbd4574e58644d48220','Kết quả: 0 P0, 2 P1, 1 P2, 0 P3.']
print('VERDICT bytes='+str(v.stat().st_size)+'; directions='+str(len(re.findall(r"^### HƯỚNG ",v.read_text(),re.M)))+'; HINT bytes='+str((b/'HINT.patch').stat().st_size))
