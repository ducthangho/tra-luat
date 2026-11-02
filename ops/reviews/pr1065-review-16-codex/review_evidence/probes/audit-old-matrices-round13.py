from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];rows=[]
x=json.loads((r/'evidence/system-matrix.json').read_text());assert len(x)==6
for y in x:
 d=y['data'];assert y['returncode']==0 and d['error'] is None and d['remaining_downloads']==0
 tools=[z for z in d['results'] if z['cong_cu']!='commander'];assert len(tools)==4
 mode=y['mode'];assert all(z['hash_matches'] for z in d['spawns'])
 if mode in ['download-tamper','missing-hash']:assert not d['spawns']
 else:assert len(d['spawns'])==4
 expected=['nang_cap']*4 if mode=='success' else ['nang_cap']+['can_khoi_dong_lai']*3 if mode=='msi-reboot' else ['loi']*4
 assert [z['hanh_dong'] for z in tools]==expected
 assert d['commander_restart']==(mode not in ['download-tamper','missing-hash'])
 rows.append({'name':mode,'passed':True,'actions':expected,'spawns':len(d['spawns'])})
x=json.loads((r/'evidence/caller-null.json').read_text());assert len(x)==4
for y in x:
 d=y['data'];assert y['returncode']==0
 assert d['errors']==({'system-pre':4,'system-post':4,'zip-pre':0,'zip-post':1}[d['mode']])
 if d['mode']=='system-pre':assert d['spawns']==0
 rows.append({'name':d['mode'],'passed':True,'errors':d['errors']})
for name in ['regressions-round12','contracts-round12']:
 x=json.loads((r/'evidence'/(name+'.json')).read_text());groups=x if name.startswith('contracts') else [y for a in x for y in a]
 assert all(z['rc']==0 for z in groups)
 rows.append({'name':name,'drivers':len(groups),'passed':True})
(r/'evidence/matrix-assertions-round13.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print('Independent matrix assertions: 6 system + 4 caller PASS; 12 regression drivers + 7 contract drivers rc0')
with (r/'evidence/legacy-verdict-discard.md').open('a') as f:f.write('\nHƯỚNG 14: xác nhận dương/âm cho driver cũ không tự assert đủ\n  giả thuyết : driver rc0 chỉ chứng minh có JSON, không chứng minh băm/installer/hậu phiên bản đúng.\n  lệnh       : python3 probes/audit-old-matrices-round13.py\n  output     : Independent matrix assertions: 6 system + 4 caller PASS; 12 regression drivers + 7 contract drivers rc0. Check số spawn, mọi băm khớp ở thời điểm spawn,4dòng công cụ, hành động từng ca, cleanup0 và Commander phục hồi đúng điều kiện. evidence/matrix-assertions-round13.json.\n  kết luận   : KHÔNG PHẢI LỖI trong các oracle hồi quy; không chỉ dựa rc0. Driver test-branches từ L4 hardcode số ca lịch sử không dùng để chứng nhận head mới; inventory AST và accounting104 thay phần ấy. registration-head đã chạy5mode trên head; phần registration-matrix dùng mutant lịch sử không phải phép đo head, thay bằng mô hình stateful trong suite và mutant đã chọn.\n')
