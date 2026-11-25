from pathlib import Path
import importlib.util, sys, ast, json
W=Path(__file__).resolve().parent.parent;R=W/'cay-kho';sys.dont_write_bytecode=True
sys.path.insert(0,str(R/'ops'));sys.path.insert(0,str(R/'.claude/dev'));import ci_duong_nhanh as c
paths=['docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md','docs/PROTOCOL_DA_PHIEN.md','.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py']
for p in paths:print('CI_PR',p,c.phan_loai_packet_loop('pull_request',[p]))
print('CI_PUSH',c.phan_loai_packet_loop('push',paths))
s=(R/'.claude/dev/packet_loop.py').read_text();node=next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='_verify_lease_ref');f=ast.get_source_segment(s,node)
print('I2_CLOSURE_READER',any(x in f for x in ('change-impact','write_closure','change_policy_sha')))
print('I2_PUBLISHED_LEASE_DEPENDENCIES',{x:x in f for x in ('ls-remote','lease_path','BOT_LEASE','I2(R)','effective_write_set')})
print('POLICY_EXISTS',(R/'.github/coordination/change-impact.v1.json').exists())
# Đọc hàm thuần, không gọi record-lease/network.
sp=importlib.util.spec_from_file_location('pl',R/'.claude/dev/packet_loop.py');m=importlib.util.module_from_spec(sp);sys.modules['pl']=m;sp.loader.exec_module(m)
print('PREFIX_OVERLAP',m._giao('docs/','docs/a.md'))
print('CASE_OVERLAP',m._giao('DOCS/A.md','docs/a.md'))
print('NFC_OVERLAP',m._giao('docs/é.md','docs/e\u0301.md'))
print('RAW_POLICY_EXAMPLE_OVERLAP',m._giao('SKILL.md','references/GOTCHAS.md'))
print('SPEC_1460_WRITESET','.github/workflows/ci-dot-bien-du.yml, .claude/dev/ci_dang_ky_test.py, 2 hop_dong files; no literal overlap wp1466')
print('SPEC_B4_WRITESET','.claude/dev/packet_loop.py, .claude/dev/packet_loop_test.py; wait predecessor merged')
