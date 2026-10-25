import pathlib,json,re,datetime,collections
R=pathlib.Path('.review');root=pathlib.Path.cwd();out={}
def ts(v):return datetime.datetime.fromisoformat(v.replace('Z','+00:00'))
for rid in (39342960764,40074551995):
 jobs=json.loads((root/f'.review-input/a10/out-{rid}/jobs.json').read_text())['jobs'];counts=collections.Counter()
 for j in jobs:
  rest=[s for s in sorted(j['steps'],key=lambda s:s['number']) if s['name'] not in ('Set up job','Complete job') and not s['name'].startswith('Post ') and s['conclusion']!='skipped']
  heads=[re.match(r'^(\S+) ##\[group\]Run (.*)$',l).groups() for l in (root/f'.review-input/log-that/{rid}/{j["id"]}.log').read_text().splitlines() if re.match(r'^(\S+) ##\[group\]Run (.*)$',l)]
  for raw,_ in heads:
   for kind,time in [('raw',ts(raw)),('floor',ts(raw).replace(microsecond=0))]:
    n=sum(ts(s['started_at'])<=time<=ts(s['completed_at']) for s in rest);counts[kind+'_unique']+=n==1;counts[kind+'_zero']+=n==0
 out[rid]=dict(counts)
(R/'q1-time-details.json').write_text(json.dumps(out,indent=2));print(out)
