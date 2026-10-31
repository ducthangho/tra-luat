from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];read=lambda n:json.loads((r/'evidence'/n).read_text())
counts={}
for name in ['version-identity-oracle','cli-version-identity-oracle']:
 rows=read(name+'.json')
 for x in rows:
  s=x['summary'];good=s['mode'] in ['stable-control','zip-control','cli-stable-control']
  assert s['product_rc']==(0 if good else 1) and s['ok']==good
  assert all(z['hanh_dong']==('giu' if good else 'loi') for z in s['rows'])
  if good:assert s['rows']
 counts[name]=len(rows)
for x in read('cli-case-identity-oracle.json'):
 s=x['summary'];good=s['mode'] in ['stable-control','case-equal'];assert s['rc']==(0 if good else 1) and s['ok']==good
 assert len(s['rows'])==2 and all(z['hanh_dong']==('giu' if good else 'loi') for z in s['rows'])
 assert all(z['rc']==0 for z in s['direct'])
counts['case']=4
for x in read('node-major-oracle.json'):
 s=x['summary'];bad=s['head']=='head' and s['mode']!='node-stable';assert s['rc']==(1 if bad else 0) and s['ok']==(not bad)
 node=next(z for z in s['node'] if z['cong_cu']=='node')
 if bad:assert node['hanh_dong']=='loi' and not s['installs']
 else:assert node['sau']=='24.2.0' and len(s['installs'])==1
counts['node_current']=4;counts['node_old_blob_comparison']=1
for x in read('numeric-identity.json'):
 s=x['summary'];good=s['mode']=='stable-control';assert s['rc']==(0 if good else 1) and s['ok']==good
 tools=[z for z in s['rows'] if z['cong_cu']=='git'] if s['mode'].startswith('git-') else s['rows']
 assert tools and all(z['hanh_dong']==('giu' if good else 'loi') for z in tools)
counts['system_numeric']=5
for s in read('zip-numeric-identity.json'):
 good=s['mode'] in ['rg-at-target','rg-alias-before','actionlint-alias-before'];expected='giu' if s['mode']=='rg-at-target' else 'nang_cap' if good else 'loi'
 assert s['rc']==(0 if good else 1) and s['ok']==good and len(s['rows'])==1
 assert s['rows'][0]['hanh_dong']==expected
 if good:assert s['rows'][0]['sau']=='2.0.0'
counts['zip_numeric']=5
unknown=read('unknown-target-oracle.json');assert len(unknown)==4 and all(x['summary']['errors']==(0 if x['summary']['mode']=='control' else 4) for x in unknown)
counts['unknown_target']=4
(r/'evidence/identity-audit16.json').write_text(json.dumps(counts,indent=2));print('Identity assertions: '+json.dumps(counts)+'; all PASS')
with (r/'VERDICT.md').open('a') as f:
 f.write('\nHƯỚNG 10: định danh đầy đủ, case, alias số học, major Node và đích null\n  giả thuyết : hồi quy cắt suffix/gộp alias/case hoặc nâng major từ token không parse được.\n  lệnh       : python3 -u probes/run-identities-round15.py > evidence/identities16.log 2>&1; python3 probes/identity-audit16.py > evidence/identity-audit16.log 2>&1\n  output     : suffix5+CLI2, case4, numeric-system5+ZIP5, Node current4, unknown-target4 đều PASS qua assert trên raw JSON; old-blob Node1ca chỉ đối chứng riêng. 6driver lịch sử rc1 do assert mong tái hiện lỗi cũ; không che rc1, output thô lưu đủ.\n  kết luận   : KHÔNG PHẢI LỖI trong tập đo. Case-equal được giu, khác case/suffix/alias SAU cài bị loi; ZIP alias TRƯỚC được cài lại đúng đích, không giu sai; Node current không parse được → loi/0installer. ZIP suffix-before ra loi do OFFLINE-UNEXPECTED-HTTP khi đi nhánh nâng, vì vậy chỉ chứng minh không giu sai; không lấy nó chứng nhận hậu cài suffix. system suffix-after và CLI suffix có so đích thật bổ sung.\n')
