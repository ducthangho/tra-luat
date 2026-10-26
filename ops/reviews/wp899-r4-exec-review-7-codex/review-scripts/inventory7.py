from pathlib import Path
import json,collections,hashlib
R=Path(__file__).resolve().parent
producers=['mutants/results.json','historical-targets6/results.json','operators6-combined.json','operator-errors6-results.json','normalization6-results.json','frontier5/results.json','frontier6/results.json','frontier6-extra/results.json','frontier6-extra2/results.json','frontier6-extra3/results.json','frontier7/results.json','frontier7b/results.json','reanchored6-results.json','signature6-results.json']
producers += [str(p.relative_to(R)) for p in sorted(R.glob('prior*/old*/extra-mutants/results.json'))]
proof={}
for f in ['proof7-results.json','proof-repairs7-results.json']:
 for z in json.loads((R/f).read_text()):proof[z['name']]=z
notes={
 'name_uses_whole_value':('P3 / D02','uses nhiều dòng: chưa có chính sách cho action reference malformed; cần owner chốt so toàn giá trị hoặc từ chối, chưa có runner evidence'),
 'mode_prior_strip_empty_run':('P3 / tương đương','Thay str(v) bằng str(v or "") chỉ đổi các giá trị falsy; không giá trị nào trong miền yaml.safe_load ấy chứa GITHUB_ENV/PATH.'),
 'log_header_full_timestamp_required':('P3 / tương đương ở đầu ra công khai','Header không có RE_DONG hợp lệ không thể có giờ hợp lệ cho M12(c); hai đường đều không ghép/sinh marker.'),
 'env_only_keys_str':('P3 / tương đương','Khoá scalar safe YAML không phải str không có tiền tố CI_DANG_KY_; không ép giết.'),
 'log_nested_after_only':('P3 / tương đương','Cấu trúc trước shell đã từ chối nhóm lồng, sau shell hai predicate giống nhau; equivalence.json.'),
 'nested_only_after_shell':('P3 / tương đương','Cùng predicate log_nested_after_only; không đếm thành lớp mới.'),
}
rows=[];summary={}
for f in producers:
 p=R/f
 if not p.exists():raise FileNotFoundError(p)
 a=json.loads(p.read_text());assert isinstance(a,list),f
 summary[f]=dict(collections.Counter(z.get('rank',z.get('status','?')) for z in a))
 for z in a:
  n=z.get('name','?');rank=z.get('rank',z.get('status','?'));target=z.get('case') or z.get('target') or ', '.join(z.get('killed',[]))
  if rank=='CHECK_OUTPUT':
   ks=[c['case'] for c in z['cases'] if c['rc']==3 and c['output'].startswith('DO:'+c['case']+':')]
   bad=[c for c in z['cases'] if c['rc'] and not(c['rc']==3 and c['output'].startswith('DO:'+c['case']+':'))]
   rank='GIET+NEM' if ks and bad else 'GIET' if ks else 'TIN_DUNG_GIA' if bad else 'SONG_SOT';target=', '.join(ks)
   assert all(rc==0 for c,rc,o in json.loads((R/'frontier7/baseline.json').read_text()))
  if not target and (z.get('cases') or z.get('mutant',{}).get('cases')):
   cs=z.get('cases') or z['mutant']['cases'];target=str(len(cs))+' ca; xem JSON'
  if not target and z.get('pair'):
   cc=z['pair'][-1].get('case');target=cc[0] if isinstance(cc,list) else ''
  finding='không mở finding' if rank in ('GIET','GIET+NEM','GIET_DUNG_CA') else 'lỗi dựng phép đo; không nhận tín dụng' if rank in ('HONG_NEO','HONG_BASE','HONG') else 'ngoại lệ vô can; không nhận tín dụng' if rank=='TIN_DUNG_GIA' else 'cần xem ledger'
  detail=''
  if f.startswith(('frontier7/','frontier7b/')) and rank=='SONG_SOT':
   if n in notes:finding,detail=notes[n]
   else:
    assert proof[n]['rank']=='PROVEN',(n,proof.get(n));finding='P1 / F10';detail='50/50 ca xanh; phản chứng HEAD0 → mutant3 đúng TinHieuChotCa; '+('proof-repairs7-results.json' if n in ('job_suffix_no_dot_pure','name_run_strip_cr') else 'proof7-results.json')
  elif n in notes and rank in ('SONG_SOT','SONG'):finding,detail=notes[n]
  if f=='mutants/results.json' and z.get('expected')!='GIET':finding='tự kiểm có chủ ý: '+str(z.get('expected'))
  if f=='operator-errors6-results.json':detail='chỉ đo lại các cặp lỗi đã liệt kê trong kq8.txt; không phải quét mọi ca'
  rows.append({'producer':f,'name':n,'rank':rank,'target':target,'finding':finding,'detail':detail,'old':z.get('old'),'new':z.get('new')})
summary={f:dict(collections.Counter(z['rank'] for z in rows if z['producer']==f)) for f in producers}
(R/'inventory7.json').write_text(json.dumps({'summary':summary,'rows':rows},ensure_ascii=False,indent=2))
def cell(v):return str(v or '').replace('|','\\|').replace('\n','<br>')
md=['# Danh mục đột biến — wp899 r4 lượt 7','', 'Kết quả GIET chỉ nói phép đo được liệt kê. GIET+NEM có ít nhất một tín hiệu đúng và ngoại lệ ngoài ca đích; không nhận ngoại lệ làm tín dụng. Bản sao nguồn/neo/thay, command, rc, output và phạm vi đầy đủ trong JSON producer. Các producer trùng neo/thay là lần đo lặp, không cộng thành mutant độc lập.','', '| producer | số mục / phân hạng |','|---|---|']
md += ['| '+cell(k)+' | '+cell(v)+' |' for k,v in summary.items()]
md += ['', '| producer | mutant | kết quả | ca đích / phạm vi | hạng finding / quyết định |','|---|---|---|---|---|']
md += ['| '+' | '.join(cell(x) for x in (z['producer'],z['name'],z['rank'],z['target'],z['finding']+'; '+z['detail']))+' |' for z in rows]
(R/'MUTANTS.md').write_text('\n'.join(md)+'\n');print(json.dumps(summary,ensure_ascii=False,indent=2));print('rows',len(rows))
