from pathlib import Path
import csv,json,re,subprocess,hashlib
B=Path(__file__).resolve().parents[1];R=B/'cay-kho';O=B/'do-review9'
def git(*args):return subprocess.check_output(['git','-C',str(R),*args])
g=(B/'tai-lieu/GATE-TACH-JOB-CAT-CHI-PHI.md').read_text();lo=(B/'tai-lieu/LO-319-LINUX-BANG-CHUNG-XANH.md').read_text();issue=(B/'tai-lieu/463-GATE-TACH-JOB-CAT-CHI-PHI.md').read_text()
report={}
report['remaining_prose']={
 'a2_stale_ordering':[(n,t) for n,t in enumerate(g.splitlines(),1) if 'A1/A2/A5' in t and 'còn đúng' in t],
 'lo_denials':[(n,t) for n,t in enumerate(lo.splitlines(),1) if 'chưa được chọn' in t or 'ứng viên — chưa chọn' in t],
 'gate_noise_claims':[(n,t) for n,t in enumerate(g.splitlines(),1) if any(s in t for s in ['nhiễu runner cỡ','biên cho nhiễu runner','để đối chiếu nhiễu','rộng hơn nhiễu job','**hai** lượt master'])],
 'stale_round8_target_phrases':{x:(x in g or x in issue) for x in ['**mười một** lượt master chạy trọn','Mẫu là **mọi lượt master trong ~9,6 giờ**','(đổi băm ⇒ lease cấp lại), chưa làm ở PR này.']},
}
# Text-only remedy experiment. This is evidence data outside the checkout, not a proposed workflow implementation.
replacements_g=[
 ('⇒ **nhiễu runner cỡ `1`–`2,3` phút ở mức job là có thật**, và mọi ngưỡng ở `nghiem_thu` phải chừa\nbiên cho nó.', '⇒ Chênh lệch job giữa hai lượt là `0,92`–`2,27` phút; event/lane khác nhau nên chưa tách được nhiễu runner. A1 và A5 giữ nguyên ngưỡng.'),
 ('khi chỉ có **hai** lượt master chạy trọn','khi mới đối chiếu hai lượt chạy trọn (một nhánh/dispatch, một master/push)'),
 ('cộng `~4` phút biên cho nhiễu runner (chênh job\nđo được giữa hai lượt: `0,92`–`2,27`).','cộng `~4` phút biên thiết kế; chênh job `0,92`–`2,27` giữa hai event/lane không phải phép đo nhiễu runner riêng.'),
 ('(để đối chiếu nhiễu)','(đối chiếu lịch sử khác event/lane)'),
 ('rộng hơn nhiễu job đo được `2,27` nhân hệ số','là biên thiết kế; chưa có phép đo tách nhiễu runner để suy ra biên này'),
 ('đo trên cây **chưa đổi** — nền `34045664423`/`34048685345` còn đúng','đo trước ba packet kế nhiệm; A2 dùng nền mới tại `start_from_sha` đúng event/lane theo A2 r3; hai run lịch sử chỉ làm nền ước A1/A5'),
]
fixed=g
for before,after in replacements_g:assert fixed.count(before)==1,(before,fixed.count(before));fixed=fixed.replace(before,after)
lf=lo
before='**không khai `§12` đã xong**: câu hỏi *"có nên tiếp tục cách làm này không"* là quyết định của **chủ kho**,\nđặt lên bàn ở mục *"§12 — bốn lần hỏng"* cùng ba lựa chọn và năm điều kiện đo được; H là ứng viên đã đo,\n**chưa được chọn**.'
after='ghi quyết định chủ kho đã chọn (1) tiếp H ngày 07-09-2026 theo mục §12 và comment 5567158069; lease chưa cấp, Đ1–Đ5 tiếp tục ràng buộc.'
assert lf.count(before)==1;lf=lf.replace(before,after)
assert lf.count('**ứng viên — chưa chọn** (`§12` thuộc chủ kho)')==1;lf=lf.replace('**ứng viên — chưa chọn** (`§12` thuộc chủ kho)','**đã chọn (1), 07-09-2026** (mục §12; lease chưa cấp, Đ1–Đ5 còn ràng buộc)')
assert lf.count('### Các hướng vá đã ĐO — A-b, A-c, T, T\' đều bị bác; H là ứng viên')==1
lf=lf.replace("### Các hướng vá đã ĐO — A-b, A-c, T, T' đều bị bác; H là ứng viên","### Các hướng vá đã ĐO — A-b, A-c, T, T' đều bị bác; chủ kho đã chọn H theo §12")
report['prose_repair_experiment']=dict(gate_anchors=len(replacements_g),lo_anchors=3,gate_noise_assertions_removed=all(x not in fixed for x in ['nhiễu runner cỡ','biên cho nhiễu runner','để đối chiếu nhiễu','rộng hơn nhiễu job','**hai** lượt master']),a2_stale_row_removed='`34045664423`/`34048685345` còn đúng' not in fixed,lo_denials_removed=all(x not in lf for x in ['chưa được chọn','ứng viên — chưa chọn']),A1_preserved='**≤ 25,00 phút**' in fixed,A5_preserved='**≤ 135,00**' in fixed,branch_numbers_preserved=fixed.count('43,20')==g.count('43,20') and fixed.count('21,03')==g.count('21,03'),lo_code_blocks_unchanged=re.findall(r'```python\n(.*?)\n```',lf,re.S)==re.findall(r'```python\n(.*?)\n```',lo,re.S),H_decision_url_preserved='https://github.com/ducthangho/tra-luat/issues/464#issuecomment-5567158069' in lf)
# Store experiment outputs only as reviewer artifacts; every edit requires spec/lease rehash by executor.
(O/'prose-experiment').mkdir(exist_ok=True);(O/'prose-experiment/GATE.md').write_text(fixed);(O/'prose-experiment/LO.md').write_text(lf);(O/'prose-experiment/README.md').write_text('chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n\nĐây là thử nghiệm văn bản trên bản sao của reviewer; không phải spec/lease đã được cấp lại. Không sửa workflow hay mã cổng.\n')
S=R/'ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5';rows=list(csv.DictReader((S/'buoc.tsv').open(),delimiter='\t'));jobs=list(csv.DictReader((S/'job.tsv').open(),delimiter='\t'))
def triples(h):return {(r['step_name'],'windows' if 'windows' in r['job_name'] else 'ubuntu',r['step_conclusion']) for r in rows if r['head7']==h}
x,y=triples('426bfc0'),triples('1b3caa1')
report['two_run_context']=dict(jobs=[{k:j[k] for k in ['run_id','head7','head_branch','event','job_name','conclusion','started_at','completed_at']} for j in jobs if j['head7'] in ['426bfc0','1b3caa1']],same_tree=git('rev-parse','426bfc0^{tree}')==git('rev-parse','1b3caa1^{tree}'),diff_paths=git('diff','--name-only','426bfc0','1b3caa1').decode().splitlines(),triples_before=len(x),triples_after=len(y),added=sorted(y-x),removed=sorted(x-y),warning='Different event and release-verify lane; job range does not identify pure runner noise.')
report['merge']={'history':git('log','--format=%h %p %s','4d0ead5..HEAD').decode().splitlines(),'merge_982_paths':git('diff','--name-only','896c1c0','982cd1d').decode().splitlines(),'merge_master_paths':git('diff','--name-only','982cd1d','HEAD').decode().splitlines(),'issues':[]}
for issueid in [463,464,465,466]:
 f=next((R/'ops/issues').glob(str(issueid)+'-*.md'));rel=str(f.relative_to(R));current=f.read_text();old=git('show','896c1c0:'+rel).decode();blocks=re.findall(r'^> \*\*⚠ ĐÍNH CHÍNH 09:3xZ.*?(?:\n\n)',current,re.M|re.S);assert len(blocks)==1
 stripped=current.replace(blocks[0],'');row=dict(issue=issueid,block_count=len(blocks),outside_block_identical_to_executor=stripped==old,first_line=blocks[0].splitlines()[0],merged_file_same_as_head=git('show','982cd1d:'+rel)==f.read_bytes());report['merge']['issues'].append(row);assert row['outside_block_identical_to_executor'] and row['merged_file_same_as_head']
report['merge']['review_note_equals_ec03c85']=git('show','ec03c85:ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md')==(R/'ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md').read_bytes()
(O/'followup-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
