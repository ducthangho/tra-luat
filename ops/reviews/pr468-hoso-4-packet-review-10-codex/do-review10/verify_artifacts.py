from pathlib import Path
import json,hashlib,subprocess,yaml
R=Path(__file__).resolve().parents[1];T=R/'cay-kho';O=R/'do-review10'
sha=lambda b:hashlib.sha256(b).hexdigest()
p8=T/'ops/reviews/pr468-hoso-4-packet-review-8-codex';p9=T/'ops/reviews/pr468-hoso-4-packet-review-9-codex';repair=p9/'artifact-repair'
report={'repair_existing':[],'repair_missing':[],'command_metadata':[]}
for line_no,line in enumerate((repair/'ARTIFACTS.sha256').read_text().splitlines(),1):
    h,rel=line.split(maxsplit=1);rel=rel.lstrip('*');f=repair/rel;s=p8/rel
    row={'line':line_no,'path':rel,'expected':h,'source':str(s.relative_to(T)),'source_matches':s.is_file() and sha(s.read_bytes())==h}
    if f.is_file():row.update(actual=sha(f.read_bytes()),identical_to_round8=f.read_bytes()==s.read_bytes());report['repair_existing'].append(row)
    else:report['repair_missing'].append(row)
for p in p9.rglob('*.json'):
    d=json.loads(p.read_text())
    if not isinstance(d,dict) or not ('stdout_sha256' in d or 'stdout_bytes' in d):continue
    row={'metadata':str(p.relative_to(T)),'rc_recorded':d.get('rc'),'utc':d.get('utc',d.get('start_utc')),'streams':[]}
    for stream in ['stdout','stderr']:
        f=p.with_suffix('.'+stream)
        if f.is_file():
            b=f.read_bytes();row['streams'].append({'name':stream,'bytes':len(b),'sha256':sha(b),'bytes_match':d.get(stream+'_bytes',len(b))==len(b),'hash_match':d.get(stream+'_sha256',sha(b))==sha(b)})
        else:row['streams'].append({'name':stream,'unavailable':True})
    report['command_metadata'].append(row)
receipt=T/'ops/reviews/pr468-hoso-4-packet-review-9-codex-verdict.receipt.yaml';d=yaml.safe_load(receipt.read_text());f=T/d['verdict_path'];raw=f.read_bytes()
report['receipt9']={'bytes':len(raw),'hash':sha(raw),'declared_bytes':d['verdict_bytes'],'declared_hash':d['verdict_sha256'],'bytes_and_hash_match':len(raw)==d['verdict_bytes'] and sha(raw)==d['verdict_sha256'],'reviewed_sha':d['reviewed_sha'],'equals_delivered_verdict':raw==(R/'VERDICT-luot9.md').read_bytes()}
report['repair_claims']=json.loads((p9/'artifact-checks.json').read_text())
report['p9_final']=json.loads((p9/'final-check.json').read_text())
report['ref_extra_tip']=subprocess.check_output(['git','--git-dir='+str(R/'kho.git'),'log','-1','--format=%H %cI %s','refs/heads/ops/lease-wp461-g2'],text=True).strip()
report['metadata_failure']=[r for r in report['command_metadata'] if any(not s.get('bytes_match',True) or not s.get('hash_match',True) for s in r['streams'])]
(O/'artifacts.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'repair_existing':len(report['repair_existing']),'repair_existing_identical':sum(r['identical_to_round8'] for r in report['repair_existing']),'repair_missing':len(report['repair_missing']),'all_19_recoverable':all(r['source_matches'] for r in report['repair_missing']),'metadata_checked':len(report['command_metadata']),'metadata_failure':report['metadata_failure'],'receipt9':report['receipt9'],'ref_extra_tip':report['ref_extra_tip']},ensure_ascii=False,indent=2))
