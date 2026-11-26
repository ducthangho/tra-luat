from pathlib import Path
import json,re,collections,hashlib
w=Path(__file__).resolve().parent
def read(n):return json.loads((w/n).read_text())
summary={}
if (w/'table/bang.json').exists():
 our=read('table/bang.json');their=json.loads((w.parent/'bang_chung/bang-toan-tu/bang.json').read_text());fields=['ket_luan','hang','ca','rc']
 ours={(x['id'],x['op']):x for x in our['o']};theirs={(x['id'],x['op']):x for x in their['o']};diff=[]
 for k in set(ours)|set(theirs):
  if k not in ours or k not in theirs:diff.append({'id':k,'missing':True})
  else:
   d={f:[theirs[k][f],ours[k][f]] for f in fields if theirs[k][f]!=ours[k][f]}
   if d:diff.append({'id':k,'differences':d})
 summary['table']={'counts':our['dem'],'cells':len(ours),'matches':len(ours)-len(diff),'differences':diff,'baseline':our['nen'],'nested_error_kills':[{'id':x['id'],'op':x['op'],'dong':x['dong']} for x in our['o'] if 'rc=4' in x['dong'] or 'HONG:' in x['dong']]}
if (w/'trace-v2.json').exists():
 tr=read('trace-v2.json');groups=collections.defaultdict(list)
 for x in tr['calls']:
  if x['case']!=x['outer']:groups[x['outer']].append(x)
 summary['trace']={k:{'calls':len(v),'rc':dict(collections.Counter(x['rc'] for x in v)),'valid_DO':all(x['output'].startswith('DO:'+x['case']+':') for x in v if x['rc']==3)} for k,v in groups.items()}
 summary['c39_line_events']=dict(collections.Counter(x['iterations'] for x in tr['c39_loops']))
 summary['loops']=dict(collections.Counter(x['actual_counter_calls'] for x in tr['c39_loops']))
if (w/'cache-review.json').exists():
 a=read('cache-review.json');summary['cache']={'modes':[{k:x[k] for k in ['mode','c36','c40','cache_size']} for x in a]}
 if len(a)==2:summary['cache'].update(identical_calls=a[0]['calls']==a[1]['calls'],identical_A_results=a[0]['a_calls']==a[1]['a_calls'],inputs=sum(len(x['inputs']) for x in a[0]['calls'] if x['case'].startswith('c36')))
if (w/'a136-cache.json').exists():
 a=read('a136-cache.json');summary['a136_cache_equal']=len(a)==2 and a[0]['calls']==a[1]['calls']
for side in ['base','head']:
 f=w/(side+'-selftest.log')
 if f.exists():
  t=f.read_text();summary[side+'_selftest']={'totals':re.findall(r'== tl selftest.*',t),'failed_lines':[x for x in t.splitlines() if re.search(r'FAIL|✗|❌|\[DO\]',x)]}
if (w/'independent.json').exists():summary['independent']=[{k:x.get(k) for k in ['id','rc','classification']} for x in read('independent.json')]
(w/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2));print(json.dumps(summary,ensure_ascii=False,indent=2))
