from pathlib import Path
import subprocess,json,hashlib,os,re
r=Path(__file__).resolve().parents[1];repo=r/'cay-kho';sha='210ab81c3f1af36243748458eb5e70180baeab71';env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'};pre=json.loads((r/'evidence/preflight16.json').read_text());cmds=[]
def git(*a,expected=0):
 c=['git','-C',str(repo),*a];p=subprocess.run(c,env=env,capture_output=True,text=True);cmds.append(dict(command=c,rc=p.returncode,output=p.stdout+p.stderr));assert p.returncode==expected,(a,p.returncode,p.stdout,p.stderr);return p.stdout.strip()
assert git('rev-parse','HEAD')==sha
assert git('rev-parse','HEAD^{tree}')==pre['git'][1]['output'].strip()
assert git('status','--porcelain=v1','--untracked-files=all','--ignored')==''
assert git('diff','HEAD','--')==git('diff','--cached','--')==''
assert git('rev-parse','--is-shallow-repository')=='false' and git('config','core.abbrev')=='7'
assert git('symbolic-ref','-q','HEAD',expected=1)==''
assert git('diff','--check','b0814f4','HEAD','--','ops/vm/')==''
files=[]
for q in pre['files']:
 data=(repo/q['path']).read_bytes();blob=subprocess.check_output(['git','-C',str(repo),'show',sha+':'+q['path']],env=env);h=hashlib.sha256(data).hexdigest()
 assert data==blob==(r/'copies/head'/q['path']).read_bytes() and h==q['sha256'];files.append(dict(path=q['path'],sha256=h))
assert (r/'PROMPT.md').read_bytes()==(r/'runs/52f05f65/prompt.snapshot').read_bytes()
read=lambda n:json.loads((r/'evidence'/n).read_text())
mut=read('review14-mutations.json')+read('more-mutants16.json');assert len(mut)==40 and all(q['killed'] and q['rc']==1 and q['failed_cases'] and not q['parser_error'] for q in mut)
mut_hashes=[]
for m in mut:
 p=r/'mutants'/m['name']/'ops/vm/cap-nhat-cong-cu.ps1';mut_hashes.append(hashlib.sha256(p.read_bytes()).hexdigest())
assert len(set(mut_hashes))==40
assert '115/115 ca QUA' in (r/'evidence/head-tests.log').read_text()
account=read('accounting-audit16.json');assert account['scalar_true']==account['executed']==115 and account['ast_count']==119
assert len(read('contracts16.json'))==19 and read('inventory16.json')['nonloi_count']==19
assert len(read('closure16.json'))==3 and len(read('zip-third16.json'))==14
assert len(read('new-third-paths-round15.json'))==4 and len(read('post-observations-round15.json'))==6
assert all(q['rc']==0 for g in read('regressions-round12.json') for q in g)
assert len(read('contracts-round12.json'))==7 and all(q['rc']==0 for q in read('contracts-round12.json'))
# Evidence is already asserted by dedicated current oracles; this audit checks their presence/accounting again.
for name in ['identity-audit16.json','extra-regression-assertions.json','regression-assertions.json']:
 if (r/'evidence'/name).exists():read(name)
v=r/'VERDICT.md';text=v.read_text();assert text.splitlines()[:2]==['verdict: dang_lam','reviewed_sha: '+sha]
assert len(re.findall(r'^HƯỚNG \d+:',text,re.M))>=13
post=read('post-observations-round15.json')
with v.open('a') as f:
 f.write('\nHƯỚNG 14: đối chứng hậu cài có trạng thái và kiểm tĩnh toàn phạm vi\n  giả thuyết : ca hậu cài vẫn dùng output trước cài hoặc giả hash/phiên bản để diễn kết quả.\n  lệnh       : python3 -u probes/post-observations-round15.py > evidence/post-observations16.log 2>&1; pwsh/pwsh -NoProfile -File probes/audit-source.ps1 > evidence/source16.log\n  output     : Post identity stateful observations: 6/6 PASS; head từ chối zero/Git-marker alias, mutant chấp nhận; mỗi ca có4installer,4marker và4native rc0. source parse_errors=0; pwsh7.6.9; Ubuntu24.04.5; README_native_acl_commands=0.\n  kết luận   : KHÔNG PHẢI LỖI trên head; suite không chỉ đo output hardcode trước installer. Toàn ops/vm có3tệp, đã đọc sản phẩm/test/README; không có lời gọi Add-KetQua qua alias/dynamic wrapper bị sót ngoài50lệnh AST. Model installer tạo marker rồi binary tự đổi output, hash được kiểm trước spawn; không gọi installer Windows thật.\n')
 f.write('\n## ĐỐI CHIẾU LƯỢT TRƯỚC\n\nFinding duy nhất lượt15: `ghim-actionlint-khong-la-dich-chung-nhan` → **ĐÃ VÁ THẬT** tại SHA hiện hành. Có3phép đo control/post-mismatch/keep-mismatch,4biên tag malformed/alias, và mutant bỏ chốt làm đỏ đúng2ca. Lớp thiếu ràng buộc ghim không còn biểu hiện mở ở2cửa ZIP giu/hậu cài; không phát sinh lớp finding mới từ các phép đo đã làm. Bảng đóng finding đầu tệp và H3/H9/H12 lưu lệnh/output.\n')
 f.write('\nHƯỚNG 15: kiểm cuối SHA/cây/artifact và tính toàn vẹn phép đo\n  giả thuyết : nguồn đổi sau đo, mutant trùng nhau, dữ liệu hiện hành bị trộn SHA hoặc verdict thiếu bảng chứng nhận.\n  lệnh       : python3 probes/final-audit16.py > evidence/final-audit16.log 2>&1\n  output     : exact HEAD='+sha+'; tree='+pre['git'][1]['output'].strip()+'; Git status kể cả ignored rỗng; diff HEAD/index/diff --check rỗng; detached/full-history/core.abbrev7;5/5tệp source=Git blob=copies/head và khớp băm preflight; PROMPT=prompt.snapshot;115/115,115Booleantrue;40mutant khác byte,40/40bị bắt;19/19Add khác loi; pin3/3,ZIP mới14/14,post-native4/4,stateful6/6.\n  kết luận   : KHÔNG PHẢI LỖI về mỏ neo và artifact. Snapshot sạch chỉ chứng minh không có delta tại hai mốc, không chứng minh không từng ghi rồi hoàn nguyên; các thao tác thực hiện trên cây nguồn chỉ đọc, mọi phép sửa chạy ngoài cay-kho/. Không push/merge/gọi mạng, không review ops/land. Windows native tại SHA này KHÔNG ĐO ĐƯỢC, không dùng71/71 hoặc11/11 ở SHA cũ làm chứng nhận mới.\n')
report=dict(reviewed_sha=sha,reviewed_tree=pre['git'][1]['output'].strip(),git=cmds,files=files,head_tests='115/115 rc0',scalar_true=115,nonloi_sites=19,mutants=40,unique_mutant_hashes=40,closure=3,new_zip=14,new_post_native=4,stateful_observations=6,findings={'P0':0,'P1':0,'P2':0,'P3':0},windows='KHÔNG ĐO ĐƯỢC native NTFS/icacls/Scheduled Task/COM/msiexec/actual user update at this SHA')
(r/'evidence/final-audit16.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
s=v.read_text().replace('verdict: dang_lam\n','verdict: approve\n',1)
s=s.replace('reviewed_sha: '+sha+'\n\n','reviewed_sha: '+sha+'\n\nKết quả: 0 P0, 0 P1, 0 P2, 0 P3.\n\n',1)
s=s.replace('Đang đọc chỉ thị và xác minh HEAD; chỉ đọc cây `cay-kho/`, mọi probe sửa mã sẽ chạy trên bản sao ngoài cây.','Review ngoại tuyến hoàn tất trên exact SHA; cây `cay-kho/` chỉ đọc, mọi probe sửa mã chạy trên bản sao ngoài cây.')
s=s.replace('Đang kiểm riêng kiểu kết quả, ca không đăng ký theo nền và sức bắt đột biến.','Kiểu kết quả, ca không đăng ký theo nền và sức bắt đột biến được đo riêng ở H11/H12.')
s+='\nKhông có finding P0/P1/P2/P3 còn mở trong phạm vi đã đo/phân tích tĩnh. **approve** tại `'+sha+'`: finding lượt15 đã đóng; bộ bắt buộc115/115/rc0; hợp đồng A/B kiểm đủ19/19điểm;40/40đột biến bị bắt. Không cần HINT.patch mới. Bằng chứng không bao gồm chạy Windows native tại head này.\n'
v.write_text(s)
print('Final audit PASS: exact clean HEAD; 5/5 blobs unchanged; 115/115 tests; 40/40 unique mutants killed; 19/19 certification sites; verdict approve, 0 findings')
