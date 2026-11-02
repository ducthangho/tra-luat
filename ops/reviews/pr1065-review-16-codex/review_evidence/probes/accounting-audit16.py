from pathlib import Path
import json,subprocess,hashlib
r=Path(__file__).resolve().parents[1];x=json.loads((r/'evidence/inventory16.json').read_text());cases=[json.loads(l) for l in (r/'evidence/cases16.jsonl').read_text().splitlines()]
assert len(cases)==115 and len({v['name'] for v in cases})==115 and all(v['type']=='System.Boolean' and v['value'] is True for v in cases)
missing=sorted({v['name'] for v in x['cases']}-{v['name'] for v in cases});assert len(missing)==4 and x['case_count']==x['unique_case_names']==119
assert (r/'copies/head/ops/vm/cap-nhat-cong-cu.ps1').read_bytes()==(r/'copies/accounting/ops/vm/cap-nhat-cong-cu.ps1').read_bytes()
ic=json.loads((r/'evidence/icacls16.json').read_text());assert len(ic)==5
for q in ic[:4]:assert q['roundtrip'] and q['threw']==(q['rc']!=0)
assert ic[4]['threw']
# Compare previous/current product diff: only the pinned response guard + explanation were added in round 15.
p=subprocess.run(['git','-C',str(r/'cay-kho'),'diff','c489c722db43623f1d9b2250420edce0005a96d5','210ab81c3f1af36243748458eb5e70180baeab71','--','ops/vm/cap-nhat-cong-cu.ps1'],capture_output=True,text=True,check=True)
(r/'evidence/product-round15-to16.diff').write_text(p.stdout)
assert p.stdout.count('\n+')==3 and '\n- ' not in p.stdout
out=dict(executed=115,scalar_true=115,ast_count=119,not_registered_on_linux=missing,icacls_fixture_cases=5,product_diff_rc=p.returncode)
(r/'evidence/accounting-audit16.json').write_text(json.dumps(out,ensure_ascii=False,indent=2));print(json.dumps(out,ensure_ascii=False))
with (r/'VERDICT.md').open('a') as f:
 f.write('\nHƯỚNG 11: không đếm skip là PASS; try/catch mới và argv native\n  giả thuyết : Ca chấp nhận mảng truthy, thiếu nền/dependency vẫn tính QUA hoặc pinned helper diễn sẵn kết quả.\n  lệnh       : python3 probes/test-accounting-round12.py; TL_TEST_PYTHON=python3 REVIEW_CASE_LOG=$PWD/evidence/cases16.jsonl pwsh/pwsh -NoProfile -File copies/accounting/ops/vm/cap-nhat-cong-cu_test.ps1 > evidence/accounting16.log 2>&1; pwsh/pwsh -NoProfile -File probes/inventory.ps1 > evidence/inventory16.json; pwsh/pwsh -NoProfile -File probes/icacls-round15.ps1 > evidence/icacls16.json; python3 probes/accounting-audit16.py\n  output     : 115/115/rc0; 115tên duy nhất, tất cả System.Boolean true; AST119tên duy nhất; 4ca Windows không đăng ký trên Linux: '+', '.join(missing)+'. icacls fixture5/5: argv roundtrip cả4lần, rc0 không ném, rc1/5 ném, rc1332 cấu hình bị POSIX thu thành52 vẫn ném; mất binary tuyệt đối cũng ném. Diff sản phẩm c489c72..head chỉ thêm2dòng guard/comment, không thêm try/catch.\n  kết luận   : KHÔNG PHẢI LỖI trong phép đo. Nhánh Windows admin không đo mã3 trả false; các nhánh chỉ chạy trên Linux không được đếm trên Windows. Pinned helper chỉ thay HTTP+execute bit Linux; version/hash/archive/copy thực, control đòi native2.0.0/rc0/download1, 2negative đòi loi. Getter/caller không bị giả. Không tính4ca vắng vào115ca và không dùng rc1332 cấu hình làm kết quả native Windows.\n')
